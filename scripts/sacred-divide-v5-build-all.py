#!/usr/bin/env python3
"""Rebuild the v5 PDF for every volume (or the ids given), run the checks, and write one report.
For each volume: build (3 layout passes) -> sacred-divide-v5-qa (type sizes, palette, fonts) -> veraPDF PDF/UA-1 -> page metrics.
Report: docs/sacred-divide-v5/PDF-BUILD-REPORT.md. Usage: sacred-divide-v5-build-all.py [id ...]"""
import glob, json, os, re, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
PDFDIR = os.path.join(ROOT, 'library/_undeployed/sacred-divide-v5')
RELIG = os.path.join(ROOT, 'content/sacred-divide/religions')
VERAPDF = (glob.glob('/tmp/claude-0/-home-user/*/scratchpad/src/verapdf/verapdf') + [''])[0]
ids = sys.argv[1:] or sorted(f[:-3] for f in os.listdir(RELIG) if f.endswith('.md') and not f.startswith('_') and f != 'README.md')
rows = []
for rid in ids:
    t0 = time.time()
    r = subprocess.run([sys.executable, os.path.join(HERE, 'sacred-divide-v5-build.py'), rid], capture_output=True, text=True)
    pdf = os.path.join(PDFDIR, f'{rid}-expanded.pdf'); pj = pdf.replace('.pdf', '.pages.json')
    if r.returncode or not os.path.exists(pdf):
        rows.append({'id': rid, 'ok': False, 'err': (r.stderr or r.stdout)[-300:]}); print(rid, 'BUILD FAILED', flush=True); continue
    pages = json.load(open(pj))
    light = [p for p in pages if not p.get('dark') and p.get('foot', 0) > 0.15]
    nearly_blank = [p['n'] for p in pages if not p.get('dark') and p.get('foot', 0) > 0.85]
    qa = subprocess.run([sys.executable, os.path.join(HERE, 'sacred-divide-v5-qa.py'), pdf], capture_output=True, text=True).stdout
    off = re.search(r'outside the 7-step scale.*?: (.*)', qa); pal = re.search(r'outside the 5-value palette: (.*)', qa)
    ua = ''
    if VERAPDF:
        v = subprocess.run([VERAPDF, '--flavour', 'ua1', pdf], capture_output=True, text=True, timeout=600).stdout
        ua = 'pass' if 'isCompliant="true"' in v else 'FAIL'
    rows.append({'id': rid, 'ok': True, 'pages': len(pages), 'empty15': len(light), 'blank': nearly_blank, 'size_ok': (off.group(1).strip() == 'none') if off else None,
                 'palette_ok': (pal.group(1).strip() == 'none') if pal else None, 'ua': ua, 'kb': os.path.getsize(pdf) // 1024, 's': round(time.time() - t0)})
    print(rid, rows[-1]['pages'], 'pages', rows[-1]['empty15'], '>15% empty', 'UA', ua, f"{rows[-1]['s']}s", flush=True)

out = ['# PDF build report', '', f'Built {time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())}. Pages with a foot more than 15% empty are layout slack the design pass will reduce; "nearly blank" pages (more than 85% empty) are listed by number.', '',
       '| Volume | Pages | Pages >15% empty | Nearly blank pages | Type sizes in scale | Palette | PDF/UA-1 | KB |', '|---|---|---|---|---|---|---|---|']
for r in rows:
    if not r['ok']: out.append(f"| {r['id']} | BUILD FAILED: {r['err']!r} | | | | | | |"); continue
    out.append(f"| {r['id']} | {r['pages']} | {r['empty15']} | {', '.join(map(str, r['blank'])) or 'none'} | {'yes' if r['size_ok'] else 'NO'} | {'yes' if r['palette_ok'] else 'NO'} | {r['ua']} | {r['kb']} |")
open(os.path.join(ROOT, 'docs/sacred-divide-v5/PDF-BUILD-REPORT.md'), 'w').write('\n'.join(out) + '\n')
print('report written')

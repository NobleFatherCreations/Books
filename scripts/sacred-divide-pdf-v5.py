#!/usr/bin/env python3
"""The Sacred Divide v5 — redesigned print edition (US Letter). One stylesheet (tools/pdf/sacred-divide-v5.css),
a per-volume theme, and the same build_sections() the site uses, so the text is identical to v4 except where
the wording log records a proposed edit.

Usage: python3 scripts/sacred-divide-pdf-v5.py catholicism
Output: library/_undeployed/sacred-divide-v5/<id>.pdf
"""
import importlib.util, math, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
spec = importlib.util.spec_from_file_location('ex', os.path.join(HERE, 'sacred-divide-pdf-expanded.py'))
ex = importlib.util.module_from_spec(spec); spec.loader.exec_module(ex)
e = ex.e
ex.OUTDIR = os.path.join(ROOT, 'library/_undeployed/sacred-divide-v5')

# ---- proposed wording (mockup only): Loop 2 for Catholicism, built ONLY from techniques 5, 8, 20, 21 in the same volume.
LOOPS = {
 ('catholicism', 2): {
  'steps': [
   'Sin and confession are installed in childhood. Children are bonded early through fear of sin, reverence for priests and sacramental dependency, before they can weigh the teaching.',
   'The conscience is kept under permanent examination. Sexual teaching makes ordinary desire evidence of spiritual disorder, so there is always something to confess.',
   'Absolution runs through one route. Grave sin is taught to sever a person from grace, and the only authorized way back is confession to an ordained man, then penance.',
   'Relief arrives and wears off. The peace is real, and by Friday the anxiety has returned; the guilt, relief and returning guilt keep the penitent in weekly orbit.',
   'The debt regenerates. The institution is both the source of the shame and the distributor of mercy, so each act of relief renews the need for the next one.'],
  'feeds': [(5, 'Devaluation'), (8, 'Intermittent Reinforcement'), (20, 'Trauma Bonding'), (21, 'Learned Helplessness')],
  'closes': 'A repeating pattern would end when the penitent stopped. This one closes because the only relief on offer comes from the office that defines the debt. Devaluation creates the need, Intermittent Reinforcement meters the relief, Trauma Bonding ties the relief to the source of the wound, and Learned Helplessness teaches the penitent to endure rather than leave.',
  'breaks': 'The loop needs all four parts. It weakens wherever one is removed: where forgiveness can be sought from a source other than the office that names the sin (the person), or where the institution stops treating frequency of confession as the measure of devotion (the institution). This paragraph is analysis, not a documented finding.',
  'example': 'The volume’s own example is the scrupulous Catholic who finds confession relieving one week and anxious again by Friday.',
 }}

def wrap(text, n=12):
    lines, cur = [], ''
    for w in text.split():
        if cur and len(cur) + 1 + len(w) > n: lines.append(cur); cur = w
        else: cur = (cur + ' ' + w).strip()
    return lines + [cur]

def loop_svg(n, title):
    parts = [p.strip() for p in title.split(' to ')]
    if len(parts) > 1 and parts[0].lower() == parts[-1].lower(): parts = parts[:-1]
    k = len(parts); W, H, cx, cy, rx, ry = 260, 214, 130, 107, 80, 68
    pos = [(cx + rx * math.sin(2 * math.pi * i / k), cy - ry * math.cos(2 * math.pi * i / k)) for i in range(k)]
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="lt{n} ld{n}"><title id="lt{n}">Loop {n}: {e(title)}</title>'
           f'<desc id="ld{n}">A cycle of {k} steps in order: {e(", then ".join(parts))}, and back to the start.</desc>'
           '<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#7E1F2B"/></marker></defs>']
    for i in range(k):  # arrows along the ellipse, clear of the pills
        a0, a1 = 2 * math.pi * i / k, 2 * math.pi * (i + 1) / k; d = 0.42 if k > 2 else 0.6
        s0, s1 = a0 + d, a1 - d
        p0 = (cx + rx * math.sin(s0), cy - ry * math.cos(s0)); p1 = (cx + rx * math.sin(s1), cy - ry * math.cos(s1))
        out.append(f'<path d="M{p0[0]:.1f} {p0[1]:.1f} A{rx} {ry} 0 0 1 {p1[0]:.1f} {p1[1]:.1f}" fill="none" stroke="#7E1F2B" stroke-width="1.4" marker-end="url(#ah)"/>')
    for i, (x, y) in enumerate(pos):
        lines = wrap(parts[i], 11); h = 15 * len(lines) + 12; w = 80
        out.append(f'<rect x="{x-w/2:.1f}" y="{y-h/2:.1f}" width="{w}" height="{h}" fill="#FBF8F1" stroke="#7E1F2B" stroke-width="1"/>')
        for j, ln in enumerate(lines):
            out.append(f'<text x="{x:.1f}" y="{y-h/2+19+15*j:.1f}" text-anchor="middle" font-size="11.5" fill="#1D1915">{e(ln)}</text>')
        out.append(f'<circle cx="{x-w/2:.1f}" cy="{y-h/2:.1f}" r="8" fill="#7E1F2B"/><text x="{x-w/2:.1f}" y="{y-h/2+3.5:.1f}" text-anchor="middle" font-size="10" fill="#fff">{i+1}</text>')
    out.append(f'<text x="{cx}" y="{cy-2}" text-anchor="middle" font-size="8" letter-spacing="2" fill="#8C6F2A">LOOP</text><text x="{cx}" y="{cy+22}" text-anchor="middle" font-size="26" fill="#7E1F2B" style="font-family:EB Garamond,serif">{n}</text></svg>')
    return ''.join(out)

def loops_html(rid, h):
    def one(m):
        n, title, text = int(m.group(1)), m.group(2), m.group(3)
        x = LOOPS.get((rid, n)); svg = loop_svg(n, title)
        if not x:
            return f'<div class="loop"><h4>{n} · {title}</h4><div class="row">{svg}<div><p>{text}</p></div></div></div>'
        steps = ''.join(f'<li>{e(s)}</li>' for s in x['steps'])
        feeds = ', '.join(f'<a class="tlink" href="#t-{t}">{t} · {e(nm)}</a>' for t, nm in x['feeds'])
        return (f'<div class="loop long"><h4>{n} · {title}</h4><span class="prop">Proposed expansion · pending review</span>'
                f'<div class="row">{svg}<div><p>{text}</p><p class="feeds"><b>Techniques that feed it</b>{feeds}</p></div></div>'
                f'<h4>How it runs</h4><ol class="steps">{steps}</ol><h4>Why it closes</h4><p>{e(x["closes"])}</p>'
                f'<h4>Where it could be broken, and by whom</h4><p>{e(x["breaks"])}</p><h4>An example from this page</h4><p>{e(x["example"])}</p></div>')
    return re.sub(r'<div class="box card">\s*<h4>(\d+) · (.+?)</h4>\s*<p>(.*?)</p>\s*</div>', one, h, flags=re.S)

def tactics_html(h):
    def one(m):
        blk = m.group(0)
        g = re.search(r'<p><strong>Evidence grade\.</strong>(.*?)</p>', blk, re.S)
        if not g: return blk
        blk = blk.replace(g.group(0), '')
        note = '<p class="gradenote"><strong>Evidence grade</strong>' + g.group(1) + '</p>'
        return re.sub(r'(</h4>\s*<p><em>.*?</em></p>)', lambda k: k.group(1) + note, blk, count=1, flags=re.S)
    return re.sub(r'<div class="box tactic">.*?</div>', one, h, flags=re.S)

def rose(accent='#C9A45E'):
    petals = ''.join(f'<path transform="rotate({i*30} 100 100)" d="M100 100 C 86 78, 86 48, 100 30 C 114 48, 114 78, 100 100 Z" fill="none" stroke="{accent}" stroke-width=".9"/>' for i in range(12))
    rings = ''.join(f'<circle cx="100" cy="100" r="{r}" fill="none" stroke="{accent}" stroke-width=".8"/>' for r in (94, 70, 22))
    return f'<svg class="orn" viewBox="0 0 200 200" role="img" aria-label="Twelve-fold geometric ornament">{rings}{petals}<circle cx="100" cy="100" r="3" fill="{accent}"/></svg>'

def build_html(rid):
    secs_data, meta = ex.build_sections(rid); name = meta.get('title', rid)
    toc, secs = [], []
    for num, title, slug, h, subs in secs_data:
        if slug == 'loops': h = loops_html(rid, h)
        if slug == 'techniques': h = tactics_html(h)
        if slug == 'a-day-inside': h = re.sub(r'(<p><em>[^<]*</em></p>\s*<p)>', r'\1 class="dropcap">', h, count=1)
        h = re.sub(r'(<h[34][^>]*>(?:(?!</h[34]>).)*</h[34]>)\s*(<div class="box (?:case|card|tell|stage)"[^>]*>(?:(?!<div).)*?</div>)', r'<div class="keep">\1\2</div>', h, flags=re.S) if slug not in ('techniques', 'loops') else h
        h = re.sub(r'(<h[34][^>]*>(?:(?!</h[34]>).)*</h[34]>)\s*(<table(?![^>]*long)[^>]*>(?:(?!</table>).)*</table>)', lambda m: f'<div class="keep">{m.group(1)}{m.group(2)}</div>' if m.group(2).count('<tr>') <= 8 else m.group(0), h, flags=re.S)
        h = re.sub(r'<table class="short( wide)?">((?:(?!</table>).)*)</table>', lambda m: ('<table class="long">' if m.group(2).count('<tr>') > 6 else m.group(0)[:m.group(0).index('>')+1]) + m.group(2) + '</table>', h, flags=re.S)
        toc.append((num, title, slug, subs))
        im = re.match(r'\s*(<div class="box note-a intro">.*?</div>)', h, re.S)
        intro = im.group(1).replace('<div class="box note-a intro">', '<aside class="intro">', 1)[:-6] + '</aside>' if im else ''
        if im: h = h[im.end():]
        secs.append(f'<section class="sec" id="sec-{slug}"><header class="opener"><h2 id="{slug}"><span class="num">{int(num):02d}</span><span class="t">{e(title)}</span></h2>{intro}<div class="orn-rule"></div></header>{h}</section>')
    howto = ex.md_to_html(open(os.path.join(ex.SRC, '_how-to-read.md'), encoding='utf-8').read())
    def toc_item(num, title, slug, subs):
        sl = ''.join('<a href="#%s">%s</a>' % (s, re.sub(r'<[^>]+>', '', t)) for s, t in subs[:14])
        return (f'<li><a class="sec" href="#{slug}"><span class="n">{int(num):02d}</span><span class="t">{e(title)}</span><span class="dots"></span></a>' + (f'<div class="subs">{sl}</div>' if subs else '') + '</li>')
    lede = re.search(r'<div class="box lede">\s*<p>(.*?)</p>', secs[2] + secs[3], re.S)
    blurb = re.sub(r'<[^>]+>', '', lede.group(1)) if lede else ''
    if len(blurb) > 260: blurb = blurb[:257].rsplit(' ', 1)[0] + '…'
    cover = (f'<div class="cover"><div class="band"></div>{rose()}<div class="eyebrow">The Sacred Divide</div>'
             f'<div class="for">The full record · <b>with reader narration</b></div><h1>{e(name)}</h1><div class="family">{e(meta.get("family", ""))} family</div>'
             f'<div class="rule"></div><div class="tagline">Honor the faith · Name the machinery</div><div class="blurb">{e(blurb)}</div>'
             f'<div class="meta"><span>v5 draft · text checked {e(meta.get("checked", ""))}</span><span>{ex.SITE}</span></div></div>')
    preface = f'<div class="front preface"><h1 id="preface">How this edition works</h1>{ex.md_to_html(ex.PREFACE.replace("{name}", name))}</div>'
    doc = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{e(name)} — The Sacred Divide</title>
<meta name="author" content="Noble Father Creations"><meta name="subject" content="{e(name)}: the full record">
<link rel="stylesheet" href="sacred-divide-v5.css">
<script>
window.PagedConfig = {{ auto: true, before: () => {{
  const q = new URLSearchParams(location.search), list = k => (q.get(k) || '').split(',').filter(Boolean);
  list('snug').forEach(v => {{ const [id, lvl] = v.split(':'), s = document.getElementById(id); if (s) s.classList.add('snug' + (lvl === '1' ? '' : lvl)); }});
  const tables = document.querySelectorAll('table'); tables.forEach((t, i) => t.dataset.ti = i);
  list('brk').forEach(i => {{ const t = tables[+i]; if (!t) return; const p = t.previousElementSibling; (p && /^H[34]$/.test(p.tagName) ? p : t).classList.add('newpage'); }});
}}, after: () => {{ document.querySelectorAll('.pagedjs_margin, .pagedjs_margin-content').forEach(m => m.setAttribute('aria-hidden', 'true')); window.__paged = true; }} }};
</script><script src="paged.polyfill.js"></script></head><body>
{cover}{preface}<div class="front toc"><h1 id="contents">Contents</h1><ol>{"".join(toc_item(*t) for t in toc)}</ol></div><div class="front howto">{howto}</div>{"".join(secs)}</body></html>'''
    # heading levels must not skip (PDF/UA 7.4.2): promote a skipped h4 to the next legal level, keeping its h4 look
    last = [1]
    def lvl(m):
        n = int(m.group(1)); attrs = m.group(2) or ''
        if n > last[0] + 1:
            fixed = last[0] + 1; last[0] = fixed
            return f'<h{fixed}{attrs} class="look{n}">{m.group(3)}</h{fixed}>'
        last[0] = n; return m.group(0)
    doc = re.sub(r'<h([1-6])((?: [^>]*)?)>(.*?)</h\1>', lvl, doc, flags=re.S)
    doc = re.sub(r'<figure class="fig">(.*?)</figure>', lambda m: '<figure class="fig" role="img" aria-label="' + re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', m.group(1)))[:300].strip().replace('"', '') + '">' + m.group(1) + '</figure>', doc, flags=re.S)
    return doc, name, meta

def accessibility_pass(path, title):
    """Document-level PDF/UA hygiene: language, title display, XMP with the PDF/UA id, and a /Contents string on every link."""
    import pikepdf
    with pikepdf.open(path, allow_overwriting_input=True) as pdf:
        pdf.Root.Lang = pikepdf.String('en')
        pdf.Root.ViewerPreferences = pikepdf.Dictionary(DisplayDocTitle=True)
        with pdf.open_metadata(set_pikepdf_as_editor=False) as m:
            m['dc:title'] = title; m['dc:creator'] = ['Noble Father Creations']; m['dc:language'] = ['en']
            m['{http://www.aiim.org/pdfua/ns/id/}part'] = '1'
        n = 0
        for i, page in enumerate(pdf.pages):
            for a in page.get('/Annots', []):
                if a.get('/Subtype') != '/Link' or '/Contents' in a: continue
                act = a.get('/A')
                if act is not None and '/URI' in act: a.Contents = pikepdf.String('External link: ' + str(act.URI))
                else: a.Contents = pikepdf.String('Jump to a section or source on another page of this document')
                n += 1
        pdf.save(path)
    return n

ex.build_html = build_html
if __name__ == '__main__':
    for rid in [a for a in sys.argv[1:] if not a.startswith('--')]:
        out = ex.render(rid, '--html' in sys.argv)
        if out and not '--html' in sys.argv:
            print('links given a description:', accessibility_pass(out, f'{rid.replace("-", " ").title()} — The Sacred Divide'))
            import sacred_divide_pdfua as UA
            print('artifact blocks, list items restructured:', UA.run(out))

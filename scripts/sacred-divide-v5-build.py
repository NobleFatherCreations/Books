#!/usr/bin/env python3
"""Build a v5 PDF and run the whitespace pass: lay out, find light pages whose foot is more than 15% empty,
and drop the approved pullquote for that section at the page boundary (it grows to the page foot). Up to 3 layouts.
Usage: sacred-divide-v5-build.py catholicism"""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
rid = sys.argv[1]
pdf = os.path.join(ROOT, f'library/_undeployed/sacred-divide-v5/{rid}-expanded.pdf'); pj = pdf.replace('.pdf', '.pages.json')
pq = {}
for it in range(3):
    env = dict(os.environ, PQ_PLACE=json.dumps(pq), TAILFILL='0.3')
    subprocess.run([sys.executable, os.path.join(HERE, 'sacred-divide-pdf-v5.py'), rid], env=env, check=True, stdout=subprocess.DEVNULL)
    pages = json.load(open(pj))
    add = {}
    for i, p in enumerate(pages):
        if p.get('dark') or p.get('foot', 0) <= 0.15 or p.get('footPt', 0) < 260 or not p.get('sec') or p.get('pq'): continue
        slug = p['sec'][4:]
        if slug in pq or slug in add: continue
        nxt = pages[i + 1] if i + 1 < len(pages) else {}
        same = [b for b in nxt.get('blocks', []) if b['sec'] == p['sec'] and not b['split']]
        add[slug] = [same[0]['ci'] if same else -1, round(p['footPt']) - 14]
    fail = [(p['n'], round(p['foot'], 2)) for p in pages if not p.get('dark') and p.get('foot', 0) > 0.15]
    print(f'layout {it + 1}: {len(pages)} pages, {len(fail)} pages >15% empty, placing {len(add)} pullquotes', flush=True)
    if not add: break
    pq.update(add)
json.dump(pq, open(os.path.join(ROOT, f'library/_undeployed/sacred-divide-v5/{rid}.pq.json'), 'w'))
print('pullquotes placed:', pq)
print('remaining failing pages:', fail)

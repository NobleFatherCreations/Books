#!/usr/bin/env python3
"""Write library/_undeployed/sacred-divide-v5/manifest.json from the PDFs on disk (pages, bytes) and each volume's
front matter (title, family, version, checked). The site generator reads it for the Download button on each page.
Run after sacred-divide-v5-build-all.py. Usage: sacred-divide-v5-manifest.py"""
import json, os, re, sys
import pikepdf
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDFDIR = os.path.join(ROOT, 'library/_undeployed/sacred-divide-v5')
RELIG = os.path.join(ROOT, 'content/sacred-divide/religions')
out = {}
for f in sorted(os.listdir(RELIG)):
    if not f.endswith('.md') or f.startswith('_') or f == 'README.md':
        continue
    rid = f[:-3]
    fm = open(os.path.join(RELIG, f), encoding='utf-8').read().split('---')[1]
    get = lambda k: (re.search(rf'^{k}: "?(.*?)"?$', fm, re.M) or [None, ''])[1]
    pdf = os.path.join(PDFDIR, f'{rid}-expanded.pdf')
    with pikepdf.open(pdf) as p:
        pages = len(p.pages)
    out[rid] = {'title': get('title'), 'family': get('family'), 'file': f'{rid}-expanded.pdf', 'pages': pages,
                'bytes': os.path.getsize(pdf), 'version': get('version'), 'checked': get('checked')}
json.dump(out, open(os.path.join(PDFDIR, 'manifest.json'), 'w'), indent=1)
print(len(out), 'volumes,', sum(v['pages'] for v in out.values()), 'pages,', sum(v['bytes'] for v in out.values()) // 1048576, 'MB')

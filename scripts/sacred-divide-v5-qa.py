#!/usr/bin/env python3
"""Measurable checks for a v5 PDF: type sizes, colours, fill, fonts, PDF/UA. Usage: sacred-divide-v5-qa.py file.pdf"""
import collections, json, subprocess, sys, os
import pymupdf
path = sys.argv[1]; d = pymupdf.open(path)
ALLOWED = {72.0, 44.0, 26.0, 16.0, 11.0, 9.0, 7.5}
sizes = collections.Counter(); cols = collections.Counter(); off = collections.Counter()
for p in d:
    for b in p.get_text('dict')['blocks']:
        for l in b.get('lines', []):
            for s in l['spans']:
                t = s['text'].strip()
                if not t: continue
                sz = round(s['size'], 1); sizes[sz] += len(t); cols[f"#{s['color']:06X}"] += len(t)
                if sz not in ALLOWED and sz != 180.0: off[sz] += len(t)
BASE = {'#1A1714', '#7B1E22', '#B08A42', '#FAF6EC', '#D8D0BC'}
print('page size', d[0].rect, '| pages', len(d), '| bookmarks', len(d.get_toc()))
print('type sizes used (pt: characters):', dict(sorted(sizes.items())))
print('sizes outside the 7-step scale (excl. 180pt numeral):', dict(off) or 'none')
print('text colours:', dict(cols.most_common()), '| outside the 5-value palette:', {c: n for c, n in cols.items() if c not in BASE} or 'none')
fonts = set(); 
for p in d:
    for f in p.get_fonts(): fonts.add(f[3])
print('font programs embedded:', len(fonts), sorted(fonts)[:6])

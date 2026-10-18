#!/usr/bin/env python3
"""The Sacred Divide — audit pack: what a reader sees, as plain Markdown.

For each of the 34 traditions, writes the exported page (content/sacred-divide/religions/<id>.md) with the
reader narration placed exactly where the site and the PDF place it: a "Before you read" note opening each
of the 27 sections, a "Why this matters to you" caption closing it, and the section-23 hard questions
expanded into why-asked / example-on-this-page. Also writes the home page's text and a corpus index.

Usage: python3 scripts/sacred-divide-audit-pack.py <outdir>
"""
import html as H
import importlib.util
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import sacred_divide_narration as narr  # noqa: E402

RELIG = os.path.join(ROOT, 'content/sacred-divide/religions')
out = sys.argv[1]
os.makedirs(os.path.join(out, 'traditions'), exist_ok=True)


def quote(label, text):
    lines = text.strip().split('\n')
    return f'> **{label}** ' + lines[0] + ''.join('\n> ' + l for l in lines[1:]) + '\n'


def q_expand(content, ex):
    def one(m):
        n = int(m.group(1)); x = ex.get(n, {})
        extra = ''
        if x.get('why'):
            extra += f'\n   - *Why this is asked:* {x["why"]}'
        if x.get('example'):
            extra += f'\n   - *Example already on this page:* {x["example"]}'
        return m.group(0).rstrip('\n') + extra + '\n'
    return re.sub(r'^(\d+)\.\s.*?(?=^\d+\.\s|^### |\Z)', one, content, flags=re.M | re.S)


rows = []
for f in sorted(os.listdir(RELIG)):
    if not f.endswith('.md') or f.startswith('_') or f == 'README.md':
        continue
    rid = f[:-3]
    raw = open(os.path.join(RELIG, f), encoding='utf-8').read()
    parts = re.split(r'^(## (\d+)\. (.+?) \{#([\w-]+)\}\s*)$', raw, flags=re.M)
    res = parts[0]
    ex = narr.questions(rid)
    for i in range(1, len(parts), 5):
        head, num, title, slug, content = parts[i], parts[i + 1], parts[i + 2], parts[i + 3], parts[i + 4]
        intro, fy = narr.intro(rid, slug), narr.foryou(rid, slug)
        if slug == 'questions':
            content = q_expand(content, ex)
        res += head + '\n\n' + (quote(narr.INTRO_LABEL + '.', intro) + '\n' if intro else '') + content.strip('\n') + '\n\n' + (quote(narr.FORYOU_LABEL + '.', fy) if fy else '') + '\n'
    open(os.path.join(out, 'traditions', f), 'w', encoding='utf-8').write(res)
    rows.append((rid, len(res.split()), len(re.findall(r'^## \d+\.', res, re.M)), len(re.findall(r'\[\[(\w+)\]\]', res))))

# home page text
h = open(os.path.join(ROOT, 'library/faith/index.html'), encoding='utf-8').read()
h = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', h, flags=re.S)
h = re.sub(r'<svg.*?</svg>', '', h, flags=re.S)
h = re.sub(r'</(p|div|li|h\d|tr|section|aside|header|footer|nav|blockquote)>', '\n', h)
h = re.sub(r'</t[dh]>', ' | ', h)
h = re.sub(r'<[^>]+>', '', h)
h = H.unescape(h)
h = re.sub(r'[ \t]+', ' ', h); h = re.sub(r'\n\s*\n+', '\n\n', h).strip()
open(os.path.join(out, 'home-page-text.md'), 'w', encoding='utf-8').write('# Home page (https://noblefathercreations.com/faith), text as rendered\n\n' + h + '\n')
json.dump(rows, open(os.path.join(out, '.rows.json'), 'w'))
print(len(rows), 'traditions;', sum(r[1] for r in rows), 'words')

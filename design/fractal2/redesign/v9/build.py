#!/usr/bin/env python3
"""Fractal² intro v9: scenes. python3 design/fractal2/redesign/v9/build.py [BASE] -> index.html. Text+camera from content/fractal2/intro-v9.md"""
import os, re, json, html, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
BASE = sys.argv[1] if len(sys.argv) > 1 else '../v8/'  # art and fonts are unchanged since v8, so v9 reuses that asset folder
md = open(os.path.join(ROOT, 'content/fractal2/intro-v9.md'), encoding='utf-8').read()
def kv(s): return dict(re.findall(r'([a-z]+)=([^\s>]+)', s))
def mk(d, end):
    a = ''
    for k, v in d.items():
        x = v.split(':')[-1] if end else v.split(':')[0]
        a += f' data-{k}="{x}"'
    return f'<i class="mk{" end" if end else ""}"{a}></i>'
def wrap(text):
    out = []
    for tok in re.split(r'(\*\*[^*]+\*\*|\*[^*]+\*|\s+)', text):
        if not tok: continue
        if tok.isspace(): out.append(' '); continue
        b = tok.startswith('**'); i = (not b) and tok.startswith('*')
        inner = tok[2:-2] if b else tok[1:-1] if i else tok
        ws = ' '.join(f'<span class="w">{html.escape(w, quote=False)}</span>' for w in inner.split())
        out.append(f'<b>{ws}</b>' if b else f'<em>{ws}</em>' if i else ws)
    return ''.join(out)
blocks, n = [], 0
for blk in re.split(r'\n\n+', md):
    blk = blk.strip()
    m = re.match(r'## (.+)', blk)
    if m: blocks.append(f'<h2 class="sr">{html.escape(m.group(1))}</h2>'); continue
    m = re.match(r'<!--run (\d+) ?(.*?)-->', blk)
    if m:
        d = kv(m.group(2)); blocks.append(f'<div class="run" style="--h:{m.group(1)}" aria-hidden="true">{mk(d, False)}{mk(d, True)}</div>'); continue
    m = re.match(r'<!--scene (\d+) ?(.*?)-->\n(.*)', blk, re.S)
    if m:
        n += 1; d = kv(m.group(2)); text = m.group(3).strip(); big = text.endswith('{big}'); text = text.replace('{big}', '').strip()
        blocks.append(f'<section class="scene" style="--h:{m.group(1)}"{" id=%s" % chr(34)+"s1"+chr(34) if n == 1 else ""}>{mk(d, False)}<div class="say"><p{" class=%s" % chr(34)+"big"+chr(34) if big else ""}>{wrap(text)}</p></div>{mk(d, True)}</section>')
FR = [.207, .296, .38, .462, .547, .624, .713, .829]
hlr = ''.join(f'<g style="opacity:0;transition:opacity .25s"><circle cx="500" cy="500" r="{f*500:.1f}" stroke="#F4F0E6" stroke-opacity=".18" stroke-width="30"/><circle cx="500" cy="500" r="{f*500:.1f}" stroke="#F4F0E6" stroke-opacity=".9" stroke-width="2"/></g>' for f in FR)
sectors = json.load(open(os.path.join(ROOT, 'content/fractal2/sectors.json')))['sectors']
atlas = []
for s in sectors:
    if s.get('built'): atlas.append(f'<li class="here"><span class="n">{s["n"]:02d}</span><span>Entertainment &amp; Music (mapped)</span></li>')
    else: atlas.append(f'<li><span class="n">{s["n"]:02d}</span><span>{html.escape(s["name"])}</span></li>')
tpl = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
out = tpl.replace('%%SCENES%%', '\n  '.join(blocks)).replace('%%HL%%', hlr).replace('%%ATLAS%%', '\n'.join(atlas)).replace('%%BASE%%', BASE)
open(os.path.join(HERE, 'index.html'), 'w', encoding='utf-8').write(out)
print('wrote index.html', len(out) // 1024, 'KB;', n, 'scenes')

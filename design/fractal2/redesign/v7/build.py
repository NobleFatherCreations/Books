#!/usr/bin/env python3
"""Fractal² intro v7: paced scenes. Text from content/fractal2/intro-v7.md (directives: <!--@ k=v-->, <!--move H k=a:b-->, <!--pad H-->, <!--steps [eight|down]-->, <!--plunge-->).
   python3 design/fractal2/redesign/v7/build.py [BASE]  -> index.html"""
import os, re, json, html, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
BASE = sys.argv[1] if len(sys.argv) > 1 else ''
md = open(os.path.join(ROOT, 'content/fractal2/intro-v7.md'), encoding='utf-8').read().split('\n')
parts, cur = {}, None
for line in md:
    m = re.match(r'^## ([IVX]+)\. (.+)$', line)
    if m: cur = m.group(1); parts[cur] = {'title': m.group(2), 'lines': []}
    elif cur: parts[cur].append(line) if False else parts[cur]['lines'].append(line)
def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t); return re.sub(r'\*(.+?)\*', r'<em>\1</em>', t)
def kv(s):
    d = {}
    for m in re.finditer(r'([a-z]+)=([^\s>]+)', s): d[m.group(1)] = m.group(2)
    return d
def attrs(d):
    out = ''
    for k, v in d.items():
        if k == 'rest':
            if v not in ('0', ''): out += ' data-rest="1"'
        else: out += f' data-{k}="{v}"'
    return out
def beat(h, spec):
    a, b = {'lit': '1'}, {'lit': '1'}
    for k, v in spec.items():
        if ':' in v: x, y = v.split(':', 1)
        else: x = y = v
        a[k], b[k] = x, y
    return f'<div class="beat" style="--bh:{h}svh" aria-hidden="true"><i{attrs(a)}></i><i{attrs(b)}></i></div>'
EIGHT = [2.1, 1.9, 1.75, 1.6, 1.45, 1.35, 1.25, 1.15]
def render(lines):
    out, para, pend, mode, steps = [], [], {}, None, []
    def flags(raw):
        fl = re.findall(r'\{(big|safe|note)\}\s*$', raw)
        raw = re.sub(r'\s*\{(big|safe|note)\}\s*$', '', raw)
        return raw, (fl[0] if fl else '')
    def flush():
        nonlocal para, pend
        if not para: return
        raw = ' '.join(para).strip(); para = []
        if not raw: return
        raw, fl = flags(raw)
        cls = {'big': 'big', 'safe': 'safe', 'note': 'note-in'}.get(fl, '')
        out.append(f'<p{(" class=%s" % chr(34)+cls+chr(34)) if cls else ""}{attrs(pend)}>{inline(raw)}</p>'); pend = {}
    for ln in lines:
        s = ln.rstrip()
        m = re.match(r'<!--@ (.*?)-->', s)
        if m: flush(); pend = kv(m.group(1)); continue
        m = re.match(r'<!--move (\d+) (.*?)-->', s)
        if m: flush(); out.append(beat(m.group(1), kv(m.group(2)))); continue
        m = re.match(r'<!--pad (\d+)-->', s)
        if m: flush(); out.append(f'<div class="beat" style="--bh:{m.group(1)}svh" aria-hidden="true"><i data-lit="1"></i><i data-lit="1"></i></div>'); continue
        if s.startswith('<!--plunge-->'):
            flush(); out.append('<div aria-hidden="true" style="height:36svh"></div>')
            out.append(beat(300, {'z': '0.48:3.8', 'rest': '1:0', 'p': '0:1', 'lb': '1'}))
            out.append('<div aria-hidden="true" style="height:70svh"></div>'); continue
        m = re.match(r'<!--steps ?(\w*)-->', s)
        if m: flush(); mode, steps = (m.group(1) or 'plain'), []; continue
        if s.startswith('<!--/steps-->'):
            lis = []
            for j, st in enumerate(steps):
                if mode == 'eight': lis.append(f'<li data-z="{EIGHT[j]}" data-hl="{j}">{inline(st)}</li>')
                elif mode == 'down': lis.append(f'<li data-z="{0.6 - j*0.03:.2f}" data-rest="1" data-rd="0.45">{inline(st)}</li>')
                else: lis.append(f'<li>{inline(st)}</li>')
            out.append('<ol class="st">' + ''.join(lis) + '</ol>'); mode = None; continue
        if mode is not None:
            if s.strip(): steps.append(s.strip())
            continue
        if s.startswith('<!--') or s.strip() == '---' or s.startswith('# '): flush(); continue
        if not s.strip(): flush(); continue
        para.append(s)
    flush(); return '\n      '.join(out)
blocks = []
for key in parts:
    p = parts[key]
    blocks.append(f'<section class="part" id="p{key.lower()}"><p class="kick">Part {key}</p><h2>{inline(p["title"])}</h2>\n      {render(p["lines"])}\n    </section>')
parts_html = '\n    '.join(blocks).replace('id="pi"', 'id="p1"')
# stage-name ring highlights, as fractions of the disc radius measured on the drawn original
FR = [.207, .296, .38, .462, .547, .624, .713, .829]
hlr = ''.join(f'<g style="opacity:0;transition:opacity .25s"><circle cx="500" cy="500" r="{f*500*1.0:.1f}" stroke="#F4F0E6" stroke-opacity=".18" stroke-width="30"/><circle cx="500" cy="500" r="{f*500:.1f}" stroke="#F4F0E6" stroke-opacity=".9" stroke-width="2"/></g>' for f in FR)
sectors = json.load(open(os.path.join(ROOT, 'content/fractal2/sectors.json')))['sectors']
atlas, builtn = [], ''
for s in sectors:
    if s.get('built'): builtn = f'{s["n"]:02d}'; atlas.append(f'<li class="here"><span class="n">{s["n"]:02d}</span><span class="t">Entertainment &amp; Music (mapped)</span></li>')
    else: atlas.append(f'<li><span class="n">{s["n"]:02d}</span><span class="t">{html.escape(s["name"])}</span></li>')
tpl = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
out = tpl.replace('%%PARTS%%', parts_html).replace('%%HL%%', hlr).replace('%%ATLAS%%', '\n'.join(atlas)).replace('%%NSECT%%', str(len(sectors))).replace('%%BUILTN%%', builtn).replace('%%BASE%%', BASE)
open(os.path.join(HERE, 'index.html'), 'w', encoding='utf-8').write(out)
print('wrote index.html', len(out)//1024, 'KB;', out.count('data-z='), 'anchors')

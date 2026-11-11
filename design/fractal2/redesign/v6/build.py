#!/usr/bin/env python3
"""Fractal² intro v6: one camera over vector artwork. Text from content/fractal2/intro-story.md (unchanged).
   python3 design/fractal2/redesign/v6/build.py [BASE]   -> index.html   (BASE e.g. /fractal2/_a/v6/ for the deployed copy)"""
import os, re, json, html, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
BASE = sys.argv[1] if len(sys.argv) > 1 else ''
md = open(os.path.join(ROOT, 'content/fractal2/intro-story.md'), encoding='utf-8').read().split('\n')
parts, cur = {}, None
for line in md:
    m = re.match(r'^## ([IVX]+)\. (.+)$', line)
    if m: cur = m.group(1); parts[cur] = {'title': m.group(2), 'lines': []}
    elif cur: parts[cur]['lines'].append(line)
def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t); return re.sub(r'\*(.+?)\*', r'<em>\1</em>', t)
plain = lambda t: re.sub(r'\*+', '', t)

# camera keyframes by paragraph start: z = zoom (log-interpolated), lit = text-free beat (dial full strength), g = 2,700-point grid, dim = dial dimmed
K = [
 ('There is a room, and everyone', dict(z=3.8, rd=0.3)), ('So you leave.', dict(z=3.5, rd=0.3)), ('This work began as a refusal', dict(z=3.1, rd=0.25)),
 ('A fractal is a pattern that repeats', dict(z=2.6)), ('The cycle that runs inside', dict(z=2.25)),
 ('Thirty techniques carry', dict(z=1.1)), ('Then I walked that map', dict(z=1.0)),
 ('Thirty techniques. Three levels', dict(z=1.0, g=0)), ('Two thousand seven hundred examples', dict(z=1.0, g=1, dim=.95)),
 ('And a dare', dict(z=1.0, g=0, dim=0)), ('A fractal has one more property', dict(z=1.0)), ('Measure a coastline', dict(z=1.0)),
 ('Then I looked closer.', dict(z=1.0)),
 ('The true map has more than three hundred', dict(z=0.31, rest=1)), ('That is what the small', dict(z=0.31, rest=1)),
 ('It is a Tuesday', dict(z=0.31, rest=1)), ('This is what almost no one names', dict(z=0.34, rest=1)), ('And here is the turn', dict(z=0.4, rest=1)), ('I have experienced manipulation', dict(z=0.48, rest=1)), ('Justice comes from', dict(z=0.6, rest=1)), ('For thousands of years', dict(z=0.6, rest=1)), ('Go back, now', dict(z=3.8, rd=0.35)), ('Only now you know', dict(z=3.8, rd=0.45)),
 ('You are not afraid of this room', dict(z=3.8, rd=0.5)), ('And at the bottom', dict(z=3.8, p=0.3, rd=0.9)), ('I believe a world', dict(z=3.8, p=0.4, rd=0.7)),
]
def A(t, extra=''):
    for p, d in K:
        if t.startswith(p):
            return ' ' + ' '.join(f'data-{k}="{v}"' for k, v in d.items()) + extra
    return ''
BEAT = lambda a, b: f'<div class="beat" aria-hidden="true"><i {a}></i><i {b}></i></div>'
EIGHT = [2.1, 1.9, 1.75, 1.6, 1.45, 1.35, 1.25, 1.15]
def render(lines, key):
    out, para, steps, ins, nsteps = [], [], [], False, 0
    def flush():
        nonlocal para
        if not para: return
        raw = ' '.join(para).strip(); para = []
        if not raw or raw == '---': return
        t = plain(raw); cls = ''
        if t in ('It must be me.', "What if it isn't you?", 'Nothing struck you.') or raw.startswith('**The true map has more'): cls = 'big'
        if raw.startswith('*A note before'): cls = 'note-in'
        out.append(f'<p{(" class=%s" % chr(34)+cls+chr(34)) if cls else ""}{A(t)}>{inline(raw)}</p>')
        if t.startswith('Two thousand seven hundred examples'): out.append(BEAT('data-z="1.0" data-g="1" data-dim=".95"', 'data-z="1.0" data-g="1" data-dim=".95"').replace('class="beat"', 'class="beat" style="--bh:90svh"'))
        if t.startswith('Then I looked closer.'): out.append(BEAT('data-z="1.0" data-lit="1" data-lb="1"', 'data-z="0.31" data-rest="1" data-lit="1" data-lb="1"').replace('class="beat"', 'class="beat" style="--bh:260svh"'))
    for ln in lines:
        s = ln.rstrip()
        if s.startswith('<!--steps-->'): flush(); ins = True; steps = []; continue
        if s.startswith('<!--/steps-->'):
            ins = False; lis = []
            for j, st in enumerate(steps):
                if key == 'II' and nsteps == 0 and len(steps) == 8: lis.append(f'<li data-z="{EIGHT[j]}" data-hl="{j}">{inline(st)}</li>')
                elif key == 'VII' and nsteps == 0: lis.append(f'<li data-z="{0.6 - j*0.03:.2f}" data-rest="1" data-rd="0.45">{inline(st)}</li>')
                else: lis.append(f'<li>{inline(st)}</li>')
            out.append('<ol class="st">' + ''.join(lis) + '</ol>')
            if key == 'VII' and nsteps == 0:
                out.append('<div aria-hidden="true" style="height:36svh"></div>')
                out.append(BEAT('data-z="0.48" data-rest="1" data-lit="1" data-p="0" data-lb="1"', 'data-z="3.8" data-lit="1" data-p="1" data-lb="1"').replace('class="beat"', 'class="beat" style="--bh:300svh"'))
                out.append('<div aria-hidden="true" style="height:70svh"></div>')
            nsteps += 1; continue
        if ins:
            if s.strip(): steps.append(s.strip())
            continue
        if s.startswith('<!--') or s.strip() == '---' or not s.strip(): flush(); continue
        para.append(s)
    flush(); return '\n      '.join(out)
blocks = []
for key in parts:
    p = parts[key]
    blocks.append(f'<section class="part" id="p{key.lower()}"><p class="kick">Part {key}</p><h2>{inline(p["title"])}</h2>\n      {render(p["lines"], key)}\n    </section>')
parts_html = '\n    '.join(blocks).replace('id="pi"', 'id="p1"')
# stage-name ring highlights, as fractions of the disc radius measured on the drawn original
FR = [.207, .296, .38, .462, .547, .624, .713, .829]
hlr = ''.join(f'<g style="opacity:0;transition:opacity .25s"><circle cx="500" cy="500" r="{f*500*1.0:.1f}" stroke="#F4F0E6" stroke-opacity=".18" stroke-width="30"/><circle cx="500" cy="500" r="{f*500:.1f}" stroke="#F4F0E6" stroke-opacity=".9" stroke-width="2"/></g>' for f in FR)
sectors = json.load(open(os.path.join(ROOT, 'content/fractal2/sectors.json')))['sectors']
atlas, builtn = [], ''
for s in sectors:
    if s.get('built'): builtn = f'{s["n"]:02d}'; atlas.append(f'<li class="here"><span class="n">{s["n"]:02d}</span><span class="t">Entertainment &amp; Music ●</span></li>')
    else: atlas.append(f'<li><span class="n">{s["n"]:02d}</span><span class="t">{html.escape(s["name"])}</span></li>')
tpl = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
out = tpl.replace('%%PARTS%%', parts_html).replace('%%HL%%', hlr).replace('%%ATLAS%%', '\n'.join(atlas)).replace('%%NSECT%%', str(len(sectors))).replace('%%BUILTN%%', builtn).replace('%%BASE%%', BASE)
open(os.path.join(HERE, 'index.html'), 'w', encoding='utf-8').write(out)
print('wrote index.html', len(out)//1024, 'KB;', out.count('data-z='), 'anchors')

#!/usr/bin/env python3
"""Fractal² redesign, vertical slice (Direction A, "The Survey"). Generates index.html from template.html.
Every ring, tick and label is computed from the same data (eight stages, 30 techniques), so nothing can be misspelled or miscounted.
   python3 design/fractal2/redesign/build.py      -> design/fractal2/redesign/index.html"""
import math, json, os, html
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
STAGES = [('Idealize', 2), ('Hook', 2), ('Devalue', 4), ('Confuse', 5), ('Isolate', 6), ('Extract', 7), ('Discard', 2), ('Replace', 2)]
assert sum(n for _, n in STAGES) == 30
GAP = 4.0

def pol(r, a):
    return r * math.cos(a), r * math.sin(a)

def arc(r, a0, a1):
    x0, y0 = pol(r, a0); x1, y1 = pol(r, a1)
    return f"M{x0:.2f} {y0:.2f}A{r:g} {r:g} 0 {1 if (a1 - a0) > math.pi else 0} 1 {x1:.2f} {y1:.2f}"

def spans():
    usable = 360.0 - GAP * len(STAGES)
    a = -90.0 + GAP / 2
    out = []
    for name, n in STAGES:
        w = usable * n / 30.0
        out.append((a, a + w, n)); a += w + GAP
    return out

def ring(r, w, cls='', ticks=True, lit=None):
    """One eight-stage ring: bands with body (stroke width w), 30 technique ticks outside the band."""
    s = []
    for i, (a0, a1, n) in enumerate(spans()):
        d = arc(r, math.radians(a0), math.radians(a1))
        on = '' if lit is None else (' on' if lit else '')
        s.append(f'<path class="band s{i}{on}" data-i="{i}" pathLength="1" d="{d}" stroke-width="{w}"/>')
        if ticks:
            for j in range(n):
                ang = math.radians(a0 + (a1 - a0) * (j + 0.5) / n)
                x0, y0 = pol(r + w / 2 + 5, ang); x1, y1 = pol(r + w / 2 + 14, ang)
                s.append(f'<line class="tick s{i}" x1="{x0:.2f}" y1="{y0:.2f}" x2="{x1:.2f}" y2="{y1:.2f}"/>')
    return f'<g class="ring {cls}">' + ''.join(s) + '</g>'

def scale_ticks(r0, r1, step=10):
    out = []
    for k in range(0, 360, step):
        ang = math.radians(k - 90)
        ln = r1 if k % 30 == 0 else r0 + (r1 - r0) * 0.55
        x0, y0 = pol(r0, ang); x1, y1 = pol(ln, ang)
        out.append(f'<line class="minor" x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}"/>')
    return '<g>' + ''.join(out) + '</g>'

def crosshair():
    ls = []
    for (x0, y0, x1, y1) in [(0, -188, 0, -112), (0, 112, 0, 188), (-188, 0, -112, 0), (112, 0, 188, 0)]:
        ls.append(f'<line class="cross" x1="{x0}" y1="{y0}" x2="{x1}" y2="{y1}"/>')
    return ''.join(ls)

def numerals(r):
    out = []
    for i, (a0, a1, n) in enumerate(spans()):
        x, y = pol(r, math.radians((a0 + a1) / 2))
        out.append(f'<text class="num" x="{x:.1f}" y="{y:.1f}" text-anchor="middle" dominant-baseline="central">{i + 1}</text>')
    return ''.join(out)

emblem = ('<svg class="emblem" viewBox="-240 -240 480 480" role="img" aria-label="The Fractal: eight stages in a ring, thirty techniques marked around it">'
          '<circle class="guide" r="100"/><circle class="guide" r="190"/>' + crosshair() + scale_ticks(200, 212) + ring(150, 30) +
          '<circle class="core" r="5"/></svg>')

cycle_svg = ('<svg id="cyc" class="fig" viewBox="-240 -240 480 480" role="img" aria-label="Eight stages arranged in a ring, lighting one after another: Idealize, Hook, Devalue, Confuse, Isolate, Extract, Discard, Replace. After Replace the ring begins again at Idealize.">'
             '<circle class="guide" r="100"/><circle class="guide" r="190"/>' + crosshair() + scale_ticks(200, 212) + ring(150, 30, 'cycle', True, False) + numerals(232) +
             '<text id="c-name" class="cname" x="0" y="-6" text-anchor="middle">Eight stages</text>'
             '<text id="c-of" class="cof" x="0" y="30" text-anchor="middle">in order</text></svg>')

zoom_svg = ('<svg id="zm" class="fig" viewBox="-300 -300 600 600" role="img" aria-label="The same eight-stage ring drawn at three scales, one inside the next: one life at the centre, an institution around it, a civilization around that. A small mark at the centre is you.">'
            '<g id="zg"><g class="lv l0 on">' + ring(70, 20, '', True, None) + '</g>'
            '<g class="lv l1 on">' + ring(160, 20, '', True, None) + '</g>'
            '<g class="lv l2 on">' + ring(250, 20, '', True, None) + '</g>'
            '<circle class="core" r="6"/></g>'
            '</svg>')

cycle_steps = [
    ('Idealize.', 'You are seen, chosen, flooded with warmth.'),
    ('Hook.', 'You commit, and leaving begins to cost something.'),
    ('Devalue.', 'The warmth cools, and your worth becomes a thing you have to earn back.'),
    ('Confuse.', 'What you saw, what you heard and what you felt are put in doubt.'),
    ('Isolate.', 'The people who could have told you what they saw are moved out of reach.'),
    ('Extract.', 'What you have is taken: time, money, labor, body, belief.'),
    ('Discard.', 'You are dropped when there is nothing left to take.'),
    ('Replace.', 'Someone new is in your seat before it is cold.'),
]
zoom_steps = [
    ('In one life:', 'the partner, the parent, the boss. The pattern wearing a human face.'),
    ('Inside an institution:', 'the church, the school, the hospital, the company. The pattern wearing a logo.'),
    ('Across a civilization:', 'the economy, the culture, the law. The pattern wearing the sky.'),
]
def steps_html(steps, label):
    return ''.join(f'<li data-i="{i}"><p class="k">{label} {i + 1} of {len(steps)}</p><p><b>{html.escape(a)}</b> {html.escape(b)}</p></li>' for i, (a, b) in enumerate(steps))

sectors = json.load(open(os.path.join(ROOT, 'content/fractal2/sectors.json')))['sectors']
tiles = []
enter = ''
for s in sectors:
    nm = html.escape('Entertainment & Music' if s.get('built') else s['name'])
    if s.get('built'):
        tiles.append(f'<li class="here"><span class="n">{s["n"]:02d}</span><span class="t">{nm} <b aria-hidden="true">●</b></span></li>')
        enter = f'<div class="lit-wrap"><a class="enter" href="/fractal2/entertainment"><span class="n mono">Sector {s["n"]:02d} · enter</span><span class="t">{nm}</span><span class="m mono">mapped in full</span></a></div>'
    else:
        tiles.append(f'<li><span class="n">{s["n"]:02d}</span><span class="t">{nm}</span></li>')
built = [s['name'] for s in sectors if s.get('built')]

tpl = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
out = (tpl.replace('%%EMBLEM%%', emblem).replace('%%CYCLE_SVG%%', cycle_svg).replace('%%CYCLE_STEPS%%', steps_html(cycle_steps, 'Stage'))
       .replace('%%ZOOM_SVG%%', zoom_svg).replace('%%ZOOM_STEPS%%', steps_html(zoom_steps, 'Level')).replace('%%ATLAS%%', '\n'.join(tiles)).replace('%%ENTER%%', enter)
       .replace('%%BUILT%%', html.escape(', '.join(built) or 'none')).replace('%%NSECT%%', str(len(sectors))))
open(os.path.join(HERE, 'index.html'), 'w', encoding='utf-8').write(out)
print('wrote index.html', len(out) // 1024, 'KB; sectors', len(sectors), '| built:', built)

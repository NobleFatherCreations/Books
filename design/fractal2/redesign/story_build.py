#!/usr/bin/env python3
"""Zoom intro built around the original Fractal artwork. Text comes verbatim from content/fractal2/intro-story.md (Parts I, II, V).
   python3 design/fractal2/redesign/zoom_build.py   -> design/fractal2/redesign/zoom.html"""
import os, re, json, math, html, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
md = open(os.path.join(ROOT, 'content/fractal2/intro-story.md'), encoding='utf-8').read().split('\n')

# --- split into parts by "## X. Title"
parts, cur = {}, None
for line in md:
    m = re.match(r'^## ([IVX]+)\. (.+)$', line)
    if m:
        cur = m.group(1); parts[cur] = {'title': m.group(2), 'lines': []}
    elif cur:
        parts[cur]['lines'].append(line)

def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'\*(.+?)\*', r'<em>\1</em>', t)
    return t
def plain(t):
    return re.sub(r'\*+', '', t)

# --- scroll keyframes: paragraph prefix -> (A scale, B reveal, A opacity)
KEY = [
    ('There is a room, and everyone', 4.6, 0, 1),
    ('So you leave.', 4.2, 0, 1),
    ('This work began as a refusal', 3.5, 0, 1),
    ('A fractal is a pattern that repeats at every scale', 2.8, 0, 1),
    ('The cycle that runs inside a manipulative relationship', 2.3, 0, 1),
    ('Thirty techniques carry a person', 1.08, 0, 1),
    ('Thirty techniques. Three levels', 1.0, 0, 1),
    ('A fractal has one more property', 1.0, 0, 1),
    ('Measure a coastline', 1.0, 0, 1),
    ('Then I looked closer.', 1.0, 0.0, 1),
    ('The true map has more than three hundred', 0.55, 0.6, 1),
    ('That is what the small', 0.36, 1.0, 1),
    ('More than a thousand observations', 0.30, 1.18, 1),
    ('The closer I looked, the further back', 0.28, 1.18, 1),
    ('It is a Tuesday', 0.28, 1.18, 1),
    ('Nothing struck you.', 0.28, 1.18, 1),
    ('Go back, now', 2.2, 0, 1),
    ('Only now you know what the tightening is', 4.4, 0, 1),
    ('You are not afraid of this room', 4.4, 0, 1),
    ('I believe a world without this cycle', 0.30, 1.18, 1),
]
def attrs(prefix_text, hl=-1):
    for p, s, b, ao in KEY:
        if prefix_text.startswith(p):
            return f' data-s="{s}" data-b="{b}" data-hl="{hl}" data-ao="{ao}"'
    return ''

def render(lines, key):
    out, i, steps_n = [], 0, 0
    blocks_seen = 0
    para, in_steps, steps = [], False, []
    def flush():
        nonlocal para
        if para:
            raw = ' '.join(para).strip(); para = []
            if not raw or raw == '---':
                return
            at = attrs(plain(raw))
            cls = ''
            if plain(raw) in ('It must be me.', "What if it isn't you?", 'Nothing struck you.') or raw.startswith('**The true map has more than three hundred'):
                cls = ' class="big"'
            out.append(f'<p{cls}{at}>{inline(raw)}</p>')
    for ln in lines:
        s = ln.rstrip()
        if s.startswith('<!--steps-->'):
            flush(); in_steps = True; steps = []; continue
        if s.startswith('<!--/steps-->'):
            in_steps = False
            n = len(steps); eight = (n == 8) and key == 'II' and blocks_seen == 0
            drives = key == 'II' and blocks_seen < 2
            blocks_seen += 1
            lis = []
            for j, st in enumerate(steps):
                if not drives:
                    lis.append(f'<li>{inline(st)}</li>')
                elif eight:
                    sc = math.exp(math.log(2.0) + (math.log(1.1) - math.log(2.0)) * j / 7)
                    lis.append(f'<li data-hl="{j}" data-s="{sc:.3f}" data-b="0" data-ao="1">{inline(st)}</li>')
                else:
                    lis.append(f'<li data-hl="-1" data-s="1.0" data-b="0" data-ao="1">{inline(st)}</li>')
            out.append('<ol class="st">' + ''.join(lis) + '</ol>')
            continue
        if in_steps:
            if s.strip(): steps.append(s.strip())
            continue
        if s.startswith('### '):
            flush(); out.append(f'<h3>{inline(s[4:].strip())}</h3>'); continue
        if s.startswith('<!--') or s.strip() == '---':
            flush(); continue
        if not s.strip():
            flush(); continue
        para.append(s)
    flush()
    return '\n      '.join(out)

blocks = []
for key in ('I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII'):
    p = parts[key]
    blocks.append(f'<section class="part" id="p{key.lower()}"><p class="kick">Part {key}</p><h2>{inline(p["title"])}</h2>\n      {render(p["lines"], key)}\n    </section>')
# skip-link target
parts_html = '\n    '.join(blocks).replace('id="pi"', 'id="p1"')

# highlight rings at each stage's label radius (artwork measured, 1000-unit viewBox, centre 500, 486.5)
RAD = [93, 135, 176, 217, 260, 302, 347, 401]
hl = ''.join(f'<g style="opacity:0;transition:opacity .5s"><circle cx="500" cy="486.5" r="{r}" stroke="#F4D58A" stroke-opacity=".30" stroke-width="40"/><circle cx="500" cy="486.5" r="{r}" stroke="#FFE9A8" stroke-opacity=".85" stroke-width="2.5"/></g>' for r in RAD)

sectors = json.load(open(os.path.join(ROOT, 'content/fractal2/sectors.json')))['sectors']
atlas, builtn = [], ''
for s in sectors:
    if s.get('built'):
        builtn = f'{s["n"]:02d}'
        atlas.append(f'<li class="here"><span class="n">{s["n"]:02d}</span><span class="t">Entertainment &amp; Music ●</span></li>')
    else:
        atlas.append(f'<li><span class="n">{s["n"]:02d}</span><span class="t">{html.escape(s["name"])}</span></li>')

tpl = open(os.path.join(HERE, 'story_template.html'), encoding='utf-8').read()
tpl = tpl.replace("lis.forEach(function(li){li.classList.toggle('on',+li.dataset.hl===st.hl&&li.dataset.hl!==undefined)});", "lis.forEach(function(li){li.classList.toggle('on',st.hl>=0&&+li.dataset.hl===st.hl)});")
out = tpl.replace('%%PARTS%%', parts_html).replace('%%HL%%', hl).replace('%%ATLAS%%', '\n'.join(atlas)).replace('%%NSECT%%', str(len(sectors))).replace('%%BUILTN%%', builtn)
open(os.path.join(HERE, 'story.html'), 'w', encoding='utf-8').write(out)
for f in ('favicon.ico', 'emblem-64.png'):
    shutil.copy(os.path.join(ROOT, 'brand/out', f), os.path.join(HERE, f))
print('wrote story.html', len(out) // 1024, 'KB;', out.count('data-s='), 'keyframes')

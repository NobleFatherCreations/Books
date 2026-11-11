#!/usr/bin/env python3
"""Plain-text, numbered, annotated view of an intro script for story audits: python3 scripts/story-annotate.py content/fractal2/intro-v8.md out.txt"""
import re, sys
md = open(sys.argv[1], encoding='utf-8').read()
def note(p):
    d = dict(re.findall(r'([a-z]+)=([^\s>]+)', p)); n = []
    z = d.get('z', '').split(':'); z0, z1 = float(z[0]) if z[0] else None, float(z[-1]) if z[0] else None
    if z0 is not None:
        if abs(z0 - z1) < 0.01: n.append('camera holds' + (' at the full circle fitting the screen' if abs(z0 - 1) < .02 else ' on the large map' if z0 < .5 else ''))
        else: n.append('camera zooms ' + ('OUT' if z1 < z0 else 'IN') + f' ({z0:g} to {z1:g}; 1.0 = circle fits the screen)')
    if 'hl' in d: n.append(f'ring {int(d["hl"])+1} of 8 lights')
    if 'g' in d: n.append('2,700-dot field assembles')
    if 'w' in d: n.append('the tactic words fill the rings')
    if 'bk' in d: n.append('screen goes to black')
    if 'sp' in d: n.append('a spark of light grows in the black')
    if 'a' in d: n.append('pulls out to the atlas of 30 sectors')
    return '; '.join(n)
out, i = [], 0
for blk in re.split(r'\n\n+', md):
    blk = blk.strip()
    m = re.match(r'## (.+)', blk)
    if m: out.append(f'\n=== {m.group(1).upper()} ==='); continue
    m = re.match(r'<!--run (\d+) ?(.*?)-->', blk)
    if m: out.append(f'   [silent stretch, about {int(m.group(1))*0.7/100:.1f} screens of scroll, no words: {note(m.group(2))}]'); continue
    m = re.match(r'<!--scene (\d+) ?(.*?)-->\n(.*)', blk, re.S)
    if m:
        i += 1; t = re.sub(r'\s*\{big\}$', '', m.group(3).strip()).replace('**', '')
        out.append(f'[{i}] ({int(m.group(1))*0.5/100+0.0:.1f} extra screens of scroll; words appear one by one, hold, dissolve; {note(m.group(2))})\n    "{t}"')
open(sys.argv[2], 'w', encoding='utf-8').write('\n'.join(out))
print(i, 'scenes')

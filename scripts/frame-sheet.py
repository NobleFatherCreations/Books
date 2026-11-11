#!/usr/bin/env python3
"""Contact sheets for scripts/frame-walk.mjs. python3 scripts/frame-sheet.py <dir> [cols]. Writes sheet-NN.jpg (rows of labelled tiles)."""
import json, sys, os, textwrap
from PIL import Image, ImageDraw, ImageFont
d = sys.argv[1]; cols = int(sys.argv[2]) if len(sys.argv) > 2 else 8
w = json.load(open(os.path.join(d, 'walk.json'))); meta = w['meta']
tw = 1568 // cols; th = round(tw * w['vh'] / w['vw']); lab = 44; rows_per = max(1, 1500 // (th + lab))
try: font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 11)
except Exception: font = ImageFont.load_default()
per = cols * rows_per
for s in range(0, len(meta), per):
    chunk = meta[s:s + per]; rows = -(-len(chunk) // cols)
    sheet = Image.new('RGB', (cols * tw, rows * (th + lab)), (24, 24, 28)); dr = ImageDraw.Draw(sheet)
    for i, m in enumerate(chunk):
        x, y = (i % cols) * tw, (i // cols) * (th + lab)
        im = Image.open(os.path.join(d, m['f'] + '.jpg')).resize((tw - 4, th - 4), Image.LANCZOS); sheet.paste(im, (x + 2, y + 2))
        cam = (' z=%.2f' % m['cam']['z']) if m.get('cam') else ''
        dr.text((x + 4, y + th), ('%s%%%s' % (m['pct'], cam)), fill=(255, 210, 120), font=font)
        for k, line in enumerate(textwrap.wrap(m.get('cap') or '(no words)', tw // 6)[:2]): dr.text((x + 4, y + th + 13 + k * 13), line, fill=(215, 215, 215), font=font)
    out = os.path.join(d, 'sheet-%02d.jpg' % (s // per)); sheet.save(out, quality=82); print('wrote', out)

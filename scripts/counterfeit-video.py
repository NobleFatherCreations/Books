#!/usr/bin/env python3
"""Assemble one Counterfeit deck into a 1080x1920 H.264 slideshow (MP4) with ffmpeg's concat demuxer: each slide held for a set time,
longer for the dense 15-line pages. Usage: counterfeit-video.py religion|fractal [out.mp4]
Reads exports/counterfeit-slides/<deck>/manifest.json; writes exports/counterfeit-<deck>.mp4 by default."""
import json, os, subprocess, sys, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
deck = sys.argv[1]; D = os.path.join(ROOT, 'exports/counterfeit-slides', deck)
out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, f'exports/counterfeit-{deck}.mp4')
man = json.load(open(os.path.join(D, 'manifest.json')))
def hold(f):
    if 'cover' in f: return 3.5
    if 'mother-earth' in f: return 7.0
    if any(k in f for k in ('religion-', 'sector-', 'mirror-', 'body-')): return 10.0   # 15 one-sentence lines per page
    return 8.0
lst = os.path.join(tempfile.mkdtemp(), 'list.txt'); total = 0
with open(lst, 'w') as fh:
    for m in man:
        d = hold(m['file']); total += d; fh.write(f"file '{os.path.join(D, m['file'])}'\nduration {d}\n")
    fh.write(f"file '{os.path.join(D, man[-1]['file'])}'\n")   # concat needs the last frame repeated
print(f'{deck}: {len(man)} slides, {total / 60:.1f} minutes')
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-vf', 'scale=1080:1920,format=yuv420p', '-r', '30',
                '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-movflags', '+faststart', out], check=True)
print('wrote', out, round(os.path.getsize(out) / 1e6, 1), 'MB')

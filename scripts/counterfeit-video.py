#!/usr/bin/env python3
"""Assemble the Counterfeit slides into one 1080x1920 H.264 slideshow (MP4) with ffmpeg's concat demuxer: each slide held for a set time,
longer for the dense 30-line pages. Usage: counterfeit-video.py [out.mp4]   Reads exports/counterfeit-slides/manifest.json."""
import json, os, subprocess, sys, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, 'exports/counterfeit-slides'); out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'exports/counterfeit-slideshow.mp4')
man = json.load(open(os.path.join(D, 'manifest.json')))
def hold(f):
    if 'cover' in f: return 3.5
    if 'mother-earth' in f: return 6.0
    if 'religion-' in f: return 14.0            # 30 sentences on one page
    if 'sector-' in f: return 9.0               # 15 sentences per page
    return 8.0
lst = os.path.join(tempfile.mkdtemp(), 'list.txt'); total = 0
with open(lst, 'w') as fh:
    for m in man:
        d = hold(m['file']); total += d; fh.write(f"file '{os.path.join(D, m['file'])}'\nduration {d}\n")
    fh.write(f"file '{os.path.join(D, man[-1]['file'])}'\n")   # concat needs the last frame repeated
print(f'{len(man)} slides, {total / 60:.1f} minutes')
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-vf', 'scale=1080:1920,format=yuv420p', '-r', '30',
                '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-movflags', '+faststart', out], check=True)
print('wrote', out, round(os.path.getsize(out) / 1e6, 1), 'MB')

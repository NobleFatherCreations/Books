#!/usr/bin/env python3
"""Assemble the Counterfeit slides into one 1080x1920 H.264 slideshow (MP4) with ffmpeg: a short crossfade between slides,
longer holds for the dense 30-line slides. Usage: counterfeit-video.py [out.mp4]   Reads exports/counterfeit-slides/manifest.json."""
import json, os, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, 'exports/counterfeit-slides'); out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'exports/counterfeit-slideshow.mp4')
man = json.load(open(os.path.join(D, 'manifest.json')))
HOLD = lambda f: 3.5 if 'cover' in f else 5.0 if 'mother-earth' in f else 12.0 if ('religion-' in f or 'sector-' in f) else 8.0
XF = 0.4; FPS = 30
inputs, filt, last = [], [], None; t = 0.0
for i, m in enumerate(man):
    d = HOLD(m['file']); inputs += ['-loop', '1', '-t', f'{d + XF:.2f}', '-i', os.path.join(D, m['file'])]
    filt.append(f'[{i}:v]scale=1080:1920,setsar=1,fps={FPS},format=yuv420p[v{i}]')
    if i == 0: last = 'v0'; t = d
    else:
        filt.append(f'[{last}][v{i}]xfade=transition=fade:duration={XF}:offset={t:.2f}[x{i}]'); last = f'x{i}'; t += d
print(f'{len(man)} slides, about {t / 60:.1f} minutes')
cmd = ['ffmpeg', '-y', '-loglevel', 'error'] + inputs + ['-filter_complex', ';'.join(filt), '-map', f'[{last}]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out]
subprocess.run(cmd, check=True); print('wrote', out, round(os.path.getsize(out) / 1e6, 1), 'MB')

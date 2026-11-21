#!/usr/bin/env python3
"""Download every Listening Room mp3 from the owner's Google Drive folder ("MP3 music") into
instruments/music/audio/ (gitignored, 1.26 GB), using the Drive ids in instruments/music/MANIFEST.json,
and check each file's size against the manifest. Safe to re-run: files already present at the right size are skipped."""
import json, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
M = json.load(open(ROOT / "instruments/music/MANIFEST.json"))
OUT = ROOT / "instruments/music/audio"; OUT.mkdir(parents=True, exist_ok=True)
bad = []
for n, t in enumerate(M["tracks"], 1):
    f = OUT / t["file"]
    if f.exists() and f.stat().st_size == t["bytes"]:
        continue
    url = f"https://drive.usercontent.google.com/download?id={t['driveId']}&export=download&confirm=t"
    for attempt in range(4):
        subprocess.run(["curl", "-sL", "--retry", "3", "-o", str(f), url])
        if f.exists() and f.stat().st_size == t["bytes"]:
            break
    ok = f.exists() and f.stat().st_size == t["bytes"]
    if not ok: bad.append(t["file"])
    print(f"{n:3}/{len(M['tracks'])} {'ok ' if ok else 'BAD'} {t['file']}", flush=True)
print("done;", len(M["tracks"]) - len(bad), "ok,", len(bad), "bad", bad)
sys.exit(1 if bad else 0)

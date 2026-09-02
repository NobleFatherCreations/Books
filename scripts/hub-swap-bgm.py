#!/usr/bin/env python3
"""Swap the hub's #npAudio background track.

The hub inlines exactly one always-loaded ambient track as base64 (see
scripts/wook-add-soundtrack.py's docstring for why that's the right call
for a single persistent atmosphere track, versus hosting many optional
ones). Swapping it is just replacing that one data URI -- everything else
about the feature (starts on the first door click, mute persists per tab,
never re-attempts without a fresh gesture) is untouched.

Run: python3 scripts/hub-swap-bgm.py <path-to-new-mp3>
"""
import base64
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HUB = ROOT / "hub/catalogue-redesign.html"

PATTERN = re.compile(
    r'(<audio id="npAudio"[^>]*src="data:audio/mpeg;base64,)([A-Za-z0-9+/=]+)("></audio>)')


def main():
    if len(sys.argv) != 2:
        print("usage: hub-swap-bgm.py <new-track.mp3>")
        return 1
    new_track = Path(sys.argv[1])
    assert new_track.exists(), new_track

    html = HUB.read_text(errors="surrogateescape")
    m = PATTERN.search(html)
    assert m, "no #npAudio element found"
    old_len = len(m.group(2))

    new_b64 = base64.b64encode(new_track.read_bytes()).decode()
    html = html[:m.start(2)] + new_b64 + html[m.end(2):]

    HUB.write_text(html, errors="surrogateescape")
    print(f"npAudio swapped: {old_len:,} -> {len(new_b64):,} base64 chars "
          f"({new_track.stat().st_size:,} raw bytes from {new_track.name})")


if __name__ == "__main__":
    sys.exit(main())

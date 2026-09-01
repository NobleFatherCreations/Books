#!/usr/bin/env python3
"""Swap the base64 payload for each of the 5 new books' portrait jacket
<img> inside the hub, matched by its distinctive alt text."""
import re
from pathlib import Path

HUB = Path(__file__).resolve().parents[2] / "hub/catalogue-redesign.html"
COVERS = Path(__file__).resolve().parent / "_work"

TITLES = {
    "longafter": "The Long After",
    "silence": "The Silence",
    "atwill": "At Will",
    "repair": "The Repair",
    "slowtake": "The Slow Take",
}


def main():
    html = HUB.read_text()
    for slug, title in TITLES.items():
        alt = f"Cover &mdash; {title} by Shae Stovell"
        pattern = re.compile(
            r'(<img src="data:image/jpeg;base64,)[A-Za-z0-9+/=]+'
            r'(" alt="' + re.escape(alt) + r'")'
        )
        m = pattern.search(html)
        assert m, f"{slug}: jacket img tag not found (alt={alt!r})"
        new_b64 = (COVERS / f"{slug}-jacket.b64").read_text().strip()
        html = html[:m.start()] + m.group(1) + new_b64 + m.group(2) + html[m.end():]
        print(slug, "re-embedded,", len(new_b64), "b64 chars")
    HUB.write_text(html)
    print("hub now", len(html), "chars")


if __name__ == "__main__":
    main()

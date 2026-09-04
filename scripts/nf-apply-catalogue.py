#!/usr/bin/env python3
"""Write the canonical catalogue (scripts/nf-catalogue.py) into every page that
already carries the nf-chrome drawer."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import importlib
cat = importlib.import_module("nf-catalogue")

ROOT = Path(__file__).resolve().parent.parent

# page file -> the catalogue slug that page IS (None = not itself in the list)
# Kept in sync with every file that actually carries the nf-chrome drawer --
# `grep -rl 'id="nf-chrome"' library workshop instruments hub other` is the
# check, not this dict from memory; it had drifted (festival, longafter,
# slowtake, repair, atwill, silence, the nfc guide itself, and reaction-map
# were all missing as of 2026-09-04, so none of them had picked up XVI-XX).
PAGES = {
    "library/wook/index.html": "wook",
    "library/children/index.html": "children",
    "library/feminine/index.html": "feminine",
    "library/fracture/index.html": "fracture",
    "library/fractal/index.html": "fractal",
    "library/festival/index.html": "festival",
    "library/longafter/index.html": "longafter",
    "library/slowtake/index.html": "slowtake",
    "library/repair/index.html": "repair",
    "library/atwill/index.html": "atwill",
    "library/silence/index.html": "silence",
    "workshop/seals/index.html": "press",
    "workshop/portals/index.html": "portals",
    "workshop/nfcguide/index.html": "nfc/",
    "instruments/music/index.html": "music",
    "instruments/shadowroot/index.html": "shadowroot",
    "other/reaction-map/index.html": None,
    "hub/catalogue-redesign.html": None,
    "library/_undeployed/sacred-divide-faith-redesign.html": "faith",
}


def main():
    for rel, here in PAGES.items():
        path = ROOT / rel
        html = path.read_text(errors="surrogateescape")
        before = len(html)
        out = cat.retoc(html, here)
        if out == html:
            print(f"  unchanged  {rel}")
            continue
        path.write_text(out, errors="surrogateescape")
        print(f"  updated    {rel}  ({before} -> {len(out)} bytes, here={here})")


if __name__ == "__main__":
    main()

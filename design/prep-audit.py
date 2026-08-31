#!/usr/bin/env python3
"""Strip base64 payloads from the single-file books to produce audit views.

Why: these pages are 0.1–11MB, but 85–99% of that is embedded base64 images
and fonts. Stripping those leaves the real markup+CSS, which is what any
reviewer — the impeccable detector, a subagent, a person — actually needs to
look at. It turns "too big to audit" into "every page fits comfortably".

The stripped copies are for ANALYSIS ONLY and live outside the repo. Never
edit a stripped file and never ship one — fixes go to the real source file.

Usage: python3 design/prep-audit.py [outdir]
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, ".audit-view")

# any base64 payload of meaningful length — images, fonts, audio
B64 = re.compile(r"data:[a-zA-Z0-9/;+.-]*?base64,[A-Za-z0-9+/=]{200,}")


def main():
    os.makedirs(OUT, exist_ok=True)
    targets = (
        sorted(glob.glob(os.path.join(ROOT, "library/*/index.html")))
        + sorted(glob.glob(os.path.join(ROOT, "fixes/*.html")))
        + [os.path.join(ROOT, "festie-codex-full.html")]
    )
    print(f"{'FILE':40s} {'ORIGINAL':>10s} {'STRIPPED':>10s} {'REAL':>7s}")
    for f in targets:
        if not os.path.exists(f):
            continue
        d = open(f, encoding="utf-8", errors="replace").read()
        s = B64.sub("data:STRIPPED", d)
        dest = os.path.join(OUT, os.path.basename(f))
        open(dest, "w", encoding="utf-8").write(s)
        print(f"{os.path.basename(f):40s} {len(d)/1e6:9.1f}M {len(s)/1024:9.1f}K {100*len(s)/len(d):6.1f}%")
    print(f"\nAudit views written to {OUT}")


if __name__ == "__main__":
    main()

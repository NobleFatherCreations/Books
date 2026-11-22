#!/usr/bin/env python3
"""Subset the two Fractal² typefaces to Latin woff2 (build-time tool; nothing here ships to readers).
  python3 design/fractal2/fonts.py     -> design/fractal2/fonts/*.woff2
Newsreader (reading + display serif, optical size axis kept) and Hanken Grotesk (interface)."""
from pathlib import Path
from fontTools import subset
ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent / "fonts"
OUT.mkdir(exist_ok=True)
UNI = "U+0020-007E,U+00A0-00FF,U+0131,U+0152-0153,U+02C6,U+02DA,U+02DC,U+2013-2014,U+2018-201A,U+201C-201E,U+2022,U+2026,U+2032-2033,U+2039-203A,U+2044,U+20AC,U+2122,U+2190-2193,U+2212,U+00B2,U+00D7,U+2192,U+2715"
JOBS = [("newsreader/Newsreader[opsz,wght].ttf", "newsreader.woff2"),
        ("newsreader/Newsreader-Italic[opsz,wght].ttf", "newsreader-italic.woff2"),
        ("hankengrotesk/HankenGrotesk[wght].ttf", "hanken.woff2")]
for src, dst in JOBS:
    o = subset.Options()
    o.flavor = "woff2"; o.layout_features = ["kern", "liga", "onum", "lnum", "tnum", "pnum", "smcp", "c2sc", "frac", "sups"]
    o.unicodes = subset.parse_unicodes(UNI); o.drop_tables += ["DSIG"]; o.notdef_outline = True
    f = subset.load_font(str(ROOT / "tools/fonts" / src), o)
    s = subset.Subsetter(o); s.populate(unicodes=o.unicodes); s.subset(f)
    subset.save_font(f, str(OUT / dst), o)
    print(dst, (OUT / dst).stat().st_size // 1024, "KB")
for lic in ("newsreader/OFL.txt", "hankengrotesk/OFL.txt"):
    (OUT / ("LICENSE-" + lic.split("/")[0] + ".txt")).write_text((ROOT / "tools/fonts" / lic).read_text())

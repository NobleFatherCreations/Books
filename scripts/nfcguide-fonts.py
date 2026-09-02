#!/usr/bin/env python3
"""Re-cut the NFC guide's inlined typefaces from Playfair/Poppins to the
Noble Father house faces (Fraunces, Hanken Grotesk, Space Mono).

The guide arrived with its own two-family pairing. Every other Noble Father
property -- hub, all 14 books, both craft sites -- uses Fraunces for display
and Hanken Grotesk for body, with Space Mono for labels, so the guide read as
a different studio's page. This swaps the four @font-face payloads and leaves
the guide's own CSS structure alone; only the family names in :root change.

The books inline the *full* TTFs (Fraunces alone is 360KB). That is fine for a
single-file book but would triple this page, so the guide keeps its own
approach instead: subset to exactly the glyphs it uses (assets/fonts/
charset.txt) and ship woff2. Same result, ~40x smaller.

Variable axes are instanced away rather than kept -- the guide asks for four
fixed weights, so shipping the whole wght axis is payload nobody reads.

Re-run after adding a recipe that uses a character outside charset.txt.
"""
import base64
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GUIDE = ROOT / "workshop/nfcguide"
FONTS = ROOT / "tools/fonts"

# family, weight, source ttf, axis pins for the variable ones.
CUTS = [
    ("Fraunces",        700, FONTS / "fraunces/Fraunces[SOFT,WONK,opsz,wght].ttf",
     {"wght": 700, "opsz": 60, "SOFT": 0, "WONK": 0}),
    ("Fraunces",        900, FONTS / "fraunces/Fraunces[SOFT,WONK,opsz,wght].ttf",
     {"wght": 900, "opsz": 90, "SOFT": 0, "WONK": 0}),
    ("Hanken Grotesk",  400, FONTS / "hankengrotesk/HankenGrotesk[wght].ttf",
     {"wght": 400}),
    ("Hanken Grotesk",  600, FONTS / "hankengrotesk/HankenGrotesk[wght].ttf",
     {"wght": 600}),
    ("Hanken Grotesk",  700, FONTS / "hankengrotesk/HankenGrotesk[wght].ttf",
     {"wght": 700}),
    ("Space Mono",      400, FONTS / "spacemono/SpaceMono-Regular.ttf", None),
]

LAYOUT = "kern,liga,calt,ccmp,locl,mark,mkmk,rlig"


def cut(src, pins, charset, out):
    """Instance the variable axes away, then subset to the charset, as woff2."""
    with tempfile.TemporaryDirectory() as tmp:
        stage = Path(tmp) / "stage.ttf"
        if pins:
            subprocess.run(
                ["fonttools", "varLib.instancer", "-o", str(stage), str(src)]
                + [f"{k}={v}" for k, v in pins.items()],
                check=True, capture_output=True)
        else:
            stage.write_bytes(src.read_bytes())
        subprocess.run(
            ["pyftsubset", str(stage), f"--text-file={charset}",
             "--flavor=woff2", f"--layout-features={LAYOUT}",
             f"--output-file={out}"],
            check=True, capture_output=True)


FACE_RE = re.compile(
    r"@font-face\{font-family:'(?:Playfair Display|Poppins)'[^}]*\}\n?")


def main():
    charset = GUIDE / "assets/fonts/charset.txt"
    assert charset.exists(), charset

    faces, total = [], 0
    with tempfile.TemporaryDirectory() as tmp:
        for family, weight, src, pins in CUTS:
            out = Path(tmp) / f"{family}-{weight}.woff2"
            cut(src, pins, charset, out)
            b = out.read_bytes()
            total += len(b)
            print(f"  {family} {weight}: {len(b):,} bytes")
            faces.append(
                f"@font-face{{font-family:'{family}';font-style:normal;"
                f"font-weight:{weight};font-display:swap;src:url(data:font/woff2;"
                f"base64,{base64.b64encode(b).decode()}) format('woff2')}}")
    print(f"  total: {total:,} bytes of font data")

    path = GUIDE / "index.html"
    html = path.read_text(errors="surrogateescape")
    n = len(FACE_RE.findall(html))
    assert n == 4, f"expected 4 old @font-face rules, found {n}"
    html = FACE_RE.sub("", html, count=4)

    # Re-insert as one block where the old rules were: right after the
    # typeface comment block that still explains why they are inlined.
    anchor = "   ============================================================ */\n"
    i = html.index(anchor) + len(anchor)
    html = html[:i] + "\n".join(faces) + "\n" + html[i:]

    path.write_text(html, errors="surrogateescape")
    print(f"index.html: {len(html):,} bytes")


if __name__ == "__main__":
    sys.exit(main())

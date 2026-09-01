#!/usr/bin/env python3
"""Swap the base64 payload inside each book's existing <img class="cover-mark">
tag for the freshly recomposited version (real logo watermark instead of the
placeholder wax seal). Alt text and everything else on the page is untouched."""
import re
from pathlib import Path

BOOKS_DIR = Path(__file__).resolve().parents[2] / "library"
COVERS = Path(__file__).resolve().parent / "_work"

BOOKS = ["longafter", "silence", "atwill", "repair", "slowtake"]

PATTERN = re.compile(
    r'(<img class="cover-mark" alt="[^"]*" src="data:image/jpeg;base64,)'
    r'[A-Za-z0-9+/=]+(">)'
)


def main():
    for name in BOOKS:
        path = BOOKS_DIR / name / "index.html"
        html = path.read_text()
        m = PATTERN.search(html)
        assert m, f"{name}: cover-mark img tag not found"
        new_b64 = (COVERS / f"{name}-final.b64").read_text().strip()
        new_tag = m.group(1) + new_b64 + m.group(2)
        html = html[:m.start()] + new_tag + html[m.end():]
        path.write_text(html)
        print(name, "re-embedded,", len(new_b64), "b64 chars,", path.stat().st_size, "file bytes")


if __name__ == "__main__":
    main()

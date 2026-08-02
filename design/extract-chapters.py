#!/usr/bin/env python3
"""Extract real chapter/movement data from a book's own source HTML.

These books author their chapter data as JS literals: `var MOVEMENTS=[...]`
(movement roman numeral, title, chapter-number list, blurb) and
`var CH={...}` (per-chapter title, blurb, readMin). This script parses that
straight out of the shipped page — no invented content, only what the book
itself already says about itself.

Usage: python3 design/extract-chapters.py <path-to-book-html> <slug> <title> <url>
Prints the book's chapters.json entry as JSON to stdout.
"""
import json
import re
import sys


def unescape(s):
    return (
        s.replace("\\'", "'")
        .replace("\\u2019", "\u2019")
        .replace("\\u2014", "\u2014")
        .replace('\\"', '"')
    )


def extract(path, slug, title, url):
    data = open(path, "r", encoding="utf-8", errors="replace").read()

    mv_start = data.find("var MOVEMENTS=[")
    mv_end = data.find("\n];", mv_start)
    if mv_start == -1 or mv_end == -1:
        sys.exit(f"no 'var MOVEMENTS=[...]' block found in {path}")
    mv_chunk = data[mv_start:mv_end]

    mv_pattern = re.compile(
        r"\{r:'(?P<r>[IVX]+)',\s*t:'(?P<t>(?:[^'\\]|\\.)*)',\s*c:\[(?P<c>[0-9, ]+)\],\s*b:'(?P<b>(?:[^'\\]|\\.)*)'\}",
        re.DOTALL,
    )
    movements = [
        {
            "r": m.group("r"),
            "title": unescape(m.group("t")),
            "chapters": [int(x) for x in m.group("c").split(",")],
            "blurb": unescape(m.group("b")),
        }
        for m in mv_pattern.finditer(mv_chunk)
    ]
    if not movements:
        sys.exit(f"MOVEMENTS block found but regex matched nothing in {path} — check the format by hand")

    ch_start = data.find("var CH={")
    ch_end = data.find("\n};", ch_start)
    if ch_start == -1 or ch_end == -1:
        sys.exit(f"no 'var CH={{...}}' block found in {path}")
    ch_chunk = data[ch_start:ch_end]

    ch_pattern = re.compile(
        r"(?P<n>\d+):\{t:'(?P<t>(?:[^'\\]|\\.)*)',d:'(?P<d>(?:[^'\\]|\\.)*)',m:(?P<m>\d+)(?:,h:1)?\}"
    )
    chapters = {
        int(m.group("n")): {
            "title": unescape(m.group("t")),
            "blurb": unescape(m.group("d")),
            "readMin": int(m.group("m")),
        }
        for m in ch_pattern.finditer(ch_chunk)
    }

    missing = [n for mv in movements for n in mv["chapters"] if n not in chapters]
    if missing:
        print(f"WARNING: {path} — chapter numbers in MOVEMENTS but missing from CH: {missing}", file=sys.stderr)

    book = {"project": None, "slug": slug, "title": title, "url": url, "movements": []}
    for mv in movements:
        entry = {"movement": mv["r"], "name": mv["title"], "blurb": mv["blurb"], "chapters": []}
        for n in mv["chapters"]:
            ch = chapters.get(n)
            entry["chapters"].append(
                {
                    "n": n,
                    "title": ch["title"] if ch else None,
                    "blurb": ch["blurb"] if ch else None,
                    "readMin": ch["readMin"] if ch else None,
                    "slug": None,
                    "url": f"{url}#{n}",
                }
            )
        book["movements"].append(entry)
    return book


if __name__ == "__main__":
    if len(sys.argv) != 5:
        sys.exit(__doc__)
    print(json.dumps(extract(*sys.argv[1:5]), indent=2, ensure_ascii=False))

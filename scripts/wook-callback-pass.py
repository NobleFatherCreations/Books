#!/usr/bin/env python3
"""Second 2026-09-10 pass: stale counts and wrong callbacks OUTSIDE the cold opens.

The cold-open audit only read THE DROP and "Tales From ... The Save" for each
chapter, so it could not see these. Verifying the whole book surfaced:

STALE CHAPTER COUNTS (same root cause as the cold-open ones -- the Encore grew
from 3 chapters to 6 and nothing that counted chapters was re-counted):
  - front matter, Kandi Trade definition: "across twenty-three chapters"
  - ch24 x2, ch25 x8 (incl. one hyphenated), ch26 x2

WRONG CHARACTER CALLBACKS (references to Save protagonists that name the wrong
person -- these are worse than the counts, because a reader who remembers the
chapter will trust their memory less, which is the exact opposite of what a
book about discernment wants):
  - ch21 credits Priya with photographing the wristband. That is Dani, in ch16.
    Priya, in ch16, is one of the friends who cannot remember Jess's last name.
  - ch25's Save-protagonist roster says "Priya from the yurt". The yurt Save
    protagonist is Preethi.
  - ch25's roster says "Dev from the hot springs". Dev is row 14 (ch15). The
    hot springs is Lena (ch4), who is already listed correctly on the same line.
  - ch25's roster says "Cara from the bus", which was correct until the
    cold-open pass renamed ch18's Save protagonist to Wren to stop her
    colliding with the Cara whose arc runs through ch21, ch24 and ch26.

Also finishes the name de-duplication the first pass started: Priya was doing
duty as four unrelated characters.

Run: python3 scripts/wook-callback-pass.py   (idempotent)
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WOOK = ROOT / "library/wook/index.html"

applied, skipped = [], []


def sub(html, label, old, new, count=1):
    global applied, skipped
    if new in html and old not in html:
        skipped.append(label)
        return html
    found = html.count(old)
    assert found == count, f"{label}: expected {count} of {old[:70]!r}, found {found}"
    applied.append(label)
    return html.replace(old, new, count)


def bounds(html, n):
    s = re.search(r'<div class="chwrap s\d" data-ch="%d">' % n, html)
    e = re.search(r'<i class="ch-end" data-ch="%d">' % n, html)
    return s.start(), e.start()


def sub_in_chapter(html, n, label, old, new, count=None):
    global applied, skipped
    a, b = bounds(html, n)
    chunk = html[a:b]
    if new in chunk and old not in chunk:
        skipped.append(label)
        return html
    found = chunk.count(old)
    if count is None:
        count = found
    assert found == count and count > 0, \
        f"{label}: expected {count} of {old[:70]!r} in ch{n}, found {found}"
    applied.append(f"{label} (x{count})")
    return html[:a] + chunk.replace(old, new, count) + html[b:]


def main():
    html = WOOK.read_text(errors="surrogateescape")
    before = len(html)

    # ------------------------------------------------------------------
    # Stale chapter counts
    # ------------------------------------------------------------------
    # Front matter: the Kandi Trade vow accumulates across the whole book.
    html = sub(html, "front matter: kandi accumulates 23->26",
        "Accumulates across twenty-three chapters.",
        "Accumulates across twenty-six chapters.")

    # ch24 is the one chapter about prevented harm; the other twenty-five
    # are the unprevented kind.
    html = sub(html, "ch24: unpreventable harm 23->25",
        "This book has twenty-three chapters of unpreventable harm.",
        "This book has twenty-five chapters of unpreventable harm.")

    # ch24's closing montage looks back across everything before it.
    html = sub(html, "ch24: full scene 21->23",
        "from across the full twenty-one chapters of the scene",
        "from across the full twenty-three chapters of the scene")

    # ch25: twenty-four chapters precede the confession.
    a25, b25 = bounds(html, 25)
    n25 = html[a25:b25].count("twenty-one chapters")
    html = sub_in_chapter(html, 25, "ch25: twenty-one chapters -> twenty-four",
        "twenty-one chapters", "twenty-four chapters", count=n25)
    html = sub(html, "ch25: hyphenated 21-chapter -> 24-chapter",
        "a twenty-one-chapter persuasion operation",
        "a twenty-four-chapter persuasion operation")

    # ch26: twenty-five chapters precede the closer.
    a26, b26 = bounds(html, 26)
    n26 = html[a26:b26].count("twenty-three chapters")
    html = sub_in_chapter(html, 26, "ch26: twenty-three chapters -> twenty-five",
        "twenty-three chapters", "twenty-five chapters", count=n26)

    # ------------------------------------------------------------------
    # Wrong character callbacks
    # ------------------------------------------------------------------
    # ch16's wristband photographer is Dani, not Priya.
    html = sub(html, "ch21: wristband credit Priya -> Dani",
        "By Priya photographing the wristband",
        "By Dani photographing the wristband")

    # The yurt Save protagonist is Preethi (ch3).
    html = sub(html, "ch25 roster: Priya from the yurt -> Preethi",
        "Priya from the yurt", "Preethi from the yurt")

    # Dev is row 14 (ch15). Lena is the hot springs, and is already on this line.
    html = sub(html, "ch25 roster: Dev from the hot springs -> row 14",
        "Dev from the hot springs", "Dev from row 14")

    # ch18's Save protagonist was renamed to Wren in the cold-open pass.
    html = sub(html, "ch25 roster: Cara from the bus -> Wren",
        "Cara from the bus", "Wren from the bus")

    # ------------------------------------------------------------------
    # Finish the Priya de-duplication
    # ------------------------------------------------------------------
    # ch1's Priya Chandrasekhar keeps the name (first and most established).
    # ch16's searching friend and ch19's Save protagonist get their own.
    html = sub_in_chapter(html, 16, "ch16: Priya -> Noor", "Priya", "Noor")
    html = sub_in_chapter(html, 19, "ch19: Priya -> Anjali", "Priya", "Anjali")

    WOOK.write_text(html, errors="surrogateescape")
    print(f"wook: {before:,} -> {len(html):,} bytes\n")
    print(f"applied {len(applied)}:")
    for a_ in applied:
        print(f"  + {a_}")
    if skipped:
        print(f"\nskipped {len(skipped)} (already applied):")
        for s in skipped:
            print(f"  = {s}")


if __name__ == "__main__":
    sys.exit(main())

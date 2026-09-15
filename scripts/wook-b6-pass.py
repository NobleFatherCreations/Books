#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pass B6 of the full review: chapters 21-23, every section.

See content/wook-audits/wook-full-review-plan.md.

Idempotent.

Run: python3 scripts/wook-b6-pass.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WOOK = ROOT / "library/wook/index.html"

log = []


def note(step, n, what):
    log.append((step, n, what))


def fix_ch23_chapter_count(src):
    """Chapter 23 states its own distance from chapter 1 two different ways
    within the same section: "twenty chapters later" here, "twenty-two
    chapters" two sentences later for what is explicitly the same span
    (the mirror checks running since chapter 1). Twenty-three minus one is
    twenty-two; the second figure is the one the rest of the chapter uses
    and the one that is arithmetically correct.
    """
    old = ("which is now, twenty chapters later, going to receive the "
           "fuller answer.")
    new = ("which is now, twenty-two chapters later, going to receive "
           "the fuller answer.")
    if new in src:
        note("ch23-count", 0, "already corrected")
        return src
    if old not in src:
        sys.exit("ch23: chapter-count sentence not found in its expected form")
    src = src.replace(old, new, 1)
    note("ch23-count", 1,
         "self-reference now agrees with the 'twenty-two chapters' used "
         "two sentences later for the same span")
    return src


STEPS = [fix_ch23_chapter_count]


def main():
    src = WOOK.read_text(encoding="utf-8")
    before = len(src)
    for step in STEPS:
        src = step(src)
    WOOK.write_text(src, encoding="utf-8")
    width = max(len(s) for s, _, _ in log) if log else 0
    for step, n, what in log:
        print(f"  {step:<{width}}  {n:>3}  {what}")
    print(f"\n{before:,} -> {len(src):,} bytes")


if __name__ == "__main__":
    main()

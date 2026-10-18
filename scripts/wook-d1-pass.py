#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pass D1 of the full review: book-wide coherence.

See content/wook-audits/wook-full-review-plan.md.

Idempotent.

Run: python3 scripts/wook-d1-pass.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WOOK = ROOT / "library/wook/index.html"

log = []


def note(step, n, what):
    log.append((step, n, what))


def fix_sister_lou_tenure(src):
    """Chapter 16 says Sister Lou has run the briefing for twelve years;
    every other mention in the book -- nine of them, in chapters 20, 21
    and the appendices -- says eleven. Eleven is the established figure
    everywhere it actually matters (her own chapters), so the chapter 16
    outlier is corrected to match.
    """
    bad = "Sister Lou has been running it for twelve years"
    n = src.count(bad)
    if n == 0:
        note("sister-lou-tenure", 0, "already corrected")
        return src
    if n > 1:
        sys.exit("ch16: Sister Lou tenure sentence matched more than once")
    src = src.replace(bad, "Sister Lou has been running it for eleven years", 1)
    note("sister-lou-tenure", 1,
         "outlier corrected from twelve to eleven years, matching the "
         "other nine mentions across the book")
    return src


STEPS = [fix_sister_lou_tenure]


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

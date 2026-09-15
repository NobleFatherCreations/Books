#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pass B4 of the full review: chapters 14-17, every section.

See content/wook-audits/wook-full-review-plan.md.

Idempotent.

Run: python3 scripts/wook-b4-pass.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WOOK = ROOT / "library/wook/index.html"

log = []


def note(step, n, what):
    log.append((step, n, what))


def fix_ch15_stray_label(src):
    """Chapter 15's Bridge ends with a stray, wrong trailing chapter label.

    Chapters 1 and 2 end their Bridge with a plain <p>Chapter N</p> naming
    the chapter that follows (Chapter 2, Chapter 3). Chapter 15 has the same
    tag, but it says "Chapter  14" -- a double space and the wrong number,
    fifteen chapters removed from ch16, which is the chapter that actually
    follows. The other 23 chapters have no such label at all, so this is a
    stray leftover rather than a load-bearing structural element -- fixed
    to the correct number rather than removed, matching what chapters 1
    and 2 do with the same tag.
    """
    old = "<p>Chapter  14</p></section><i class=\"ch-end\" data-ch=\"15\">"
    new = "<p>Chapter 16</p></section><i class=\"ch-end\" data-ch=\"15\">"
    if new in src:
        note("ch15-label", 0, "already corrected")
        return src
    if old not in src:
        sys.exit("ch15: stray trailing label not found in its expected form")
    src = src.replace(old, new, 1)
    note("ch15-label", 1, "stray 'Chapter  14' corrected to 'Chapter 16'")
    return src


STEPS = [fix_ch15_stray_label]


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

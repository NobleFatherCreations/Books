#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pass B2 of the full review: chapters 6-9, every section.

See content/wook-audits/wook-full-review-plan.md.

Idempotent.

Run: python3 scripts/wook-b2-pass.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WOOK = ROOT / "library/wook/index.html"

log = []


def note(step, n, what):
    log.append((step, n, what))


def fix_ch8_mateo_naming(src):
    """The hoop artist is "Hooper" (a category, not a name) for a full
    paragraph, then the narrator starts calling him Mateo with no on-page
    source for the name. Chapter 7's bridge already knows him as Mateo, but
    a reader will not be holding that bridge in memory several hundred
    words into the next chapter.

    The fix stays in the narrator's own voice: he is established, in this
    same cold open, as someone who reads a Pelican case and a laminated
    price card for tenure -- so having him clock a name off the gear is the
    same character trait, not a new one, and it gives "Mateo" a source in
    the paragraph where he first uses it.
    """
    old = ('He picks up the hoop.</p><p>I smile. “Of course. Blessings.”')
    new = ('He picks up the hoop. His gear bag has a competition bib '
           'still zip-tied to the strap, faded, a name and a year on it: '
           'MATEO, 2019.</p><p>I smile. “Of course. Blessings.”')
    if 'MATEO, 2019' in src:
        note("ch8-mateo", 0, "already grounded")
        return src
    if old not in src:
        sys.exit("ch8: hoop artist exit line not found in its expected form")
    src = src.replace(old, new, 1)
    note("ch8-mateo", 1, "the name Mateo now has a source inside ch8 itself")
    return src


STEPS = [fix_ch8_mateo_naming]


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

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pass A2 of the full review: what the extended continuity checker found.

See content/wook-audits/wook-full-review-plan.md. This pass added four
checks to scripts/wook-continuity-check.py -- cards, index, numbering,
dropnames -- and this applies what they turned up.

Three of the four came back clean on the whole book, which is worth
recording: Track numbers run 01..N in all 26 chapters, every poster key
line names a Track that chapter actually has, and all 114 counter-drop
names in Appendix F are unique.

Idempotent.

Run: python3 scripts/wook-a2-pass.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WOOK = ROOT / "library/wook/index.html"

log = []


def note(step, n, what):
    log.append((step, n, what))


def fix_ch10_double_read(src):
    """Chapter 10's last Track carried two THE READ blocks.

    The second holds one paragraph -- the exit narrative your partner
    prepared before you needed one -- which belongs to that Track and reads
    as a continuation of the first. So this folds the paragraph into the
    first block rather than moving it anywhere; the defect was the second
    header, not the content.
    """
    stray = ('</div><div class="subplain"><p class="plain-tag">🧠 THE READ</p>'
             '<p>The sentence “we’ve been having problems” is the tell.')
    if stray not in src:
        note("ch10-double-read", 0, "already merged")
        return src
    if src.count(stray) != 1:
        sys.exit("ch10: expected exactly one stray READ block")
    src = src.replace(stray, '<p>The sentence “we’ve been having problems” is the tell.', 1)
    note("ch10-double-read", 1,
         "second THE READ header folded into the Track's first one")
    return src


def fix_trifecta_entry(src):
    """Appendix A calls itself an index of every named Track, and filed the
    Trifecta under chapter 1 as though it were one.

    It is the book's opening diagnostic, introduced in chapter 1's Fanny
    Pack, and readers will look for it here -- so it stays, labelled for
    what it is instead of wearing a Track's clothes.
    """
    old = ('<p>The Trifecta — Pattern · Intent · Refusal To Change '
           '(coercive-control diagnostic) → Counter: Name the pattern '
           'specifically. Require behavior change, not explanation.</p>')
    new = ('<p><em>The chapter’s diagnostic, not one of its Tracks:</em> '
           'The Trifecta — Pattern · Intent · Refusal To Change → Counter: '
           'Name the pattern specifically. Require behavior change, not '
           'explanation.</p>')
    if new in src:
        note("trifecta-entry", 0, "already labelled")
        return src
    if old not in src:
        sys.exit("appendix A: Trifecta entry not found in its expected form")
    src = src.replace(old, new, 1)
    note("trifecta-entry", 1, "the Trifecta no longer reads as a Track")
    return src


STEPS = [fix_ch10_double_read, fix_trifecta_entry]


def main():
    src = WOOK.read_text(encoding="utf-8")
    before = len(src)
    for step in STEPS:
        src = step(src)
    WOOK.write_text(src, encoding="utf-8")
    width = max(len(s) for s, _, _ in log)
    for step, n, what in log:
        print(f"  {step:<{width}}  {n:>3}  {what}")
    print(f"\n{before:,} -> {len(src):,} bytes")


if __name__ == "__main__":
    main()

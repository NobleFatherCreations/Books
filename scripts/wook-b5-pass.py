#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pass B5 of the full review: chapters 18-20, every section.

See content/wook-audits/wook-full-review-plan.md.

Idempotent.

Run: python3 scripts/wook-b5-pass.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WOOK = ROOT / "library/wook/index.html"

log = []


def note(step, n, what):
    log.append((step, n, what))


def fix_ch19_bridge(src):
    """Chapter 19's Bridge describes chapter 21, mislabeled as chapter 20.

    "Sister Lou at the gate with a clipboard... running this briefing for
    eleven straight years" is chapter 21's cold open verbatim (its own
    opening line is "Sister Lou is standing at the camp's designated
    briefing spot"). Chapter 20 is actually Ines's drive home and the
    Comedown Text -- the re-entry window, not a pre-event briefing. Every
    other Bridge in the book previews the chapter immediately following;
    this one skipped 20 and jumped to 21's content while still saying
    "Chapter 20." Rewritten to preview what chapter 20 actually is.
    """
    old = ("The room has windows. Chapter 20 is Sister Lou at the gate "
           "with a clipboard and a printed sheet and the specific "
           "authority of someone who has been running this briefing for "
           "eleven straight years, and nobody flakes, and the reason "
           "nobody flakes is that everybody already knows what happens "
           "in the chapters before this one.")
    new = ("The room has windows. Chapter 20 is Ines on the seven-hour "
           "drive home with the wristband still on her wrist, and the "
           "first text from the festival arrives before the tent is even "
           "dry, aimed at the thirty-six hours when she is least equipped "
           "to answer it.")
    if new in src:
        note("ch19-bridge", 0, "already fixed")
        return src
    if old not in src:
        sys.exit("ch19: bridge sentence not found in its expected form")
    src = src.replace(old, new, 1)
    note("ch19-bridge", 1, "bridge now previews ch20's actual content instead of ch21's")
    return src


STEPS = [fix_ch19_bridge]


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

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Resolve the four duplicate Counter-Drop names, retire the one Track name
that breaks the forbidden-register rule, and repair the stale chapter tags
in the Appendix F master list.

A counter-drop is the thing the book most wants a reader to be able to say
out loud, so two different procedures answering to one name is the single
collision the book cannot afford. Each keeper was chosen by which chapter
the name actually describes:

  The Clean Plate Protocol  kept at ch16 (a gift/a pour), ch1 -> The Favor Ledger
  The Temperature Check     kept at ch2 (it probes warmth), ch8 -> The Draft Check
  The Plain English ...     kept at ch7, ch23 -> The Tuesday Translation
  The Pattern Map           kept at ch29 (maps your own patterns),
                            ch23 -> The Sleeping Chart (it is literally a
                            map of who sleeps where on the bus)

Track rename: THE GIFT-FRAMEWORK GRIFT -> THE UNPAID HEADLINER. "Framework"
is banned in Track names, and the new name is what the move actually is:
you are the draw and you are free.

Appendix F repairs: three tags carried pre-expansion chapter numbers, and
one entry named a counter-drop that does not exist ("The Dose Plan (Ch11)"
-- the real one is "The Pre-Set Dose Plan" in ch5).

Idempotent: every edit asserts its expected occurrence count, and a second
run is a no-op.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WOOK = ROOT / "library/wook/index.html"

# (old, new, expected count) -- applied to the whole document, so each
# string is chosen to be unambiguous on its own.
EDITS = [
    # --- back-matter counter lists (these live outside any chwrap, so the
    #     chapter-scoped sweep below cannot reach them). Each string is
    #     unambiguous because it carries its own Track name. ---
    ('The Covert Facilitator (ingratiation grooming) → Counter: The Clean Plate Protocol',
     'The Covert Facilitator (ingratiation grooming) → Counter: The Favor Ledger', 1),
    ('The “We Don’t Do That Here” Soft Exile (norms enforcement as ostracism) → Counter: The Temperature Check',
     'The “We Don’t Do That Here” Soft Exile (norms enforcement as ostracism) → Counter: The Draft Check', 1),
    ('The Sister Word (linguistic capture/lexicon control) → Counter: The Plain English Translation',
     'The Sister Word (linguistic capture/lexicon control) → Counter: The Tuesday Translation', 1),
    ('The Bus Hierarchy (age-based sexual access stratification) → Counter: The Pattern Map',
     'The Bus Hierarchy (age-based sexual access stratification) → Counter: The Sleeping Chart', 1),
    # twice: once as the Track's own clinical anchor in ch9, once in the
    # back-matter counter list. Same replacement both times.
    ('The Gift-Framework Grift (labor extraction via reciprocity norms)',
     'The Unpaid Headliner (labor extraction via reciprocity norms)', 2),
    ('The Gift-Framework Grift — Asymmetrical application of gift-economy value',
     'The Unpaid Headliner — Asymmetrical application of gift-economy value', 1),

    # --- Appendix F: stale chapter tags ---
    ('The Temperature Check (Ch2/Ch8/Ch19)', 'The Temperature Check (Ch2)', 1),
    ('The Plain English Translation (Ch7/Ch21)', 'The Plain English Translation (Ch7)', 1),
    ('The Pattern Map (Ch21/Ch25)', 'The Pattern Map (Ch29)', 1),
    # "The Dose Plan (Ch11)" named a counter-drop that does not exist and
    # pointed at a chapter that does not contain it. The real one is
    # "The Pre-Set Dose Plan (Ch5)", which Appendix F already lists in its
    # correct alphabetical slot -- so this stale entry is deleted, not
    # renamed, or the list ends up carrying it twice.
    ('The Dose Plan (Ch11) · ', '', 1),
]

# New Appendix F entries, inserted alphabetically. (entry, the entry it
# should be placed immediately before)
INSERTS = [
    ('The Draft Check (Ch8)', 'The Dump-It-Now Protocol (Ch12)'),
    ('The Favor Ledger (Ch1)', 'The Five-Minute FOMO Freeze (Ch2)'),
    ('The Sleeping Chart (Ch23)', 'The Supply Independence Plan (Ch5)'),
    ('The Tuesday Translation (Ch23)', 'The Two-Anchor System (Ch5)'),
]

# In-chapter references beyond the counter-drop card itself.
SCOPED = [
    (1, "The Clean Plate Protocol", "The Favor Ledger"),
    (8, "The Temperature Check", "The Draft Check"),
    (23, "The Plain English Translation", "The Tuesday Translation"),
    (23, "The Pattern Map", "The Sleeping Chart"),
    (9, "The Gift-Framework Grift", "The Unpaid Headliner"),
    (9, "THE GIFT-FRAMEWORK GRIFT", "THE UNPAID HEADLINER"),
    (9, "Gift-Framework Grift", "Unpaid Headliner"),
]


def main():
    raw = WOOK.read_text(errors="surrogateescape")
    applied = skipped = 0

    for old, new, expect in EDITS:
        n = raw.count(old)
        if n == 0 and raw.count(new):
            skipped += 1
            continue
        if n != expect:
            raise SystemExit(f"expected {expect} of {old[:70]!r}, found {n}")
        raw = raw.replace(old, new)
        applied += 1

    for entry, before in INSERTS:
        if entry in raw:
            skipped += 1
            continue
        if before not in raw:
            raise SystemExit(f"anchor not found for insert: {before!r}")
        raw = raw.replace(before, f"{entry} · {before}", 1)
        applied += 1

    # chapter-scoped sweeps for any remaining in-body references
    starts = {int(m.group(1)): m.start() for m in
              re.finditer(r'<div class="chwrap s\d" data-ch="(\d+)">', raw)}
    ends = {int(m.group(1)): m.start() for m in
            re.finditer(r'<i class="ch-end" data-ch="(\d+)">', raw)}
    for ch, old, new in SCOPED:
        s, e = starts[ch], ends[ch]
        seg = raw[s:e]
        if old in seg:
            hits = seg.count(old)
            raw = raw[:s] + seg.replace(old, new) + raw[e:]
            print(f"  ch{ch}: {hits}x {old!r} -> {new!r}")
            applied += hits
            starts = {int(m.group(1)): m.start() for m in
                      re.finditer(r'<div class="chwrap s\d" data-ch="(\d+)">', raw)}
            ends = {int(m.group(1)): m.start() for m in
                    re.finditer(r'<i class="ch-end" data-ch="(\d+)">', raw)}

    WOOK.write_text(raw, errors="surrogateescape")
    print(f"{applied} edit(s) applied, {skipped} already done")
    return 0


if __name__ == "__main__":
    sys.exit(main())

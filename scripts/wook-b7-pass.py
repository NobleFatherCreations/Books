#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pass B7 of the full review: chapters 24-26, every section.

See content/wook-audits/wook-full-review-plan.md.

Idempotent.

Run: python3 scripts/wook-b7-pass.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WOOK = ROOT / "library/wook/index.html"

log = []


def note(step, n, what):
    log.append((step, n, what))


def fix_ch25_confession_ten(src):
    """Confession Ten's Mara reference points at the wrong chapter too.

    Mara "Hot Water" Delgado's four Soundboard-Quote appearances are
    explicit and numbered in her own attributions: chapter 4 (first),
    chapter 13 ("Second appearance in the book"), chapter 18 (third,
    unlabelled but confirmed by elimination), chapter 22 ("Fourth and
    final appearance"). She does not appear in chapter 19 at all. Same
    renumbering-drift family as Confession Nine.
    """
    bad = "By Chapter 19, when Mara appears for the third time"
    n = src.count(bad)
    if n == 0:
        note("ch25-confession-ten", 0, "already corrected")
        return src
    if n > 1:
        sys.exit("ch25: Confession Ten's Mara sentence matched more than once")
    src = src.replace(bad, "By Chapter 18, when Mara appears for the third time", 1)
    note("ch25-confession-ten", 1, "Mara's third appearance corrected to ch18")
    return src


def fix_ch25_confession_nine(src):
    """Confession Nine misattributes three Kandi Trade vows to the wrong
    chapters -- the same three-chapter-insertion renumbering bug behind
    every other continuity defect in this book (The Road inserted at 11,
    The Free One at 13, The Re-Entry Window at 20).

    "Cooking something on Tuesdays and calling the sister" is chapter 19's
    vow verbatim ("I will cook something on a Tuesday. I will call the
    person I have not called in a while"), not chapter 17's (which is
    about supply-source discipline). "The inventory" and "name the name
    and write it down" are chapter 23's vow verbatim ("I will make the
    inventory... I know the name"), not chapter 20's (the re-entry-window
    vow, about not deciding in the window). 19 and 23 are exactly 17 and
    20 shifted by the two insertions (at 11, 13) and all three (at 11, 13,
    20) respectively -- textbook drift from the same root cause.

    The vow count follows: 22 Kandi Trades precede chapter 23 (chapters
    1-22), not 20.
    """
    old = ("By Chapter 17\u2019s Kandi Trade, the vows were about internal "
           "identity and practice, about cooking something on Tuesdays and "
           "calling the sister and doing the non-scene thing. By Chapter "
           "20\u2019s Kandi Trade, the vow was the inventory")
    new = ("By Chapter 19\u2019s Kandi Trade, the vows were about internal "
           "identity and practice, about cooking something on Tuesdays and "
           "calling the sister and doing the non-scene thing. By Chapter "
           "23\u2019s Kandi Trade, the vow was the inventory")
    n = src.count(old)
    if n == 0 and new in src:
        note("ch25-confession-nine-a", 0, "already corrected")
    elif n == 1:
        src = src.replace(old, new, 1)
        note("ch25-confession-nine-a", 1,
             "chapter 17->19 and 20->23 misattributions corrected")
    else:
        sys.exit("ch25: Confession Nine's first sentence not found as expected")

    old2 = ("By Chapter 20, when the Kandi Trade asks you to name the name "
           "and write it down, you have made twenty prior vows")
    new2 = ("By Chapter 23, when the Kandi Trade asks you to name the name "
           "and write it down, you have made twenty-two prior vows")
    n2 = src.count(old2)
    if n2 == 0 and new2 in src:
        note("ch25-confession-nine-b", 0, "already corrected")
    elif n2 == 1:
        src = src.replace(old2, new2, 1)
        note("ch25-confession-nine-b", 1,
             "chapter number and prior-vow count both corrected to match ch23")
    else:
        sys.exit("ch25: Confession Nine's second sentence not found as expected")
    return src


def fix_ch25_vow_count(src):
    """Chapter 25's Confession Fourteen undercounts its own vow.

    "PROTECT THE F*CKING MAGIC" closes every chapter's Kandi Trade from
    chapter 1 through chapter 25 itself, verified against the live text:
    25 chapters, 25 occurrences, no gaps. "By the time you finish Chapter
    25's Kandi Trade" the count is 25, not 22.
    """
    bad = "\u201cprotect the fucking magic\u201d twenty-two times"
    n = src.count(bad)
    if n == 0:
        note("ch25-vow-count", 0, "already corrected")
        return src
    if n > 1:
        sys.exit("ch25: vow-count phrase matched more than once, expected exactly one")
    src = src.replace(bad, "\u201cprotect the fucking magic\u201d twenty-five times", 1)
    note("ch25-vow-count", 1,
         "vow count corrected to 25, matching every chapter 1-25 verified live")
    return src


def fix_ch26_chapter_map(src):
    """Chapter 26's own summary of the book misattributes recovery,
    accountability and confession to the wrong chapters -- the same
    three-chapter-insertion drift (The Road at 11, The Free One at 13,
    The Re-Entry Window at 20) behind every other defect in this family.

    Verified against the live chapters' own subtitles and content:
    chapter 22 is explicitly subtitled "RECOVERY, THE 3 A.M. ENCORE, AND
    RE-ENTRY"; chapter 23 is explicitly subtitled "THE FULL ACCOUNTABILITY
    SET"; chapter 25 is where the Author's Wook Confession is delivered in
    full (chapter 23 only delivers it "first," per chapter 25's own
    Confession Sixteen). "Chapters 19 through 21" for recovery, "Chapter
    20" for accountability, and "Chapter 22" for confession are all off by
    the same drift pattern. "The warnings are in Chapters 1 through 16" is
    left alone -- a real range, not a single mis-pointed reference, and
    not contradicted by any other passage in the book.
    """
    bad = ("The recovery is in Chapters 19 through 21. The accountability "
           "is in Chapter 20. The confession is in Chapter 22.")
    n = src.count(bad)
    if n == 0:
        note("ch26-chapter-map", 0, "already corrected")
        return src
    if n > 1:
        sys.exit("ch26: chapter-map sentence matched more than once")
    new = ("The recovery is in Chapter 22. The accountability is in "
           "Chapter 23. The confession is in Chapter 25.")
    src = src.replace(bad, new, 1)
    note("ch26-chapter-map", 1,
         "recovery/accountability/confession pointers corrected to 22/23/25")
    return src


def fix_ch26_pillar_three(src):
    """Pillar Three misattributes its own source chapter.

    "What would I still be if I could not attend festivals for a year?" is
    chapter 19's own Identity Erosion Drift question verbatim, not chapter
    17's (which is about supply-source dependency). Same renumbering
    drift as the other chapter-26 fixes.
    """
    bad = "This is Chapter 17\u2019s construction side."
    n = src.count(bad)
    if n == 0:
        note("ch26-pillar-three", 0, "already corrected")
        return src
    if n > 1:
        sys.exit("ch26: Pillar Three's chapter reference matched more than once")
    src = src.replace(bad, "This is Chapter 19\u2019s construction side.", 1)
    note("ch26-pillar-three", 1, "Identity Floor's source chapter corrected to 19")
    return src


def fix_ch26_pillar_four(src):
    """Pillar Four misattributes its own source chapter three times.

    The closed-door audit and the capacity-state accountability question
    both belong to chapter 23 (THE FULL ACCOUNTABILITY SET), not chapter
    20 (the re-entry-window chapter). Same drift family.
    """
    n = 0
    bad1 = "The accountability practice is Chapter 20\u2019s maintenance routine."
    if bad1 in src:
        src = src.replace(bad1, "The accountability practice is Chapter 23\u2019s maintenance routine.", 1)
        n += 1
    bad2 = "the same clarity you have been examining everyone else\u2019s for twenty-five chapters."
    # left as-is: this is a separate, correct count (chapters 1-25 precede ch26's summary here)
    bad3 = "If yes: Chapter 20.\u003c/p\u003e\u003cp\u003eThe quarterly closed-door audit from Chapter 20 runs"
    old3 = "If yes: Chapter 20.</p><p>The quarterly closed-door audit from Chapter 20 runs"
    if old3 in src:
        src = src.replace(
            old3,
            "If yes: Chapter 23.</p><p>The quarterly closed-door audit from Chapter 23 runs", 1)
        n += 1
    note("ch26-pillar-four", n,
         "three accountability-chapter references corrected from 20 to 23")
    return src


def fix_ch26_mirror_count(src):
    """The Last Mirror undercounts the mirrors that precede it.

    Every one of chapters 1 through 25 carries a "Have You Been The Wook?"
    mirror section, verified against the live text -- 25 chapters, 25
    mirrors, no gaps. "Twenty-three chapters of mirrors" is short by two,
    the same span the book's insertions added.
    """
    bad = "Twenty-three chapters of mirrors."
    n = src.count(bad)
    if n == 0:
        note("ch26-mirror-count", 0, "already corrected")
        return src
    if n > 1:
        sys.exit("ch26: mirror-count sentence matched more than once")
    src = src.replace(bad, "Twenty-five chapters of mirrors.", 1)
    note("ch26-mirror-count", 1, "mirror count corrected to 25, matching every chapter 1-25 verified live")
    return src


def fix_ch26_discog_reference(src):
    """Chapter 26's Discog entry misdates David Reyes's reckoning.

    David Reyes's accountability chapter is 23, not 20 -- same drift
    family as this chapter's other three fixes.
    """
    bad = "David Reyes at the first festival after Chapter 20."
    n = src.count(bad)
    if n == 0:
        note("ch26-discog", 0, "already corrected")
        return src
    if n > 1:
        sys.exit("ch26: Discog's David Reyes sentence matched more than once")
    src = src.replace(bad, "David Reyes at the first festival after Chapter 23.", 1)
    note("ch26-discog", 1, "David Reyes's reckoning chapter corrected to 23")
    return src


def fix_ch24_bridge_count(src):
    """Chapter 24's Bridge conflates two different numbers from its own
    Save. The Save is explicit and states each figure separately: "The
    thread is seven women now" (Signal-thread membership) versus "The
    napkin is now four cases in a legal consultation" (the legal clinic's
    case count, which includes the seventh woman plus three unrelated
    prior cases -- not all seven thread members). The Bridge merged them
    into "seven women in a legal consultation," which neither sentence in
    the Save actually says.

    "The napkin is now four cases in a legal consultation" already exists
    verbatim in the Save, so a plain substring check for the fixed text
    would false-positive against that line -- this counts occurrences of
    the wrong phrase specifically instead.
    """
    bad = "The napkin is now seven women in a legal consultation"
    n = src.count(bad)
    if n == 0:
        note("ch24-bridge", 0, "already corrected")
        return src
    if n > 1:
        sys.exit("ch24: bridge phrase matched more than once, expected exactly one")
    src = src.replace(bad, "The napkin is now four cases in a legal consultation", 1)
    note("ch24-bridge", 1,
         "bridge count now matches the Save's own 'four cases' line "
         "instead of conflating it with the seven-woman thread")
    return src


STEPS = [fix_ch25_confession_nine, fix_ch25_confession_ten, fix_ch25_vow_count, fix_ch26_chapter_map, fix_ch26_pillar_three, fix_ch26_pillar_four, fix_ch26_mirror_count, fix_ch26_discog_reference, fix_ch24_bridge_count]


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

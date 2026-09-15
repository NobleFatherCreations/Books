#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pass B1 of the full review: chapters 1-5, every section.

See content/wook-audits/wook-full-review-plan.md. This carries what the
reading turns up, chapter by chapter, plus one book-wide mechanical class
that the reading exposed and the proofreader now checks for.

Idempotent.

Run: python3 scripts/wook-b1-pass.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WOOK = ROOT / "library/wook/index.html"

log = []


def note(step, n, what):
    log.append((step, n, what))


# Book-wide, found while reading chapter 1's rail label. A title-casing
# script ran over the nav labels at some point and capitalised the S after
# an apostrophe, and lowercased an initialism. The rail uppercases so it
# hides there; the Setlist and the nav drawer do not, so both show it.
TITLECASE = [
    ("It’S Not Drama, It’S Warfare", "It’s Not Drama, It’s Warfare"),
    ("The Taper’S Reveal", "The Taper’s Reveal"),
    ("Chapter 15 · The Rv", "Chapter 15 · The RV"),
    ('<span class="n">15</span>The Rv</a>', '<span class="n">15</span>The RV</a>'),
    ('<span class="sl-t">The Rv</span>', '<span class="sl-t">The RV</span>'),
]


def fix_titlecase(src):
    n = 0
    for old, new in TITLECASE:
        if old in src:
            n += src.count(old)
            src = src.replace(old, new)
    note("titlecase", n, "title-casing artifacts in nav labels and rails")
    return src


def fix_ch1_repeat(src):
    """Chapter 1 tells the same joke twice, 700 words apart.

    THE WOOK'S SETLIST previews the Overt Lot Rat with the calendar-app
    line, and THE BEHAVIOR then opens on it verbatim. The preview is the
    one that should change: the Track body is where the joke belongs, and
    the preview's job is to say what the front is.
    """
    old = ("The Overt Lot Rat — loud, obvious, grabby, immediate. Does not "
           "have a long game because that would require a calendar app and "
           "object permanence.")
    new = ("The Overt Lot Rat — loud, obvious, grabby, immediate. Takes what "
           "is in reach while you are deciding whether to be polite about it.")
    if new in src:
        note("ch1-repeat", 0, "already varied")
        return src
    if old not in src:
        sys.exit("ch1: setlist preview not found in its expected form")
    src = src.replace(old, new, 1)
    note("ch1-repeat", 1, "the calendar-app joke now lands once, in the Track")
    return src


def fix_ch2_bridge_typo(src):
    """Chapter 2's bridge garbles its own forward reference.

    Two errors in one sentence: "markdown director" for "marketing
    director" (Nadia's actual title, established in ch3's own cold open
    and Tapers Section), and "two thousand dollars" where ch3 is
    specific and repeated about \$2,400. The bridge is the only place
    either number/word drifted.
    """
    old = ('the markdown director who writes bias memos is Venmo-ing two '
           'thousand dollars to a woman she met ninety-three minutes ago '
           'in a yurt')
    new = ('the marketing director who writes bias memos is Venmo-ing '
           'twenty-four hundred dollars to a woman she met two hours '
           'ago in a yurt')
    if new in src:
        note('ch2-bridge', 0, 'already fixed')
        return src
    if old not in src:
        sys.exit('ch2: bridge sentence not found in its expected form')
    src = src.replace(old, new, 1)
    note('ch2-bridge', 1, "bridge's forward reference now matches ch3's own facts")
    return src


def fix_ch4_dani_collision(src):
    """Chapter 4 has two different Danis in the same chapter.

    The cold open's Dani is Jade's friend who tracks her GPS ping. The
    Save's protagonist is Lena, a different POV entirely -- and her own
    camp-breakfast friend is also called Dani. Same chapter, two unrelated
    people sharing a name, which is the exact defect family the recurring-
    cast passes exist to catch, just not caught here because Lena's Dani
    never appears anywhere the callback/roster checks look.
    """
    i = src.find("Tales From The Hot Springs Run")
    j = src.find("THE FANNY PACK", i)
    if i == -1 or j == -1:
        sys.exit("ch4: Save section not found")
    block = src[i:j]
    if "Naomi" in block:
        note("ch4-dani", 0, "already renamed")
        return src
    n = block.count("Dani")
    if n != 3:
        sys.exit("ch4: expected 3 occurrences of Dani in the Save, found %d" % n)
    block = block.replace("Dani", "Naomi")
    note("ch4-dani", n, "Lena's Save-only friend renamed off Jade's Dani")
    return src[:i] + block + src[j:]


def fix_ch1_hopper_age(src):
    """Hopper's arithmetic contradicts his own discography.

    The cold open has him at forty-one, "doing this for twenty-one years,"
    which puts the start at twenty. The Wook Discog's Studio Debut has him
    at twenty-two, at his first big festival, explicitly "not yet knowing he
    is running plays." Nineteen years makes the two agree and changes
    nothing else.
    """
    old = "Hopper has been doing this for twenty-one years"
    new = "Hopper has been doing this for nineteen years"
    if new in src:
        note("ch1-hopper-age", 0, "already reconciled")
        return src
    if old not in src:
        sys.exit("ch1: Hopper's tenure not found in its expected form")
    src = src.replace(old, new, 1)
    note("ch1-hopper-age", 1, "Hopper's tenure now agrees with his Studio Debut")
    return src


STEPS = [fix_titlecase, fix_ch1_repeat, fix_ch1_hopper_age, fix_ch2_bridge_typo, fix_ch4_dani_collision]


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

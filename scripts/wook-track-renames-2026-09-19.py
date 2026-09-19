#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rename the eight Track names from the expansion that fail the PLURth
Angel test, replacing policy-brief nouns with scene-coded ones.

The 2026-09-19 voice audit measured zero scene nouns and zero
quoted-dialogue constructions across all 25 Tracks added by the
seven-chapter expansion, against 29 and 10 in the original 139. These
eight were the worst offenders:

  ch10  The Off-Season Problem   -> The November Cliff
  ch10  The Promotion That Isn't -> The Lanyard Raise      (ch10's own image)
  ch14  The Wellness-Threat Sort -> The Two Tents          (echoes ch14's title)
  ch14  The Credibility Gap      -> The Default Story      ("default world" family)
  ch14  The Pre-Loaded Tax       -> The Invisible Shift
  ch17  The Unverifiable Lineage -> The Borrowed Grandmother
  ch26  The Persistence Frame    -> The Devotion Cover     ("___ Cover" family)
  ch26  The Porous Scene         -> The Open Phonebook

Each name is unique to its chapter, so a document-wide replacement is
safe; it also catches the Appendix A index entry, the back-matter counter
list, the chapter poster's key line, the Wook's Setlist roster and the
Fanny Pack, which all carry the name. Case is preserved, because the book
uses the ALL-CAPS form on posters and Track headers, Title Case in
rosters, and lowercase mid-sentence in the Runs In Every Direction cards.

Idempotent: a name already renamed is reported and skipped.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WOOK = ROOT / "library/wook/index.html"

RENAMES = [
    ("Off-Season Problem", "November Cliff", 7),
    ("Promotion That Isn’t", "Lanyard Raise", 7),
    ("Wellness-Threat Sort", "Two Tents", 5),
    ("Credibility Gap", "Default Story", 7),
    ("Pre-Loaded Tax", "Invisible Shift", 6),
    ("Unverifiable Lineage", "Borrowed Grandmother", 5),
    ("Persistence Frame", "Devotion Cover", 6),
    ("Porous Scene", "Open Phonebook", 6),
]


def cased_like(sample, new):
    """Return `new` in the same case style as the matched `sample`."""
    if sample.isupper():
        return new.upper()
    if sample.islower():
        return new.lower()
    return new


def main():
    raw = WOOK.read_text(errors="surrogateescape")
    total = 0
    for old, new, expect in RENAMES:
        pat = re.compile(re.escape(old), re.I)
        found = len(pat.findall(raw))
        if found == 0 and re.search(re.escape(new), raw, re.I):
            print(f"  already renamed: {old} -> {new}")
            continue
        if found != expect:
            raise SystemExit(f"{old!r}: expected {expect} occurrences, found {found}")
        raw = pat.sub(lambda m: cased_like(m.group(0), new), raw)
        print(f"  {found}x  {old:24} -> {new}")
        total += found
    WOOK.write_text(raw, errors="surrogateescape")
    print(f"{total} replacement(s) across 8 Track renames")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit every chapter cross-reference in the seven new chapters against
the old-to-new chapter map in content/wook-audits/wook-expansion-plan.md.

The single largest defect family in this book's history is a cross-
reference written before a chapter was inserted and never renumbered.
The expansion adds seven chapters at once, so every "Chapter N" written
into a new fragment has to mean the chapter it will sit next to *after*
the splice, not the one that holds that number today.

This resolves each reference and prints what it actually points at, so a
human can read the list and catch a wrong one. It cannot know intent --
it makes the claim checkable rather than checking it.

Run: python3 scripts/wook-expansion-xref.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "content/wook-new-chapters"

OLD2NEW = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 7, 7: 8, 8: 9, 9: 11, 10: 12,
           11: 13, 12: 15, 13: 16, 14: 18, 15: 19, 16: 21, 17: 22, 18: 23,
           19: 24, 20: 25, 21: 27, 22: 28, 23: 29, 24: 30, 25: 32, 26: 33}
NEW2OLD = {v: k for k, v in OLD2NEW.items()}

NEW_TITLES = {6: "The Group Chat", 10: "The Love Of It", 14: "The Two Festivals",
              17: "The Container", 20: "The Next Twelve Hours",
              26: "He Still Has Your Number", 31: "What To Tell Your Mom"}

OLD_TITLES = {
    1: "It’s Not Drama, It’s Warfare", 2: "How They Get Your Yes",
    3: "Your Brain On Day Three", 4: "Your Body Made A Friend",
    5: "Yes Is A Sober Word", 6: "The Weep Tent Hustle",
    7: "The Cult That Calls Itself Family", 8: "Vendor Row Bloodsport",
    9: "The Bad Trip Babysitter", 10: "The Tampon Bag", 11: "The Road",
    12: "The Batch", 13: "The Free One", 14: "The Undercover", 15: "The RV",
    16: "The Missing Friend", 17: "The Plug Wook", 18: "The Lantern Family",
    19: "The Festie Hollowing", 20: "The Re-Entry Window",
    21: "The Sober Set Captain", 22: "The Long Comedown",
    23: "Have You Been The Wook?", 24: "Protecting The Magic",
    25: "The Taper’s Reveal", 26: "The After-Party",
}


def describe(n):
    if n in NEW_TITLES:
        return f"NEW  — {NEW_TITLES[n]}"
    if n in NEW2OLD:
        return f"old {NEW2OLD[n]:>2} — {OLD_TITLES[NEW2OLD[n]]}"
    return "!!! OUT OF RANGE"


def main():
    bad = 0
    for f in sorted(SRC.glob("ch??.html")):
        html = f.read_text(encoding="utf-8")
        me = int(re.search(r'data-ch="(\d+)"', html).group(1))
        print(f"\n=== {f.name}  (new chapter {me}) ===")
        seen = {}
        for m in re.finditer(r"Chapters?\s+(\d+)", html):
            n = int(m.group(1))
            ctx = re.sub(r"<[^>]+>", "", html[max(0, m.start() - 70):m.start() + 90])
            seen.setdefault(n, ctx.strip())
        for n in sorted(seen):
            flag = "  " if (n in NEW_TITLES or n in NEW2OLD) else "!!"
            if flag == "!!":
                bad += 1
            print(f" {flag} Chapter {n:>2} -> {describe(n)}")
            print(f"       … {seen[n][:150]}")
    print(f"\n{bad} out-of-range reference(s).")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()

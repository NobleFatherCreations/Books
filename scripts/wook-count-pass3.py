#!/usr/bin/env python3
"""Third 2026-09-10 pass: the stale counts only the checker could find.

Passes one and two were driven by reading, so they caught what a reader
notices. scripts/wook-continuity-check.py reads the whole book mechanically
and turned up five more cumulative chapter-count claims plus a wrong
callback, all in Tracks, Bridges and the Confession -- sections the
cold-open audit never opened.

Same root cause as everything before it: the Encore grew from three
chapters to six, and every sentence that counted chapters was left
counting the old book.

Also strips a Vellum build instruction that was shipping to the live page,
which CLAUDE.md forbids outright.

Run: python3 scripts/wook-count-pass3.py   (idempotent)
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WOOK = ROOT / "library/wook/index.html"

# (label, old, new)
EDITS = [
    # ch21: twenty chapters precede the Encore's first chapter.
    ("ch21: entire book has been 17 -> 20 chapters",
     "the entire book has been seventeen chapters of interesting things",
     "the entire book has been twenty chapters of interesting things"),

    # ch22's bridge teases ch23, which twenty-two chapters precede.
    ("ch22 bridge: mirror checks 19 -> 22 chapters",
     "skipping the mirror checks for nineteen chapters",
     "skipping the mirror checks for twenty-two chapters"),

    # ch23 is the same claim from inside the chapter.
    ("ch23: mirror checks 19 -> 22 chapters",
     "doing the mirror checks for nineteen chapters",
     "doing the mirror checks for twenty-two chapters"),

    # ch23's abbreviated confession opens by counting the reader's time.
    ("ch23 confession: spent 20 -> 22 chapters together",
     "We have spent twenty chapters together.",
     "We have spent twenty-two chapters together."),
    ("ch23 confession: given me 20 -> 22 chapters",
     "You have given me twenty chapters of your time",
     "You have given me twenty-two chapters of your time"),
    ("ch23 confession: building toward it 20 -> 22 chapters",
     "building toward it for twenty chapters",
     "building toward it for twenty-two chapters"),

    # The abbreviated confession is delivered in ch23, not ch20.
    ("ch25: confession delivered first in Ch20 -> Ch23",
     "delivered first in Chapter 20, fully in this chapter",
     "delivered first in Chapter 23, fully in this chapter"),

    # A build instruction for a different publishing tool, on a live page.
    ("colophon: strip Vellum build instruction",
     "<p>[In Vellum, add your real sign-up link here as a Store Link or button. "
     "Do not embed Amazon links if you plan to distribute to Apple Books, Kobo, "
     "or other retailers.]</p>",
     ""),
]


def main():
    html = WOOK.read_text(errors="surrogateescape")
    before = len(html)
    applied, skipped, missing = [], [], []

    for label, old, new in EDITS:
        if old in html:
            assert html.count(old) == 1, f"{label}: {html.count(old)} matches, expected 1"
            html = html.replace(old, new, 1)
            applied.append(label)
        elif new and new in html:
            skipped.append(label)
        else:
            missing.append(label)

    if missing:
        print("COULD NOT APPLY (anchor not found):")
        for m in missing:
            print(f"  ! {m}")
        return 1

    WOOK.write_text(html, errors="surrogateescape")
    print(f"wook: {before:,} -> {len(html):,} bytes\n")
    print(f"applied {len(applied)}:")
    for a in applied:
        print(f"  + {a}")
    if skipped:
        print(f"\nskipped {len(skipped)} (already applied):")
        for s in skipped:
            print(f"  = {s}")

    print("\nStill needs the author's real values (not inventable):")
    for ph in ["[your newsletter URL]", "[Author Legal Name / Pen Name]"]:
        if ph in html:
            print(f"  ? {ph}")


if __name__ == "__main__":
    sys.exit(main())

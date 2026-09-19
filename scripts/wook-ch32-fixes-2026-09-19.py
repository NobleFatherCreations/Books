#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Chapter 32 factual repairs, from the 2026-09-19 reveal-chapter audit.

Chapter 32 is the book's confession -- its whole authority rests on being
accurate about the book's own machinery, so a wrong cross-reference in it
costs more than the same error anywhere else. Five classes of defect:

1. Stale vow counts. The seven-chapter expansion's renumber pass updated
   "Chapter N" references but not free-standing quantity claims, so three
   numbers still describe the 26-chapter edition. Verified against the
   live book: 31 Kandi Trades precede ch32, 28 precede ch29, and a reader
   finishing ch32's Kandi Trade has said the closing vow 32 times.

2. A wrong Track citation for the Trauma Tax. The heading said Chapter 4
   and the body said "Chapter 7, Track 1"; ch7 Track 1 is The Trauma Dump
   Trap. The Trauma Tax is Chapter 2, Track 9. The heading's chapter
   number is dropped rather than corrected, because the confession is
   about the cold opens across the whole book, not one chapter's.

3. Two Tracks cited by a description instead of their own name -- the
   book calls them The Halo In The Pashmina and The Ride-Or-Die
   Chokehold, and the naming chapter should use the book's names.

4. Confession Nine's heading carried a pre-expansion chapter range
   ("ACROSS SEVENTEEN TO TWENTY") and also duplicated Confession Seven's
   "Commitment Escalation" label. Renamed to The Escalating Vows, which
   is already what the chapter's own Fanny Pack recap calls move nine.

5. "You are in." closes the theory block in all 32 other chapters and is
   absent here, because ch32 repurposes that block to hold the sixteen
   confessions. Added as "You are out." at the exact beat the list
   completes -- the one deliberate inversion of a phrase the book has
   used 32 times, at the moment the reader steps outside the machinery.

Verified NOT defects, left alone: "Field Reports" (ch29's confession list
and Appendix Q use the same name), and Confession Nine's ch24/ch29
citations (both check out against those chapters' actual vows).

Idempotent: every edit asserts its occurrence count and a second run is
a no-op.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WOOK = ROOT / "library/wook/index.html"

EDITS = [
    # --- 1. stale vow counts ---
    ("You have made approximately twenty iterations of the",
     "You have made approximately thirty iterations of the"),
    ("you have made twenty-two prior vows that have built the posture",
     "you have made twenty-eight prior vows that have built the posture"),
    ("who have said “protect the fucking magic” twenty-five times.",
     "who have said “protect the fucking magic” thirty-two times."),

    # --- 2. the Trauma Tax citation ---
    ("CONFESSION FIVE — THE TRAUMA TAX I CHARGED YOU IN CHAPTER 4",
     "CONFESSION FIVE — THE TRAUMA TAX I CHARGED YOU IN THE COLD OPENS"),
    ("This is the Trauma Tax from Chapter 7, Track 1.",
     "This is the Trauma Tax from Chapter 2, Track 9."),

    # --- 3. Tracks cited by description instead of name ---
    ("This is the Halo Effect from Chapter 3, Track 3.",
     "This is the Halo In The Pashmina from Chapter 3, Track 3."),
    ("This is the Commitment Escalation from Chapter 2, Track 2, applied to a sequence",
     "This is the Ride-Or-Die Chokehold from Chapter 2, Track 2, applied to a sequence"),

    # --- 4. Confession Nine's heading ---
    ("CONFESSION NINE — THE COMMITMENT ESCALATION ACROSS SEVENTEEN TO TWENTY",
     "CONFESSION NINE — THE ESCALATING VOWS"),

    # --- 5. the one-time inversion of the book's theory-block close ---
    ("The best I can offer is the list. The list is complete to the best of my knowledge. The knowing has limits.",
     "The best I can offer is the list. The list is complete to the best of my knowledge. The knowing has limits.</p><p>You are out."),
]


def main():
    raw = WOOK.read_text(errors="surrogateescape")
    applied = skipped = 0
    for old, new in EDITS:
        n = raw.count(old)
        if n == 0 and new in raw:
            print(f"  already applied: {old[:62]}...")
            skipped += 1
            continue
        if n != 1:
            raise SystemExit(f"expected exactly 1 of {old[:70]!r}, found {n}")
        raw = raw.replace(old, new)
        print(f"  fixed: {old[:66]}...")
        applied += 1
    WOOK.write_text(raw, errors="surrogateescape")
    print(f"\n{applied} fix(es) applied, {skipped} already done")
    return 0


if __name__ == "__main__":
    sys.exit(main())

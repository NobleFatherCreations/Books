#!/usr/bin/env python3
"""Sixth 2026-09-10 pass: the recurring cast, and three stale cross-references.

The tone/humor audit (content/wook-audits/wook-tone-humor-and-voice-audit.md)
turned up nine more defects, seven of them inside the Soundboard Quote -- the
book's strongest component and the one a reader is most likely to trust.

Same root cause as the five passes before it. Three chapters were inserted late
(The Road at 11, The Free One at 13, The Re-Entry Window at 20) and nothing that
counted a position was updated. Here that shows up as a cast who age backwards
and cross-references that point at the wrong chapters.

THE CAST ERRORS.

  Beans is twenty-one in Chapter 11 and nineteen in Chapter 14, so he gets
  younger as the book moves forward. Nineteen is canonical: Chapter 14 says it
  twice, Chapter 23 says "still nineteen-year-old Beans in spirit, now
  twenty-three in practice," and Chapter 25's roster confirms twenty-three at
  final appearance. Chapter 11 is an inserted chapter and is the outlier.

  Mara's appearance counter is wrong at both ends. She speaks in Chapters 4, 13,
  18 and 22. Chapter 13 calls itself her third (it is her second) and Chapter 22
  calls itself "third and final" (it is her fourth). The Free One being slotted
  in at 13 is exactly what put an extra appearance in front of her.

  Sister Lou and Yo-Yo are both introduced by full name AFTER a chapter has
  already used the short form. A reader meets "Sister Lou Mantilla" in 16, again
  in 20, and only then is told in 21 that she is Lourdes. Same shape for Yolanda
  in 6 after Yo-Yo in 5. Introductions move to the first appearance.

  Spool's Chapter 19 attribution contradicts itself inside one paragraph: "Ten
  years on the lot" and "has been doing this since she was twenty-six," which at
  forty-one is fifteen. Chapter 8 also says ten years on the lot, so the lot
  figure is the consistent one and the vaguer clause is what moves: she has been
  IN THE SCENE since twenty-six and vending on the lot for ten of those years.
  Both numbers become true and no character history changes.

  Bear's Chapter 12 attribution gives his age twice in two sentences.

THE CROSS-REFERENCE ERRORS.

  Chapter 9's briefing claims it "Prevents Chapters 9, 10, 12, 13, 14, and 15"
  and omits Chapter 16, The Missing Friend -- the one chapter the fifteen-minute
  briefing exists to prevent, whose own Track is literally called THE BRIEFING
  YOU SKIPPED. Read against the old numbering the list decodes cleanly: it was
  written after The Road was inserted but before The Free One was, when that set
  meant Bad Trip, Tampon Bag, Batch, Undercover, RV, Missing Friend. Shifting the
  tail by one restores exactly that set.

  The front-matter content disclosure names Chapters 9-15 as the ones carrying
  substance, legal and safety material with appendices. The appendices actually
  live in 9, 10, 12, 14, 15, 16, 17 and 18. A content warning that is too narrow
  is the one kind that hurts a reader, so it widens to the true span.

  NOT FIXED HERE, deliberately: Chapter 21 says the briefing drill has appeared
  "in abbreviated forms in Chapters 9, 12, 13, and 14." Checking the actual
  briefing elements (government names, ICE contacts, meet-up spot, code word,
  check-in interval, sober anchor) they cluster in Chapters 9 and 16, with only
  fragments in 12, 13 and 15. The renumbering shift would produce 9, 12, 14, 15,
  which I can see is still wrong. That one needs an authorial call on what counts
  as an abbreviated form, so it stays flagged rather than guessed at.

Run: python3 scripts/wook-cast-pass.py   (idempotent)
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WOOK = ROOT / "library/wook/index.html"

# (label, old, new)
EDITS = [
    ("ch11: Beans twenty-one -> nineteen, so he stops aging backwards",
     "Beans. Twenty-one.",
     "Beans. Nineteen."),

    ("ch13: Mara's third appearance -> second",
     "Forty-seven. Third appearance in the book.",
     "Forty-seven. Second appearance in the book."),

    ("ch22: Mara's third and final -> fourth and final",
     "forty-seven. Third and final appearance.",
     "forty-seven. Fourth and final appearance."),

    ("ch16: Sister Lou introduced by full name at first appearance",
     "Sister Lou Mantilla, fifty-eight, founding member",
     "Lourdes “Sister Lou” Mantilla, fifty-eight, founding member"),

    ("ch21: Sister Lou drops to short form, having been introduced in ch16",
     "Lourdes “Sister Lou” Mantilla, fifty-eight, twenty-three years in recovery",
     "Sister Lou Mantilla, fifty-eight, twenty-three years in recovery"),

    ("ch5: Yo-Yo introduced by full name at first appearance",
     "Yo-Yo Brennan, forty-three, harm-reduction coordinator",
     "Yolanda “Yo-Yo” Brennan, forty-three, harm-reduction coordinator"),

    ("ch6: Yo-Yo drops to short form, having been introduced in ch5",
     "Yolanda “Yo-Yo” Brennan, forty-three, twelve years",
     "Yo-Yo Brennan, forty-three, twelve years"),

    ("ch19: Spool's ten years on the lot and fifteen in the scene both hold",
     "Has been doing this since she was twenty-six",
     "Has been in the scene since she was twenty-six"),

    ("ch12: Bear's age given once, not twice",
     "Forty-four years old, thirty-two years in the scene",
     "Thirty-two years in the scene"),

    ("ch9: briefing prevents Ch16, The Missing Friend, which it had omitted",
     "Prevents Chapters 9, 10, 12, 13, 14, and 15.",
     "Prevents Chapters 9, 10, 12, 14, 15, and 16."),

    ("front matter: content disclosure widened to the true appendix span",
     "Chapters 9, 10, 11, 12, 13, 14, 15:",
     "Chapters 9 through 18:"),
]

FLAGGED = [
    "ch21: “abbreviated forms in Chapters 9, 12, 13, and 14” -- the drill's "
    "elements actually cluster in 9 and 16. Needs an authorial call on what "
    "counts as an abbreviated form.",
    "ch5/ch6: Yo-Yo is the Soundboard voice two chapters running, the only time "
    "this happens. Reassigning one is a writing decision, not a fix.",
]


def main():
    html = WOOK.read_text(errors="surrogateescape")
    before = len(html)
    applied, skipped, missing = [], [], []

    for label, old, new in EDITS:
        if old in html:
            n = html.count(old)
            assert n == 1, "%s: %d matches, expected 1" % (label, n)
            html = html.replace(old, new, 1)
            applied.append(label)
        elif new in html:
            skipped.append(label)
        else:
            missing.append(label)

    if missing:
        print("COULD NOT APPLY (anchor not found):")
        for m in missing:
            print("  ! " + m)
        return 1

    WOOK.write_text(html, errors="surrogateescape")
    print("wook: %s -> %s bytes\n" % (format(before, ","), format(len(html), ",")))
    print("applied %d:" % len(applied))
    for a in applied:
        print("  + " + a)
    if skipped:
        print("\nskipped %d (already applied):" % len(skipped))
        for s in skipped:
            print("  = " + s)
    print("\nflagged, not applied (needs your call):")
    for f in FLAGGED:
        print("  ? " + f)
    print("\nStill needs the author's real values (not inventable):")
    for ph in ["[your newsletter URL]", "[Author Legal Name / Pen Name]"]:
        if ph in html:
            print("  ? " + ph)
    return 0


if __name__ == "__main__":
    sys.exit(main())

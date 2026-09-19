#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Confess the four devices Chapter 32's sixteen confessions never named.

The 2026-09-19 reveal audit measured the confession list against every
reader-facing device in the book and found it covers roughly 60% of the
apparatus -- missing, among others, the two devices doing the most
persuasion work in the whole book.

These are folded into the existing confessions rather than added as new
numbered ones. Changing the count would touch ~24 places across ch29,
ch31, ch32 and the back matter, including two numbered lists that must
stay in sync, an appendix title, and the chapter poster -- and the book's
own patch notes record this exact count breaking twice already (v8 found
it drifted to "seventeen", v9 found the appendix listing fifteen). A
third renumber of the one number this book has never managed to keep
straight is not worth the prominence.

Each device goes where it actually belongs:

  Soundboard Quote Oracles -> Confession Four, already about borrowed
      authority. The Oracles are the same move with invented names
      instead of real ones, which is the sharper version of it.
  The Wook Discog          -> Confession Six, already about normalising
      the scene's patterns by anchoring them to something larger.
  The Bridge               -> Confession Seven, already about sequencing
      producing cumulative recognition; the Bridge is what carries the
      reader across the sequence.
  The Vibe Check           -> Confession Sixteen, because pre-conceding
      the obvious objection to buy credibility is the same mechanism the
      meta-confession runs, only it ran 164 times first.

Idempotent: each insert asserts its anchor appears exactly once and is
skipped if its text is already present.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WOOK = ROOT / "library/wook/index.html"

ORACLES = (
    "</p><p>And there is a worse version of this, one component up the page, "
    "in every single chapter.</p>"
    "<p>The Soundboard Quote is attributed to a named person with an age, a tenure, "
    "a job, and one detail built to make them a person instead of a citation — the "
    "wall chart of phrases heard verbatim across unrelated cases, the three photos of "
    "dogs, none of them police dogs, the road name from a sticker on a laptop that "
    "predates the career. Thirty-three of them. I made them up.</p>"
    "<p>Not the patterns they describe. Those are real and I have watched them happen. "
    "The people. The tenures. The counts. The seventeen documented cases across nine "
    "years, the four hundred laminated cards, the eleven years of iteration.</p>"
    "<p>The invented expert is doing more work than Cialdini is. Cialdini lends a "
    "chapter a discipline. The Oracle lends it a witness — somebody who was there, "
    "who counted, who is telling you this at a kitchen table at eleven at night with "
    "the moderating queue still open. A witness is harder to argue with than a finding. "
    "That is exactly why I built thirty-three of them and gave every one a road name."
)

DISCOG = (
    "</p><p>The Wook Discog ran the same play in the other direction. Every one of them "
    "ends at the Greatest Hits Compilation — the institutional, scaled-up version of "
    "whatever the chapter just showed you. The guy at the gas station, then the operation "
    "that runs the same architecture as policy. That escalation tells you the thing you "
    "just read is not a scene problem but a scale problem, and that the scene is only "
    "where you happened to notice it.</p>"
    "<p>I believe that claim. It is also a claim that makes the book feel larger than its "
    "subject, which makes it feel more necessary than a book about festivals, which is a "
    "thing I wanted."
)

BRIDGE = (
    " The sequence also had a handrail.</p>"
    "<p>Every chapter ends on a Bridge: one sentence naming what is next, almost always "
    "with somebody already moving inside it. Raya pulled over. Thea’s canopy is up and "
    "her phone is in someone else’s truck. Petey’s heart rate is coming down and the "
    "medic is writing something on a clipboard. A Bridge is not a summary. It is a "
    "cliffhanger with a service-industry smile, and its whole job is to make stopping feel "
    "like walking out in the middle of something.</p>"
    "<p>Thirty-two of them. You were not handed a single clean place to put the book down."
)

VIBE = (
    "There is one more in this family, and it was running long before this chapter was.</p>"
    "<p>Every Track carries a Vibe Check — the card that says not every version of this "
    "is a Wook, and here is how to tell the difference. A hundred and sixty-four of them. "
    "Every one is honest. Every one is also the most efficient persuasion device in the "
    "book, because a book that concedes your objection before you can raise it is a book "
    "you stop arguing with.</p>"
    "<p>The Vibe Check inoculated the Tracks against the response that would have cost me "
    "the most — that this is paranoid, that it makes a suspect out of everybody who is "
    "ever warm to you. I answered that a hundred and sixty-four times before you could say "
    "it, and each time I answered it I bought a little more of your trust for the paragraph "
    "immediately after.</p>"
    "<p>Which is this chapter’s entire move, run early and run often.</p>"
    "<p>"
)

EDITS = [
    # Confession Four -- the invented Oracles
    ("A seminar does not fit in a chapter.</p>",
     "A seminar does not fit in a chapter." + ORACLES + "</p>",
     "The Soundboard Quote is attributed to a named person"),
    # Confession Six -- the Discog
    ("Acceptance increased the book’s persuasiveness.</p>",
     "Acceptance increased the book’s persuasiveness." + DISCOG + "</p>",
     "The Wook Discog ran the same play in the other direction"),
    # Confession Seven -- the Bridge
    ("The sequencing was designed to produce this accumulation. It was not organic.</p>",
     "The sequencing was designed to produce this accumulation. It was not organic."
     + BRIDGE + "</p>",
     "It is a cliffhanger with a service-industry smile"),
    # Confession Sixteen -- the Vibe Check
    ("<p>I genuinely do not know if there is an outside of this.",
     "<p>" + VIBE + "I genuinely do not know if there is an outside of this.",
     "the most efficient persuasion device in the book"),
]


def main():
    raw = WOOK.read_text(errors="surrogateescape")
    applied = skipped = 0
    for anchor, replacement, marker in EDITS:
        if marker in raw:
            print(f"  already present: {marker[:54]}...")
            skipped += 1
            continue
        n = raw.count(anchor)
        if n != 1:
            raise SystemExit(f"anchor appears {n}x, expected 1: {anchor[:70]!r}")
        raw = raw.replace(anchor, replacement)
        words = len(replacement.split()) - len(anchor.split())
        print(f"  added ~{words} words at: {anchor[:58]}...")
        applied += 1
    WOOK.write_text(raw, errors="surrogateescape")
    print(f"\n{applied} device confession(s) added, {skipped} already present")
    return 0


if __name__ == "__main__":
    sys.exit(main())

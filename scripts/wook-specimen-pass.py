#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Eighth 2026-09-10 pass: install a Field Specimen in the 19 chapters that
lack one, plus renumber all 26 in chapter order.

From content/wook-audits/wook-book-wide-additions.md, Part A. Five chapters
already carried the device (1, 2, 7, 13, 14); two more carry a variant of it
(23's Field Mirror, 26's Last Cameo). This installs the remaining 19 as
text-only variants of the same '.specimen' component -- the existing five
each pair a custom cartoon SVG with the caption card, but nineteen bespoke
illustrations are an art pass this round doesn't include, so the new ones
ship as the caption card alone ('.spec-info' with no '.spec-art'), which the
existing flexbox layout already supports cleanly.

Insertion point: right before each chapter's '<div class="wristband"
role="presentation"><span class="wb-clasp">THE TRACKS</span></div>', the same
position the five existing specimens already occupy (after the chapter's
thesis/roster section, before its Tracks). Chapters 21 and 25 have no Tracks
and therefore no wristband anchor; both insert right after their comp-thesis
section closes instead.

Run: python3 scripts/wook-specimen-pass.py   (idempotent)
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WOOK = ROOT / "library/wook/index.html"

# chapter -> (NAME, [caption fragments], kicker)
SPECIMENS = {
 3:  ("THE NOW GOBLIN",
      "Habitat: hour fifty-two. Diet: whatever is closest. Time horizon: eleven minutes. Has never once considered Tuesday.",
      "It is not lying to you. It genuinely cannot see that far."),
 4:  ("THE SAFE HANDS",
      "Habitat: wherever someone is falling apart. Response time: suspicious. Hug duration: calibrated. Exit strategy: yours, not theirs.",
      "The comfort is real. So is the invoice."),
 5:  ("THE FORTY-FIVE SECOND MAN",
      "Habitat: the best sightline in the room. Method: math, not chemistry. Selection criteria: alone, open-faced, not performing for the camera.",
      "He counted you before you finished your first drink."),
 6:  ("THE WEEP TENT OPERATOR",
      "Coat: linen, intentional. Tears: real. Timing: also real. Has a lantern and a very specific idea of where you're camped.",
      "The crying is not the ask. The crying is the invoice's cover letter."),
 8:  ("THE FOUNDER (VENDOR ROW)",
      "Business card: letterpress. Payment terms: vibes. Will describe your labor as a contribution and his couch as Topanga.",
      "Exposure has never once paid for a booth fee."),
 9:  ("THE FORTY-FIVE MINUTE FRIEND",
      "Habitat: wherever you're having a rough one. Warmth: genuine. Timeline: forty-five minutes to the bag. Vibe: chemistry, not charity.",
      "The kindness was real. So was the countdown."),
 10: ("THE ESTABLISHED FACT",
      "Habitat: the passenger seat, mid-nod. Delivery: casual, pre-decided, no question mark. Specialty: making a request sound like it already happened.",
      "It was never really a question. That was the point."),
 11: ("THE FRIENDLIEST SEVEN MINUTES",
      "Habitat: the shoulder of the interstate. Register: warm, practiced, rehearsed a thousand times. Badge: real. Warmth: also real. Purpose: not what it looks like.",
      "They train the tone. You don't have to buy it."),
 12: ("MY GUY",
      "Habitat: exists only in sentences, never in person. Track record: two years, allegedly. Test kit: theoretical. Confidence: total.",
      "My guy has never once met the person who died."),
 15: ("THE ROW 14 SITUATION",
      "Curtains: drawn. Generator: running. Distance from the nearest witness: forty feet and one corner.",
      "The geometry was decided before you were invited."),
 16: ("THE FIFTEEN MINUTES YOU SKIPPED",
      "Habitat: the tailgate, before doors. Cost: fifteen minutes. Cost of skipping it: four hours, 1:47 a.m., and a dead phone.",
      "Everyone meant to do it. That's the whole tragedy."),
 17: ("THE PLUG WHO LOVES YOU",
      "First one: free. Second one: free. Third one: a conversation about loyalty.",
      "You are not a customer. You are a subscription."),
 18: ("EL (NOT THEIR REAL NAME)",
      "Bus: converted. Hierarchy: converted. Sister count: growing. Exit interviews: none on file.",
      "Family is a word here. It is also a fee schedule."),
 19: ("THE CONTACT LIST",
      "Habitat: your phone, three hundred names deep. Function: none outside a four-mile radius and a specific weekend. Sister who stopped asking: not in it.",
      "Every name here only knows one version of you."),
 20: ("THE SUNDAY AFTERNOON TEXT",
      "Habitat: your notifications, 4:47 p.m., still in the car. Urgency: manufactured. Half-life: gone by Tuesday.",
      "Nothing that dies by Tuesday was ever really an emergency."),
 21: ("THE BRIEFING CAPTAIN",
      "Uniform: none. Authority: eleven years, zero incidents. Tolerance for “we'll find each other”: none. Clipboard: mental, but total.",
      "You'll roll your eyes for four minutes. You'll thank her at 1 a.m."),
 22: ("THE INSTALLED VOICE",
      "Habitat: your own head, 3 a.m. Wears: your voice's clothes. Belongs to: someone who left two years ago. Accuracy: zero. Volume: maximum.",
      "Not tonight. You don't have to win the argument. You have to survive it."),
 24: ("THE MISSING STAIR",
      "Location: known to everyone, fixed by no one. Workaround: informal, exhausting, permanent. Sign posted: never.",
      "Routing around him is not the same as removing him."),
 25: ("THE TAPER",
      "Equipment: two mic stands, a field recorder, opinions about capsule mics. Position: behind you the whole book. Motive: the most honest one here.",
      "He's been recording this the entire time. So has the book."),
}

TRACKS_ANCHOR = '<div class="wristband" role="presentation"><span class="wb-clasp">\U0001f3ab THE TRACKS</span></div>'


def card_html(number, name, caption, kicker):
    return (
        '<section class="panel pp-cream specimen"><div class="spec-info">'
        '<p class="spec-no">FIELD SPECIMEN №%02d</p>'
        '<p class="spec-name">%s</p>'
        '<p class="spec-cap">%s</p>'
        '<p class="spec-joke">→ %s</p>'
        '</div></section>'
    ) % (number, name, caption, kicker)


def bounds(html, n):
    s = re.search(r'<div class="chwrap s\d" data-ch="%d">' % n, html)
    e = re.search(r'<i class="ch-end" data-ch="%d">' % n, html)
    return s.start(), e.start()


def main():
    html = WOOK.read_text(errors="surrogateescape")
    before = len(html)

    if "FIELD SPECIMEN №24" in html:
        print("already applied (renumbered through №24 present) -- nothing to do")
        return 0

    # ---- Step 1: strip the five existing specimens' numbering so we can
    # renumber everything 01-24 in one consistent pass below. Their content
    # (including custom spec-art) is preserved; only the "FIELD SPECIMEN NNN"
    # label text is rewritten.
    OLD_TO_CHAPTER = {1: "THE LOT RAT", 2: "THE WOOK IN SHEEP’S CLOTHING",
                       7: "KING DAVE (SELF-CROWNED)", 13: "THE GENEROUS ONE",
                       14: "DEFINITELY NOT A COP"}
    for n in sorted(OLD_TO_CHAPTER):
        pass  # renumbered in the sweep below by chapter order, not by name

    # ---- Step 2: insert the 19 new specimens ----
    inserted = 0
    for n in sorted(SPECIMENS, reverse=True):
        name, caption, kicker = SPECIMENS[n]
        s, e = bounds(html, n)
        chunk = html[s:e]
        card = card_html(0, name, caption, kicker)  # number fixed in step 3
        if n in (21, 25):
            m = re.search(r'<section class="panel pp-purple prose comp-thesis">.*?</section>', chunk, re.S)
            assert m, "ch%d: comp-thesis not found" % n
            pos = m.end()
        else:
            pos = chunk.find(TRACKS_ANCHOR)
            assert pos != -1, "ch%d: tracks anchor not found" % n
        chunk = chunk[:pos] + card + chunk[pos:]
        html = html[:s] + chunk + html[e:]
        inserted += 1

    # ---- Step 3: renumber every FIELD SPECIMEN 01-24 in chapter order ----
    numbered = 0
    for i, m in enumerate(re.finditer(r'<p class="spec-no">FIELD SPECIMEN №\d+</p>', html), start=1):
        pass
    # do the actual rewrite via re.sub with a counter (spec-no blocks appear
    # in document order, which is chapter order for this book)
    counter = [0]

    def renum(m):
        counter[0] += 1
        return '<p class="spec-no">FIELD SPECIMEN №%02d</p>' % counter[0]

    html, numbered = re.subn(r'<p class="spec-no">FIELD SPECIMEN №\d+</p>', renum, html)

    WOOK.write_text(html, errors="surrogateescape")
    print("wook: %s -> %s bytes" % (format(before, ","), format(len(html), ",")))
    print("inserted %d new specimens, renumbered %d total (№01-№%02d)" % (inserted, numbered, counter[0]))
    return 0


if __name__ == "__main__":
    sys.exit(main())

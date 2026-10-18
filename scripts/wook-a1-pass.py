#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pass A1 of the full review: what the extended proofreader found.

See content/wook-audits/wook-full-review-plan.md. This pass added four
checks to scripts/wook-proofread.py -- duplicates, typography, sequence,
headings -- and this applies what they turned up.

The typography checks came back clean apart from three deliberate,
in-character cases now allowlisted with reasons: a lowercase "pm" inside a
text message, a folder a character named "competitors - general", and an
ellipsis that opens a line because the speaker is trailing into it.

Idempotent.

Run: python3 scripts/wook-a1-pass.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WOOK = ROOT / "library/wook/index.html"

log = []


def note(step, n, what):
    log.append((step, n, what))


# The "Tales From ... The Save" header names the place the Save happens in.
# Four names were doing double duty. In each pair the chapter that keeps the
# name is the one whose Save is actually set there; the renamed one gets the
# thing its own scene turns on, checked against that Save's text.
SAVE_RENAMES = {
    # ch11's Save has no rest stop in it at all -- it turns on a logistics
    # call to the group chat three weeks out. ch20's literally stops at one.
    "The Road": ("Tales From The Rest Stop — The Save",
                 "Tales From The Logistics Call — The Save"),
    # Two Saves both called "The Festival", which names nothing. ch12 is
    # Devi working her camp network for a vouched source; ch13 is Yara at
    # the edge of a fire circle when the mason jar comes around.
    "The Batch": ("Tales From The Festival — The Save",
                  "Tales From The Camp Network — The Save"),
    "The Free One": ("Tales From The Festival — The Save",
                     "Tales From The Fire Circle — The Save"),
    # ch16's Save is at the gate; ch21's is the briefing working, with the
    # Inner Anchor four minutes away because the role said four minutes.
    "The Sober Set Captain": ("Tales From The Gate — The Save",
                              "Tales From The Anchor Crew — The Save"),
    # ch19's Save is Anjali on her couch on a Tuesday; ch22's is Simone's
    # fourth week, which is the one the apartment belongs to.
    "The Festie Hollowing": ("Tales From The Apartment — The Save",
                             "Tales From The Tuesday Couch — The Save"),
}

CHAPTER_OF = {"The Road": 11, "The Batch": 12, "The Free One": 13,
              "The Sober Set Captain": 21, "The Festie Hollowing": 19}


def chapter_span(src, n):
    start = re.search(r'<div class="chwrap s\d" data-ch="%d">' % n, src)
    end = re.search(r'<i class="ch-end" data-ch="%d">' % n, src)
    if not start or not end:
        sys.exit("chapter %d not found" % n)
    return start.start(), end.start()


def fix_save_titles(src):
    n = 0
    for label, (old, new) in SAVE_RENAMES.items():
        ch = CHAPTER_OF[label]
        a, b = chapter_span(src, ch)
        body = src[a:b]
        if new in body:
            continue
        if old not in body:
            sys.exit("ch%d: expected Save title %r not found" % (ch, old))
        src = src[:a] + body.replace(old, new, 1) + src[b:]
        n += 1
    note("save-titles", n, "Save headers that shared a name with another chapter")
    return src


# Appendix A indexes every Track by chapter, and three chapters have none.
# It jumped 20 -> 22 and stopped at 24, so a reader counting chapters finds
# three of them simply absent with nothing saying why.
TRACKLESS = {
    21: ("<h4 class=\"h4\">Chapter 21</h4><p>No Tracks. Five protocols instead "
         "&mdash; The 3-Tier Anchor System, The Pre-Show Crew Briefing, The "
         "Code-Word Protocol, The Anchor&rsquo;s Bill of Rights, The Anchor "
         "Backup Plan.</p>"),
    25: ("<h4 class=\"h4\">Chapter 25</h4><p>No Tracks. Sixteen confessions "
         "instead &mdash; the book&rsquo;s own persuasion moves, listed in "
         "full in Appendix Q.</p>"),
    26: ("<h4 class=\"h4\">Chapter 26</h4><p>No Tracks. Five pillars instead "
         "&mdash; The Known Perimeter, The Vetted Community, The Identity "
         "Floor, The Accountability Practice, The Passed-Forward "
         "Information.</p>"),
}


def fix_track_index(src):
    start = src.find('id="apA"')
    end = src.find('</section>', start)
    if start == -1 or end == -1:
        sys.exit("appendix A not found")
    block = src[start:end]
    n = 0

    # Chapter 21 opens the Encore, so it belongs after that movement header.
    marker = '<h4 class="h4">ENCORE — PROTECT THE MAGIC</h4>'
    if 'Chapter 21</h4>' not in block:
        if marker not in block:
            sys.exit("appendix A: Encore header not found")
        block = block.replace(marker, marker + TRACKLESS[21], 1)
        n += 1

    # 25 and 26 close the book, so they close the index.
    for ch in (25, 26):
        if 'Chapter %d</h4>' % ch not in block:
            block = block + TRACKLESS[ch]
            n += 1

    intro = ("<p>Every named Track in the book, with clinical anchor, chapter, "
             "and primary counter-drop. Screenshot-ready. Organized by chapter.</p>")
    if intro in block:
        block = block.replace(
            intro,
            intro.replace("Organized by chapter.</p>",
                          "Organized by chapter. Three chapters carry no Tracks "
                          "&mdash; 21, 25 and 26 &mdash; and say so in place.</p>"), 1)

    note("track-index", n, "trackless chapters named in the Master Track Index")
    return src[:start] + block + src[end:]


def fix_heading_levels(src):
    """h2 -> h4 skipped a rung. The CSS styles .h4, never the h4 element,
    so promoting the three movement headers is invisible and fixes the
    document outline."""
    start = src.find('id="apA"')
    end = src.find('</section>', start)
    block = src[start:end]
    n = 0
    for movement in ("SET ONE — KNOW THE PATTERN", "SET TWO — READ THE ROOM",
                     "ENCORE — PROTECT THE MAGIC"):
        old = '<h4 class="h4">%s</h4>' % movement
        new = '<h3 class="h4">%s</h3>' % movement
        if old in block:
            block = block.replace(old, new, 1)
            n += 1
    note("heading-levels", n, "movement headers promoted so the outline stops skipping h3")
    return src[:start] + block + src[end:]


STEPS = [fix_save_titles, fix_track_index, fix_heading_levels]


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

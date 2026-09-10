#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Twelfth 2026-09-10 pass: hand-built icon art for the 19 text-only specimens.

The book's five original Field Specimens (and the existing King Dave, Definitely
Not A Cop, etc.) are full hand-coded SVG character illustrations -- dozens of
paths per figure, built the same way as the book's other decorative symbols
(#flower, #smile, #star). An AI image generator would produce a raster asset
in a different visual language (photographic/painterly) and require a paid
credit-approval step for 19 images; embedding raster would also be the first
non-vector asset in a book that's been entirely hand-built SVG until now.

So this builds a second, simpler visual language instead: a circular "field
tag" badge -- one flat-color icon per specimen, in the book's own palette,
with the same stroke weight and a small SPECIMEN pennant, matching the
existing badges' spirit (a collector's-guide ID tag) without trying to
imitate character-illustration work that was hand-drawn by an artist and
can't be reliably reproduced blind. Rendered and visually reviewed (all 19
together, at true card size) before being wired in.

Run: python3 scripts/wook-specimen-art-pass.py   (idempotent)
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WOOK = ROOT / "library/wook/index.html"
DEFS = Path("/tmp/icon_defs.txt").read_text()

# chapter -> (symbol id, aria-label)
SYMBOL_FOR_CHAPTER = {
    3:  ("spec-nowgoblin", "The Now Goblin"),
    4:  ("spec-safehands", "The Safe Hands"),
    5:  ("spec-45sec", "The Forty-Five Second Man"),
    6:  ("spec-weeptent", "The Weep Tent Operator"),
    8:  ("spec-founder", "The Founder"),
    9:  ("spec-45min", "The Forty-Five Minute Friend"),
    10: ("spec-establishedfact", "The Established Fact"),
    11: ("spec-7min", "The Friendliest Seven Minutes"),
    12: ("spec-myguy", "My Guy"),
    15: ("spec-row14", "The Row 14 Situation"),
    16: ("spec-15min", "The Fifteen Minutes You Skipped"),
    17: ("spec-plug", "The Plug Who Loves You"),
    18: ("spec-el", "El (Not Their Real Name)"),
    19: ("spec-contactlist", "The Contact List"),
    20: ("spec-sundaytext", "The Sunday Afternoon Text"),
    21: ("spec-briefingcaptain", "The Briefing Captain"),
    22: ("spec-installedvoice", "The Installed Voice"),
    24: ("spec-missingstair", "The Missing Stair"),
    25: ("spec-taper", "The Taper"),
}


def bounds(html, n):
    s = re.search(r'<div class="chwrap s\d" data-ch="%d">' % n, html)
    e = re.search(r'<i class="ch-end" data-ch="%d">' % n, html)
    return s.start(), e.start()


def main():
    html = WOOK.read_text(errors="surrogateescape")
    before = len(html)

    if "spec-nowgoblin" in html:
        print("already applied -- nothing to do")
        return 0

    # ---- 1. insert the 19 new <symbol> defs alongside the book's other ones ----
    defs_anchor = '<symbol id="star" viewBox="0 0 64 64">'
    assert html.count(defs_anchor) == 1
    html = html.replace(defs_anchor, DEFS + defs_anchor, 1)

    # ---- 2. give each of the 19 text-only specimens its spec-art column ----
    inserted = 0
    for n, (symbol_id, label) in sorted(SYMBOL_FOR_CHAPTER.items(), reverse=True):
        s, e = bounds(html, n)
        chunk = html[s:e]
        old = '<section class="panel pp-cream specimen"><div class="spec-info">'
        assert chunk.count(old) == 1, "ch%d: spec-info anchor not found/not unique" % n
        art = (
            '<section class="panel pp-cream specimen">'
            '<div class="spec-art"><svg viewBox="0 0 220 210" role="img" '
            'aria-label="%s — field-tag icon"><use href="#%s"/></svg></div>'
            '<div class="spec-info">'
        ) % (label, symbol_id)
        chunk = chunk.replace(old, art, 1)
        html = html[:s] + chunk + html[e:]
        inserted += 1

    WOOK.write_text(html, errors="surrogateescape")
    print("wook: %s -> %s bytes" % (format(before, ","), format(len(html), ",")))
    print("added symbol defs for %d icons, wired spec-art into %d specimens" % (len(SYMBOL_FOR_CHAPTER), inserted))
    return 0


if __name__ == "__main__":
    sys.exit(main())

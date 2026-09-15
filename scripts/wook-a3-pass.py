#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pass A3 of the full review: the vernacular sweep's structural half.

See content/wook-audits/wook-full-review-plan.md. A3's main output is
content/wook-audits/wook-vernacular-word-bank.md -- the measured per-POV
vocabulary the B passes write against. This applies the one structural
finding that came out of building it.

Every cold open announces its point of view, and the announcement was
wearing three different costumes: a styled badge in 13 chapters, an
italic line in 8, a plain paragraph in 3. The 13 with the badge are
exactly the 13 whose POV is the ordinary one -- plain Festie. Every
chapter with an unusual POV, where a reader most needs telling that the
first person speaking is a predator, had the quietest version of the
label. This normalizes all 26 onto the badge.

Chapter 25 is left alone: it has no POV label at all, opening instead on
"The PLURth Angel. Tuesday morning." Giving it a badge would mean
inventing a label, which is an authorial call, so it is in the ledger's
decision queue instead.

Idempotent.

Run: python3 scripts/wook-a3-pass.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WOOK = ROOT / "library/wook/index.html"

# chapter -> (exact paragraph as it stands, badge text to replace it with)
POV_BADGES = {
    5:  ('<p><em><mark class="mk-y">Wook</mark> POV</em></p>', "📍 WOOK POV"),
    6:  ('<p><em>Witness POV</em></p>', "📍 WITNESS POV"),
    7:  ('<p><em>Witness POV</em></p>', "📍 WITNESS POV"),
    8:  ('<p><em><mark class="mk-y">Wook</mark> POV</em></p>', "📍 WOOK POV"),
    12: ('<p><em><mark class="mk-y">Wook</mark> POV</em></p>', "📍 WOOK POV"),
    13: ('<p><em><mark class="mk-y">Wook</mark> POV</em></p>', "📍 WOOK POV"),
    14: ('<p><em><mark class="mk-y">Wook</mark> POV</em></p>', "📍 WOOK POV"),
    17: ('<p><em><mark class="mk-y">Wook</mark> POV</em></p>', "📍 WOOK POV"),
    18: ('<p>Festie POV — Inside the coercive group</p>',
         "📍 FESTIE POV — INSIDE THE GROUP"),
    21: ('<p>Festie POV — No predator</p>', "📍 FESTIE POV — NO PREDATOR"),
    24: ('<p><em>Montage POV</em></p>', "📍 MONTAGE POV"),
    26: ('<p>Festie POV — Six months later</p>',
         "📍 FESTIE POV — SIX MONTHS LATER"),
}


def chapter_span(src, n):
    a = re.search(r'<div class="chwrap s\d" data-ch="%d">' % n, src)
    b = re.search(r'<i class="ch-end" data-ch="%d">' % n, src)
    if not a or not b:
        sys.exit("chapter %d not found" % n)
    return a.start(), b.start()


def main():
    src = WOOK.read_text(encoding="utf-8")
    before = len(src)
    done = 0
    for ch, (old, badge) in POV_BADGES.items():
        a, b = chapter_span(src, ch)
        body = src[a:b]
        new = '<p class="pov">%s</p>' % badge
        if new in body:
            continue
        # Only the first occurrence, and only inside the cold open, so an
        # identical italic line elsewhere in the chapter is never touched.
        drop = body.find('comp-drop')
        head = body.find('</div></div>', drop)
        if head == -1 or old not in body[head:head + 400]:
            sys.exit("ch%d: POV line not found in its expected form" % ch)
        body = body[:head] + body[head:head + 400].replace(old, new, 1) + body[head + 400:]
        src = src[:a] + body + src[b:]
        done += 1
    WOOK.write_text(src, encoding="utf-8")
    print(f"  pov-badges  {done:>3}  cold-open POV labels normalized onto the badge")
    print(f"\n{before:,} -> {len(src):,} bytes")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pass D2-content: resolve the sixteen-moves discrepancy, fix a duplicate
item 14 in Appendix Q left by an earlier pass, fill Appendix G's six
missing Discog entries, and a targeted humor pass.

See content/wook-audits/wook-full-review-plan.md.

Idempotent.

Run: python3 scripts/wook-d2-content-pass.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WOOK = ROOT / "library/wook/index.html"

log = []


def note(step, n, what):
    log.append((step, n, what))


def fix_apQ_duplicate(src):
    """Pass A1 inserted a plain-text item 14 into Appendix Q because its
    string check for the existing item failed -- the live item 14 has a
    <mark> tag splitting "Kandi" from the surrounding words, so a plain
    substring search for "14. The Kandi Trade Vows" never matched it and
    the pass concluded the item was missing. Removes the inserted
    duplicate, keeping the original marked-up item.
    """
    bad = "<p>14. The Kandi Trade Vows As Group Identification</p><p>14. The <mark"
    n = src.count(bad)
    if n == 0:
        note("apQ-duplicate", 0, "already fixed")
        return src
    if n > 1:
        sys.exit("apQ: duplicate item 14 pattern matched more than once")
    src = src.replace(
        bad,
        "<p>14. The <mark", 1)
    note("apQ-duplicate", 1, "duplicate item 14 removed, original kept")
    return src


def fix_sixteen_moves_canon(src):
    """Resolves the standing decision-queue item: chapters 23 and 25 each
    list "the sixteen moves" and disagree at positions 3-5. Chapter 25 is
    the one the book itself calls the full delivery ("delivered first in
    Chapter 23, fully in this chapter"), and its item 3 -- the tattoo-the-
    three-words command -- is a sharper, funnier, more specific piece of
    writing than chapter 23's "Scarcity Of Specific Protocols," which it
    replaces. Chapter 25 needs no edit. Chapter 23 and Appendix Q are
    brought into line with it: item 3 becomes the tattoo confession
    (rewritten in ch23's first-person "I" register, folding in a
    shortened version of the protocols-scarcity idea so nothing is lost
    outright), Halo shifts to 4, Trauma Tax to 5.
    """
    n = 0

    old_ch23 = (
        '3. The Halo Of The Named Thinkers. Every Tapers’ Section — '
        'Cialdini, Kahneman, Walker, Bowlby, Lifton — was a Halo. The '
        'naming of recognized intellectual authorities transferred '
        'credibility to everything that followed in the chapter, including '
        'the claims that were the PLURth Angel’s observations rather '
        'than the thinkers’ documented findings. The Tapers’ '
        'Section is real and useful. It is also a halo effect running on '
        'academic names.</p><p>4. The Trauma Tax I Charged You In Chapter '
        '4. The cold opens involving the worst outcomes — the Santa '
        'hat, the gray lips, the napkin — asked you to hold real '
        'emotional weight on behalf of people who may or may not have '
        'existed as described. You held it. Holding it created a felt '
        'investment in the chapter’s conclusions that made those '
        'conclusions harder to resist. The Tax was functional.</p>'
        '<p>5. The Scarcity Of Specific Protocols. The counter-drops, '
        'named and numbered, created urgency. “The three-minute '
        'gate.” “The Tuesday Quarantine.” “The Sister '
        'Lou Briefing.” Named protocols carry the scarcity heuristic: '
        'they sound like tools that are available in limited supply from '
        'a specific source, which is this book. The naming was designed '
        'to make the content feel exclusive. It is not exclusive. The '
        'principles are available from many sources. The names are mine.'
        '</p>'
    )

    new_ch23 = (
        '3. The Scarcity Of The Tattoo The Three Words Command. In the '
        'early chapters, there were commands. Not suggestions. Commands '
        'delivered in the second person with the urgency of scarcity: '
        'write this down, remember this, this is the thing, this is the '
        'move, tattoo the three words. Nobody has ever actually tattooed '
        'the three words. I checked. The command-plus-scarcity '
        'construction activates a compliance reflex — the same one '
        'Chapter 2’s Secret Set Sucker Punch relies on — by '
        'making the non-compliance feel like a loss. You were not going '
        'to lose the thing. The thing was in the book. The book was in '
        'your hands. You could find the thing again in thirty seconds, '
        'which is a sentence I also used on you about a mason jar. The '
        'named counter-drops did the same work at scale — “The '
        'Three-Minute Gate,” “The Tuesday Quarantine,” '
        '“The Sister Lou Briefing” — proprietary-sounding '
        'tools that are, in fact, available from many sources for free, '
        'wearing brand names I gave them so they would feel like yours '
        'to lose.</p><p>4. The Halo Of The Named Thinkers. Every '
        'Tapers’ Section — Cialdini, Kahneman, Walker, Bowlby, '
        'Lifton — was a Halo. The naming of recognized intellectual '
        'authorities transferred credibility to everything that followed '
        'in the chapter, including the claims that were the PLURth '
        'Angel’s observations rather than the thinkers’ '
        'documented findings. The Tapers’ Section is real and '
        'useful. It is also a halo effect running on academic names, '
        'which is a sentence Kahneman would probably enjoy and Cialdini '
        'would probably bill you for.</p><p>5. The Trauma Tax I Charged '
        'You In Chapter 4. The cold opens involving the worst outcomes '
        '— the Santa hat, the gray lips, the napkin — asked you '
        'to hold real emotional weight on behalf of people who may or '
        'may not have existed as described. You held it. Holding it '
        'created a felt investment in the chapter’s conclusions '
        'that made those conclusions harder to resist. The Tax was '
        'functional.</p>'
    )

    c = src.count(old_ch23)
    if c == 0 and new_ch23 in src:
        note("ch23-sixteen-moves", 0, "already harmonized")
    elif c == 1:
        src = src.replace(old_ch23, new_ch23, 1)
        n += 1
        note("ch23-sixteen-moves", 1,
             "items 3-5 harmonized with chapter 25's fuller version")
    else:
        sys.exit("ch23: confession items 3-5 block not found as expected "
                 "(found %d times)" % c)

    old_apQ = (
        '<p>3. The Halo Of The Named Thinkers</p>'
        '<p>4. The Trauma Tax Charged In The Cold Opens</p>'
        '<p>5. The Scarcity Of Specific Protocols</p>'
    )
    new_apQ = (
        '<p>3. The Scarcity Of The Tattoo The Three Words Command</p>'
        '<p>4. The Halo Of The Named Thinkers</p>'
        '<p>5. The Trauma Tax Charged In The Cold Opens</p>'
    )
    c2 = src.count(old_apQ)
    if c2 == 0 and new_apQ in src:
        note("apQ-sixteen-moves", 0, "already harmonized")
    elif c2 == 1:
        src = src.replace(old_apQ, new_apQ, 1)
        n += 1
        note("apQ-sixteen-moves", 1, "items 3-5 reordered to match")
    else:
        sys.exit("apQ: items 3-5 block not found as expected (found %d times)" % c2)

    return src


def fix_apG_missing(src):
    """Appendix G bills itself as "The Wook Discog Complete" but is missing
    the six chapters inserted late in the book's development (11, 13, 20,
    21) or added after the appendix was last touched (25, 26). Each new
    entry condenses that chapter's own Studio Debut / Live Album /
    Greatest Hits Compilation sections, matching the terse house style of
    every existing entry. Also corrects Ch23's Greatest Hits line, which
    reads "every Chapter 22 that didn't get written" -- Chapter 22 in this
    book is the ally-who-sides-with-the-Wook chapter and has nothing to do
    with unwritten disclosure chapters. Chapter 23's own Greatest Hits
    Compilation section is about the book itself being a field manual on
    manipulation that used manipulation to teach it; the Appendix G line
    is rewritten to match that, rather than the mismatched cross-reference
    it shipped with.
    """
    n = 0

    old_ch10_12 = (
        '<p><strong class="lead">Ch10:</strong> Debut: the twenty-three who '
        'asks the girlfriend to carry. Live: him in the Subaru. Greatest '
        'Hits: the criminal organization using festival romance for '
        'distribution logistics.</p><p><strong class="lead">Ch12:</strong>'
    )
    new_ch10_12 = (
        '<p><strong class="lead">Ch10:</strong> Debut: the twenty-three who '
        'asks the girlfriend to carry. Live: him in the Subaru. Greatest '
        'Hits: the criminal organization using festival romance for '
        'distribution logistics.</p><p><strong class="lead">Ch11:</strong> '
        'Debut: the twenty-two-year-old on his first festival drive, '
        'pulled over for a real violation and talked into consent by an '
        'officer who seemed warm. Live: the officer in the unmarked '
        'Explorer at mile marker 231, four years into working the '
        'corridor. Greatest Hits: the rideshare Facebook group that has '
        'never once mentioned what to say if you get stopped.</p>'
        '<p><strong class="lead">Ch12:</strong>'
    )
    c = src.count(old_ch10_12)
    if c == 0 and 'Ch11:</strong> Debut: the twenty-two-year-old on his first festival drive' in src:
        note("apG-ch11", 0, "already added")
    elif c == 1:
        src = src.replace(old_ch10_12, new_ch10_12, 1)
        n += 1
        note("apG-ch11", 1, "Ch11 Discog entry added")
    else:
        sys.exit("apG: Ch10/Ch12 boundary not found as expected (found %d times)" % c)

    old_ch12_14 = (
        '<p><strong class="lead">Ch12:</strong> Debut: the twenty-one with '
        'the gummies and no testing instinct. Live: the twenty-seven with '
        'the eighty caps. Greatest Hits: the pressing operation two levels '
        'above the source.</p><p><strong class="lead">Ch14:</strong>'
    )
    new_ch12_14 = (
        '<p><strong class="lead">Ch12:</strong> Debut: the twenty-one with '
        'the gummies and no testing instinct. Live: the twenty-seven with '
        'the eighty caps. Greatest Hits: the pressing operation two levels '
        'above the source.</p><p><strong class="lead">Ch13:</strong> '
        'Debut: the twenty-year-old with genuinely good vibes who put '
        'something in a drink at a college house party and mostly '
        'hasn’t thought about it since. Live: Cosmo, twenty-eight, '
        'Derek in Sacramento, eight years into the same jar. Greatest '
        'Hits: the workshop dome that administers the medicine before the '
        'consent conversation happens.</p><p><strong class="lead">Ch14:</strong>'
    )
    c2 = src.count(old_ch12_14)
    if c2 == 0 and 'Ch13:</strong> Debut: the twenty-year-old with genuinely good vibes' in src:
        note("apG-ch13", 0, "already added")
    elif c2 == 1:
        src = src.replace(old_ch12_14, new_ch12_14, 1)
        n += 1
        note("apG-ch13", 1, "Ch13 Discog entry added")
    else:
        sys.exit("apG: Ch12/Ch14 boundary not found as expected (found %d times)" % c2)

    old_ch19_22 = (
        '<p><strong class="lead">Ch19:</strong> Debut: the twenty-three at '
        'first festival, contrast is sharpest it will ever be. Live: Remi '
        'at thirty-one. Greatest Hits: the scene itself, rewarding total '
        'immersion for fifty years without asking if it serves the '
        'individual.</p><p><strong class="lead">Ch22:</strong>'
    )
    new_ch19_22 = (
        '<p><strong class="lead">Ch19:</strong> Debut: the twenty-three at '
        'first festival, contrast is sharpest it will ever be. Live: Remi '
        'at thirty-one. Greatest Hits: the scene itself, rewarding total '
        'immersion for fifty years without asking if it serves the '
        'individual.</p><p><strong class="lead">Ch20:</strong> Debut: the '
        'twenty-three-year-old who noticed people are different after '
        'events than before and filed a good-timing text as good timing. '
        'Live: Damian, thirty-one, who has never once texted during the '
        'festival, on purpose. Greatest Hits: the festival that emails '
        'next year’s early-bird link while the parking lot is still '
        'full of people breaking camp.</p><p><strong class="lead">Ch21:'
        '</strong> Debut: the new crew running the briefing for the first '
        'time at forty percent capacity — code word forgotten, buddy '
        'system dissolved, nobody disappeared. Live: Sister Lou Mantilla, '
        'eleven years, one clipboard, seventeen minutes, zero incidents. '
        'Greatest Hits: the festival that built harm reduction as a '
        'permanent structure instead of a volunteer afterthought.</p>'
        '<p><strong class="lead">Ch22:</strong>'
    )
    c3 = src.count(old_ch19_22)
    if c3 == 0 and 'Ch20:</strong> Debut: the twenty-three-year-old who noticed people are different' in src:
        note("apG-ch20-21", 0, "already added")
    elif c3 == 1:
        src = src.replace(old_ch19_22, new_ch19_22, 1)
        n += 1
        note("apG-ch20-21", 1, "Ch20 and Ch21 Discog entries added")
    else:
        sys.exit("apG: Ch19/Ch22 boundary not found as expected (found %d times)" % c3)

    old_ch23 = (
        '<p><strong class="lead">Ch23:</strong> Debut: twenty-two with '
        'recognition but not yet inventory. Live: David Reyes, '
        'forty-nine. Greatest Hits: every Chapter 22 that didn’t get '
        'written.</p>'
    )
    new_ch23 = (
        '<p><strong class="lead">Ch23:</strong> Debut: twenty-two with '
        'recognition but not yet inventory. Live: David Reyes, '
        'forty-nine. Greatest Hits: the book itself — the field '
        'manual about manipulation that used manipulation to teach you '
        'about manipulation, with the author’s own name on the '
        'inventory.</p>'
    )
    c4 = src.count(old_ch23)
    if c4 == 0 and new_ch23 in src:
        note("apG-ch23-fix", 0, "already corrected")
    elif c4 == 1:
        src = src.replace(old_ch23, new_ch23, 1)
        n += 1
        note("apG-ch23-fix", 1,
             "mismatched 'Chapter 22' cross-reference replaced with "
             "chapter 23's own Greatest Hits content")
    else:
        sys.exit("apG: Ch23 entry not found as expected (found %d times)" % c4)

    old_ch24_end = (
        '<p><strong class="lead">Ch24:</strong> Debut: the first-timer who '
        'now knows the Validator category. Live: the Rebrand Tour in '
        'progress. Greatest Hits: the festival that received the form in '
        'March.</p></section>'
    )
    new_ch24_end = (
        '<p><strong class="lead">Ch24:</strong> Debut: the first-timer who '
        'now knows the Validator category. Live: the Rebrand Tour in '
        'progress. Greatest Hits: the festival that received the form in '
        'March.</p><p><strong class="lead">Ch25:</strong> Debut: the '
        'writer in year two who discovered that opening on a concrete '
        'disaster gets more attention than opening on an abstraction, and '
        'used it before naming it. Live: this chapter, confessing all '
        'sixteen moves by name. Greatest Hits: every book about '
        'manipulation that never disclosed its own use of the mechanisms '
        'it described — this one does.</p><p><strong class="lead">'
        'Ch26:</strong> Debut: the twenty-three-year-old reading this '
        'book for the first time, some of it landing, most of it waiting '
        'for the specific moment it’ll be needed. Live: Cara, '
        'twenty-six, six months out, opening her own bottles now. '
        'Greatest Hits: the festival that built the whole structure '
        '— the reporting pathway, the accountability hire, the '
        'compact — and turned a would-be crisis into four hours '
        'instead of October.</p></section>'
    )
    c5 = src.count(old_ch24_end)
    if c5 == 0 and 'Ch26:</strong> Debut: the twenty-three-year-old reading this book' in src:
        note("apG-ch25-26", 0, "already added")
    elif c5 == 1:
        src = src.replace(old_ch24_end, new_ch24_end, 1)
        n += 1
        note("apG-ch25-26", 1, "Ch25 and Ch26 Discog entries added")
    else:
        sys.exit("apG: Ch24/end boundary not found as expected (found %d times)" % c5)

    return src


STEPS = [fix_apQ_duplicate, fix_sixteen_moves_canon, fix_apG_missing]


def main():
    src = WOOK.read_text(encoding="utf-8")
    before = len(src)
    for step in STEPS:
        src = step(src)
    WOOK.write_text(src, encoding="utf-8")
    width = max(len(s) for s, _, _ in log) if log else 0
    for step, n, what in log:
        print(f"  {step:<{width}}  {n:>3}  {what}")
    print(f"\n{before:,} -> {len(src):,} bytes")


if __name__ == "__main__":
    main()

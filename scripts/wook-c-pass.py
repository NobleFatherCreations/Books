#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pass C of the full review: front matter, standalone sections, appendices.

See content/wook-audits/wook-full-review-plan.md.

Idempotent.

Run: python3 scripts/wook-c-pass.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WOOK = ROOT / "library/wook/index.html"

log = []


def note(step, n, what):
    log.append((step, n, what))


def fix_apU_chapter(src):
    """Appendix U's vocabulary table is chapter 18's coercive-group
    language ("the container," "holding space," "surrender to the
    medicine," "we need you on the rail"), attributed to chapter 16
    (the missing-friend chapter, which has nothing to do with any of it).
    Same three-chapter-insertion drift as the B7 fixes: 18 minus the two
    insertions before it (at 11, 13) is 16.
    """
    bad = "APPENDIX U — The Vocabulary Translation List</h2><p>From Chapter 16."
    n = src.count(bad)
    if n == 0:
        note("apU-chapter", 0, "already corrected")
        return src
    if n > 1:
        sys.exit("apU: heading not found exactly once")
    src = src.replace(
        bad,
        "APPENDIX U — The Vocabulary Translation List</h2><p>From Chapter 18.",
        1)
    note("apU-chapter", 1, "vocabulary list's source chapter corrected to 18")
    return src


def fix_front_matter_confession(src):
    """The "Before We Roll" front matter names the wrong chapter for the
    book's own confession, twice in one sentence. The Content Disclosure
    section elsewhere in the same front matter already gets this right
    ("Chapter 25: The book confesses its persuasion techniques"); this
    passage still says 22. Same drift as the other fixes in this pass.
    """
    bad = ("<strong class=\"lead\">On Chapter 22:</strong> The book, at "
           "Chapter 22, confesses the persuasion techniques it used on "
           "you to get you to trust it.")
    n = src.count(bad)
    if n == 0:
        note("front-matter-confession", 0, "already corrected")
        return src
    if n > 1:
        sys.exit("front matter: confession sentence matched more than once")
    new = ("<strong class=\"lead\">On Chapter 25:</strong> The book, at "
           "Chapter 25, confesses the persuasion techniques it used on "
           "you to get you to trust it.")
    src = src.replace(bad, new, 1)
    note("front-matter-confession", 1,
         "both chapter-22 references corrected to 25, matching the "
         "Content Disclosure section")
    return src


def fix_front_matter_3am_voice(src):
    """The front matter's 3 a.m. resource note points to the wrong
    chapter and Track. "The voice sounds like yours but says things you
    would never say to someone you love" is chapter 22's 3 A.M. Encore --
    its own cold open is built entirely around that voice, and THE 3 A.M.
    ENCORE is the first Track listed in that chapter's own Setlist.
    Chapter 19 (Festie Hollowing) has no 3 a.m.-voice content at all.
    """
    bad = "that is Chapter 19, Track 1."
    n = src.count(bad)
    if n == 0:
        note("front-matter-3am-voice", 0, "already corrected")
        return src
    if n > 1:
        sys.exit("front matter: 3am-voice sentence matched more than once")
    src = src.replace(bad, "that is Chapter 22, Track 1.", 1)
    note("front-matter-3am-voice", 1,
         "3 a.m. voice pointer corrected to chapter 22, its own source chapter")
    return src


def fix_alsoby_placeholder(src):
    """The "Also By The PLURth Angel" section is entirely unfilled Vellum
    ebook-export placeholder text shipping live: "[List other titles
    here... you can delete this element in Vellum...]" followed by two
    literal "[Title Two] — [one-line description]" lines. No real
    bibliography data exists to fill it with, and CLAUDE.md's standing
    rule is explicit: never ship build-instruction placeholders to a live
    page. Same category the colophon's ISBN/publisher/newsletter block
    was in before v8 removed it. Removed rather than invented.
    """
    marker = '<section class="panel pp-cream prose" id="alsoby">'
    if marker not in src:
        note("alsoby-placeholder", 0, "already removed")
        return src
    start = src.index(marker)
    end = src.index("</section>", start) + len("</section>")
    src = src[:start] + src[end:]
    note("alsoby-placeholder", 1,
         "unfilled Vellum 'Also By' placeholder section removed")
    return src


STEPS = [fix_apU_chapter, fix_front_matter_confession, fix_front_matter_3am_voice,
         fix_alsoby_placeholder]


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

#!/usr/bin/env python3
"""Idempotent grammar/spelling/formatting fixes for The Festie Codex (v13).

Applies the same corrections to the live book and to the new-chapter source
fragments so the two never drift. Every change here was confirmed by hand
against its surrounding sentence — see scripts/wook-grammar-check.py for the
sweep that surfaced them.
"""
import glob
import re
import sys

BOOK = "library/wook/index.html"
FRAGMENTS = sorted(glob.glob("content/wook-new-chapters/*.html"))

# House style is American throughout (behavior 316, defense 32, recognize 17).
# These British forms all arrived with the seven new chapters.
DIALECT = [
    ("recognising", "recognizing"), ("organising", "organizing"),
    ("memorise", "memorize"), ("organised", "organized"),
    ("mobilise", "mobilize"), ("rationalisation", "rationalization"),
    ("recognises", "recognizes"), ("recognise", "recognize"),
    ("metabolise", "metabolize"), ("apologised", "apologized"),
    ("realising", "realizing"), ("hospitalised", "hospitalized"),
    ("monetised", "monetized"), ("behavioural", "behavioral"),
    ("behaviours", "behaviors"), ("behaviour", "behavior"),
    ("defence", "defense"), ("offence", "offense"),
    ("practising", "practicing"), ("reorganises", "reorganizes"),
]

# Everything else: exact strings, so a near-miss fails loudly instead of
# silently rewriting the wrong sentence.
EXACT = [
    # article agreement
    ("in a accountability conversation", "in an accountability conversation"),
    # the book spells this out in the three other places it says it
    ("All 50 US states have some form as of 2026.",
     "All fifty US states have some form as of 2026."),
    # remaining British forms, replaced as exact strings so the nav chrome's
    # "The Catalogue" (a Noble Father Creations proper noun) is never touched
    ("the organisers cannot face", "the organizers cannot face"),
    ("the nonbinary organiser who", "the nonbinary organizer who"),
    ("sealed, labelled with a number", "sealed, labeled with a number"),
    ("your entire public catalogue", "your entire public catalog"),
    ("Your entire public catalogue", "Your entire public catalog"),
    ("is being catalogued for", "is being cataloged for"),
    ("have catalogued a set of techniques", "have cataloged a set of techniques"),
]

# Appendix U shipped as a literal Markdown table — pipes and padding spaces
# rendered in the body face, so the columns did not even line up. Rebuilt in
# the book's own pair pattern (<strong class="lead">), which is what every
# other appendix uses. The last three rows translate to themselves on purpose.
APU_ROWS = [
    ("“The work”", "Doing what the head of the group needs"),
    ("“The container”", "The group’s structure and the head’s authority over it"),
    ("“Not ready”", "Disagreed with the head and left"),
    ("“Beautiful breakthrough”", "I have no memory of what happened"),
    ("“We need you on the rail tonight”", "You are required to be physically present near me"),
    ("“Sister” / “Brother”", "You have been categorized and are being managed"),
    ("“Sacred space”", "A private space without external accountability"),
    ("“Holding space”", "Staying in this conversation"),
    ("“Your resistance is fear”", "I dislike your no"),
    ("“Surrender to the medicine”", "Remove your capacity to say no"),
    ("“The universe brought us together”", "I want access to you"),
    ("“You haven’t done the work”", "You are not complying"),
    ("“They weren’t ready”", "They left for reasons that implicate us"),
    ("“I don’t consent to a search”", "I don’t consent to a search"),
    ("“Am I being detained?”", "Am I being detained?"),
    ("“I want a lawyer”", "I want a lawyer"),
]


def fix_appendix_u(src):
    """Replace the raw pipe table in Appendix U with the house pair pattern."""
    table = re.compile(r"(?:<p>\|[^<]*</p>)+")
    anchor = src.find("APPENDIX U —")
    if anchor < 0:
        return src, 0
    m = table.search(src, anchor)
    if not m:
        return src, 0  # already converted
    rebuilt = "".join(
        '<p><strong class="lead">{}</strong>&nbsp;→ {}</p>'.format(term, plain)
        for term, plain in APU_ROWS
    )
    return src[:m.start()] + rebuilt + src[m.end():], m.group(0).count("<p>")


def main():
    total = 0
    for path in [BOOK] + FRAGMENTS:
        src = open(path, encoding="utf-8").read()
        before = src
        counts = {}

        for brit, amer in DIALECT:
            src, n = re.subn(r"\b" + brit + r"\b", amer, src)
            src, n2 = re.subn(r"\b" + brit.capitalize() + r"\b", amer.capitalize(), src)
            if n + n2:
                counts[brit] = n + n2

        for old, new in EXACT:
            n = src.count(old)
            if n:
                src = src.replace(old, new)
                counts[old[:34]] = n

        if path == BOOK:
            src, n = fix_appendix_u(src)
            if n:
                counts["Appendix U pipe table"] = n

        if src != before:
            open(path, "w", encoding="utf-8").write(src)
            total += sum(counts.values())
            print(path)
            for k, v in sorted(counts.items()):
                print("   {:<36} {}".format(k, v))

    print("\n{} substitutions".format(total) if total else "\nnothing to fix (already clean)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

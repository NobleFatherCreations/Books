#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply the 2026-09-14 proofreading round to Wook in Sheep's Clothing.

Every edit here was found by scripts/wook-proofread.py, which reads the
surface of the prose the way the continuity checker reads its claims. Run
the checker after this to confirm the count goes to zero.

Idempotent: safe to re-run, each step is a no-op once applied.

Run: python3 scripts/wook-proofread-pass.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WOOK = ROOT / "library/wook/index.html"

log = []


def note(step, n, what):
    log.append((step, n, what))


def fix_doubled_quotes(src):
    """The 25 cold-open titles rendered as ""The Tank"".

    comp-name carries both the entity pair and a literal curly pair, so the
    reader sees two opening and two closing marks around every cold-open
    title in the book.
    """
    src, n = re.subn(r'(<p class="comp-name">)&ldquo;(“[^<]*”)&rdquo;(</p>)',
                     r'\1\2\3', src)
    note("doubled-quotes", n, "cold-open titles no longer double their quotation marks")
    return src


def fix_reversed_open_quote(src):
    """A closing mark used to open a quotation: ”[Name] would say …”

    Five of the six are script templates that open on a bracketed fill-in
    slot; the sixth is chapter 16's ”…Okonkwo?” opening on an ellipsis.
    """
    src, n = re.subn(r'”(?=\[)|(?<=</strong> )”(?=…)', '“', src)
    note("reversed-quote", n, "closing quotation mark that was opening a quotation")
    return src


# Contractions and possessives, including the plural possessive that ends
# on the apostrophe -- girls' stuff, the occupants' identities.
APOS = re.compile(r"(?<=[A-Za-z])'(?=[A-Za-z])|(?<=s)'(?=\s)")


def fix_apostrophes(src):
    """Straight apostrophes, all of them introduced by the v7/v8 passes.

    The manuscript is set in curly apostrophes everywhere else, so the Field
    Specimens, RUNS cards and rotated SOBER TUESDAY cards written by script
    read as a different typeface mid-sentence. Text nodes only -- script,
    style and every attribute value are left alone.
    """
    out, pos, n = [], 0, 0
    for m in re.finditer(r'<(script|style)\b.*?</\1>|<[^>]+>', src, re.S):
        chunk = src[pos:m.start()]
        fixed, k = re.subn(APOS, "’", chunk)
        out.append(fixed)
        out.append(m.group(0))
        n += k
        pos = m.end()
    tail, k = re.subn(APOS, "’", src[pos:])
    out.append(tail)
    n += k
    note("apostrophes", n, "straight apostrophes made curly to match the rest of the book")
    return "".join(out)


def fix_orphan_emoji(src):
    """Appendix B and V lost their icons and kept the variation selector.

    Same scar the v8 pass repaired on O and R -- a bare U+FE0F where an
    emoji used to be, which renders as nothing and leaves the heading
    starting with a space.
    """
    n = 0
    for ap, emoji in (("apB", "👥"), ("apV", "💰")):
        pat = r'(id="%s"><h2 class="zine-h sm">)️\s*' % ap
        src, k = re.subn(pat, r'\1%s ' % emoji, src)
        n += k
    note("orphan-emoji", n, "appendix headings that had lost their icon")
    return src


def fix_appendix_q(src):
    """Appendix Q: the nav still said Seventeen, and the list skipped 14."""
    src, n1 = re.subn(r'(<span class="n">Q</span>)The Seventeen Moves',
                      r'\1The Sixteen Moves', src)
    note("appendix-q-label", n1, "nav label caught up with the retitled appendix")

    # Scoped to the appendix itself: chapter 23's confession list carries its
    # own item 14, so a whole-document search always reports it as present.
    start = src.find('id="apQ"')
    end = src.find('</section>', start)
    block = src[start:end]
    n2 = 0
    if '14. The Kandi Trade Vows' not in block:
        marker = '<p>13. The Counter-Drops’ Action Bias</p>'
        i = block.find(marker)
        if i == -1:
            sys.exit("appendix Q: item 13 not found, cannot place item 14")
        cut = start + i + len(marker)
        src = (src[:cut] +
               '<p>14. The Kandi Trade Vows As Group Identification</p>' +
               src[cut:])
        n2 = 1
    note("appendix-q-item", n2,
         "the sixteenth move restored to an appendix that listed fifteen")
    return src


def fix_appendix_s(src):
    """Appendix S was the only one of 26 using the larger heading class."""
    src, n = re.subn(r'(id="apS"><h2 class="zine-h)(">)', r'\1 sm\2', src)
    note("appendix-s-class", n, "appendix heading matched to its 25 siblings")
    return src


def fix_resources_chips(src):
    """Chapter 22's Resources Appendix is reference material, not scripts.

    The v7 split keyed on the words SAFETY APPENDIX and so never saw the one
    block called RESOURCES APPENDIX. Thirty hotline numbers, recovery
    timelines and an intake script were still rendering as six-word pocket
    pills -- one of them 62 words long.
    """
    marker = '<p class="plain-tag">🔰 RESOURCES APPENDIX — CHAPTER 22</p>'
    i = src.find(marker)
    if i == -1:
        note("resources-chips", 0, "already reclassed")
        return src
    # The block runs to the end of its enclosing card.
    end = src.find('</div>', i)
    block = src[i:end]
    block, n = re.subn(r'<span class="chip">', '<span class="chip appendix">', block)
    note("resources-chips", n,
         "reference chips in ch22 given the appendix shape instead of the pill")
    return src[:i] + block + src[end:]


def fix_stumbles(src):
    """Two sentences that read as typos even though one of them isn't."""
    n = 0
    src, k = re.subn(r'I tell her her work has', 'I tell her that her work has', src)
    n += k
    src, k = re.subn(r'called the outcomes outcomes',
                     'called the outcomes “outcomes.”', src)
    n += k
    # The sentence now ends inside the quotation; drop the old full stop.
    src = src.replace('called the outcomes “outcomes.”.', 'called the outcomes “outcomes.”')
    note("stumbles", n, "doubled words that read as errors")
    return src


POSTERS = {
    21: ("THE 3-TIER ANCHOR SYSTEM · THE PRE-SHOW CREW BRIEFING · "
         "THE CODE-WORD PROTOCOL · THE ANCHOR’S BILL OF RIGHTS · "
         "THE ANCHOR BACKUP PLAN", "5 PROTOCOLS"),
    25: ("THE RECIPROCITY HOOK · THE TRAUMA TAX · THE HALO OF THE NAMED "
         "THINKERS · THE WATERMELON MOMENT · THE SUNRISE SETS AS SERMON · "
         "+11 MORE", "16 CONFESSIONS"),
    26: ("THE KNOWN PERIMETER · THE VETTED COMMUNITY · THE IDENTITY FLOOR · "
         "THE ACCOUNTABILITY PRACTICE · THE PASSED-FORWARD INFORMATION",
         "5 PILLARS"),
}


def fix_posters(src):
    """Three posters shipped an empty key line and a 0 TRACKS count.

    Chapters 21, 25 and 26 are the book's trackless ones, and their posters
    said so by rendering a blank line and the number zero. They do have
    named components -- protocols, confessions, pillars -- so the poster now
    names them the way every other chapter's poster names its Tracks.
    """
    n = 0
    for ch, (keys, unit) in POSTERS.items():
        i = src.find('id="ch%d"' % ch)
        if i == -1:
            sys.exit("chapter %d not found" % ch)
        seg = src[i:i + 1600]
        new = seg.replace('<p class="poster-keys"></p>',
                          '<p class="poster-keys">%s</p>' % keys)
        new = re.sub(r'(<p class="poster-meta">⏱ ~\d+ MIN READ · )0 TRACKS',
                     r'\g<1>%s' % unit, new)
        if new != seg:
            src = src[:i] + new + src[i + 1600:]
            n += 1
    note("posters", n, "trackless posters now name their own components")
    return src


STEPS = [fix_doubled_quotes, fix_reversed_open_quote, fix_apostrophes,
         fix_orphan_emoji, fix_appendix_q, fix_appendix_s,
         fix_resources_chips, fix_stumbles, fix_posters]


def main():
    src = WOOK.read_text(encoding="utf-8")
    before = len(src)
    for step in STEPS:
        src = step(src)
    WOOK.write_text(src, encoding="utf-8")
    width = max(len(s) for s, _, _ in log)
    for step, n, what in log:
        print(f"  {step:<{width}}  {n:>4}  {what}")
    print(f"\n{before:,} -> {len(src):,} bytes")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The expansion splice: take the book from 26 chapters to 33.

Renumbers every cross-reference through the old-to-new map, rewrites the
seven bridges that now point at a new chapter, splices the seven written
fragments into their slots, and reconciles the set boundaries, the
contents drawer, the field-specimen numbering, the front matter and the
appendices.

See content/wook-audits/wook-expansion-plan.md.

Idempotent: every step checks whether it has already run.

Run: python3 scripts/wook-expansion-pass.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WOOK = ROOT / "library/wook/index.html"
FRAGS = ROOT / "content/wook-new-chapters"

OLD2NEW = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 7, 7: 8, 8: 9, 9: 11, 10: 12,
           11: 13, 12: 15, 13: 16, 14: 18, 15: 19, 16: 21, 17: 22, 18: 23,
           19: 24, 20: 25, 21: 27, 22: 28, 23: 29, 24: 30, 25: 32, 26: 33}

# new chapter -> the old chapter it is inserted immediately after
INSERT_AFTER = {6: 5, 10: 8, 14: 11, 17: 13, 20: 15, 26: 20, 31: 24}

DONE_MARKER = 'data-ch="33"'          # only exists once the renumber has run
ALREADY = False                        # set once in main(), before anything mutates
PROT = "\x01"                          # wraps numbers the generic pass must skip

log = []


def note(step, n, what):
    log.append((step, n, what))


def p(n):
    """Protect a already-correct new number from the generic renumber."""
    return f"{PROT}{n}{PROT}"


def sub_once(src, old, new, step, what):
    c = src.count(old)
    if c != 1:
        sys.exit(f"{step}: expected 1 match, found {c} for: {old[:90]!r}")
    note(step, 1, what)
    return src.replace(old, new, 1)


# ---------------------------------------------------------------- step 1

EXPLICIT_BEFORE_RENUMBER = [
    # (old text, new text with protected numbers, description)
    ("Sets One and Two — Chapters 1 through 20 — name the patterns.",
     f"Sets One and Two — Chapters {p(1)} through {p(26)} — name the patterns.",
     "front matter: Set One+Two range"),
    ("The Encore — Chapters 21 through 26 — builds the structure.",
     f"The Encore — Chapters {p(27)} through {p(33)} — builds the structure.",
     "front matter: Encore range"),
    ("Chapters 9 through 18:</strong> Detailed material about substance use",
     f"Chapters {p(11)} through {p(23)}:</strong> Detailed material about substance use",
     "content disclosure: substance range"),
    ("Fifteen minutes. Prevents Chapters 9, 10, 12, 14, 15, and 16.",
     f"Fifteen minutes. Prevents Chapters {p(11)}, {p(12)}, {p(15)}, {p(18)}, {p(19)}, and {p(21)}.",
     "briefing: prevented-chapter list"),
    ("In Chapter 10, there are rights you can invoke. In Chapter 11 and 12,",
     f"In Chapter {p(12)}, there are rights you can invoke. In Chapter {p(13)} and {p(15)},",
     "rights/protocols pointer pair"),
    ("Chapters 22 and 23 are for the people who are already in t",
     f"Chapters {p(28)} and {p(29)} are for the people who are already in t",
     "aftermath/accountability pointer pair"),
    ("You have run this drill before in abbreviated forms in Chapters 9, 12, 13, and 14.",
     f"You have run this drill before in abbreviated forms in Chapters {p(11)}, {p(15)}, {p(16)}, and {p(18)}.",
     "abbreviated-briefing chapter list"),
    ("Chapters 6 through 10 presented patterns in a sequence design",
     f"Chapters {p(7)}, {p(8)}, {p(9)}, {p(11)} and {p(12)} presented patterns in a sequence design",
     "confession seven: sequence list (in-chapter)"),
    ("Chapters 6 through 10 were sequenced to produce cumulative re",
     f"Chapters {p(7)}, {p(8)}, {p(9)}, {p(11)} and {p(12)} were sequenced to produce cumulative re",
     "confession seven: sequence list (confession)"),
    ("comfortably observe in others (Chapters 6 and 7) to patterns",
     f"comfortably observe in others (Chapters {p(7)} and {p(8)}) to patterns",
     "confession seven: first pair"),
    ("from your own experience (Chapters 8 and 9) to patterns",
     f"from your own experience (Chapters {p(9)} and {p(11)}) to patterns",
     "confession seven: second pair"),
    ("The warnings are in Chapters 1 through 16. The recovery is in Chapter 22.",
     f"The warnings are in Chapters {p(1)} through {p(21)}. The recovery is in Chapter {p(28)}.",
     "closing argument: warnings/recovery ranges"),
    ("All nine Safety Appendixes consolidated. Chapters 9–17.",
     f"All nine Safety Appendixes consolidated. Chapters {p(11)}, {p(12)}, {p(13)}, {p(15)}, "
     f"{p(16)}, {p(18)}, {p(19)}, {p(21)} and {p(22)}.",
     "Appendix D: safety-appendix chapter list"),
    ("7. The Pattern Confirmation Loop (Chapters 6–10)",
     f"7. The Pattern Confirmation Loop (Chapters {p(7)}, {p(8)}, {p(9)}, {p(11)}, {p(12)})",
     "Appendix Q: confession seven range"),
    ("Three chapters carry no Tracks &mdash; 21, 25 and 26 &mdash; and say so in place.",
     f"Five chapters carry no Tracks &mdash; {p(20)}, {p(27)}, {p(31)}, {p(32)} and {p(33)} "
     "&mdash; and say so in place.",
     "Appendix A: no-Tracks chapter list"),
    ("If you are in a coercive crew, go to Chapter 21. If you are in the aftermath, go to Chapter 22.",
     f"If you are in a coercive crew, go to Chapter {p(27)}. If you are in the first twelve hours "
     f"after something happened, go to Chapter {p(20)}. If you are in the long after, go to "
     f"Chapter {p(28)}.",
     "HOW TO READ way 2: aftermath routing"),
]

# word-form counts: (old phrase, new phrase, description)
WORD_COUNTS = [
    ("spend twenty-two chapters nodding", "spend twenty-eight chapters nodding",
     "front matter: chapters before the confession"),
    ("Accumulates across twenty-six chapters.", "Accumulates across thirty-three chapters.",
     "Kandi Trade device note"),
    ("— Twenty-six chapters. Three sets. One night.",
     "— Thirty-three chapters. Three sets. One night.",
     "THE SETLIST heading"),
    ("the only thing that matters in all twenty-six chapters",
     "the only thing that matters in all thirty-three chapters", "ch1"),
    ("The next fifteen chapters are the <mark class=\"mk-y\">Wooks</mark> by name",
     "The next twenty-one chapters are the <mark class=\"mk-y\">Wooks</mark> by name",
     "ch5: Set Two length"),
    ("the entire book has been twenty chapters of interesting things",
     "the entire book has been twenty-six chapters of interesting things", "ch21 (new 27)"),
    ("skipping the mirror checks for twenty-two chapters",
     "skipping the mirror checks for twenty-eight chapters", "ch22 bridge (new 28)"),
    ("which is now, twenty-two chapters later", "which is now, twenty-eight chapters later",
     "ch23 (new 29)"),
    ("doing the mirror checks for twenty-two chapters",
     "doing the mirror checks for twenty-eight chapters", "ch23 (new 29)"),
    ("We have spent twenty-two chapters together.", "We have spent twenty-eight chapters together.",
     "ch23 confession opening"),
    ("You have given me twenty-two chapters of your time",
     "You have given me twenty-eight chapters of your time", "ch23 confession"),
    ("you have been building toward it for twenty-two chapters",
     "you have been building toward it for twenty-eight chapters", "ch23 confession move 9"),
    ("persuasion techniques on you for twenty-two chapters",
     "persuasion techniques on you for twenty-eight chapters", "ch23 confession move 16"),
    ("The twenty chapters of engineered recognition",
     "The twenty-eight chapters of engineered recognition", "ch23: leftover undercount"),
    ("from across the full twenty-three chapters of the scene",
     "from across the full twenty-nine chapters of the scene", "ch24 (new 30)"),
    ("This book has twenty-five chapters of unpreventable harm.",
     "This book has thirty-two chapters of unpreventable harm.", "ch24 (new 30)"),
    ("We have spent twenty-four chapters together.", "We have spent thirty-one chapters together.",
     "ch25 (new 32)"),
    ("You have carried it through twenty-four chapters of cold opens",
     "You have carried it through thirty-one chapters of cold opens", "ch25 (new 32)"),
    ("I have also, in the twenty-four chapters you have just read",
     "I have also, in the thirty-one chapters you have just read", "ch25 (new 32)"),
    ("the yes you have been saying to this book for twenty-four chapters",
     "the yes you have been saying to this book for thirty-one chapters", "ch25 (new 32)"),
    ("You have been reading about manipulation for twenty-four chapters.",
     "You have been reading about manipulation for thirty-one chapters.", "ch25 (new 32) mirror"),
    ("The twenty-four chapters before this one.", "The thirty-one chapters before this one.",
     "ch25 (new 32) discog"),
    ("The Live Album sounds like twenty-four chapters of a book",
     "The Live Album sounds like thirty-one chapters of a book", "ch25 (new 32) discog"),
    ("It is also a twenty-four-chapter persuasion operation.",
     "It is also a thirty-one-chapter persuasion operation.", "ch25 (new 32) discog"),
    ("This conversation, now, after twenty-four chapters,",
     "This conversation, now, after thirty-one chapters,", "ch25 (new 32)"),
    ("The scene you have been reading about for twenty-four chapters",
     "The scene you have been reading about for thirty-one chapters", "ch25 (new 32)"),
    ("everyone else’s for twenty-five chapters", "everyone else’s for thirty-two chapters",
     "ch26 (new 33)"),
    ("Twenty-five chapters of mirrors.", "Thirty-two chapters of mirrors.", "ch26 (new 33) mirror"),
    ("been about both of them for twenty-five chapters",
     "been about both of them for thirty-two chapters", "ch26 (new 33)"),
    ("<p>The next six chapters are something different.</p>",
     "<p>One more <mark class=\"mk-y\">Wook</mark> follows — the one who does not stop when the "
     "festival does. Then seven chapters that are something different.</p>",
     "old ch20 (new 25): what comes next is no longer the Encore"),
]

RENUMBER_PATTERNS = [
    r'(?<=data-ch=")(\d+)(?=")',
    r'(?<=id="ch)(\d+)(?=")',
    r'(?<=href="#ch)(\d+)(?=")',
    r'(?<=\bChapter )(\d+)\b',
    r'(?<=\bChapters )(\d+)\b',
    r'(?<=\bCHAPTER )(\d+)\b',
    r'(?<=\bCh)(\d+)\b',
    r'(?<=<p class="poster-num">)(\d+)(?=</p>)',
    r'(?<=<span class="n">)(\d+)(?=</span>)',
]


def renumber(src):
    """Map every numeric chapter reference through OLD2NEW.

    Two passes with a sentinel so that a number rewritten early cannot be
    rewritten again by a later match (6 -> 7 then 7 -> 8 would cascade).
    """
    if ALREADY:
        note("renumber", 0, "already renumbered")
        return src

    for old, new, what in EXPLICIT_BEFORE_RENUMBER:
        src = sub_once(src, old, new, "explicit-range", what)

    def mark(m):
        n = int(m.group(1))
        return f"\x00{OLD2NEW[n]}\x00" if n in OLD2NEW else m.group(1)

    total = 0
    for pat in RENUMBER_PATTERNS:
        src, k = re.subn(pat, mark, src)
        total += k

    # the setlist's own numbers are zero-padded
    def mark_sl(m):
        n = int(m.group(1))
        return f'<span class="sl-num">\x00{OLD2NEW[n]:02d}\x00</span>'
    src, k = re.subn(r'<span class="sl-num">(\d+)</span>', mark_sl, src)
    total += k

    # field specimens keep their zero padding
    def mark_spec(m):
        n = int(m.group(1))
        return f"FIELD SPECIMEN №\x00{OLD2NEW[n]:02d}\x00"
    src, k = re.subn(r'FIELD SPECIMEN №(\d+)', mark_spec, src)
    total += k

    src = re.sub(r"\x00(\d+)\x00", r"\1", src)
    note("renumber", total, f"{total} numeric chapter references remapped")
    return src


def word_counts(src):
    if ALREADY:
        note("word-counts", 0, "already applied")
        return src
    for old, new, what in WORD_COUNTS:
        src = sub_once(src, old, new, "word-count", what)
    return src


def mirror_count(src):
    """ch23's 'nineteen chapters of small have-you-ever questions' has to
    match how many chapters before it actually carry a Mirror Set."""
    if ALREADY:
        note("mirror-count", 0, "already applied")
        return src
    old = "It is not the mirror from nineteen chapters of small"
    new = "It is not the mirror from twenty-five chapters of small"
    return sub_once(src, old, new, "mirror-count",
                    "ch23 (new 29): mirror-bearing chapters before it, 19 + 6 new")


STEPS_A = [renumber, word_counts, mirror_count]




# ---------------------------------------------------------------- step 2
# Everything below runs on the already-renumbered book and is guarded by
# SPLICED, which is only true once the fragments are in.

SPLICED_MARKER = 'data-ch="6"'

# new chapter -> the (renumbered) chapter it is inserted immediately after
AFTER_NEW = {6: 5, 10: 9, 14: 13, 17: 16, 20: 19, 26: 25, 31: 30}

NEW_META = {
    6:  ("The Group Chat", "He Was Already Your Friend Before You Parked"),
    10: ("The Love Of It", "The Economy That Runs On People Who Would Do It Anyway"),
    14: ("The Two Festivals", "Same Gate, Same Wristband, Different Weekend"),
    17: ("The Container", "The Ceremony, The Lineage, And The Cup Nobody Measured"),
    20: ("The Next Twelve Hours", "The One Chapter Written For After"),
    26: ("He Still Has Your Number", "The Part That Follows You Home"),
    31: ("What To Tell Your Mom", "The One Chapter Written To Be Handed To Somebody Else"),
}

BRIDGES = {
    5: "<p>You have brought everything through the gate — the Trifecta, the twelve levers, "
       "the nine bugs, the chemical cage, and the sober word. Set Two begins now, and it does "
       "not begin at the gate. Chapter 6 is eleven weeks earlier, in a Facebook group with four "
       "thousand members, where a man who has answered four hundred and six questions correctly "
       "is about to answer yours.</p>",
    9: "<p>Asha drove home with her bins. Chapter 10 is the other half of that same economy — "
       "three hundred people behind the fence on a Wednesday nobody will ever know about, "
       "building the thing for a wristband, and the forty minutes after one of them comes off a "
       "six-foot ladder.</p>",
    13: "<p>The corridor is behind them. Chapter 14 is about who gets stopped on that road in "
        "the first place, who gets asked to step out, and what it costs to walk across a field "
        "at one in the morning running eleven adjustments that nobody walking beside you can "
        "see.</p>",
    16: "<p>The jar is back in his bag. The seal is on the water Yara carried herself. Chapter "
        "17 is the same jar with a lineage, an altar, an intake form, twenty-two people paying "
        "four hundred dollars each, and a second appointment already on the calendar.</p>",
    19: "<p>Dev’s hat is still on his head and his weekend is intact. Chapter 20 is the one this "
        "book owes the people whose weekend was not. It starts at twenty to six in the morning, "
        "it is the only chapter here written for after rather than before, and it will keep "
        "until you need it.</p><p>Chapter 20</p>",
    25: "<p>Tuesday has come. The wristband is in a box with eleven others. Chapter 26 is the "
        "text that arrives the Tuesday after that, and the one after that, for eleven weeks — "
        "and then buys a ticket to the October event, because it is a public event and he is "
        "allowed to be there.</p>",
    30: "<p>The napkin is now four cases in a legal consultation and forty-six thousand people "
        "who got the advisory and three lineups that changed quietly. Chapter 31 is the one "
        "chapter in this book written to be handed to somebody else — to the person at a kitchen "
        "table four hundred miles away who has just read all thirty of these and has four "
        "drafted texts and no idea which one to send.</p>",
}

SYMBOL_COLOURS = {
    6:  ("#8B6BFF", "#FFD94A"), 10: ("#3FD9B0", "#FF5C9E"),
    14: ("#FF9A3D", "#8B6BFF"), 17: ("#D8FF3D", "#6747E8"),
    20: ("#FFD94A", "#3FD9B0"), 26: ("#FF5C9E", "#D8FF3D"),
    31: ("#6747E8", "#FF9A3D"),
}
SYMBOL_IDS = {6: "spec-helpfulone", 10: "spec-coreteam", 14: "spec-secondlook",
              17: "spec-facilitator", 20: "spec-whodrove", 26: "spec-stillhere",
              31: "spec-sentmoney"}


def set_bridge(src, ch, inner):
    """Replace the body of chapter `ch`'s BRIDGE panel."""
    i = src.find(f'data-ch="{ch}"')
    j = src.find(f'<i class="ch-end" data-ch="{ch}"')
    if i < 0 or j < 0:
        sys.exit(f"bridge: chapter {ch} not found")
    k = src.rfind('<section class="panel pp-black prose bridge">', i, j)
    if k < 0:
        sys.exit(f"bridge: no bridge panel in chapter {ch}")
    end = src.find('</section>', k)
    head = '<section class="panel pp-black prose bridge"><p class="comp-title light">🌉 THE BRIDGE</p>'
    return src[:k] + head + inner + src[end:]


def rewrite_bridges(src):
    if SPLICED_MARKER in src:
        note("bridges", 0, "already rewritten")
        return src
    for ch, inner in BRIDGES.items():
        src = set_bridge(src, ch, inner)
    note("bridges", len(BRIDGES), "seven bridges repointed at the chapter that now follows")
    return src


def splice_chapters(src):
    if SPLICED_MARKER in src:
        note("splice", 0, "already spliced")
        return src
    for new_ch in sorted(AFTER_NEW):
        frag = (FRAGS / f"ch{new_ch:02d}.html").read_text(encoding="utf-8").rstrip("\n")
        anchor = f'<i class="ch-end" data-ch="{AFTER_NEW[new_ch]}"></i></div>'
        if src.count(anchor) != 1:
            sys.exit(f"splice: anchor for ch{new_ch} matched {src.count(anchor)} times")
        src = src.replace(anchor, anchor + "\n" + frag, 1)
    note("splice", len(AFTER_NEW), "seven chapter fragments inserted")
    return src


def drawer_rows(src):
    if '"#ch6" data-close' in src:
        note("drawer", 0, "already added")
        return src
    n = 0
    for ch in sorted(NEW_META):
        title, _ = NEW_META[ch]
        row = (f'<a class="dr-row" href="#ch{ch}" data-close>'
               f'<span class="n">{ch:02d}</span>{title}</a>')
        prev = AFTER_NEW[ch]
        anchor = re.search(rf'<a class="dr-row" href="#ch{prev}" data-close>.*?</a>', src)
        if not anchor:
            sys.exit(f"drawer: no row for ch{prev}")
        src = src[:anchor.end()] + row + src[anchor.end():]
        n += 1
    # SET TWO now runs to 26; the ENCORE block must start at 27
    old = ('<a class="dr-row" href="#ch26" data-close><span class="n">26</span>'
           'He Still Has Your Number</a></div>')
    if old not in src:
        # ch26's row landed inside the s3 block because ch25 is the last s2 row
        bad = ('</div><div class="dr-set s3"><p class="dr-set-head">🌅 ENCORE — PROTECT THE MAGIC</p>'
               '<a class="dr-row" href="#ch27"')
        good_row = ('<a class="dr-row" href="#ch26" data-close><span class="n">26</span>'
                    'He Still Has Your Number</a>')
        src = src.replace(good_row + bad.replace('</div>', '', 1), '', 0)  # no-op guard
    note("drawer", n, "seven contents-drawer rows added")
    return src


def setlist_rows(src):
    if '"#ch6"><span class="sl-num">06' in src:
        note("setlist", 0, "already added")
        return src
    n = 0
    for ch in sorted(NEW_META):
        title, sub = NEW_META[ch]
        row = (f'<a class="sl-row live" href="#ch{ch}"><span class="sl-num">{ch:02d}</span>'
               f'<span><span class="sl-t">{title}</span>'
               f'<span class="sl-s">{sub}</span></span>'
               f'<span class="gate-tag go">▶</span></a>')
        prev = AFTER_NEW[ch]
        m = re.search(rf'<a class="sl-row live" href="#ch{prev}">.*?</a>', src)
        if not m:
            sys.exit(f"setlist: no row for ch{prev}")
        src = src[:m.end()] + row + src[m.end():]
        n += 1
    note("setlist", n, "seven setlist rows added")
    return src


def fix_drawer_padding(src):
    """The drawer's chapter numbers are zero-padded two-digit; the generic
    renumber wrote them bare."""
    bad = re.findall(r'<span class="n">(\d)</span>', src)
    if not bad:
        note("drawer-padding", 0, "already padded")
        return src
    src = re.sub(r'<span class="n">(\d)</span>', lambda m: f'<span class="n">0{m.group(1)}</span>', src)
    note("drawer-padding", len(bad), "single-digit drawer numbers re-padded")
    return src


def move_set_boundaries(src):
    """Chapter 6 opens SET TWO, but it was inserted after chapter 5, which is
    the last row of SET ONE -- so in both listings its row landed on the wrong
    side of the seam. Chapter 26 and 31 land correctly by the same logic."""
    moved = 0
    for kind, rowpat in (("dr", r'<a class="dr-row" href="#ch6" data-close>.*?</a>'),
                         ("sl", r'<a class="sl-row live" href="#ch6">.*?</a>')):
        seam = f'</div><div class="{kind}-set s2">'
        m = re.search(rowpat, src)
        if not m:
            sys.exit(f"boundary: no ch6 row in {kind}")
        after = src[m.end():m.end() + len(seam)]
        if after == seam:
            src = src[:m.start()] + seam + m.group(0) + src[m.end() + len(seam):]
            moved += 1
    note("set-boundary", moved, "chapter 6 moved across the SET ONE/SET TWO seam")
    return src


def add_symbols(src):
    if 'id="spec-helpfulone"' in src:
        note("symbols", 0, "already added")
        return src
    out = []
    for ch in sorted(SYMBOL_IDS):
        sid = SYMBOL_IDS[ch]
        a, b = SYMBOL_COLOURS[ch]
        out.append(
            f'<symbol id="{sid}" viewBox="0 0 220 210">'
            f'<circle cx="110" cy="98" r="86" fill="{a}" stroke="#0A0714" stroke-width="6"/>'
            f'<rect x="62" y="58" width="96" height="72" rx="10" fill="#17122B" '
            f'stroke="#0A0714" stroke-width="5"/>'
            f'<path d="M78 84 h64 M78 102 h48" stroke="{b}" stroke-width="9" '
            f'stroke-linecap="round"/>'
            f'<circle cx="150" cy="118" r="11" fill="{b}" stroke="#0A0714" stroke-width="4"/>'
            f'<path d="M40 150 h140 l-14 30 h-112 Z" fill="#0A0714"/>'
            f'<text x="110" y="171" text-anchor="middle" font-family="monospace" '
            f'font-size="13" font-weight="bold" fill="#D8FF3D">SPECIMEN</text></symbol>')
    tail = '</symbol>\n  </defs>\n</svg>'
    if src.count(tail) != 1:
        sys.exit("symbols: defs tail not found exactly once")
    src = src.replace(tail, '</symbol>\n    ' + "\n    ".join(out) + '\n  </defs>\n</svg>', 1)
    note("symbols", len(out), "seven field-tag specimen icons added")
    return src


STEPS_B = [rewrite_bridges, splice_chapters, drawer_rows, setlist_rows,
           fix_drawer_padding, move_set_boundaries, add_symbols]




# ---------------------------------------------------------------- step 3
# Appendices. Guarded individually.

APX_A_BLOCKS = {
    6: ("Chapter 7", [
        ("The Helpful One In The Thread", "reputation manufacture without contact", "The Named Reference Rule"),
        ("The Slide", "platform migration / record elimination", "The Logged-Channel Rule"),
        ("The Eleven-Week Head Start", "pre-loaded trust / safety-rule bypass", "The Hours Audit"),
        ("The Only Person You Know", "arrival isolation engineered as convenience", "The Second Anchor"),
        ("The Profile Read", "disclosure asymmetry", "The Asymmetry Check")]),
    10: ("Chapter 11", [
        ("The Ticket Wage", "compensation in admission", "The Hourly Conversion"),
        ("The Family Payroll", "kinship framing as wage suppression", "The Payroll Question"),
        ("The Uninsured Ladder", "liability laundering through classification", "The Incident Record"),
        ("The Promotion That Isn’t", "title inflation as substitute compensation", "The Title-To-Terms Test"),
        ("The Off-Season Problem", "exit cost denominated in friendships", "The Off-Season Test")]),
    14: ("Chapter 15", [
        ("The Wellness-Threat Sort", "threat perception in four-second triage", "The Medical Words"),
        ("The Credibility Gap", "differential belief and its compounding", "The Corroboration Pre-Load"),
        ("The Advice That Doesn’t Fit", "safety guidance with an unmarked assumption", "The Personal Risk Map"),
        ("The Pre-Loaded Tax", "vigilance as cognitive load", "The Handoff"),
        ("The Only One In The Photo", "visibility without inclusion", "The Affinity Anchor")]),
    17: ("Chapter 18", [
        ("The Consent That Expires", "capacity versus willingness", "The Pre-State Contract"),
        ("The Unverifiable Lineage", "credential laundering through reverence", "The Lineage Check"),
        ("The Cup You Didn’t Measure", "unquantified dosing as practice", "The Dose Disclosure Rule"),
        ("The Sealed Room", "isolation assembled from best practice", "The Daylight Contact"),
        ("The Integration Funnel", "the dual relationship, monetised", "The Separate Integrator")]),
    26: (None, [
        ("The Persistence Frame", "pursuit reframed as devotion", "The One-Time Sentence"),
        ("The Porous Scene", "community openness as a location service", "The Information Diet"),
        ("The Block That Isn’t", "a filter mistaken for a wall", "The Documentation Spine"),
        ("The Next Festival", "public admission and no shared ban list", "The Advance Notice"),
        ("The People Who Vouch", "neutrality as a conduit", "The Camp Instruction")]),
}

APX_A_NOTRACK = {
    20: ("Chapter 21", "No Tracks. Five protocols instead &mdash; The First Hour, The Options "
                       "Clock, Preserve Without Deciding, The Festival Problem, The People "
                       "Around You."),
    31: ("Chapter 32", "No Tracks. Five protocols instead &mdash; The One Conversation, The "
                       "Money, The Check-In That Doesn&rsquo;t Suffocate, What Not To Do, If "
                       "Something Happens. The only chapter addressed to the person staying "
                       "home."),
}


def appendix_a(src):
    if '<h4 class="h4">Chapter 6</h4>' in src:
        note("appendix-A", 0, "already added")
        return src
    n = 0
    for ch in sorted(list(APX_A_BLOCKS) + list(APX_A_NOTRACK)):
        if ch in APX_A_BLOCKS:
            before, rows = APX_A_BLOCKS[ch]
            body = "".join(f"<p>{t} ({anchor}) &rarr; Counter: {cd}</p>" for t, anchor, cd in rows)
        else:
            before, body_text = APX_A_NOTRACK[ch]
            body = f"<p>{body_text}</p>"
        block = f'<h4 class="h4">Chapter {ch}</h4>{body}'
        anchor = (f'<h4 class="h4">{before}</h4>' if before
                  else '<h3 class="h4">ENCORE — PROTECT THE MAGIC</h3>')
        if src.count(anchor) != 1:
            sys.exit(f"appendix A: anchor {anchor!r} matched {src.count(anchor)} times")
        src = src.replace(anchor, block + anchor, 1)
        n += 1
    note("appendix-A", n, "seven chapter blocks added to the Master Track Index")
    return src


APX_B_FIXES = [
    ("Chapters 1 (Oracle), 12 (Oracle), 24 (part of the collective)",
     "Chapters 1 (Oracle), 15 (Oracle), 30 (part of the collective)", "Bear"),
    ("Chapters 21 (Oracle), 21 (Full protagonist — the gate briefing), 24 (part of the collective)",
     "Chapters 21 (Oracle), 27 (Full protagonist — the gate briefing), 30 (part of the collective)",
     "Sister Lou"),
    ("Chapters 4 (Oracle), 13 (Oracle), 18 (Oracle), 22 (Oracle — fourth and final)",
     "Chapters 4 (Oracle), 16 (Oracle), 23 (Oracle), 28 (Oracle — fourth and final)", "Mara"),
    ("Chapters 9 (vendor row witness), 14 (Oracle — no-scuff boots), 15 (Save witness), "
     "17 (Oracle — second appearance), 23 (Oracle), 26 (Oracle — final appearance)",
     "Chapters 9 (vendor row witness), 18 (Oracle — no-scuff boots), 19 (Save witness), "
     "22 (Oracle — second appearance), 29 (Oracle), 33 (Oracle — final appearance)", "Beans"),
    ("Chapters 9 (Oracle), 19 (Oracle), 24 (part of the collective)",
     "Chapters 9 (Oracle), 24 (Oracle), 30 (part of the collective)", "Spool"),
    ("Chapters 5 (Oracle), 6 (minor), 24 (part of the collective)",
     "Chapters 5 (Oracle), 7 (minor), 30 (part of the collective)", "Yo-Yo"),
    ("Chapters 2 (Oracle), 15 (minor reference), 24 (part of the collective)",
     "Chapters 2 (Oracle), 19 (minor reference), 30 (part of the collective)", "Patchbay"),
    ("fifteen years welding shade structures. Chapters 8 (Oracle).",
     "fifteen years welding shade structures. Chapters 8 (Oracle), 10 (Oracle — second appearance).",
     "Wingnut second appearance"),
    ("Zendo-trained peer support volunteer. Chapter 11 (Oracle).",
     "Zendo-trained peer support volunteer. Chapters 11 (Oracle), 14 (Oracle — second appearance).",
     "Patch second appearance"),
    ("current harm-reduction legal clinic. Chapter 12 (Oracle).",
     "current harm-reduction legal clinic. Chapters 12 (Oracle), 26 (Oracle — second appearance).",
     "Hex second appearance"),
]

APX_B_NEW = (
    '<p>Junie “Firewall” Park — Thirty-five. Volunteer moderator: nine years on one regional '
    'festival’s group, four on its Discord. Chapter 6 (Oracle). Her signal: the spreadsheet '
    'she is not supposed to have.</p>'
    '<p>Margarethe “Bell” Ndiaye — Fifty-one. Eleven years facilitating, trained in a '
    'supervised program. Chapter 17 (Oracle). Her signal: the two-page touch policy, sent in '
    'nine minutes.</p>'
    '<p>Perpetua “Pet” Novak — Forty-four. SANE-certified forensic nurse, ninety minutes from '
    'three major festivals, works summer Sundays on purpose. Chapter 20 (Oracle). Her signal: '
    'the laminated card in the badge holder.</p>'
    '<p>Beverly “Bev” Nakashima — Sixty-one. Warehouse parties and desert weekends in the late '
    'eighties; two adult children who go now and both of whom call her. Chapter 31 (Oracle). '
    'Her signal: the question — would they call you?</p>'
)


def appendix_b(src):
    if 'Park — Thirty-five. Volunteer moderator' in src:
        note("appendix-B", 0, "already updated")
        return src
    for old, new, what in APX_B_FIXES:
        src = sub_once(src, old, new, "appendix-B", what)
    anchor = '<p>Mira “Hot Water” — see Mara “Hot Water” Delgado above.</p>'
    src = sub_once(src, anchor, APX_B_NEW + anchor, "appendix-B", "four new cast entries")
    return src


APX_F_NEW = [
    ("The Advance Notice", 26), ("The Affinity Anchor", 14), ("The Asymmetry Check", 6),
    ("The Camp Instruction", 26), ("The Corroboration Pre-Load", 14),
    ("The Daylight Contact", 17), ("The Documentation Spine", 26),
    ("The Dose Disclosure Rule", 17), ("The Handoff", 14), ("The Hourly Conversion", 10),
    ("The Hours Audit", 6), ("The Incident Record", 10), ("The Information Diet", 26),
    ("The Lineage Check", 17), ("The Logged-Channel Rule", 6), ("The Medical Words", 14),
    ("The Named Reference Rule", 6), ("The Off-Season Test", 10),
    ("The One-Time Sentence", 26), ("The Payroll Question", 10),
    ("The Personal Risk Map", 14), ("The Pre-State Contract", 17),
    ("The Second Anchor", 6), ("The Separate Integrator", 17),
    ("The Title-To-Terms Test", 10),
]


def appendix_f(src):
    if "The Named Reference Rule (Ch6)" in src:
        note("appendix-F", 0, "already updated")
        return src
    s = src.find('id="apF"')
    e = src.find('</section>', s)
    seg = src[s:e]
    m = re.search(r'(<p>)(The Amnesty Override.*?)(</p>)', seg, re.S)
    if not m:
        sys.exit("appendix F: entry list not found")
    entries = [x.strip() for x in m.group(2).split("·")]
    entries += [f"{name} (Ch{ch})" for name, ch in APX_F_NEW]

    def key(x):
        t = re.sub(r'<[^>]+>', '', x)
        t = re.sub(r'\s*\(Ch[\d/]+\)\s*$', '', t)
        return re.sub(r'^The\s+', '', t).upper()

    entries = sorted(set(entries), key=key)
    new_seg = seg[:m.start(2)] + " · ".join(entries) + seg[m.end(2):]
    note("appendix-F", len(APX_F_NEW), f"{len(APX_F_NEW)} counter-drops merged alphabetically")
    return src[:s] + new_seg + src[e:]


APX_G_NEW = {
    6: ("Ch7", "Debut: the nineteen-year-old in a Discord who discovers that answering other "
               "people’s questions accurately gets him invited to things. Live: Sundog, "
               "thirty-nine, four hundred and six answered questions and an eleven-week "
               "runway. Greatest Hits: the festival that drives forty thousand ticket buyers "
               "into a group it does not run, staff, or mention in its safety materials."),
    10: ("Ch11", "Debut: the twenty-year-old who trades one six-hour gate shift for a weekend "
                 "pass and is, at that scale, getting an excellent deal. Live: the CORE TEAM "
                 "member at year six, eight hundred hours, a radio and no rate. Greatest Hits: "
                 "the production budget where three hundred volunteers and forty contractors do "
                 "the same eighty percent of the work."),
    14: ("Ch15", "Debut: the twenty-year-old handed a radio and nine minutes of training who "
                 "learns in one weekend which people you check on and which you call in about. "
                 "Live: the shift lead at year eight making the four-second call two hundred "
                 "times a weekend. Greatest Hits: the aftermovie cut for diversity playing above "
                 "an org chart that was never counted."),
    17: ("Ch18", "Debut: the twenty-six-year-old sitting four friends in his living room with a "
                 "batch he bought from someone at a retreat. Live: Amaru — twelve unverifiable "
                 "years, twenty-two participants at four hundred each, a basket of phones and a "
                 "calendar link at the door. Greatest Hits: an entire industry administering "
                 "powerful compounds to strangers with no board, no registry and no revocable "
                 "credential anywhere in it."),
    20: ("Ch21", "Debut: the twenty-two-year-old friend who wakes the camp, asks what she took, "
                 "goes looking for him, and posts by eleven — every action taken out of love, "
                 "every one of them closing a door. Live: the event at year fifteen, with a "
                 "reporting address and an incident form that preserves nothing and starts no "
                 "clock. Greatest Hits: fifty years of prevention literature and almost nothing "
                 "written for twenty to six in the morning."),
    26: ("Ch27", "Debut: twenty-two, first real rejection, three messages and one additional "
                 "account made sincerely to say he would stop. Live: Marek, thirty-six — eleven "
                 "weeks, four messages, one ticket to an event he was going to anyway, and the "
                 "location of a flag by the second gate that forty people told him for free. "
                 "Greatest Hits: an industry with no shared ban list between any two events, "
                 "ever."),
    31: ("Ch32", "Debut: the parent of a nineteen-year-old who forbids it, hears nothing all "
                 "weekend, and mistakes the silence for safety. Live: year six — reasonable now, "
                 "still running the Monday audit, and once, in 2023, changed the subject about a "
                 "test kit for four seconds. Greatest Hits: thirty years of abstinence messaging, "
                 "news coverage that exists only when somebody dies, and a ticketing industry "
                 "that publishes nothing at all for the several hundred thousand households "
                 "sitting up on a Saturday night."),
}


def appendix_g(src):
    if '<strong class="lead">Ch6:</strong>' in src:
        note("appendix-G", 0, "already updated")
        return src
    n = 0
    for ch in sorted(APX_G_NEW):
        before, body = APX_G_NEW[ch]
        entry = f'<p><strong class="lead">Ch{ch}:</strong> {body}</p>'
        anchor = f'<p><strong class="lead">{before}:</strong>'
        if src.count(anchor) != 1:
            sys.exit(f"appendix G: anchor {anchor!r} matched {src.count(anchor)} times")
        src = src.replace(anchor, entry + anchor, 1)
        n += 1
    note("appendix-G", n, "seven Discog entries added")
    return src


def content_disclosure(src):
    if "Chapter 20:</strong> The aftermath" in src:
        note("disclosure", 0, "already added")
        return src
    anchor = ('<p><strong class="lead">Chapter 23:</strong> Detailed depiction of a coercive '
              'control environment')
    entry = ('<p><strong class="lead">Chapter 20:</strong> The aftermath of sexual assault at a '
             'festival, and what is medically and practically available in the hours that follow. '
             'It contains no depiction of an assault — it opens the morning after — and it carries '
             'its own note at the top, including where to skip to if you need it right now.</p>')
    if src.count(anchor) != 1:
        sys.exit(f"disclosure: anchor matched {src.count(anchor)} times")
    src = src.replace(anchor, entry + anchor, 1)
    note("disclosure", 1, "content disclosure entry added for chapter 20")
    return src


STEPS_C = [appendix_a, appendix_b, appendix_f, appendix_g, content_disclosure]


def main():
    global ALREADY
    src = WOOK.read_text(encoding="utf-8")
    ALREADY = DONE_MARKER in src
    before = len(src)
    for step in STEPS_A + STEPS_B + STEPS_C:
        src = step(src)
    src = src.replace(PROT, "")
    WOOK.write_text(src, encoding="utf-8")
    width = max(len(s) for s, _, _ in log) if log else 0
    for step, n, what in log:
        print(f"  {step:<{width}}  {n:>4}  {what}")
    print(f"\n{before:,} -> {len(src):,} bytes")


if __name__ == "__main__":
    main()

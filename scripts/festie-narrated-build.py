#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the narrated teleprompter series: one intro episode and one closing
episode per guide, plus every scenario rewritten as flowing, full-sentence
narration instead of the site's labeled-field format -- matching the
A.C.C.E.S.S. example the user hand-wrote as the template for this pass.

This is a from-scratch narration layer, not a trim of the existing
combined/posts scripts. Same house rule as every other teleprompter builder
in this project: the underlying content (who/scene/tells/happening/check/
dark/move/say/truth) is never invented or embellished with claims that
aren't already in the book's own data -- what changes here is *form*: bullet
labels become connected prose, and every paragraph gets a rotating
rhetorical lead-in ("So here's what to watch for," "Now here's the
mechanism," "So run this check," "Here's exactly what to say," "And here's
the truth") matching the template's own rhythm.

Rotation is deterministic (scenario global index mod N), never random, so a
re-run is stable. Per-guide intro/closing episodes are generated from the
guide's own checks/outline/sentences fields, not hand-authored per guide --
the ONE hand-authored file is 00-SERIES-INTRO.md, which this script does not
touch or regenerate.

Source of truth: content/festie-bible-data.json. Run after any content
change so these stay in sync with the live book.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "content/festie-bible-data.json"
OUT_DIR = ROOT / "content/festie-teleprompter-narrated"
SITE_URL = "noblefathercreations.com/festival"
WPM = 150

SECTION_TITLES = {
    "CAPTURE": "how access and trust get established",
    "CONDITION": "how the situation gets shaped once you're already in it",
    "CONTROL": "how leverage gets held and used",
    "TOOLS": "the practical scripts and tools that actually work",
    "COMMUNITY": "how to tell real community from the counterfeit version",
    "ACCOUNTABILITY": "what you owe when the power is yours",
    "EMERGENCY": "what to do when it's already happening",
    "SUPPORT": "holding the line for yourself and for each other",
    "RESPONSIBILITY": "what you owe the people around you",
    "STANDARDS": "what you actually own, and what you owe",
    "LEGACY": "the toolkit that outlasts one event",
    "PROTECTION": "what real leadership actually looks like",
    "HYDRATION": "the physical infrastructure that holds you up",
    "SUBSTANCES": "testing, combinations, and the trouble between them",
    "SEE SOMETHING": "reading the room and knowing when to step in",
    "MENTAL HEALTH": "crises, and what actually helps",
    "COMMUNITY CARE": "looking out past your own camp",
}

LETTER_RE = re.compile(r'["“]([A-Z])["”]\s*CHECK')
QUESTION_RE = re.compile(r'CHECK:\s*["“](.+?)["”]\s*(.*)$', re.S)
LEAD_DASH_RE = re.compile(r'^[—-]\s*')
SLUG_RE = re.compile(r"[^a-z0-9]+")
CONTRACTION_RE = re.compile(r"'(S|Re|T|Ll|D|Ve|M)\b")

ORDINALS = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth"]


def slugify(s):
    return SLUG_RE.sub("-", s.lower()).strip("-")[:60]


ACRONYM_FIX_RE = re.compile(r"\b(Lgbtq\+?|Bipoc)\b", re.I)
ACRONYM_FIX = {"lgbtq": "LGBTQ", "lgbtq+": "LGBTQ+", "bipoc": "BIPOC"}


def titlecase(s):
    t = CONTRACTION_RE.sub(lambda m: "'" + m.group(1).lower(), s.title())
    return ACRONYM_FIX_RE.sub(lambda m: ACRONYM_FIX[m.group(1).lower()], t)


def role_no_article(role):
    """Title-case an all-caps role label with any leading article stripped,
    for use right after a caller-supplied 'the' (e.g. 'the {role} Edition').
    One role -- 'THE PEOPLE AT HOME' -- already carries its own, and without
    this it doubles up: 'the The People At Home Edition'."""
    t = titlecase(role)
    if t.lower().startswith("the "):
        t = t[4:]
    return t


def split_check(raw):
    raw = raw.strip()
    lm = LETTER_RE.search(raw)
    letter = lm.group(1) if lm else None
    qm = QUESTION_RE.search(raw)
    if qm:
        q = qm.group(1).strip()
        rest = LEAD_DASH_RE.sub("", qm.group(2).strip())
        return letter, q, rest
    m2 = re.search(r'CHECK:\s*["“]?(.+)$', raw, re.S)
    return letter, (m2.group(1) if m2 else raw).strip(), ""


def sentence(s):
    """Ensure a fragment reads as a complete sentence: capitalized, and
    closed with terminal punctuation if it doesn't already have one."""
    s = s.strip()
    if not s:
        return s
    s = s[0].upper() + s[1:]
    if s[-1] not in ".!?”’":
        s += "."
    return s


def fmt_time(words):
    secs = round(words / WPM * 60)
    m, s = divmod(secs, 60)
    return f"{m}:{s:02d}"


def wc(*parts):
    text = " ".join(p for p in parts if p)
    text = re.sub(r'^[-•#>].*$', '', text, flags=re.M)
    return len(text.split())


# ---------------------------------------------------------------------
# rotating rhetorical lead-ins, one family per paragraph role, matching
# the template's own vocabulary. Picked by scenario global index mod N.
# ---------------------------------------------------------------------
LEAD = {
    "who": [
        "Let me tell you about {who_ref}.",
        "Let's talk about {who_ref}.",
        "Here's {who_ref}.",
    ],
    "scene": [
        "Here's how it plays out.",
        "Here's the scene.",
        "Picture it.",
    ],
    "tells": [
        "So here's what to watch for.",
        "So watch for these.",
        "Here are the signs.",
    ],
    "mechanism": [
        "Now here's what's really going on.",
        "Here's the mechanism underneath it.",
        "Now here's what's really happening.",
    ],
    "check": [
        "So run this check.",
        "So ask yourself this.",
        "So here's your check.",
    ],
    "dark": [
        "And here's the darker reality.",
        "Now here's the part that's hard to hear.",
        "And here's what sits underneath all of it.",
    ],
    "move": [
        "So here's the play.",
        "So here's what you do.",
        "So here's your move.",
    ],
    "say": [
        "Here's exactly what to say.",
        "Here's what to say, out loud.",
        "Here are the words.",
    ],
    "truth": [
        "And here's the truth.",
        "And remember this.",
        "And here's the truth underneath it.",
    ],
}


def lead(role, i):
    return LEAD[role][i % len(LEAD[role])]


def who_ref(sc, i):
    """A short noun phrase standing in for 'the person', varied so 270
    scenarios in a row don't all open on the same words."""
    options = ["a particular kind of person", "the person you'll meet here",
               "someone you'll recognize", "a specific type"]
    return options[i % len(options)]


# ---------------------------------------------------------------------
# per-scenario narration
# ---------------------------------------------------------------------
def keyword(name):
    """One-word distillation of a check name for the framework recap line
    ('Gut Check' -> 'Gut', 'Exit Is Mine' -> 'Exit'). Keeps internal
    apostrophes (e.g. "Don't Assume Safe Spaces" -> "Don't", not "Dont")."""
    first = re.sub(r"[^A-Za-z']", '', name.split()[0]).strip("'")
    return first


def render_say(say):
    """47 of 270 'say' fields already arrive self-quoted -- either a
    bracketed stage direction ('[To your tour manager]: "I need you to..."')
    or the whole line already wrapped in its own straight quotes. Wrapping
    those in another layer of curly quotes stacks quote glyphs right next
    to each other ('“"I need...'). Every one of those 47 starts with '[' or
    '\"' (checked against the full dataset), so that's the signal to leave
    it alone; anything else gets the normal outer curly-quote wrap."""
    s = say.strip()
    if s.startswith("[") or s.startswith('"'):
        return s
    return f"“{say}”"


def scenario_script(g, sc, n, total, gi):
    lines = []
    hook_title = titlecase(sc["hook"])
    lines.append(f"SCENARIO {n} — “{hook_title}”")
    lines.append("\U0001F3AC TELEPROMPTER SCRIPT")
    lines.append("")

    # who
    who_line = lead('who', gi).format(who_ref=who_ref(sc, gi))
    lines.append(f"{who_line} {sc['who']}")
    lines.append("")

    # scene
    lines.append(f"{lead('scene', gi)} {sc['scene']}")
    lines.append("")

    # tells -> flowing sentences, not bullets
    tells_prose = " ".join(sentence(t) for t in sc["tells"])
    lines.append(f"{lead('tells', gi)} {tells_prose}")
    lines.append("")

    # mechanism
    lines.append(f"{lead('mechanism', gi)} {sc['happening']}")
    lines.append("")

    # check
    letter, q, rest = split_check(sc["check"])
    check_line = f"I call it the {letter} check. Ask: “{q}”" if letter else f"Ask: “{q}”"
    if rest:
        check_line += f" — {rest}"
    lines.append(f"{lead('check', gi)} {check_line}")
    lines.append("")

    # dark (optional)
    if sc.get("dark") and sc.get("darkTitle"):
        lines.append(f"{lead('dark', gi)} {sc['darkTitle']}. {sc['dark']}")
        lines.append("")

    # move
    lines.append(f"{lead('move', gi)} {sc['move']}")
    lines.append("")

    # say
    lines.append(f"{lead('say', gi)} {render_say(sc['say'])}")
    lines.append("")

    # truth
    lines.append(f"{lead('truth', gi)} {sc['truth']}")
    lines.append("")

    body = "\n".join(lines)
    words = wc(body)
    header = (f"<!-- {g['acronym']} scenario {n}/{total} — “{hook_title}” "
              f"— ~{words} spoken words — est. {fmt_time(words)} at {WPM}wpm -->\n")
    return header + body, words


# ---------------------------------------------------------------------
# per-guide intro episode
# ---------------------------------------------------------------------
def ordinal_for_letter(checks, idx):
    """'first C' / 'second C' / 'last S' -- matches the letter's own
    repeat-count within this guide's framework, English Angel-voice."""
    letter = checks[idx]["letter"]
    same = [c["letter"] for c in checks]
    positions = [i for i, l in enumerate(same) if l == letter]
    pos = positions.index(idx)
    if len(positions) == 1:
        return None
    if pos == len(positions) - 1:
        return "last"
    return ORDINALS[pos] if pos < len(ORDINALS) else f"{pos + 1}th"


def intro_episode(g):
    n_checks = len(g["checks"])
    n_scenarios = len(g["scenarios"])
    lines = []
    lines.append(f"{g['acronym']} — INTRO EPISODE")
    lines.append(f"\U0001F3AC TELEPROMPTER SCRIPT — “Welcome to {g['acronym']}”")
    lines.append("")
    lines.append("Before we get into it, let me tell you where you are and what you're holding.")
    lines.append("")
    lines.append(
        "This is one of twenty-one guides in the festival series, and every single "
        f"one of them lives for free over at {SITE_URL}. No login, no paywall — you "
        "just go and read the one that's yours. Between all twenty-one of them, there "
        "are two hundred and seventy scenarios, each one built from real patterns in "
        "the festival world, not invented for effect."
    )
    lines.append("")
    lines.append(
        f"This guide is the one called {g['acronym']} — the {role_no_article(g['role'])} Edition. "
        f"And it exists for a specific reason. {g['intro']}"
    )
    lines.append("")
    lines.append(
        f"So let me walk you through what {g['acronym']} stands for, because these "
        f"{n_checks} ideas are the frame that everything else in this guide runs on."
    )
    lines.append("")
    for i, c in enumerate(g["checks"]):
        ordn = ordinal_for_letter(g["checks"], i)
        if ordn:
            lead_phrase = f"The {ordn} {c['letter']} stands for"
        else:
            lead_phrase = f"The letter {c['letter']} stands for"
        lines.append(f"{lead_phrase} “{titlecase(c['name'])}.” {c['desc']}")
        lines.append("")

    keywords = " ".join(f"{keyword(c['name'])}." for c in g["checks"])
    lines.append(
        f"That's the framework. {keywords} {n_checks} ideas, and they hold this "
        "whole thing together."
    )
    lines.append("")

    outline_bits = [SECTION_TITLES.get(o["key"], o["desc"].lower()) for o in g["outline"]]
    if len(outline_bits) > 1:
        outline_prose = ", ".join(outline_bits[:-1]) + ", and finally " + outline_bits[-1]
    else:
        outline_prose = outline_bits[0] if outline_bits else "what this guide covers"
    lines.append(
        f"Now, coming up after this, there are {n_scenarios} scenarios in this guide "
        "— and each one is its own short video. We'll move through "
        f"{outline_prose}."
    )
    lines.append("")
    lines.append("So that's where you are, and that's what's ahead. Let's get into it.")
    lines.append("")

    body = "\n".join(lines)
    words = wc(body)
    header = f"<!-- {g['acronym']} intro episode — ~{words} spoken words — est. {fmt_time(words)} at {WPM}wpm -->\n"
    return header + body, words


# ---------------------------------------------------------------------
# per-guide closing episode
# ---------------------------------------------------------------------
def check_recap(desc):
    """First full sentence of a check's desc, for the closing episode's
    rapid-fire recap line. Most descs are statements, not questions, so this
    keeps the recap grammatical rather than forcing a broken interrogative
    ('is your accommodations are not gifts?') -- if the desc already
    contains a real question, use that verbatim instead.

    Finds the first true sentence-terminator (., !, or ?) rather than
    naively splitting on '.', so a desc that opens with a quoted,
    punctuated aside (e.g. 'Not "with the camp". A named adult...', where
    the closing quote mark sits *before* the period) keeps its own
    terminal punctuation instead of losing it to the split -- a bare
    split(".") would cut right after the quote mark and leave a fragment
    that looks already-terminated to sentence() but isn't."""
    m = re.search(r'([^.?!]*\?)', desc)
    if m:
        return m.group(1).strip()
    end = re.search(r'[.!?]', desc)
    first_clause = desc[:end.end()].strip() if end else desc.strip()
    dash_idx = first_clause.find(" — ")
    if dash_idx != -1:
        first_clause = sentence(first_clause[:dash_idx])
    return first_clause


def closing_episode(g, remaining_total):
    n = len(g["scenarios"])
    lines = []
    lines.append(f"{g['acronym']} — CLOSING EPISODE")
    lines.append(f"\U0001F3AC TELEPROMPTER SCRIPT — “What {g['acronym']} Leaves You With”")
    lines.append("")
    lines.append(
        f"So that's the whole guide. {n} scenarios, and a framework that holds them "
        "all together. Before you go, let me pull it back into one piece — because "
        "the individual scenarios matter, but the shape underneath them matters more."
    )
    lines.append("")
    lines.append(
        f"Here's the thing running through every scenario in this guide. Every one of "
        f"them counts on you not having run the {g['acronym']} checks before it "
        "mattered. Not on you being careless — on you being tired, or flattered, or "
        "already three days in. That's not a coincidence. That's the design. And it's "
        "also the good news, because it tells you exactly where to stand: decide the "
        "checks while you're rested, and let the tired version of you just run them."
    )
    lines.append("")
    if g.get("sentences"):
        vows = " ".join(sentence(s) for s in g["sentences"])
        lines.append(f"Carry this forward. {vows}")
        lines.append("")
    lines.append(
        f"And let me leave you with the {len(g['checks'])} checks, because if you "
        "remember nothing else, remember these."
    )
    lines.append("")
    recap_bits = []
    for c in g["checks"]:
        recap_bits.append(f"{keyword(c['name'])} — {check_recap(c['desc'])}")
    lines.append(" ".join(recap_bits))
    lines.append("")
    lines.append(
        f"Here's the last truth, and it's the one this whole guide is really about. "
        f"You belong here, completely, and this guide never asked you to doubt that. "
        "It asked you to make it real for you, specifically, on the ground, at hour "
        "twenty. That's the whole job."
    )
    lines.append("")
    lines.append(
        f"Every one of these scenarios, and {remaining_total} more across the other "
        f"twenty guides, lives free at {SITE_URL}. Go read the one that's yours. Take "
        "one person with you. And I'll see you in the next section."
    )
    lines.append("")

    body = "\n".join(lines)
    words = wc(body)
    header = f"<!-- {g['acronym']} closing episode — ~{words} spoken words — est. {fmt_time(words)} at {WPM}wpm -->\n"
    return header + body, words


def main():
    only = set(sys.argv[1:]) if len(sys.argv) > 1 else None
    d = json.loads(DATA.read_text(encoding="utf-8"))
    guides = d["guides"]
    total_scenarios = sum(len(g["scenarios"]) for g in guides)

    if only:
        guides = [g for g in guides if g["slug"] in only]
        if not guides:
            raise SystemExit(f"no guide matches {only}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest = []
    gi_counter = 0  # global scenario index, for deterministic lead-in rotation

    for g in guides:
        gdir = OUT_DIR / g["slug"]
        gdir.mkdir(parents=True, exist_ok=True)

        intro_body, intro_words = intro_episode(g)
        (gdir / "00-intro.md").write_text(intro_body, encoding="utf-8")

        scenario_words = 0
        for n, sc in enumerate(g["scenarios"], start=1):
            body, words = scenario_script(g, sc, n, len(g["scenarios"]), gi_counter)
            fname = f"{n:02d}-{slugify(sc['hook'])}.md"
            (gdir / fname).write_text(body, encoding="utf-8")
            scenario_words += words
            gi_counter += 1

        closing_body, closing_words = closing_episode(g, total_scenarios - len(g["scenarios"]))
        (gdir / "99-closing.md").write_text(closing_body, encoding="utf-8")

        total_words = intro_words + scenario_words + closing_words
        manifest.append((g["acronym"], g["role"], len(g["scenarios"]), total_words, g["slug"]))
        print(f"  {g['acronym']:14} {len(g['scenarios']):3} scenarios + intro + closing  "
              f"~{total_words:7,} words -> {g['slug']}/")

    if not only or len(guides) == 21:
        idx = [
            "# The Festie Bible — Narrated Teleprompter Series", "",
            "One intro episode, one closing episode, and one flowing-narration script "
            "per scenario, for all twenty-one guides. Start with `00-SERIES-INTRO.md`, "
            "then each guide's own `00-intro.md`, then its numbered scenarios in order, "
            "then `99-closing.md`.", "",
            f"Live and updated at **{SITE_URL}**.", "",
            "| Guide | Audience | Scenarios | ~Words (intro+scenarios+closing) | Folder |",
            "|---|---|---:|---:|---|",
        ]
        for acr, role, n, words, slug in manifest:
            idx.append(f"| {acr} | {titlecase(role)} | {n} | {words:,} | `{slug}/` |")
        idx.append("")
        (OUT_DIR / "00-INDEX.md").write_text("\n".join(idx), encoding="utf-8")

    print(f"\n{len(manifest)} guide(s) processed -> {OUT_DIR}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())

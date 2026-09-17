#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate teleprompter-ready spoken-word scripts from the Festie Bible data.

One markdown file per guide (21 total), each holding every scenario in that
guide rewritten as continuous read-aloud narration. The rule this follows:
change as few words as possible from the actual scenario text. What gets
added is connective tissue only -- a lead-in phrase before each field ("Here's
the scene.", "Run the check.") so the fields read as one flowing piece instead
of a labeled data card. The who/scene/tells/happening/check/dark/move/say/
truth content itself is the book's own text, verbatim.

Source of truth: content/festie-bible-data.json (never hand-edit the output).
Run after any content change to the data so the scripts stay in sync.
"""
import json
import re
import sys
from pathlib import Path

DATA = "content/festie-bible-data.json"
OUT_DIR = Path("content/festie-teleprompter")
SITE_URL = "www.noblefathercreations.com/festival"

SECTION_TITLES = {
    "CAPTURE": "Capture — how access and trust get established",
    "CONDITION": "Condition — how the situation gets shaped once you're in it",
    "CONTROL": "Control — how leverage is held and used",
    "TOOLS": "Tools — practical structures, scripts and kit",
    "COMMUNITY": "Community — the real version versus the counterfeit",
    "ACCOUNTABILITY": "Accountability — what you owe when the power is yours",
    "EMERGENCY": "Emergency — what to do when it's already happening",
    "SUPPORT": "Support — holding the line for yourself and others",
    "RESPONSIBILITY": "Responsibility — what you owe the people around you",
    "STANDARDS": "Standards — what you actually own and owe",
    "LEGACY": "Legacy — the toolkit that outlasts one event",
    "PROTECTION": "Protection — what real leadership looks like",
    "HYDRATION": "Hydration — the physical infrastructure",
    "SUBSTANCES": "Substances — testing, combinations, and trouble",
    "SEE SOMETHING": "See Something — reading the room and stepping in",
    "MENTAL HEALTH": "Mental Health — crises and what actually helps",
    "COMMUNITY CARE": "Community Care — looking out past your own camp",
}

# Rotating lead-ins so 270 scripts in a row don't all sound identical. Picked
# deterministically per scenario (global index mod 3), not randomly, so a
# re-run always produces the same script.
LEADS = {
    "who": ["Here's who you're dealing with.", "Here's who this is.", "Let's talk about who does this."],
    "scene": ["Here's the scene.", "Picture this.", "Here's how it plays out."],
    "tells": ["Here's what to watch for.", "Here are the signs.", "Watch for these."],
    "happening": ["Here's what's actually happening.", "Here's the mechanism underneath it.", "Here's what's really going on."],
    "check": ["Run the check.", "Here's your check.", "Ask yourself this."],
    "dark": ["Here's the dark reality.", "Here's the part that's hard to hear.", "Here's what's underneath all of it."],
    "move": ["Here's your move.", "Here's what you do.", "Here's the play."],
    "say": ["Here's exactly what to say.", "Say this, out loud.", "Here are the words."],
    "truth": ["And here's the truth.", "Here's the truth underneath it.", "Remember this."],
}

LETTER_RE = re.compile(r'["“]([A-Z])["”]\s*CHECK')
QUESTION_RE = re.compile(r'CHECK:\s*["“](.+?)["”]\s*(.*)$', re.S)
LEAD_DASH_RE = re.compile(r'^[—-]\s*')
ACRONYM_RE = re.compile(r'^[A-Z0-9]+$')


def lead(field, i):
    return LEADS[field][i % 3]


def split_check(raw):
    """Pull the letter, the question, and the trailing explanation out of a
    check line. The source data has two shapes -- '"Q?" — rest' and '"Q?"
    Rest' with no dash at all -- and both curly and straight quotes, so this
    matches loosely rather than assuming one exact pattern.

    A meaningful share of the original book's check fields (52 of the 149
    scenarios that predate this project's own writing) are truncated
    mid-sentence with no closing quote at all -- a pre-existing content
    defect, not something to paper over by inventing an ending. Where that
    happens this returns closed=False and the caller leaves the quote open
    rather than fabricating a close."""
    raw = raw.strip()
    lm = LETTER_RE.search(raw)
    letter = lm.group(1) if lm else None
    qm = QUESTION_RE.search(raw)
    if qm:
        q = qm.group(1).strip()
        rest = LEAD_DASH_RE.sub("", qm.group(2).strip())
        return letter, q, rest, True
    m2 = re.search(r'CHECK:\s*["“]?(.+)$', raw, re.S)
    q = (m2.group(1) if m2 else raw).strip()
    return letter, q, "", False


def soft_lower(s):
    """Lowercase for mid-sentence use, but leave real acronyms (BITE, IP,
    MDMA...) alone rather than turning them into lowercase mush."""
    out = []
    for tok in re.split(r'(\s+)', s):
        core = re.sub(r'[^A-Za-z]', '', tok)
        if ACRONYM_RE.match(core) and len(core) >= 2:
            out.append(tok)
        else:
            out.append(tok.lower())
    return "".join(out)


def scenario_script(sc, i):
    lines = []
    lines.append(f"### {i}. “{sc['hook']}”")
    lines.append(f"*{sc['archetype']} — clinically, {soft_lower(sc['clinical'])}.*")
    lines.append("")
    lines.append(f"{lead('who', i)} {sc['who']}")
    lines.append("")
    lines.append(f"{lead('scene', i)} {sc['scene']}")
    lines.append("")
    lines.append(lead('tells', i))
    lines.append("")
    for t in sc["tells"]:
        lines.append(f"- {t}")
    lines.append("")
    lines.append(f"{lead('happening', i)} {sc['happening']}")
    lines.append("")
    letter, q, rest, closed = split_check(sc["check"])
    close_mark = "”" if closed else ""
    if letter:
        check_line = f"{lead('check', i)} The {letter} check: “{q}{close_mark}"
    else:
        check_line = f"{lead('check', i)} “{q}{close_mark}"
    if rest:
        check_line += f" — {rest}"
    lines.append(check_line)
    lines.append("")
    if sc.get("dark") and sc.get("darkTitle"):
        lines.append(f"{lead('dark', i)} {sc['darkTitle']}. {sc['dark']}")
        lines.append("")
    lines.append(f"{lead('move', i)} {sc['move']}")
    lines.append("")
    lines.append(f"{lead('say', i)} “{sc['say']}”")
    lines.append("")
    lines.append(f"{lead('truth', i)} {sc['truth']}")
    lines.append("")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def guide_doc(g, total_scenarios):
    n = len(g["scenarios"])
    others = total_scenarios - n
    lines = []
    lines.append(f"# {g['acronym']} — {g['role']}")
    lines.append(f"### {g['edition']}")
    lines.append("")
    lines.append("*A spoken-word teleprompter script — one scenario at a time, ready to read straight to camera.*")
    lines.append("")
    lines.append(f"**Quick shoutout before we start:** every scenario in this guide — and {others} more across the other twenty guides — lives free at **{SITE_URL}**.")
    lines.append("")
    lines.append(f"This is {g['acronym']}: {g['edition']}. {g['intro']}")
    lines.append("")
    lines.append("Here's the framework this whole guide runs on.")
    lines.append("")
    for c in g["checks"]:
        name = c["name"].rstrip()
        sep = "" if name[-1] in "?!." else "."
        lines.append(f"- **{c['letter']}** — {name}{sep} {c['desc']}")
    lines.append("")
    lines.append("Let's get into it.")
    lines.append("")
    lines.append("---")
    lines.append("")

    # group scenarios by section, preserving the guide's own outline order
    by_section = {}
    for sc in g["scenarios"]:
        by_section.setdefault(sc["section"], []).append(sc)
    order = [o["key"] for o in g["outline"] if o["key"] in by_section]
    for key in by_section:
        if key not in order:
            order.append(key)

    idx = 1
    for key in order:
        title = SECTION_TITLES.get(key, key.title())
        lines.append(f"## {title}")
        lines.append("")
        desc = next((o["desc"] for o in g["outline"] if o["key"] == key), None)
        if desc:
            lines.append(f"*{desc}.*")
            lines.append("")
        for sc in by_section[key]:
            lines.append(scenario_script(sc, idx))
            idx += 1

    lines.append(f"## That's every scenario in {g['acronym']}")
    lines.append("")
    lines.append(f"You've just read all {n} of them — built from real patterns in the festival world, not invented for effect.")
    lines.append("")
    lines.append("Before you go, here's what this guide asks you to carry:")
    lines.append("")
    for s in g["sentences"]:
        lines.append(f"- {s}")
    lines.append("")
    lines.append(f"All twenty-one guides. Two hundred and seventy scenarios. Free, no login, no paywall, at **{SITE_URL}**.")
    lines.append("")
    lines.append("Read the one that's yours. Or read them all.")
    lines.append("")
    return "\n".join(lines)


def main():
    d = json.load(open(DATA, encoding="utf-8"))
    total = sum(len(g["scenarios"]) for g in d["guides"])
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    index_rows = []
    for g in d["guides"]:
        doc = guide_doc(g, total)
        path = OUT_DIR / f"{g['slug']}.md"
        path.write_text(doc, encoding="utf-8")
        words = len(doc.split())
        index_rows.append((g["acronym"], g["role"], len(g["scenarios"]), words, path.name))
        print(f"  {g['acronym']:14} {len(g['scenarios']):3} scenarios  ~{words:6,} words -> {path}")

    idx_lines = [
        "# The Festie Bible — Teleprompter Scripts",
        "",
        f"Spoken-word, copy-paste-ready narration for all {total} scenarios across all {len(d['guides'])} guides.",
        f"Read live and updated at **{SITE_URL}**.",
        "",
        "| Guide | Audience | Scenarios | ~Words | File |",
        "|---|---|---:|---:|---|",
    ]
    for acr, role, n, w, fname in index_rows:
        idx_lines.append(f"| {acr} | {role} | {n} | {w:,} | `{fname}` |")
    idx_lines.append("")
    (OUT_DIR / "00-INDEX.md").write_text("\n".join(idx_lines), encoding="utf-8")
    print(f"\n{len(index_rows)} guide scripts written to {OUT_DIR}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())

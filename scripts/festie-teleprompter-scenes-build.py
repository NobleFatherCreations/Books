#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate one individually-postable teleprompter script per scenario.

270 files, one per scenario, meant to be loaded to social media one at a
time -- unlike scripts/festie-teleprompter-build.py's 21 combined per-guide
files (still generated separately, good for a full read-through), these
carry no guide-wide framework or affirmations repeated 8-21 times over.
Each is a self-contained unit: a short VIDEO INTRO block (spoken line +
on-screen text cue naming the guide, section and this scenario) followed by
the scenario itself in the same flowing narration style, then the shoutout.

Same rule as the combined build: change as few words from the actual
scenario text as possible. What's trimmed here versus the combined file is
framing overhead (the guide's full check-framework, its affirmations list),
not scenario content -- the who/scene/tells/happening/check/dark/move/say/
truth text is never shortened to hit a time target. An honest estimated
read time is printed on every file instead, at a stated words-per-minute
assumption, so nothing is silently forced under 3 minutes.

Source of truth: content/festie-bible-data.json. Run after any content
change (including scripts/festie-repair-truncated-checks.py) so scripts
stay in sync.
"""
import json
import re
import sys
from pathlib import Path

DATA = "content/festie-bible-data.json"
OUT_DIR = Path("content/festie-teleprompter/posts")
SITE_URL = "www.noblefathercreations.com/festival"
WPM = 150  # stated assumption -- natural teleprompter pace, not a maximum

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

LETTER_RE = re.compile(r'["“]([A-Z])["”]\s*CHECK')
QUESTION_RE = re.compile(r'CHECK:\s*["“](.+?)["”]\s*(.*)$', re.S)
LEAD_DASH_RE = re.compile(r'^[—-]\s*')
ACRONYM_RE = re.compile(r'^[A-Z0-9]+$')
SLUG_RE = re.compile(r"[^a-z0-9]+")


def slugify(s):
    return SLUG_RE.sub("-", s.lower()).strip("-")[:60]


CONTRACTION_RE = re.compile(r"'(S|Re|T|Ll|D|Ve|M)\b")


def titlecase(s):
    """str.title() capitalizes after every apostrophe (You'Re, Doesn'T).
    This fixes the contraction tail back down."""
    return CONTRACTION_RE.sub(lambda m: "'" + m.group(1).lower(), s.title())


def split_check(raw):
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
    out = []
    for tok in re.split(r'(\s+)', s):
        core = re.sub(r'[^A-Za-z]', '', tok)
        if ACRONYM_RE.match(core) and len(core) >= 2:
            out.append(tok)
        else:
            out.append(tok.lower())
    return "".join(out)


def fmt_time(words):
    secs = round(words / WPM * 60)
    m, s = divmod(secs, 60)
    return f"{m}:{s:02d}"


def img_marker(path, note):
    return f"> 🖼️ **[INSERT IMAGE HERE: `{path}`]** — {note}"


def spoken_word_count(*parts):
    """Word count of what a presenter actually says out loud -- excludes
    markdown metadata (Guide:/Section:/Accent color: labels, the on-screen
    text suggestion, headers, bullet dashes, image-insert callouts) that a
    reader sees but never voices. Used for the runtime estimate so it isn't
    inflated by the file's own formatting."""
    text = " ".join(parts)
    text = re.sub(r'^[-•]\s*', '', text, flags=re.M)
    text = re.sub(r'^>.*$', '', text, flags=re.M)
    return len(text.split())


def scenario_body(sc, slug):
    """The scenario narration, same flowing shape as the combined build but
    with single fixed lead-ins (no rotation needed -- one scenario per
    file, so there's no repetition to break up)."""
    lines = []
    lines.append(f"Here's who you're dealing with. {sc['who']}")
    lines.append("")
    lines.append(f"Here's the scene. {sc['scene']}")
    lines.append("")
    lines.append(img_marker(f"images/{slug}/tells-card.png",
                             "hold this on screen with this scenario's tells typed in; you can "
                             "shorten the next line to \"Here's what to watch for\" instead of "
                             "narrating every tell if you want this under 3 minutes."))
    lines.append("")
    lines.append("Watch for these signs.")
    lines.append("")
    for t in sc["tells"]:
        lines.append(f"- {t}")
    lines.append("")
    lines.append(f"Here's what's actually happening. {sc['happening']}")
    lines.append("")
    letter, q, rest, closed = split_check(sc["check"])
    close_mark = "”" if closed else ""
    if letter:
        check_line = f"Run the check. The {letter} check: “{q}{close_mark}"
    else:
        check_line = f"Run the check. “{q}{close_mark}"
    if rest:
        check_line += f" — {rest}"
    lines.append(img_marker(f"images/{slug}/check-card.png",
                             "hold this on screen with the check question and letter typed in; "
                             "you can shorten the line below to just naming the check instead of "
                             "reading the full quote if you want this under 3 minutes."))
    lines.append("")
    lines.append(check_line)
    lines.append("")
    if sc.get("dark") and sc.get("darkTitle"):
        lines.append(f"Here's the dark reality. {sc['darkTitle']}. {sc['dark']}")
        lines.append("")
    lines.append(f"Here's your move. {sc['move']}")
    lines.append("")
    lines.append(f"Here's exactly what to say. “{sc['say']}”")
    lines.append("")
    lines.append(f"And here's the truth. {sc['truth']}")
    return "\n".join(lines)


def scenario_doc(g, sc, n, total_in_guide, section_title, section_desc):
    accent = g.get("_accent", "")
    section_short = section_title.split("—")[0].strip()
    video_intro_spoken = f"This one's {g['acronym']} — {section_short}. Here's the scenario."
    closing_line = f"Find this one, and every other scenario, free, at {SITE_URL}."
    lines = []
    lines.append(f"# \U0001F3AC VIDEO INTRO")
    lines.append("")
    lines.append(f"**Guide:** {g['acronym']} — {g['role']} ({g['edition']})  ")
    lines.append(f"**Section:** {section_title}  ")
    lines.append(f"**Scenario {n} of {total_in_guide} in this guide**  ")
    if accent:
        lines.append(f"**Accent color (matches this guide on the live site):** `{accent}`  ")
    lines.append("")
    lines.append("*Suggested on-screen text, first 3–4 seconds:*")
    lines.append("")
    lines.append(f"> **{g['acronym']}** · {sc['section']}")
    lines.append(f"> “{sc['hook']}”")
    lines.append("")
    lines.append("*Spoken intro — read this first, about 5–8 seconds:*")
    lines.append("")
    lines.append(f"“{video_intro_spoken}”")
    lines.append("")
    lines.append(img_marker(f"images/{g['slug']}/cover.png",
                             "video open — type this scenario's title into the blank bottom "
                             "third before recording, then cut or fade from it into the scene."))
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"# “{sc['hook']}”")
    lines.append(f"*{sc['archetype']} — clinically, {soft_lower(sc['clinical'])}.*")
    lines.append("")
    body = scenario_body(sc, g["slug"])
    lines.append(body)
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(closing_line)
    lines.append("")

    title_line = f"{sc['hook']} {sc['archetype']} clinically {sc['clinical']}"
    word_count = spoken_word_count(video_intro_spoken, title_line, body, closing_line)
    runtime = fmt_time(word_count)
    header = (
        f"<!-- {g['acronym']} #{n} — “{sc['hook']}” — "
        f"~{word_count} spoken words — est. {runtime} at {WPM}wpm -->\n"
    )
    return header + "\n".join(lines), word_count, runtime


def main():
    d = json.load(open(DATA, encoding="utf-8"))

    # pull each guide's live accent color out of the rendered page so the
    # video-intro spec can tell someone which color to use, rather than
    # inventing one
    page = Path("library/festival/index.html").read_text(encoding="utf-8")
    accents = dict(re.findall(r"\.(fb-g-[a-z]+)\{ --acc:(#[0-9A-Fa-f]{6});", page))
    for g in d["guides"]:
        g["_accent"] = accents.get(g["acronymClass"], "")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    total_files = 0
    under_3min = 0
    manifest = []

    for g in d["guides"]:
        gdir = OUT_DIR / g["slug"]
        gdir.mkdir(parents=True, exist_ok=True)

        by_section = {}
        for sc in g["scenarios"]:
            by_section.setdefault(sc["section"], []).append(sc)
        order = [o["key"] for o in g["outline"] if o["key"] in by_section]
        for key in by_section:
            if key not in order:
                order.append(key)

        n = 0
        for key in order:
            title = SECTION_TITLES.get(key, key.title())
            desc = next((o["desc"] for o in g["outline"] if o["key"] == key), key.title())
            for sc in by_section[key]:
                n += 1
                doc, words, runtime = scenario_doc(g, sc, n, len(g["scenarios"]), title, desc)
                fname = f"{n:02d}-{slugify(sc['hook'])}.md"
                (gdir / fname).write_text(doc, encoding="utf-8")
                total_files += 1
                secs = round(words / WPM * 60)
                if secs <= 180:
                    under_3min += 1
                manifest.append((g["acronym"], n, sc["hook"], words, runtime, secs <= 180,
                                 f"{g['slug']}/{fname}"))

        print(f"  {g['acronym']:14} {n:3} posts -> {gdir}/")

    # a manifest so the person can find "the S.A.F.E. one about crowd crush"
    # without opening 270 files
    idx = [
        "# The Festie Bible — Individual Post Scripts", "",
        f"{total_files} scenarios, each its own file in `posts/<guide>/`, ready to load "
        "to social media one at a time.", "",
        f"Runtimes are estimated from what actually gets spoken out loud (not the markdown "
        f"labels), at {WPM} words per minute — a natural, unhurried teleprompter pace. Read "
        "faster and everything runs shorter than shown.", "",
        f"**{under_3min}/{total_files} land at or under 3:00** with nothing cut to force it "
        "— that's just how long those particular scenarios take to read. Nothing in any file "
        "was shortened to hit a time target; only the video-intro framing (which this "
        "script wrote, not the book) was kept as lean as possible.", "",
        f"Live and updated at **{SITE_URL}**.", "",
        "| Guide | # | Scenario | Est. time | ≤3:00 | File |",
        "|---|---:|---|---:|:---:|---|",
    ]
    for acr, n, hook, words, runtime, ok, path in manifest:
        idx.append(f"| {acr} | {n} | {titlecase(hook)} | {runtime} | {'✓' if ok else ''} | `posts/{path}` |")
    idx.append("")
    Path("content/festie-teleprompter/01-POSTS-INDEX.md").write_text("\n".join(idx), encoding="utf-8")

    print(f"\n{total_files} individual post scripts written to {OUT_DIR}/")
    print(f"{under_3min}/{total_files} land at or under 3:00 at {WPM}wpm without any content cut")
    return 0


if __name__ == "__main__":
    sys.exit(main())

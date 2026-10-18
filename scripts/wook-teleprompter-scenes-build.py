#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Split Wook's teleprompter scripts one step further: one file per natural
video section (the same modules scripts/wook-teleprompter-build.py already
identifies -- cold open, setup, one per Track, mirror+discog, tales/the
save, fanny pack, soundcheck, closer) instead of one combined file per
chapter. Same relationship as the Festie Bible's posts/ split to its 21
combined guide scripts: nothing new is written, the existing per-chapter
breakdown is just separated into individually-postable files.

No images, no [INSERT IMAGE HERE] markers -- text only, per the ask.

Reuses scripts/wook-teleprompter-build.py's HTML parsing (imported directly
since the filename isn't a valid module name) rather than re-implementing
it, so both stay in sync with a single parser.

Source of truth: library/wook/index.html. Run after any change to the live
book, or after re-running wook-teleprompter-build.py, so the two stay
consistent with each other.
"""
import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "content/wook-teleprompter/posts"
SITE_URL = "www.noblefathercreations.com/wook"

CONTRACTION_RE = re.compile(r"[’'](S|Re|T|Ll|D|Ve|M)\b")


def titlecase(s):
    """str.title() capitalizes after every apostrophe (It'S, Don'T). This
    fixes the contraction tail back down -- several chapter titles
    (IT'S NOT DRAMA, IT'S WARFARE) hit this. Source text uses a curly
    apostrophe (U+2019), not a straight one, so both need matching."""
    return CONTRACTION_RE.sub(lambda m: m.group(0)[0] + m.group(1).lower(), s.title())

spec = importlib.util.spec_from_file_location("wook_teleprompter_build", ROOT / "scripts/wook-teleprompter-build.py")
wtb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wtb)


def chapter_sections(ch):
    """Same module sequence as wtb.chapter_doc, but yielding
    (title, body_text) pairs instead of concatenating into one doc."""
    out = []

    if ch["cold_open"]:
        body = ch["cold_open"]
        if ch["pov"]:
            body = f"*{ch['pov']}*\n\n{body}"
        out.append(("THE DROP (Cold Open)", body))

    setup_parts = []
    if ch["quote"]:
        q = f"Here's the soundboard quote for this chapter. {ch['quote']}"
        if ch["quote_attr"]:
            q += f" {ch['quote_attr']}"
        setup_parts.append(q)
    if ch["thesis"]:
        setup_parts.append(f"Here's what this chapter is actually about. {ch['thesis']}")
    if ch["roster"]:
        setup_parts.append(f"And here's the roster — the fronts in this chapter. {ch['roster']}")
    if setup_parts:
        out.append(("The Setup", "\n\n".join(setup_parts)))

    for t in ch["tracks"]:
        out.append((f"Track {t['n']:02d} — {t['title']}", wtb.track_script(t)))

    mm_parts = []
    if ch["mirror"]:
        title = ch["mirror_title"] or "Here's the mirror check"
        sep = "" if title[-1] in "?!." else "."
        mm_parts.append(f"{title}{sep} {ch['mirror']}")
    if ch["discog"]:
        mm_parts.append(f"Here's the Wook Discog for this chapter. {ch['discog']}")
    if mm_parts:
        out.append(("The Mirror + The Discog", "\n\n".join(mm_parts)))

    if ch["tales"]:
        out.append((ch["tales_title"] or "Tales From — The Save", ch["tales"]))

    if ch["fanny"]:
        out.append(("The Fanny Pack (chapter recap)", ch["fanny"]))

    if ch["soundcheck"]:
        title = "The Soundcheck" + (f" — {ch['soundcheck_name']}" if ch["soundcheck_name"] else "")
        out.append((title, ch["soundcheck"]))

    close_parts = []
    if ch["sunrise"]:
        close_parts.append(f"Here's the Sunrise Set. Zero slang — just the true thing. {ch['sunrise']}")
    if ch["kandi_vows"]:
        vows = "\n".join(f"- {v}" for v in ch["kandi_vows"])
        close_parts.append(f"And here's the Kandi Trade — the vow.\n\n{vows}")
        if ch["kandi_final"]:
            close_parts.append(ch["kandi_final"])
    if close_parts:
        body = "\n\n".join(close_parts)
        if ch["bridge"]:
            body += f"\n\n*(Optional tease over the outro, into next chapter: “{ch['bridge']}”)*"
        out.append(("The Sunrise Set + The Kandi Trade (closer)", body))

    return out


def post_doc(ch, n, total, title, body):
    words = wtb.wc(body)
    runtime = wtb.rt(words)
    lines = []
    lines.append(f"# \U0001F3AC VIDEO INTRO")
    lines.append("")
    lines.append(f"**Book:** Wook in Sheep's Clothing  ")
    lines.append(f"**Chapter {ch['num']}:** {ch['title']}  ")
    lines.append(f"**This video:** {title}  ")
    lines.append(f"**Video {n} of {total} in this chapter**  ")
    lines.append("")
    lines.append("*Suggested on-screen text, first 3–4 seconds:*")
    lines.append("")
    lines.append(f"> **Chapter {ch['num']}** · {title}")
    lines.append("")
    lines.append("*Spoken intro — read this first, about 3–5 seconds:*")
    lines.append("")
    lines.append(f"“Chapter {ch['num']}: {titlecase(ch['title'])}. {title}.”")
    lines.append("")
    lines.append("---")
    lines.append("")
    # Track sections already open with their own "### TRACK NN -- TITLE"
    # heading (from wtb.track_script) -- adding another "## title" above it
    # would just repeat the same line twice.
    if not body.lstrip().startswith("###"):
        lines.append(f"## {title}")
        lines.append("")
    lines.append(body)
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"Every chapter, every Track, free, at {SITE_URL}.")
    lines.append("")

    header = f"<!-- Ch{ch['num']} #{n}/{total} — {title} — ~{words} spoken words — est. {runtime} at {wtb.WPM}wpm -->\n"
    return header + "\n".join(lines), words, runtime


def main():
    only = set(int(a) for a in sys.argv[1:]) if len(sys.argv) > 1 else None
    chapters = wtb.load_chapters()
    if only:
        chapters = [c for c in chapters if c["num"] in only]
        if not chapters:
            raise SystemExit(f"no chapter matches {only}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    total_files = 0
    manifest = []

    for ch in chapters:
        cdir = OUT_DIR / f"{ch['num']:02d}-{wtb.slugify(ch['short_title'])}"
        cdir.mkdir(parents=True, exist_ok=True)
        sections = chapter_sections(ch)
        for i, (title, body) in enumerate(sections, start=1):
            doc, words, runtime = post_doc(ch, i, len(sections), title, body)
            fname = f"{i:02d}-{wtb.slugify(title)}.md"
            (cdir / fname).write_text(doc, encoding="utf-8")
            total_files += 1
            manifest.append((ch["num"], ch["title"], i, len(sections), title, words, runtime,
                              f"{cdir.name}/{fname}"))
        print(f"  ch{ch['num']:2} {ch['title']:32} {len(sections):2} posts -> {cdir}/")

    if not only or len(chapters) == 33:
        idx = [
            "# Wook in Sheep's Clothing — Individual Video Scripts", "",
            f"{total_files} video sections, each its own file in `posts/<chapter>/`, ready to "
            "post or film one at a time. Same modules as the combined chapter scripts in "
            "`../` (see `../00-APPROACH.md`), just split apart.", "",
            f"Live and updated at **{SITE_URL}**.", "",
            "| Ch | Chapter | # | Section | Est. time | File |",
            "|---:|---|---:|---|---:|---|",
        ]
        for num, ch_title, i, total_i, title, words, runtime, path in manifest:
            idx.append(f"| {num} | {titlecase(ch_title)} | {i}/{total_i} | {title} | {runtime} | `posts/{path}` |")
        idx.append("")
        idx.append(f"**{total_files} individual video scripts across {len(manifest and set(m[0] for m in manifest))} chapters.**")
        idx.append("")
        (OUT_DIR.parent / "01-POSTS-INDEX.md").write_text("\n".join(idx), encoding="utf-8")

    print(f"\n{total_files} individual video scripts written to {OUT_DIR}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build teleprompter-ready scripts for Wook in Sheep's Clothing, one file
per chapter, organized into the book's own natural video-sized modules
instead of an invented chunking scheme.

The book already ships in labeled sections that map cleanly onto separate
videos: a cold open, a setup, one module per Track, a mirror/discog
interlude, a real-world save story, a practical recap, a drill, and a
closing pair. This script pulls each of those straight out of the live
HTML (same parsing approach as scripts/wook-continuity-check.py's Book
class -- chwrap/ch-end markers, balanced <section> scanning) and turns
each into flowing read-aloud narration, the same house rule as the Festie
Bible builders: change as few words as possible, add only the connective
lead-ins a presenter needs between fields.

Source of truth: library/wook/index.html (never hand-edit the output).
Run after any change to the live book so the scripts stay in sync.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WOOK = ROOT / "library/wook/index.html"
OUT_DIR = ROOT / "content/wook-teleprompter"
WPM = 150

ENTITIES = {
    "&rsquo;": "’", "&lsquo;": "‘", "&rdquo;": "”", "&ldquo;": "“",
    "&mdash;": "—", "&ndash;": "–", "&amp;": "&", "&#8217;": "’",
    "&middot;": "·", "&hellip;": "…", "&nbsp;": " ", "&#39;": "'",
    "&quot;": '"', "&lt;": "<", "&gt;": ">",
}


def decode_entities(s):
    for k, v in ENTITIES.items():
        s = s.replace(k, v)
    return s


def clean_text(html):
    """HTML fragment -> flowing plain text. Paragraph breaks become blank
    lines; <strong>/<em> become markdown emphasis; everything else
    (marks, spans, svg, data attrs) is stripped, not translated."""
    s = re.sub(r'<(script|style|svg)[^>]*>.*?</\1>', ' ', html, flags=re.S)
    s = re.sub(r'<br\s*/?>', '\n', s)
    # "Pocket scripts" and the Safety Appendix are laid out as individual
    # <span class="chip">...</span> pills, not <p> paragraphs -- without
    # this they'd run together with no breaks at all.
    s = re.sub(r'<span class="chip[^"]*">(.*?)</span>', r'\n- \1', s, flags=re.S)
    # Every <p> opens a new paragraph, regardless of what precedes it (a
    # </p>, a </div>, nothing) -- a naive "only after </p>" rule loses the
    # break whenever a <p> sits inside a nested <div> (e.g. the thesis
    # section's "tapers" aside), producing a run-on paragraph.
    s = re.sub(r'<p[^>]*>', '\n\n', s)
    s = re.sub(r'</p>', '', s)
    s = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', s, flags=re.S)
    s = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', s, flags=re.S)
    s = re.sub(r'<mark[^>]*>(.*?)</mark>', r'\1', s, flags=re.S)
    s = re.sub(r'<[^>]+>', '', s)
    s = decode_entities(s)
    s = re.sub(r'[ \t]{2,}', ' ', s)
    s = re.sub(r'\n{3,}', '\n\n', s)
    return s.strip()


def top_level_sections(html):
    """Balanced-tag scan for top-level <section ...>...</section> blocks --
    a regex split can't handle nested sections correctly, this can."""
    out = []
    tag_re = re.compile(r'<(/?)section\b([^>]*)>')
    depth = 0
    start_pos = start_attrs = None
    for m in tag_re.finditer(html):
        if m.group(1) != '/':
            if depth == 0:
                start_pos, start_attrs = m.start(), m.group(2)
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                out.append((start_attrs or "", html[start_pos:m.end()]))
    return out


def sec_class(attrs):
    m = re.search(r'class="([^"]*)"', attrs)
    return (m.group(1) if m else "").split()


def field(html, cls, tag="p"):
    m = re.search(rf'<{tag} class="{cls}[^"]*">(.*?)</{tag}>', html, re.S)
    return clean_text(m.group(1)) if m else None


def top_level_divs(html):
    """Balanced-tag scan for top-level <div ...>...</div> blocks, same
    technique as top_level_sections -- used to split a track's cards."""
    out = []
    tag_re = re.compile(r'<(/?)div\b([^>]*)>')
    depth = 0
    start_pos = start_attrs = None
    for m in tag_re.finditer(html):
        if m.group(1) != '/':
            if depth == 0:
                start_pos, start_attrs = m.start(), m.group(2)
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                out.append((start_attrs or "", html[start_pos:m.end()]))
    return out


def parse_track(html, n):
    title = field(html, "track-title", "h3") or f"TRACK {n}"
    subtitle_m = re.search(r'</h3>\s*<p><em>\(([^)]*)\)</em></p>', html)
    subtitle = clean_text(subtitle_m.group(1)) if subtitle_m else None

    cards = {}
    for attrs, div in top_level_divs(html):
        cls = sec_class(attrs)
        if "subplain" in cls:
            tag = field(div, "plain-tag")
            body = re.sub(r'<p class="plain-tag">.*?</p>', '', div, flags=re.S)
            body = clean_text(body)
            if tag and "BEHAVIOR" in tag:
                cards["behavior"] = body
            elif tag and "READ" in tag:
                cards["read"] = body
        elif "counterdrop" in cls:
            name = field(div, "cd-name")
            if name:
                name = name.lstrip("→ ").strip()
            body = re.sub(r'<div class="cd-head">.*?</div>', '', div, flags=re.S)
            cards["counterdrop_name"] = name
            cards["counterdrop"] = clean_text(body)
        elif "subcard" in cls:
            tag = field(div, "sub-tag")
            body = re.sub(r'<p class="sub-tag">.*?</p>', '', div, flags=re.S)
            body = clean_text(body)
            if "vibe" in cls:
                cards["vibe"] = body
            elif "mirror" in cls:
                cards["mirror"] = body
            elif "refraction" in cls:
                cards["refractions"] = body
            elif "runs" in cls:
                cards["runs"] = body
            elif "tuesday" in cls:
                cards["tuesday"] = body
    return {"n": n, "title": title, "subtitle": subtitle, **cards}


def parse_chapter(num, html):
    poster_m = re.search(r'<section class="ch-poster[^"]*" id="ch\d+">(.*?)</section>', html, re.S)
    poster = poster_m.group(1) if poster_m else ""
    title = clean_text(re.search(r'poster-title">(.*?)</h2>', poster, re.S).group(1))
    subtitle = field(poster, "poster-and")
    part = field(poster, "poster-part")
    meta = field(poster, "poster-meta")
    rail_m = re.search(r'<div class="rail rail-l"><span>([^<]*)</span></div>', poster)
    short_title = rail_m.group(1).split("·")[-1].strip() if rail_m else title

    ch = {
        "num": num, "title": title, "short_title": short_title,
        "subtitle": subtitle, "part": part, "meta": meta,
        "cold_open": None, "pov": None, "quote": None, "quote_attr": None,
        "thesis": None, "roster": None, "tracks": [], "mirror": None,
        "mirror_title": None, "discog": None, "tales": None, "tales_title": None,
        "fanny": None, "soundcheck": None, "soundcheck_name": None,
        "sunrise": None, "kandi_vows": [], "kandi_final": None, "bridge": None,
    }

    for attrs, sec in top_level_sections(html):
        cls = sec_class(attrs)
        if "ch-poster" in cls:
            continue
        if "comp-drop" in cls:
            ch["pov"] = field(sec, "pov")
            body = re.sub(r'<div class="comp-head">.*?</div>', '', sec, flags=re.S)
            body = re.sub(r'<p class="pov">.*?</p>', '', body, flags=re.S)
            ch["cold_open"] = clean_text(body)
        elif "comp-board" in cls:
            ch["quote"] = field(sec, "board-q")
            ch["quote_attr"] = field(sec, "attr")
        elif "comp-thesis" in cls:
            body = re.sub(r'<div class="comp-head">.*?</div>', '', sec, flags=re.S)
            ch["thesis"] = clean_text(body)
        elif "comp-roster" in cls:
            body = re.sub(r'<div class="comp-head">.*?</div>', '', sec, flags=re.S)
            ch["roster"] = clean_text(body)
        elif "specimen" in cls:
            continue
        elif "track" in cls:
            ch["tracks"].append(parse_track(sec, len(ch["tracks"]) + 1))
        elif "inter-mirror-big" in cls:
            ch["mirror_title"] = field(sec, "comp-title")
            body = re.sub(r'<div class="comp-head">.*?</div>', '', sec, flags=re.S)
            ch["mirror"] = clean_text(body)
        elif "inter-discog" in cls:
            body = re.sub(r'<div class="comp-head">.*?</div>', '', sec, flags=re.S)
            ch["discog"] = clean_text(body)
        elif "inter-tales" in cls:
            ch["tales_title"] = field(sec, "comp-title")
            body = re.sub(r'<div class="comp-head">.*?</div>', '', sec, flags=re.S)
            ch["tales"] = clean_text(body)
        elif "comp-fanny" in cls:
            body = re.sub(r'<div class="comp-head">.*?</div>', '', sec, flags=re.S)
            ch["fanny"] = clean_text(body)
        elif "comp-drill" in cls:
            ch["soundcheck_name"] = field(sec, "comp-name")
            body = re.sub(r'<div class="comp-head">.*?</div>', '', sec, flags=re.S)
            ch["soundcheck"] = clean_text(body)
        elif "comp-sunrise" in cls:
            body = re.sub(r'<div class="comp-head">.*?</div>', '', sec, flags=re.S)
            ch["sunrise"] = clean_text(body)
        elif "comp-kandi" in cls:
            ch["kandi_vows"] = [clean_text(v) for v in re.findall(r'<p class="vow">(.*?)</p>', sec, re.S)]
            final_m = re.search(r'<p class="vow-final">(.*?)</p>', sec, re.S)
            ch["kandi_final"] = clean_text(final_m.group(1)) if final_m else None
        elif "bridge" in cls:
            body = re.sub(r'<p class="comp-title[^"]*">.*?</p>', '', sec, flags=re.S)
            ch["bridge"] = clean_text(body)
    return ch


def load_chapters():
    raw = WOOK.read_text(errors="surrogateescape")
    raw = re.sub(r'(src="data:[^"]{200,}")', 'src="data:..."', raw)
    starts = {int(m.group(1)): m.start() for m in
              re.finditer(r'<div class="chwrap s\d" data-ch="(\d+)">', raw)}
    ends = {int(m.group(1)): m.start() for m in
            re.finditer(r'<i class="ch-end" data-ch="(\d+)">', raw)}
    chapters = []
    for n in sorted(starts):
        html = raw[starts[n]:ends[n]]
        chapters.append(parse_chapter(n, html))
    return chapters


SLUG_RE = re.compile(r"[^a-z0-9]+")


def slugify(s):
    return SLUG_RE.sub("-", s.lower()).strip("-")


def wc(text):
    return len(text.split()) if text else 0


def rt(words):
    secs = round(words / WPM * 60)
    m, s = divmod(secs, 60)
    return f"{m}:{s:02d}"


def video_header(n, title, words):
    return f"## \U0001F3AC VIDEO {n} — {title}\n*~{words} spoken words · est. {rt(words)} at {WPM}wpm*\n"


def track_script(t):
    lines = [f"### TRACK {t['n']:02d} — {t['title']}"]
    if t.get("subtitle"):
        lines.append(f"*({t['subtitle']})*")
    lines.append("")
    if t.get("behavior"):
        lines.append(f"Here's the behavior. {t['behavior']}")
        lines.append("")
    if t.get("read"):
        lines.append(f"Here's the read on it. {t['read']}")
        lines.append("")
    if t.get("counterdrop"):
        name = f" {t['counterdrop_name']}." if t.get("counterdrop_name") else ""
        lines.append(f"Here's your counter-drop — run this.{name} {t['counterdrop']}")
        lines.append("")
    if t.get("vibe"):
        lines.append(f"Quick vibe check. {t['vibe']}")
        lines.append("")
    if t.get("mirror"):
        lines.append(f"Turn it around — the mirror set. {t['mirror']}")
        lines.append("")
    if t.get("refractions"):
        lines.append(f"Refractions — this lands differently depending on who you are. {t['refractions']}")
        lines.append("")
    if t.get("runs"):
        lines.append(f"This runs in every direction. {t['runs']}")
        lines.append("")
    if t.get("tuesday"):
        lines.append(f"And Sober Tuesday — the morning-after truth. {t['tuesday']}")
        lines.append("")
    return "\n".join(lines)


def chapter_doc(ch):
    lines = []
    lines.append(f"# Chapter {ch['num']} — {ch['title']}")
    if ch["subtitle"]:
        lines.append(f"### {ch['subtitle']}")
    meta_bits = [b for b in (ch["part"], ch["meta"]) if b]
    if meta_bits:
        lines.append(f"*{' · '.join(meta_bits)}*")
    lines.append("")
    lines.append("*A teleprompter breakdown of this chapter's own built-in modules "
                  "— each `VIDEO` heading below is a natural, separately-postable "
                  "video, in the order the book already presents them.*")
    lines.append("")
    lines.append("---")
    lines.append("")

    vid = 1
    total_words = 0

    # VIDEO 1 -- the cold open
    if ch["cold_open"]:
        words = wc(ch["cold_open"])
        total_words += words
        lines.append(video_header(vid, "THE DROP (Cold Open)", words)); vid += 1
        if ch["pov"]:
            lines.append(f"*{ch['pov']}*\n")
        lines.append(ch["cold_open"])
        lines.append("")
        lines.append("---")
        lines.append("")

    # VIDEO 2 -- the setup (quote + thesis + roster)
    setup_parts = []
    if ch["quote"]:
        # ch["quote"] and ch["quote_attr"] already carry their own quote
        # marks / leading em-dash from the source markup -- adding more
        # here would double them up.
        q = f"Here's the soundboard quote for this chapter. {ch['quote']}"
        if ch["quote_attr"]:
            q += f" {ch['quote_attr']}"
        setup_parts.append(q)
    if ch["thesis"]:
        setup_parts.append(f"Here's what this chapter is actually about. {ch['thesis']}")
    if ch["roster"]:
        setup_parts.append(f"And here's the roster — the fronts in this chapter. {ch['roster']}")
    if setup_parts:
        body = "\n\n".join(setup_parts)
        words = wc(body)
        total_words += words
        lines.append(video_header(vid, "The Setup", words)); vid += 1
        lines.append(body)
        lines.append("")
        lines.append("---")
        lines.append("")

    # VIDEO 3.. -- one per track
    for t in ch["tracks"]:
        body = track_script(t)
        words = wc(body)
        total_words += words
        lines.append(video_header(vid, f"Track {t['n']:02d} — {t['title']}", words)); vid += 1
        lines.append(body)
        lines.append("---")
        lines.append("")

    # VIDEO -- the mirror + the discog
    mm_parts = []
    if ch["mirror"]:
        title = ch["mirror_title"] or "Here's the mirror check"
        sep = "" if title[-1] in "?!." else "."
        mm_parts.append(f"{title}{sep} {ch['mirror']}")
    if ch["discog"]:
        mm_parts.append(f"Here's the Wook Discog for this chapter. {ch['discog']}")
    if mm_parts:
        body = "\n\n".join(mm_parts)
        words = wc(body)
        total_words += words
        lines.append(video_header(vid, "The Mirror + The Discog", words)); vid += 1
        lines.append(body)
        lines.append("")
        lines.append("---")
        lines.append("")

    # VIDEO -- Tales From ... The Save
    if ch["tales"]:
        words = wc(ch["tales"])
        total_words += words
        title = ch["tales_title"] or "Tales From — The Save"
        lines.append(video_header(vid, title, words)); vid += 1
        lines.append(ch["tales"])
        lines.append("")
        lines.append("---")
        lines.append("")

    # VIDEO -- the fanny pack
    if ch["fanny"]:
        words = wc(ch["fanny"])
        total_words += words
        lines.append(video_header(vid, "The Fanny Pack (chapter recap)", words)); vid += 1
        lines.append(ch["fanny"])
        lines.append("")
        lines.append("---")
        lines.append("")

    # VIDEO -- the soundcheck (drill)
    if ch["soundcheck"]:
        words = wc(ch["soundcheck"])
        total_words += words
        title = "The Soundcheck" + (f" — {ch['soundcheck_name']}" if ch["soundcheck_name"] else "")
        lines.append(video_header(vid, title, words)); vid += 1
        lines.append(ch["soundcheck"])
        lines.append("")
        lines.append("---")
        lines.append("")

    # VIDEO -- closer: sunrise set + kandi trade + bridge tease
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
        words = wc(body)
        total_words += words
        lines.append(video_header(vid, "The Sunrise Set + The Kandi Trade (closer)", words)); vid += 1
        lines.append(body)
        if ch["bridge"]:
            lines.append("")
            lines.append(f"*(Optional tease over the outro, into next chapter: “{ch['bridge']}”)*")
        lines.append("")
        lines.append("---")
        lines.append("")

    lines.append(f"**{vid - 1} videos this chapter · ~{total_words:,} spoken words total "
                  f"· ~{rt(total_words)} read straight through at {WPM}wpm.**")
    lines.append("")
    return "\n".join(lines), vid - 1, total_words


def main():
    only = set(int(a) for a in sys.argv[1:]) if len(sys.argv) > 1 else None
    chapters = load_chapters()
    if only:
        chapters = [c for c in chapters if c["num"] in only]
        if not chapters:
            raise SystemExit(f"no chapter matches {only}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest = []
    for ch in chapters:
        doc, n_videos, words = chapter_doc(ch)
        fname = f"{ch['num']:02d}-{slugify(ch['short_title'])}.md"
        (OUT_DIR / fname).write_text(doc, encoding="utf-8")
        manifest.append((ch["num"], ch["title"], len(ch["tracks"]), n_videos, words, fname))
        print(f"  ch{ch['num']:2} {ch['title']:32} {len(ch['tracks'])} tracks  "
              f"{n_videos:2} videos  ~{words:6,} words -> {fname}")

    if not only or len(chapters) == 33:
        idx = [
            "# Wook in Sheep's Clothing — Teleprompter Scripts", "",
            f"One markdown file per chapter, {sum(m[3] for m in manifest)} videos total across "
            f"{len(manifest)} chapters, each internally divided into `VIDEO` sections that "
            "map onto the book's own built-in modules — see `00-APPROACH.md` for the "
            "reasoning behind the breakdown.", "",
            "| Ch | Title | Tracks | Videos | ~Words | File |",
            "|---:|---|---:|---:|---:|---|",
        ]
        for num, title, n_tracks, n_videos, words, fname in manifest:
            idx.append(f"| {num} | {title} | {n_tracks} | {n_videos} | {words:,} | `{fname}` |")
        idx.append("")
        idx.append(f"**Totals: {sum(m[3] for m in manifest)} videos, "
                    f"~{sum(m[4] for m in manifest):,} spoken words across all 33 chapters.**")
        idx.append("")
        (OUT_DIR / "00-INDEX.md").write_text("\n".join(idx), encoding="utf-8")

    print(f"\n{len(manifest)} chapter script(s) written to {OUT_DIR}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())

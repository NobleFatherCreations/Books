#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render the seven new chapters as one readable markdown file for review.

The chapters live as HTML fragments so they can be spliced into the book
byte-for-byte. This converts them to markdown for reading — the point is
to check tone, slang and voice, so it keeps every component label and
every word, and drops only the markup.

Run: python3 scripts/wook-newchapters-md.py
"""
import html as htmlmod
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "content/wook-new-chapters"
OUT = ROOT / "content/wook-audits/wook-new-chapters-READTHIS.md"

CHAPTERS = [6, 10, 14, 17, 20, 26, 31]


def text_of(fragment):
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", fragment, flags=re.S)
    s = re.sub(r"<svg\b.*?</svg>", "", s, flags=re.S)
    s = re.sub(r"</?(?:span|mark|a|u|code|small|sup|sub|abbr|q|s)\b[^>]*>", "", s)
    s = re.sub(r"<strong[^>]*>(.*?)</strong>", r"**\1**", s, flags=re.S)
    s = re.sub(r"<em>(.*?)</em>", r"*\1*", s, flags=re.S)
    s = re.sub(r"<[^>]+>", "\n", s)
    s = htmlmod.unescape(s)
    lines = [re.sub(r"[ \t]+", " ", ln).strip() for ln in s.split("\n")]
    return [ln for ln in lines if ln]


def render(ch):
    frag = (SRC / f"ch{ch:02d}.html").read_text(encoding="utf-8")

    title = re.search(r'<h2 class="poster-title">(.*?)</h2>', frag, re.S).group(1)
    title = re.sub(r"<[^>]+>", "", title).strip()
    andline = re.search(r'<p class="poster-and">([^<]*)</p>', frag).group(1)
    keys = re.search(r'<p class="poster-keys">([^<]*)</p>', frag).group(1)
    meta = re.search(r'<p class="poster-meta">([^<]*)</p>', frag).group(1)
    part = re.search(r'<p class="poster-part">([^<]*)</p>', frag).group(1)

    out = [f"\n\n---\n\n# CHAPTER {ch} — {title}",
           f"### {andline}",
           f"*{part.strip('◇ ').strip()} · {meta}*",
           f"\n**Keys:** {keys}\n"]

    # each top-level section becomes a block, in document order
    body = frag[frag.find('<section class="panel'):]
    for m in re.finditer(r'<section class="([^"]*)"[^>]*>(.*?)</section>', body, re.S):
        cls, inner = m.group(1), m.group(2)
        track_no = re.search(r'TRACK (\d+)', inner)
        # the <div class="comp-head"> repeats the component's own name, which
        # the markdown heading below already carries
        inner = re.sub(r'<div class="comp-head">.*?</div></div>', '', inner, flags=re.S)
        inner = re.sub(r'<div class="track-head">.*?</div>', '', inner, flags=re.S)
        lines = text_of(inner)
        lines = [ln for ln in lines if not re.fullmatch(r'[^\w]{1,4}', ln)]
        if not lines:
            continue
        if "comp-drop" in cls:
            head = "## 🎬 THE DROP — the cold open"
        elif "comp-board" in cls:
            head = "## 🎚️ THE SOUNDBOARD QUOTE"
        elif "comp-thesis" in cls:
            head = "## 🎯 THE REAL F*CKING SETLIST"
        elif "comp-roster" in cls:
            head = "## 🪖 THE WOOK’S SETLIST"
        elif "specimen" in cls:
            head = "## 🔬 FIELD SPECIMEN"
        elif "prose track" in cls:
            t = re.search(r'<h3 class="track-title">([^<]*)</h3>', inner)
            head = (f"## 🎫 TRACK {track_no.group(1)} — {t.group(1)}"
                    if t and track_no else "## 🎫 TRACK")
        elif "inter-mirror-big" in cls:
            head = "## 🪞 HAVE YOU BEEN THE WOOK?"
        elif "inter-discog" in cls:
            head = "## 📊 THE WOOK DISCOG"
        elif "inter-tales" in cls:
            head = "## 🌵 THE SAVE"
        elif "comp-fanny" in cls:
            head = "## 🎒 THE FANNY PACK"
        elif "comp-drill" in cls:
            head = "## 🔦 THE SOUNDCHECK"
        elif "comp-sunrise" in cls:
            head = "## 🌅 THE SUNRISE SET"
        elif "comp-kandi" in cls:
            head = "## 🤝 THE KANDI TRADE"
        elif "bridge" in cls:
            head = "## 🌉 THE BRIDGE"
        elif "pp-yellow" in cls:
            head = "## ⚠️ CONTENT NOTE"
        else:
            head = "## —"
        out.append("\n" + head + "\n")
        out.extend(lines)
    return "\n\n".join(out)


def main():
    words = 0
    parts = ["# The Festie Codex — the seven new chapters",
             "",
             "Reading copy of everything written for the v12 expansion, in book order, "
             "with every component label kept so the structure is visible. This is for "
             "checking tone, slang and voice — the live book is the HTML.",
             "",
             "| New # | Title | Words | Sits after | POV |",
             "|---|---|---|---|---|",
             "| 6 | The Group Chat | 10,594 | Yes Is A Sober Word | Festie |",
             "| 10 | The Love Of It | 10,741 | Vendor Row Bloodsport | Witness |",
             "| 14 | The Two Festivals | 10,857 | The Road | Festie |",
             "| 17 | The Container | 11,287 | The Free One | Festie |",
             "| 20 | The Next Twelve Hours | 8,238 | The RV | Festie — After |",
             "| 26 | He Still Has Your Number | 11,565 | The Re-Entry Window | Wook |",
             "| 31 | What To Tell Your Mom | 7,636 | Protecting The Magic | Default-World |",
             ""]
    for ch in CHAPTERS:
        block = render(ch)
        words += len(re.sub(r"[#*`|—]", " ", block).split())
        parts.append(block)
    OUT.write_text("\n".join(parts), encoding="utf-8")
    print(f"{OUT.relative_to(ROOT)}  —  {OUT.stat().st_size:,} bytes, ~{words:,} words")


if __name__ == "__main__":
    main()

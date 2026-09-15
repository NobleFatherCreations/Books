#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assemble a new wook chapter from its part files and validate it before
it ever touches the book.

Each chapter is written as chNN-part1/2/3.html in
content/wook-new-chapters/. This concatenates them into chNN.html and runs
the checks that the two book-wide checkers would run, so a fragment is
never spliced in dirty:

  - straight apostrophes / quotes in prose (the book is set entirely curly)
  - tag balance for every block element used in a chapter
  - the component checklist from the expansion plan
  - data-ch / id / poster number agreement
  - no <hr>, no placeholder brackets, no doubled spaces

Run: python3 scripts/wook-newchapter-build.py 06
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "content/wook-new-chapters"

REQUIRED = [
    'class="ch-poster',
    'comp-drop',
    'comp-board',
    'comp-thesis',
    'class="tapers"',
    'class="panel pp-cream specimen"',
    'inter-mirror-big',
    'inter-discog',
    'inter-tales',
    'comp-fanny',
    'comp-drill',
    'comp-sunrise',
    'comp-kandi',
    'class="panel pp-black prose bridge"',
    'vow-final',
    'ch-end',
]

BLOCKS = ["div", "section", "p", "h2", "h3", "span", "em", "strong", "i", "svg"]


def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s)


def check(chapter):
    parts = sorted(SRC.glob(f"ch{chapter}-part*.html"))
    if not parts:
        sys.exit(f"no part files found for ch{chapter}")
    html = "".join(p.read_text(encoding="utf-8") for p in parts)
    out = SRC / f"ch{chapter}.html"
    out.write_text(html, encoding="utf-8")

    findings = []

    text = strip_tags(html)
    for m in re.finditer(r"\w'\w|\w'\s|\s'\w", text):
        findings.append(("quotes", "straight apostrophe: " + text[max(0, m.start() - 50):m.start() + 30]))
    for m in re.finditer(r'"', text):
        findings.append(("quotes", "straight double quote: " + text[max(0, m.start() - 50):m.start() + 30]))

    for tag in BLOCKS:
        opens = len(re.findall(rf"<{tag}[\s>]", html))
        closes = len(re.findall(rf"</{tag}>", html))
        selfclose = len(re.findall(rf"<{tag}[^>]*/>", html))
        if opens - selfclose != closes:
            findings.append(("markup", f"<{tag}> {opens} open ({selfclose} self-closing) vs {closes} close"))

    for req in REQUIRED:
        if req not in html:
            findings.append(("structure", f"missing component: {req}"))

    if "<hr" in html:
        findings.append(("markup", "<hr> is not used anywhere in this book"))

    for m in re.finditer(r"\[(?:your|add|insert|tk|todo)[^\]]{0,60}\]", html, re.I):
        findings.append(("placeholder", m.group(0)))

    # only inside prose paragraphs -- the poster block is indented markup,
    # exactly as every original chapter's poster is, and that is not a defect
    for para in re.findall(r"<p[^>]*>(.*?)</p>", html, re.S):
        body = strip_tags(para)
        if "  " in body:
            findings.append(("spacing", "doubled space in prose: " + repr(body[:80])))

    n_wrap = re.findall(r'<div class="chwrap [^"]*" data-ch="(\d+)">', html)
    n_end = re.findall(r'<i class="ch-end" data-ch="(\d+)">', html)
    n_id = re.findall(r'id="ch(\d+)"', html)
    n_poster = re.findall(r'<p class="poster-num">(\d+)</p>', html)
    nums = set(n_wrap + n_end + n_id + n_poster)
    if len(nums) != 1:
        findings.append(("numbering", f"chapter number disagrees across wrapper/end/id/poster: {nums}"))

    tracks = re.findall(r'<span class="gate-tag track-tag">TRACK (\d+)</span>', html)
    expected = [f"{i:02d}" for i in range(1, len(tracks) + 1)]
    if tracks != expected:
        findings.append(("tracks", f"track numbering {tracks} != {expected}"))

    keys = re.search(r'<p class="poster-keys">([^<]*)</p>', html)
    titles = re.findall(r'<h3 class="track-title">([^<]*)</h3>', html)
    if keys and titles:
        listed = [k.strip() for k in keys.group(1).split("·")]
        if len(listed) != len(titles):
            findings.append(("poster", f"poster lists {len(listed)} keys but chapter has {len(titles)} Tracks"))
        else:
            for a, b in zip(listed, titles):
                if a.upper().replace("’", "'") != b.upper().replace("’", "'"):
                    findings.append(("poster", f"poster key {a!r} != track title {b!r}"))

    meta = re.search(r'⏱ ~\d+ MIN READ · (\d+) TRACKS', html)
    if meta and int(meta.group(1)) != len(titles):
        findings.append(("poster", f"poster meta says {meta.group(1)} tracks, chapter has {len(titles)}"))

    words = len(strip_tags(html).split())
    print(f"ch{chapter}: {len(html):,} chars, ~{words:,} words, {len(titles)} Tracks -> {out.name}")
    if findings:
        print(f"\n{len(findings)} finding(s):\n")
        for kind, msg in findings[:40]:
            print(f"  [{kind}] {msg}")
        sys.exit(1)
    print("  clean")


if __name__ == "__main__":
    check(sys.argv[1] if len(sys.argv) > 1 else "06")

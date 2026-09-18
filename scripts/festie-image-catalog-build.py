#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the single catalog document for the Festie Bible's reusable video
assets (scripts/festie-image-assets-build.py's output) -- one markdown file,
same 21-guide order used throughout this project, so the whole 84-image set
can be handed over or browsed as one thing instead of 21 separate folders.

Run after festie-image-assets-build.py, and re-run either whenever the
image set changes or whenever festie-bible-data.json's guide roster/roles
change, so the catalog's captions stay accurate.
"""
import json
import re
from pathlib import Path

DATA = Path("content/festie-bible-data.json")
PAGE = Path("library/festival/index.html")
IMAGES_DIR = Path("content/festie-teleprompter/images")
OUT = Path("content/festie-teleprompter/02-IMAGE-CATALOG.md")


def load_guides():
    d = json.loads(DATA.read_text(encoding="utf-8"))
    page = PAGE.read_text(encoding="utf-8")
    accents = dict(re.findall(r"\.(fb-g-[a-z]+)\{ --acc:(#[0-9A-Fa-f]{6});", page))
    out = []
    for g in d["guides"]:
        out.append({
            "slug": g["slug"], "acronym": g["acronym"], "role": g["role"],
            "edition": g["edition"], "accent": accents.get(g["acronymClass"], ""),
            "scenario_count": len(g["scenarios"]),
        })
    return out


INTRO = """# The Festie Bible — Video Asset Catalog

Every image here is **repeatable** — built once per guide, reused across
every scenario/video in that guide. None of these are per-scenario or
per-individual-video art; those 42 (a cover + a badge, times 21 guides) are
exactly what was asked for, and everything else below rides on top of them.
84 images total: 21 guides × 4 images each.

Nothing here is AI-generated art. Every image is composed from the book's
own real logo, real fonts and real accent colors (Pillow, driven straight
from `content/festie-bible-data.json` and the live page's CSS) — the same
approach the book's own cover jackets use — because an image model still
mangles exact text (an acronym, a URL), and both need to be exact here.

## The four image types, per guide

| Type | Size | What it's for |
|---|---|---|
| **Cover** | 1080×1920 | The video's opening frame. Logo, `THE FESTIE BIBLE` label, the guide's acronym in large letters, its role line, and the site URL — with the **bottom third left genuinely blank** so you can type in that specific video's scenario title yourself before posting. Also fine as a still opening title card. |
| **Badge** | 1080×1080 | A standalone acronym mark — square, so it drops cleanly into a mid-video insert, a lower-third, or a end-card without needing to be cropped. |
| **Tells-card** | 1080×1920 | Reusable "Watch for these signs" template — header band plus six blank guide-lines. Swap in that scenario's actual tells as on-screen text instead of (or alongside) speaking them. |
| **Check-card** | 1080×1920 | Reusable "Run the check" template — header band, one open frame for the question, a small roundel for the check's letter. Same idea: put the check text on screen instead of narrating every word of it. |

## Cutting toward a 3-minute runtime with images instead of narration

The two content-card templates (tells-card, check-card) are the actual lever
here — the cover and badge are identity/branding, not narration replacements.
The "who," "scene," "here's what's actually happening," "your move," "what to
say" and "the truth" beats are the heart of each scenario and shouldn't be
cut or rushed. But the **tells list** and the **check's exact wording** are
both list-like, already read like on-screen text, and are what the
teleprompter scripts currently speak in full. Holding a tells-card or
check-card on screen while a *shorter* spoken line carries the same
information ("Here's what to watch for — it's on screen" instead of reading
all six tells aloud verbatim, or "Here's the check, read it with me" instead
of speaking the full quoted line) trims real seconds without cutting any
scenario content — the words are just moved from the voiceover to the frame.
Both combined per-guide scripts and all 270 individual post scripts below
now mark `[INSERT IMAGE HERE]` at each point one of these four images belongs,
including a note on which spoken line can shrink when the image carries it.

## How the folders map

Every image lives in `images/<slug>/` next to this file: `cover.png`,
`badge.png`, `tells-card.png`, `check-card.png`. The table below links
directly to each.

---

"""


def gh_anchor(heading):
    """GitHub's heading-to-anchor rule: lowercase, drop anything that isn't
    a letter/digit/space/hyphen, then turn spaces into hyphens."""
    s = heading.lower()
    s = re.sub(r"[^a-z0-9 \-]", "", s)
    return re.sub(r"\s+", "-", s).strip("-")


def guide_section(g):
    slug = g["slug"]
    lines = []
    lines.append(f"## {g['acronym']} — {g['role']}")
    lines.append("")
    lines.append(f"*{g['edition']} · {g['scenario_count']} scenarios"
                  + (f" · accent `{g['accent']}`" if g["accent"] else "") + "*")
    lines.append("")
    lines.append("| Cover | Badge |")
    lines.append("|---|---|")
    lines.append(f"| ![{g['acronym']} cover](images/{slug}/cover.png) | "
                  f"![{g['acronym']} badge](images/{slug}/badge.png) |")
    lines.append(f"| `images/{slug}/cover.png` — video open, blank bottom third for your title | "
                  f"`images/{slug}/badge.png` — square mid-video / lower-third insert |")
    lines.append("")
    lines.append("| Tells-card | Check-card |")
    lines.append("|---|---|")
    lines.append(f"| ![{g['acronym']} tells-card](images/{slug}/tells-card.png) | "
                  f"![{g['acronym']} check-card](images/{slug}/check-card.png) |")
    lines.append(f"| `images/{slug}/tells-card.png` — reusable across every scenario in this guide | "
                  f"`images/{slug}/check-card.png` — reusable across every scenario in this guide |")
    lines.append("")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def main():
    guides = load_guides()
    parts = [INTRO]

    toc = ["## Contents", ""]
    for g in guides:
        heading = f"{g['acronym']} — {g['role']}"
        toc.append(f"- [{heading}](#{gh_anchor(heading)})")
    toc.append("")
    toc.append("---")
    toc.append("")
    parts.append("\n".join(toc))

    for g in guides:
        parts.append(guide_section(g))

    parts.append(f"\n84 images, 21 guides. Built by `scripts/festie-image-assets-build.py`, "
                  f"cataloged by `scripts/festie-image-catalog-build.py`. Live book at "
                  f"www.noblefathercreations.com/festival.\n")

    OUT.write_text("\n".join(parts), encoding="utf-8")
    print(f"Catalog written to {OUT} ({len(guides)} guides, {len(guides) * 4} images referenced)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

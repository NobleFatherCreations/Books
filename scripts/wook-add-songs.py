#!/usr/bin/env python3
"""Add companion songs (and eventually a video) to "THE REAL ONES" section
of Wook in Sheep's Clothing (library/wook/index.html).

This is the first audio in any Noble Father book. It does NOT follow the
brass/plum "house" identity used by the hub, the guide, and the thank-you
card -- this book has its own zine aesthetic (cream paper cards, hard
black borders, offset drop shadows, Bungee/Permanent Marker/Space Mono)
and CLAUDE.md is explicit that a design pattern is never pasted uniformly
across books. The player chrome is built from wook's own tokens
(--paperA, --ink, --neon, --teal, --mono, --sign), read from its live
<style> block, not invented.

Why the audio is NOT inlined as base64, unlike every image in this book:
an image runs tens-to-hundreds of KB; these mp3s run 4-7MB each. The
Listening Room (instruments/music/) already solves this exact problem --
audio lives as sibling files, referenced by ABSOLUTE url, never
root-relative. Root-relative breaks because this book is proxied at
/wook through the hub: a `/audio/x.mp3` path resolves against
noblefathercreations.com, which has no /audio -- confirmed already broken
The Casting twice (see instruments/music/README.md). So every src here is
`https://wook-in-sheeps-clothing.netlify.app/audio/<slug>.mp3`.

Uses the *native* <audio controls> element rather than a custom player:
no JS to break, keyboard/screen-reader accessible for free, robust on a
phone at a festival. The zine identity comes from the label chip wrapped
around it, not from reimplementing browser chrome.

Idempotent and multi-song-per-org: SONGS lists every song for an org, in
display order, past and new together. A song already present (its audio
src already appears in the file) is skipped, so re-running after adding
new entries only inserts what's missing -- this is what let a second
DanceSafe and Zendo song get added without disturbing the first.

Insertion point: NOT "the last </div></div> in the card", which was this
script's first version and had a real bug -- once a card already holds a
mixtape, that mixtape's OWN internal double-close (closing its label's
inner name/sub div, then the label div) is later in the segment than
nothing, so a naive rfind lands a second song's markup mid-way through
the first song's card, between its label and its <audio> tag. Fixed by
inserting at the segment's right BOUNDARY instead (the next org-card's
start, or the closing salute paragraph for the last card) -- a position
that stays correct however many songs already sit in that card, because
it is defined by what comes AFTER the card, not by anything inside it.

Run: python3 scripts/wook-add-songs.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WOOK = ROOT / "library/wook/index.html"
AUDIO_BASE = "https://wook-in-sheeps-clothing.netlify.app/audio/"

# domain in the org's existing link -> [(audio filename, song title, blurb), ...]
# in display order. Every song, past and new -- see "Idempotent" above.
SONGS = {
    "dancesafe.org": [
        ("dancesafe.mp3", "Repetitive Beats", "an original song for DanceSafe"),
        ("dancesafe-2.mp3", "Marquis Purple", "another original song for DanceSafe"),
        ("dancesafe-3.mp3", "Come As You Are (Free Water)", "another original song for DanceSafe"),
        ("dancesafe-4.mp3", "The Chill Out Room", "another original song for DanceSafe"),
    ],
    "bunkpolice.com": [
        ("bunkpolice.mp3", "What&rsquo;s in the Baggie", "an original song for The Bunk Police"),
    ],
    "zendoproject.org": [
        ("zendo.mp3", "Sit With It", "an original song for The Zendo Project"),
        ("zendo-2.mp3", "Difficult Is Not the Same as Bad", "another original song for The Zendo Project"),
    ],
    "firesideproject.org": [
        ("fireside.mp3", "Pick Up", "an original song for Fireside Project"),
    ],
    "maps.org": [
        ("maps.mp3", "Bicycle Day", "an original song for MAPS"),
    ],
    "wharfrats.org": [
        ("wharfrats.mp3", "Lowest Bar", "an original song for The Wharf Rats"),
    ],
}

MIXTAPE_CSS = """
  /* ---- companion songs, "THE REAL ONES" (scripts/wook-add-songs.py) ----
     Built from this book's own zine tokens, not the house brass/plum
     identity -- paper card, hard border, offset shadow, mono label. */
  .mixtape{margin-top:.95rem;background:var(--paperA);border:2.5px solid #000;
    border-radius:.6rem;box-shadow:3px 3px 0 rgba(0,0,0,.6);
    padding:.7rem .75rem .8rem;color:var(--ink)}
  .mixtape-label{display:flex;align-items:center;gap:.6rem;margin-bottom:.55rem}
  .mixtape-note{width:34px;height:34px;border-radius:.45rem;border:2.5px solid #000;
    background:var(--neon);flex:none;display:grid;place-items:center;
    font-size:1.05rem;box-shadow:2px 2px 0 rgba(0,0,0,.6)}
  .mixtape-title{font-family:var(--sign);font-size:.92rem;line-height:1.15;color:var(--ink)}
  .mixtape-sub{font-family:var(--mono);font-weight:700;font-size:.6rem;
    letter-spacing:.1em;text-transform:uppercase;color:#6747E8;margin-top:.2rem}
  .mixtape audio{width:100%;display:block;height:32px}
"""


def install_css(html):
    if "class=\"mixtape\"" in html.replace(MIXTAPE_CSS, "", 1) and MIXTAPE_CSS in html:
        return html  # already installed, e.g. on a second run
    marker = ".org-links a.alt{background:var(--teal)}"
    assert html.count(marker) == 1
    return html.replace(marker, marker + "\n" + MIXTAPE_CSS, 1)


def mixtape_html(filename, title, blurb):
    src = AUDIO_BASE + filename
    return (
        '<div class="mixtape">'
        '<div class="mixtape-label">'
        '<span class="mixtape-note" aria-hidden="true">&#9834;</span>'
        f'<div><p class="mixtape-title">{title}</p>'
        f'<p class="mixtape-sub">{blurb}</p></div></div>'
        f'<audio controls preload="none" src="{src}">'
        f'<a href="{src}">{title} (MP3)</a></audio></div>'
    )


def card_bounds(html, domain):
    """The [start, end) span covering this org's whole card, INCLUDING any
    mixtapes already inserted after it -- end is the next org-card's start
    (or the closing salute paragraph, for the last card), which is exactly
    the right insertion point and stays right regardless of what already
    sits inside the span. See the module docstring for why this replaced
    an earlier, buggier approach."""
    needle = f'href="https://{domain}"'
    hit = html.find(needle)
    assert hit != -1, f"{domain} link not found anywhere in the page"

    card_starts = [m.start() for m in re.finditer(r'<div class="org-card">', html)]
    card_starts.append(html.index('<p class="org-salute">'))
    start = max(s for s in card_starts if s <= hit)
    end = min(s for s in card_starts if s > hit)
    return start, end


def install_songs(html):
    added, already = [], []
    for domain, songs in SONGS.items():
        for filename, title, blurb in songs:
            src = AUDIO_BASE + filename
            if src in html:
                already.append((domain, title))
                continue
            _, end = card_bounds(html, domain)
            html = html[:end] + mixtape_html(filename, title, blurb) + html[end:]
            added.append((domain, title))
    return html, added, already


def main():
    html = WOOK.read_text(errors="surrogateescape")
    before = len(html)

    html = install_css(html)
    html, added, already = install_songs(html)

    WOOK.write_text(html, errors="surrogateescape")
    print(f"wook: {before:,} -> {len(html):,} bytes")
    for domain, title in added:
        print(f"  + {domain:24s} {title}")
    for domain, title in already:
        print(f"  = {domain:24s} {title}  (already present)")


if __name__ == "__main__":
    sys.exit(main())

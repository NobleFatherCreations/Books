#!/usr/bin/env python3
"""Add the companion songs to "THE REAL ONES" section of Wook in Sheep's
Clothing (library/wook/index.html), and a "book, in songs" section near
the colophon for the pieces about the book itself.

This is the first audio in any Noble Father book. It does NOT follow the
brass/plum "house" identity used by the hub, the guide, and the thank-you
card -- this book has its own zine aesthetic (cream paper cards, hard
black borders, offset drop shadows, Bungee/Permanent Marker/Space Mono)
and CLAUDE.md is explicit that a design pattern is never pasted uniformly
across books. The player chrome below is built from wook's own tokens
(--paperA, --ink, --neon, --teal, --mono, --sign), read from its live
<style> block, not invented.

Why the audio is NOT inlined as base64, unlike every image in this book:
an image runs tens-to-hundreds of KB; these mp3s run 4.5-6.7MB each. The
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

Run: python3 scripts/wook-add-songs.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WOOK = ROOT / "library/wook/index.html"
AUDIO_BASE = "https://wook-in-sheeps-clothing.netlify.app/audio/"

# domain in the org's existing link -> (audio filename, song title, blurb)
# The domain is how each card is located -- stable regardless of card order.
SONGS = {
    "dancesafe.org": ("dancesafe.mp3", "Repetitive Beats",
                       "an original song for DanceSafe"),
    "bunkpolice.com": ("bunkpolice.mp3", "What&rsquo;s in the Baggie",
                        "an original song for The Bunk Police"),
    "zendoproject.org": ("zendo.mp3", "Sit With It",
                          "an original song for The Zendo Project"),
    "firesideproject.org": (None, None, None),   # pending upload
    "maps.org": ("maps.mp3", "Bicycle Day",
                 "an original song for MAPS"),
    "wharfrats.org": ("wharfrats.mp3", "Lowest Bar",
                       "an original song for The Wharf Rats"),
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
    assert "class=\"mixtape\"" not in html.replace(MIXTAPE_CSS, ""), \
        "mixtape CSS already present"
    anchor = ".org-salute{"
    i = html.index(anchor)
    # insert just before the rule containing the anchor, i.e. before its
    # preceding rule boundary -- simplest stable spot: right after the
    # closing brace of .org-links a.alt{...}, which sits just above.
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


def find_card(html, domain):
    """Locate the org-card containing this domain's link, and the exact
    offset to insert into -- the LAST "</div></div>" in that card, which
    closes org-links then org-card. Anchoring on the domain rather than
    card position means a reorder can't misroute a song.

    A card is not just "the domain link plus a fixed tail": DanceSafe and
    Fireside each carry a SECOND link after their primary one (DrugsData,
    the phone number), so the domain's own <a> is not always the last
    thing in org-links. Isolating the whole card first, then taking the
    last double-close within it, handles both the single-link and
    multi-link cards the same way. (org-head's own inner div also ends in
    a "</p></div></div>" double-close, but it always comes earlier in the
    card than org-links' -- the last one in the segment is always right.)
    """
    needle = f'href="https://{domain}"'
    hit = html.find(needle)
    assert hit != -1, f"{domain} link not found anywhere in the page"

    card_starts = [m.start() for m in re.finditer(r'<div class="org-card">', html)]
    card_starts.append(html.index('<p class="org-salute">'))  # end of the last card
    start = max(s for s in card_starts if s <= hit)
    end = min(s for s in card_starts if s > hit)

    close = html.rfind("</div></div>", start, end)
    assert close != -1, f"{domain}: no card-closing pattern found"
    return close + len("</div></div>")


def install_songs(html):
    added, skipped = [], []
    for domain, (filename, title, blurb) in SONGS.items():
        if filename is None:
            skipped.append(domain)
            continue
        at = find_card(html, domain)
        insert = mixtape_html(filename, title, blurb)
        html = html[:at] + insert + html[at:]
        added.append((domain, title))
    return html, added, skipped


def main():
    html = WOOK.read_text(errors="surrogateescape")
    before = len(html)

    html = install_css(html)
    html, added, skipped = install_songs(html)

    WOOK.write_text(html, errors="surrogateescape")
    print(f"wook: {before:,} -> {len(html):,} bytes")
    for domain, title in added:
        print(f"  + {domain:24s} {title}")
    for domain in skipped:
        print(f"  - {domain:24s} no file yet, left as-is")


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Add the five 2026-09 books to the hub's Library shelf.

Cards are inserted before the collection-closer card, numbered XI-XV (the
shelf already skips IX; the closer is comment 9). Cover art is the portrait
jacket built for the shelf's own 1:1.42 book face -- the wide banner used
inside each book would crop to its middle third here.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COVERS = Path("/tmp/claude-0/-home-user/a0ec5e44-ffe5-5bba-b9bd-3cb1a2115366/scratchpad/covers")
HUB = ROOT / "hub/catalogue-redesign.html"

CLOSER = "<!-- 9 · Collection closer -->"

CARDS = [
    dict(n=11, roman="XI", slug="longafter", title="The Long After", glow="#d98466",
         hook="Leaving was supposed to be the ending. For a lot of people, it&#8217;s the middle.",
         desc="Forty-five chapters on what happens after you leave &mdash; control that changes "
              "channel rather than stopping, a body and a nervous system that don&#8217;t know the "
              "danger has technically passed, and rebuilding that runs slower and less straight "
              "than everyone around you expects. Starts at the door and stays for the years after.",
         tags=["45 chapters", "Post-separation"]),
    dict(n=12, roman="XII", slug="silence", title="The Silence", glow="#93a7b8",
         hook="Almost nothing exists for this. This is that.",
         desc="For men in coercive relationships &mdash; controlled, isolated, frightened, "
              "sometimes hurt &mdash; who went looking for something written for them and found "
              "almost nothing. Forty-six chapters that stand alongside the library&#8217;s book "
              "for women rather than instead of it, and say so out loud in chapter three.",
         tags=["46 chapters", "For men"]),
    dict(n=13, roman="XIII", slug="atwill", title="At Will", glow="#8fb2dc",
         hook="You spend more hours here than anywhere else.",
         desc="The same architecture this library maps in a marriage, a church and a feed, "
              "applied to a job. Forty-seven chapters on what makes a workplace coercive rather "
              "than merely difficult, what you are actually owed, and the full sequence of moves "
              "available to you &mdash; not just the one everybody reaches for first.",
         tags=["47 chapters", "Workplace"]),
    dict(n=14, roman="XIV", slug="repair", title="The Repair", glow="#a8474f",
         hook="You recognised yourself in a list. This is what to do about it.",
         desc="Almost every book about coercion is written for the person it was done to. This "
              "one is not. Forty-eight chapters with a single objective: that the people around "
              "you have a different year than the last one &mdash; not that you feel better about "
              "yourself, and not that you are forgiven.",
         tags=["48 chapters", "For the other side"]),
    dict(n=15, roman="XV", slug="slowtake", title="The Slow Take", glow="#b99a3f",
         hook="You noticed something. That noticing is worth trusting.",
         desc="For the son or daughter who has watched a new friend appear too fast, paperwork "
              "nobody explained, a will that changed. Forty-five chapters holding one tension the "
              "whole way through without resolving it by picking a side: an older adult&#8217;s "
              "right to make their own choices, and their right to be free of undue influence.",
         tags=["45 chapters", "Later life"]),
]


def card(c):
    b64 = (COVERS / f"{c['slug']}-jacket.b64").read_text().strip()
    tags = "".join(f"<li>{t}</li>" for t in c["tags"] + ["Free"])
    href = "/" + c["slug"]
    return (
        f'<!-- {c["n"]} · {c["title"]} -->\n'
        f'        <article class="st-vol reveal" style="--glow:{c["glow"]}">'
        f'<div class="st-vol-plate"><div class="st-book"><div class="st-book-face">'
        f'<img src="data:image/jpeg;base64,{b64}" '
        f'alt="Cover &mdash; {c["title"]} by Shae Stovell" loading="lazy" /></div>'
        f'<span class="st-book-spine" aria-hidden="true"></span>'
        f'<span class="st-book-edge" aria-hidden="true"></span>'
        f'<span class="st-book-gloss" aria-hidden="true"></span></div>'
        f'<span class="st-shelf" aria-hidden="true"></span>'
        f'<span class="st-pool" aria-hidden="true"></span></div>'
        f'<div class="st-vol-entry"><div class="st-vol-rule">'
        f'<span class="st-vol-n">{c["roman"]}</span>'
        f'<span class="st-vol-code">VOL. {c["roman"]}</span></div>'
        f'<h3 class="st-vol-title">{c["title"]}</h3>'
        f'<p class="st-vol-hook">{c["hook"]}</p>'
        f'<p class="st-vol-desc">{c["desc"]}</p>'
        f'<ul class="st-vol-tags">{tags}</ul>'
        f'<a class="st-vol-open" href="{href}" target="_blank" rel="noopener">'
        f'Open the book<span class="st-arr" aria-hidden="true">&#8594;</span></a></div>'
        f'<a class="stretch" tabindex="-1" href="{href}" target="_blank" rel="noopener" '
        f'aria-label="Open {c["title"]}"></a></article>\n\n        '
    )


def main():
    html = HUB.read_text(errors="surrogateescape")
    assert html.count(CLOSER) == 1, "closer card marker not found"
    for c in CARDS:
        assert f'>{c["title"]}</h3>' not in html, f'{c["title"]} card already present'
    block = "".join(card(c) for c in CARDS)
    html = html.replace(CLOSER, block + CLOSER, 1)
    HUB.write_text(html, errors="surrogateescape")
    print(f"inserted {len(CARDS)} cards; hub now {len(html)} chars")


if __name__ == "__main__":
    main()

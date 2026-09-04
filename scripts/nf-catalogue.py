#!/usr/bin/env python3
"""Canonical Noble Father catalogue (THE HOUSE nav).

One list, generated here, written into every page that carries the nf-chrome
drawer. Before this existed the same nav had drifted to 11/12/13/15/21 entries
across pages with two different volume counts in the footer. Regenerate rather
than hand-editing any page's <ul class="nf-toc">.

Every destination is a clean path on the main domain -- hub/catalogue-redesign
._redirects proxies each one to its own separately-deployed Netlify site, so
these stay same-origin (which is what lets the ink-veil page transition run).
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://noblefathercreations.com"

ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
         "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX",
         "XXI"]

WORD = {13: "thirteen", 14: "fourteen", 15: "fifteen", 16: "sixteen",
        17: "seventeen", 18: "eighteen", 19: "nineteen", 20: "twenty",
        21: "twenty-one"}

# slug, title, description, dot colour.
# Order is append-only: I-XIII are the order the book pages already carried,
# XIV-XV are the two the hub listed but the books had dropped, XVI-XX are the
# 2026-09-01 additions, XXI is the 2026-09-04 addition (the NFC guide was
# reachable from the hub but missing from THE HOUSE drawer that travels with
# every other page -- someone on a book or craft page had no way to find it).
# Nothing is renumbered when the list grows.
CATALOGUE = [
    ("loop",       "The Loop",                      "The machine that learns you",             "#6E93B5"),
    ("press",      "The Press",                     "Real wax, a voice inside",                "#E8C879"),
    ("portals",    "The Portals",                   "Strontium glow, no battery",              "#7FD9D4"),
    ("shadowroot", "The Root",                      "A shadow work practice",                  "#D9964A"),
    ("scale",      "The Weighing",                  "How to be right about people",            "#9B8FA8"),
    ("faith",      "The Sacred Divide",             "25 traditions, 750 entries",              "#C29A52"),
    ("fractal",    "The Fractal",                   "One pattern runs the world",              "#E5A93C"),
    ("fracture",   "The Fracture",                  "The reading edition",                     "#C9A35B"),
    ("feminine",   "The Sovereign Divine Feminine", "A field guide",                           "#C85F7E"),
    ("children",   "Playground Protectors",         "Shaela&#8217;s guide for brave kids",     "#FFC23D"),
    ("wook",       "The Festie Codex",              "The gate &mdash; attendee&#8217;s cut",   "#D8FF3D"),
    ("playbook",   "The Pattern Decoder",           "349 tactics, decoded",                    "#8A8071"),
    ("music",      "The Music",                     "Free to stream",                          "#C9A24A"),
    ("festival",   "The Festie Bible",              "Twelve guides for the festival world",    "#E8C879"),
    ("resin",      "The Casting",                   "Eco-resin, hand-painted",                 "#7FD6C2"),
    ("longafter",  "The Long After",                "What happens once you&#8217;ve left",     "#D9846A"),
    ("silence",    "The Silence",                   "For men nobody thought to ask",           "#93A7B8"),
    ("atwill",     "At Will",                       "The coercive workplace",                  "#C98A2E"),
    ("repair",     "The Repair",                    "For the person on the other side of it",  "#A8474F"),
    ("slowtake",   "The Slow Take",                 "Coercion in later life",                  "#B99A3F"),
    ("nfc/",       "How to Program NFC Tags",       "139 recipes, iPhone &amp; Android",       "#C9A35B"),
]

FOOT = ("Bound by hand in the study &mdash; %s volumes &amp; counting."
        % WORD[len(CATALOGUE)])


def row(i, entry, here_slug):
    slug, title, desc, dot = entry
    here = slug == here_slug
    cls = "nf-row nf-here" if here else "nf-row"
    href = "#" if here else f"{SITE}/{slug}"
    attrs = ' aria-current="page"' if here else ""
    vol = title + ('<span class="nf-here-dot" aria-hidden="true"></span>' if here else "")
    return (
        f'<li class="{cls}" style="--nf-i:{i}">'
        f'<a href="{href}"{attrs}>'
        f'<span class="nf-dot" style="--va:{dot}" aria-hidden="true"></span>'
        f'<span class="nf-num">{ROMAN[i]}</span>'
        f'<span class="nf-vol">{vol}</span>'
        f'<span class="nf-desc">{desc}</span>'
        f"</a></li>"
    )


def toc(here_slug):
    """The full <ul class="nf-toc"> for a page, with its own row marked."""
    rows = "".join(row(i, e, here_slug) for i, e in enumerate(CATALOGUE))
    return f'<ul class="nf-toc">{rows}</ul>'


TOC_RE = re.compile(r'<ul class="nf-toc">.*?</ul>', re.S)
FOOT_RE = re.compile(
    r'(<div class="nf-panel-foot">)Bound by hand in the study[^<]*(</div>)')


def retoc(html, here_slug):
    """Swap a page's existing catalogue + volume count for the canonical one."""
    assert TOC_RE.search(html), "no <ul class=\"nf-toc\"> found"
    html = TOC_RE.sub(lambda _: toc(here_slug), html, count=1)
    html = FOOT_RE.sub(lambda m: m.group(1) + FOOT + m.group(2), html, count=1)
    return html


if __name__ == "__main__":
    print(f"{len(CATALOGUE)} volumes; foot: {FOOT}")
    print(toc("longafter")[:400] + " ...")

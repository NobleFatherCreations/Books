#!/usr/bin/env python3
"""Patch the 'nh-drawer' cross-project list (loop, scale -- an older, still-
live nav generation distinct from nf-chrome) to include every current
project. Preserves the drawer's own grouped-section design rather than
replacing it with nf-chrome; this component works and matches those two
books' own visual language, it was just never updated with anything added
after it was built.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://noblefathercreations.com"

# (data-nh key, href, title, description) -- grouped, in display order.
GROUPS = [
    ("The books", [
        ("faith",     f"{SITE}/faith",     "The Coercive Control Codex", "Honor the faith &middot; name the machinery"),
        ("loop",      f"{SITE}/loop",      "The Loop", "The machine that learns you"),
        ("scale",     f"{SITE}/scale",     "The Weighing", "How to be right about people"),
        ("fractal",   f"{SITE}/fractal",   "The Fractal", "The architecture, 29 sectors wide"),
        ("fracture",  f"{SITE}/fracture",  "The Fracture", "The wealth transfer &middot; 195 citations"),
        ("feminine",  f"{SITE}/feminine",  "The Sovereign Divine Feminine", "42 chapters &middot; recovery for women"),
        ("children",  f"{SITE}/children",  "Playground Protectors", "For kids &amp; their guardians"),
        ("wook",      f"{SITE}/wook",      "The Festie Codex", "Festival &amp; field harm reduction"),
        ("festival",  f"{SITE}/festival",  "The Festie Bible", "Twelve guides for the festival world"),
        ("longafter", f"{SITE}/longafter", "The Long After", "What happens once you&#8217;ve left"),
        ("silence",   f"{SITE}/silence",   "The Silence", "For men nobody thought to ask"),
        ("atwill",    f"{SITE}/atwill",    "At Will", "The coercive workplace"),
        ("repair",    f"{SITE}/repair",    "The Repair", "For the person on the other side of it"),
        ("slowtake",  f"{SITE}/slowtake",  "The Slow Take", "Coercion in later life"),
    ]),
    ("The living tools", [
        ("shadowroot", f"{SITE}/shadowroot", "The Root", "Shadow work, guided"),
        ("playbook",   f"{SITE}/playbook",   "The Pattern Decoder", "349 tactics &middot; type what happened"),
        ("music",      f"{SITE}/music",      "The Listening Room", "Sorted by what each song is for"),
    ]),
    ("Keeps it free", [
        ("shop",  "https://nfcportals.netlify.app/",   "The Shop", "Wax seals &middot; jewelry &middot; NFC craft"),
        ("press", "https://noblenfcseals.netlify.app/", "The Press", "Real wax, a voice inside"),
        ("resin", f"{SITE}/resin", "The Casting", "Eco-resin, hand-painted"),
    ]),
]

MAIN_ROW = (
    '<div class="nh-g">The hallway</div>\n'
    f'    <a data-nh="main" href="{SITE}/"><b>The main site</b><i>Every book, tool, and door</i></a>\n'
)


def build(here_key):
    out = [MAIN_ROW.rstrip("\n")]
    for label, rows in GROUPS:
        out.append(f'    <div class="nh-g">{label}</div>')
        for key, href, title, desc in rows:
            current = ' aria-current="page"' if key == here_key else ""
            out.append(f'    <a data-nh="{key}" href="{href}"{current}><b>{title}</b><i>{desc}</i></a>')
    return "\n".join(out)


ANCHOR_START = '<div class="nh-g">The hallway</div>'
ANCHOR_END = '<p class="nh-f">'


def retoc(html, here_key):
    i = html.index(ANCHOR_START)
    j = html.index(ANCHOR_END, i)
    new_body = build(here_key) + "\n    "
    return html[:i] + new_body + html[j:]


if __name__ == "__main__":
    for slug in ("loop", "scale"):
        path = ROOT / "library" / slug / "index.html"
        html = path.read_text(errors="surrogateescape")
        before_rows = html.count("data-nh=")
        out = retoc(html, slug)
        after_rows = out.count("data-nh=")
        path.write_text(out, errors="surrogateescape")
        print(f"{slug}: {before_rows} -> {after_rows} entries")

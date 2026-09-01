#!/usr/bin/env python3
"""Expand faith's minimal 'Noble Father Creations' sidebar stub (2 book
links out of 20) to the full catalogue. Pure content addition -- these are
plain <a target="_blank"> links with no drawer/JS component to touch, so
there's no Escape-handling or open/close state to worry about breaking.
Keeps the existing "Main site" first and "TikTok" last.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://noblefathercreations.com"

BOOKS = [
    ("loop",       "The Loop"),
    ("scale",      "The Weighing"),
    ("fractal",    "The Fractal"),
    ("fracture",   "The Fracture"),
    ("feminine",   "The Sovereign Divine Feminine"),
    ("children",   "Playground Protectors"),
    ("wook",       "The Festie Codex"),
    ("festival",   "The Festie Bible"),
    ("shadowroot", "The Root"),
    ("playbook",   "The Pattern Decoder"),
    ("music",      "The Listening Room"),
    ("longafter",  "The Long After"),
    ("silence",    "The Silence"),
    ("atwill",     "At Will"),
    ("repair",     "The Repair"),
    ("slowtake",   "The Slow Take"),
]
CRAFT = [
    ("https://nfcportals.netlify.app/",   "The Shop"),
    ("https://noblenfcseals.netlify.app/", "The Press"),
    (f"{SITE}/resin", "The Casting"),
]

OLD = (
    '<a href="https://noblefathercreations.com/" target="_blank" rel="noopener noreferrer">Main site</a>\n'
    '      <a href="https://noblefathercreations.com/fractal" target="_blank" rel="noopener noreferrer">The Fractal &mdash; 29 other sectors</a>\n'
    '      <a href="https://www.tiktok.com/@noblefathercreatorsource?_r=1&amp;_t=ZT-98KgivKbWN3" target="_blank" rel="noopener noreferrer">TikTok</a>'
)


def link(href, title):
    return f'<a href="{href}" target="_blank" rel="noopener noreferrer">{title}</a>'


def build():
    rows = [link(SITE + "/", "Main site")]
    for slug, title in BOOKS:
        rows.append(link(f"{SITE}/{slug}", title))
    for href, title in CRAFT:
        rows.append(link(href, title))
    rows.append(link(
        "https://www.tiktok.com/@noblefathercreatorsource?_r=1&amp;_t=ZT-98KgivKbWN3",
        "TikTok"))
    return "\n      ".join(rows)


if __name__ == "__main__":
    path = ROOT / "library/faith/index.html"
    html = path.read_text(errors="surrogateescape")
    assert html.count(OLD) == 1, f"stub not found or not unique ({html.count(OLD)})"
    html = html.replace(OLD, build(), 1)
    path.write_text(html, errors="surrogateescape")
    print("faith: sidelinks expanded from 3 to", 1 + len(BOOKS) + len(CRAFT) + 1, "entries")

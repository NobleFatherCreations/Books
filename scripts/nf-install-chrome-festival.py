#!/usr/bin/env python3
"""Install the nf-chrome catalogue drawer onto festival, which never had any
sitewide cross-project navigation (live or repo -- confirmed identical on
that point). Simpler than the 2026-08-31 install for the 5 new books:

- No font substitution needed. Festival already self-hosts Fraunces and
  Space Mono via its own @font-face rules, which are exactly what
  nf-chrome's CSS asks for by name -- the browser resolves font-family:
  'Fraunces' to whatever @font-face already registered that name on the
  page, so there is nothing to override and nothing gets embedded twice.
- No Escape-conflict fix needed. Festival's own Escape handler only closes
  its own chapter-navigation drawer (#fbDrawer); it has no emergency exit
  that a second handler could misfire.

Run against a fetched copy of LIVE (not the repo file) -- see
scripts/covers/README.md's reasoning for why live, not repo, is the
source of truth for pre-existing pages this session didn't build.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import importlib
cat = importlib.import_module("nf-catalogue")

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "library/wook/index.html"


def component_css():
    html = SRC.read_text(errors="surrogateescape")
    css = re.search(r'<style id="nf-chrome-css">(.*?)</style>', html, re.S).group(1)
    css = css.split("/* ---- wook page styles")[0]
    css = re.sub(r'\n\.cover-title\{.*$', "\n", css, flags=re.S)
    return css.rstrip() + "\n"


def component_js():
    html = SRC.read_text(errors="surrogateescape")
    return re.search(r'<script id="nf-chrome-js">(.*?)</script>', html, re.S).group(1)


def component_html(slug):
    return (
        f'<div id="nf-chrome" class="nf-chrome" data-nf-page="{slug}">'
        '<div class="nf-veil" aria-hidden="true"></div>'
        '<button class="nf-seal" type="button" aria-expanded="false" '
        'aria-controls="nf-panel" '
        'aria-label="Open the Catalogue — Noble Father Creations">NF</button>'
        '<div class="nf-scrim" aria-hidden="true"></div>'
        '<nav class="nf-panel" id="nf-panel" aria-label="The Catalogue" aria-hidden="true">'
        '<div class="nf-panel-head"><div>'
        '<div class="nf-eyebrow">Noble Father Creations</div>'
        '<h2 class="nf-panel-title">The Catalogue</h2></div>'
        '<button class="nf-close" type="button" aria-label="Close the Catalogue">'
        "&#10005;</button></div>"
        + cat.toc(slug)
        + f'<div class="nf-panel-foot">{cat.FOOT}</div>'
        "</nav></div>"
    )


def install(html, slug):
    css, js = component_css(), component_js()
    assert html.count("</head>") == 1
    html = html.replace("</head>", f'<style id="nf-chrome-css">{css}</style>\n</head>', 1)

    assert html.count('<div id="app">') == 1
    html = html.replace(
        '<div id="app">',
        component_html(slug) + '\n\n<div id="app">', 1)

    assert html.count("</body>") == 1
    html = html.replace("</body>", f'<script id="nf-chrome-js">{js}</script>\n</body>', 1)
    return html


if __name__ == "__main__":
    live_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2]) if len(sys.argv) > 2 else live_path
    html = live_path.read_text(errors="surrogateescape")
    assert 'id="nf-chrome"' not in html, "already installed"
    had_analytics = "cloudflareinsights" in html
    out = install(html, "festival")
    assert ("cloudflareinsights" in out) == had_analytics, "analytics state changed"
    out_path.write_text(out, errors="surrogateescape")
    print("festival: installed,", len(out), "chars, analytics preserved:", had_analytics)

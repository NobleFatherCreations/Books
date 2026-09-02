#!/usr/bin/env python3
"""Install THE HOUSE catalogue drawer into the NFC guide.

The guide shipped with a `.housetab` reading "Part of the Noble Father
network -- see the rest", pointing at a `#REPLACE-house` placeholder. It
promised the network and delivered a dead anchor. This gives it the real
thing: the same wax-seal button and 20-volume drawer every book carries, so
the guide reaches every other property.

Note the asymmetry, which is deliberate and was asked for: the guide links
OUT to all twenty, but is NOT added to the twenty pages' own drawers. Only
the hub features it. So `nf-catalogue.CATALOGUE` is untouched here -- adding
the guide to it would rewrite the drawer on every page in the catalogue,
which is exactly what we were told not to do.

Three integration fixes the books don't need, because they have no fixed
furniture of their own in that corner:

1. The guide's back-to-top button sits at right:1rem/bottom:1rem -- the same
   spot as the seal. It moves up by the seal's height.
2. The seal (z-index 9950) would float over the recipe sheet and the section
   drawer (z-index 61/70). It hides while either is open.
3. The seal is dropped from print output along with the guide's own chrome.

Run: python3 scripts/nfcguide-chrome.py
"""
import importlib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
cat = importlib.import_module("nf-catalogue")

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "library/wook/index.html"
GUIDE = ROOT / "workshop/nfcguide/index.html"

# The guide is not one of the twenty, so no row is marked "here"; the panel
# says where you are instead of a page silently claiming to be a volume.
GLUE = """
/* ---- NFC guide integration (see scripts/nfcguide-chrome.py) ---- */
.totop{bottom:calc(1rem + 70px)}
.scrim.on ~ #nf-chrome .nf-seal,
.drawer.on ~ #nf-chrome .nf-seal{opacity:0;pointer-events:none;transform:scale(.9)}
#nf-chrome .nf-panel-where{font:400 12.4px/1.5 var(--nf-mono);color:var(--nf-brass);
  letter-spacing:.06em;text-transform:uppercase;padding:0 22px 14px}
@media print{#nf-chrome{display:none!important}}
"""


def component_css():
    html = SRC.read_text(errors="surrogateescape")
    css = re.search(r'<style id="nf-chrome-css">(.*?)</style>', html, re.S).group(1)
    css = css.split("/* ---- wook page styles")[0]
    css = re.sub(r"\n\.cover-title\{.*$", "\n", css, flags=re.S)
    return css.rstrip() + "\n" + GLUE


def component_js():
    html = SRC.read_text(errors="surrogateescape")
    return re.search(r'<script id="nf-chrome-js">(.*?)</script>', html, re.S).group(1)


def component_html():
    return (
        '<div id="nf-chrome" class="nf-chrome" data-nf-page="nfcguide">'
        '<div class="nf-veil" aria-hidden="true"></div>'
        '<button class="nf-seal" type="button" aria-expanded="false" '
        'aria-controls="nf-panel" '
        'aria-label="Open the Catalogue &mdash; Noble Father Creations">NF</button>'
        '<div class="nf-scrim" aria-hidden="true"></div>'
        '<nav class="nf-panel" id="nf-panel" aria-label="The Catalogue" aria-hidden="true">'
        '<div class="nf-panel-head"><div>'
        '<div class="nf-eyebrow">Noble Father Creations</div>'
        '<h2 class="nf-panel-title">The Catalogue</h2></div>'
        '<button class="nf-close" type="button" aria-label="Close the Catalogue">'
        "&#10005;</button></div>"
        '<p class="nf-panel-where">You are in the NFC guide</p>'
        + cat.toc("")
        + f'<div class="nf-panel-foot">{cat.FOOT}</div>'
        "</nav></div>"
    )


def install(html):
    assert 'id="nf-chrome"' not in html, "already installed"

    assert html.count("</head>") == 1
    html = html.replace(
        "</head>", f'<style id="nf-chrome-css">{component_css()}</style>\n</head>', 1)

    # Last thing in the body, after the sheet and the drawer, so the sibling
    # selectors in GLUE can see them.
    assert html.count("</body>") == 1
    html = html.replace(
        "</body>",
        component_html()
        + f'\n<script id="nf-chrome-js">{component_js()}</script>\n</body>', 1)
    return html


if __name__ == "__main__":
    html = GUIDE.read_text(errors="surrogateescape")
    out = install(html)
    rows = out.count('class="nf-row')
    assert rows == 20, f"expected 20 catalogue rows, got {rows}"
    GUIDE.write_text(out, errors="surrogateescape")
    print(f"nfcguide: drawer installed, {rows} volumes, {len(out):,} bytes")

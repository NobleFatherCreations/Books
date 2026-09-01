#!/usr/bin/env python3
"""Install the sitewide nf-chrome drawer (THE HOUSE / the Catalogue) into the
five 2026-09 books.

The component is lifted from library/wook/index.html, which is where it was
first built, with four deliberate changes for these books:

1. --nf-display / --nf-mono point at each book's OWN already-embedded faces
   instead of pulling in another ~480KB of base64 Fraunces per file. The
   drawer keeps the shared brass/wax colour system and motion; only the
   letterforms follow the book they sit in.
2. No .nf-ribbon element. These books already draw their own reading-progress
   bar; a second one would be a duplicate. The engine no-ops without it.
3. Escape is handled in the CAPTURE phase and stops the event when the drawer
   is open. These books bind Escape to an emergency exit that blanks the page,
   so without this, closing the catalogue with Escape would also trigger it.
4. No scroll-reveal (data-nf-reveal is not set) -- the books run their own
   IntersectionObserver fades.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import importlib
cat = importlib.import_module("nf-catalogue")

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "library/wook/index.html"

BOOKS = ["longafter", "silence", "atwill", "repair", "slowtake"]


def component_css():
    html = SRC.read_text(errors="surrogateescape")
    css = re.search(r'<style id="nf-chrome-css">(.*?)</style>', html, re.S).group(1)
    # drop wook's own page styles that ride along at the end of the block
    css = css.split("/* ---- wook page styles")[0]
    css = re.sub(r'\n\.cover-title\{.*$', "\n", css, flags=re.S)
    # the drawer borrows the host book's faces rather than embedding its own
    css = css.replace(
        "  --nf-display:'Fraunces',Georgia,'Times New Roman',serif;\n"
        "  --nf-mono:'Space Mono','IBM Plex Mono',ui-monospace,'SFMono-Regular',monospace;",
        "  --nf-display:var(--serif,Georgia,serif);\n"
        "  --nf-mono:var(--mono,ui-monospace,monospace);")
    assert "--nf-display:var(--serif" in css, "font override did not apply"
    assert ".cover-cta" not in css, "wook page styles still present"
    return css.rstrip() + "\n"


def component_js():
    html = SRC.read_text(errors="surrogateescape")
    js = re.search(r'<script id="nf-chrome-js">(.*?)</script>', html, re.S).group(1)
    old = """  document.addEventListener('keydown',function(e){
    if(e.key==='Escape'&&root.classList.contains('nf-open')){shut();return}"""
    new = """  document.addEventListener('keydown',function(e){
    if(e.key==='Escape'&&root.classList.contains('nf-open')){
      /* This book binds Escape to its emergency exit, which blanks the page.
         Closing the catalogue must not also do that -- capture phase plus
         stopImmediatePropagation keeps Escape from reaching that handler. */
      e.preventDefault();e.stopImmediatePropagation();shut();return}"""
    assert js.count(old) == 1, "escape handler not found to patch"
    js = js.replace(old, new)
    old_end = """      links[next].focus();e.preventDefault();
    }});"""
    new_end = """      links[next].focus();e.preventDefault();e.stopImmediatePropagation();
    }},true);"""
    assert js.count(old_end) == 1, "keydown listener tail not found to patch"
    js = js.replace(old_end, new_end)
    return js


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


def main():
    css, js = component_css(), component_js()
    print(f"component: {len(css)} css chars, {len(js)} js chars")
    for slug in BOOKS:
        path = ROOT / "library" / slug / "index.html"
        html = path.read_text(errors="surrogateescape")
        if 'id="nf-chrome"' in html:
            print(f"  skip (already installed)  {slug}")
            continue
        before = len(html)

        assert html.count("</head>") == 1
        html = html.replace(
            "</head>",
            f'<style id="nf-chrome-css">{css}</style>\n</head>', 1)

        assert html.count('<div id="app"></div>') == 1
        html = html.replace(
            '<div id="app"></div>',
            '<div id="app"></div>\n\n' + component_html(slug), 1)

        assert html.count("</body>") == 1
        html = html.replace(
            "</body>",
            f'<script id="nf-chrome-js">{js}</script>\n</body>', 1)

        path.write_text(html, errors="surrogateescape")
        print(f"  installed  {slug}  ({before} -> {len(html)} bytes)")


if __name__ == "__main__":
    main()

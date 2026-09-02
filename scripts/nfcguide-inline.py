#!/usr/bin/env python3
"""Make the NFC guide a genuine single file, like every book on the site.

The guide arrived as a directory: index.html plus assets/ holding the seal,
the favicon, the touch icon and 17 real app screenshots, all referenced with
relative paths. That is fine on its own domain and cost a real bug on ours.

Proxied at a clean path, a relative reference resolves against whatever the
address bar says. At /nfc/ that is /nfc/assets/... and the proxy catches it.
At /nfc -- no slash, which people type -- it is /assets/..., which on
noblefathercreations.com belongs to The Casting. The page then loads and
looks nearly right with every screenshot silently gone. Two attempts to fix
that in _redirects both failed, and for the same underlying reason: Netlify
strips a trailing slash from a redirect's source, and prefers a real file to
a rewrite, so neither a 301 nor a redirect page can hold the distinction.

The repo's own _redirects file already says why the books never hit this:
"every book is a single self-contained HTML file, so proxying them at /slug
just works." So rather than defend a special case, this removes it. After
this the guide has no relative references at all, the trailing slash stops
mattering, and it is back inside the architecture CLAUDE.md describes --
fully offline-capable, including straight from file://, which is where the
screenshots were most fragile anyway.

Cost: about 780KB of base64, taking the page to roughly 1.1MB. That is
smaller than nine of the fourteen books, and it buys away a whole class of
routing bug.

assets/ still deploys -- og:image needs a real URL for scrapers, robots.txt
and sitemap.xml are fetched by crawlers, and the OFL licences have to ship
with the fonts. Nothing in index.html asks for any of it.

Run: python3 scripts/nfcguide-inline.py
"""
import base64
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GUIDE = ROOT / "workshop/nfcguide"
INDEX = GUIDE / "index.html"


def uri(path):
    mime = {".png": "image/png", ".jpg": "image/jpeg"}[path.suffix]
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def seal_uri(path):
    """The seal, quantised before inlining.

    It ships as a 256x256 full-colour RGBA PNG at 68KB, which is a lot for a
    two-tone mark that is never drawn larger than about 190 CSS pixels. A
    256-colour palette is visually identical here and roughly a quarter of
    the bytes.
    """
    from io import BytesIO

    from PIL import Image

    im = Image.open(path).convert("RGBA")
    # Median cut cannot handle an alpha channel; Fast Octree can, and
    # the mark's transparency is the whole point of the file.
    small = im.quantize(colors=256, method=Image.FASTOCTREE)
    buf = BytesIO()
    small.save(buf, "PNG", optimize=True)
    if len(buf.getvalue()) >= len(path.read_bytes()):
        buf = BytesIO(path.read_bytes())          # quantising didn't help
    print(f"    seal: {path.stat().st_size:,} -> {len(buf.getvalue()):,} bytes")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def main():
    html = INDEX.read_text(errors="surrogateescape")
    before = len(html)

    # 1. The seal appears five times -- top bar, drawer, hero, colophon, print
    #    header. Inlining each <img> separately would carry five copies of the
    #    same payload, which is most of the weight for none of the benefit. So
    #    it goes into one custom property and every use becomes a <span> that
    #    paints it. The four decorative ones were alt="" aria-hidden already;
    #    the hero one carries real alt text and keeps it as role="img" +
    #    aria-label, which is exactly equivalent to a screen reader.
    seal = seal_uri(GUIDE / "assets/logo-seal.png")
    html = html.replace(
        ":root{\n  color-scheme: dark light;",
        ":root{\n  color-scheme: dark light;\n\n"
        "  /* the wax-seal mark, carried once and painted by .sealimg below */\n"
        f"  --seal: url({seal});", 1)
    assert "--seal:" in html, "could not place the seal custom property"

    html = html.replace(
        ".brandlink .seal{width:32px; height:32px; flex:none}",
        ".sealimg{background:var(--seal) center/contain no-repeat; display:block}\n"
        ".brandlink .seal{width:32px; height:32px; flex:none}", 1)

    seals = [
        ('<img class="seal" src="assets/logo-seal.png" alt="" width="32" height="32" aria-hidden="true">',
         '<span class="seal sealimg" aria-hidden="true"></span>'),
        ('<img src="assets/logo-seal.png" alt="" width="28" height="28" aria-hidden="true">',
         '<span class="sealimg" style="width:28px;height:28px;flex:none" aria-hidden="true"></span>'),
        ('<img src="assets/logo-seal.png" width="512" height="512"\n'
         '           alt="Noble Father Creations seal: a gentleman in a top hat holding a cane, inside a wax seal ring.">',
         '<span class="sealimg" role="img"\n'
         '           aria-label="Noble Father Creations seal: a gentleman in a top hat holding a cane, inside a wax seal ring."></span>'),
        ('<img class="seal" src="assets/logo-seal.png" alt="" width="26" height="26" aria-hidden="true">',
         '<span class="seal sealimg" aria-hidden="true"></span>'),
        ('<img src="assets/logo-seal.png" alt="">',
         '<span class="sealimg" aria-hidden="true"></span>'),
    ]
    for old, new in seals:
        assert html.count(old) == 1, f"seal markup not unique: {old[:60]!r}"
        html = html.replace(old, new, 1)

    # Those CSS rules selected `img`; the elements are spans now.
    for old, new in (
        (".hero .sealwrap img", ".hero .sealwrap .sealimg"),
        (".printhead .pm img", ".printhead .pm .sealimg"),
    ):
        assert old in html, f"{old} rule not found"
        html = html.replace(old, new)
    # The hero span has no intrinsic size the way an <img> did.
    html = html.replace(
        ".hero .sealwrap .sealimg{width:100%; height:auto; display:block;",
        ".hero .sealwrap .sealimg{width:100%; aspect-ratio:1; display:block;", 1)
    print("  seal: one copy, painted at all 5 uses")

    # 2. Favicon and touch icon.
    for rel, name in (("icon", "favicon.png"), ("apple-touch-icon", "apple-touch-icon.png")):
        old = re.search(r'<link rel="%s"[^>]*>' % re.escape(rel), html)
        assert old, f"{rel} link not found"
        attrs = ' type="image/png"' if rel == "icon" else ""
        html = html.replace(
            old.group(0),
            f'<link rel="{rel}" href="{uri(GUIDE / "assets" / name)}"{attrs}>', 1)
    print("  favicon + touch icon inlined")

    # 3. The 17 real screenshots. screenFig() builds an <img> whose src is a
    #    path and falls back to a hand-drawn SVG on error; give it a lookup
    #    table instead, and keep the fallback for the ten with no capture.
    shots = sorted(p for p in (GUIDE / "assets/screens").glob("*.png"))
    assert shots, "no screenshots found"
    rows = ",\n ".join(f'"{p.stem}":"{uri(p)}"' for p in shots)
    table = ("/* The real captures, inlined -- see scripts/nfcguide-inline.py.\n"
             "   A name missing from here has no capture and still falls back\n"
             "   to its hand-drawn SVG, exactly as before. */\n"
             "var SHOT_SRC = {\n " + rows + "\n};\n")

    anchor = "var SHOT_SIZE_DEFAULT = [620, 1000];\n"
    assert html.count(anchor) == 1
    html = html.replace(anchor, anchor + "\n" + table, 1)

    old_src = '  img.src = "assets/screens/" + name + ".png";'
    new_src = ('  /* No path: a missing capture must fail synchronously into the\n'
               '     drawing, not fire a network request that cannot succeed. */\n'
               '  if(SHOT_SRC[name]) img.src = SHOT_SRC[name];\n'
               '  else return figWithDrawing(fig, name, caption);')
    assert html.count(old_src) == 1
    html = html.replace(old_src, new_src, 1)
    print(f"  screenshots: {len(shots)} inlined")

    # The helper the branch above needs: build the figure from the drawing.
    helper = """
/* Used when a screen has no real capture. Same figure, drawing instead of
   an <img>, so nothing ever requests a file that is not there. */
function figWithDrawing(fig, name, caption){
  fig.appendChild(svgFor(name));
  if(caption){
    var c = document.createElement("figcaption");
    c.textContent = caption;
    fig.appendChild(c);
  }
  return fig;
}

/* An <img> that quietly becomes the drawing if no real screenshot exists. */"""
    old_comment = '\n/* An <img> that quietly becomes the drawing if no real screenshot exists. */'
    assert html.count(old_comment) == 1
    html = html.replace(old_comment, helper, 1)

    left = re.findall(r'(?:src|href)="(?!data:|https?:|#|mailto:)([^"]+)"', html)
    assert not left, f"still referencing files: {sorted(set(left))}"

    INDEX.write_text(html, errors="surrogateescape")
    print(f"\nindex.html: {before:,} -> {len(html):,} bytes; "
          "no relative references remain")


if __name__ == "__main__":
    sys.exit(main())

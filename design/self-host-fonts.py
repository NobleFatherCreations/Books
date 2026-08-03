#!/usr/bin/env python3
"""Replace a page's Google Fonts CDN <link> tags with self-hosted, embedded
@font-face rules — the fix for the headline finding in ENHANCEMENT-PLAN.md.

Removes every <link rel="preconnect" href="...fonts.g...">  and
<link ... href="https://fonts.googleapis.com/...">, and inserts one <style>
block with base64-embedded @font-face rules for exactly the families the
page's own CSS uses (matched against a per-page manifest below — nothing
extra, no bloat).

Idempotent: does nothing on a page with no Google Fonts links left.

Usage: python3 design/self-host-fonts.py <page> [--apply]
  <page> is one of: catalogue, portals, root, seals, reaction-map,
  sovereign, fractal, fracture, playground, festival, divide
"""
import argparse
import base64
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "tools" / "fonts"

# One @font-face per (family, file). Variable files cover a weight/opsz/ital
# range in one embed; static files are named per weight.
FRAUNCES_VF = FONTS / "fraunces" / "Fraunces[SOFT,WONK,opsz,wght].ttf"
FRAUNCES_VF_IT = FONTS / "fraunces" / "Fraunces-Italic[SOFT,WONK,opsz,wght].ttf"

MANIFESTS = {
    "catalogue": {
        "file": ROOT / "source" / "projects" / "noble-father-catalogue.html",
        "fonts": [
            ("Fraunces", "normal", "1 999", FRAUNCES_VF),
            ("Fraunces", "italic", "1 999", FRAUNCES_VF_IT),
            ("Hanken Grotesk", "normal", "100 900", FONTS / "hankengrotesk" / "HankenGrotesk[wght].ttf"),
            ("Hanken Grotesk", "italic", "100 900", FONTS / "hankengrotesk" / "HankenGrotesk-Italic[wght].ttf"),
            ("Space Mono", "normal", "400", FONTS / "spacemono" / "SpaceMono-Regular.ttf"),
            ("Space Mono", "normal", "700", FONTS / "spacemono" / "SpaceMono-Bold.ttf"),
        ],
    },
    "portals": {
        "file": ROOT / "source" / "projects" / "noble-father-portals.html",
        "fonts": [
            ("Fraunces", "normal", "1 999", FRAUNCES_VF),
            ("Fraunces", "italic", "1 999", FRAUNCES_VF_IT),
            ("Newsreader", "normal", "200 800", FONTS / "newsreader" / "Newsreader[opsz,wght].ttf"),
            ("Newsreader", "italic", "200 800", FONTS / "newsreader" / "Newsreader-Italic[opsz,wght].ttf"),
            ("Jost", "normal", "100 900", FONTS / "jost" / "Jost[wght].ttf"),
            ("IBM Plex Mono", "normal", "400", FONTS / "ibmplexmono" / "IBMPlexMono-Regular.ttf"),
            ("IBM Plex Mono", "normal", "500", FONTS / "ibmplexmono" / "IBMPlexMono-Medium.ttf"),
        ],
    },
    "root": {
        "file": ROOT / "source" / "projects" / "noble-father-root.html",
        "fonts": [
            ("Fraunces", "normal", "1 999", FRAUNCES_VF),
            ("Fraunces", "italic", "1 999", FRAUNCES_VF_IT),
            ("Inter", "normal", "1 999", FONTS / "inter" / "font-files" / "InterVariable.ttf"),
            ("Inter", "italic", "1 999", FONTS / "inter" / "font-files" / "InterVariable-Italic.woff2"),
        ],
    },
    "seals": {
        "file": ROOT / "source" / "projects" / "noble-father-seals.html",
        "fonts": [
            ("Fraunces", "normal", "1 999", FRAUNCES_VF),
            ("Fraunces", "italic", "1 999", FRAUNCES_VF_IT),
            ("Newsreader", "normal", "200 800", FONTS / "newsreader" / "Newsreader[opsz,wght].ttf"),
            ("Newsreader", "italic", "200 800", FONTS / "newsreader" / "Newsreader-Italic[opsz,wght].ttf"),
            ("Jost", "normal", "100 900", FONTS / "jost" / "Jost[wght].ttf"),
            ("IBM Plex Mono", "normal", "400", FONTS / "ibmplexmono" / "IBMPlexMono-Regular.ttf"),
            ("IBM Plex Mono", "normal", "500", FONTS / "ibmplexmono" / "IBMPlexMono-Medium.ttf"),
        ],
    },
    "reaction-map": {
        "file": ROOT / "source" / "projects" / "noble-father-reaction-map.html",
        "fonts": [
            ("Fraunces", "normal", "1 999", FRAUNCES_VF),
            ("Fraunces", "italic", "1 999", FRAUNCES_VF_IT),
            ("Inter", "normal", "1 999", FONTS / "inter" / "font-files" / "InterVariable.ttf"),
            ("Inter", "italic", "1 999", FONTS / "inter" / "font-files" / "InterVariable-Italic.woff2"),
        ],
    },
    "sovereign": {
        "file": ROOT / "source" / "projects" / "noble-father-sovereign.html",
        "fonts": [
            ("Fraunces", "normal", "1 999", FRAUNCES_VF),
            ("Fraunces", "italic", "1 999", FRAUNCES_VF_IT),
            ("Cormorant Garamond", "normal", "1 999", FONTS / "cormorantgaramond" / "CormorantGaramond[wght].ttf"),
            ("Cormorant Garamond", "italic", "1 999", FONTS / "cormorantgaramond" / "CormorantGaramond-Italic[wght].ttf"),
            ("Outfit", "normal", "1 999", FONTS / "outfit" / "Outfit[wght].ttf"),
            ("DM Mono", "normal", "400", FONTS / "dmmono" / "DMMono-Regular.ttf"),
            ("DM Mono", "normal", "500", FONTS / "dmmono" / "DMMono-Medium.ttf"),
        ],
    },
    "fractal": {
        "file": ROOT / "source" / "projects" / "noble-father-fractal.html",
        "fonts": [
            ("Fraunces", "normal", "1 999", FRAUNCES_VF),
            ("Fraunces", "italic", "1 999", FRAUNCES_VF_IT),
            ("Bricolage Grotesque", "normal", "1 999", FONTS / "bricolagegrotesque" / "BricolageGrotesque[opsz,wdth,wght].ttf"),
            ("Spectral", "normal", "400", FONTS / "spectral" / "Spectral-Regular.ttf"),
            ("Spectral", "normal", "500", FONTS / "spectral" / "Spectral-Medium.ttf"),
            ("Spectral", "normal", "600", FONTS / "spectral" / "Spectral-SemiBold.ttf"),
            ("Spectral", "italic", "400", FONTS / "spectral" / "Spectral-Italic.ttf"),
            ("Spectral", "italic", "500", FONTS / "spectral" / "Spectral-MediumItalic.ttf"),
            ("Spectral", "italic", "600", FONTS / "spectral" / "Spectral-SemiBoldItalic.ttf"),
            ("IBM Plex Sans", "normal", "1 999", FONTS / "ibmplexsans" / "IBMPlexSans[wdth,wght].ttf"),
            ("IBM Plex Mono", "normal", "400", FONTS / "ibmplexmono" / "IBMPlexMono-Regular.ttf"),
            ("IBM Plex Mono", "normal", "500", FONTS / "ibmplexmono" / "IBMPlexMono-Medium.ttf"),
            ("IBM Plex Mono", "normal", "600", FONTS / "ibmplexmono" / "IBMPlexMono-SemiBold.ttf"),
        ],
    },
    "fracture": {
        "file": ROOT / "source" / "projects" / "noble-father-fracture.html",
        "fonts": [
            ("Fraunces", "normal", "1 999", FRAUNCES_VF),
            ("Fraunces", "italic", "1 999", FRAUNCES_VF_IT),
            ("Crimson Text", "normal", "400", FONTS / "crimsontext" / "CrimsonText-Regular.ttf"),
            ("Crimson Text", "normal", "600", FONTS / "crimsontext" / "CrimsonText-SemiBold.ttf"),
            ("Crimson Text", "italic", "400", FONTS / "crimsontext" / "CrimsonText-Italic.ttf"),
            ("IBM Plex Mono", "normal", "400", FONTS / "ibmplexmono" / "IBMPlexMono-Regular.ttf"),
            ("IBM Plex Mono", "normal", "500", FONTS / "ibmplexmono" / "IBMPlexMono-Medium.ttf"),
        ],
    },
    "playground": {
        "file": ROOT / "source" / "projects" / "noble-father-playground.html",
        "fonts": [
            ("Fraunces", "normal", "1 999", FRAUNCES_VF),
            ("Fraunces", "italic", "1 999", FRAUNCES_VF_IT),
            ("Bangers", "normal", "400", FONTS / "bangers" / "Bangers-Regular.ttf"),
            ("Baloo 2", "normal", "1 999", FONTS / "baloo2" / "Baloo2[wght].ttf"),
            ("Nunito", "normal", "1 999", FONTS / "nunito" / "Nunito[wght].ttf"),
            ("Nunito", "italic", "1 999", FONTS / "nunito" / "Nunito-Italic[wght].ttf"),
            ("Patrick Hand", "normal", "400", FONTS / "patrickhand" / "PatrickHand-Regular.ttf"),
        ],
    },
    "festival": {
        "file": ROOT / "source" / "projects" / "noble-father-festival.html",
        "fonts": [
            ("Fraunces", "normal", "1 999", FRAUNCES_VF),
            ("Fraunces", "italic", "1 999", FRAUNCES_VF_IT),
            ("Anton", "normal", "400", FONTS / "anton" / "Anton-Regular.ttf"),
            ("Bungee", "normal", "400", FONTS / "bungee" / "Bungee-Regular.ttf"),
            ("Bungee Shade", "normal", "400", FONTS / "bungeeshade" / "BungeeShade-Regular.ttf"),
            ("Shrikhand", "normal", "400", FONTS / "shrikhand" / "Shrikhand-Regular.ttf"),
            ("Permanent Marker", "normal", "400", FONTS / "permanentmarker" / "PermanentMarker-Regular.ttf"),
            ("Bricolage Grotesque", "normal", "1 999", FONTS / "bricolagegrotesque" / "BricolageGrotesque[opsz,wdth,wght].ttf"),
            ("Space Mono", "normal", "400", FONTS / "spacemono" / "SpaceMono-Regular.ttf"),
            ("Space Mono", "normal", "700", FONTS / "spacemono" / "SpaceMono-Bold.ttf"),
            ("Caveat", "normal", "1 999", FONTS / "caveat" / "Caveat[wght].ttf"),
        ],
    },
    "divide": {
        "file": ROOT / "source" / "projects" / "noble-father-divide.html",
        "fonts": [
            ("Fraunces", "normal", "1 999", FRAUNCES_VF),
            ("Fraunces", "italic", "1 999", FRAUNCES_VF_IT),
        ],
    },
}

LINK_RE = re.compile(r'<link\s+[^>]*(?:fonts\.googleapis\.com|fonts\.gstatic\.com)[^>]*>\s*\n?')


def build_style_block(fonts):
    rules = []
    for family, style, weight, path in fonts:
        if not path.exists():
            sys.exit(f"missing font file: {path}")
        b64 = base64.b64encode(path.read_bytes()).decode("ascii")
        is_variable = " " in weight
        if path.suffix == ".woff2":
            mime, base_fmt = "font/woff2", "woff2"
        else:
            mime, base_fmt = "font/ttf", "truetype"
        fmt = f"{base_fmt}-variations" if is_variable else base_fmt
        rules.append(
            f"  @font-face {{ font-family:'{family}'; font-style:{style}; font-weight:{weight}; "
            f"font-display:swap; src:url(data:{mime};base64,{b64}) format('{fmt}'); }}"
        )
    return "<style id=\"nfc-self-hosted-fonts\">\n" + "\n".join(rules) + "\n</style>\n"


def process(page, apply):
    m = MANIFESTS[page]
    path = m["file"]
    text = path.read_text(encoding="utf-8")

    links = LINK_RE.findall(text)
    if not links:
        print(f"{page}: no Google Fonts links found — already done or nothing to do")
        return

    new_text = LINK_RE.sub("", text)
    style_block = build_style_block(m["fonts"])
    head_end = new_text.find("</head>")
    if head_end == -1:
        sys.exit("no </head> found")
    new_text = new_text[:head_end] + style_block + new_text[head_end:]

    removed_bytes = len(text) - len(LINK_RE.sub("", text))
    added_bytes = len(style_block)
    print(f"{page}: removed {len(links)} CDN link(s) ({removed_bytes}B), "
          f"embedded {len(m['fonts'])} font files ({added_bytes:,}B self-hosted)")

    if apply:
        path.write_text(new_text, encoding="utf-8")
        print(f"  -> written to {path}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("page", choices=list(MANIFESTS))
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    process(args.page, args.apply)

#!/usr/bin/env python3
"""Homepage v18 "The Press" (owner, 2026-11-21). Replaces build_hub.py, which reshaped the old v17 page.

Sources (edit these, never the output):
  design/hub-v18/data.json   books, shelves, situations, tools, songs, Portals, links
  design/hub-v18/home.css    styles (tokens in docs/hub-redesign/DESIGN-STATE.md)
  design/hub-v18/home.js     behaviour
  design/hub-v18/img/        Portals photos, the NFC guide picture
  content/covers/signed/     the book covers (signature versions)
  tools/vendor/gsap-3.13.0/  GSAP core + ScrollTrigger, pasted inline (no outside requests)
Output: hub/catalogue-redesign.html, hub/media/v18/*.webp, hub/f/*.woff2

Full chain (sites.json hub.buildCommand):
  build_home.py && build_site.py && visit-counter.py hub/catalogue-redesign.html hub/topics.html
"""
import html, json, re, subprocess, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "design/hub-v18"
HUB = ROOT / "hub"
MEDIA = HUB / "media/v18"
FONTS = HUB / "f"
E = lambda s: html.escape(str(s), quote=True)


GSAP_PLUGINS = ["ScrollTrigger", "SplitText", "DrawSVGPlugin"]
ROOTS_SVG = '<svg class="roots" viewBox="0 0 200 120" aria-hidden="true"><path d="M100 0 C100 30 96 48 84 66 S60 96 40 118"/><path d="M100 0 C102 34 110 52 124 70 S150 98 168 116"/><path d="M98 26 C86 40 70 46 52 50"/><path d="M103 40 C118 52 134 56 152 58"/><path d="M90 62 C84 80 86 98 92 116"/><path d="M118 66 C124 84 122 100 116 118"/></svg>'

def webp(src, name, width, quality=80):
    """Resize to a width and save as WebP under /media/v18; returns (url, w, h)."""
    MEDIA.mkdir(parents=True, exist_ok=True)
    out = MEDIA / f"{name}-{width}.webp"
    im = Image.open(src).convert("RGB")
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    if not out.exists() or out.stat().st_mtime < Path(src).stat().st_mtime:
        im.save(out, "WEBP", quality=quality, method=6)
    return f"/media/v18/{out.name}", im.width, im.height


def subset_fonts(text):
    """Subset the two families to the characters the page uses."""
    FONTS.mkdir(exist_ok=True)
    chars = "".join(sorted(set(text + " .,;:!?'\"“”‘’—–-()&/0123456789$@%+…")))
    jobs = [("tools/fonts/gloock/Gloock-Regular.ttf", "gloock-400-normal.woff2"),
            ("tools/fonts/public-sans/PublicSans[wght].ttf", "public-sans-100-900-normal.woff2")]
    for src, out in jobs:
        subprocess.run([sys.executable, "-m", "fontTools.subset", str(ROOT / src), f"--text={chars}",
                        "--flavor=woff2", f"--output-file={FONTS / out}", "--layout-features=kern,liga,calt,onum,pnum,tnum"],
                       check=True)
    return ("@font-face{font-family:'Gloock';font-style:normal;font-weight:400;font-display:swap;src:url(/f/gloock-400-normal.woff2) format('woff2')}"
            "@font-face{font-family:'Public Sans';font-style:normal;font-weight:100 900;font-display:swap;src:url(/f/public-sans-100-900-normal.woff2) format('woff2')}")


ICONS = {
    # a wax seal: scalloped rim, pressed monogram
    "seal": '<svg class="ico" viewBox="0 0 64 64" aria-hidden="true"><path fill="currentColor" opacity=".9" d="M32 4l4.6 3.4 5.6-.9 2.6 5 5.3 2-.3 5.7 3.9 4.1-2.4 5.2 2.4 5.2-3.9 4.1.3 5.7-5.3 2-2.6 5-5.6-.9L32 60l-4.6-3.4-5.6.9-2.6-5-5.3-2 .3-5.7-3.9-4.1 2.4-5.2-2.4-5.2 3.9-4.1-.3-5.7 5.3-2 2.6-5 5.6.9z"/><circle cx="32" cy="32" r="16" fill="none" stroke="#07090a" stroke-width="2" opacity=".55"/><path d="M25 40V24l14 16V24" fill="none" stroke="#07090a" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" opacity=".7"/></svg>',
    # a casting: a pour into a mould, a figure rising
    "cast": '<svg class="ico" viewBox="0 0 64 64" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M14 8h18l-4 8H18z"/><path d="M23 16v10"/><path d="M10 30h44v22a4 4 0 0 1-4 4H14a4 4 0 0 1-4-4z"/><path d="M26 56V44a6 6 0 0 1 12 0v12"/><circle cx="32" cy="38" r="0.5" fill="currentColor"/><path d="M23 26c0 2 1 3 0 4"/></svg>',
}
PLAY = '<svg viewBox="0 0 14 14" aria-hidden="true"><path d="M3 1l10 6-10 6z"/></svg>'
KNOB = '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M7 5l-4 5 4 5M13 5l4 5-4 5"/></svg>'


def main():
    d = json.loads((SRC / "data.json").read_text())
    man = {t["file"]: t for t in json.loads((ROOT / "instruments/music/MANIFEST.json").read_text())["tracks"]}

    # images
    for b in d["books"]:
        folder = "original" if b.get("src") == "original" else "signed"
        src = ROOT / "content/covers" / folder / b["cover"]
        b["img"], b["w"], b["h"] = webp(src, b["slug"], 480)
        b["imgLg"] = webp(src, b["slug"], 760)[0]
    for t in d["tools"]:
        t["img"], t["w"], t["h"] = webp(ROOT / "content/covers/signed" / t["cover"], t["slug"], 480)
    for i, p in enumerate(d["portals"]):
        p["dayImg"] = webp(SRC / "img" / p["day"], f"portal-{i}-day", 720)[0]
        p["nightImg"] = webp(SRC / "img" / p["night"], f"portal-{i}-night", 720)[0]
    d["guide"]["src"] = webp(SRC / "img" / d["guide"]["img"], "nfc-guide", 640)[0]
    for t in d["music"]["tracks"]:
        t["dur"] = round(man[t["file"]]["duration"])
    books = {b["slug"]: b for b in d["books"]}
    fmt = lambda s: f"{s // 60}:{s % 60:02d}"

    def book_li(b, eager=False):
        return (f'<li><a class="bk" href="/{b["slug"]}"><span class="cov" style="aspect-ratio:{b["w"]}/{b["h"]}"><img src="{b["img"]}" width="{b["w"]}" height="{b["h"]}" '
                f'alt="" loading="{"eager" if eager else "lazy"}" decoding="async"><span class="glint" aria-hidden="true"></span></span><b>{E(b["title"])}</b><small>{E(b["line"])}</small></a></li>')

    shelves = "".join(
        f'<div class="shelf" id="shelf-{s["id"]}"><div><h3>{E(s["name"])}</h3><svg class="rule" viewBox="0 0 200 10" preserveAspectRatio="none" aria-hidden="true"><path d="M2 6 C40 3 80 8 120 5 S180 3 198 6"/></svg><p class="why">{E(s["why"])}</p></div>'
        f'<ul class="books" aria-label="{E(s["name"])}">' + "".join(book_li(b) for b in d["books"] if b["shelf"] == s["id"]) + "</ul></div>"
        for s in d["shelves"])
    bigger = "".join(book_li(b) for b in d["books"] if b["shelf"] == "bigger")
    spines = "".join(f'<i style="background-image:url({b["img"]})"></i>' for b in d["books"] if b["shelf"] == "bigger")
    chips = "".join(f'<button class="chip" type="button" data-s="{s["id"]}" aria-pressed="false">{E(s["label"])}</button>' for s in d["situations"])
    tools = "".join(f'<a class="tool tool-{t["slug"]}" href="/{t["slug"]}"><span class="tool-art"><img src="{t["img"]}" width="{t["w"]}" height="{t["h"]}" alt="" loading="lazy" decoding="async">' + ('<span class="scan" aria-hidden="true"></span>' if t["slug"] == "playbook" else ROOTS_SVG if t["slug"] == "shadowroot" else '') + '</span><span class="glare" aria-hidden="true"></span>'
                    f'<span><h3>{E(t["title"])}</h3><p class="muted">{E(t["line"])}</p></span></a>' for t in d["tools"])
    live = d["music"]["live"]
    music_link = '<a class="more" href="/music">All 176 songs</a>' if live else '<p class="more is-off">176 songs, back soon</p>'
    tracks = "".join(
        f'<li class="trk" data-src="/music/audio/{E(t["file"])}" data-title="{E(t["title"])}">'
        + (f'<button class="play" type="button" aria-label="Play {E(t["title"])}">{PLAY}</button>' if live else f'<span class="n" aria-hidden="true">{i + 1}</span>')
        + f'<span><span class="t">{E(t["title"])}</span><span class="s">{E(t["shelf"])}</span></span><time>{fmt(t["dur"])}</time>'
        + '<span class="bar" aria-hidden="true"><i></i></span></li>' for i, t in enumerate(d["music"]["tracks"]))
    pairs = "".join(
        f'<li><figure class="portal" data-name="{E(p["name"])}"><img class="day" src="{p["dayImg"]}" width="720" height="720" alt="{E(p["name"])} pendant in daylight" loading="lazy" decoding="async">'
        f'<img class="night" src="{p["nightImg"]}" width="720" height="720" alt="" loading="lazy" decoding="async">'
        f'<span class="lamp" aria-hidden="true"></span></figure>'
        f'<p class="legend"><span>{E(p["name"])}</span><button class="charge" type="button">'
        f'<svg viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="24" r="20" class="track"/><circle cx="24" cy="24" r="20" class="fill" pathLength="1"/></svg>'
        f'<span class="label">Hold to charge</span><span class="vh"> {E(p["name"])}</span></button></p><p class="vh portal-status" role="status"></p></li>'
        for p in d["portals"])
    making = "".join(f'<div class="mk card soon">{ICONS[m["icon"]]}<span><b>{E(m["title"])}</b><small>{E(m["line"])}</small></span></div>' for m in d["making"])
    g = d["guide"]
    pay = "".join(f'<a class="btn" href="{E(p["url"])}" target="_blank" rel="noopener">{E(p["name"])} {E(p["handle"])}</a>' for p in d["support"])
    ribbon_titles = [books[s]["title"] for s in ("longafter", "silence", "atwill", "repair", "loop", "scale", "slowtake", "feminine")]
    ribbon = "".join(f"<span>{E(t)}</span>" for t in ribbon_titles) * 2
    first = books["longafter"]

    client = {"books": [{k: b[k] for k in ("slug", "title", "line", "img", "imgLg", "w", "h")} for b in d["books"]],
              "tools": [{k: t[k] for k in ("slug", "title", "line", "img")} for t in d["tools"]],
              "situations": d["situations"]}
    nav = [("books", "#library", "Books"), ("tools", "#tools", "Tools"), ("music", "#music", "Music"), ("art", "#art", "Art"), ("nfc", "#guide", "NFC guide")]
    navhtml = "".join(f'<a href="{h}" data-nav="{k}">{t}</a>' for k, h, t in nav)
    sheet_links = "".join(f'<a href="{h}">{t}</a>' for k, h, t in nav) + '<a href="/topics">Topics A to Z</a><a href="#support">Support the work</a>'

    body = f"""<a class="skip" href="#main">Skip to the books</a>
<header class="top"><div class="wrap"><a class="brand" href="/">Noble Father</a>
<nav class="nav" aria-label="Sections"><span class="pill" aria-hidden="true"></span>{navhtml}</nav>
<div class="top-actions"><button class="ico" id="sound-btn" type="button" aria-label="Sound" aria-pressed="false" title="Sound is off until you turn it on"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M11 4.702a.705.705 0 0 0-1.203-.498L6.413 7.587A1.4 1.4 0 0 1 5.416 8H3a1 1 0 0 0-1 1v6a1 1 0 0 0 1 1h2.416a1.4 1.4 0 0 1 .997.413l3.383 3.384A.705.705 0 0 0 11 19.298z"/><g class="on"><path d="M16 9a5 5 0 0 1 0 6"/><path d="M19.364 18.364a9 9 0 0 0 0-12.728"/></g><g class="off"><line x1="22" x2="16" y1="9" y2="15"/><line x1="16" x2="22" y1="9" y2="15"/></g></svg><span class="ico-w">Sound</span></button><button class="ico" id="still-btn" type="button" aria-label="Still" aria-pressed="false" title="Stop every moving effect and sound"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="10" x2="10" y1="15" y2="9"/><line x1="14" x2="14" y1="15" y2="9"/></svg><span class="ico-w">Still</span></button><button class="menu-btn" id="menu-btn" type="button" aria-label="Menu" aria-expanded="false" aria-controls="sheet"><svg viewBox="0 0 24 24" aria-hidden="true"><line x1="4" x2="20" y1="7" y2="7"/><line x1="4" x2="20" y1="12" y2="12"/><line x1="4" x2="20" y1="17" y2="17"/></svg><span class="menu-w">Menu</span></button>
<a class="leave" href="https://www.google.com/search?q=weather" data-leave title="Leave this site now (or press Esc twice)">Leave now</a></div></div><span class="progress" aria-hidden="true"><i></i></span></header>
<div class="sheet" id="sheet" hidden><div class="sheet-panel" role="dialog" aria-modal="true" aria-label="Menu">{sheet_links}<div class="sheet-row"><button class="btn sheet-sound" id="sheet-still" type="button" aria-pressed="false"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="10" x2="10" y1="15" y2="9"/><line x1="14" x2="14" y1="15" y2="9"/></svg>Still</button><button class="btn sheet-sound" id="sheet-sound" type="button" aria-pressed="false"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M11 4.702a.705.705 0 0 0-1.203-.498L6.413 7.587A1.4 1.4 0 0 1 5.416 8H3a1 1 0 0 0-1 1v6a1 1 0 0 0 1 1h2.416a1.4 1.4 0 0 1 .997.413l3.383 3.384A.705.705 0 0 0 11 19.298z"/><g class="on"><path d="M16 9a5 5 0 0 1 0 6"/><path d="M19.364 18.364a9 9 0 0 0 0-12.728"/></g><g class="off"><line x1="22" x2="16" y1="9" y2="15"/><line x1="16" x2="22" y1="9" y2="15"/></g></svg>Sound</button></div><button class="btn sheet-close" id="sheet-close" type="button">Close</button></div></div>
<div class="ribbon" aria-hidden="true"><div class="ribbon-track">{ribbon}</div></div>
<main id="main">
<section class="hero" id="start-here" data-nav="books"><span class="anchor" id="top"></span><div class="wrap"><div>
<h1><span class="ln"><span>Free books for</span></span> <span class="ln"><span>the moment you</span></span> <span class="ln"><span>start to wonder.</span></span></h1>
<p class="lede">Field guides on manipulation and control, written plainly by Shae Stovell. Free to read, nothing to sign up for.</p>
<p class="ask" id="ask">What's happening?</p>
<div class="chips" role="group" aria-labelledby="ask">{chips}</div>
<p class="vh" id="result-status" role="status"></p>
<div class="result" id="result" role="region" aria-labelledby="result-title"><div><div class="result-inner">
<div class="result-head"><h2 id="result-title">Your starting point</h2><button class="redo" id="redo" type="button">Change answer</button><p class="muted" id="result-note"></p></div>
<div class="result-grid" id="result-grid"></div></div></div></div></div>
<figure class="stage"><div class="halo"></div><span class="floor" aria-hidden="true"></span><div class="book-in"><div class="book-tilt"><div class="book3d"><span class="sp"></span><div class="inside" aria-hidden="true"><span class="page-k">Chapter one</span><span class="lines"></span><span class="page-sig"></span></div><span class="riffle" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></span><div class="face" id="hero-face"><div class="leaf" id="hero-leaf"><span class="sheen" aria-hidden="true"></span><img id="hero-cover" src="{first["imgLg"]}" width="760" height="1133" alt="{E(first["title"])}, cover" fetchpriority="high" decoding="async"></div></div><span class="pg"></span></div></div></div>
<figcaption>Your answer turns the book.</figcaption></figure></div></section>



<section class="sec" id="library" data-nav="books"><div class="wrap">
<div class="sec-head"><h2>The library</h2><p class="muted">Fourteen free books. Find the shelf that sounds like your life; each one opens straight to the first chapter.</p></div>
{shelves}
<div class="door" id="door"><span class="leafs" aria-hidden="true"><span class="door-l"></span><span class="door-r"></span><span class="burst"></span></span><span class="seam" aria-hidden="true"></span><div class="door-head"><div class="spines" aria-hidden="true">{spines}</div>
<div><h3>{E(d["bigger"]["name"])}</h3><p class="muted">{E(d["bigger"]["why"])}</p></div>
<button class="btn hold" id="door-btn" type="button" aria-expanded="false" aria-controls="door-body"><svg class="ring" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="10"/></svg><span class="lbl">Open the bigger picture</span></button></div>
<div class="door-body" id="door-body" inert><div><ul class="books" aria-label="The bigger picture">{bigger}</ul></div></div></div>
</div></section>

<section class="sec" id="tools" data-nav="tools" style="padding-top:0"><span class="anchor" id="instruments"></span><div class="wrap">
<div class="sec-head"><h2>Free tools</h2><p class="muted">For when you need a name for something, or a few quiet minutes.</p></div>
<div class="tools">{tools}</div></div></section>

<section class="sec music" id="music" data-nav="music"><div class="wrap"><div class="music-head"><div><h2>The Listening Room</h2><p class="muted" style="margin-top:16px">Songs written and produced by Shae: call-outs, love songs, festival anthems.</p></div>
{music_link}</div>
<ul class="tracks">{tracks}</ul><p class="note" id="music-note" role="status">{"" if live else E(d["music"]["note"])}</p></div></section>

<section class="threshold" id="art" data-nav="art" data-night="1"><span class="anchor" id="workshop"></span><span class="anchor" id="manifesto"></span><span class="burn" aria-hidden="true"></span><span class="stars" aria-hidden="true"></span><div class="wrap">
<h2><span class="lit">Worn in the light.</span> <span class="glowline">Alive in the dark.</span></h2>
<p class="muted">The Workshop: hand-poured resin pendants with a strontium glow and a chip inside that plays a song, a message or a memory when a phone touches it.</p></div></section>

<section class="workshop" data-nav="art" data-night="1"><div class="wrap">
<h3>The Portals</h3><p class="muted" style="margin-top:8px">A portfolio of finished pieces. Strontium drinks in light and gives it back in the dark: press and hold a pendant to charge it, then let go. Every photo shows the real glow: blue or green, depending on the pigment. The shop opens soon.</p>
<ul class="pairs portals">{pairs}</ul>
<a class="more" href="/portals" style="margin-top:24px">See every Portal</a>
<div class="wk-row" id="guide" data-nav="nfc">
<a class="card guide" href="{E(g["url"])}"><img src="{g["src"]}" width="600" height="852" alt="" loading="lazy" decoding="async"><span><span class="tag">Free guide</span><h3>{E(g["title"])}</h3><p class="muted">{E(g["line"])}</p><span class="btn">Read the guide</span></span></a>
<div class="making"><p>In the making</p>{making}</div></div></div></section>

<section class="support" id="support" data-night="1"><div class="wrap"><div><h2 style="font-size:clamp(32px,2vw + 18px,48px)">Every book is free, and always will be.</h2>
<p class="muted" style="margin-top:16px">If one found you at the right moment, you can leave something in the hat. Pay what you like, or nothing at all; it keeps the next one free for the next person.</p></div>
<div class="pay">{pay}</div></div><span class="anchor" id="maker"></span></section>
</main>
<footer><div class="wrap"><div><h2>Noble Father Creations</h2><p>Books, tools and art by</p><img class="sig" src="/media/v18/signature.png" width="220" height="64" alt="Shae Stovell" loading="lazy"></div>
<div><h2>Books</h2><ul>{"".join(f'<li><a href="#shelf-{s["id"]}">{E(s["name"])}</a></li>' for s in d["shelves"])}<li><a href="#door">The bigger picture</a></li></ul></div>
<div><h2>Tools and music</h2><ul><li><a href="/playbook">The Pattern Decoder</a></li><li><a href="/shadowroot">The Root</a></li><li><a href="/music">The Listening Room</a></li><li><a href="/topics">Topics A to Z</a></li></ul></div>
<div><h2>Art</h2><ul><li><a href="/portals">The Portals</a></li><li><a href="/nfc/">NFC guide</a></li><li><a href="{E(d["tiktok"])}" target="_blank" rel="noopener">TikTok</a></li><li><a href="#support">Support the work</a></li></ul></div>
<p class="legal">Every book is free to share under <a href="https://creativecommons.org/licenses/by-nc-nd/4.0/">CC BY-NC-ND 4.0</a>: credit the author, no selling, no changes.</p></div></footer>"""

    # signature as a light PNG for the footer
    sig = Image.open(ROOT / "tools/brand/signature-shae-stovell.png").convert("L")
    rgba = Image.new("RGBA", sig.size, (236, 226, 207, 0)); rgba.putalpha(Image.eval(sig, lambda v: 255 - v))
    rgba = rgba.crop(rgba.getbbox()); rgba.thumbnail((440, 160)); MEDIA.mkdir(parents=True, exist_ok=True); rgba.save(MEDIA / "signature.png", optimize=True)
    ink = Image.new("RGBA", rgba.size, (58, 44, 26, 0)); ink.putalpha(rgba.getchannel("A")); ink.save(MEDIA / "signature-ink.png", optimize=True)

    text = re.sub(r"<[^>]+>", " ", body) + json.dumps(client, ensure_ascii=False) + "Close the bigger picture Pause That song could not start"
    fontcss = subset_fonts(html.unescape(text))
    # GSAP core + only the plugins the page uses (all vendored in tools/vendor/gsap-3.13.0, free under the GSAP standard licence)
    gs = "\n".join((ROOT / f"tools/vendor/gsap-3.13.0/{p}.min.js").read_text() for p in ["gsap"] + GSAP_PLUGINS)
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#16110d"><meta name="color-scheme" content="dark">
<title>Noble Father Creations</title>
<meta name="description" content="Free books and tools by Shae Stovell.">
{(SRC / "favicon.html").read_text()}
<link rel="preload" href="/f/gloock-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{first["imgLg"]}" as="image">
<style>{fontcss}{(SRC / "home.css").read_text()}</style>
</head><body>
{body}
<script type="application/json" id="home-data">{json.dumps(client, ensure_ascii=False).replace("</", "<\\/")}</script>
<script>{gs}</script>
<script>{(SRC / "home.js").read_text()}</script>
</body></html>
"""
    (HUB / "catalogue-redesign.html").write_text(page)
    print(f"hub/catalogue-redesign.html {len(page.encode()) // 1024} KB; media {sum(f.stat().st_size for f in MEDIA.iterdir()) // 1024} KB")


if __name__ == "__main__":
    main()

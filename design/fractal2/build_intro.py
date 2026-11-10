#!/usr/bin/env python3
"""Fractal² intro builder.   python3 design/fractal2/build_intro.py

Reads  content/fractal2/intro-final.md   (the text; edit that file to change any word on the page)
       content/fractal2/sectors.json     (the thirty sectors)
       content/fractal/ent/build/sector.json (combo names and tactic stages, for the roster figure)
       design/fractal2/tokens.css, intro.css, intro.js
Writes library/fractal2/site/fractal2.html   (one self-contained page; fonts and audio are same-site files)
       library/fractal2/site/fractal2/_a/f/  (fonts)

Markers understood in the text (all are HTML comments, invisible in any Markdown viewer):
  <!--scene:NAME-->                      which visualization is on the stage from here on
  <!--steps--> ... <!--/steps-->         lines that step through the next figure
  <!--fig:NAME hold=N | text-->          the figure itself, N screens tall, with its text equivalent
  <!--more:URL | label-->                connector link (the build refuses a URL whose page does not exist)
  <!--cta:URL | label-->, <!--cta2:...-->  closing buttons
"""
import datetime
import html
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SITE = ROOT / "library/fractal2/site"
ORIGIN = "https://noblefathercreations.com"
BASE = json.loads((ROOT / "content/fractal2/sectors.json").read_text())["base"]
ASSETS = ROOT / "design/decoder-v10/assets"
VERSION = ("v1", "2026-11-10", "First edition of the introduction.")
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]


def esc(s):
    return html.escape(s, quote=True)


def page_exists(url):
    """Connector links are checked against files in this repo. Never guess a link."""
    u = url.split("#")[0].strip("/")
    if u.startswith("fractal2"):
        return True          # built by this pipeline; the link check in verify covers it
    parts = u.split("/")
    base = ROOT / "library" / parts[0]
    if len(parts) == 1:
        return (base / "index.html").exists()
    return (base / ("/".join(parts[1:]) + ".html")).exists()


def inline(s):
    s = esc(s)
    s = re.sub(r"\[([^\]]+)\]\((/[^)\s]*)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", s)
    return s


def parse(md):
    """-> list of tokens: (kind, payload)."""
    md = re.sub(r"\A<!--.*?\n-->\s*", "", md, flags=re.S)    # leading build note (ends at a line that is only "-->")
    toks, buf, in_steps, steps = [], [], False, []

    def flush():
        if buf:
            toks.append(("p", [l for l in buf]))
            buf.clear()

    for raw in md.split("\n"):
        line = raw.rstrip()
        m = re.match(r"<!--(\w+)(?::(.*?))?-->$", line.strip())
        if m:
            flush()
            k, v = m.group(1), (m.group(2) or "").strip()
            if k == "steps":
                in_steps, steps = True, []
            elif k == "/steps" or (k == "" and v == ""):
                pass
            elif k == "scene":
                toks.append(("scene", v))
            elif k == "fig":
                head, _, alt = v.partition("|")
                bits = head.split()
                hold = next((float(b.split("=")[1]) for b in bits[1:] if b.startswith("hold=")), None)
                toks.append(("fig", {"name": bits[0], "hold": hold, "alt": alt.strip(), "steps": steps}))
                steps = []
            elif k in ("more", "cta", "cta2"):
                url, _, label = v.partition("|")
                url, label = url.strip(), label.strip()
                assert page_exists(url), "connector link to a page that does not exist: " + url
                toks.append((k, (url, label)))
            continue
        if line.strip() == "<!--/steps-->":
            flush()
            in_steps = False
            continue
        if in_steps:
            if line.strip():
                steps.append(line.strip())
            continue
        if not line.strip():
            flush()
        elif line.startswith("# "):
            flush(); toks.append(("h1", line[2:]))
        elif line.startswith("### "):
            flush(); toks.append(("h3", line[4:]))
        elif line.startswith("## "):
            flush(); toks.append(("h2", line[3:]))
        elif line.strip() == "---":
            flush()
        else:
            buf.append(line.strip())
    flush()
    return toks


def build_body(toks):
    out, toc, n = [], [], 0
    units = []
    scene_open = sec_open = False
    hero_done = False
    figs = []

    def close_scene():
        nonlocal scene_open
        if scene_open:
            out.append("</div>")
            scene_open = False

    def nid(kind="p", text=""):
        nonlocal n
        n += 1
        units.append({"n": n, "kind": kind, "text": re.sub(r"\s+", " ", re.sub(r"[*]", "", text)).strip()})
        return n

    i = 0
    while i < len(toks):
        k, v = toks[i]
        if k == "h1":
            # hero: h1, tagline (h3), optional scene marker, lens note (p)
            tag = lens = ""
            scene = "signal"
            j = i + 1
            while j < len(toks) and toks[j][0] in ("h3", "scene", "p") and not (toks[j][0] == "p" and lens):
                if toks[j][0] == "h3":
                    tag = toks[j][1]
                elif toks[j][0] == "scene":
                    scene = toks[j][1]
                else:
                    lens = " ".join(toks[j][1])
                j += 1
            out.append(f'''<section class="hero sn" data-scene="{scene}" id="top">
  <div class="hero-in">
    <p class="kicker">Noble Father Creations · Shae Stovell</p>
    <h1 class="title">{inline(v).replace("²", '<sup>2</sup>')}</h1>
    <p class="tagline" data-n="{nid('title', v + '. ' + tag)}">{inline(tag)}</p>
    <p class="lens" data-n="{nid('lens', lens)}">{inline(lens)}</p>
  </div>
  <p class="cue" aria-hidden="true"><span>Scroll</span><i></i></p>
</section>''')
            i = j
            continue
        if k == "h2":
            close_scene()
            if sec_open:
                out.append("</section>")
            m = re.match(r"([IVX]+)\.\s+(.*)", v)
            rn, title = (m.group(1), m.group(2)) if m else ("", v)
            sid = "part-" + rn.lower() if rn else re.sub(r"[^a-z]+", "-", v.lower())
            toc.append((sid, rn, title))
            out.append(f'<section class="ch" id="{sid}" aria-labelledby="{sid}-h">')
            out.append(f'<div class="col"><p class="rn" aria-hidden="true">{rn}</p><h2 id="{sid}-h" data-n="{nid('h2', 'Part ' + rn + '. ' + title)}"><span class="vh">Part {rn}: </span>{inline(title)}</h2></div>')
            sec_open = True
        elif k == "scene":
            close_scene()
            out.append(f'<div class="sn" data-scene="{v}">')
            scene_open = True
        elif k == "h3":
            out.append(f'<div class="col"><h3 data-n="{nid('h3', v)}">{inline(v)}</h3></div>')
        elif k == "p":
            lines = v
            cls = ""
            txt = "<br>".join(inline(l) for l in lines)
            whole = " ".join(lines)
            if re.fullmatch(r"\*[^*].*\*", whole) and len(whole) < 60:
                cls = ' class="aside"'
            elif re.fullmatch(r"\*\*[^*]+\*\*", whole):
                cls = ' class="strike"'
            elif len(lines) > 1:
                cls = ' class="lines"'
            kind = "short" if cls in (' class="aside"', ' class="strike"') else "p"
            out.append(f'<div class="col"><p{cls} data-n="{nid(kind, " / ".join(lines) if len(lines) > 1 else whole)}">{txt}</p></div>')
        elif k == "fig":
            f = v
            steps = "".join(f'<li class="step" data-n="{nid("step", s)}"><p>{inline(s)}</p></li>' for s in f["steps"])
            hold = f["hold"] if f["hold"] else (1.0 if f["steps"] else 1.6)
            figs.append(f["name"])
            out.append(f'''<figure class="fig{' has-steps' if f['steps'] else ''}" data-fig="{f['name']}" style="--hold:{hold};--n:{len(f['steps'])}" aria-label="Figure: {esc(f['name'])}">
  {'<ol class="steps">' + steps + '</ol>' if steps else '<div class="fig-space" aria-hidden="true"></div>'}
  <figcaption class="alt"><span class="alt-k">What the figure shows</span> {inline(f['alt'])}</figcaption>
</figure>''')
        elif k == "more":
            out.append(f'<div class="col"><p class="more"><a href="{v[0]}">{esc(v[1])} <span aria-hidden="true">→</span></a></p></div>')
        elif k in ("cta", "cta2"):
            out.append(f'<div class="col"><p class="{k}"><a href="{v[0]}">{esc(v[1])} <span aria-hidden="true">→</span></a></p></div>')
        i += 1
    close_scene()
    if sec_open:
        out.append("</section>")
    return "\n".join(out), toc, units, figs


def data_blob():
    reg = json.loads((ROOT / "content/fractal2/sectors.json").read_text())
    sec = json.loads((ROOT / "content/fractal/ent/build/sector.json").read_text())
    stage_no = {t["single_no"]: t["stage_no"] for t in sec["tactics"]}
    combos = [[c["name"], [stage_no.get(t["single_no"], 0) if t.get("single_no") else 0 for t in c["tactics"]]] for c in sec["combos"]]
    counts = [sum(1 for t in sec["tactics"] if t["stage"] == s) for s in sec["stages"]]
    return {"art": BASE + "/_a/img/the-fractal.webp",
            "tactics": [[t["name"] for t in sec["tactics"] if t["stage"] == s] for s in sec["stages"]],
            "sectors": [[s["name"], s["relationship"], 1 if s["built"] else 0] for s in reg["sectors"]],
            "combos": combos, "stageCounts": counts, "techCounts": [2, 2, 4, 5, 6, 7, 2, 2],
            "stages": ["Idealize", "Hook", "Devalue", "Confuse", "Isolate", "Extract", "Discard", "Replace"],
            "originals": ["Chosen", "Covenant", "Inherent worth", "Truth", "Community", "Abundance", "Unfailing presence", "Irreplaceable worth"]}


ROMAN_WORD = {"I": "one", "II": "two", "III": "three", "IV": "four", "V": "five", "VI": "six", "VII": "seven", "VIII": "eight", "IX": "nine", "X": "ten", "XI": "eleven", "XII": "twelve"}
PAUSE = {"title": 3.0, "lens": 2.5, "h2": 2.5, "h3": 2.0, "short": 1.6, "step": 1.2, "p": 0.9}
WPM = 138.0


def spoken(u, edits):
    """The spoken edit of one unit: the page text with the few changes a voice needs."""
    t = u["text"]
    if t in edits:
        return edits[t]
    t = t.replace("Fractal²", "Fractal Squared").replace("A&R", "A and R").replace(" / ", " ")
    m = re.match(r"Part ([IVX]+)\. (.*)", t)
    if u["kind"] == "h2" and m:
        t = "Part %s. %s." % (ROMAN_WORD[m.group(1)], m.group(2))
    if u["kind"] in ("h3",) and not t.endswith((".", "?", "!")):
        t += "."
    return t


def narration(units):
    """Writes the narration script (for the owner to read aloud) and a placeholder timing file for the player."""
    ep = ROOT / "content/fractal2/narration-edits.json"
    edits = json.loads(ep.read_text()) if ep.exists() else {}
    t, sync, takes, cur = 2.0, [], [], None
    for u in units:
        sp = spoken(u, edits)
        if u["kind"] in ("title", "h2"):
            cur = {"title": sp.rstrip("."), "lines": [], "start": t, "words": 0}
            takes.append(cur)
            if u["kind"] == "h2":
                t += 2.0
        sync.append({"n": u["n"], "t": round(t, 2)})
        w = len(sp.split())
        dur = w / WPM * 60.0
        cur["lines"].append((u, sp))
        cur["words"] += w
        t += dur + PAUSE[u["kind"]]
        cur["end"] = t
    total = t + 2.0
    mark = {"title": "[pause 3]", "lens": "[pause 2] [breath]", "h2": "[pause 2] [breath]", "h3": "[pause 2]", "short": "[pause 1.5]", "step": "[pause 1]", "p": "[breath]"}
    fmt = lambda x: "%d:%02d" % (x // 60, x % 60)
    out = ["# Fractal² — narration script", "",
           "> Generated from `content/fractal2/intro-final.md` by `design/fractal2/build_intro.py`. Do not edit this file by hand: change the page text, or add a spoken wording to `content/fractal2/narration-edits.json` (page sentence → how to say it), and rebuild.", "",
           "**How to read the marks.** `[breath]` a natural breath, about one second. `[pause 2]` hold that many seconds of silence. A line on its own is said on its own. The small numbers at the left are for the editor (they tie each line to the page); do not read them.", "",
           "**Pace.** About %d words a minute: slower than conversation. Whole piece about %s at that pace. Record one take per part (file names are given in the recording guide). If you stumble, pause, and start that sentence again; do not restart the part." % (WPM, fmt(total)), "",
           "**Section VI is yours.** Say it plainly, at your own speed. Nothing in it is to be added to or performed.", ""]
    for i, tk in enumerate(takes):
        out += ["---", "", "## Take %02d — %s" % (i, tk["title"]), "", "*About %s · %d words · starts at %s in the full piece*" % (fmt(tk["end"] - tk["start"]), tk["words"], fmt(tk["start"])), ""]
        for u, sp in tk["lines"]:
            if u["kind"] == "h2":
                out += ["`%03d` **%s** %s" % (u["n"], sp, mark["h2"]), ""]
            elif u["kind"] == "h3":
                out += ["`%03d` **%s** %s" % (u["n"], sp, mark["h3"]), ""]
            else:
                out += ["`%03d` %s %s" % (u["n"], sp, mark[u["kind"]]), ""]
    (ROOT / "content/fractal2/narration-script.md").write_text("\n".join(out))
    au = SITE / BASE.strip("/") / "_a/au"
    au.mkdir(parents=True, exist_ok=True)
    real = au / "intro.sync.recorded.json"       # written by design/fractal2/sync_audio.py once the owner's recording exists
    if not real.exists():
        (au / "intro.sync.json").write_text(json.dumps({"placeholder": True, "duration": round(total, 1),
            "note": "Placeholder: a silent timing track. The author's recorded voice will replace it. Press play to be led through the page at reading pace.",
            "units": sync}, separators=(",", ":")))
        (au / "PLACEHOLDER-DURATION.txt").write_text("%.1f\n" % total)
    return total


def main():
    md = (ROOT / "content/fractal2/intro-final.md").read_text()
    body, toc, units, figs = build_body(parse(md))
    n = len(units)
    narration(units)
    fdir = BASE + "/_a/f/"
    css = (HERE / "tokens.css").read_text().replace("/F/", fdir) + "\n" + (HERE / "intro.css").read_text()
    js = (HERE / "intro.js").read_text()
    house = (ASSETS / "house.html").read_text()
    beacon = (ASSETS / "beacon.html").read_text()
    title = "Fractal²: The Closer You Look, the More There Is"
    desc = "The full map of manipulation: more than 300 tactics per sector at three levels, and the combinations where the order is the weapon. Start here."
    url = ORIGIN + BASE
    today = datetime.date.today().isoformat()
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": title, "description": desc, "url": url, "inLanguage": "en",
         "datePublished": VERSION[1], "dateModified": today,
         "author": {"@type": "Person", "name": "Shae Stovell", "url": ORIGIN},
         "publisher": {"@type": "Organization", "name": "Noble Father Creations", "url": ORIGIN},
         "isPartOf": {"@type": "CreativeWorkSeries", "name": "Fractal²", "url": url},
         "about": ["manipulation tactics", "coercive control", "the narcissistic abuse cycle", "recovery"]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Noble Father Creations", "item": ORIGIN + "/"},
            {"@type": "ListItem", "position": 2, "name": "Fractal²", "item": url}]}]}
    toc_html = "".join(f'<li><a href="#{sid}"><span class="num">{rn}</span>{esc(t)}</a></li>' for sid, rn, t in toc)
    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article"><meta property="og:site_name" content="Fractal² · Noble Father Creations">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{ORIGIN}{BASE}/_a/og/intro.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="preload" href="{fdir}newsreader.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{fdir}hanken.woff2" as="font" type="font/woff2" crossorigin>
<meta name="theme-color" content="#0B0C0F" media="(prefers-color-scheme: dark)"><meta name="theme-color" content="#F5F0E6" media="(prefers-color-scheme: light)">
<script>document.documentElement.className+=' js'</script>
<style>{css}</style>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False).replace("</", "<\\/")}</script>
</head>
<body class="intro">
<a class="skip" href="#main">Skip to the text</a>
<canvas id="stage" aria-hidden="true"></canvas>
<div id="labels" aria-hidden="true"></div>
<header class="bar" id="bar">
  <a class="mark" href="{BASE}">Fractal<sup>2</sup><span class="vh"> (Fractal squared): top of the page</span></a>
  <div class="bar-r">
    <button class="bb" id="listen" type="button" aria-expanded="false" aria-controls="player"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 14v-2a9 9 0 0 1 18 0v2"/><path d="M21 15v2a2 2 0 0 1-2 2h-1v-6h3zM3 15v2a2 2 0 0 0 2 2h1v-6H3z"/></svg><span>Listen</span></button>
    <button class="bb" id="toc-b" type="button" aria-expanded="false" aria-controls="toc"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h10"/></svg><span>Contents</span></button>
    <button class="bb leave" id="leave" type="button" aria-label="Leave this site now"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 4h5v16h-5M10 8l-4 4 4 4M6 12h10"/></svg><span>Leave</span></button>
  </div>
  <div class="prog" aria-hidden="true"><i id="prog"></i></div>
</header>
<nav class="toc" id="toc" aria-label="Contents" hidden>
  <ol>{toc_html}</ol>
  <p class="toc-x"><a href="{BASE}/entertainment">The first sector: Entertainment &amp; Music <span aria-hidden="true">→</span></a></p>
</nav>
<main id="main">
{body}
<section class="updates" id="updates" aria-labelledby="up-h"><div class="col">
  <h2 id="up-h" class="kicker">Updates</h2>
  <p class="ui"><span class="badge">{VERSION[0]} — {VERSION[1]}</span> {esc(VERSION[2])}</p>
  <p class="ui fine">Fractal² · Shae Stovell · Noble Father Creations. Free to read and share with credit. Press Escape twice, or Leave, to exit quickly.</p>
</div></section>
</main>
<section class="player" id="player" aria-label="Narration" hidden>
  <div class="pl-in">
    <button class="pl-b" id="pl-play" type="button" aria-label="Play narration"><svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true"><path class="i-play" d="M7 4.5v15l13-7.5z" fill="currentColor"/><path class="i-pause" d="M7 5h4v14H7zM14 5h4v14h-4z" fill="currentColor"/></svg></button>
    <div class="pl-mid">
      <p class="pl-cap" id="pl-cap" aria-live="off">Narration in the author's voice. Press play to begin; the page follows the voice.</p>
      <div class="pl-row"><input id="pl-seek" type="range" min="0" max="1000" value="0" aria-label="Position in the narration"><span class="pl-time num" id="pl-time">0:00</span></div>
    </div>
    <button class="pl-b sm" id="pl-rate" type="button" title="Playback speed">1×</button>
    <button class="pl-b sm" id="pl-mute" type="button" aria-pressed="false" aria-label="Mute"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M11 5 6 9H3v6h3l5 4z"/><path class="i-on" d="M15.5 8.5a5 5 0 0 1 0 7M18.5 5.5a9 9 0 0 1 0 13"/><path class="i-off" d="m16 9 5 6M21 9l-5 6"/></svg></button>
    <button class="pl-b sm" id="pl-follow" type="button" aria-pressed="true" aria-label="Page follows the voice">Follow</button>
    <button class="pl-b sm" id="pl-close" type="button" aria-label="Close narration"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg></button>
  </div>
  <audio id="pl-audio" preload="none" data-src="{BASE}/_a/au/intro.mp3" data-sync="{BASE}/_a/au/intro.sync.json"></audio>
</section>
<script>window.F2={json.dumps(data_blob(), ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")};</script>
<script>{js}</script>
{house}
{beacon}
</body>
</html>
"""
    assert "{{" not in page and "#REPLACE" not in page
    SITE.mkdir(parents=True, exist_ok=True)
    (SITE / (BASE.strip("/") + ".html")).write_text(page)
    f = SITE / BASE.strip("/") / "_a/f"
    f.mkdir(parents=True, exist_ok=True)
    for p in (HERE / "fonts").iterdir():
        shutil.copy2(p, f / p.name)
    img = SITE / BASE.strip("/") / "_a/img"
    img.mkdir(parents=True, exist_ok=True)
    for p in (HERE / "art").glob("*.webp"):
        shutil.copy2(p, img / p.name)
    words = len(re.sub(r"<[^>]+>", " ", body).split())
    print("built %s  (%d KB, %d narration units, %d figures, ~%d words)" % (SITE / (BASE.strip('/') + '.html'), len(page) // 1024, n, len(figs), words))


if __name__ == "__main__":
    main()

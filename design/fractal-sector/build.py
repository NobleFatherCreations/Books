#!/usr/bin/env python3
"""Fractal sector site generator.  python3 design/fractal-sector/build.py ent [--target preview|production]

Reads  content/fractal/<sector>/build/sector.json  (from ingest.py)
Writes library/fractal/sectors/<sector>/site/fractal/<slug>/...   (the publish dir is .../site)

Pages (flat .html, served extensionless by Netlify; every link absolute):
  /fractal/<slug>                  sector home: cover, three doors, top 10, stages, families
  /fractal/<slug>/stage-<stage>    8 stage pages, every tactic with its own anchor
  /fractal/<slug>/family-<cat>     10 category pages
  /fractal/<slug>/<combo-slug>     one page per combo (no internal C-numbers anywhere a reader sees)
  /fractal/<slug>/standards        sector standards
  /fractal/<slug>/a-z              every tactic and combo, with a filter
  sitemap.xml, og/ cards (rendered by og.mjs), f/ fonts

Words are the author's. This file only lays them out: production cues and the Credibility Audit are left
out, credibility tags become labels, fill-in blanks stay visible. Publish gate: --target production builds
only combos whose review_state is in PUBLISH_STATES; links to held-back combos render as plain text.
"""
import datetime
import html
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
ORIGIN = "https://noblefathercreations.com"
ASSETS = ROOT / "design/decoder-v10/assets"   # house drawer + beacon, shared with the rest of the site

# One-line owner decision: which review states may go to production.
PUBLISH_STATES = {"preview": {"unreviewed", "expert_reviewed", "sources_verified"},
                  "production": {"unreviewed", "expert_reviewed", "sources_verified"}}

STAGE_INFO = {
    "IDEALIZE": "The approach: attention, warmth and promise arrive before any terms do.",
    "HOOK": "The binding: small commitments, debts and identities that make leaving costly.",
    "DEVALUE": "The turn: worth is chipped away so approval has to be earned back.",
    "CONFUSE": "The fog: facts, memory and meaning are made unreliable.",
    "ISOLATE": "The narrowing: outside voices and allies are cut away.",
    "CONTROL": "The system: rules, money, information and surveillance do the steering.",
    "DISCARD": "The exit on their terms: dropping, erasing or punishing the person.",
    "REPLACE": "The reset: someone new is brought in and the story is rewritten.",
}
LEVELS = [("Individual", "ind", "Individual"), ("Institutional", "inst", "Institutional"),
          ("Civilizational", "civ", "Civilizational")]
TAG_KIND = {"REQUIRES SUBJECT-MATTER REVIEW": "review", "VERIFIED SOURCE NEEDED": "source",
            "HISTORICAL EXAMPLE TO VERIFY": "source", "LEGAL CLAIM — JURISDICTION-SPECIFIC": "legal",
            "LEGAL CLAIM": "legal", "COMMON INDUSTRY PATTERN": "pattern", "HYPOTHETICAL COMPOSITE": "composite"}
TAG_LABEL = {  # (label, explanation); review/source labels follow the combo's review_state
    "legal": ("Varies by place", "Law and contract practice differ by country and state. Get local advice."),
    "pattern": ("Common pattern", "Widely reported in the industry; not a claim about any one company."),
    "composite": ("Composite", "A made-up example built from common situations. No real person is described."),
    ("review", "unreviewed"): ("Awaiting expert review", "This point has not yet been checked by an industry expert."),
    ("review", "expert_reviewed"): ("Expert reviewed", "An industry expert has checked this point."),
    ("review", "sources_verified"): ("Expert reviewed", "An industry expert has checked this point."),
    ("source", "unreviewed"): ("Source being checked", "A source for this point is still being verified."),
    ("source", "expert_reviewed"): ("Source being checked", "A source for this point is still being verified."),
    ("source", "sources_verified"): ("Source verified", "The source for this point has been verified."),
}
STATE_NOTE = {
    "unreviewed": "Written with care, not yet checked by an industry expert. Labels in the text show which points are still being checked.",
    "expert_reviewed": "Checked by an industry expert. Labels show any sources still being verified.",
    "sources_verified": "Checked by an industry expert, with its sources verified.",
}
# Section order and headings a reader sees (author headings are kept where they read well).
COMBO_ORDER = [
    ("Cold Open", "The scene"), ("The Name", None), ("Definition", "What it is"),
    ("Verbal Breakdown", "The tactics, in order"), ("Why This Order", "Why this order"),
    ("LEVELS", "One pattern, three altitudes"),
    ("Observable Indicators", "What you might notice"), ("Recognition Cue Cards", "Spot it"),
    ("False-Positive Check — Specific", "Before you read too much into it"),
    ("Evidence To Preserve — Additions", "What to keep"), ("Chain Breakers", "What breaks the chain"),
    ("Escalation Triggers — Specific", "When to get help, and where"),
    ("Safer Response Language", "Words you could use"), ("Reflection", None),
]


BRACKET = re.compile(r"\[([^\[\]\n]{1,120})\]")


def esc(s):
    return html.escape(str(s if s is not None else ""), quote=True)


def slugify(s):
    s = s.lower().replace("&", " and ").replace("’", "").replace("'", "")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def clip(s, n=158):
    s = re.sub(r"\s+", " ", s).strip()
    return s if len(s) <= n else s[:n].rsplit(" ", 1)[0].rstrip(",;:") + "…"


def plain(s):
    """Derived snippets (cards, descriptions, structured data): no cues, no credibility tags."""
    s = BRACKET.sub(lambda m: "" if m.group(1) in ("SPEAK", "HARD CUT") or all(p.strip() in TAG_KIND for p in m.group(1).split(";")) else m.group(0), s or "")
    return re.sub(r"\s{2,}", " ", s.replace("**", "")).strip()


def first_sentence(s):
    s = plain(s)
    m = re.match(r"(.+?[.!?])(\s|$)", s.strip())
    return m.group(1) if m else s


class Ctx:
    def __init__(self, data, target):
        self.d, self.target = data, target
        self.base = "/fractal/" + data["slug"]
        self.allowed = PUBLISH_STATES[target]
        self.combos = {c["combo_id"]: c for c in data["combos"]}
        self.live = {k for k, c in self.combos.items() if c["review_state"] in self.allowed}
        self.tactics = {t["single_no"]: t for t in data["tactics"]}
        self.cats = {c["category_id"]: c for c in data["categories"]}
        self.date = datetime.date.today().isoformat()
        self.house = (ASSETS / "house.html").read_text()
        self.beacon = (ASSETS / "beacon.html").read_text()
        xl = ROOT / "content/fractal/_crosslinks.json"     # combo_id -> [{sector, title, url}] once sectors exist
        self.cross = json.loads(xl.read_text()) if xl.exists() else {}

    def u(self, path=""):
        return self.base + ("/" + path if path else "")

    def combo_link(self, cid, label=None):
        c = self.combos.get(cid)
        if not c:
            return esc(label or cid)
        if cid not in self.live:
            return '<span class="held">%s</span>' % esc(label or c["name"])
        return '<a href="%s">%s</a>' % (self.u(c["slug"]), esc(label or c["name"]))

    def tactic_href(self, no):
        t = self.tactics[no]
        return "%s#%s" % (self.u("stage-" + t["stage_slug"]), t["anchor"])


# ---------- inline + block markdown (tiny, only what the scripts use) ----------


def inline(s, state="unreviewed"):
    out, last = [], 0
    for m in BRACKET.finditer(s):
        out.append(esc(s[last:m.start()]))
        tok = m.group(1)
        parts = [p.strip() for p in tok.split(";")]
        if tok in ("SPEAK", "HARD CUT"):
            pass
        elif all(p in TAG_KIND for p in parts):
            for p in parts:
                k = TAG_KIND[p]
                lab, tip = TAG_LABEL.get((k, state)) or TAG_LABEL[k]
                out.append('<span class="tg tg-%s" title="%s">%s</span>' % (k, esc(tip), esc(lab)))
        else:
            out.append('<span class="slot">[%s]</span>' % esc(tok))
        last = m.end()
    out.append(esc(s[last:]))
    h = "".join(out)
    h = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", h)
    h = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", h)
    return re.sub(r"\s{2,}", " ", h).strip()


def blocks(md):
    return [b.strip("\n") for b in re.split(r"\n\s*\n", md.strip()) if b.strip()]


def md(text, state="unreviewed", first_cls=None):
    out = []
    for i, b in enumerate(blocks(text)):
        lines = b.split("\n")
        if all(re.match(r"\s*[-*]\s+", l) or not l.strip() for l in lines if l.strip()) and re.match(r"\s*[-*]\s", lines[0]):
            out.append("<ul>%s</ul>" % "".join("<li>%s</li>" % inline(re.sub(r"^\s*[-*]\s+", "", l), state)
                                               for l in lines if l.strip()))
        elif re.match(r"\s*\d+\.\s", lines[0]):
            items, cur = [], []
            for l in lines:
                if re.match(r"\s*\d+\.\s", l):
                    if cur:
                        items.append(" ".join(cur))
                    cur = [re.sub(r"^\s*\d+\.\s+", "", l)]
                else:
                    cur.append(l.strip())
            items.append(" ".join(cur))
            out.append("<ol>%s</ol>" % "".join("<li>%s</li>" % inline(x, state) for x in items))
        elif all(l.startswith(">") for l in lines):
            out.append('<blockquote class="caution">%s</blockquote>' %
                       inline(" ".join(re.sub(r"^>\s?", "", l) for l in lines), state))
        else:
            cls = ' class="%s"' % first_cls if (first_cls and i == 0) else ""
            out.append("<p%s>%s</p>" % (cls, "<br>".join(inline(l, state) for l in lines)))
    return "\n".join(out)


def src(inner, cls=""):
    """Author words live inside data-src, so verify.mjs can count them against ingest's reader_words."""
    return '<div class="prose%s" data-src>%s</div>' % (" " + cls if cls else "", inner)


# ---------- page frame ----------
def css():
    return (HERE / "style.css").read_text()


ICON = {
    "leave": '<path d="M14 4h5v16h-5M10 8l-4 4 4 4M6 12h10"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "alert": '<path d="M12 9v4M12 17h.01"/><path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/>',
}


def svg(name, size=18):
    return ('<svg width="%d" height="%d" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % (size, size, ICON[name]))


def frame(cx, *, title, desc, path, crumbs, body, ld, og, progress=False, cls=""):
    url = ORIGIN + cx.u(path)
    crumb_html = " <span aria-hidden=\"true\">/</span> ".join(
        '<a href="%s">%s</a>' % (u, esc(n)) if u else '<span aria-current="page">%s</span>' % esc(n) for n, u in crumbs)
    ld_all = {"@context": "https://schema.org", "@graph": ld + [{
        "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": ORIGIN + (u or cx.u(path))}
            for i, (n, u) in enumerate(crumbs)]}]}
    f = cx.u("f/")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article"><meta property="og:site_name" content="The Fractal · Noble Father Creations">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{ORIGIN}{cx.u('og/' + og + '.png')}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0A0B11">
<link rel="preload" href="{f}spectral-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{f}bricolage.woff2" as="font" type="font/woff2" crossorigin>
<style>{css().replace('/F/', f)}</style>
<script type="application/ld+json">{json.dumps(ld_all, ensure_ascii=False).replace("</", "<\\/")}</script>
</head>
<body class="{cls}">
<a class="skip" href="#main">Skip to the text</a>
{'<div class="progress" aria-hidden="true"><span></span></div>' if progress else ''}
<header class="top">
  <a class="mark" href="/fractal"><span class="mk-a">The Fractal</span><span class="mk-b">{esc(cx.d['title'])}</span></a>
  <button class="leave" id="leave" type="button" aria-label="Leave this site now">{svg('leave')}<span>Leave</span></button>
</header>
<nav class="crumbs" aria-label="You are here">{crumb_html}</nav>
<main id="main">
{body}
</main>
<footer class="foot">
  <nav aria-label="In this sector"><a href="{cx.u()}">{esc(cx.d['title'])} home</a><a href="{cx.u('a-z')}">A to Z</a><a href="{cx.u('standards')}">Sector standards</a><a href="/fractal">All sectors</a><a href="/playbook">Pattern Decoder</a></nav>
  <p>Recognition, not a verdict, legal advice or therapy. Patterns describe situations, not people; intent always needs more evidence. If anyone is in danger, contact emergency services. If a child is involved, contact child protection. Press Escape twice or Leave to exit quickly.</p>
  <p class="fine">The Fractal · Shae Stovell · Noble Father Creations · updated {cx.date}</p>
</footer>
<script>{(HERE / 'site.js').read_text()}</script>
{cx.house}
{cx.beacon}
</body>
</html>
"""


def article_ld(cx, name, desc, path, kind="Article", extra=None):
    o = {"@type": kind, "headline": name, "name": name, "description": desc, "url": ORIGIN + cx.u(path),
         "inLanguage": "en", "dateModified": cx.date,
         "author": {"@type": "Person", "name": "Shae Stovell"},
         "publisher": {"@type": "Organization", "name": "Noble Father Creations", "url": ORIGIN},
         "isPartOf": {"@type": "CollectionPage", "name": "The Fractal: " + cx.d["title"], "url": ORIGIN + cx.u()}}
    o.update(extra or {})
    return o


# ---------- pages ----------
def stage_no(cx, stage):
    return cx.d["stages"].index(stage) + 1


def home(cx):
    d = cx.d
    stages = "".join(
        '<li><a class="stg" style="--c:var(--s%d)" href="%s"><span class="n">%02d</span><b>%s</b><small>%s</small>'
        '<span class="ct">%d tactics</span></a></li>' % (
            i + 1, cx.u("stage-" + s.lower()), i + 1, s.title(), esc(STAGE_INFO[s]),
            sum(t["stage"] == s for t in d["tactics"]))
        for i, s in enumerate(d["stages"]))
    fams = "".join(
        '<li><a class="fam" href="%s"><span class="n">%02d</span><b>%s</b><span class="ct">%d patterns</span></a></li>' % (
            cx.u("family-" + c["slug"]), i + 1, esc(re.sub(r"\s*Composites?$", "", c["name"])),
            sum(1 for k in c["combos"] if k in cx.live))
        for i, c in enumerate(d["categories"]))
    top = "".join(
        '<li><span class="rk">%02d</span><div><h3>%s</h3><p>%s</p></div></li>' % (
            t["rank"], cx.combo_link(t["combo_id"], t["name"]), esc(plain(t["why_it_ranks"])))
        for t in d["top10"])
    body = f"""
<section class="cover">
  <p class="kicker">The Fractal · a sector</p>
  <h1>{esc(d['title'])}</h1>
  <p class="lede">How manipulation and control show up in music and entertainment: {len(d['tactics'])} tactics at three altitudes, and {len(cx.live)} patterns where they combine. Recognition and safe routing, written for artists, writers, crew and the people who care about them.</p>
  {f'<p class="book">From the sector book <cite>{esc(d["book_title"])}</cite></p>' if d.get('book_title') else ''}
</section>
<nav class="doors" aria-label="Three ways in">
  <a class="door" href="#start"><span class="dn">01</span><b>Start with the ten that matter most</b><small>The patterns most likely to cost people money, credit, years or safety here.</small></a>
  <a class="door" href="#stages"><span class="dn">02</span><b>Learn the eight stages</b><small>Every tactic, from first approach to replacement, at three altitudes.</small></a>
  <a class="door" href="#families"><span class="dn">03</span><b>See how they combine</b><small>Ten families of patterns, each a full scene, signs and next steps.</small></a>
</nav>
<section id="start" class="band">
  <p class="label">Start here</p><h2>The ten that matter most</h2>
  <ol class="top10">{top}</ol>
  <p class="note">{esc(d.get('top10_method', ''))}</p>
</section>
<section id="stages" class="band">
  <p class="label">Eight stages</p><h2>From first approach to replacement</h2>
  <ol class="stages">{stages}</ol>
</section>
<section id="families" class="band">
  <p class="label">Ten families</p><h2>How the tactics combine</h2>
  <ol class="fams">{fams}</ol>
</section>
<section class="band small">
  <p>Not sure what you're looking at? The <a href="/playbook">Pattern Decoder</a> explains single tactics in plain words, for any setting. The <a href="{cx.u('standards')}">sector standards</a> list what to keep, ordinary explanations to rule out first, and when concern should grow.</p>
</section>"""
    desc = clip("How manipulation and control work in the music and entertainment industry: %d tactics and %d patterns, with signs, what to keep and what to do." % (len(d["tactics"]), len(cx.live)))
    ld = [article_ld(cx, "The Fractal: " + d["title"], desc, "", "CollectionPage", {
        "mainEntity": {"@type": "ItemList", "itemListElement": [
            {"@type": "ListItem", "position": t["rank"], "url": ORIGIN + cx.u(cx.combos[t["combo_id"]]["slug"]), "name": t["name"]}
            for t in d["top10"] if t["combo_id"] in cx.live]}})]
    return frame(cx, title="Manipulation in the Music Industry: Tactics, Patterns and What to Do · The Fractal",
                 desc=desc, path="", crumbs=[("The Fractal", "/fractal"), (d["title"], None)],
                 body=body, ld=ld, og="home", cls="home")


def stage_page(cx, stage):
    d, i = cx.d, stage_no(cx, stage)
    ts = [t for t in d["tactics"] if t["stage"] == stage]
    chips = "".join('<a href="#%s">%s</a>' % (t["anchor"], esc(t["name"])) for t in ts)
    arts = []
    for t in ts:
        lv = "".join('<div class="lv lv-%s"><span class="lvn">%s</span>%s</div>' % (
            k, lab, src("<p>%s</p>" % inline(t["examples"].get(key, ""))))
            for key, k, lab in LEVELS if t["examples"].get(key))
        seen = [k for k in t["combos"]]
        seen_html = ('<p class="seen"><span>Seen in these patterns</span> %s</p>' %
                     " ".join(cx.combo_link(k) for k in seen)) if seen else ""
        aka = '<p class="aka">Also called: %s</p>' % esc(t["also_called"]) if t.get("also_called") else ""
        arts.append(f"""<article class="tac" id="{t['anchor']}">
  <p class="tno">{i}.{int(t['standard_id'].split('-')[-1])} · {stage.title()}</p>
  <h2><a href="#{t['anchor']}">{esc(t['name'])}</a></h2>
  {src('<p class="def">%s</p>' % inline(t['definition']))}
  {aka}
  <div class="levels">{lv}</div>
  {seen_html}
</article>""")
    prev_s = d["stages"][i - 2] if i > 1 else None
    next_s = d["stages"][i] if i < 8 else None
    pn = '<nav class="pn" aria-label="Stages">%s%s</nav>' % (
        '<a href="%s"><small>Previous stage</small><b>%s</b></a>' % (cx.u("stage-" + prev_s.lower()), prev_s.title()) if prev_s else "<span></span>",
        '<a class="nx" href="%s"><small>Next stage</small><b>%s</b></a>' % (cx.u("stage-" + next_s.lower()), next_s.title()) if next_s else "<span></span>")
    body = f"""
<header class="phead" style="--c:var(--s{i})">
  <p class="kicker">Stage {i} of 8</p>
  <h1>{stage.title()}</h1>
  <p class="lede">{esc(STAGE_INFO[stage])} {len(ts)} tactics, each shown in a person's life, inside an organization, and in the culture around it.</p>
  <nav class="chips" aria-label="Tactics in this stage">{chips}</nav>
</header>
<div class="tacs" style="--c:var(--s{i})">{''.join(arts)}</div>
{pn}"""
    desc = clip("The %s stage of manipulation in the music industry: %d tactics including %s, with examples for a person, an organization and the culture." % (
        stage.title(), len(ts), ", ".join(t["name"] for t in ts[:3])))
    ld = [article_ld(cx, "%s: stage %d of manipulation in the music industry" % (stage.title(), i), desc, "stage-" + stage.lower(),
                     "CollectionPage", {"hasPart": {"@type": "DefinedTermSet", "name": stage.title(), "hasDefinedTerm": [
                         {"@type": "DefinedTerm", "name": t["name"], "description": plain(t["definition"]), "termCode": t["standard_id"],
                          "url": ORIGIN + cx.tactic_href(t["single_no"])} for t in ts]}})]
    return frame(cx, title="%s Tactics in the Music Industry (Stage %d of 8) · The Fractal" % (stage.title(), i), desc=desc,
                 path="stage-" + stage.lower(), crumbs=[("The Fractal", "/fractal"), (d["title"], cx.u()), ("Stage %d: %s" % (i, stage.title()), None)],
                 body=body, ld=ld, og="stage-" + stage.lower(), cls="stage")


def family_page(cx, cat, idx):
    d = cx.d
    nm = re.sub(r"\s*Composites?$", "", cat["name"])
    cards = []
    for k in cat["combos"]:
        c = cx.combos[k]
        if k not in cx.live:
            continue
        cards.append('<li><a class="card" href="%s"><b>%s</b><small>%s</small><span class="meta">%d tactics%s</span></a></li>' % (
            cx.u(c["slug"]), esc(c["name"]), esc(clip(first_sentence(c["definition"]), 190)), len(c["tactics"]),
            " · safety note" if c["has_safety_note"] else ""))
    cats = d["categories"]
    prv, nxt = (cats[idx - 1] if idx > 0 else None), (cats[idx + 1] if idx + 1 < len(cats) else None)
    pn = '<nav class="pn" aria-label="Families">%s%s</nav>' % (
        '<a href="%s"><small>Previous family</small><b>%s</b></a>' % (cx.u("family-" + prv["slug"]), esc(re.sub(r"\s*Composites?$", "", prv["name"]))) if prv else "<span></span>",
        '<a class="nx" href="%s"><small>Next family</small><b>%s</b></a>' % (cx.u("family-" + nxt["slug"]), esc(re.sub(r"\s*Composites?$", "", nxt["name"]))) if nxt else "<span></span>")
    body = f"""
<header class="phead">
  <p class="kicker">Family {idx + 1} of {len(cats)} · {len(cards)} patterns</p>
  <h1>{esc(nm)}</h1>
</header>
{src(md(cat['intro_md'], first_cls='first'), 'intro')}
<ul class="cards">{''.join(cards)}</ul>
{pn}"""
    desc = clip("%s in the music and entertainment industry: %d patterns, each with a scene, signs, what to keep and what to do." % (nm, len(cards)))
    ld = [article_ld(cx, "%s in the music industry" % nm, desc, "family-" + cat["slug"], "CollectionPage", {
        "mainEntity": {"@type": "ItemList", "itemListElement": [
            {"@type": "ListItem", "position": n + 1, "url": ORIGIN + cx.u(cx.combos[k]["slug"]), "name": cx.combos[k]["name"]}
            for n, k in enumerate(k for k in cat["combos"] if k in cx.live)]}})]
    return frame(cx, title="%s in the Music Industry · The Fractal" % nm, desc=desc, path="family-" + cat["slug"],
                 crumbs=[("The Fractal", "/fractal"), (d["title"], cx.u()), (nm, None)], body=body, ld=ld,
                 og="family-" + cat["slug"], cls="family")


def levels_block(c):
    st = c["review_state"]
    parts = []
    for key, k, lab in [("Individual Level", "ind", "Individual"), ("Institutional Echo", "inst", "Institutional"),
                        ("Civilizational Echo", "civ", "Civilizational")]:
        if c["sections"].get(key):
            parts.append('<div class="lv lv-%s"><h3 class="lvn">%s</h3>%s</div>' % (k, lab, src(md(c["sections"][key], st))))
    return '<div class="levels big">%s</div>' % "".join(parts)


def cue_cards(text, st):
    cards = []
    for b in blocks(text):
        lines = b.split("\n")
        m = re.match(r"\*\*(.+?):?\*\*:?\s*$", lines[0])
        if m:
            cards.append('<div class="cue"><h3>%s</h3>%s</div>' % (
                inline(m.group(1).rstrip(":"), st), src("".join("<p>%s</p>" % inline(l, st) for l in lines[1:]))))
        else:
            cards.append(src(md(b, st)))
    # the card titles are author words too: count them by wrapping the grid
    return '<div class="cues" data-src>%s</div>' % "".join(cards)


def escalation(text, st):
    out = []
    for b in blocks(text):
        m = re.match(r"\*\*(.+?):\*\*\s*(.*)", b, re.S)
        if m and "→" in m.group(1):
            lvl = m.group(1).split("→")[-1].strip().lower()
            out.append('<div class="esc esc-%s"><p class="esc-h">%s</p><p>%s</p></div>' % (
                slugify(lvl), inline(m.group(1), st), inline(m.group(2), st)))
        else:
            out.append(md(b, st))
    return '<div class="escs" data-src>%s</div>' % "".join(out)


def breakdown(c, st):
    """Link each tactic name at the start of a numbered item to its stage entry (resolved ids only)."""
    h = md(c["sections"]["Verbal Breakdown"], st)
    for r in c["tactics"]:
        if r["single_no"]:
            nm = esc(r["name"])
            h = h.replace("<li><strong>%s</strong>" % nm, '<li><strong><a href="%s">%s</a></strong>' % ("{{T:%s}}" % r["single_no"], nm), 1)
    return h


def combo_page(cx, c):
    d, st = cx.d, c["review_state"]
    cat = cx.cats[c["category_id"]]
    fam = re.sub(r"\s*Composites?$", "", cat["name"])
    S = c["sections"]
    toc, parts = [], []
    if c["has_safety_note"]:
        parts.append('<aside class="safety" id="safety" role="note" aria-label="Safety note">'
                     '<p class="safety-h">%s Read this first</p>%s</aside>' % (svg("alert"), src(md(S["Safety Note (read first)"], st))))
    for key, head in COMBO_ORDER:
        if key == "LEVELS":
            sid = "levels"
            parts.append('<section id="%s"><h2>%s</h2>%s</section>' % (sid, head, levels_block(c)))
            toc.append((sid, head))
            continue
        if not S.get(key):
            continue
        sid = slugify(head or key)
        if key == "Cold Open":
            inner = src(md(S[key], st, first_cls="first"), "scene")
        elif key == "The Name":
            parts.append('<p class="name-line" data-src>%s</p>' % inline(S[key], st))
            continue
        elif key == "Reflection":
            parts.append('<blockquote class="reflect" data-src>%s</blockquote>' % inline(" ".join(blocks(S[key])), st))
            continue
        elif key == "Verbal Breakdown":
            inner = src(breakdown(c, st))
        elif key == "Recognition Cue Cards":
            inner = cue_cards(S[key], st)
        elif key == "Escalation Triggers — Specific":
            inner = escalation(S[key], st)
        else:
            inner = src(md(S[key], st))
        parts.append('<section id="%s"><h2>%s</h2>%s</section>' % (sid, esc(head), inner))
        toc.append((sid, head))
    body_html = "\n".join(parts)
    body_html = re.sub(r"\{\{T:(T\d+)\}\}", lambda m: cx.tactic_href(m.group(1)), body_html)
    tac = "".join('<li>%s</li>' % ('<a href="%s">%s</a>' % (cx.tactic_href(r["single_no"]), esc(r["name"])) if r["single_no"]
                                   else esc(r["name"])) for r in c["tactics"])
    sib = [k for k in cat["combos"] if k != c["combo_id"] and k in cx.live][:6]
    cross = [x for x in cx.cross.get(c["combo_id"], []) if x.get("sector") != d["sector"]]
    cross_html = ('<section class="aside-sec"><h2>This pattern in other sectors</h2><ul class="plain">%s</ul></section>' %
                  "".join('<li><a href="%s">%s</a></li>' % (esc(x["url"]), esc(x["title"])) for x in cross)) if cross else ""
    toc_html = "".join('<li><a href="#%s">%s</a></li>' % (i, esc(h)) for i, h in toc)
    body = f"""
<article class="combo">
<header class="phead">
  <p class="kicker"><a href="{cx.u('family-' + cat['slug'])}">{esc(fam)}</a> · {len(c['tactics'])} tactics combined</p>
  <h1>{esc(c['name'])}</h1>
  <p class="sub">in the music and entertainment industry</p>
  <p class="state state-{st}"><span>{'Unreviewed draft' if st == 'unreviewed' else 'Expert reviewed' if st == 'expert_reviewed' else 'Sources verified'}</span> {esc(STATE_NOTE[st])} <a href="#labels">What the labels mean</a></p>
</header>
<div class="combo-grid">
<aside class="toc"><details open><summary>On this page</summary><ol>{toc_html}<li><a href="#tactics">The tactics in it</a></li></ol></details></aside>
<div class="combo-body">
{body_html}
<section id="tactics" class="aside-sec"><h2>The tactics in it</h2><ol class="plain">{tac}</ol></section>
{cross_html}
<section class="aside-sec"><h2>More in {esc(fam)}</h2><ul class="plain">{''.join('<li>%s</li>' % cx.combo_link(k) for k in sib)}</ul></section>
<section id="labels" class="aside-sec legend"><h2>What the labels mean</h2>
<p><span class="tg tg-composite">Composite</span> a made-up example built from common situations; no real person is described.
<span class="tg tg-pattern">Common pattern</span> widely reported in the industry, not a claim about any one company.
<span class="tg tg-legal">Varies by place</span> law and contract practice differ by country and state.
<span class="tg tg-review">{TAG_LABEL[('review', st)][0]}</span> and <span class="tg tg-source">{TAG_LABEL[('source', st)][0]}</span> show where checking stands.
<span class="slot">[X]</span> marks a blank for you to fill in.</p></section>
</div></div>
</article>"""
    desc = clip("%s: %s" % (c["name"], first_sentence(c["definition"])))
    ld = [article_ld(cx, "%s in the music industry" % c["name"], desc, c["slug"], "Article", {
        "articleSection": fam, "wordCount": c["reader_words"],
        "about": [{"@type": "DefinedTerm", "name": r["name"], "url": ORIGIN + cx.tactic_href(r["single_no"])}
                  for r in c["tactics"] if r["single_no"]],
        "identifier": c["combo_id"]})]
    ttl = "%s: Signs in the Music Industry and What to Do · The Fractal" % c["name"]
    if len(ttl) > 70:
        ttl = "%s: Signs in the Music Industry · The Fractal" % c["name"]
    return frame(cx, title=ttl, desc=desc,
                 path=c["slug"], crumbs=[("The Fractal", "/fractal"), (d["title"], cx.u()), (fam, cx.u("family-" + cat["slug"])), (c["name"], None)],
                 body=body, ld=ld, og="family-" + cat["slug"], progress=True, cls="combo-page")


def standards_page(cx):
    S = cx.d["standards"]
    secs = "".join('<section id="%s"><h2>%s</h2>%s</section>' % (slugify(h), esc(h), src(md(v))) for h, v in S.items())
    body = f"""<header class="phead"><p class="kicker">Applies to every pattern in this sector</p><h1>Sector standards</h1>
<p class="lede">What to keep, the ordinary explanations to rule out first, and the signs that concern should grow.</p></header>
<div class="std">{secs}</div>"""
    desc = "Sector standards for the music and entertainment industry: what records to keep, ordinary explanations to rule out, and when concern should grow."
    return frame(cx, title="Music Industry Standards: Evidence, Benign Explanations and Warning Signs · The Fractal", desc=desc,
                 path="standards", crumbs=[("The Fractal", "/fractal"), (cx.d["title"], cx.u()), ("Sector standards", None)],
                 body=body, ld=[article_ld(cx, "Sector standards: music and entertainment", desc, "standards")], og="home", cls="standards")


def az_page(cx):
    rows = [(c["name"], cx.u(c["slug"]), "Pattern", re.sub(r"\s*Composites?$", "", cx.cats[c["category_id"]]["name"]))
            for c in cx.d["combos"] if c["combo_id"] in cx.live]
    rows += [(t["name"], cx.tactic_href(t["single_no"]), "Tactic", t["stage"].title()) for t in cx.d["tactics"]]
    rows.sort(key=lambda r: re.sub(r"^(the|a)\s+", "", r[0].lower().strip('"“')))
    lis = "".join('<li data-k="%s"><a href="%s">%s</a><span>%s · %s</span></li>' % (
        esc(r[0].lower()), r[1], esc(r[0]), r[2], esc(r[3])) for r in rows)
    body = f"""<header class="phead"><p class="kicker">{len(rows)} entries</p><h1>A to Z</h1>
<label class="filter"><span>Filter</span><input id="q" type="search" autocomplete="off" placeholder="Type a word, e.g. royalty"></label></header>
<ul class="az" id="az">{lis}</ul><p id="none" class="note" hidden>Nothing matches. Try a shorter word.</p>"""
    desc = "Every manipulation tactic and pattern in the music and entertainment industry, A to Z."
    return frame(cx, title="Music Industry Manipulation Tactics and Patterns, A to Z · The Fractal", desc=desc, path="a-z",
                 crumbs=[("The Fractal", "/fractal"), (cx.d["title"], cx.u()), ("A to Z", None)],
                 body=body, ld=[article_ld(cx, "A to Z", desc, "a-z", "CollectionPage")], og="home", cls="az-page")


def og_cards(cx, outdir):
    """HTML for social cards; og.mjs screenshots them to og/<name>.png at 1200x630."""
    cards = {"home": ("The Fractal", cx.d["title"], "%d tactics · %d patterns" % (len(cx.d["tactics"]), len(cx.live)), "var(--s1)")}
    for i, s in enumerate(cx.d["stages"]):
        cards["stage-" + s.lower()] = ("Stage %d of 8" % (i + 1), s.title(), cx.d["title"], "var(--s%d)" % (i + 1))
    for c in cx.d["categories"]:
        cards["family-" + c["slug"]] = (cx.d["title"], re.sub(r"\s*Composites?$", "", c["name"]), "The Fractal", "var(--s1)")
    outdir.mkdir(parents=True, exist_ok=True)
    style = css().replace("/F/", "../site" + cx.u("f/"))
    for name, (k, h, s, col) in cards.items():
        (outdir / (name + ".html")).write_text(
            '<!DOCTYPE html><html><head><meta charset="utf-8"><style>%s</style></head><body class="ogb">'
            '<div class="og" style="--c:%s"><p class="kicker">%s</p><h1>%s</h1><p class="ogs">%s</p>'
            '<p class="ogf">noblefathercreations.com/fractal</p></div></body></html>' % (style, col, esc(k), esc(h), esc(s)))
    return list(cards)


def sitemap(urls):
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
            "".join("<url><loc>%s</loc></url>\n" % (ORIGIN + u) for u in urls) + "</urlset>\n")


def main(sector, target):
    data = json.loads((ROOT / "content/fractal" / sector / "build/sector.json").read_text())
    cx = Ctx(data, target)
    out_root = ROOT / "library/fractal/sectors" / sector
    site = out_root / "site"
    if site.exists():
        shutil.rmtree(site)
    d = site / cx.base.strip("/")
    d.mkdir(parents=True)
    pages = {"": home(cx), "standards": standards_page(cx), "a-z": az_page(cx)}
    for s in data["stages"]:
        pages["stage-" + s.lower()] = stage_page(cx, s)
    for i, cat in enumerate(data["categories"]):
        pages["family-" + cat["slug"]] = family_page(cx, cat, i)
    for c in data["combos"]:
        if c["combo_id"] in cx.live:
            pages[c["slug"]] = combo_page(cx, c)
    for p, h in pages.items():
        assert "{{" not in h, "unfilled template in " + p
        (site / (cx.base.strip("/") + ".html") if p == "" else d / (p + ".html")).write_text(h)
    shutil.copytree(out_root / "fonts", d / "f") if (out_root / "fonts").exists() else None
    urls = [cx.u(p) for p in pages]
    (d / "sitemap.xml").write_text(sitemap(urls))
    og = og_cards(cx, out_root / "og-src")
    (out_root / "manifest.json").write_text(json.dumps({
        "sector": data["sector"], "target": target, "base": cx.base, "built": cx.date, "pages": len(pages),
        "combos_live": len(cx.live), "combos_held": len(cx.combos) - len(cx.live), "og": og,
        "expect": {c["slug"]: {"words": c["reader_words"], "safety": c["has_safety_note"]}
                   for c in data["combos"] if c["combo_id"] in cx.live}}, indent=1))
    print("built %d pages (%d combos live, %d held back) -> %s" % (len(pages), len(cx.live), len(cx.combos) - len(cx.live), site))


if __name__ == "__main__":
    a = sys.argv[1:]
    tgt = a[a.index("--target") + 1] if "--target" in a else "preview"
    main(a[0] if a and not a[0].startswith("--") else "ent", tgt)

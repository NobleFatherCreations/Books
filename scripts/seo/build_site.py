#!/usr/bin/env python3
"""Site-wide findability files for noblefathercreations.com (served by the hub site):

  hub/robots.txt   every crawler allowed, AI crawlers named, every sitemap listed
  hub/sitemap.xml  the domain's top-level pages (scripts/build-root-sitemap.py)
  hub/llms.txt     a plain map of the library for AI assistants (llmstxt.org format)
  hub/og.png       share card for the homepage
  hub/catalogue-redesign.html  head: canonical, Open Graph, WebSite + Organization + ItemList JSON-LD

Run after the book builds: python3 scripts/seo/build_site.py
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parent))
import seo_common as S

HUB = S.ROOT / "hub"
FRACTAL_SECTORS = ["entertainment"]   # Fractal sector sites (design/fractal-sector), each its own Netlify site
JS_BOOKS = ["longafter", "silence", "repair", "atwill", "slowtake", "loop", "scale"]   # round 2 (scripts/seo/build_jsbook.py)
BOOKS_WITH_PAGES = ["faith", "children", "feminine", "fractal", "fracture", "wook", "festival"] + JS_BOOKS
AI_BOTS = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "Claude-User", "PerplexityBot",
           "Perplexity-User", "Google-Extended", "Applebot", "Applebot-Extended", "Amazonbot", "DuckAssistBot",
           "meta-externalagent", "meta-webindexer", "meta-externalfetcher", "MistralAI-User", "CCBot", "Bingbot", "Googlebot"]


def robots():
    maps = [f"{S.DOMAIN}/sitemap.xml", f"{S.DOMAIN}/playbook/sitemap.xml"] + [f"{S.DOMAIN}/{b}/sitemap.xml" for b in BOOKS_WITH_PAGES]
    maps += [f"{S.DOMAIN}/fractal/{x}/sitemap.xml" for x in FRACTAL_SECTORS]
    txt = ("# Noble Father Creations. Every page is open to search engines and AI assistants (owner decision, 2026-10-27;\n"
           "# reaffirmed 2026-11-08: these free books should be findable everywhere).\n"
           "User-agent: *\nAllow: /\n\n"
           "# Search engines and AI assistants, named so the invitation is explicit.\n"
           + "".join(f"User-agent: {b}\n" for b in AI_BOTS) + "Allow: /\n\n"
           "# A plain map of the library for AI assistants: https://noblefathercreations.com/llms.txt\n\n"
           + "".join(f"Sitemap: {m}\n" for m in maps))
    S.write(HUB / "robots.txt", txt)
    return maps


def book_pages(slug):
    sm = S.ROOT / "library" / slug / "sitemap.xml"
    locs = [e.text for e in ET.parse(sm).getroot().iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
    out = []
    for u in locs:
        if u.rstrip("/").endswith(f"/{slug}") or u.endswith("/contents"):
            continue
        f = S.ROOT / "library" / slug / (u.rsplit("/", 1)[-1] + ".html")
        page = S.read(f)
        t = re.search(r"<h1[^>]*>(.*?)</h1>", page, re.S)
        d = re.search(r'<meta name="description" content="([^"]*)"', page)
        out.append((S.plain(t.group(1)) if t else u, u, d.group(1) if d else ""))
    return out


def llms(sites):
    import importlib
    by = {p["url"].rstrip("/").rsplit("/", 1)[-1]: p for p in sites["projects"]}
    lines = ["# Noble Father Creations", "",
             "> Free books and tools by Shae Stovell for seeing manipulation, coercive control and power clearly, and for "
             "staying safe: field guides for women, kids, festival-goers and families, an investigation of where $50 trillion "
             "went, a sourced record of power inside 34 faiths, and the Pattern Decoder (335 named tactics and 32 patterns). Everything is "
             "free to read, offline-friendly, and licensed CC BY-NC-ND 4.0 (share with credit; no selling; no edited copies).", "",
             "Every book below has a contents page and one plain HTML page per chapter, so you can cite the exact chapter. "
             "Each page carries a short notice: these are educational resources, not legal, medical or psychological advice.", "",
             "## Who made this", "",
             f"- [Shae Stovell, in his own words]({S.DOMAIN}/about): " + __import__("about_content").plain_summary(),
             "- Elsewhere: " + ", ".join(f"{n} {u}" for n, u, _ in __import__("about_content").SOCIAL), ""]
    names = {"faith": "The Sacred Divide", "children": "Playground Protectors", "feminine": "The Sovereign Divine Feminine",
             "fractal": "The Fractal", "fracture": "The Fracture", "wook": "The Festie Codex", "festival": "The Festie Bible"}
    jb = importlib.import_module("build_jsbook")
    names.update({b: jb.BOOKS[b]["title"] for b in JS_BOOKS})
    lines.append("## Books with chapter pages")
    lines.append("")
    for b in BOOKS_WITH_PAGES:
        if b in JS_BOOKS:
            jb_h = S.read(S.ROOT / "library" / b / "index.html")
            desc = re.search(r'<meta name="description" content="([^"]*)"', jb_h).group(1)
        else:
            desc = importlib.import_module(f"build_{b}").BOOK["description"]
        cont = f"{S.DOMAIN}/{b}/contents" if b != "faith" else f"{S.DOMAIN}/faith"
        lines.append(f"- [{names[b]}]({S.DOMAIN}/{b}): {desc} Contents: {cont}")
    for b in BOOKS_WITH_PAGES:
        lines += ["", f"## {names[b]}: chapters", ""]
        pages = book_pages(b)
        if b == "festival":                       # 291 pages: list the 21 guides; each links its scenarios
            fb = __import__("build_festival")
            guide_slugs = {S.slugify(g["role"], 40) for g in fb.data_of(S.read(S.ROOT / "library/festival/index.html"))["guides"]}
            pages = [p for p in pages if p[1].rsplit("/", 1)[-1] in guide_slugs]
        lines += [f"- [{t}]({u})" + (f": {d}" if b == "longafter" and d else "") for t, u, d in pages]
    dl = S.read(S.ROOT / "instruments/playbook/site/llms.txt")
    m = re.search(r"guide to (\d+) manipulation and control tactics and (\d+) patterns", dl)
    count = f"{m.group(1)} manipulation and control tactics and {m.group(2)} patterns" if m else "manipulation and control tactics"
    lines += ["", "## Tools", "",
              f"- [The Pattern Decoder]({S.DOMAIN}/playbook): {count}, each with its own page "
              f"(signs both ways, what you can do, checked sources). Every tactic: {S.DOMAIN}/playbook/tactics. "
              f"Full list for assistants: {S.DOMAIN}/playbook/llms.txt",
              f"- [The Root]({S.DOMAIN}/shadowroot): {by['shadowroot'].get('tagline', 'A shadow work practice')}",
              f"- [The Listening Room]({S.DOMAIN}/music): free original music", ""]
    lines += ["", "## Optional", "", f"- [Home]({S.DOMAIN}/): the whole catalogue",
              f"- [Topics]({S.DOMAIN}/topics): every term (gaslighting, DARVO, coercive control, harm reduction...) with the chapters that cover it",
              "- Corrections and contact: dapperdadnfc@gmail.com", ""]
    S.write(HUB / "llms.txt", "\n".join(lines))
    return len(lines)


def hub_head(sites):
    f = HUB / "catalogue-redesign.html"
    h = S.SEO_TAG.sub("", S.read(f))
    title = "Manipulation & Narcissistic Abuse: Free Books | Noble Father"
    desc = ("Free books and a Pattern Decoder on manipulation, narcissistic abuse, gaslighting and coercive control. "
            "Name the pattern, take a safe next step.")
    h = re.sub(r"<title>.*?</title>", f"<title>{S.esc(title)}</title>", h, count=1, flags=re.S)
    h = re.sub(r'<meta\s+name="description"[^>]*>', f'<meta name="description" content="{S.esc(desc)}">', h, count=1)
    h = re.sub(r'[ \t]*<link\s+rel="canonical"[^>]*>\n?', "", h)
    h = re.sub(r'[ \t]*<meta\s+(?:property="og:[^"]+"|name="twitter:[^"]+")[^>]*>\n?', "", h)
    items = []
    for p in sites["projects"]:
        items.append({"@type": "ListItem", "position": len(items) + 1, "url": p["url"], "name": p["title"]})
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "@id": S.DOMAIN + "/#site", "url": S.DOMAIN + "/", "name": "Noble Father Creations",
         "description": desc, "publisher": {"@id": S.ORG["@id"]}, "creator": {"@id": S.PERSON["@id"]}, "inLanguage": "en", "license": S.LICENSE_URL,
         # the subjects people search for, each pointing at the page that explains it (homepage "Look up a pattern")
         "about": [{"@type": "Thing", "name": x["label"], "url": S.DOMAIN + x["href"]} for x in json.loads((S.ROOT / "design/hub-v18/data.json").read_text())["lookups"]],
         "keywords": "manipulation, narcissistic abuse, gaslighting, coercive control, love bombing, trauma bonding, emotional abuse, DARVO, silent treatment",
         "hasPart": [{"@id": p["url"] + "#book"} if p["url"].rsplit("/", 1)[-1] in BOOKS_WITH_PAGES else {"@type": "CreativeWork", "name": p["title"], "url": p["url"]}
                     for p in sites["projects"]]},
        {"@type": "CollectionPage", "@id": S.DOMAIN + "/", "url": S.DOMAIN + "/", "name": title, "description": desc,
         "isPartOf": {"@id": S.DOMAIN + "/#site"}, "dateModified": S.TODAY,
         "mainEntity": {"@type": "ItemList", "numberOfItems": len(items), "itemListElement": items}},
        S.PERSON, S.ORG]}
    tags = (f'<link data-seo rel="canonical" href="{S.DOMAIN}/">\n'
            f'<meta data-seo property="og:type" content="website">\n<meta data-seo property="og:site_name" content="Noble Father Creations">\n'
            f'<meta data-seo property="og:title" content="{S.esc(title)}">\n<meta data-seo property="og:description" content="{S.esc(desc)}">\n'
            f'<meta data-seo property="og:url" content="{S.DOMAIN}/">\n<meta data-seo property="og:image" content="{S.DOMAIN}/og.png">\n'
            f'<meta data-seo property="og:image:width" content="1200">\n<meta data-seo property="og:image:height" content="630">\n'
            f'<meta data-seo property="og:image:alt" content="Noble Father Creations: free books by Shae Stovell">\n'
            f'<meta data-seo name="twitter:card" content="summary_large_image">\n<meta data-seo name="twitter:image" content="{S.DOMAIN}/og.png">\n'
            f'<link data-seo rel="license" href="{S.LICENSE_URL}">\n'
            f'<script type="application/ld+json" data-seo>{S.ld_json(ld)}</script>\n')
    h = h.replace("</title>", "</title>\n" + tags, 1)
    # Owner 2026-11-20: no version/update notes on the homepage; build_hub.py removes the section.
    S.write(f, h)
    # share card, drawn with The Fracture's faces
    tmp = S.ROOT / "library" / "_seo_tmp_hub"
    shutil.copytree(S.ROOT / "library/fracture/f", tmp / "f", dirs_exist_ok=True)
    try:
        card = {"slug": "", "title": "Noble Father Creations", "fonts": ["Fraunces", "Crimson Text"],
                "theme": {"bg": "#0B0E18", "fg": "#ECE6D9", "fg2": "#B6AF9E", "panel": "#0E1322", "glow": "#2a2014", "acc": "#E6C570",
                          "disp": "'Fraunces',Georgia,serif", "body": "'Crimson Text',Georgia,serif"}}
        S.make_og(card, tmp, "Free books · free tools · free forever", "See manipulation clearly. Stay safe. Help each other home.")
        brand = S.ROOT / "design/brand/og-home-1200x630.png"     # the owner's own brand header, cropped to 1200x630
        if brand.exists(): shutil.copyfile(brand, tmp / "og.png")
        shutil.copy(tmp / "og.png", HUB / "og.png")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


TOPICS_CSS = """:root{color-scheme:dark}*{box-sizing:border-box}body{margin:0;background:#141019;color:#ECE4D6;font:400 1.0625rem/1.65 Georgia,'Times New Roman',serif}
a{color:#E8C879;text-underline-offset:.18em}a:hover{color:#ECE4D6}main{max-width:46rem;margin:0 auto;padding:32px 16px 96px}
h1{font:600 clamp(2rem,1.4rem + 3vw,3rem)/1.1 Georgia,serif;margin:0 0 16px}.lede{color:#BCB1A0;font-size:1.1875rem;margin:0 0 24px}
.az{display:flex;flex-wrap:wrap;gap:4px 12px;margin:0 0 32px;font:700 1rem/1 system-ui,sans-serif}.az a{min-width:24px;min-height:44px;display:inline-flex;align-items:center;text-decoration:none}
h2{font:600 1.375rem/1.25 Georgia,serif;margin:40px 0 8px;scroll-margin-top:16px}h2.letter{font:700 .875rem/1 system-ui,sans-serif;letter-spacing:.12em;color:#C9A35B;margin:48px 0 0}
ul{margin:0;padding-left:1.2em}li{margin:4px 0}.book{color:#BCB1A0}.dec{font-size:.9375rem}
.crumbs{font-size:.9375rem;color:#BCB1A0;margin:0 0 24px}.crumbs a{color:#BCB1A0}footer{max-width:46rem;margin:0 auto;padding:24px 16px 96px;color:#BCB1A0;font-size:.9375rem;border-top:1px solid #2C2236}"""
BOOK_NAMES = {"faith": "The Sacred Divide", "children": "Playground Protectors", "feminine": "The Sovereign Divine Feminine",
              "fractal": "The Fractal", "fracture": "The Fracture", "wook": "The Festie Codex", "festival": "The Festie Bible",
              "longafter": "The Long After", "silence": "The Silence", "repair": "The Repair", "atwill": "At Will",
              "slowtake": "The Slow Take", "loop": "The Loop", "scale": "The Weighing"}


def seal_menu():
    """The site-wide seal menu (every book and project, scripts/nf-catalogue.py) for hub pages built here."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("nf_catalogue", S.ROOT / "scripts/nf-catalogue.py")
    cat = importlib.util.module_from_spec(spec); spec.loader.exec_module(cat)
    return S.house_parts(cat.retoc(S.read(S.ROOT / "library/silence/index.html"), None))


def topics():
    """/topics: every searched term the chapter pages declare (their 'Also known as' line), with every chapter across
    the library that covers it, plus the Pattern Decoder's own page for that tactic where one exists."""
    import collections
    terms = collections.defaultdict(list)
    shown = {}
    for b in BOOKS_WITH_PAGES:
        for f in sorted((S.ROOT / "library" / b).glob("*.html")):
            if f.name in ("index.html", "contents.html"):
                continue
            h = S.read(f)
            m = re.search(r'"@type":"Chapter".*?"name":"(.*?)".*?"url":"(.*?)"(.*?)\}', h)
            ld = re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', h, re.S)
            node = None
            for blk in ld:
                for n in json.loads(blk).get("@graph", []):
                    if n.get("@type") == "Chapter":
                        node = n
            if not node or not node.get("alternateName"):
                continue
            for a in node["alternateName"]:
                key = re.sub(r"[^a-z0-9 ]+", "", a.lower().replace("’", "'").strip('"')).strip()
                if len(key) < 3:
                    continue
                shown.setdefault(key, a.strip('"'))
                terms[key].append((b, S.smart(node["name"]), node["url"].replace(S.DOMAIN, "")))
    dec = {re.sub(r"[^a-z0-9 ]+", "", n.lower()): u for n, u in S.decoder_terms()}
    keep = {k: v for k, v in terms.items() if len({x[2] for x in v}) >= 2 or k in dec}
    order = sorted(keep, key=lambda k: shown[k].lower())
    letters, body, cur = [], [], None
    for k in order:
        L = shown[k][0].upper() if shown[k][0].isalpha() else "#"
        if L != cur:
            cur = L
            letters.append(L)
            body.append(f'<h2 class="letter" id="letter-{L.lower() if L != "#" else "num"}">{L}</h2>')
        items = "".join(f'<li><a href="{u}">{S.esc(n)}</a> <span class="book">· {BOOK_NAMES[b]}{" (for kids)" if b == "children" else ""}</span></li>'
                        for b, n, u in sorted(set(keep[k]), key=lambda x: (BOOK_NAMES[x[0]], x[1])))
        d = f'<p class="dec">In the Pattern Decoder: <a href="{dec[k]}">{S.esc(shown[k])}, signs and what to do</a></p>' if k in dec else ""
        body.append(f'<h2 id="{S.slugify(shown[k], 60)}">{S.esc(S.smart(shown[k][0].upper() + shown[k][1:]))}</h2>{d}<ul>{items}</ul>')
    az = "".join(f'<a href="#letter-{L.lower() if L != "#" else "num"}">{L}</a>' for L in letters)
    url = f"{S.DOMAIN}/topics"
    menu = seal_menu()
    title = "Topics: Manipulation, Coercive Control and Safety, Free Chapters"
    desc = (f"{len(order)} topics, from gaslighting and DARVO to consent and harm reduction, each linked to the free chapters "
            "that cover it across the Noble Father Creations library.")
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": ["CollectionPage", "DefinedTermSet"], "@id": url, "url": url, "name": title, "description": desc, "inLanguage": "en",
         "isPartOf": {"@id": S.DOMAIN + "/#site"}, "dateModified": S.TODAY, "license": S.LICENSE_URL,
         "hasDefinedTerm": [{"@type": "DefinedTerm", "name": shown[k], "url": f"{url}#{S.slugify(shown[k], 60)}"} for k in order]},
        S.crumbs_ld([("Noble Father Creations", S.DOMAIN + "/"), ("Topics", url)]), S.PERSON, S.ORG]}
    page = ("<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
            f"<title>{S.esc(title)}</title>\n<meta name=\"description\" content=\"{S.esc(desc)}\">\n<link rel=\"canonical\" href=\"{url}\">\n"
            f'<meta property="og:type" content="website">\n<meta property="og:site_name" content="Noble Father Creations">\n'
            f'<meta property="og:title" content="{S.esc(title)}">\n<meta property="og:description" content="{S.esc(desc)}">\n'
            f'<meta property="og:url" content="{url}">\n<meta property="og:image" content="{S.DOMAIN}/og.png">\n'
            f'<meta property="og:image:alt" content="Noble Father Creations: free books by Shae Stovell">\n<meta name="twitter:card" content="summary_large_image">\n'
            f'<link rel="license" href="{S.LICENSE_URL}">\n<meta name="theme-color" content="#141019">\n<style>{TOPICS_CSS}</style>\n{menu[0]}\n'
            f'<script type="application/ld+json">{S.ld_json(ld)}</script>\n</head>\n<body>\n<main>\n'
            '<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Noble Father Creations</a> › Topics</nav>\n'
            f'<h1>Topics</h1>\n<p class="lede">{S.esc(desc)} Every chapter is free to read.</p>\n'
            f'<nav class="az" aria-label="Jump to a letter">{az}</nav>\n' + "\n".join(body) + "\n</main>\n"
            f'<footer><p>{S.LICENSE_LINE}</p><p><a href="/">All books</a> · <a href="/playbook/tactics">Every tactic in the Pattern Decoder</a></p></footer>\n'
            + menu[1] + "\n" + menu[2] + '\n</body>\n</html>\n')
    S.write(HUB / "topics.html", page)
    return len(order)


ABOUT_CSS = """:root{color-scheme:dark;--ink:#16110d;--night:#0c1112;--line:#1f2a28;--paper:#ece2cf;--muted:#cbbda4;--brass:#c9a24a;--brass-hi:#e7c77d}
*{box-sizing:border-box}body{margin:0;background:var(--night);color:#e6dcc9;font:400 clamp(18px,.3vw + 17px,20px)/1.7 'Public Sans',system-ui,sans-serif;-webkit-font-smoothing:antialiased}
img{display:block;max-width:100%;height:auto}a{color:var(--brass-hi);text-underline-offset:.2em;text-decoration-thickness:1px}a:hover{color:var(--paper)}
:focus-visible{outline:2px solid var(--brass-hi);outline-offset:3px;border-radius:3px}
.bar{display:flex;justify-content:space-between;align-items:center;gap:16px;max-width:72rem;margin:0 auto;padding:8px 16px}
.bar a{display:inline-flex;align-items:center;min-height:44px;font-size:15px;color:var(--muted);text-decoration:none}.bar .leave{color:var(--paper);border:1px solid #3a4644;border-radius:999px;padding:0 16px}
.hero{max-width:72rem;margin:0 auto 0;padding:0 16px}.hero img{width:100%;border-radius:12px}
main{max-width:40rem;margin:0 auto;padding:48px 16px 96px}
.eyebrow{font-size:15px;letter-spacing:.08em;text-transform:uppercase;color:var(--brass-hi);margin:0 0 24px}
h1,h2,h3{font-family:'Gloock',Georgia,serif;font-weight:400;color:var(--paper);text-wrap:balance}
h1{font-size:clamp(36px,2.8vw + 20px,60px);line-height:1.05;letter-spacing:-.015em;margin:0 0 48px}
h2{font-size:clamp(26px,1.4vw + 16px,36px);line-height:1.15;margin:64px 0 24px}
p{margin:0 0 1.15em;text-wrap:pretty}ul{margin:0 0 1.15em;padding-left:1.2em}li{margin:0 0 .5em}li::marker{color:var(--brass)}
strong,em{color:var(--paper)}strong{font-weight:650}
.ab-rule{border:0;height:1px;margin:48px auto;width:96px;background:linear-gradient(90deg,transparent,var(--brass),transparent);opacity:.7}
.ab-wordmark{width:min(280px,70%);margin:24px 0 0}
.social{list-style:none;margin:48px 0 0;padding:32px 0 0;border-top:1px solid var(--line);display:flex;flex-wrap:wrap;gap:8px 24px}
.social a{display:inline-flex;align-items:center;gap:8px;min-height:44px;text-decoration:none;color:var(--paper)}.social span{color:var(--muted);font-size:15px}
footer{max-width:40rem;margin:0 auto;padding:24px 16px 96px;color:var(--muted);font-size:15px;border-top:1px solid var(--line)}footer a{color:var(--muted)}"""


def about():
    """/about: the owner's bio in full (content/about.md), with ProfilePage + Person schema. The homepage carries the same text."""
    import about_content as AB
    from PIL import Image
    title_h1, body = AB.blocks()
    media = HUB / "media/v18"
    wm = Image.open(media / "wordmark.webp")                      # written by build_home.py
    body = body.replace("{WORDMARK}", AB.WORDMARK.format(w=wm.width, h=wm.height)).replace("<h3>", "<h2>").replace("</h3>", "</h2>")   # h1 here, so sections are h2
    hero = Image.open(S.ROOT / "design/brand/noble-father-header.png").convert("RGB")
    hero.thumbnail((1600, 1600), Image.LANCZOS); hero.save(media / "brand-header-1600.webp", "WEBP", quality=82, method=6)
    url = f"{S.DOMAIN}/about"
    title = "Who Made This: Shae Stovell, Noble Father Creations"
    desc = ("Shae Stovell, father of four, on why he wrote fourteen free books and the Pattern Decoder on manipulation "
            "and coercive control, and why they will always be free.")
    menu = seal_menu()
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": ["ProfilePage", "AboutPage"], "@id": url, "url": url, "name": title, "headline": S.plain(title_h1), "description": desc,
         "inLanguage": "en", "isPartOf": {"@id": S.DOMAIN + "/#site"}, "dateModified": S.TODAY, "datePublished": "2026-11-23",
         "mainEntity": {"@id": S.PERSON["@id"]}, "author": {"@id": S.PERSON["@id"]},
         "primaryImageOfPage": f"{S.DOMAIN}/media/v18/brand-header-1600.webp", "license": S.LICENSE_URL},
        S.crumbs_ld([("Noble Father Creations", S.DOMAIN + "/"), ("Who made this", url)]),
        dict(S.PERSON, image=f"{S.DOMAIN}/media/v18/brand-header-1600.webp", description=AB.plain_summary()), S.ORG]}
    social = "".join(f'<li><a href="{S.esc(u)}" target="_blank" rel="noopener me"><b>{S.esc(n)}</b> <span>{S.esc(h)}</span></a></li>' for n, u, h in AB.SOCIAL)
    fonts = ("@font-face{font-family:'Gloock';font-style:normal;font-weight:400;font-display:swap;src:url(/f/gloock-400-normal.woff2) format('woff2')}"
             "@font-face{font-family:'Public Sans';font-style:normal;font-weight:100 900;font-display:swap;src:url(/f/public-sans-100-900-normal.woff2) format('woff2')}")
    page = ("<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
            f"<title>{S.esc(title)}</title>\n<meta name=\"description\" content=\"{S.esc(desc)}\">\n<meta name=\"author\" content=\"Shae Stovell\">\n<link rel=\"canonical\" href=\"{url}\">\n"
            f'<meta property="og:type" content="profile">\n<meta property="profile:first_name" content="Shae">\n<meta property="profile:last_name" content="Stovell">\n'
            f'<meta property="og:site_name" content="Noble Father Creations">\n<meta property="og:title" content="{S.esc(title)}">\n'
            f'<meta property="og:description" content="{S.esc(desc)}">\n<meta property="og:url" content="{url}">\n<meta property="og:image" content="{S.DOMAIN}/og.png">\n'
            f'<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
            f'<meta property="og:image:alt" content="Noble Father Creations: free books by Shae Stovell">\n<meta name="twitter:card" content="summary_large_image">\n'
            + "".join(f'<link rel="me" href="{S.esc(u)}">\n' for _, u, _ in AB.SOCIAL) +
            f'<link rel="preload" href="/f/gloock-400-normal.woff2" as="font" type="font/woff2" crossorigin>\n'
            f'<meta name="theme-color" content="#0c1112">\n<style>{fonts}{ABOUT_CSS}</style>\n{menu[0]}\n'
            f'<script type="application/ld+json">{S.ld_json(ld)}</script>\n</head>\n<body>\n'
            '<header><div class="bar"><a href="/">&larr; Noble Father Creations</a><a class="leave" href="https://www.google.com/search?q=weather" onclick="location.replace(this.href);return false">Leave now</a></div>\n'
            '<div class="hero"><img src="/media/v18/brand-header-1600.webp" width="' + str(hero.width) + '" height="' + str(hero.height) + '" alt="Noble Father Creations: the hatted figure holding a glowing chip" fetchpriority="high"></div></header>\n'
            f'<main>\n<p class="eyebrow">Who made this</p>\n<h1>{S.esc(title_h1)}</h1>\n{body}\n'
            f'<nav aria-label="Shae Stovell elsewhere"><ul class="social">{social}</ul></nav>\n</main>\n'
            f'<footer><p>{S.LICENSE_LINE}</p><p><a href="/">All the free books</a> · <a href="/playbook">The Pattern Decoder</a> · <a href="/topics">Topics A to Z</a></p></footer>\n'
            + menu[1] + "\n" + menu[2] + '\n</body>\n</html>\n')
    S.write(HUB / "about.html", page)


def main():
    sites = json.loads((S.ROOT / "sites.json").read_text())
    maps = robots()
    subprocess.run([sys.executable, str(S.ROOT / "scripts/build-root-sitemap.py")], check=True)
    n = llms(sites)
    hub_head(sites)
    nt = topics()
    about()
    sm = S.read(HUB / "sitemap.xml")
    for path in ("/topics", "/about"):
        if f"{path}<" not in sm:
            sm = sm.replace("</urlset>", f"  <url><loc>{S.DOMAIN}{path}</loc><lastmod>{S.TODAY}</lastmod></url>\n</urlset>")
    S.write(HUB / "sitemap.xml", sm)
    print(f"topics: {nt}")
    print(f"robots.txt: {len(maps)} sitemaps; llms.txt: {n} lines; hub head + og.png written")


if __name__ == "__main__":
    main()

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
BOOKS_WITH_PAGES = ["faith", "children", "feminine", "fractal", "fracture", "wook", "festival"]
AI_BOTS = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "Claude-User", "PerplexityBot",
           "Perplexity-User", "Google-Extended", "Applebot", "Applebot-Extended", "Amazonbot", "DuckAssistBot",
           "meta-externalagent", "meta-webindexer", "meta-externalfetcher", "MistralAI-User", "CCBot", "Bingbot", "Googlebot"]


def robots():
    maps = [f"{S.DOMAIN}/sitemap.xml", f"{S.DOMAIN}/playbook/sitemap.xml"] + [f"{S.DOMAIN}/{b}/sitemap.xml" for b in BOOKS_WITH_PAGES]
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
    by = {p["url"].rstrip("/").rsplit("/", 1)[-1]: p for p in sites["projects"]}
    lines = ["# Noble Father Creations", "",
             "> Free books and tools by Shae Stovell for seeing manipulation, coercive control and power clearly, and for "
             "staying safe: field guides for women, kids, festival-goers and families, an investigation of where $50 trillion "
             "went, a sourced record of power inside 34 faiths, and the Pattern Decoder (310 named tactics). Everything is "
             "free to read, offline-friendly, and licensed CC BY-NC-ND 4.0 (share with credit; no selling; no edited copies).", "",
             "Every book below has a contents page and one plain HTML page per chapter, so you can cite the exact chapter. "
             "Each page carries a short notice: these are educational resources, not legal, medical or psychological advice.", ""]
    names = {"faith": "The Sacred Divide", "children": "Playground Protectors", "feminine": "The Sovereign Divine Feminine",
             "fractal": "The Fractal", "fracture": "The Fracture", "wook": "The Festie Codex", "festival": "The Festie Bible"}
    import importlib
    lines.append("## Books with chapter pages")
    lines.append("")
    for b in BOOKS_WITH_PAGES:
        mod = importlib.import_module(f"build_{b}")
        desc = mod.BOOK["description"]
        cont = f"{S.DOMAIN}/{b}/contents" if b != "faith" else f"{S.DOMAIN}/faith"
        lines.append(f"- [{names[b]}]({S.DOMAIN}/{b}): {desc} Contents: {cont}")
    for b in BOOKS_WITH_PAGES:
        lines += ["", f"## {names[b]}: chapters", ""]
        pages = book_pages(b)
        if b == "festival":                       # 291 pages: list the 21 guides; each links its scenarios
            fb = __import__("build_festival")
            guide_slugs = {S.slugify(g["role"], 40) for g in fb.data_of(S.read(S.ROOT / "library/festival/index.html"))["guides"]}
            pages = [p for p in pages if p[1].rsplit("/", 1)[-1] in guide_slugs]
        lines += [f"- [{t}]({u})" for t, u, _ in pages]
    lines += ["", "## Tools", "",
              f"- [The Pattern Decoder]({S.DOMAIN}/playbook): 310 manipulation and control tactics, each with its own page "
              f"(signs, what it is, what to do). Every tactic: {S.DOMAIN}/playbook/tactics",
              f"- [The Root]({S.DOMAIN}/shadowroot): {by['shadowroot'].get('tagline', 'A shadow work practice')}",
              f"- [The Listening Room]({S.DOMAIN}/music): free original music", "",
              "## More books (single page)", ""]
    for b in ("loop", "scale", "longafter", "silence", "atwill", "repair", "slowtake"):
        p = by[b]
        lines.append(f"- [{p['title']}]({S.DOMAIN}/{b}): {p.get('tagline', '')}")
    lines += ["", "## Optional", "", f"- [Home]({S.DOMAIN}/): the whole catalogue",
              f"- [Topics]({S.DOMAIN}/topics): every term (gaslighting, DARVO, coercive control, harm reduction...) with the chapters that cover it",
              "- Corrections and contact: dapperdadnfc@gmail.com", ""]
    S.write(HUB / "llms.txt", "\n".join(lines))
    return len(lines)


def hub_head(sites):
    f = HUB / "catalogue-redesign.html"
    h = S.SEO_TAG.sub("", S.read(f))
    title = "Noble Father Creations: Free Books on Manipulation, Safety and Power"
    desc = ("Free books and tools by Shae Stovell: field guides to manipulation and coercive control for women, kids, "
            "festival-goers and families, plus the Pattern Decoder.")
    h = re.sub(r"<title>.*?</title>", f"<title>{S.esc(title)}</title>", h, count=1, flags=re.S)
    h = re.sub(r'<meta\s+name="description"[^>]*>', f'<meta name="description" content="{S.esc(desc)}">', h, count=1)
    h = re.sub(r'[ \t]*<link\s+rel="canonical"[^>]*>\n?', "", h)
    h = re.sub(r'[ \t]*<meta\s+(?:property="og:[^"]+"|name="twitter:[^"]+")[^>]*>\n?', "", h)
    items = []
    for p in sites["projects"]:
        items.append({"@type": "ListItem", "position": len(items) + 1, "url": p["url"], "name": p["title"]})
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "@id": S.DOMAIN + "/#site", "url": S.DOMAIN + "/", "name": "Noble Father Creations",
         "description": desc, "publisher": {"@id": S.ORG["@id"]}, "inLanguage": "en", "license": S.LICENSE_URL,
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
    v16 = ('<p class="updates-version">v16 &mdash; 2026-11-08</p>\n      <ul>\n        <li>Seven books now have a page for every '
           'chapter, so search engines and AI assistants can send people straight to the part they need.</li>\n        <li>Every '
           'book is now free to share under a Creative Commons licence: credit the author, no selling.</li>\n        <li>Fixed menu '
           'names: The Listening Room, The Sacred Divide, and the Pattern Decoder\u2019s 310 tactics.</li>\n        <li>New: <a href="/topics">browse every topic</a>, from gaslighting to harm reduction, with the chapters that cover it.</li>\n      </ul>\n      ')
    h = re.sub(r'<p class="updates-version">v16 &mdash; 2026-11-08</p>.*?</ul>\n      ', "", h, count=1, flags=re.S)
    if "v16 &mdash; 2026-11-08" not in h:
        anchor = '<p class="updates-version">v15 &mdash; 2026-09-04</p>'
        assert anchor in h, "hub: updates badge not found"
        h = h.replace(anchor, v16 + anchor, 1)
    S.write(f, h)
    # share card, drawn with The Fracture's faces
    tmp = S.ROOT / "library" / "_seo_tmp_hub"
    shutil.copytree(S.ROOT / "library/fracture/f", tmp / "f", dirs_exist_ok=True)
    try:
        card = {"slug": "", "title": "Noble Father Creations", "fonts": ["Fraunces", "Crimson Text"],
                "theme": {"bg": "#0B0E18", "fg": "#ECE6D9", "fg2": "#B6AF9E", "panel": "#0E1322", "glow": "#2a2014", "acc": "#E6C570",
                          "disp": "'Fraunces',Georgia,serif", "body": "'Crimson Text',Georgia,serif"}}
        S.make_og(card, tmp, "Free books · free tools · free forever", "See manipulation clearly. Stay safe. Help each other home.")
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
              "fractal": "The Fractal", "fracture": "The Fracture", "wook": "The Festie Codex", "festival": "The Festie Bible"}


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
            f'<link rel="license" href="{S.LICENSE_URL}">\n<meta name="theme-color" content="#141019">\n<style>{TOPICS_CSS}</style>\n'
            f'<script type="application/ld+json">{S.ld_json(ld)}</script>\n</head>\n<body>\n<main>\n'
            '<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Noble Father Creations</a> › Topics</nav>\n'
            f'<h1>Topics</h1>\n<p class="lede">{S.esc(desc)} Every chapter is free to read.</p>\n'
            f'<nav class="az" aria-label="Jump to a letter">{az}</nav>\n' + "\n".join(body) + "\n</main>\n"
            f'<footer><p>{S.LICENSE_LINE}</p><p><a href="/">All books</a> · <a href="/playbook/tactics">Every tactic in the Pattern Decoder</a></p></footer>\n'
            '</body>\n</html>\n')
    S.write(HUB / "topics.html", page)
    return len(order)


def main():
    sites = json.loads((S.ROOT / "sites.json").read_text())
    maps = robots()
    subprocess.run([sys.executable, str(S.ROOT / "scripts/build-root-sitemap.py")], check=True)
    n = llms(sites)
    hub_head(sites)
    nt = topics()
    sm = S.read(HUB / "sitemap.xml")
    if "/topics<" not in sm:
        S.write(HUB / "sitemap.xml", sm.replace("</urlset>", f"  <url><loc>{S.DOMAIN}/topics</loc><lastmod>{S.TODAY}</lastmod></url>\n</urlset>"))
    print(f"topics: {nt}")
    print(f"robots.txt: {len(maps)} sitemaps; llms.txt: {n} lines; hub head + og.png written")


if __name__ == "__main__":
    main()

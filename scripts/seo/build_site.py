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
           "meta-externalagent", "MistralAI-User", "CCBot", "Bingbot", "Googlebot"]


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
           'names: The Listening Room, The Sacred Divide, and the Pattern Decoder\u2019s 310 tactics.</li>\n      </ul>\n      ')
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


def main():
    sites = json.loads((S.ROOT / "sites.json").read_text())
    maps = robots()
    subprocess.run([sys.executable, str(S.ROOT / "scripts/build-root-sitemap.py")], check=True)
    n = llms(sites)
    hub_head(sites)
    print(f"robots.txt: {len(maps)} sitemaps; llms.txt: {n} lines; hub head + og.png written")


if __name__ == "__main__":
    main()

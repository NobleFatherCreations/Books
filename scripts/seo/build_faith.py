#!/usr/bin/env python3
"""The Sacred Divide: findability pass over the pages scripts/sacred-divide-site.py generates.

The Sacred Divide is already one page per tradition (34) plus a front page, so no text is split or
moved. This step adds, idempotently (every tag carries data-seo / data-seo-block):
  * title, description, canonical, Open Graph, Twitter card, JSON-LD (Book / Chapter / BreadcrumbList);
  * ids on the few headings without one;
  * a one-line notice + the licence at the foot of each tradition page, and a full notice on the front page;
  * the v6 entry in the front page's Updates, og.png and sitemap.xml.

ALWAYS run after scripts/sacred-divide-site.py (sites.json buildCommand says so), or a rebuild drops it.
Run: python3 scripts/seo/build_faith.py
"""
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import seo_common as S
from bs4 import BeautifulSoup

OUT = S.ROOT / "library/faith"
CONTACT = "dapperdadnfc@gmail.com"
BOOK = {
    "slug": "faith", "title": "The Sacred Divide", "version": "v6",
    "fonts": ["Codex Display", "Newsreader"],
    "theme": {"scheme": "dark", "bg": "#141010", "fg": "#ECE4D6", "fg2": "#BCB1A0", "panel": "#1E1817",
              "line": "#2E2624", "glow": "#33231a", "acc": "#C9A35B", "accink": "#141010",
              "disp": "'Codex Display',Georgia,serif", "body": "'Newsreader',Georgia,serif"},
    "description": ("A free, sourced record of how institutional power works inside 34 religious traditions, each held to "
                    "the same standard: leadership, money, disclosure, what leaving costs, and 30 control techniques graded "
                    "with evidence."),
    "index_title": "The Sacred Divide: How Power Works in 34 Faiths (Free, Sourced)",
    "index_desc": ("How institutional power works inside 34 religious traditions, each held to one standard and every claim "
                   "sourced. Free to read, with PDFs."),
    "genre": ["Religion", "Sociology of religion", "Investigative reference"],
    "about": ["Religious authority", "Spiritual abuse", "High-control groups", "Coercive control", "Shunning",
              "Religious freedom", "Financial transparency", "Leaving religion"],
    "keywords": ["spiritual abuse", "high-control religion", "shunning", "leaving a religion", "church financial transparency",
                 "religious trauma", "free book"],
    "notice_short": ("A sourced record of institutional teachings and practices, not a judgement of individual believers; "
                     "not legal, medical or religious advice."),
    "notice_href": "/faith#notice",
}
NOTICE_INDEX = f"""<section id="notice" data-seo-block style="max-width:44rem;margin:48px auto;padding:24px;border:1px solid #2E2624;border-radius:12px;color:#BCB1A0;font:400 1rem/1.6 'Newsreader',Georgia,serif">
<h2 id="h-notice" style="font:600 1.25rem/1.3 'Codex Display',Georgia,serif;color:#ECE4D6;margin:0 0 12px">About this record</h2>
<p style="margin:0 0 12px">The Sacred Divide describes how institutions are organized and what they teach and practise, using cited sources on every page. It is about institutions, not the faith or worth of the people in them, and it is not legal, medical or religious advice. If you are in danger, contact emergency services; each page lists help lines.</p>
<p style="margin:0 0 12px">Every page lists its sources and its own corrections. If you find an error, write to <a href="mailto:{CONTACT}" style="color:#C9A35B">{CONTACT}</a> and it will be reviewed and corrected.</p>
<p style="margin:0">{S.LICENSE_LINE}</p>
</section>"""
PAGE_FOOT = (f'<aside data-seo-block style="max-width:44rem;margin:48px auto 120px;padding:24px 16px 0;border-top:1px solid #2E2624;'
             f'color:#BCB1A0;font:400 .9375rem/1.6 \'Newsreader\',Georgia,serif"><p style="margin:0 0 8px">By Shae Stovell · Updated '
             f'<time datetime="{S.TODAY}">{S.TODAY_HUMAN}</time> · Free to read</p><p style="margin:0 0 8px">{BOOK["notice_short"]} '
             f'<a href="/faith#notice" style="color:#C9A35B">Full notice</a>.</p><p style="margin:0">{S.LICENSE_LINE}</p></aside>')
TAG = re.compile(r'[ \t]*<(?:meta|link)\b[^>]*\bdata-seo\b[^>]*>\n?|[ \t]*<script type="application/ld\+json" data-seo>.*?</script>\n?|'
                 r'\n?<(section|aside) id="notice" data-seo-block.*?</\1>|\n?<aside data-seo-block.*?</aside>', re.S)


def head_block(title, desc, url, ld, og_type):
    tags = S.head_tags(BOOK, title, desc, url, f"{S.DOMAIN}/faith/og.png", "The Sacred Divide by Shae Stovell, free to read", og_type)
    tags = "\n".join(t for t in tags.split("\n") if t and not t.startswith(("<title>", '<meta name="description"')))
    return re.sub(r"<(meta|link)\b", r"<\1 data-seo", tags) + f'\n<script type="application/ld+json" data-seo>{S.ld_json(ld)}</script>\n'


def set_title_desc(h, title, desc):
    h = re.sub(r"<title>.*?</title>", f"<title>{S.esc(title)}</title>", h, count=1, flags=re.S)
    return re.sub(r'<meta name="description"[^>]*>', f'<meta name="description" content="{S.esc(desc)}">', h, count=1)


def heading_ids(h):
    """Give the few h2/h3 without an id a readable one (no other change to the markup)."""
    def fix(m):
        tag, attrs, inner = m.group(1), m.group(2) or "", m.group(3)
        if "id=" in attrs:
            return m.group(0)
        return f'<{tag}{attrs} id="{S.slugify(re.sub("<[^>]+>", "", inner), 50)}">{inner}</{tag}>'
    return re.sub(r"<(h[23])(\s[^>]*)?>(.*?)</\1>", fix, h, flags=re.S)


def main():
    pages = sorted(p for p in OUT.glob("*.html") if p.name != "index.html")
    chs = []
    for p in pages:
        h = S.read(p)
        name = BeautifulSoup(h[:h.find("</h1>") + 5], "html.parser").find("h1").get_text(" ", strip=True)
        chs.append({"slug": p.stem, "title": name, "file": p})
    burl = f"{S.DOMAIN}/faith"
    for i, c in enumerate(chs):
        h = TAG.sub("", S.read(c["file"]))
        url = f"{burl}/{c['slug']}"
        title = S.fit_title(f"{c['title']}: How Institutional Power Works", BOOK["title"])
        desc = S.clip(f"How institutional power works in {c['title']}: size, leadership, money, disclosure and what leaving "
                      f"costs, held to one standard with every claim sourced. Free.", 158)
        crumbs = [("Noble Father Creations", S.DOMAIN + "/"), (BOOK["title"], burl), (c["title"], url)]
        ld = {"@context": "https://schema.org", "@graph": [
            {"@type": "WebPage", "@id": url, "url": url, "name": title, "description": desc, "inLanguage": "en",
             "isPartOf": {"@id": burl + "#book"}, "breadcrumb": {"@id": url + "#crumbs"}, "dateModified": S.TODAY,
             "author": {"@id": S.PERSON["@id"]}, "isAccessibleForFree": True, "license": S.LICENSE_URL,
             "about": {"@type": "Thing", "name": c["title"]}, "mainEntity": {"@id": url + "#chapter"}},
            {"@type": "Chapter", "@id": url + "#chapter", "name": c["title"], "position": i + 1, "url": url,
             "isPartOf": {"@id": burl + "#book"}, "author": {"@id": S.PERSON["@id"]}, "license": S.LICENSE_URL,
             "isAccessibleForFree": True, "inLanguage": "en", "about": {"@type": "Thing", "name": c["title"]}},
            dict(S.crumbs_ld(crumbs), **{"@id": url + "#crumbs"}), S.book_node(BOOK), S.PERSON, S.ORG]}
        h = set_title_desc(h, title, desc)
        h = h.replace("</head>", head_block(title, desc, url, ld, "article") + "</head>", 1)
        h = heading_ids(h)
        i_nf = h.find('<div id="nf-chrome"')
        h = h[:i_nf] + PAGE_FOOT + "\n" + h[i_nf:]
        S.write(c["file"], h)
    # front page
    idx = OUT / "index.html"
    h = TAG.sub("", S.read(idx))
    h = set_title_desc(h, BOOK["index_title"], BOOK["index_desc"])
    ld = {"@context": "https://schema.org", "@graph": [
        dict(S.book_node(BOOK, chs), **{"mainEntityOfPage": burl}),
        {"@type": "WebPage", "@id": burl, "url": burl, "name": BOOK["index_title"], "description": BOOK["index_desc"],
         "inLanguage": "en", "about": {"@id": burl + "#book"}, "dateModified": S.TODAY, "isAccessibleForFree": True,
         "license": S.LICENSE_URL}, S.PERSON, S.ORG]}
    h = h.replace("</head>", head_block(BOOK["index_title"], BOOK["index_desc"], burl, ld, "book") + "</head>", 1)
    h = h.replace('<footer class="updates" id="updates"', NOTICE_INDEX + '\n<footer class="updates" id="updates"', 1)
    v6 = ('<span class="ver">v6 — 2026-11-08</span><ul><li>Each tradition page now tells search engines and AI assistants '
          'exactly what it is, with a share card, so people looking for this can find it.</li><li>Added a notice on what this '
          'record is and is not, a corrections address, and the free licence (credit required, no selling).</li></ul>\n')
    if "v6 — 2026-11-08" not in h:
        h = h.replace('<span class="ver">v5 — 2026-10-27</span>', v6 + '<span class="ver">v5 — 2026-10-27</span>', 1)
    S.write(idx, h)
    S.write(OUT / "sitemap.xml", S.sitemap(BOOK, chs).replace(f"  <url><loc>{burl}/contents</loc><lastmod>{S.TODAY}</lastmod></url>\n", ""))
    tmp = S.ROOT / "library" / "_seo_tmp_faith"          # fonts are only needed to draw the share card
    (tmp / "f").mkdir(parents=True, exist_ok=True)
    try:
        S.export_fonts(S.read(idx), tmp / "f", BOOK["fonts"])
        S.make_og(BOOK, tmp, "Free · 34 traditions · every claim sourced", "How institutional power works inside the world's faiths.")
        shutil.copy(tmp / "og.png", OUT / "og.png")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"faith: {len(chs)} tradition pages + front page tagged; sitemap + og.png written")


if __name__ == "__main__":
    main()

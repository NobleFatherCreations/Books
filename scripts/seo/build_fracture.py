#!/usr/bin/env python3
"""The Fracture: one plain page per episode + findability head on the book itself.

Run:  python3 scripts/seo/build_fracture.py
Reads/writes library/fracture/. Text comes only from the book's own episode sections and
its own per-episode source lists; nothing is reworded.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import seo_common as S
from bs4 import BeautifulSoup

OUT = S.ROOT / "library/fracture"
BOOK = {
    "slug": "fracture", "title": "The Fracture", "version": "v6",
    "fonts": ["Fraunces", "Crimson Text"],
    "theme": {"scheme": "dark", "bg": "#05060B", "fg": "#ECE6D9", "fg2": "#B6AF9E", "panel": "#0E1322",
              "line": "#1B2132", "glow": "#2a1418", "acc": "#E6C570", "accink": "#05060B",
              "disp": "'Fraunces',Georgia,serif", "body": "'Crimson Text',Georgia,serif"},
    "description": ("A free twelve-episode reading edition on where roughly $50 trillion went over 43 years: who "
                    "received it, the 30 pipelines and six loops that move it, and what changes at every scale. "
                    "195 public-record sources."),
    "index_title": "The Fracture: Who Received $50 Trillion (Free Book, 195 Sources)",
    "index_desc": ("A free reading edition tracing roughly $50 trillion transferred over 43 years: who received it, "
                   "the 30 pipelines and six loops, and what changes. 195 sources."),
    "genre": ["Investigative journalism", "Economics", "Political economy"],
    "about": ["Wealth inequality", "Economic extraction", "Wealth transfer", "Regulatory capture",
              "Private equity", "Financialization", "Corporate power", "Economic history"],
    "keywords": ["where did the money go", "50 trillion transfer", "wealth inequality", "who owns America",
                 "economic extraction", "regulatory capture", "free book"],
    "notice_short": ("Analysis and commentary drawn from public records; the creator's interpretation, not "
                     "investment, legal, financial or tax advice."),
    "notice_href": "/fracture#notice",
    "unit": "episodes",
}
RELATED = [("fractal", "The Fractal", "The where and the how: one manipulation pattern at every scale"),
           ("playbook", "The Pattern Decoder", "310 manipulation and control tactics, each with signs and what to do"),
           ("loop", "The Loop", "The machine that learns you: algorithms, ad auctions and dark patterns")]


def episodes(h):
    soup = BeautifulSoup(h, "html.parser")
    secs = soup.select("section.ep")
    srcs = {g["id"]: g for g in soup.select("div.src-group")}
    id_map, chs = {}, []
    for sec in secs:
        plate = sec.select_one("header.plate")
        eyebrow = plate.select_one(".plate-eyebrow").get_text(strip=True)
        title = plate.select_one(".plate-title").get_text(" ", strip=True)
        desc_line = plate.select_one(".plate-desc").get_text(" ", strip=True)
        base = title.split(":")[0] if ":" in title else title
        slug = S.slugify(base, 48)
        link = sec.select_one(".ep-srcs a")
        src_id = link["href"][1:] if link and link.get("href", "").startswith("#src-") else None
        prose = sec.select_one(".prose") or sec
        norm = lambda s: S.slugify(s, 200)
        lede = None if norm(desc_line) in norm(title) else desc_line.rstrip(".") + "."
        chs.append({"sec": sec, "prose": prose, "eyebrow": eyebrow, "title": title, "slug": slug,
                    "lede": lede, "tagline": desc_line.rstrip(".") + ".", "src": srcs.get(src_id)})
        for el in sec.find_all(id=True):
            id_map[el["id"]] = slug
        id_map[sec["id"]] = slug
        if src_id:
            id_map[src_id] = slug
    terms = S.decoder_terms()
    for c in chs:
        page_ids = {el["id"] for el in c["prose"].find_all(id=True)}
        body = S.clean_fragment(str(c["prose"]), id_map, "fracture", page_ids)
        body = re.sub(r"<(/?)h3\b", r"<\1h2", body)          # the book's sub-heads are the page's h2s
        body, heads = S.give_heading_ids(body)
        body = S.link_terms(body, terms, limit=5)
        c["html"], c["heads"] = body, heads
        if c["src"] is not None:
            ol = c["src"].select_one("ol")
            items = [li.get_text(" ", strip=True) for li in ol.select("li")]
            c["sources_html"] = ("<ol>" + "".join(f"<li><cite>{S.esc(t)}</cite></li>" for t in items) + "</ol>"
                                 f'<p><a href="/fracture#sources">All 195 sources for the series</a></p>')
            c["citations"] = [{"@type": "CreativeWork", "name": S.clip(t, 200)} for t in items]
        elif c["eyebrow"] in ("Episode 9", "Episode 10"):
            c["sources_html"] = ('<p>The book itself notes that sources are not yet attached to this episode. '
                                 '<a href="/fracture#sources">See the full source list for the series</a>.</p>')
        c["desc"] = S.clip(f"{c['eyebrow']} of The Fracture, free to read: {c['tagline']} "
                           + S.first_sentences(c["html"], 200), 158)
        c["seo_title"] = f"{S.plain(c['title'])} · The Fracture"
        del c["sec"], c["prose"], c["src"]
    return chs


def patch_index(h, chs):
    h = S.inject_index(BOOK, h, chs)
    h = h.replace("no cookies, no personal data, nothing that leaves this domain",
                  "anonymous visit counts through Cloudflare: no cookies, no personal data")
    lic = (f'<p class="foot-lic" style="font-size:.9375rem;line-height:1.6;opacity:.85;max-width:36rem;margin:24px auto 0">'
           f'{S.LICENSE_LINE} <a href="/fracture/contents">Read it episode by episode</a>.</p>')
    h = re.sub(r'\n?<p class="foot-lic".*?</p>', "", h, flags=re.S)
    h = h.replace('<p class="foot-mark">The Fracture</p>', '<p class="foot-mark">The Fracture</p>\n  ' + lic, 1)
    reply = ("Any individual or entity named may submit written response for consideration in companion materials.")
    contact = (reply + ' Corrections and responses: <a href="mailto:dapperdadnfc@gmail.com">dapperdadnfc@gmail.com</a>.')
    if "dapperdadnfc@gmail.com" not in h:
        assert reply in h, "fracture: right-of-reply sentence not found"
        h = h.replace(reply, contact, 1)
    entry = ('<p><b>v6 &middot; November 8, 2026.</b> Every episode now also has its own page, so a search or an '
             'AI assistant can point you straight to it. Added the free licence (credit required, no selling) and '
             'clearer wording about the anonymous visit counter, and a corrections address in the legal notice.</p>')
    if "v6 &middot; November 8, 2026" not in h:
        h = h.replace('<h2>Updates</h2>\n', '<h2>Updates</h2>\n  ' + entry + "\n", 1)
    return h


def main():
    src = OUT / "index.html"
    h = S.read(src)
    chs = episodes(h)
    names = S.write_book(BOOK, h, chs, OUT, RELATED)
    S.write(src, patch_index(h, chs))
    S.make_og(BOOK, OUT, "Free to read · 12 episodes · 195 sources", "Who received fifty trillion dollars, and how.")
    print(f"fracture: {len(names)} episode pages + contents + sitemap; fonts in {OUT / 'f'}")
    for c in chs:
        print(f"  /fracture/{c['slug']:40} {len(S.plain(c['html']).split()):>6} words  {len(c['heads'])} heads  "
              f"{'sources' if c.get('citations') else '-'}")


if __name__ == "__main__":
    main()

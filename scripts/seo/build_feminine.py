#!/usr/bin/env python3
"""The Sovereign Divine Feminine: one plain page per chapter (42) plus the Preface, the 30-Minute
Rescue and the three appendices, and the findability head on the book itself.

Run: python3 scripts/seo/build_feminine.py   (reads/writes library/feminine/)
Text comes only from the book's own sections; card labels become sub-headings, nothing is reworded.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import seo_common as S
from bs4 import BeautifulSoup

OUT = S.ROOT / "library/feminine"
BOOK = {
    "slug": "feminine", "contents_eyebrow": "Free to read · 42 chapters, the Preface, the Rescue and the Archive", "title": "The Sovereign Divine Feminine", "version": "v6",
    "fonts": ["Fraunces", "Cormorant Garamond"],
    "theme": {"fs": "1.375rem", "scheme": "dark", "bg": "#140E1C", "fg": "#F8F3EB", "fg2": "#D9CDE6", "panel": "#1C1428",
              "line": "#33264A", "glow": "#3a1f3f", "acc": "#F0CC83", "accink": "#140E1C",
              "disp": "'Fraunces',Georgia,serif", "body": "'Cormorant Garamond',Georgia,serif"},
    "description": ("A free field guide to psychological manipulation for women: 42 chapters naming the tactics "
                    "(DARVO, fog, credibility theft, the digital leash, post-separation control) with counter-moves, "
                    "safety planning and identity repair."),
    "index_title": "The Sovereign Divine Feminine: Free Guide to Manipulation Tactics",
    "index_desc": ("A free field guide for women: 42 chapters naming manipulation tactics, from DARVO to post-separation "
                   "control, with counter-moves, safety planning and healing."),
    "genre": ["Self-help", "Psychology", "Relationships"],
    "about": ["Psychological manipulation", "Coercive control", "Emotional abuse", "DARVO", "Gaslighting",
              "Boundaries", "Safety planning", "Narcissistic abuse recovery", "Women's wellbeing"],
    "keywords": ["manipulation tactics", "coercive control", "DARVO", "gaslighting", "how to leave safely",
                 "boundaries", "free book for women"],
    "audience": {"@type": "PeopleAudience", "audienceType": "Women experiencing or recovering from manipulation and coercive control"},
    "notice_short": ("For education only: not medical, psychological, legal or financial advice. If you fear physical "
                     "harm, put safety first; in immediate danger, contact emergency services."),
    "notice_href": "/feminine#copyright",
    "unit": "chapters",
}
RELATED = [("playbook", "The Pattern Decoder", "310 manipulation and control tactics, each with signs and what to do"),
           ("children", "Playground Protectors", "Shaela's guide for brave kids: tricky people, power and friendship"),
           ("faith", "The Sacred Divide", "Coercive control inside faith communities, tradition by tradition")]

PROMOTE = [("section.ch-open", "drop"), ("p.c-tag", "h3"), ("div.beat-head", "h3"), ("p.cheat-name", "h3"),
           ("p.dr-part-head", "h3"), ("p.sub-label", "strong"), ("div.aside", "blockquote"),
           ("p.eyebrow", "drop"), ("i.ch-end", "drop"), ("div.ch-tags", "drop"), ("p.ch-meta", "drop")]


def is_stop(n):
    cls = n.get("class") or []
    return n.name == "section" or "part-div" in cls or "end-plate" in cls or n.name == "footer"


def build_chapters(h):
    soup = BeautifulSoup(h[h.find("<body"):], "html.parser")
    pages, movement = [], "Before you begin"
    order = []
    for el in soup.find_all(["section"]):
        if el.find_parent("section"):
            continue
        cls = el.get("class") or []
        sid = el.get("id") or ""
        if "part-div" in cls:
            kick = el.select_one(".part-kicker")
            name = el.select_one(".part-name")
            movement = (f"{kick.get_text(strip=True)}: {name.get_text(strip=True)}" if kick and name
                        else el.get_text(" ", strip=True))
            continue
        if "ch-open" in cls:
            title = S.title_case(el.select_one(".ch-title").get_text(" ", strip=True))
            eyebrow = el.select_one(".ch-kicker").get_text(strip=True)
            body = collect_until(el, is_stop)
            order.append(dict(id=sid, title=title, eyebrow=eyebrow, movement=movement, raw=body))
        elif sid in ("preface", "rescue-body", "apB", "apC"):
            h2 = el.find("h2")
            title = S.title_case(h2.get_text(" ", strip=True))
            eb = el.select_one(".eyebrow")
            eyebrow = eb.get_text(" ", strip=True).lstrip("🧭⟡✦❧🤝🚨🧘🗝️🗂️📜🛠️© ").strip() if eb else ""
            inner = BeautifulSoup(str(el), "html.parser").section
            inner.find("h2").decompose()
            mv = "The Archive" if sid.startswith("ap") else ("Part Zero: The 30-Minute Rescue" if sid == "rescue-body" else movement)
            order.append(dict(id=sid, title=title, eyebrow=eyebrow, movement=mv, raw="".join(str(x) for x in inner.children)))
    # slugs + id map
    id_map = {}
    for c in order:
        base = c["title"].split("—")[-1].strip() if c["title"].startswith("Appendix") else c["title"].split(":")[0]
        c["slug"] = S.slugify(base, 52)
        for m in re.finditer(r'id="([^"]+)"', c["raw"]):
            id_map[m.group(1)] = c["slug"]
        id_map[c["id"]] = c["slug"]
    terms = S.decoder_terms()
    for c in order:
        frag = S.promote(c["raw"], PROMOTE)
        page_ids = set(re.findall(r'id="([^"]+)"', frag))
        body = S.clean_fragment(frag, id_map, "feminine", page_ids)
        body, heads = S.give_heading_ids(body, "")
        body = S.link_terms(body, terms, limit=5)
        c["html"], c["heads"] = body, heads
        mission = BeautifulSoup(c["raw"], "html.parser").select_one(".card-concept p:not(.c-tag)")
        c["lede"] = mission.get_text(" ", strip=True) if mission else None
        what = f"{c['eyebrow']}: " if c["eyebrow"].startswith("Chapter") else ""
        c["desc"] = S.clip(f"{what}{c['lede'] or S.first_sentences(body, 150)}", 158)
        if len(c["desc"]) < 70:
            c["desc"] = S.clip(c["desc"] + " " + S.first_sentences(body, 120), 158)
        c["seo_title"] = c["title"]
        del c["raw"]
    return order


collect_until = S.collect_until


def patch_index(h, chs):
    h = S.inject_index(BOOK, h, chs)
    h = h.replace("no cookies, no personal data, nothing that leaves this domain",
                  "anonymous visit counts through Cloudflare: no cookies, no personal data")
    # the copyright panel shipped with an unfilled template line; it becomes the licence
    h = re.sub(r"Copyright \(c\) \[Year\] \[Author Name\]\. All rights reserved\.", S.LICENSE_LINE, h)
    if S.LICENSE_URL not in h:
        raise SystemExit("feminine: licence line not placed (copyright template not found)")
    # the author note named the children's book by its old title
    h = h.replace("Shaela’s Playground Book of Spells: How to Level Up and Become a Better Friend",
                  '<a href="https://noblefathercreations.com/children">Playground Protectors</a>')
    h = h.replace("Copyright &amp;amp; Disclaimer", "Copyright &amp; Disclaimer").replace("Establish &amp;amp; Enforce", "Establish &amp; Enforce")
    h = h.replace('can increase risk in volatile or violent</p><ul class="dots"><li>situations.</li></ul>',
                  'can increase risk in volatile or violent situations.</p>')
    entry = ('<p><strong class="lead">v6 &middot; November 8, 2026.</strong> Every chapter, the 30-Minute Rescue and the appendices now also have '
             'their own pages, so a search or an AI assistant can point you straight to the one you need '
             '(<a href="/feminine/contents">see them all</a>). The copyright note now carries the free licence '
             '(credit required, no selling), the children\'s book is called by its current name, and the visit-counter '
             'wording is clearer.</p>')
    return h, entry


def main():
    src = OUT / "index.html"
    h = S.read(src)
    h = (h.replace("Copyright &amp;amp; Disclaimer", "Copyright &amp; Disclaimer").replace("Establish &amp;amp; Enforce", "Establish &amp; Enforce")
          .replace('can increase risk in volatile or violent</p><ul class="dots"><li>situations.</li></ul>', 'can increase risk in volatile or violent situations.</p>'))
    for f in OUT.glob("*.html"):
        if f.name != "index.html":
            f.unlink()          # rebuild from scratch so renamed pages leave no orphans
    chs = build_chapters(h)
    S.write_book(BOOK, h, chs, OUT, RELATED)
    h2, entry = patch_index(h, chs)
    if "v6 &middot; November 8, 2026" not in h2:
        anchor = '<h2 class="h-sec">Updates</h2>\n'
        assert anchor in h2, "feminine: updates heading not found"
        h2 = h2.replace(anchor, anchor + "  " + entry + "\n", 1)
    S.write(src, h2)
    S.make_og(BOOK, OUT, "Free field guide · 42 chapters", "Psychological manipulation: tactics, names and counter-moves.")
    print(f"feminine: {len(chs)} pages")
    for c in chs:
        print(f"  {c['movement'][:28]:28} /feminine/{c['slug']:44} {len(S.plain(c['html']).split()):>5}w {len(c['heads']):>3}h")


if __name__ == "__main__":
    main()

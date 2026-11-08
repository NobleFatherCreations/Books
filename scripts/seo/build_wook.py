#!/usr/bin/env python3
"""The Festie Codex: one plain page per chapter (33), the front-of-book essays, the author's confession,
and every appendix long enough to stand on its own; plus the findability head on the book itself.

Run: python3 scripts/seo/build_wook.py   (reads/writes library/wook/; audio/ and video/ are untouched)
Text is the book's own; poster labels become headings, nothing is reworded.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import seo_common as S
from bs4 import BeautifulSoup

OUT = S.ROOT / "library/wook"
BOOK = {
    "slug": "wook", "title": "The Festie Codex", "version": "v15",
    "alternateName": "The Festie Codex: A Field Manual for Spotting Wooks in Sheep's Clothing",
    "fonts": ["Fraunces", "Bricolage Grotesque"],
    "theme": {"scheme": "dark", "bg": "#0D0918", "fg": "#F4EDDA", "fg2": "#CFC6E6", "panel": "#17122B",
              "line": "#2A2346", "glow": "#2b1a52", "acc": "#FFD94A", "accink": "#0D0918",
              "disp": "'Fraunces',Georgia,serif", "body": "'Bricolage Grotesque',system-ui,sans-serif"},
    "description": ("A free field manual for the festival scene: 33 chapters on spotting manipulators, predators and "
                    "coercive groups at festivals and raves, plus harm reduction, consent, drug-checking, bad trips, "
                    "the next twelve hours after an assault, and recovery."),
    "index_title": "The Festie Codex: Free Festival Safety & Manipulation Guide",
    "index_desc": "A free field manual for festivals and raves: spot manipulators and predators, plus harm reduction, consent, bad trips, drug checking and aftercare.",
    "genre": ["Harm reduction", "Self-help", "Psychology"],
    "about": ["Festival safety", "Rave safety", "Harm reduction", "Consent", "Coercive control", "Drug checking",
              "Sexual assault aftercare", "Cults and high-control groups", "Manipulation tactics"],
    "keywords": ["festival safety guide", "rave safety", "harm reduction", "how to help someone having a bad trip",
                 "festival predators", "consent at festivals", "free book"],
    "notice_short": ("Harm-reduction information, not medical, psychological or legal advice; laws vary by place. "
                     "People in the stories are composites. In crisis, call or text 988, or text HOME to 741741."),
    "notice_href": "/wook#copyright",
    "unit": "chapters and appendices",
}
RELATED = [("festival", "The Festie Bible", "Twelve guides for staying safe and kind in the festival world"),
           ("playbook", "The Pattern Decoder", "310 manipulation and control tactics, each with signs and what to do"),
           ("feminine", "The Sovereign Divine Feminine", "A field guide to manipulation tactics and counter-moves")]

FRONT = ["before-we-roll", "cast", "lexicon", "methodology", "real-ones"]
STOP_IDS = re.compile(r"^(intermission-\d|ap[A-Z]|appendixes|acknowledgments|wook-confession|about|loop|updates|copyright|end)$")
PROMOTE = [("p.comp-title", "h2"), ("p.plain-tag", "h3"), ("p.spec-name", "h3"), ("p.sub-tag", "h3"), ("div.rail", "drop"), ("div.ebars", "drop"), ("p.poster-part", "drop"), ("p.poster-num", "drop"),
           ("p.poster-meta", "drop"), ("p.script-note", "drop"), ("h2.zine-h", "drop")]
INNER = [("h3", "h2"), ("h4", "h3")]


def structure(frag):
    """Codex labels -> real headings: component titles, Track names, counter-drops, specimen names."""
    soup = BeautifulSoup(frag, "html.parser")
    for x in soup.select("span.comp-emo, span.track-emo, span.cd-icon, span.ph-emo"):
        x.decompose()
    for th in soup.select("div.track-head"):
        tag = th.select_one(".track-tag")
        ttl = th.select_one(".track-title") or th.find_next_sibling(class_="track-title")
        if ttl is not None and ttl.parent is th.parent and ttl is not th:
            ttl = ttl.extract()
        new = soup.new_tag("h2")
        new.string = (f"{S.title_case(tag.get_text(strip=True))}: " if tag else "") + S.title_case(ttl.get_text(" ", strip=True) if ttl else th.get_text(" ", strip=True))
        th.replace_with(new)
    for cd in soup.select("div.cd-head"):
        tag, name = cd.select_one(".cd-tag"), cd.select_one(".cd-name")
        new = soup.new_tag("h3")
        new.string = (f"{S.title_case(tag.get_text(strip=True))}: " if tag else "") + (name.get_text(" ", strip=True) if name else "")
        cd.replace_with(new)
    return str(soup)


def is_stop(n):
    cls = n.get("class") or []
    return "ch-poster" in cls or bool(STOP_IDS.match(n.get("id") or "")) or n.name == "footer"


def words(html):
    return len(S.plain(html).split())


def build(h):
    soup = BeautifulSoup(h[h.find("<body"):], "html.parser")
    order, movement = [], "Before the gates open"
    for el in soup.find_all("section"):
        if el.find_parent("section"):
            continue
        cls = el.get("class") or []
        sid = el.get("id") or ""
        if "setdiv" in cls:
            movement = el.get_text(" | ", strip=True).split(" | ")[0]
            movement = S.title_case(movement) if sid != "appendixes" else "The Archive: Appendices"
            continue
        if "ch-poster" in cls:
            title = S.title_case(el.select_one(".poster-title").get_text(" ", strip=True))
            sub_el = el.select_one(".poster-and")
            sub = S.title_case(sub_el.get_text(" ", strip=True)) if sub_el else None
            keys = el.select_one(".poster-keys")
            order.append(dict(id=sid, title=title, lede=sub, eyebrow=f"Chapter {sid[2:]}", movement=movement,
                              keys=S.title_case(keys.get_text(" ", strip=True)) if keys else "",
                              raw=S.collect_until(el, is_stop)))
        elif sid in FRONT or sid == "wook-confession" or (re.match(r"^ap[A-Z]$", sid)):
            h2 = el.find("h2")
            heading = re.sub(r"^[^\w“\"(]+", "", h2.get_text(" ", strip=True)).strip()
            if sid.startswith("ap"):
                letter, _, name = heading.partition("—")
                title, eyebrow = S.title_case(name.strip()), S.title_case(letter.strip())
            else:
                title, eyebrow = S.title_case(heading), ("From the author" if sid == "wook-confession" else "Before the gates open")
            note = el.select_one(".script-note")
            inner = BeautifulSoup(str(el), "html.parser").section
            inner.find("h2").decompose()
            raw = "".join(str(x) for x in inner.children)
            if words(raw) < 120:
                continue          # too thin to stand alone; stays in the book
            order.append(dict(id=sid, title=title, eyebrow=eyebrow,
                              lede=note.get_text(" ", strip=True).lstrip("— ").strip() if note else None,
                              movement=("Before the gates open" if sid in FRONT else
                                        "Encore — Protect the Magic" if sid == "wook-confession" else movement),
                              raw=raw))
    # the confession sits after chapter 29 in the book
    conf = next((c for c in order if c["id"] == "wook-confession"), None)
    if conf:
        order.remove(conf)
        i = next(i for i, c in enumerate(order) if c["id"] == "ch29")
        order.insert(i + 1, conf)
    id_map = {}
    for c in order:
        c["slug"] = S.slugify(c["title"].split(":")[0], 52)
        for m in re.finditer(r'id="([^"]+)"', c["raw"]):
            id_map[m.group(1)] = c["slug"]
        id_map[c["id"]] = c["slug"]
    seen = {}
    for c in order:                              # unique slugs (an appendix may share a chapter's name)
        if c["slug"] in seen:
            c["slug"] = f"{c['slug']}-{c['eyebrow'].lower().replace(' ', '-')}"
        seen[c["slug"]] = 1
    terms = S.decoder_terms()
    for c in order:
        frag = S.promote(structure(c["raw"]), PROMOTE)
        page_ids = set(re.findall(r'id="([^"]+)"', frag))
        body = S.clean_fragment(frag, id_map, "wook", page_ids)
        body, heads = S.give_heading_ids(body)
        body = S.link_terms(body, terms, limit=5)
        c["html"], c["heads"] = body, heads
        if c["eyebrow"].startswith("Chapter"):
            cand = f"{c['title']}: {c['lede']}" if c.get("lede") and ":" not in c["title"] else c["title"]
            c["seo_title"] = cand if len(cand) <= 65 else c["title"]
            c["desc"] = S.clip(f"{c['eyebrow']} of The Festie Codex, free: {c['lede'] + '. ' if c.get('lede') else ''}"
                               + (f"Covers {c['keys'].replace(' · ', ', ')}." if c.get("keys") else S.first_sentences(body, 120)), 158)
        else:
            c["seo_title"] = c["title"]
            c["desc"] = S.clip(f"{c['title']}, from The Festie Codex (free): " + (c.get("lede") or S.first_sentences(body, 120)), 158)
        for k in ("raw", "keys"):
            c.pop(k, None)
    return order


def patch_index(h, chs):
    h = S.inject_index(BOOK, h, chs)
    h = h.replace("<p>Copyright © 2026 by Shae Stovell</p>", f"<p>{S.LICENSE_LINE}</p>")
    h = re.sub(r"<p>All rights reserved\. No part of this book may be reproduced, distributed, or transmitted in any form "
               r"or by any means, including photocopying, recording, or other electronic or mechanical methods, without "
               r"the prior written permission of the publisher, except in the case of brief quotations embodied in critical "
               r"reviews and certain other noncommercial uses permitted by copyright law\.</p>",
               "<p>You may copy and share this book for free, as long as you credit Shae Stovell, don’t sell it, and don’t "
               "share changed versions. Every chapter also has its own page: "
               '<a href="/wook/contents">noblefathercreations.com/wook/contents</a>.</p>', h)
    if S.LICENSE_URL not in h:
        raise SystemExit("wook: licence line not placed")
    entry = ('<p><strong class="lead">v15 · November 8, 2026.</strong> Every chapter, the opening essays, the confession '
             'and the bigger appendices now also have their own pages, so a search or an AI assistant can send someone '
             'straight to the part they need, like the Good Samaritan guide or the next-twelve-hours chapter '
             '(<a href="/wook/contents">see them all</a>). The book is now free to share under a Creative Commons licence '
             '(credit to the author, no selling).</p>')
    if "v15 · November 8, 2026" not in h:
        anchor = re.search(r'(<section class="panel pp-yellow prose" id="updates">.*?</div>)', h, re.S)
        h = h[:anchor.end()] + entry + h[anchor.end():]
    return h


def main():
    src = OUT / "index.html"
    h = S.read(src)
    for f in OUT.glob("*.html"):
        if f.name != "index.html":
            f.unlink()
    chs = build(h)
    S.write_book(BOOK, h, chs, OUT, RELATED)
    S.write(src, patch_index(h, chs))
    S.make_og(BOOK, OUT, "Free field manual · 33 chapters", "Spot the Wooks. Protect the magic. Get everyone home.")
    print(f"wook: {len(chs)} pages; index {src.stat().st_size/1e6:.2f} MB")
    for c in chs:
        print(f"  {c['movement'][:24]:24} /wook/{c['slug']:40} {len(S.plain(c['html']).split()):>6}w {len(c['heads']):>3}h  {c['seo_title'][:62]}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Playground Protectors: one plain page per mission (28) plus the grown-ups' note, the Power-Up
Master Guide, the glossary, the feelings index, the cheat sheets, the pledge and the resources.

Run: python3 scripts/seo/build_children.py   (reads/writes library/children/)
The book's gamified design stays exactly as it is (BOOKS.md: this book WANTS gamification);
the plain pages are only an extra way in. Text is the book's own; nothing is reworded.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import seo_common as S
from bs4 import BeautifulSoup

OUT = S.ROOT / "library/children"
BOOK = {
    "slug": "children", "contents_eyebrow": "Free to read · 28 missions and the toolkit", "title": "Playground Protectors", "version": "v6",
    "alternateName": "Shaela's Complete Guide to Tricky People, Power-Ups, and Real Friendships",
    "fonts": ["Baloo 2", "Nunito"],
    "theme": {"scheme": "light", "bg": "#FFFEFA", "fg": "#221A4A", "fg2": "#4A4470", "panel": "#FFF7E8",
              "line": "#E9E1F7", "glow": "#C7E9FF", "acc": "#4A30B8", "accink": "#FFFFFF",
              "disp": "'Baloo 2',system-ui,sans-serif", "body": "'Nunito',system-ui,sans-serif"},
    "description": ("A free illustrated book for kids ages 5 and up about tricky people: 28 missions that teach children to spot "
                    "manipulation (\"that didn't happen\", guilt trips, secrets, exclusion), with Power-Ups to say and "
                    "do, and notes for the grown-ups reading along."),
    "index_title": "Playground Protectors: Free Kids' Book on Tricky People (Ages 5+)",
    "index_desc": ("A free illustrated book for kids 5+: 28 missions to spot tricky people and manipulation, "
                   "with Power-Ups to say and do, and notes for parents and teachers."),
    "genre": ["Children's literature", "Social-emotional learning", "Child safety"],
    "about": ["Child safety", "Manipulation", "Bullying", "Friendship", "Gaslighting", "Peer pressure",
              "Boundaries", "Social-emotional learning", "Online safety"],
    "keywords": ["kids book about manipulation", "teach kids about tricky people", "gaslighting for kids",
                 "bullying book for kids", "friendship skills", "free children's book"],
    "audience": {"@type": "PeopleAudience", "audienceType": "Children ages 5 and up, and the parents, teachers and counselors who read with them", "suggestedMinAge": 5},
    "typicalAgeRange": "5-",
    "notice_short": ("For kids and the grown-ups reading with them; not a substitute for professional, medical, legal or "
                     "mental-health advice. If a child is in danger, call emergency services. Childhelp: <span style=\"white-space:nowrap\">1-800-422-4453</span>."),
    "notice_href": "/children#copyright",
    "unit": "missions and guides",
}
RELATED = [("feminine", "The Sovereign Divine Feminine", "The grown-up field guide: manipulation tactics and counter-moves"),
           ("playbook", "The Pattern Decoder", "310 manipulation and control tactics, each with signs and what to do"),
           ("festival", "The Festie Bible", "Twelve guides for staying safe and kind in the festival world")]

PROMOTE = [("div.panel-head", "h2"), ("div.pu-burst", "drop"), ("div.pu-name", "h3"), ("span.move-tag", "drop"),
           ("span.say-lab", "strong"), ("div.saybubble", "blockquote"), ("div.res-h", "h3"), ("div.plate-tag", "drop"),
           ("div.cast", "drop"), ("div.m-top", "drop"), ("div.wb-dots", "drop"), ("p.plate-lead", "drop")]


def is_stop(n):
    cls = n.get("class") or []
    return (n.name == "header" and "mission" in cls) or n.name == "footer" or (
        n.name == "section" and ("worldbar" in cls or "plate" in cls or n.get("id") in
                                 ("powerguide", "glossary", "feelings", "cheatsheets", "pledge", "resources", "parents-tip", "about", "updates", "copyright")))


def build(h):
    soup = BeautifulSoup(h[h.find("<body"):], "html.parser")
    order, world = [], "Before the missions"
    for el in soup.find_all(["section", "header"]):
        if el.find_parent(["section", "header"]):
            continue
        cls = el.get("class") or []
        sid = el.get("id") or ""
        if "worldbar" in cls:
            world = (f"{S.title_case(el.select_one('.wb-eyebrow').get_text(strip=True))}: "
                     f"{S.title_case(el.select_one('.wb-title').get_text(strip=True))}")
        elif el.name == "header" and "mission" in cls:
            title = S.title_case(el.select_one(".m-title").get_text(" ", strip=True))
            sub = el.select_one(".m-sub").get_text(" ", strip=True)
            eyebrow = S.title_case(el.select_one(".m-world").get_text(" ", strip=True)).replace("Mission 0", "Mission ")
            raw = S.collect_until(el, is_stop)
            order.append(dict(id=sid, title=title, sub=sub, eyebrow=eyebrow, movement=world,
                              raw=raw, kid=str(el) + raw))
        elif sid in ("note", "powerguide", "glossary", "feelings", "cheatsheets", "pledge", "resources"):
            h2 = el.find("h2")
            title = h2.get_text(" ", strip=True).replace("’", "’")
            tag = el.select_one(".plate-tag")
            lead = el.select_one(".plate-lead")
            inner = BeautifulSoup(str(el), "html.parser").section
            inner.find("h2").decompose()
            order.append(dict(id=sid, title=title, sub=lead.get_text(" ", strip=True) if lead else None,
                              eyebrow=S.title_case(tag.get_text(strip=True)) if tag else "",
                              movement="For the grown-ups" if sid in ("note", "resources") else "The toolkit",
                              raw="".join(str(x) for x in inner.children), kid=str(el)))
    # the grown-ups' note reads first; toolkit and resources after the four worlds
    order.sort(key=lambda c: (0 if c["id"] == "note" else 2 if c["movement"] in ("The toolkit", "For the grown-ups") else 1))
    id_map = {}
    for c in order:
        c["slug"] = S.slugify(c["title"].split(":")[0], 52)
        for m in re.finditer(r'id="([^"]+)"', c["raw"]):
            id_map[m.group(1)] = c["slug"]
        id_map[c["id"]] = c["slug"]
    for c in order:
        frag = S.promote(c["raw"], PROMOTE)
        page_ids = set(re.findall(r'id="([^"]+)"', frag))
        body = S.clean_fragment(frag, id_map, "children", page_ids)
        body, heads = S.give_heading_ids(body)
        c["html"], c["heads"] = body, heads
        c["lede"] = c.pop("sub")
        if c["eyebrow"].startswith("World"):
            plain_sub = re.sub(r"^A Guide to (the )?", lambda m: "The " if m.group(1) else "", c["lede"]).strip()
            cand = f"{c['title']}: {plain_sub}"
            c["seo_title"] = cand if len(cand) <= 65 else c["title"]
            c["desc"] = S.clip(f"{c['eyebrow']} of Playground Protectors, a free book for kids: {c['lede']}. "
                               + S.first_sentences(body, 120), 158)
        else:
            c["seo_title"] = c["title"]
            c["desc"] = S.clip(f"{c['title']}, from Playground Protectors, a free book for kids and grown-ups: "
                               + (c["lede"] or S.first_sentences(body, 120)), 158)
        del c["raw"]
    return order


# ---------------------------------------------------------------- kid-style pages (owner, 2026-11-08: "as kid as
# possible, for 5+"): the plain pages keep the book's OWN mission markup, pictures, fonts and stylesheet.
KID_FONTS = ["Fraunces", "Bangers", "Baloo 2", "Nunito", "Patrick Hand"]
KID_CSS = """
.kp{max-width:46rem;margin:0 auto;padding:0 16px}
.cbar{max-width:46rem}
.cbar .bk{font:400 1.375rem/1.1 var(--shout);letter-spacing:.04em;color:var(--grapeD)}
.cbar .open{background:var(--grape);color:#fff;font:700 1rem/1 var(--disp);box-shadow:0 4px 0 var(--grapeD);transition:transform .2s ease,box-shadow .2s ease}
.cbar .open:hover{transform:translateY(-2px);box-shadow:0 6px 0 var(--grapeD)}
main#text{max-width:46rem;font-family:var(--body)}
.crumbs{font:700 1rem/1.4 var(--disp);margin:0 0 16px}.crumbs a,.crumbs li{color:var(--inkSoft)}
.byline{font:700 .9375rem/1.5 var(--disp);color:var(--inkSoft);margin:16px 0 8px}
.aka{font:700 .875rem/1.5 var(--disp);color:var(--inkSoft);margin:8px 0 16px}
.notice{background:#fff;border:3px dashed var(--sun);border-left-width:3px;border-radius:16px;padding:12px 16px;font:600 .875rem/1.5 var(--body);color:var(--inkSoft);margin:0 0 32px}
.kid-say{display:flex;gap:16px;align-items:flex-start;margin:24px 0}
.kid-say .cast-img{flex:none;width:72px;height:72px;border-radius:50%;border:4px solid #fff;box-shadow:0 4px 0 var(--grapeD);background-size:cover;background-position:center}
.kid-say .bubble{position:relative;flex:1;background:#fff;border:3px solid var(--grape);border-radius:24px;padding:16px 20px;box-shadow:0 6px 0 var(--grapeD)}
.kid-say .bubble::before{content:"";position:absolute;left:-14px;top:24px;border:12px solid transparent;border-right-color:var(--grape);border-left:0}
.kid-say h2{font:400 1.375rem/1.1 var(--shout);letter-spacing:.05em;color:var(--grape);margin:0 0 8px}
.kid-say p{margin:0;font:700 1.1875rem/1.6 var(--body);color:var(--ink)}
article.kid-mission{margin:24px 0}
article.kid-mission h2.panel-head{margin:0;font:inherit}
.pn a{background:#fff;border:3px solid var(--sky-deep);border-radius:20px;box-shadow:0 5px 0 var(--sky-deep);color:var(--ink)}
.pn a:hover{background:#fff;transform:translateY(-2px)}
.pn b{font:800 1.125rem/1.25 var(--disp)}
.rel{border-top:3px dotted var(--grape)}.rel h2{font:400 1.5rem/1.1 var(--shout);letter-spacing:.05em;color:var(--grape)}
.list a b{font:800 1.125rem/1.3 var(--disp)}
.mv{font:400 1.5rem/1.1 var(--shout);letter-spacing:.06em;color:var(--grape)}
.foot{font-family:var(--disp)}
.subhead.trick,.move-tag,.lv3 .lv-head{color:#B3261E!important}
.say-lab,.lv1 .lv-head{color:#0A6B49!important}
.lv2 .lv-head{color:#8A5300!important}
.story-tag{background:#4A30B8!important;color:#fff!important}
.plate-tag{color:#fff!important}
.note-who,.pl-title{color:#8A5300!important}
.big{color:#B3261E!important}
/* readable small text: the book's darker accents, one step deeper on these pages (bright colours unchanged) */
article.kid-mission{--coralD:#B3261E;--sunD:#8A5300;--mintD:#0A6B49}
.fc-word{color:#B3261E!important}
.story,.pucard,.feelcard,.thermo,.tipbox{border-color:#F2A613!important}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
"""


def export_book_assets(h):
    """book.css = the book's own stylesheet, its embedded pictures written out as files, fonts subset."""
    import base64, hashlib
    css = re.search(r"<style>([\s\S]*?)</style>", h[h.find("</title>"):]).group(1)
    css += "\n" + re.search(r'<style id="pp-fx">([\s\S]*?)</style>', h).group(1)
    img = OUT / "img"
    img.mkdir(exist_ok=True)
    def out(m):
        kind, data = m.group(1), base64.b64decode(m.group(2))
        name = hashlib.md5(data).hexdigest()[:12] + "." + kind.split("/")[1].replace("svg+xml", "svg")
        (img / name).write_bytes(data)
        return f"url(/children/img/{name})"
    css = re.sub(r"""url\(["']?data:(image/[a-z+]+);base64,([A-Za-z0-9+/=]+)["']?\)""", out, css)
    fonts = S.export_fonts(h, OUT / "f", KID_FONTS)
    S.write(OUT / "book.css", fonts + "\n" + css)


def kid_page(path, c):
    """Swap the plain article for the book's own mission markup and dress the page in the book's style."""
    page = S.read(path)
    soup = BeautifulSoup(page, "html.parser")
    main = soup.find("main")
    for sel in ("h1", ".eyebrow", ".lede", ".toc"):
        for el in main.select(sel):
            el.decompose()
    kid = BeautifulSoup(c["kid"], "html.parser")
    for x in kid.select("script, input, button, .wb-dots"):
        x.decompose()
    for fig in kid.select('figure[role="group"]'):
        del fig["role"]                          # a figure already has its own role
    for ph in kid.select("div.panel-head"):
        ph.name = "h2"
    t = kid.select_one(".m-title") or kid.find("h2")
    t.name = "h1"
    t["id"] = "top"
    art = soup.new_tag("article")
    art["class"] = "kid-mission"
    art.append(BeautifulSoup(S.give_heading_ids(str(kid))[0], "html.parser"))
    soup.find("article").replace_with(art)
    # the plain-words box becomes Shaela's speech bubble, right under the mission card
    plain = main.select_one("section.plain")
    if plain:
        txt = plain.find("p").get_text()
        plain.decompose()
        bubble = BeautifulSoup(
            '<section class="kid-say" aria-labelledby="plain-h"><span class="cast-img av-shaela" role="img" aria-label="Shaela"></span>'
            f'<div class="bubble"><h2 id="plain-h">In plain words</h2><p>{S.esc(txt)}</p></div></section>', "html.parser")
        hdr = art.find(["header", "section"])
        hdr.insert_after(bubble)
    aka = main.select_one("p.aka")
    if aka:
        aka.string = "For grown-ups, also known as: " + ", ".join(c.get("aka") or [])
        aka.extract()
        art.find(["header", "section"]).insert_after(aka)
    # card first, then the bubble, then the small print: byline and the grown-ups' notice
    after = art.select_one("section.kid-say") or art.find(["header", "section"])
    for sel in ("p.notice", "p.byline"):
        el = main.select_one(sel)
        if el:
            after.insert_after(el.extract())
    head = soup.find("head")
    pre = "".join(f'<link rel="preload" href="/children/f/{f}" as="font" type="font/woff2" crossorigin>'
                  for f in ("bangers-400-normal.woff2", "baloo-2-1-999-normal.woff2", "nunito-1-999-normal.woff2"))
    head.append(BeautifulSoup(pre + '<link rel="stylesheet" href="/children/book.css">', "html.parser"))
    style = soup.new_tag("style")
    style.string = KID_CSS
    head.append(style)
    S.write(path, str(soup))


def patch_index(h, chs):
    h = S.inject_index(BOOK, h, chs)
    h = h.replace("no cookies, no personal data, nothing that leaves this domain",
                  "anonymous visit counts through Cloudflare: no cookies, no personal data")
    # the cover is a picture with the title in it; give the page its one real <h1> without changing the look
    h = re.sub(r'\n?<h1 class="sr-title"[^>]*>.*?</h1>', "", h, flags=re.S)
    h = h.replace('<section class="cover" id="top">',
                  '<section class="cover" id="top">\n<h1 class="sr-title" style="position:absolute;width:1px;height:1px;'
                  'overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap">Playground Protectors: Shaela’s Complete Guide '
                  'to Tricky People, Power-Ups, and Real Friendships</h1>', 1)
    # licence replaces "All rights reserved" and the no-reproduction clause it contradicts
    h = h.replace("<p>© 2026 Shae Stovell · Noble Father Creations. All rights reserved.</p>",
                  f"<p>{S.LICENSE_LINE}</p>")
    h = re.sub(r"<p>No part of this book may be reproduced, distributed, or transmitted in any form without the prior "
               r"written permission of the author, except for brief quotations in reviews and certain other noncommercial "
               r"uses permitted by copyright law\.</p>",
               "<p>You may copy and share this book for free, as long as you name Shae Stovell as the author, don’t sell it, "
               "and don’t share changed versions. Read it chapter by chapter at "
               '<a href="/children/contents">noblefathercreations.com/children/contents</a>.</p>', h)
    if S.LICENSE_URL not in h:
        raise SystemExit("children: licence line not placed")
    entry = ('<p><b>v6 · November 8, 2026.</b> Every mission and guide now also has its own page, so a parent or teacher '
             'searching for help can land right on it (<a href="/children/contents">see them all</a>). The book is now '
             'free to share under a Creative Commons licence (credit to the author, no selling), and the visit-counter '
             'wording is clearer.</p>')
    if "v6 · November 8, 2026" not in h:
        h = h.replace('<div class="plate-tag">UPDATES</div>', '<div class="plate-tag">UPDATES</div> ' + entry, 1)
    return h


def main():
    src = OUT / "index.html"
    h = S.read(src)
    for f in OUT.glob("*.html"):
        if f.name != "index.html":
            f.unlink()
    chs = build(h)
    export_book_assets(h)
    S.write_book(BOOK, h, chs, OUT, RELATED)
    for c in chs:
        kid_page(OUT / f"{c['slug']}.html", c)
    S.write(src, patch_index(h, chs))
    S.make_og(BOOK, OUT, "Free book for kids · 28 missions", "Spot the trick. Use your Power-Ups. Ask for help.")
    print(f"children: {len(chs)} pages")
    for c in chs:
        print(f"  {c['movement'][:26]:26} /children/{c['slug']:36} {len(S.plain(c['html']).split()):>5}w {len(c['heads']):>3}h  {c['seo_title'][:60]}")


if __name__ == "__main__":
    main()

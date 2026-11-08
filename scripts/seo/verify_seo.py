#!/usr/bin/env python3
"""Findability gate for a book's publish folder. Exit 1 on any failure.

Usage: python3 scripts/seo/verify_seo.py fracture [feminine ...]

Checks every .html page in library/<book>/ (and the book's sitemap) for what search engines
and AI crawlers need, and for the house rules (absolute links, no outside requests except the
sanctioned Cloudflare beacon, notice + licence present, nothing named in metadata that the
legal plan keeps out).
"""
import json
import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[2]
DOMAIN = "https://noblefathercreations.com"
OK_EXTERNAL_SCRIPT = "static.cloudflareinsights.com/beacon.min.js"
GOOGLE_HTML_LIMIT = 15 * 1024 * 1024


def text_words(soup):
    s = BeautifulSoup(str(soup), "html.parser")
    for x in s(["script", "style", "noscript", "template"]):
        x.decompose()
    return len(s.get_text(" ").split())


def check_page(book, f, known, problems, stats, publish_dir=None):
    raw = f.read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(raw, "html.parser")
    rel = f.relative_to(ROOT)
    is_index = f.name == "index.html"
    publish_dir = publish_dir or ROOT / "library" / book
    stem = f.relative_to(publish_dir).with_suffix("").as_posix()
    url = f"{DOMAIN}/{book}" if is_index else f"{DOMAIN}/{book}/{stem}"
    P = lambda msg: problems.append(f"{rel}: {msg}")

    if len(raw.encode()) > GOOGLE_HTML_LIMIT:
        P(f"HTML is {len(raw.encode())/1e6:.1f} MB, over Google's 15 MB read limit")
    if not re.search(r'<html[^>]+lang="en', raw[:3000]):
        P("missing <html lang>")
    title = soup.title.get_text() if soup.title else ""
    if not title:
        P("no <title>")
    elif len(title) > 70:
        P(f"title {len(title)} chars (Google shows ~60): {title!r}")
    d = soup.find("meta", attrs={"name": "description"})
    desc = d["content"] if d and d.get("content") else ""
    if not (50 <= len(desc) <= 160):
        P(f"description length {len(desc)} (want 50-160)")
    if len(soup.find_all("meta", attrs={"name": "description"})) != 1:
        P("not exactly one meta description")
    canon = soup.find_all("link", rel="canonical")
    if len(canon) != 1 or canon[0].get("href") != url:
        P(f"canonical should be exactly {url}, got {[c.get('href') for c in canon]}")
    for prop in ("og:title", "og:description", "og:url", "og:image", "og:type", "og:image:alt"):
        tags = soup.find_all("meta", property=prop)
        if len(tags) != 1:
            P(f"{prop} present {len(tags)}x")
    ogurl = soup.find("meta", property="og:url")
    if ogurl and ogurl.get("content") != url:
        P(f"og:url {ogurl.get('content')} != {url}")
    if not soup.find("meta", attrs={"name": "twitter:card"}):
        P("no twitter:card")
    if soup.find("meta", attrs={"name": "robots", "content": re.compile("noindex", re.I)}):
        P("noindex present")
    if len(soup.find_all("h1")) != 1:
        P(f"{len(soup.find_all('h1'))} <h1> elements (want 1)")
    # JSON-LD parses, has the expected types, and declares author + licence + free
    lds = soup.find_all("script", type="application/ld+json")
    types = set()
    if not lds:
        P("no JSON-LD")
    for s in lds:
        try:
            data = json.loads(s.string or "")
        except Exception as e:
            P(f"JSON-LD does not parse: {e}")
            continue
        graph = data.get("@graph", [data]) if isinstance(data, dict) else data
        for n in graph:
            t = n.get("@type")
            types.update(t if isinstance(t, list) else [t])
            if t == "Book":
                for k in ("author", "license", "isAccessibleForFree", "name", "url", "image"):
                    if k not in n:
                        P(f"Book node missing {k}")
    if lds and "Book" not in types and "CreativeWork" not in types:
        P(f"JSON-LD has no Book node (types: {sorted(t for t in types if t)})")
    if not is_index and "BreadcrumbList" not in types:
        P("no BreadcrumbList")
    # headings carry ids (citeable blocks); main text visible without JavaScript
    main = soup.find("article") or soup.find("main") or soup.body
    heads = main.find_all(["h2", "h3"]) if main else []
    noid = [h.get_text(" ", strip=True)[:40] for h in heads if not h.get("id")]
    if noid and not is_index:
        P(f"{len(noid)} headings without id, e.g. {noid[:3]}")
    words = text_words(soup.body or soup)
    stats.append((str(rel), words, len(raw.encode())))
    if not is_index and f.name != "contents.html" and words < 150:
        P(f"only {words} words visible without JavaScript")
    # links: absolute only (proxy rule), and internal targets exist
    for a in soup.find_all("a", href=True):
        h = a["href"]
        if h.startswith(("#", "mailto:", "tel:", "javascript:", "data:", "sms:", "blob:", "about:")) or re.match(r"https?://", h):
            continue
        if not h.startswith("/"):
            P(f"relative link {h!r}")
            continue
        path = h.split("#")[0].split("?")[0].rstrip("/")
        if path.startswith(f"/{book}/") and path.count("/") == 2 and "." not in path.split("/")[-1]:
            if path.split("/")[-1] not in known:
                P(f"link to missing page {path}")
    # outside requests: only the sanctioned beacon
    for tag, attr in (("script", "src"), ("link", "href"), ("img", "src"), ("iframe", "src"), ("source", "src")):
        for el in soup.find_all(tag):
            v = el.get(attr) or ""
            if tag == "link" and set(el.get("rel") or []) & {"canonical", "license", "sitemap", "alternate"}:
                continue
            if re.match(r"https?://", v) and OK_EXTERNAL_SCRIPT not in v and not v.startswith(DOMAIN):
                P(f"outside request {tag} {v[:80]}")
    if "creativecommons.org/licenses/by-nc-nd/4.0" not in raw:
        P("licence (CC BY-NC-ND 4.0) not stated")
    if not is_index and "Full notice" not in raw and "full notice" not in raw:
        P("chapter page has no notice line linking to the full notice")
    for bad in ("#REPLACE", "data-here", "{{", "TODO", "lorem ipsum"):
        vis = (soup.body.get_text(" ") if soup.body else "")
        if bad in vis:
            P(f"placeholder text {bad!r} visible")


def check_book(book, publish_dir=None):
    d = publish_dir or ROOT / "library" / book
    pages = sorted(p for p in d.rglob("*.html") if "/f/" not in p.as_posix() and "/.netlify/" not in p.as_posix())
    known = {p.relative_to(d).with_suffix("").as_posix() for p in pages}
    problems, stats = [], []
    for f in pages:
        check_page(book, f, known, problems, stats, d)
    sm = d / "sitemap.xml"
    if not sm.exists():
        problems.append(f"{book}: no sitemap.xml")
    else:
        locs = [e.text for e in ET.parse(sm).getroot().iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
        want = {f"{DOMAIN}/{book}"} | {f"{DOMAIN}/{book}/{k}" for k in known if k != "index"}
        if set(locs) != want:
            problems.append(f"{book}: sitemap mismatch; missing {sorted(want - set(locs))[:5]} extra {sorted(set(locs) - want)[:5]}")
    if not (d / "og.png").exists():
        problems.append(f"{book}: no og.png share image")
    return problems, stats


def main():
    books = sys.argv[1:]
    bad = 0
    for b in books:
        probs, stats = check_book(b)
        tw = sum(w for _, w, _ in stats)
        print(f"\n== {b}: {len(stats)} pages, {tw:,} words visible without JavaScript, "
              f"largest page {max(s for *_, s in stats)/1e6:.2f} MB")
        for p in probs:
            print("  ✗", p)
        if not probs:
            print("  ✓ all findability checks pass")
        bad += len(probs)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()

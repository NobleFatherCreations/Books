#!/usr/bin/env python3
"""seo-audit checklist across every page of the seven books: duplicate titles/descriptions (site-wide),
heading-level skips, H1 vs title alignment, orphans (not linked from contents/index), images without alt,
near-duplicate bodies. Usage: python3 scripts/seo/audit_onpage.py"""
import re, sys, collections, hashlib
from pathlib import Path
from bs4 import BeautifulSoup
ROOT = Path(__file__).resolve().parents[2]
BOOKS = ["fracture", "feminine", "children", "wook", "fractal", "festival", "faith"]
titles, descs, bodies = collections.defaultdict(list), collections.defaultdict(list), collections.defaultdict(list)
skips, misalign, noalt, orphans = [], [], [], []
for b in BOOKS:
    d = ROOT / "library" / b
    pages = sorted(p for p in d.glob("*.html"))
    hub = (d / "contents.html") if (d / "contents.html").exists() else d / "index.html"
    linked = set(re.findall(rf'href="/{b}/([a-z0-9-]+)', hub.read_text(encoding="utf-8")))
    for p in pages:
        h = p.read_text(encoding="utf-8", errors="ignore")
        s = BeautifulSoup(h, "html.parser")
        t = s.title.get_text().strip(); titles[t].append(f"{b}/{p.stem}")
        m = s.find("meta", attrs={"name": "description"}); descs[m["content"] if m else ""].append(f"{b}/{p.stem}")
        if p.name not in ("index.html",):
            last = 1
            for hh in s.select("main h1, main h2, main h3, main h4, article h2, article h3, article h4"):
                lvl = int(hh.name[1])
                if lvl > last + 1: skips.append(f"{b}/{p.stem}: h{last}→h{lvl} '{hh.get_text(strip=True)[:40]}'"); break
                last = lvl
            h1 = s.find("h1").get_text(" ", strip=True)
            if h1.lower()[:20] not in t.lower() and p.name != "contents.html": misalign.append(f"{b}/{p.stem}: h1 '{h1[:40]}' vs title '{t[:50]}'")
            if p.name not in ("contents.html",) and p.stem not in linked and b != "faith": orphans.append(f"{b}/{p.stem}")
            art = s.find("article")
            if art: bodies[hashlib.md5(re.sub(r"\s+", " ", art.get_text(" ")).encode()).hexdigest()].append(f"{b}/{p.stem}")
        for img in s.find_all("img"):
            if not img.get("alt") and img.get("alt") != "" : noalt.append(f"{b}/{p.stem}: {str(img)[:80]}")
dup_t = {k: v for k, v in titles.items() if len(v) > 1}
dup_d = {k: v for k, v in descs.items() if len(v) > 1}
dup_b = [v for v in bodies.values() if len(v) > 1]
print("pages:", sum(len(v) for v in titles.values()))
print("duplicate titles:", len(dup_t)); [print("  ", k[:70], v[:4]) for k, v in list(dup_t.items())[:12]]
print("duplicate descriptions:", len(dup_d)); [print("  ", k[:70], v[:4]) for k, v in list(dup_d.items())[:6]]
print("identical bodies:", len(dup_b), dup_b[:5])
print("heading skips:", len(skips)); [print("  ", x) for x in skips[:8]]
print("h1/title misalign:", len(misalign)); [print("  ", x) for x in misalign[:8]]
print("orphans (not linked from contents):", len(orphans), orphans[:8])
print("images without alt:", len(noalt)); [print("  ", x) for x in noalt[:6]]

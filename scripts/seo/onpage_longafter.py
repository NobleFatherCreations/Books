#!/usr/bin/env python3
"""On-page SEO audit for library/<book> (python3 scripts/seo/onpage_longafter.py [book], default longafter) (seo-audit checklist): titles, descriptions, H1, heading order,
canonical, keyword in first 100 words, click depth from the book index, orphans, anchor text, duplicate titles,
keyword cannibalisation (two pages with the same primary keyword). Exit 1 on any failure."""
import re, sys, json, collections
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]; B = sys.argv[1] if len(sys.argv) > 1 else "longafter"; D = ROOT / f"library/{B}"
plan = json.load(open(ROOT / f"content/{B}-v2/plan.json"))
chs = [c for s in plan["sections"] for c in s["chapters"]] if "sections" in plan else plan["chapters"]
kw = {c["slug"]: c["keyword"].lower() for c in chs}
pages = {p.stem: p.read_text() for p in D.glob("*.html")}
idx = {k: v for k, v in pages.items() if 'content="noindex' not in v}
fails, warns = [], []
titles, descs = collections.defaultdict(list), collections.defaultdict(list)
links = collections.defaultdict(set)
for s, h in pages.items():
    for t in re.findall(rf'href="/{B}/([a-z0-9-]+)', h):
        links[s].add(t)
for s, h in idx.items():
    t = __import__("html").unescape(re.search(r"<title>(.*?)</title>", h).group(1)); titles[t].append(s)
    d = __import__("html").unescape(re.search(r"<meta name=\"description\" content=\"([^\"]*)\"", h).group(1)); descs[d].append(s)
    if not 30 <= len(t) <= 65: warns.append(f"{s}: title {len(t)} chars")
    if not 70 <= len(d) <= 160: warns.append(f"{s}: description {len(d)} chars")
    if len(re.findall(r"<h1[\s>]", h)) != 1: fails.append(f"{s}: h1 count")
    lv = [int(x) for x in re.findall(r"<h([1-6])[\s>]", re.sub(r'<nav class="nf-.*?</nav>', "", h, flags=re.S))]
    for a, b in zip(lv, lv[1:]):
        if b > a + 1: fails.append(f"{s}: heading skip h{a}->h{b}"); break
    if f'<link rel="canonical" href="https://noblefathercreations.com/{B}{"" if s=="index" else "/"+s}"' not in h:
        fails.append(f"{s}: canonical")
    if s in kw:
        m = re.search(r'<main id="text">(.*?)</main>', h, re.S)
        txt = re.sub(r"<[^>]+>", " ", m.group(1) if m else "").lower()
        first = " ".join(txt.split()[:110]).replace("’", "'")
        k = kw[s].replace("’", "'")
        if k not in first and not all(w in first for w in k.split() if len(w) > 3):
            warns.append(f"{s}: keyword '{k}' not in first 100 words")
    for a in re.findall(rf'<a [^>]*href="/{B}/[^"]*"[^>]*>(.*?)</a>', h, re.S):
        if re.sub(r"<[^>]+>", "", a).strip().lower() in ("click here", "here", "read more", "this"):
            warns.append(f"{s}: weak anchor '{a[:20]}'")
for t, ss in titles.items():
    if len(ss) > 1: fails.append(f"duplicate title: {ss}")
for d, ss in descs.items():
    if len(ss) > 1: fails.append(f"duplicate description: {ss}")
cann = collections.defaultdict(list)
for s, k in kw.items(): cann[k].append(s)
for k, ss in cann.items():
    if len(ss) > 1: fails.append(f"cannibalisation '{k}': {ss}")
# click depth from index (BFS over in-book links, every page incl. contents/search)
depth, q = {"index": 0}, ["index"]
while q:
    s = q.pop(0)
    for t in links.get(s, ()):
        if t in pages and t not in depth: depth[t] = depth[s] + 1; q.append(t)
deep = sorted((d, s) for s, d in depth.items() if d > 3)
for s in idx:
    if s not in depth: fails.append(f"{s}: unreachable from index")
inbound = collections.Counter(t for s, ts in links.items() for t in ts if t != s)
orph = [s for s in idx if s != "index" and inbound[s] < 2]
for s in orph: fails.append(f"{s}: fewer than 2 inbound links")
print(f"{B} on-page: {len(idx)} indexable pages; max click depth {max(depth.values())}; pages deeper than 3: {len(deep)}")
for w in warns: print("  warn", w)
for f in fails: print("  FAIL", f)
print("  ✓ on-page checks pass" if not fails else f"  {len(fails)} failures")
sys.exit(1 if fails else 0)

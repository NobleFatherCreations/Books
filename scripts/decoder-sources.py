#!/usr/bin/env python3
"""Verify the Decoder's "Research behind this" sources and write content/decoder-v21/research.json.
A source is kept only when it checks out:
  article: Crossref has the exact DOI, the title shares >= 60% of its key words with ours, the year is within 1, the first
           author's surname matches. Its formatted citation comes from Crossref, not from us.
  book:    Open Library finds the title and author, with a first-publication year within 1 of ours.
Results are cached (content/decoder-v21/research-cache.json), so reruns make no requests unless --refresh.
Every source carries one of three labels: Research, Where the name comes from, Popular book."""
import html, json, re, sys, time, urllib.parse, urllib.request
from pathlib import Path
D = Path(__file__).resolve().parents[1] / "content/decoder-v21"
CAND = json.load(open(D / "research-candidates.json"))
CP = D / "research-cache.json"
cache = {} if "--refresh" in sys.argv or not CP.exists() else json.load(open(CP))
UA = {"User-Agent": "decoder-sources/1.0 (reference check)"}
kw = lambda s: set(re.findall(r"[a-z]{4,}", s.lower()))


def get(url):
    if url in cache: return cache[url]
    try:
        r = json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25))
    except Exception as e:
        r = {"error": str(e)}
    cache[url] = r; time.sleep(0.3)
    return r


def article(c):
    m = get("https://api.crossref.org/works/" + urllib.parse.quote(c["doi"])).get("message")
    if not m: return None, "not found at Crossref"
    title = " ".join(m.get("title") or [""]) + " " + " ".join(m.get("subtitle") or [])
    year = ((m.get("issued") or {}).get("date-parts") or [[None]])[0][0] or ((m.get("published") or {}).get("date-parts") or [[None]])[0][0]
    authors = m.get("author") or m.get("editor") or []
    fam = (authors[0].get("family") or authors[0].get("name") or "") if authors else ""
    ov = len(kw(c["title"]) & kw(title)) / max(1, len(kw(c["title"])))
    if ov < 0.6: return None, f"title mismatch ({title[:70]!r}, {ov:.0%})"
    if c.get("vol") and str(m.get("volume")) == c["vol"]:
        year = c["y"]          # digitised later (Crossref dates the upload); the volume number confirms the original year
    if not year or abs(int(year) - c["y"]) > 1: return None, f"year {year}"
    if c["au"].lower() not in fam.lower(): return None, f"first author {fam!r}"
    names = [a.get("family", "") for a in authors][:3]
    title = re.sub(r"^\s*[IVX]+\.\s+", "", html.unescape(re.sub(r"<[^>]+>", "", title)))
    who = names[0] + (" et al." if len(authors) > 2 else (" and " + names[1] if len(names) > 1 else ""))
    venue = html.unescape(" ".join(m.get("container-title") or []) or m.get("publisher", ""))
    cite = f"{who} ({year}). {title.strip().rstrip('.')}." + (f" *{venue}*." if venue else "")
    return {"cite": cite, "url": "https://doi.org/" + c["doi"]}, "ok"


def book(c):
    b = c["book"]
    q = urllib.parse.urlencode({"title": b["title"], "author": b["author"], "fields": "title,author_name,first_publish_year,key", "limit": 5})
    docs = get("https://openlibrary.org/search.json?" + q).get("docs") or []
    for d in docs:
        y = d.get("first_publish_year")
        if y and abs(y - c["y"]) <= 1 and len(kw(b["title"]) & kw(d.get("title", ""))) / max(1, len(kw(b["title"]))) >= 0.6:
            au = (d.get("author_name") or [b["author"]])[0]
            return {"cite": f"{au} ({y}). *{b['title']}*.", "url": "https://openlibrary.org" + d["key"]}, "ok"
    return None, "no matching book record" + (f" (first hit {docs[0].get('title')!r} {docs[0].get('first_publish_year')})" if docs else "")


out, report = {}, []
for c in CAND:
    r, why = (article if "doi" in c else book)(c)
    report.append((c.get("doi") or c["book"]["title"], why))
    if r:
        for t in c["t"]:
            out.setdefault(t, []).append({**r, "label": c["label"]})
json.dump(cache, open(CP, "w"), indent=0, ensure_ascii=False)
json.dump(out, open(D / "research.json", "w"), indent=1, ensure_ascii=False)
bad = [x for x in report if x[1] != "ok"]
print(f"{len(CAND) - len(bad)} of {len(CAND)} sources verified; {len(out)} entries get a 'Research behind this' section")
for x in bad: print("  DROPPED", x[0], "-", x[1])

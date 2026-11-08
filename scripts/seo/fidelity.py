#!/usr/bin/env python3
"""Prove chapter pages carry the book's own words: every paragraph / list item / quote on every
generated page must appear verbatim (whitespace-normalised) in the original book source.
Usage: python3 scripts/seo/fidelity.py <book> <original index.html or git rev:path> [extra source files...]"""
import re, subprocess, sys, html, warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from pathlib import Path
from bs4 import BeautifulSoup
ROOT = Path(__file__).resolve().parents[2]
book, src, *extra = sys.argv[1:]
def load(s):
    if ":" in s and not Path(s).exists():
        return subprocess.run(["git", "show", s], capture_output=True, text=True, cwd=ROOT).stdout
    return Path(s).read_text(encoding="utf-8", errors="ignore")
def norm(t):
    t = html.unescape(t).replace(" ", " ")
    return re.sub(r"\s+", "", t)          # compare without whitespace: tag boundaries change spacing, never letters
corpus = ""
for s in [src] + extra:
    raw = load(s)
    soup = BeautifulSoup(raw, "html.parser")
    for x in soup(["style"]): x.decompose()
    corpus += norm(soup.get_text(" ")) + norm(raw)   # raw too: JS-held text (chapter data) counts as the book's
    try:                                              # and JS/JSON string escapes decoded (\" \u2019 \n)
        corpus += norm(raw.replace(chr(92) + "/", "/").encode("latin-1", "backslashreplace").decode("unicode_escape", "ignore").encode("latin-1", "ignore").decode("utf-8", "ignore"))
    except Exception:
        pass
    corpus += norm(raw.replace(chr(92) + '"', '"').replace(chr(92) + "'", "'"))
pages = [p for p in (ROOT / "library" / book).rglob("*.html") if p.name not in ("index.html", "contents.html")]
checked = missing = 0
bad = []
for p in sorted(pages):
    art = BeautifulSoup(p.read_text(encoding="utf-8"), "html.parser").select_one("article")
    if not art: continue
    for el in art.find_all(["p", "li", "blockquote", "td", "dd"]):
        if el.find(["p", "li"]): continue
        t = el.get_text("")
        lead = el.find(["strong", "b"], recursive=False)
        if lead is not None and t.strip().startswith(lead.get_text().strip()):
            t = t.strip()[len(lead.get_text().strip()):]   # a book label set in bold before the text
        if len(t.strip()) < 12: continue
        checked += 1
        if norm(t) not in corpus:
            missing += 1
            bad.append(f"{p.name}: {t.strip()[:110]}")
print(f"{book}: {checked} text blocks on {len(pages)} pages; {checked - missing} found verbatim in the book; {missing} not found")
for b in bad[:15]: print("   ✗", b)
sys.exit(1 if missing else 0)

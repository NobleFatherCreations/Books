#!/usr/bin/env python3
"""Plain text of the published books, one file per chapter, for reading without the HTML.
    python3 design/fractal2/reports/corpus_extract.py fractal fracture faith
Writes content/fractal2/library-review/text/<book>/<chapter>.txt (git-ignored) and prints a size table.
Keeps <cite> sources and the page's notice lines, so the data and the safeguards can be reviewed too."""
import html, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "content/fractal2/library-review/text"


def text_of(path):
    h = path.read_text(encoding="utf-8", errors="ignore")
    h = re.sub(r"(?s)<(script|style|svg|nav|template)\b.*?</\1>", "", h)
    m = re.search(r"(?s)<main\b.*?</main>", h)
    h = m.group(0) if m else h
    h = re.sub(r'(?s)<cite\b[^>]*>(.*?)</cite>', r" [source: \1] ", h)
    h = re.sub(r'(?i)<a\b[^>]*href="(https?://[^"]+)"[^>]*>(.*?)</a>', r"\2 <\1>", h)
    h = re.sub(r"(?i)<(h[1-6])\b[^>]*>", "\n\n## ", h)
    h = re.sub(r"(?i)<(p|li|blockquote|tr|div|section|br|figcaption)\b[^>]*>", "\n", h)
    h = html.unescape(re.sub(r"<[^>]+>", "", h))
    h = re.sub(r"[ \t]+", " ", h)
    return re.sub(r"\n\s*\n+", "\n\n", h).strip()


total = 0
for book in sys.argv[1:] or ["fractal", "fracture", "faith"]:
    d = OUT / book
    d.mkdir(parents=True, exist_ok=True)
    n = 0
    for f in sorted((ROOT / "library" / book).glob("*.html")):
        t = text_of(f)
        (d / (f.stem + ".txt")).write_text(t)
        w = len(t.split()); n += w
        print(f"{book:9s} {f.stem:44s} {w:7d} words  {len(re.findall(r'source:', t)):3d} sources")
    total += n
    print(f"{book:9s} TOTAL {n} words, about {int(n * 1.35 / 1000)}k tokens\n")
print("ALL", total, "words, about", int(total * 1.35 / 1000), "k tokens")

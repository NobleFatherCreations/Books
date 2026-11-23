#!/usr/bin/env python3
"""Prove a markup-only change kept every word: compare the reader-visible text of built pages.

  python3 scripts/book/text-diff.py snap library/longafter /path/before.json     save the text of every page
  python3 scripts/book/text-diff.py check library/longafter /path/before.json    compare; exit 1 on any difference
Text = the page with <script>/<style> removed, tags stripped and whitespace collapsed. "check" also reports whether
the HTML differs only by added <div class="blk ..."> / </div> lines.
"""
import html, json, re, sys
from pathlib import Path


def text(h):
    h = re.sub(r"<(script|style)\b.*?</\1>", " ", h, flags=re.S | re.I)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", h))).strip()


def strip_blocks(h):
    return re.sub(r'\n?<div class="blk blk-[a-z]+"(?: data-arg="[^"]*")?>|\n?</div>(?=\n|$|</article>)', "", h)


def main():
    mode, d, snap = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
    pages = {f.name: f.read_text(encoding="utf-8") for f in sorted(d.glob("*.html"))}
    if mode == "snap":
        snap.write_text(json.dumps({k: {"text": text(v), "html": v} for k, v in pages.items()}))
        print(f"saved {len(pages)} pages")
        return
    before = json.loads(snap.read_text())
    bad_text, bad_html = [], []
    for k in sorted(set(before) | set(pages)):
        if k not in pages or k not in before:
            bad_text.append(f"{k}: page {'added' if k in pages else 'missing'}"); continue
        if text(pages[k]) != before[k]["text"]:
            a, b = before[k]["text"].split(" "), text(pages[k]).split(" ")
            i = next((n for n, (x, y) in enumerate(zip(a, b)) if x != y), min(len(a), len(b)))
            bad_text.append(f"{k}: words differ near: ...{' '.join(a[max(0, i-8):i+8])}... vs ...{' '.join(b[max(0, i-8):i+8])}...")
        if strip_blocks(pages[k]) != strip_blocks(before[k]["html"]):
            bad_html.append(k)
    print(f"{len(pages)} pages compared; reader text differs on {len(bad_text)}; HTML differs beyond block wrappers on {len(bad_html)}")
    for x in bad_text[:20]:
        print("  TEXT", x)
    for x in bad_html[:20]:
        print("  HTML", x)
    sys.exit(1 if bad_text else 0)


if __name__ == "__main__":
    main()

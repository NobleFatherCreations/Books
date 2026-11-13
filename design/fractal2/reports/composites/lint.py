#!/usr/bin/env python3
"""Punctuation and capitalization check for composites.html (the same text the PDF is made from).
Flags: blocks that start in lowercase; a sentence that starts in lowercase after . ! ? or a closing quote; stray spaces before punctuation;
missing spaces after punctuation; doubled punctuation; unbalanced double quotes; repeated words; paragraphs with no end punctuation.
Intentional exceptions are whitelisted below (dialogue tags after ! or ?, the owner's ellipsis, abbreviations).
Usage: python3 lint.py [composites.html]   (exit 1 if any issue is found)"""
import re, sys, html, pathlib
HERE = pathlib.Path(__file__).parent
src = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "composites.html"
doc = src.read_text()
doc = re.sub(r"<style.*?</style>", "", doc, flags=re.S)
doc = re.sub(r'<span class="mk">.*?</span>', "", doc)
# split into blocks at block-level tags
blocks = re.split(r"</?(?:p|li|td|th|h[1-6]|blockquote|div|section|tr|ol|ul|table|i|b|span)[^>]*>", doc)
# rebuild blocks properly: only split on real block tags, keep inline tags inside text
BLOCK = re.compile(r"<(p|li|td|th|h[1-6]|blockquote)\b[^>]*>(.*?)</\1>", re.S)
texts = []
for m in BLOCK.finditer(doc):
    t = re.sub(r"<[^>]+>", "", m.group(2))
    t = re.sub(r"\s+", " ", html.unescape(t)).strip()
    if t: texts.append((m.group(1), t))
for m in re.finditer(r'<div class="(?:spot|say|tc|chain|sl)\b[^>]*>(.*?)</div>', doc, re.S):
    t = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", m.group(1)))).strip()
    if t: texts.append(("div", t))

sys.path.insert(0, str(HERE))
from textutil import titlecase
heads = []
for m in re.finditer(r"<h3[^>]*>(.*?)</h3>", doc, re.S): heads.append(re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", m.group(1)))).strip())
for m in re.finditer(r'<div class="sl"><span>(.*?)</span>', doc, re.S): heads.append(html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip())
for m in re.finditer(r'<td class="n">\d+</td><td><b>.*?</b></td><td>(.*?)</td>', doc, re.S): heads.append(html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip())
ABBR = r"(?:a\.m|p\.m|e\.g|i\.e|Mr|Mrs|Ms|Dr|St|vs|etc|No|U\.S|Jr|Sr)"
issues = []
for h in dict.fromkeys(heads):
    if titlecase(h.replace("\u2019", "'")) != h.replace("\u2019", "'"): issues.append(("heading not in Title Case", f"{h}  ->  {titlecase(h.replace(chr(0x2019), chr(39)))}"))
def flag(kind, text, ctx=None):
    issues.append((kind, (ctx or text)[:140]))

for tag, t in texts:
    if re.match(r"^qa\d+|^qz\d+", t): continue
    # 1. block starts in lowercase (labels like "tactic" headers are capitalised in the source; list items too)
    if re.match(r"^[a-z]", t): flag("starts lowercase", t)
    # 2. sentence starts lowercase
    for m in re.finditer(r"([.!?]+)([\"'\u201d\u2019)\]]*)\s+([a-z])", t):
        punct, quote, nxt = m.groups()
        before = t[:m.start()]
        if len(punct) >= 3 or before.endswith("."): continue                                   # the owner's ellipsis: "just... how things were"
        if re.search(ABBR + r"$", before + punct[:1]): continue
        if punct[-1] in "!?" and "\u201d" in quote: continue                                  # dialogue tag: "Good!" you tell the secretary
        flag("sentence starts lowercase", t, t[max(0, m.start() - 30):m.end() + 40])
    # 3. spacing and doubled punctuation
    for pat, kind in [(r" [,;:](?!\))", "space before punctuation"), (r"(?<!\.)\.\.(?!\.)", "two dots"), (r",,", "double comma"),
                      (r"[a-z][.!?][A-Z][a-z]", "no space after sentence end"), (r"[a-z],[A-Za-z]", "no space after comma"), (r"\b(\w+) \1\b", "repeated word")]:
        for m in re.finditer(pat, t):
            s = m.group(0)
            if kind == "repeated word" and s.lower().split()[0] in ("that", "had", "ha", "no", "so", "very"): continue
            if kind == "space before punctuation" and re.search(r"\d \:", t[max(0, m.start() - 2):m.end()]): continue
            if kind == "no space after sentence end" and re.search(r"(a\.m|p\.m|e\.g|i\.e|Fractal)", t[max(0, m.start() - 4):m.end()]): continue
            flag(kind, t, t[max(0, m.start() - 30):m.end() + 30])
    # 4. quotes: display text must use typographic quotes, balanced, with no closing quote at the start of a block or after a space
    if '"' in t or "'" in t: flag("straight quote left in display text", t)
    if t.count("\u201c") != t.count("\u201d") and tag in ("h3", "th", "td"): flag("unbalanced double quotes", t)
    if re.search(r"(^|\s)\u201d", t) and not re.search(r"\u201c", t[:t.find("\u201d")]) and tag != "td": flag("closing quote used as an opening quote", t)
    if re.search(r"\u201c\s", t) or re.search(r"\s\u201d", t): flag("space inside a quotation mark", t)
    # 5. standalone lowercase i
    if re.search(r"(?<![A-Za-z'])i(?![A-Za-z'.])", t) and tag != "th": flag("lowercase i", t)
    # 6. paragraphs without end punctuation (full sentences only)
    if tag == "p" and len(t) > 60 and not re.search(r"[.!?:\u2026][\"'\u201d\u2019)\]]*$", t): flag("no end punctuation", t, t[-60:])

if issues:
    seen = set(); out = []
    for k, c in issues:
        if (k, c) in seen: continue
        seen.add((k, c)); out.append((k, c))
    for k, c in out: print(f"{k:28s} | {c}")
    print(f"\n{len(out)} issue(s) in {len(texts)} text blocks")
    sys.exit(1)
print(f"punctuation check passed: {len(texts)} text blocks, no issues")

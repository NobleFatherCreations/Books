#!/usr/bin/env python3
"""Proofreading scan over a book's rendered chapter text.

Doubled words, spacing around punctuation, unbalanced quotes and brackets,
stray HTML entities, digits written inconsistently, and the escape sequences
these files store text in leaking through as literal characters.
"""
import re, sys, collections

path = sys.argv[1]
s = open(path, encoding="utf-8").read()
js = s.split('<script id="book-js">')[1].split("</script>")[0]
bodies = re.findall(r"BODIES\[(\d+)\]=`([\s\S]*?)`;", js)

def render(b):
    t = b
    for a, c in [("\\u2014","—"),("\\u2019","’"),("\\u201c","“"),("\\u201d","”"),
                 ("\\u2018","‘"),("\\u2192","→"),("\\u00b7","·"),("\\u2026","…"),
                 ("\\u00e9","é"),("\\u2013","–")]:
        t = t.replace(a, c)
    t = t.replace("&mdash;","—").replace("&rsquo;","’").replace("&ldquo;","“") \
         .replace("&rdquo;","”").replace("&amp;","&").replace("&nbsp;"," ")
    return re.sub(r"<[^>]+>", " ", t)

CHECKS = [
 ("doubled word",        r"\b(\w{3,})\s+\1\b"),
 ("space before punct",  r"\s+[,.;:!?](?:\s|$)"),
 ("missing space after", r"[,;:](?=[A-Za-z])"),
 ("double space in text",r"[^\s]  +[^\s]"),
 ("leaked escape",       r"\\u[0-9a-fA-F]{4}"),
 ("leaked entity",       r"&[a-z]{2,8};"),
 ("unclosed bracket",    r"\([^)]{160,}"),
 ("straight apostrophe", r"[a-z]'[a-z]"),
 ("double punctuation",  r"[.,;:]{2,}"),
 ("space before close",  r"\s+[”’)]"),
 ("lowercase sentence",  r"(?<=[.!?])\s+[a-z]{2,}"),
]

counts = collections.Counter()
for n, b in bodies:
    t = render(b)
    for label, rx in CHECKS:
        for m in re.finditer(rx, t):
            counts[label] += 1
            if counts[label] <= 4:
                ctx = re.sub(r"\s+", " ", t[max(0, m.start()-55):m.end()+55])
                print(f"  ch{n} [{label}] …{ctx}…")
# quote balance, per chapter
for n, b in bodies:
    t = render(b)
    if t.count("“") != t.count("”"):
        print(f"  ch{n} [quote imbalance] {t.count('“')} open vs {t.count('”')} close")
        counts["quote imbalance"] += 1

print(f"\n{path}")
for k, v in counts.most_common():
    print(f"  {k:22} {v}")
if not counts:
    print("  clean")

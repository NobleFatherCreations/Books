#!/usr/bin/env python3
"""Structural profile of a book: movements, chapter lengths, device use, routing."""
import re, sys, json, statistics

path = sys.argv[1]
s = open(path, encoding="utf-8").read()
js = s.split('<script id="book-js">')[1].split("</script>")[0]

bodies = {int(n): b for n, b in re.findall(r"BODIES\[(\d+)\]=`([\s\S]*?)`;", js)}
movs = re.findall(r"\{n:'([^']*)',t:'([^']*)'[^}]*?c:\[([\d,]+)\]", js)
if not movs:
    movs = [(m[0], m[1], m[2]) for m in re.findall(r"n:'([^']*)'\s*,\s*t:'([^']*)'[\s\S]{0,200}?c:\[([\d,]+)\]", js)]

print(f"== {path}")
print(f"chapters: {len(bodies)}   movements: {len(movs)}")
lens = {n: len(b.split()) for n, b in bodies.items()}
v = list(lens.values())
print(f"words/chapter: min {min(v)}  median {int(statistics.median(v))}  mean {int(statistics.mean(v))}  max {max(v)}")
print()
for num, title, cl in movs:
    ch = [int(x) for x in cl.split(",")]
    tot = sum(lens.get(c, 0) for c in ch)
    print(f"  {num:5} {title[:52]:54} ch {ch[0]:>2}-{ch[-1]:<3} ({len(ch):2})  {tot:5}w  {tot//len(ch):4}w/ch")
print()
# device distribution
for dev, rx in [("pull", r'class="pull"'), ("try", r'class="try"'), ("warn", r'class="warn"'), ("h3", r"<h3"), ("ul/ol", r"<[uo]l")]:
    n = sum(len(re.findall(rx, b)) for b in bodies.values())
    inch = sum(1 for b in bodies.values() if re.search(rx, b))
    print(f"  {dev:7} {n:4} total, in {inch}/{len(bodies)} chapters ({inch*100//len(bodies)}%)")
print()
# chapter body shape signature
shapes = {}
for n, b in bodies.items():
    sig = "".join(re.findall(r"<(p|h3|div class=\"(?:pull|try|warn)\"|ul|ol)", b))
    sig = re.sub(r'div class="(\w+)"', r'\1', sig)
    shapes.setdefault(sig, []).append(n)
top = sorted(shapes.items(), key=lambda kv: -len(kv[1]))[:5]
print("  most-repeated chapter shapes:")
for sig, ns in top:
    print(f"    {len(ns):3}x  {sig[:70]}")
print()
# crisis / help routing
for label, rx in [("crisis/helpline", r"(helpline|hotline|999|911|emergency|crisis line|refuge|shelter)"),
                  ("'see a doctor/clinician'", r"(doctor|clinician|GP|therapist|counsell?or)"),
                  ("safety/exit", r"(safety plan|leave (?:the|this) page|quick exit|browsing history)")]:
    ch = sorted(n for n, b in bodies.items() if re.search(rx, b, re.I))
    print(f"  {label:26} in {len(ch)} chapters: {ch[:16]}{'...' if len(ch)>16 else ''}")

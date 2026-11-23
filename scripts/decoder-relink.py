#!/usr/bin/env python3
"""Point book links at the Decoder's current addresses (skips the 301 hop).
Reads instruments/playbook/site/_redirects (old -> new) and rewrites href="/playbook/<old>" in built book pages.
Idempotent; touches nothing else. Like scripts/nf-catalogue-sweep.py, this is a sweep over built pages: the book sources
hold no old addresses, so a later rebuild produces the same links.
Usage: python3 scripts/decoder-relink.py [--check]"""
import re, sys, glob
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
red = {}
for l in open(ROOT / "instruments/playbook/site/_redirects"):
    m = re.match(r"/(\S+)\s+\S+/playbook/(\S+)", l)
    if m: red[m.group(1)] = m.group(2)
rx = re.compile(r'href="/playbook/(' + "|".join(map(re.escape, sorted(red, key=len, reverse=True))) + r')(?=["#?])')
files = [Path(p) for p in glob.glob(str(ROOT / "library/*/*.html")) + glob.glob(str(ROOT / "library/*/*/*.html")) + [str(ROOT / "hub/topics.html")]]
n = nf = 0
for p in files:
    t = p.read_text(encoding="utf-8")
    new, k = rx.subn(lambda m: 'href="/playbook/' + red[m.group(1)], t)
    if k:
        n += k; nf += 1
        if "--check" not in sys.argv: p.write_text(new, encoding="utf-8")
print(f"{n} links in {nf} files {'need' if '--check' in sys.argv else 'now point at'} the current Decoder address")
sys.exit(1 if "--check" in sys.argv and n else 0)

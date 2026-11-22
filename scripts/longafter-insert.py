#!/usr/bin/env python3
"""Insert new sections into The Long After chapters from an additions file.

Additions file format (Markdown):
  @@ chapter-slug | ## Heading to insert before        (or "| END" to append before "## Sources")
  ## New heading
  New text...
  @@ next-slug | END
  ...
Every block is applied or none: a missing chapter or anchor aborts with no file written.
Usage: python3 scripts/longafter-insert.py additions.md
"""
import re, sys, glob
from pathlib import Path

D = Path(__file__).resolve().parents[1] / "content/longafter-v2"
src = open(sys.argv[1]).read()
blocks = re.split(r"^@@ ", src, flags=re.M)[1:]
files = {f: open(f).read() for f in glob.glob(str(D / "[0-9]*.md"))}
n = 0
for b in blocks:
    head, text = b.split("\n", 1)
    slug, anchor = [x.strip() for x in head.split("|", 1)]
    text = text.strip() + "\n\n"
    f = next((k for k, v in files.items() if re.search(r"^=== " + re.escape(slug) + r"$", v, re.M)), None)
    assert f, f"no chapter {slug}"
    s = files[f]; st = s.index("=== " + slug + "\n"); en = s.find("\n=== ", st + 4); en = len(s) if en < 0 else en
    blk = s[st:en]
    key = "\n## Sources\n" if anchor == "END" else "\n" + anchor + "\n"
    i = blk.find(key)
    if i < 0 and anchor == "END":
        blk = blk.rstrip("\n") + "\n\n" + text
    else:
        assert i >= 0, f"{slug}: anchor not found: {anchor}"
        blk = blk[:i + 1] + text + blk[i + 1:]
    files[f] = s[:st] + blk + s[en:]
    n += 1
for f, v in files.items():
    open(f, "w").write(v)
print(f"{n} sections inserted")

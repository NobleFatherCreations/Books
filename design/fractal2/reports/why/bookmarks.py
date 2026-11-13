#!/usr/bin/env python3
"""Adds PDF bookmarks (outline) for every section heading. Usage: bookmarks.py in.pdf out.pdf html"""
import sys, re, html, logging
logging.disable(logging.CRITICAL)
import pdfplumber
from pypdf import PdfReader, PdfWriter
src, dst, doc = sys.argv[1:4]
h = open(doc).read()
items = [("part", html.unescape(m.group(1))) if m.group(1) else ("sec", html.unescape(m.group(2)))
         for m in re.finditer(r'<div class="part"><i>[^<]*</i><h2>([^<]*)</h2>|<a id="sec[^"]+"></a><div class="sec"[^>]*><div class="kick">[^<]*</div><h2>([^<]*)</h2>', h)]
texts = []
with pdfplumber.open(src) as pdf:
    texts = [re.sub(r"\s+", " ", p.extract_text() or "") for p in pdf.pages]
w = PdfWriter(clone_from=PdfReader(src)); parent = None; start = 9
for kind, title in items:
    key = re.sub(r"\s+", " ", title)[:40]
    pg = next((i for i in range(start, len(texts)) if key in texts[i]), None)
    if pg is None: print("not found:", title); continue
    start = pg
    if kind == "part": parent = w.add_outline_item(title, pg)
    else: w.add_outline_item(title, pg, parent=parent)
w.write(dst); print(dst, "bookmarks:", len(items))

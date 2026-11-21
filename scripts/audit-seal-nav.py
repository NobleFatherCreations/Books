#!/usr/bin/env python3
"""Audit: does every deployed page carry the seal menu, and does that menu list every other book and project?
Reference list: scripts/nf-catalogue.py ENTRIES (21). Usage: python3 scripts/audit-seal-nav.py"""
import importlib.util, re, collections
from pathlib import Path
R = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("cat", R / "scripts/nf-catalogue.py"); CAT = importlib.util.module_from_spec(spec); spec.loader.exec_module(CAT)
ALL = [e[0].rstrip("/") for e in CAT.CATALOGUE]
ROOTS = ["library", "instruments", "workshop", "hub", "other"]
report = collections.defaultdict(list)
for root in ROOTS:
    for f in sorted((R / root).rglob("*.html")):
        rel = f.relative_to(R).as_posix()
        if "_undeployed" in rel or "/node_modules/" in rel or "/qa" in rel or "/tests/" in rel:
            continue
        h = f.read_text(encoding="utf-8", errors="ignore")
        if "<html" not in h[:3000].lower():
            continue
        kind = "seal" if 'id="nf-chrome"' in h else ("old drawer" if 'id="nh-drawer"' in h else "none")
        if kind == "none":
            report[(rel.split("/")[1] if root in ("library", "instruments", "workshop") else root, "NO MENU")].append(rel); continue
        i = h.find('id="nf-chrome"' if kind == "seal" else 'id="nh-drawer"')
        block = h[i:i + 60000]
        have = set(re.findall(r'noblefathercreations\.com/([a-z]+)', block)) | set(re.findall(r'href="/([a-z]+)/?"', block))
        here = len(re.findall(r'href="#"', block[:20000]))
        missing = [s for s in ALL if s not in have]
        key = (rel.split("/")[1] if root in ("library", "instruments", "workshop") else root, kind,
               "missing: " + (", ".join(missing) if missing else "none"))
        report[key].append(rel)
bad = 0
for (site, kind, *m), pages in sorted(report.items()):
    flag = kind == "NO MENU" or kind == "old drawer" or (m and len(m[0].split(",")) > 1) or (m and m[0] != "missing: none" and "," in m[0])
    note = m[0] if m else ""
    print(f"{site:12} {len(pages):5} pages  {kind:10}  {note}   e.g. {pages[0]}")

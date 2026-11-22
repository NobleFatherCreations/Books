#!/usr/bin/env python3
"""Check every JSON-LD node on the built pages against the official schema.org vocabulary:
each @type exists, each property exists and is allowed on that type (domainIncludes, with inheritance).
Usage: python3 scripts/seo/validate_schema.py <schemaorg-current-https.jsonld>"""
import json, re, sys, collections
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
voc = json.load(open(sys.argv[1]))["@graph"]
cls, props, parents = set(), {}, collections.defaultdict(set)
def ids(v): return [x["@id"] for x in (v if isinstance(v, list) else [v])] if v else []
for n in voc:
    t = n.get("@type"); t = t if isinstance(t, list) else [t]
    nid = n["@id"].replace("schema:", "")
    if "rdfs:Class" in t:
        cls.add(nid); parents[nid] |= {p.replace("schema:", "") for p in ids(n.get("rdfs:subClassOf"))}
    if "rdf:Property" in t:
        props[nid] = {d.replace("schema:", "") for d in ids(n.get("schema:domainIncludes"))}
def ancestors(c, seen=None):
    seen = seen or set()
    for p in parents.get(c, ()):
        if p not in seen: seen.add(p); ancestors(p, seen)
    return seen | {c}
errs, counts = collections.Counter(), collections.Counter()
def walk(node, where):
    if isinstance(node, list):
        for x in node: walk(x, where)
        return
    if not isinstance(node, dict): return
    t = node.get("@type")
    if t:
        for tt in (t if isinstance(t, list) else [t]):
            counts[tt] += 1
            if tt not in cls: errs[f"unknown type {tt}"] += 1
        allowed = set().union(*(ancestors(tt) for tt in (t if isinstance(t, list) else [t]) if tt in cls)) if any(tt in cls for tt in (t if isinstance(t, list) else [t])) else set()
        for k, v in node.items():
            if k.startswith("@"): continue
            if k not in props: errs[f"unknown property {k} (on {t})"] += 1
            elif allowed and not (props[k] & allowed): errs[f"property {k} not expected on {t}"] += 1
    for k, v in node.items():
        if isinstance(v, (dict, list)): walk(v, where)
files = [p for b in ["fracture","feminine","children","wook","fractal","festival","faith"] for p in (ROOT/"library"/b).glob("*.html")] + [ROOT/"hub/catalogue-redesign.html"]
for f in files:
    h = f.read_text(encoding="utf-8", errors="ignore")
    for m in re.finditer(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', h, re.S):
        walk(json.loads(m.group(1)), f.name)
print(f"{len(files)} files; nodes by type: {dict(counts.most_common())}")
print("problems:" if errs else "no invalid types or properties")
for e, n in errs.most_common(): print(f"  {n:5}x  {e}")

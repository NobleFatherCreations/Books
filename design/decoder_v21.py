"""Decoder v21: data added on top of v20, all from files already in the repo. Nothing here writes new tactic wording.

  - aliases: content/decoder-v21/aliases.json (same-thing names only) -> "Also called", search, JSON-LD alternateName
  - research: content/decoder-v21/research.json, written by scripts/decoder-sources.py (every source verified)
  - parents: tactic -> the patterns it is part of (reverse of each pattern's made_of)
  - routes: tactic -> the routes (combos) it appears in, with the step before and after it
  - lastmod: a page's date changes only when its content changes (design/decoder-lastmod.json)
"""
import hashlib, json, os, re
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "content", "decoder-v21")
LASTMOD = os.path.join(HERE, "decoder-lastmod.json")
TOKEN = "%%LASTMOD%%"


def apply_aliases(entries, aliases):
    data = json.load(open(os.path.join(SRC, "aliases.json"), encoding="utf-8"))
    data.pop("_rule", None)
    by = {e["n"]: e for e in entries}
    added = 0
    for name, names in data.items():
        e = by.get(name)
        if not e:
            raise SystemExit("decoder_v21: aliases.json names an entry that does not exist: %s" % name)
        have = {x.lower() for x in e["abs"]} | {name.lower()}
        for a in names:
            if a.lower() in have: continue
            e["abs"].append(a); e["kw"].append(a.lower()); aliases[a] = name; have.add(a.lower()); added += 1
    return added


def research():
    p = os.path.join(SRC, "research.json")
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}


def parents(entries):
    out = defaultdict(list)
    for e in entries:
        for m in (e.get("pt") or {}).get("made_of", []):
            out[m].append(e["n"])
    return out


def route_slug(r):
    return "route-" + r["s"]


def routes_of(recipes):
    """{tactic: [(route, index in route)]}"""
    out = defaultdict(list)
    for r in recipes:
        for i, n in enumerate(r["c"]):
            out[n].append((r, i))
    return out


def stamp(pages, today):
    """Fill each page's TOKEN with the date its content last changed. Returns {page name: date}."""
    old = json.load(open(LASTMOD)) if os.path.exists(LASTMOD) else {}
    new, dates = {}, {}
    for name, text in pages.items():
        h = hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]
        prev = old.get(name)
        date = prev[1] if prev and prev[0] == h else today
        new[name] = [h, date]; dates[name] = date
        pages[name] = text.replace(TOKEN, date)
    with open(LASTMOD, "w") as fh:
        json.dump(new, fh, indent=0, sort_keys=True)
    return dates

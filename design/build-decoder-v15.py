#!/usr/bin/env python3
"""Build the Pattern Decoder v15 ("Wayfinding"): one self-contained, offline HTML file.

Run from the repo root:  python3 design/build-decoder-v15.py [--out PATH]
Default output: instruments/playbook/index.html (the deployable page).

v15 reuses v10's data merge (entries, aliases, reader meta, feelings, search stop words) and
replaces the sky with a transit network:
  group      -> line (letter + colour)
  tactic     -> station; stations on a line are ordered so neighbours are related
  related tactic in another group -> interchange
  documented sequence ("recipe")  -> route
Data is split so the page paints before it parses the bulk: a small index (names, subtitles,
search words, the short fields search reads) is parsed at start; each line's full entries sit in
their own <script type="application/json"> block at the end of the file and are parsed the first
time a station on that line opens. No CDN, no external request except the sanctioned beacon.
See docs/DECODER-V15-ARCHITECTURE.html for the reasoning behind every choice.
"""
import argparse, base64, importlib.util, json, os, re
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
V15 = os.path.join(HERE, "decoder-v15")
A15 = os.path.join(V15, "assets")
A10 = os.path.join(HERE, "decoder-v10", "assets")

_spec = importlib.util.spec_from_file_location("v10", os.path.join(HERE, "build-decoder-v10.py"))
v10 = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(v10)

VERSION = "v15"
DATE = "2026-10-24"
UPDATES = [
    "<strong>A new design, made to be easy to find your way (v15).</strong> The guide is now laid out like the signs in a metro or an airport. Each of the ten groups is a coloured line with a letter, each tactic is a station on its line, and look-alike tactics in other groups are shown as places to “change here for”.",
    "<strong>The answer comes first.</strong> Every entry now opens with what it is, what it can sound like and, where it matters, your safety. The rest is split into four short steps instead of one long page, and long lists open only when you ask.",
    "<strong>Private by default.</strong> Nothing is saved on your device unless you turn saving on. While it is off, the page addresses use numbers instead of tactic names, and the tab shows only the guide's name.",
    "<strong>Leave quickly.</strong> A green Leave button on every page switches straight to a weather page. On a keyboard, press Escape twice.",
    "<strong>Easier to read.</strong> New typefaces designed for legibility, larger small print, and nothing moving unless you tap it. Help me figure it out now shows why each match was suggested, and any two look-alikes can be compared side by side.",
] + v10.UPDATES

LETTER = {"truth": "T", "pressure": "G", "control": "C", "hook": "L", "wear": "W",
          "blame": "B", "people": "P", "systems": "S", "online": "O", "society": "M"}
NIGHT = {"truth": "#4A82FF", "pressure": "#9469FF", "control": "#1AA9DE", "hook": "#F05BA0", "wear": "#C06BE0",
         "blame": "#B07A52", "people": "#F06A52", "systems": "#8FA3BD", "online": "#17BDB0", "society": "#A2C23A"}
DAY = {"truth": "#1F55D6", "pressure": "#6A3FE0", "control": "#0B7AA6", "hook": "#C2316F", "wear": "#8E3BB0",
       "blame": "#8A5534", "people": "#C2412A", "systems": "#5A6F8A", "online": "#0A7F76", "society": "#5E7A12"}
# Fields kept in the start-up index because search and lists read them; the rest load per line.
INDEX_FIELDS = ["short_definition", "plain_language_summary", "what_it_sounds_like"]


def read(*p):
    return open(os.path.join(*p), encoding="utf-8").read()


def b64(path):
    return base64.b64encode(open(path, "rb").read()).decode()


def assemble():
    """The same entry assembly as v10, so content stays byte-identical."""
    data = json.load(open(os.path.join(ROOT, "content", "playbook-data.json"), encoding="utf-8"))
    codex, recipes = data["codex_completed"], data["recipes"]
    merges = json.load(open(os.path.join(ROOT, "content", "codex-final", "tactic-merges.json")))["groups"]
    aliases = {m: g["canonical"] for g in merges for m in g["merged"]}
    meta_p = os.path.join(ROOT, "content", "codex-final", "reader-meta.json")
    meta_doc = json.load(open(meta_p, encoding="utf-8")) if os.path.exists(meta_p) else {}
    meta = meta_doc.get("entries", {})
    feel_src = read(A10, "feelings.js")
    feeling_groups = v10.js_object_literal(feel_src, "FEELING_GROUPS")
    feelings = v10.js_object_literal(feel_src, "FEELINGS") + meta_doc.get("new_feelings", [])
    narrow = json.loads(read(A10, "narrow-by-feeling.json"))
    if meta_doc.get("feelings_index"):
        narrow = meta_doc["feelings_index"]
    narrow = {k: [aliases.get(n, n) for n in v] for k, v in narrow.items()}
    stop = re.search(r'new Set\(\("([^"]+)"', read(A10, "search-stop.js")).group(1).split()
    names = {c["name"] for c in codex}
    pop = Counter(n for r in recipes for n in r["c"])
    feel_group = {f["key"]: f["group"] for f in feelings}
    settings_of = {}
    for k, lst in narrow.items():
        s = v10.FEEL_TO_SETTING.get(feel_group.get(k))
        for n in lst:
            if s:
                settings_of.setdefault(n, set()).add(s)

    def slug(s):
        return re.sub(r"(^-+|-+$)", "", re.sub(r"[^a-z0-9]+", "-", s.lower())) or "x"

    entries, seen = [], {}
    for c in codex:
        n = c["name"]; m = meta.get(n, {})
        g = m.get("group") or v10.CAT_TO_GROUP[c["category"]]
        w = m.get("settings")
        if not w:
            w = sorted(settings_of.get(n, set()))
            if g == "systems": w = sorted(set(w) | {"work"})
            if g == "online": w = sorted(set(w) | {"online"})
            if g == "society": w = sorted(set(w) | {"society"})
        s = slug(n); k = 1
        while s in seen:
            k += 1; s = slug(n) + "-" + str(k)
        seen[s] = n
        entries.append({
            "n": n, "s": s, "g": g, "w": w, "sub": m.get("subtitle", ""), "kw": m.get("search_words", []),
            "sens": bool(c["safety_sensitive"]), "abs": c.get("absorbs") or [],
            "rel": [r for r in (m.get("related") or c.get("related_tactics", [])) if r in names and r != n],
            "pop": pop.get(n, 0),
            "kind": ("verify" if (c["branch"] == "societal" or c["boundary_script"].lower().startswith("verification"))
                     else "self" if c["branch"] == "aftermath" else "say"),
            "f": {**{f: c[f] for f in v10.FIELDS},
                  "less_concerning_if": v10.dedupe(c["less_concerning_if"], c["this_may_not_be_it_when"])},
        })
    by = {e["n"]: e for e in entries}
    recipes = [{"n": r["n"], "s": slug(r["n"]), "c": [aliases.get(x, x) for x in r["c"] if aliases.get(x, x) in by], "d": r["d"]}
               for r in recipes]
    core = sorted(codex, key=lambda c: (-((4 if c["tier"] == "Detected" else 0) + min(pop.get(c["name"], 0), 10)), c["name"]))
    common = [c["name"] for c in core[:24]]
    return entries, by, recipes, aliases, narrow, feelings, feeling_groups, stop, common


def order_line(members, by):
    """Order a line so each station sits next to a related one where the data allows: start at the
    most-read tactic, then always step to the closest unvisited station by related-link distance."""
    names = [e["n"] for e in members]
    nameset = set(names)
    adj = {n: [r for r in by[n]["rel"] if r in nameset] for n in names}
    for n in names:                       # links are not always written both ways
        for r in adj[n]:
            if n not in adj[r]: adj[r].append(n)
    rank = {n: (-by[n]["pop"], n) for n in names}
    start = min(names, key=lambda n: rank[n])
    out, seen = [start], {start}
    while len(out) < len(names):
        cur = out[-1]
        # breadth-first from the current station; nearest unvisited wins, ties by popularity
        frontier, dist, best = [cur], {cur: 0}, None
        while frontier and best is None:
            nxt = []
            for x in frontier:
                for y in sorted(adj[x], key=lambda n: rank[n]):
                    if y in dist: continue
                    dist[y] = dist[x] + 1; nxt.append(y)
                    if y not in seen and best is None: best = y
            frontier = nxt
        if best is None:
            best = min((n for n in names if n not in seen), key=lambda n: rank[n])
        out.append(best); seen.add(best)
    return out


def order_columns(keys, by, entries):
    """Put the lines that share the most look-alikes next to each other on the map."""
    w = Counter()
    for e in entries:
        for r in e["rel"]:
            g2 = by[r]["g"]
            if g2 != e["g"]: w[tuple(sorted((e["g"], g2)))] += 1
    pair = lambda a, b: w[tuple(sorted((a, b)))]
    best, best_score = None, -1
    for s in keys:                         # greedy chain from every start, keep the best
        out = [s]
        while len(out) < len(keys):
            out.append(max((k for k in keys if k not in out), key=lambda k: (pair(out[-1], k), -keys.index(k))))
        sc = sum(pair(out[i], out[i + 1]) for i in range(len(out) - 1))
        if sc > best_score: best, best_score = out, sc
    return best


def home_html(lines, count):
    """Home is written into the page at build time, so it paints before any script runs.
    app.js re-uses this exact markup when the reader comes back to it."""
    ic = lambda d: '<svg class="i" viewBox="0 0 24 24" aria-hidden="true">' + d + '</svg>'
    blade = lambda href, cls, icon, t, s: ('<a class="blade%s" href="%s"><span class="pict">%s</span><span class="bt"><b>%s</b><small>%s</small></span>'
                                            '<span class="ar" aria-hidden="true">%s</span></a>') % (cls, href, ic(icon), t, s, ic('<path d="M5 12h14M13 6l6 6-6 6"/>'))
    rows = "".join('<li><a class="lrow" href="#/line/%s"><span class="b" data-g="%s">%s</span><span class="lt"><b>%s</b><small>%s</small></span><span class="n">%d</span></a></li>'
                   % (l["k"], l["k"], l["letter"], l["label"], l["blurb"], len(l["order"])) for l in lines)
    return ('<div class="view home" id="home-src">'
            '<section class="concourse" aria-labelledby="home-h">'
            '<h1 id="home-h" class="h-page">Put a name to what is happening.</h1>'
            '<p class="lede">%d manipulation and control tactics, in plain words: how to tell if one fits, and what you can do.</p>'
            '<div class="blades">%s%s%s</div>'
            '<div id="continue"></div>'
            '</section>'
            '<section class="lines-ix" aria-labelledby="lines-h"><h2 id="lines-h" class="k">The ten lines</h2>'
            '<p class="small muted">Each line is one kind of tactic. Every tactic is a station on its line.</p>'
            '<ol class="lrows">%s</ol>'
            '<p class="more-links"><a href="#/lines/az">All %d, A to Z</a><a href="#/lines/where">By where it happens</a><a href="#/lines/common">The most common</a><a href="#/routes">Patterns seen together</a></p>'
            '</section></div>') % (
        count,
        blade("#/help", " pri", '<circle cx="12" cy="12" r="9"/><path d="M9.5 9a2.5 2.5 0 1 1 3.5 2.3c-.7.3-1 .9-1 1.7v.5"/><circle cx="12" cy="17" r=".6" fill="currentColor"/>',
              "Help me figure it out", "Answer two short questions"),
        blade("#/search", "", '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>', "I know what to look for", "Search by what was said or done"),
        blade("#/map", "", '<circle cx="6" cy="6" r="2"/><circle cx="18" cy="18" r="2"/><path d="M6 8v4a4 4 0 0 0 4 4h6"/><circle cx="18" cy="6" r="2"/><path d="M18 8v8"/>',
              "See all %d on the map" % count, "Ten lines, one for each kind"),
        rows, count)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(ROOT, "instruments", "playbook", "index.html"))
    a = ap.parse_args()
    entries, by, recipes, aliases, narrow, feelings, feeling_groups, stop, common = assemble()

    groups = [(k, l, b) for k, l, b in v10.GROUPS if any(e["g"] == k for e in entries)]
    keys = order_columns([k for k, _, _ in groups], by, entries)
    gmeta = {k: (l, b) for k, l, b in groups}
    lines = []
    for k in keys:
        members = [e for e in entries if e["g"] == k]
        lines.append({"k": k, "letter": LETTER[k], "label": gmeta[k][0], "blurb": gmeta[k][1],
                      "c": NIGHT[k], "d": DAY[k], "order": order_line(members, by)})
    pos = {}
    for li, l in enumerate(lines):
        for si, n in enumerate(l["order"]):
            pos[n] = [li, si]

    # start-up index: one record per station, in a fixed order (its number is its private address)
    idx = []
    for i, e in enumerate(entries):
        idx.append({"n": e["n"], "s": e["s"], "g": e["g"], "w": e["w"], "sub": e["sub"], "kw": e["kw"], "sens": e["sens"],
                    "abs": e["abs"], "rel": e["rel"], "pop": e["pop"], "kind": e["kind"], "p": pos[e["n"]],
                    "f": {f: e["f"][f] for f in INDEX_FIELDS}})
    full = {l["k"]: {e["n"]: {f: v for f, v in e["f"].items() if f not in INDEX_FIELDS} for e in entries if e["g"] == l["k"]}
            for l in lines}
    payload = {
        "entries": idx, "lines": lines,
        "settings": [{"k": k, "label": l, "blurb": b} for k, l, b in v10.SETTINGS],
        "recipes": recipes, "aliases": aliases, "narrow": narrow, "feelings": feelings, "feelingGroups": feeling_groups,
        "feelToSetting": v10.FEEL_TO_SETTING, "stop": stop, "common": common, "glossary": v10.GLOSSARY, "tries": v10.TRIES,
        "catToGroup": v10.CAT_TO_GROUP, "version": VERSION, "date": DATE, "updates": UPDATES,
    }
    js_json = lambda o: json.dumps(o, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    blocks = "\n".join('<script type="application/json" id="L-%s">%s</script>' % (k, js_json(v)) for k, v in full.items())

    fonts = ("@font-face{font-family:'Overpass';font-style:normal;font-weight:600 800;font-display:block;src:url(data:font/woff2;base64,%s) format('woff2')}\n"
             "@font-face{font-family:'Atkinson Next';font-style:normal;font-weight:400 700;font-display:block;src:url(data:font/woff2;base64,%s) format('woff2')}\n"
             "@font-face{font-family:'Atkinson Next';font-style:italic;font-weight:400;font-display:block;src:url(data:font/woff2;base64,%s) format('woff2')}") % (
        b64(os.path.join(A15, "overpass-var.woff2")), b64(os.path.join(A15, "atkinson-next-var.woff2")), b64(os.path.join(A15, "atkinson-next-italic.woff2")))
    # line colours: night values everywhere, day values when the page is light (system or chosen)
    day = lambda pre: "".join("%s [data-g=%s]{--lc:%s}" % (pre, l["k"], l["d"]) for l in lines)
    line_css = ("".join("[data-g=%s]{--lc:%s}" % (l["k"], l["c"]) for l in lines)
                + "@media (prefers-color-scheme: light){" + day(":root:not([data-theme=night])") + "}" + day(":root[data-theme=day]"))

    html = (read(V15, "shell.html")
            .replace("{{FONTS}}", fonts)
            .replace("{{CSS}}", read(V15, "app.css").replace("/*@@LINES@@*/", line_css))
            .replace("{{LOGO}}", read(A10, "brand-logo.txt"))
            .replace("{{COUNT}}", str(len(entries)))
            .replace("{{HOME}}", home_html(lines, len(entries)))
            .replace("{{INDEX}}", js_json(payload))
            .replace("{{JS}}", read(V15, "app.js"))
            .replace("{{BLOCKS}}", blocks)
            .replace("{{HOUSE}}", read(A10, "house.html"))
            .replace("{{BEACON}}", read(A10, "beacon.html")))
    assert "{{" not in html, "unfilled placeholder in shell"
    with open(a.out, "w", encoding="utf-8") as fh:
        fh.write(html)
    print(f"wrote {os.path.relpath(a.out, ROOT)}  {len(html.encode())//1024} KB  entries {len(entries)}  "
          f"index {len(js_json(payload).encode())//1024} KB  css {len(read(V15,'app.css').encode())//1024} KB  js {len(read(V15,'app.js').encode())//1024} KB")
    print("  lines:", " ".join(f"{l['letter']}:{l['k']}({len(l['order'])})" for l in lines))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build the Pattern Decoder v15 ("Wayfinding"): one self-contained, offline HTML file.

Run from the repo root:  python3 design/build-decoder-v15.py [--out PATH]
Default output: instruments/playbook/_undeployed/v15/index.html. The live v14 stays at
instruments/playbook/index.html until the author approves a deploy; then copy this file over it.

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
import argparse, base64, copy, hashlib, importlib.util, json, os, re, subprocess, sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
V15 = os.path.join(HERE, "decoder-v15")
A15 = os.path.join(V15, "assets")
A10 = os.path.join(HERE, "decoder-v10", "assets")
sys.path.insert(0, HERE)
import decoder_pages as pages  # noqa: E402  (plain per-tactic pages, v16)

_spec = importlib.util.spec_from_file_location("v10", os.path.join(HERE, "build-decoder-v10.py"))
v10 = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(v10)

VERSION = "v18"
DATE = "2026-10-27"
UPDATES = [
    "<strong>More room to read on a phone (v18).</strong> While you read down a tactic, only the slim step bar stays at the bottom of the screen; scroll up and the four buttons and Back to top come back. Share and Print now sit under More, two look-alikes compare one above the other on a phone, the daytime look uses the same warm gold as the night one, and a stray quote mark in a few comparisons is fixed.",
    "<strong>A new night look (v17).</strong> The guide is now matte black with a warm gold for the thing to press. Safety notes are red now, so they stand apart from everything else on the page, and the green Leave button is where it always was.",
    "<strong>Every tactic has its own page (v16).</strong> Each of the tactics now has a plain page with its own address, like noblefathercreations.com/playbook/gaslighting, so you can find it from a search engine and share a link that opens straight to it. The page address and the tab now always show what you are reading. If someone else could see this device, a private window is the safest way to read.",
    "<strong>Plainer words, all the way through.</strong> Every entry was read again for clarity. Long sentences were split, hard words were swapped for everyday ones, and the stiff, repeated phrasing was reworded so it reads like a person talking. A few claims that could not be backed up were removed, and one description of a study was corrected.",
    "<strong>Easier on a phone.</strong> A button takes you back to the top of a long page, and a slim bar lets you change step without scrolling up. Search has a Paste button, and the bottom bar steps aside while you type. Every entry has a Text size button and a Listen button that reads it aloud with a voice stored on your phone. A small buzz when you tap is available in Settings and is off until you turn it on.",
    "<strong>More ways to find your way.</strong> Every station has a short code, like T09, that you can type into search. Lines have their own shapes as well as colours. You can set a line aside if you are not ready to read about it, choose where the Leave button goes, and print one station as a clean one-page card.",
    "<strong>A new design, made to be easy to find your way (v15).</strong> The guide is now laid out like the signs in a metro or an airport. Each of the ten groups is a coloured line with a letter, each tactic is a station on its line, and look-alike tactics in other groups are shown as places to “change here for”.",
    "<strong>The answer comes first.</strong> Every entry now opens with what it is, what it can sound like and, where it matters, your safety. The rest is split into four short steps instead of one long page, and long lists open only when you ask.",
    "<strong>Private by default.</strong> Nothing is saved on your device unless you turn saving on. While it is off, the page addresses use numbers instead of tactic names, and the tab shows only the guide's name.",
    "<strong>Leave quickly.</strong> A green Leave button on every page switches straight to a weather page. On a keyboard, press Escape twice.",
    "<strong>Easier to read.</strong> New typefaces designed for legibility, larger small print, and nothing moving unless you tap it. Help me figure it out now shows why each match was suggested, and any two look-alikes can be compared side by side. Search also finds the lines and pages, a thin line in the line’s colour shows how far you have read, and Show on the map takes you to a station on the map.",
] + v10.UPDATES

LETTER = {"truth": "T", "pressure": "G", "control": "C", "hook": "L", "wear": "W",
          "blame": "B", "people": "P", "systems": "S", "online": "O", "society": "M"}
NIGHT = {"truth": "#4A82FF", "pressure": "#9469FF", "control": "#1AA9DE", "hook": "#F05BA0", "wear": "#C06BE0",
         "blame": "#B07A52", "people": "#FF8A4C", "systems": "#8FA3BD", "online": "#17BDB0", "society": "#A2C23A"}
DAY = {"truth": "#1F55D6", "pressure": "#6A3FE0", "control": "#0B7AA6", "hook": "#C2316F", "wear": "#8E3BB0",
       "blame": "#8A5534", "people": "#B4501A", "systems": "#5A6F8A", "online": "#0A7F76", "society": "#5E7A12"}
# One drawn glyph per line (24 x 24, 2px strokes): identity by shape, so lines are told apart in grey as well as in colour.
EMBLEM = {
    "truth": '<circle cx="9.5" cy="12" r="5.5"/><circle cx="14.5" cy="12" r="5.5"/>',
    "pressure": '<path d="M12 4v16"/><path d="M3 12h5M7 9l3 3-3 3"/><path d="M21 12h-5M17 9l-3 3 3 3"/>',
    "control": '<rect x="3.5" y="3.5" width="17" height="17"/><rect x="8.5" y="8.5" width="7" height="7"/>',
    "hook": '<path d="M14 3v11a4.5 4.5 0 0 1-9 0v-1.5"/><path d="M2.5 15l2.5-2.5L7.5 15"/>',
    "wear": '<path d="M4 6h16M4 12h11M4 18h6"/>',
    "blame": '<path d="M20 5H9a5 5 0 0 0 0 10h9"/><path d="M15 11l4 4-4 4"/>',
    "people": '<circle cx="6" cy="12" r="3"/><circle cx="13" cy="12" r="3"/><circle cx="20.5" cy="12" r="1.5"/>',
    "systems": '<rect x="4" y="4" width="7" height="7"/><rect x="4" y="13" width="7" height="7"/><path d="M14 6h6M14 10h6M14 15h6M14 19h4"/>',
    "online": '<path d="M3.5 9a12 12 0 0 1 17 0M6.5 12.5a8 8 0 0 1 11 0M9.5 16a4 4 0 0 1 5 0"/><circle cx="12" cy="19.5" r=".9" fill="currentColor"/>',
    "society": '<circle cx="12" cy="12" r="1.8" fill="currentColor"/><circle cx="12" cy="4.5" r="1.5"/><circle cx="18.5" cy="8.25" r="1.5"/><circle cx="18.5" cy="15.75" r="1.5"/><circle cx="12" cy="19.5" r="1.5"/><circle cx="5.5" cy="15.75" r="1.5"/><circle cx="5.5" cy="8.25" r="1.5"/>',
}
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


def _inter(s1, s2):
    (x1, y1, x2, y2), (x3, y3, x4, y4) = s1, s2
    d = (x2 - x1) * (y4 - y3) - (y2 - y1) * (x4 - x3)
    if abs(d) < 1e-9: return None
    t = ((x3 - x1) * (y4 - y3) - (y3 - y1) * (x4 - x3)) / d
    u = ((x3 - x1) * (y2 - y1) - (y3 - y1) * (x2 - x1)) / d
    return (x1 + t * (x2 - x1), y1 + t * (y2 - y1)) if 0.02 < t < 0.98 and 0.02 < u < 0.98 else None


def network_thumb(lines):
    """The ten lines as a small octilinear diagram: a picture of the network that opens the map. Static, drawn at build time."""
    n = len(lines); ys = [16 + i * 13.2 for i in range(n)]; perm = [(i * 3 + 2) % n for i in range(n)]
    paths, diag = [], []
    for i, l in enumerate(lines):
        y0, y1 = ys[i], ys[perm[i]]; a = 92 + (i % 5) * 20; b = a + abs(y1 - y0)
        paths.append('<path data-g="%s" d="M34 %.1fH%dL%.1f %.1fH326"/><circle class="e" data-g="%s" cx="34" cy="%.1f" r="4.2"/><circle class="e" data-g="%s" cx="326" cy="%.1f" r="4.2"/>' % (l["k"], y0, a, b, y1, l["k"], y0, l["k"], y1))
        diag.append((a, y0, b, y1))
    rings = []
    for i in range(n):
        for j in range(i + 1, n):
            p = _inter(diag[i], diag[j])
            if p: rings.append('<circle class="x" cx="%.1f" cy="%.1f" r="3.4"/>' % p)
    return ('<a class="net" href="#/map" aria-label="Open the map. This small picture is only a sketch of the ten lines, not the real map">'
            '<svg viewBox="0 0 340 150" aria-hidden="true" focusable="false">%s%s</svg></a>') % ("".join(paths), "".join(rings))


def home_html(lines, count):
    """Home is written into the page at build time, so it paints before any script runs.
    app.js re-uses this exact markup when the reader comes back to it."""
    ic = lambda d: '<svg class="i" viewBox="0 0 24 24" aria-hidden="true">' + d + '</svg>'
    blade = lambda href, cls, icon, t, s: ('<a class="blade%s" href="%s"><span class="pict">%s</span><span class="bt"><b>%s</b><small>%s</small></span>'
                                            '<span class="ar" aria-hidden="true">%s</span></a>') % (cls, href, ic(icon), t, s, ic('<path d="M5 12h14M13 6l6 6-6 6"/>'))
    rows = "".join('<li><a class="lrow" data-g="%s" href="#/line/%s"><span class="b" data-g="%s">%s</span><span class="lt"><b>%s</b><small>%s</small></span><span class="emb" data-g="%s" aria-hidden="true"><svg viewBox="0 0 24 24">%s</svg></span><span class="n">%d</span></a></li>'
                   % (l["k"], l["k"], l["k"], l["letter"], l["label"], l["blurb"], l["k"], l["emb"], len(l["order"])) for l in lines)
    return ('<div class="view home" id="home-src">'
            '<section class="concourse" aria-labelledby="home-h">'
            '<h1 id="home-h" class="h-page">Put a name to what is happening.</h1>'
            '<p class="lede">%d manipulation and control tactics, in plain words: how to tell if one fits, and what you can do.</p>'
            '<div class="blades">%s%s%s%s</div>'
            '<div id="continue"></div>%s'
            '</section>'
            '<section class="lines-ix" aria-labelledby="lines-h"><h2 id="lines-h" class="k">The ten lines</h2><button type="button" class="linkbtn colortoggle" data-colortoggle>Make the colours quieter</button>'
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
        blade("#/safety", " safe quiet", '<path d="M12 3 2 20h20z"/><path d="M12 10v4"/><circle cx="12" cy="17" r=".6" fill="currentColor"/>',
              "If you are not safe, read this first", "What to do, and how to leave quickly"),
        network_thumb(lines), rows, count)


# ----------------------------------------------------------------------------------------------------------------------
# The pre-compile gate. The page is only written if all of this holds. It checks the source strictly, runs the content
# validator, and then reads the finished HTML back and compares every entry byte for byte with the source it came from.
# `--selftest` proves the gate really rejects bad input.
# ----------------------------------------------------------------------------------------------------------------------
EXPECTED = 310
PLACEHOLDER = re.compile(r"\{\{|\}\}|\bTODO\b|\bTBD\b|\bFIXME\b|\bXXX\b|lorem ipsum|#REPLACE|data-here|�|[\x00-\x08\x0b\x0c\x0e-\x1f]", re.I)
TERMINAL = re.compile(r"[.!?”’\"')\]]\s*$")
PROSE_FIELDS = ["short_definition", "plain_language_summary", "expanded_definition", "why_this_matters", "safety_note"]


def _flat(v):
    if isinstance(v, str): return [v]
    if isinstance(v, list): return [x for y in v for x in _flat(y)]
    if isinstance(v, dict): return [x for y in v.values() for x in _flat(y)]
    return [str(v)]


def _digest(o):
    return hashlib.sha256(json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def gate_source(entries, recipes, expected=EXPECTED):
    """Strict checks on the source entries. Returns a list of problems (empty = clean)."""
    bad, names, slugs = [], set(), set()
    by = {e["n"]: e for e in entries}
    if len(entries) != expected: bad.append(f"{len(entries)} entries, expected {expected}")
    for e in entries:
        n = e["n"]
        if n in names: bad.append(f"{n}: duplicate name")
        if e["s"] in slugs: bad.append(f"{n}: duplicate slug {e['s']}")
        names.add(n); slugs.add(e["s"])
        if e["kind"] not in ("say", "self", "verify"): bad.append(f"{n}: unknown script kind {e['kind']!r}")
        for r_ in e["rel"]:
            if r_ not in by: bad.append(f"{n}: related tactic {r_!r} does not exist")
        for f in v10.FIELDS:
            if f not in e["f"]: bad.append(f"{n}.{f}: missing"); continue
            parts = _flat(e["f"][f])
            if not parts or any(not x.strip() for x in parts): bad.append(f"{n}.{f}: empty")
            for x in parts:
                if PLACEHOLDER.search(x): bad.append(f"{n}.{f}: placeholder or broken character in {x[:40]!r}")
                if x.count("**") % 2: bad.append(f"{n}.{f}: unclosed bold marker")
                if re.search(r"</?[a-z][^>]*>", x, re.I): bad.append(f"{n}.{f}: HTML in a text field: {x[:40]!r}")
        for f in PROSE_FIELDS:
            x = e["f"].get(f)
            if isinstance(x, str) and x.strip() and not TERMINAL.search(x): bad.append(f"{n}.{f}: ends mid-sentence ({x[-30:]!r})")
        if e["sens"] and not str(e["f"].get("safety_note", "")).strip(): bad.append(f"{n}: safety-sensitive but no safety note")
    for rc in recipes:
        for c in rc["c"]:
            if c not in by: bad.append(f"pattern {rc['n']}: {c!r} is not an entry")
        if not rc["c"]: bad.append(f"pattern {rc['n']}: empty")
    return bad


def gate_validator():
    """The repo's own content validator, run over the whole book."""
    v = os.path.join(HERE, "validate-codex-final.py")
    if not os.path.exists(v): return []
    r = subprocess.run([sys.executable, "-I", v, "--all", "--complete", "--quiet"], capture_output=True, text=True, timeout=120)
    return [] if r.returncode == 0 else ["content validator failed: " + (r.stdout + r.stderr).strip().splitlines()[-1][:200]]


def gate_output(entries, html, expected=EXPECTED):
    """Read the finished page back and compare every entry with its source, byte for byte."""
    bad = []
    m = re.search(r'<script type="application/json" id="data">(.*?)</script>', html, re.S)
    if not m: return ["the data block is missing from the page"]
    data = json.loads(m.group(1).replace("<\\/", "</"))
    blocks = {k: json.loads(v.replace("<\\/", "</")) for k, v in re.findall(r'<script type="application/json" id="L-([a-z]+)">(.*?)</script>', html, re.S)}
    got = {e["n"]: e for e in data["entries"]}
    if len(got) != expected: bad.append(f"page holds {len(got)} entries, expected {expected}")
    if sum(len(v) for v in blocks.values()) != expected: bad.append(f"line blocks hold {sum(len(v) for v in blocks.values())} entries, expected {expected}")
    for e in entries:
        g = got.get(e["n"])
        if not g: bad.append(f"{e['n']}: missing from the page"); continue
        full = {**g["f"], **blocks.get(e["g"], {}).get(e["n"], {})}
        if _digest(full) != _digest(e["f"]): bad.append(f"{e['n']}: text differs from its source")
        for k in ("s", "g", "w", "sub", "kw", "sens", "abs", "rel", "pop", "kind"):
            if _digest(g.get(k)) != _digest(e[k]): bad.append(f"{e['n']}: field {k} differs from its source")
        if e["g"] not in blocks or e["n"] not in blocks[e["g"]]: bad.append(f"{e['n']}: not in its line's data block")
    homes = re.findall(r'class="n">(\d+)</span></a></li>', html.split('id="lines-h"')[1].split("</ol>")[0]) if 'id="lines-h"' in html else []
    if sum(map(int, homes)) != expected: bad.append(f"Home's line index adds up to {sum(map(int, homes))}, expected {expected}")
    if "{{" in html: bad.append("an unfilled placeholder is left in the page")
    if len(re.findall(r"@font-face", html)) != 3: bad.append("the three embedded fonts are not all present")
    stripped = re.sub(r"<script[^>]*cloudflareinsights[^>]*></script>", "", html)
    stripped = re.sub(r'<link rel="canonical" href="https://noblefathercreations\.com/playbook">', "", stripped)  # names the address; never fetched
    if re.search(r"@import|url\(['\"]?https?:", stripped) or re.search(r"<(script|link|img|iframe)[^>]+(src|href)=['\"]https?://", stripped): bad.append("an external request is in the page")
    return bad


def run_gate(entries, recipes, html, expected=EXPECTED, with_validator=True):
    return gate_source(entries, recipes, expected) + (gate_validator() if with_validator else []) + gate_output(entries, html, expected)


def selftest(entries, recipes, html):
    """The gate must pass the real data and reject each kind of damage. Exit status 0 only if it does."""
    ok = True
    clean = run_gate(entries, recipes, html, with_validator=False)
    print("  real data:", "passes" if not clean else "FAILS: " + "; ".join(clean[:3])); ok &= not clean
    def mut(label, fn, on="source"):
        nonlocal ok
        es = copy.deepcopy(entries); h = html; fn(es) if on == "source" else None
        if on == "html": h = fn(html)
        bad = (gate_source(es, recipes) if on == "source" else gate_output(entries, h))
        print(f"  {label}:", "rejected" if bad else "NOT REJECTED"); ok &= bool(bad)
    mut("an empty field", lambda es: es[7]["f"].__setitem__("why_this_matters", ""))
    mut("an empty list item", lambda es: es[9]["f"].__setitem__("what_it_is", ["ok", " "]))
    mut("an unclosed bold marker", lambda es: es[3]["f"].__setitem__("short_definition", "A **broken definition."))
    mut("a placeholder", lambda es: es[5]["f"].__setitem__("expanded_definition", "Text {{REPLACE}} here."))
    mut("a sentence cut off mid-way", lambda es: es[11]["f"].__setitem__("plain_language_summary", "Someone keeps telling you that"))
    mut("HTML in a text field", lambda es: es[2]["f"].__setitem__("safety_note", "Call <b>now</b>."))
    mut("a sensitive entry with no safety note", lambda es: next(e for e in es if e["sens"])["f"].__setitem__("safety_note", ""))
    mut("a related tactic that does not exist", lambda es: es[4]["rel"].append("No Such Tactic"))
    mut("a missing entry", lambda es: es.pop())
    mut("one character changed in the finished page", lambda h: h.replace("what you clearly remember", "what you clearly remembar", 1), on="html")
    mut("a line's data block cut short", lambda h: re.sub(r'(<script type="application/json" id="L-truth">)\{"', r'\1{"zz":{},"', h, count=1).replace('"Gaslighting":', '"Gaslightinx":', 1), on="html")
    print("gate self-test:", "ok" if ok else "FAILED")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true", help="prove the pre-compile gate rejects bad input, then exit")
    ap.add_argument("--out", default=os.path.join(ROOT, "instruments", "playbook", "site", "index.html"),
                    help="the app page; unless --draft, the plain pages, fonts and sitemap are written beside it (the whole folder is the publish directory)")
    ap.add_argument("--draft", action="store_true", help="design iteration only: skip the content validator and write draft.html beside the build; never deploy this file")
    a = ap.parse_args()
    if a.draft: a.out = os.path.join(ROOT, "instruments", "playbook", "_undeployed", "v15", "draft.html")
    entries, by, recipes, aliases, narrow, feelings, feeling_groups, stop, common = assemble()

    groups = [(k, l, b) for k, l, b in v10.GROUPS if any(e["g"] == k for e in entries)]
    keys = order_columns([k for k, _, _ in groups], by, entries)
    gmeta = {k: (l, b) for k, l, b in groups}
    lines = []
    for k in keys:
        members = [e for e in entries if e["g"] == k]
        lines.append({"k": k, "letter": LETTER[k], "label": gmeta[k][0], "blurb": gmeta[k][1], "emb": EMBLEM[k],
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
            .replace("{{LDSET}}", pages.ld_set(len(entries)))
            .replace("{{CRAWL}}", pages.crawl_links(lines, len(entries)))
            .replace("{{COUNT}}", str(len(entries)))
            .replace("{{HOME}}", home_html(lines, len(entries)))
            .replace("{{INDEX}}", js_json(payload))
            .replace("{{JS}}", read(V15, "app.js"))
            .replace("{{BLOCKS}}", blocks)
            .replace("{{HOUSE}}", read(A10, "house.html"))
            .replace("{{BEACON}}", read(A10, "beacon.html")))
    if a.selftest:
        sys.exit(selftest(entries, recipes, html))
    problems = run_gate(entries, recipes, html, with_validator=not a.draft)
    if problems:
        print(f"PRE-COMPILE GATE FAILED ({len(problems)} problems). Nothing was written.")
        for x in problems[:25]: print("  -", x)
        if len(problems) > 25: print(f"  ... and {len(problems) - 25} more")
        sys.exit(1)
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    if a.draft:
        tmp = a.out + ".tmp"          # written whole or not at all
        with open(tmp, "w", encoding="utf-8") as fh:
            fh.write(html)
        os.replace(tmp, a.out)
    else:
        site = os.path.dirname(os.path.abspath(a.out))
        written, urls = pages.write_site(site, html, entries, lines, read(A10, "house.html"), read(A10, "beacon.html"),
                                         read(A10, "brand-logo.txt").strip(), A15, DATE)
        text_of = lambda t: re.sub(r"<(style|script)\b.*?</\1>", "", t, flags=re.S)   # CSS and JS braces are not placeholders
        bad = [n for n, t in written.items() if n != "index.html" and (PLACEHOLDER.search(text_of(t)) or "noindex" in t)]
        bad += [e["n"] for e in entries if e["s"] + ".html" not in written]
        if bad or len(urls) != len(entries) + len(lines) + 2:
            print("PLAIN PAGES FAILED:", bad[:10], len(urls)); sys.exit(1)
        print(f"plain pages: {len(written) - 1} written ({len(entries)} tactics, {len(lines)} lines, 1 index), sitemap {len(urls)} addresses")
    print("pre-compile gate: all", len(entries), "entries checked and read back from the page, byte for byte")
    print(f"wrote {os.path.relpath(a.out, ROOT)}  {len(html.encode())//1024} KB  entries {len(entries)}  "
          f"index {len(js_json(payload).encode())//1024} KB  css {len(read(V15,'app.css').encode())//1024} KB  js {len(read(V15,'app.js').encode())//1024} KB")
    print("  lines:", " ".join(f"{l['letter']}:{l['k']}({len(l['order'])})" for l in lines))


if __name__ == "__main__":
    main()

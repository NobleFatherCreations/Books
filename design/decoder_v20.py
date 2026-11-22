"""Decoder v20: the standard list of 335 single tactics (owner's Playbook Update Package, content/decoder-v20/).

Applied on top of v19's assembled entries so every live entry keeps its exact text, metadata and slug where its name
is unchanged. What it adds:
  - renamed live entries take their standard name; their old name stays as "Also called" and in search;
  - merged live entries fold into their target (old name searchable, old address redirects);
  - 32 umbrellas / built-in combos / effects stay as full entries at the SAME address, marked as patterns with the
    single tactics they are made of (Gaslighting, DARVO, FOG, Trauma Bonding ... keep their pages);
  - 110 new tactics from the package, all 21 fields as written there;
  - standard number and stage on every single tactic;
  - a redirect for every address that changed, and the books' chapters that mention each tactic.
Nothing here rewords package or live text. The only derived text: short_definition = the standard definition and
plain_language_summary = the first two sentences of expanded_definition, for the 110 new entries.
"""
import copy, csv, glob, html, json, os, re
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
SRC = os.path.join(ROOT, "content", "decoder-v20")
ORIGIN = "https://noblefathercreations.com"
BOOKS = {"fracture": "The Fracture", "feminine": "The Sovereign Divine Feminine", "wook": "The Festie Codex",
         "fractal": "The Fractal", "festival": "The Festie Bible", "faith": "The Sacred Divide",
         "loop": "The Loop", "scale": "The Weighing"}
STAGES = {"IDEALIZE": "Idealize", "HOOK": "Hook", "DEVALUE": "Devalue", "CONFUSE": "Confuse", "ISOLATE": "Isolate",
          "CONTROL": "Control", "DISCARD": "Discard", "REPLACE": "Replace"}
SENSITIVE = re.compile(r"immediate danger|in danger|emergency services|police|trafficking|forced lab|self-harm|suicid|child protection|safeguarding|violence|abuse|threat", re.I)
CALM = re.compile(r"mostly about|usually|rarely|not a physical|not in itself|on its own|by itself|not a safety|not normally|seldom", re.I)


def slug(s):
    return re.sub(r"(^-+|-+$)", "", re.sub(r"[^a-z0-9]+", "-", s.lower())) or "x"


def load(name):
    return json.load(open(os.path.join(SRC, name), encoding="utf-8"))


def sentences(t, k):
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z\"“])", t.strip())
    return " ".join(parts[:k])


def split_parts(made_of):
    return [p.strip() for p in re.split(r"\s*(?:\+|->|→)\s*", made_of or "") if p.strip()]


def transform(entries, recipes, aliases, narrow, common):
    singles = load("playbook_singles.json")
    patterns = load("playbook_patterns.json")
    index = load("standard_index.json")
    alias_map = load("alias_map.json")           # lower-case any-name -> standard id
    id_to_name = {v["standard_id"]: n for n, v in index.items()}
    sounds_p = os.path.join(SRC, "sounds_like.json")
    sounds = json.load(open(sounds_p, encoding="utf-8")) if os.path.exists(sounds_p) else {}
    rows = list(csv.DictReader(open(os.path.join(SRC, "LIVE_ENTRY_CHANGES.csv"), encoding="utf-8")))
    by19 = {e["n"]: e for e in entries}

    action = {r["live_entry"]: r for r in rows if r["live_entry"] and not r["action"].startswith("add")}
    target_of = {}                                # live name -> new entry name (None = removed)
    for n, r in action.items():
        a = r["action"]
        if a == "keep": target_of[n] = n
        elif a.startswith(("rename", "merge")): target_of[n] = r["standard_name"]
        elif a.startswith("move to patterns"): target_of[n] = n
        elif a.startswith("remove"): target_of[n] = None
    base_of = {}                                  # standard name -> live entry whose text it carries
    for n, r in action.items():
        if r["action"] == "keep" or r["action"].startswith("rename"):
            base_of[r["standard_name"] if r["action"] != "keep" else n] = n
    absorbed = defaultdict(list)                  # standard name -> live names that now resolve to it
    for n, t in target_of.items():
        if t and t != n: absorbed[t].append(n)

    def resolve(name):
        """Any name (live, old, alias, standard) -> a v20 entry name, or None."""
        if name in names: return name
        if name in target_of: return target_of[name]
        sid = alias_map.get(name.lower().strip())
        return id_to_name.get(sid) if sid else None

    new_entries, names = [], set()
    for th, objs in singles.items():
        for n in objs: names.add(n)
    pattern_names = [n for n, r in action.items() if r["action"].startswith("move to patterns")]
    names |= set(pattern_names)

    for th, objs in singles.items():
        for n, fields in objs.items():
            meta = index.get(n, {})
            if n in base_of:
                e = copy.deepcopy(by19[base_of[n]])
                e["n"] = n
            else:
                f = dict(fields)
                f["short_definition"] = meta.get("standard_definition", "").strip()
                if f["short_definition"] and not f["short_definition"].endswith((".", "!", "?")): f["short_definition"] += "."
                f["plain_language_summary"] = sentences(fields["expanded_definition"], 2)
                f["what_it_sounds_like"] = sounds.get(n, [])
                e = {"n": n, "s": "", "g": th, "w": [], "sub": "", "kw": [], "pop": 0, "abs": [], "rel": [],
                     "sens": bool(SENSITIVE.search(fields.get("safety_note", ""))) and not CALM.search(re.split(r"(?<=[.!?])\s", fields.get("safety_note", ""))[0]),
                     "kind": "verify" if str(fields.get("boundary_script", "")).lower().startswith("verification") else "say",
                     "f": {k: f[k] for k in f}, "new": True}
                if th == "systems": e["w"] = ["work"]
                if th == "online": e["w"] = ["online"]
                if th == "society": e["w"] = ["society"]
                txt = fields.get("how_to_distinguish_from_related", "")
                e["rel"] = [m for m in sorted(names) if m != n and (m in txt or m.split(" / ")[0] in txt)][:8]
            e["g"] = th
            e["abs"] = list(dict.fromkeys((e.get("abs") or []) + absorbed.get(n, []) + meta.get("also_called", [])))
            e["abs"] = [a for a in e["abs"] if a != n and a.lower() != n.lower()]
            e["kw"] = list(dict.fromkeys((e.get("kw") or []) + [a.lower() for a in e["abs"]]))
            e["std"] = {"t": meta.get("number", ""), "stage": STAGES.get(meta.get("stage", ""), "")}
            new_entries.append(e)
    for n in pattern_names:
        e = copy.deepcopy(by19[n])
        p = patterns.get(next((k for k, v in patterns.items() if n in v.get("live_entries", []) or k == n), ""), {})
        parts = [resolve(x) for x in split_parts(p.get("made_of") or action[n].get("note", ""))]
        e["pt"] = {"type": p.get("type") or action[n]["action"].split("(")[-1].rstrip(")"),
                   "made_of": [x for x in dict.fromkeys(parts) if x and x in names and x != n],
                   "seq": "->" in (p.get("made_of") or action[n].get("note", ""))}
        new_entries.append(e)

    # slugs: keep the live one where the name is unchanged, else derive; unique
    seen = set()
    old_slug = {e["n"]: e["s"] for e in entries}
    for e in new_entries:
        s = old_slug.get(e["n"]) or slug(e["n"])
        k, b = 1, s
        while s in seen:
            k += 1; s = b + "-" + str(k)
        e["s"] = s; seen.add(s)
    by = {e["n"]: e for e in new_entries}
    for e in new_entries:
        e["rel"] = [x for x in dict.fromkeys(resolve(r) for r in e["rel"]) if x and x in by and x != e["n"]]

    redirects = {}
    for e in entries:
        t = target_of.get(e["n"], e["n"])
        dest = by[t]["s"] if t in by else "tactics"
        if dest != e["s"]: redirects[e["s"]] = dest

    new_aliases = {}
    for k, v in list(aliases.items()) + list(target_of.items()):
        r = resolve(v) if v else None
        if r and r != k: new_aliases[k] = r
    new_narrow = {k: [x for x in dict.fromkeys(resolve(n) for n in v) if x in by] for k, v in narrow.items()}
    new_recipes = []
    for rc in recipes:
        c = [resolve(x) for x in rc["c"]]
        c = [x for x in c if x in by]
        c = [x for i, x in enumerate(c) if i == 0 or x != c[i - 1]]
        if len(c) >= 2: new_recipes.append({**rc, "c": c})
    pop = Counter(n for r in new_recipes for n in r["c"])
    for e in new_entries: e["pop"] = pop.get(e["n"], 0)
    new_common = [x for x in dict.fromkeys(resolve(n) for n in common) if x in by]
    return new_entries, by, new_recipes, new_aliases, new_narrow, new_common, redirects


def book_mentions(redirects):
    """{decoder slug: [(book, chapter title, url)]} from the links the books' chapter pages already carry."""
    out = defaultdict(list)
    for folder, book in BOOKS.items():
        for p in sorted(glob.glob(os.path.join(ROOT, "library", folder, "*.html"))):
            name = os.path.basename(p)[:-5]
            if name in ("index", "contents", "codex"): continue
            t = open(p, encoding="utf-8", errors="ignore").read()
            slugs = set(re.findall(r'href="/playbook/([a-z0-9-]+)"', t))
            if not slugs: continue
            m = re.search(r"<h1[^>]*>(.*?)</h1>", t, re.S)
            title = html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip() if m else name
            for s in slugs:
                s = redirects.get(s, s)
                out[s].append((book, title, "/%s/%s" % (folder, name)))
    return out


def redirects_file(redirects):
    lines = ["# Decoder v20: old tactic addresses -> their standard-name page (301, permanent)"]
    for old, new in sorted(redirects.items()):
        lines.append("/%s  %s/playbook/%s  301!" % (old, ORIGIN, new))
    return "\n".join(lines) + "\n"

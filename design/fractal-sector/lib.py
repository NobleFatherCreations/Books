"""Shared pieces of the sector generator: config, the context object, text helpers and the tiny markdown renderer."""
import datetime
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
STR = json.loads((HERE / "strings.json").read_text())

# ---- one config block ------------------------------------------------------------------------------------------
CONFIG = {
    "site": STR["site"],                                   # "Fractal²"
    "origin": "https://noblefathercreations.com",
    "registry": ROOT / "content/fractal2/sectors.json",    # base path comes from here, overridable with --base
    "publish": ROOT / "library/fractal2/site",             # shared with the intro: never deleted as a whole
    "work": ROOT / "library/fractal2",                     # manifests/, redirects/, build/ (og sources), review/
    "assets": ROOT / "design/decoder-v10/assets",          # THE HOUSE drawer + beacon, shared with the rest of the site
    "tokens": ROOT / "design/fractal2/tokens.css",
    "fonts": ROOT / "design/fractal2/fonts",
    "version": "v2",
}
PUBLISH_STATES = {"preview": {"unreviewed", "expert_reviewed", "sources_verified"},
                  "production": {"unreviewed", "expert_reviewed", "sources_verified"}}
UPDATES = [("v2", "updates_v2"), ("v1", "updates_v1")]
V1_DATE = "2026-11-09"

STAGE_INFO = {
    "IDEALIZE": "The approach: attention, warmth and promise arrive before any terms do.",
    "HOOK": "The binding: small commitments, debts and identities that make leaving costly.",
    "DEVALUE": "The turn: worth is chipped away so approval has to be earned back.",
    "CONFUSE": "The fog: facts, memory and meaning are made unreliable.",
    "ISOLATE": "The narrowing: outside voices and allies are cut away.",
    "CONTROL": "The system: rules, money, information and surveillance do the steering.",
    "DISCARD": "The exit on their terms: dropping, erasing or punishing the person.",
    "REPLACE": "The reset: someone new is brought in and the story is rewritten.",
}
LEVELS = [("Individual", "ind", "Individual"), ("Institutional", "inst", "Institutional"), ("Civilizational", "civ", "Civilizational")]
TAG_KIND = {"REQUIRES SUBJECT-MATTER REVIEW": "review", "VERIFIED SOURCE NEEDED": "source",
            "HISTORICAL EXAMPLE TO VERIFY": "source", "LEGAL CLAIM — JURISDICTION-SPECIFIC": "legal",
            "LEGAL CLAIM": "legal", "COMMON INDUSTRY PATTERN": "pattern", "HYPOTHETICAL COMPOSITE": "composite"}
TAG_LABEL = {  # (label, explanation); review/source labels follow the combo's review_state (packet 04 changes these)
    "legal": ("Varies by place", "Law and contract practice differ by country and state. Get local advice."),
    "pattern": ("Common pattern", "Widely reported in the industry; not a claim about any one company."),
    "composite": ("Composite", "A made-up example built from common situations. No real person is described."),
    ("review", "unreviewed"): ("Awaiting expert review", "This point has not yet been checked by an industry expert."),
    ("review", "expert_reviewed"): ("Expert reviewed", "An industry expert has checked this point."),
    ("review", "sources_verified"): ("Expert reviewed", "An industry expert has checked this point."),
    ("source", "unreviewed"): ("Source being checked", "A source for this point is still being verified."),
    ("source", "expert_reviewed"): ("Source being checked", "A source for this point is still being verified."),
    ("source", "sources_verified"): ("Source verified", "The source for this point has been verified."),
}
STATE_NOTE = {
    "unreviewed": "Written with care, not yet checked by an industry expert. Labels in the text show which points are still being checked.",
    "expert_reviewed": "Checked by an industry expert. Labels show any sources still being verified.",
    "sources_verified": "Checked by an industry expert, with its sources verified.",
}
STATE_NAME = {"unreviewed": "Unreviewed draft", "expert_reviewed": "Expert reviewed", "sources_verified": "Sources verified"}
BRACKET = re.compile(r"\[([^\[\]\n]{1,120})\]")
# Reserved addresses (NAV-SPEC 2). Combo slugs may not take one of these.
RESERVED = ["start", "patterns", "tactics", "map", "notice", "in-it-now", "worried-about-someone", "before-you-sign",
            "method", "take-it-with-you", "a-z", "tactic", "og", "sitemap"]


def S(key, **kw):
    s = STR[key]
    return s.format(**kw) if kw else s


def esc(s):
    return html.escape(str(s if s is not None else ""), quote=True)


def slugify(s):
    s = s.lower().replace("&", " and ").replace("’", "").replace("'", "")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def clip(s, n=158):
    s = re.sub(r"\s+", " ", s).strip()
    return s if len(s) <= n else s[:n].rsplit(" ", 1)[0].rstrip(",;:") + "…"


def plain(s):
    """Derived snippets (cards, descriptions, structured data): no cues, no credibility tags."""
    s = BRACKET.sub(lambda m: "" if m.group(1) in ("SPEAK", "HARD CUT") or m.group(1).startswith("~") or all(p.strip() in TAG_KIND for p in m.group(1).split(";")) else m.group(0), s or "")
    return re.sub(r"\s{2,}", " ", s.replace("**", "")).strip()


def first_sentence(s):
    s = plain(s)
    m = re.match(r"(.+?[.!?])(\s|$)", s.strip())
    return m.group(1) if m else s


def fam_name(cat):
    return re.sub(r"\s*Composites?$", "", cat["name"])


class Ctx:
    def __init__(self, sector, target, base=None):
        b = ROOT / "content/fractal" / sector
        self.sector = sector
        self.d = json.loads((b / "build/sector.json").read_text())
        self.links = json.loads((b / "build/links.json").read_text())
        self.der = json.loads((b / "build/derived.json").read_text())
        self.nav = json.loads((b / "nav.json").read_text())
        dl = b / "downloads.json"
        self.downloads = json.loads(dl.read_text()) if dl.exists() else []
        self.reg = json.loads(CONFIG["registry"].read_text())
        self.root = (base or self.reg["base"]).rstrip("/")          # "/fractal2"
        self.me = next(s for s in self.reg["sectors"] if (s.get("id") or "").upper() == self.d["sector"])
        self.slug = self.me["slug"]
        self.base = self.root + "/" + self.slug                      # "/fractal2/entertainment"
        self.title = self.d["title"]
        self.short = self.nav.get("short_title", self.title)
        self.ph = self.nav.get("phrases", {})
        self.ti = self.ph.get("title_industry", self.title)
        self.target = target
        self.allowed = PUBLISH_STATES[target]
        import resolve                                               # the derived layer: ledger rewrites + resolved labels
        self.res_delta, self.res, self.facts = resolve.apply_ledger(self.d, sector)
        self.combos = {c["combo_id"]: c for c in self.d["combos"]}
        self.live = {k for k, c in self.combos.items() if c["review_state"] in self.allowed}
        self.tactics = {t["single_no"]: t for t in self.d["tactics"]}
        for t in self.d["tactics"]:
            t["slug"] = slugify(t["name"])
        self.cats = {c["category_id"]: c for c in self.d["categories"]}
        self.stage_display = self.der["stage_display"]
        self.settings = {s["key"]: s for s in self.der["settings"]}
        self.date = datetime.date.today().isoformat()
        self.version = CONFIG["version"]
        self.house = (CONFIG["assets"] / "house.html").read_text()
        self.beacon = (CONFIG["assets"] / "beacon.html").read_text()
        xl = ROOT / "content/fractal/_crosslinks.json"
        self.cross = json.loads(xl.read_text()) if xl.exists() else {}
        self.top_ids = [t["combo_id"] for t in self.d["top10"]]
        self.rank = {t["combo_id"]: t["rank"] for t in self.d["top10"]}

    def u(self, path=""):
        return self.base + ("/" + path if path else "")

    def stage_name(self, stage):
        return self.stage_display[stage]

    def stage_no(self, stage):
        return self.d["stages"].index(stage) + 1

    def stage_url(self, stage):
        return self.u("stage-" + stage.lower())

    def tactic_url(self, no):
        return self.u("tactic/" + self.tactics[no]["slug"])

    def combo_url(self, cid):
        return self.u(self.combos[cid]["slug"])

    def combo_link(self, cid, label=None, frag=""):
        c = self.combos.get(cid)
        if not c:
            return esc(label or cid)
        if cid not in self.live:
            return '<span class="held">%s</span>' % esc(label or c["name"])
        return '<a href="%s%s">%s</a>' % (self.combo_url(cid), frag, esc(label or c["name"]))

    def chain(self, cid):
        return self.links["chains"][cid]


# ---------- inline + block markdown (tiny, only what the scripts use) ----------
def inline(s, state="unreviewed"):
    out, last = [], 0
    for m in BRACKET.finditer(s):
        out.append(esc(s[last:m.start()]))
        tok = m.group(1)
        parts = [p.strip() for p in tok.split(";")]
        if tok in ("SPEAK", "HARD CUT"):
            pass
        elif tok.startswith("~"):                      # a tag the resolution ledger has settled
            kind, _, val = tok[1:].partition(":")
            if kind == "s":
                out.append('<a class="tg tg-cited" href="#sources" title="%s">%s</a>' % (esc(S("lab_cited_tip")), esc(S("lab_cited"))))
            else:
                out.append('<span class="tg tg-cond" title="%s">%s</span>' % (esc(S("lab_qual_tip" if kind == "q" else "lab_cond_tip")), esc(val)))
        elif all(p in TAG_KIND for p in parts):
            for p in parts:
                k = TAG_KIND[p]
                lab, tip = TAG_LABEL.get((k, state)) or TAG_LABEL[k]
                out.append('<span class="tg tg-%s" title="%s">%s</span>' % (k, esc(tip), esc(lab)))
        else:
            out.append('<span class="slot">[%s]</span>' % esc(tok))
        last = m.end()
    out.append(esc(s[last:]))
    h = "".join(out)
    h = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", h)
    h = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", h)
    return re.sub(r"\s{2,}", " ", h).strip()


def blocks(md_text):
    return [b.strip("\n") for b in re.split(r"\n\s*\n", md_text.strip()) if b.strip()]


def md(text, state="unreviewed", first_cls=None):
    out = []
    for i, b in enumerate(blocks(text)):
        lines = b.split("\n")
        if all(re.match(r"\s*[-*]\s+", l) or not l.strip() for l in lines if l.strip()) and re.match(r"\s*[-*]\s", lines[0]):
            out.append("<ul>%s</ul>" % "".join("<li>%s</li>" % inline(re.sub(r"^\s*[-*]\s+", "", l), state)
                                               for l in lines if l.strip()))
        elif re.match(r"\s*\d+\.\s", lines[0]):
            items, cur = [], []
            for l in lines:
                if re.match(r"\s*\d+\.\s", l):
                    if cur:
                        items.append(" ".join(cur))
                    cur = [re.sub(r"^\s*\d+\.\s+", "", l)]
                else:
                    cur.append(l.strip())
            items.append(" ".join(cur))
            out.append("<ol>%s</ol>" % "".join("<li>%s</li>" % inline(x, state) for x in items))
        elif all(l.startswith(">") for l in lines):
            out.append('<blockquote class="caution">%s</blockquote>' %
                       inline(" ".join(re.sub(r"^>\s?", "", l) for l in lines), state))
        else:
            cls = ' class="%s"' % first_cls if (first_cls and i == 0) else ""
            out.append("<p%s>%s</p>" % (cls, "<br>".join(inline(l, state) for l in lines)))
    return "\n".join(out)


def src(inner, cls=""):
    """Author words live inside data-src, so verify.mjs can count them against ingest's reader_words."""
    return '<div class="prose%s" data-src>%s</div>' % (" " + cls if cls else "", inner)


ICON = {
    "leave": '<path d="M14 4h5v16h-5M10 8l-4 4 4 4M6 12h10"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "back": '<path d="M19 12H5M11 6l-6 6 6 6"/>',
    "alert": '<path d="M12 9v4M12 17h.01"/><path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
    "grid": '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',
    "x": '<path d="M18 6 6 18M6 6l12 12"/>',
    "sliders": '<path d="M4 6h10M18 6h2M4 12h4M12 12h8M4 18h12M20 18h0"/><circle cx="16" cy="6" r="2"/><circle cx="10" cy="12" r="2"/><circle cx="18" cy="18" r="2"/>',
    "print": '<path d="M6 9V3h12v6M6 18H4a1 1 0 0 1-1-1v-6a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v6a1 1 0 0 1-1 1h-2"/><rect x="6" y="14" width="12" height="7"/>',
}


def svg(name, size=18):
    return ('<svg width="%d" height="%d" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">%s</svg>' % (size, size, ICON[name]))


def dot(n):
    return '<span class="sd" style="--c:var(--s%d)" aria-hidden="true"></span>' % n

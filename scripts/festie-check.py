#!/usr/bin/env python3
"""Structural checker for The Festie Bible (library/festival/index.html).

149 scenario cards x 14 fields is ~2,086 fields that cannot be verified by
reading. This checks what a human can't: field presence and type, the
guide's own outline against what its scenarios actually deliver, check-string
agreement with the guide's acronym, duplicate hooks, and the on-page version
badge against sites.json.

Reads the sidecar content/festie-bible-data.json by default (the inline copy
in the HTML must match it -- `--inline` checks that too).
"""
import argparse
import json
import re
import sys
from collections import Counter, defaultdict

DATA = "content/festie-bible-data.json"
PAGE = "library/festival/index.html"
SITES = "sites.json"

SCENARIO_FIELDS = {
    "section": str, "hook": str, "archetype": str, "clinical": str,
    "who": str, "scene": str, "tells": list, "happening": str,
    "check": str, "darkTitle": str, "dark": str, "move": str,
    "say": str, "truth": str,
}
GUIDE_FIELDS = {
    "slug": str, "acronymClass": str, "role": str, "acronym": str,
    "edition": str, "sectionOf": int, "pages": int, "intro": str,
    "checks": list, "outline": list, "sentences": list, "scenarios": list,
}


def load_inline(page):
    s = open(page, encoding="utf-8").read()
    i = s.find("FESTIE_DATA = ") + len("FESTIE_DATA = ")
    depth = 0; j = i; instr = False; esc = False
    while j < len(s):
        c = s[j]
        if instr:
            if esc: esc = False
            elif c == "\\": esc = True
            elif c == '"': instr = False
        else:
            if c == '"': instr = True
            elif c == "{": depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    j += 1; break
        j += 1
    return json.loads(s[i:j]), s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inline", action="store_true",
                    help="also verify the HTML's inline copy matches the sidecar")
    a = ap.parse_args()

    d = json.load(open(DATA, encoding="utf-8"))
    findings = defaultdict(list)

    def err(cat, msg): findings[cat].append(("ERROR", msg))
    def warn(cat, msg): findings[cat].append(("WARN", msg))

    # --- top level -------------------------------------------------------
    for k in ("mission", "updated", "changelog", "guides"):
        if k not in d: err("schema", f"top-level key missing: {k}")

    # --- guides ----------------------------------------------------------
    slugs = Counter(g.get("slug") for g in d["guides"])
    for s, n in slugs.items():
        if n > 1: err("schema", f"duplicate guide slug: {s} x{n}")

    all_hooks = defaultdict(list)
    for g in d["guides"]:
        ac = g.get("acronym", "?")
        for f, t in GUIDE_FIELDS.items():
            if f not in g:
                err("schema", f"{ac}: guide field missing: {f}"); continue
            if not isinstance(g[f], t):
                err("schema", f"{ac}: guide field {f} is {type(g[f]).__name__}, want {t.__name__}")

        # the acronym's letters must match its checks, in order
        letters = [c for c in g.get("acronym", "") if c.isalpha()]
        check_letters = [c.get("letter") for c in g.get("checks", [])]
        if letters != check_letters:
            err("acronym", f"{ac}: acronym letters {letters} != checks {check_letters}")

        # sectionOf should be this guide's 1-based position
        pos = d["guides"].index(g) + 1
        if g.get("sectionOf") != pos:
            warn("schema", f"{ac}: sectionOf={g.get('sectionOf')} but is guide #{pos}")

        # --- outline promises vs scenarios delivered ---------------------
        promised = [o.get("key") for o in g.get("outline", [])]
        delivered = Counter(sc.get("section") for sc in g.get("scenarios", []))
        for key in promised:
            if delivered.get(key, 0) == 0:
                err("coverage", f"{ac}: outline promises section '{key}' but no scenario delivers it")
        for key in delivered:
            if key not in promised:
                warn("coverage", f"{ac}: scenario section '{key}' is not in the guide's outline")

        # --- scenarios ---------------------------------------------------
        for n, sc in enumerate(g.get("scenarios", []), 1):
            tag = f"{ac}#{n}"
            for f, t in SCENARIO_FIELDS.items():
                if f not in sc:
                    err("schema", f"{tag}: field missing: {f}"); continue
                v = sc[f]
                if not isinstance(v, t):
                    err("schema", f"{tag}: {f} is {type(v).__name__}, want {t.__name__}")
                elif t is str and not v.strip():
                    err("schema", f"{tag}: {f} is empty")
                elif t is list and not v:
                    err("schema", f"{tag}: {f} is an empty list")
            if isinstance(sc.get("tells"), list) and len(sc["tells"]) < 3:
                warn("thin", f"{tag}: only {len(sc['tells'])} tells (cards average 5)")
            # the check line must name this guide's acronym and a real letter
            chk = sc.get("check", "")
            if isinstance(chk, str) and chk:
                if ac not in chk:
                    err("check", f"{tag}: check line does not name {ac}: {chk[:60]}")
                m = re.search(r'—\s*["“]?([A-Z])["”]?\s*CHECK', chk)
                if not m:
                    warn("check", f"{tag}: check line has no parseable letter: {chk[:60]}")
                elif m.group(1) not in letters:
                    err("check", f"{tag}: check cites letter '{m.group(1)}' not in {ac}")
                # a check field must actually close its quoted question --
                # 78 of the original book's cards (all from the original 12
                # guides, none from the 9 added 2026-09-17) were found on
                # 2026-09-17 to be truncated mid-sentence ("...what do I
                # actually know..." with no closing quote), a content-
                # generation cutoff from whenever they were originally
                # written. Ended with "..." AND missing a closing quote mark
                # is the specific signature; either alone can be legitimate
                # prose.
                qm = re.search(r'CHECK:\s*["“](.+?)["”]', chk, re.S)
                if not qm and chk.rstrip().endswith("..."):
                    err("check", f"{tag}: check field is truncated, no closing quote: {chk[:70]}...")
            if sc.get("hook"):
                all_hooks[sc["hook"].strip().lower()].append(tag)

    for hook, where in all_hooks.items():
        if len(where) < 2:
            continue
        # The same subject is deliberately covered in several guides with
        # audience-specific framing, so a shared hook across guides is by
        # design. Two cards with one title inside a single guide are not --
        # that guide's jump index then lists the same title twice.
        guides = {w.split("#")[0] for w in where}
        if len(guides) == 1:
            err("dupe", f"hook '{hook}' appears twice in the same guide: {', '.join(where)}")
        else:
            findings["dupe"].append(("INFO", f"hook '{hook}' is shared across guides "
                                             f"(by design): {', '.join(where)}"))

    # --- homoglyphs / stray scripts -------------------------------------
    # A Cyrillic capital De once slipped into an English check name from a
    # keyboard switch and read as a normal D. Flag any character outside the
    # Latin/punctuation ranges the book actually uses.
    ALLOWED = set(
        "\u2018\u2019\u201c\u201d\u2013\u2014\u2026\u00a0\u00b7\u2192\u2190\u00a9\u00ae\u2122"
        "\u00e9\u00e8\u00ea\u00eb\u00e1\u00e0\u00e2\u00e4\u00ed\u00ef\u00f3\u00f6\u00f4"
        "\u00fa\u00fc\u00f1\u00e7\u00c9\u00c8\u00c1\u00d6\u00dc\u00d1\u00c7\u00e5\u00f8"
        "\u00b0\u00bd\u00bc\u00be\u00ab\u00bb\u2032\u2033"
    )
    def scan(text, where):
        for ch in set(text):
            o = ord(ch)
            if o < 128 or ch in ALLOWED:
                continue
            if 0x1F000 <= o <= 0x1FAFF or 0x2600 <= o <= 0x27BF or o in (0xFE0F, 0x200D):
                continue  # emoji, which the guides use deliberately
            err("homoglyph", f"{where}: unexpected character {ch!r} (U+{o:04X})")
    for g in d["guides"]:
        scan(g["acronym"] + g["role"] + g["edition"] + g["intro"], g["acronym"])
        for c in g["checks"]:
            scan(c["letter"] + c["name"], f"{g['acronym']} check {c['letter']}")
        for n, sc in enumerate(g["scenarios"], 1):
            scan(sc["hook"] + sc["archetype"] + sc["clinical"], f"{g['acronym']}#{n}")

    # --- version reconciliation -----------------------------------------
    inline, page_src = load_inline(PAGE)
    if a.inline and json.dumps(inline, sort_keys=True) != json.dumps(d, sort_keys=True):
        err("sync", "the HTML's inline FESTIE_DATA does not match content/festie-bible-data.json")

    # the badge should be derived from the data, not a literal in the markup
    m = re.search(r'fb-updates"><summary>(v\d+)', page_src)
    hard = m is not None
    page_v = m.group(1) if m else d.get("version")
    sites = json.load(open(SITES, encoding="utf-8"))
    seq = sites["projects"] if isinstance(sites, dict) and "projects" in sites else sites
    seq = seq if isinstance(seq, list) else list(seq.values())
    fest = next((p for p in seq if p.get("slug") == "festival"), None)
    if fest:
        if page_v != fest.get("version"):
            err("version", f"page badge says {page_v}, sites.json says {fest.get('version')}")
        n_page, n_sites = len(d["changelog"]), len(fest.get("changelog", []))
        if n_page != n_sites:
            err("version", f"page has {n_page} changelog entries, sites.json has {n_sites}")
        if d["changelog"] and not isinstance(d["changelog"][0], dict):
            warn("version", "page changelog entries are bare strings with no date or version, "
                            "so they cannot be reconciled with sites.json by script")
    if hard:
        err("version", f"page version badge '{page_v}' is a hardcoded literal, not read from the data")

    # --- hardcoded guide counts -----------------------------------------
    # Adding a 13th guide made "Section N of 12" and "Twelve Guides" wrong,
    # the same class of bug as the hardcoded version badge. The render path
    # derives them now; the static chrome cannot, so it is asserted here.
    n_guides = len(d["guides"])
    words = {12: "twelve", 13: "thirteen", 14: "fourteen", 15: "fifteen", 16: "sixteen",
             17: "seventeen", 18: "eighteen", 19: "nineteen", 20: "twenty",
             21: "twenty-one", 22: "twenty-two", 23: "twenty-three", 24: "twenty-four", 25: "twenty-five", 26: "twenty-six", 27: "twenty-seven", 28: "twenty-eight", 29: "twenty-nine", 30: "thirty"}
    word = words.get(n_guides, str(n_guides))
    if re.search(r"Section '\+g\.sectionOf\+' of \d+", page_src):
        err("counts", "'Section N of <number>' is hardcoded in the render path")
    if re.search(r"<h2>(Twelve|Thirteen|Fourteen|\d+) Guides\. One Community", page_src):
        err("counts", "the contents heading hardcodes the guide count")
    m = re.search(r'<meta name="description" content="[^"]*\u2014 (\w+) guides, one community', page_src)
    if m and m.group(1).lower() != word:
        err("counts", f"meta description says '{m.group(1)}' guides, there are {n_guides}")
    m = re.search(r'<span class="nf-desc">(\w+) guides for the festival world', page_src)
    if m and m.group(1).lower() != word:
        err("counts", f"THE HOUSE drawer row says '{m.group(1)}' guides, there are {n_guides}")

    # --- report ----------------------------------------------------------
    n_err = sum(1 for v in findings.values() for s, _ in v if s == "ERROR")
    n_warn = sum(1 for v in findings.values() for s, _ in v if s == "WARN")
    n_info = sum(1 for v in findings.values() for s, _ in v if s == "INFO")
    total_sc = sum(len(g["scenarios"]) for g in d["guides"])
    print(f"Festie Bible check — {len(d['guides'])} guides, {total_sc} scenarios, "
          f"{len(findings) and sum(len(v) for v in findings.values()) or 0} findings")
    print(f"  ERROR: {n_err}   WARN: {n_warn}   INFO: {n_info}\n")
    for cat in sorted(findings):
        print("=" * 66)
        print(f"{cat.upper()} ({len(findings[cat])})")
        print("=" * 66)
        for sev, msg in findings[cat]:
            print(f"  {sev}: {msg}")
        print()
    return 1 if n_err else 0


if __name__ == "__main__":
    sys.exit(main())

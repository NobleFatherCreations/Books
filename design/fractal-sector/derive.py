#!/usr/bin/env python3
"""Derived navigation data.  python3 design/fractal-sector/derive.py ent

Reads   content/fractal/<s>/build/sector.json (from ingest.py), content/fractal/<s>/nav.json (settings rules, input),
        content/decoder-v20/{standard_index,alias_map,playbook_patterns}.json, instruments/playbook/site/*.html,
        content/fractal2/sectors.json, library/fractal/the-spiritual-lens.html + the-frequency.html (anchor ids only)
Writes  content/fractal/<s>/build/links.json    Decoder + Fractal links, resolved chain of every combo
        content/fractal/<s>/build/derived.json  settings, positions, shared patterns, reading times, map tables
        appends a "Navigation data" section to content/fractal/<s>/build/audit.md

Every link is exact and id-based: a name resolves through the author's reverse index (ingest), then the alias map's
own key format (lower case, '&' -> 'and', other punctuation -> space) to a standard id. A Decoder link exists only if
the page file exists. No fuzzy matching anywhere.
"""
import collections
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from ingest import words, reader_text  # noqa: E402  (the same word rule as the round trip)

DEC = ROOT / "content/decoder-v20"
PLAYBOOK = ROOT / "instruments/playbook/site"
QUICK = ["Safety Note (read first)", "Definition", "Verbal Breakdown", "Recognition Cue Cards", "Chain Breakers",
         "Escalation Triggers — Specific", "Safer Response Language"]
STAGE_DISPLAY = {"CONTROL": "Extract · Control"}   # NAV-SPEC 13: data key stays CONTROL
FRACTAL_STAGE = {"CONTROL": "extract"}             # what The Fractal's own anchors call the stage


def norm(s):
    s = s.lower().replace("&", " and ")
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def pb_slug(s):
    """The Decoder's page file naming (checked against all 335 standard names: every one exists)."""
    s = re.sub(r"[^a-z0-9]+", "-", s.lower().replace("&", " and ")).strip("-")
    return s[:70].rsplit("-", 1)[0] if len(s) > 70 else s


def pb_url(name):
    s = pb_slug(name)
    return "/playbook/" + s if (PLAYBOOK / (s + ".html")).exists() else None


def ids_in(path):
    return set(re.findall(r'id="([^"]+)"', path.read_text())) if path.exists() else set()


def main(sector):
    b = ROOT / "content/fractal" / sector / "build"
    d = json.loads((b / "sector.json").read_text())
    nav = json.loads((ROOT / "content/fractal" / sector / "nav.json").read_text())
    reg = json.loads((ROOT / "content/fractal2/sectors.json").read_text())
    si = json.loads((DEC / "standard_index.json").read_text())
    am = json.loads((DEC / "alias_map.json").read_text())
    pp = json.loads((DEC / "playbook_patterns.json").read_text())
    by_sid = {t["standard_id"]: t for t in d["tactics"]}
    by_no = {t["single_no"]: t for t in d["tactics"]}
    pat_by_sid = {v["standard_id"]: k for k, v in pp.items()}
    name_of_sid = {v["standard_id"]: k for k, v in si.items()}

    # ---- Decoder link per tactic (by standard id -> standard name -> page file) ----------------------------------
    tac_links = {}
    for t in d["tactics"]:
        nm = name_of_sid.get(t["standard_id"])
        tac_links[t["standard_id"]] = {"decoder": pb_url(nm) if nm else None}

    # ---- every combo's chain, resolved ----------------------------------------------------------------------------
    chains, newly, rest = {}, collections.Counter(), collections.Counter()
    for c in d["combos"]:
        ch = []
        for r in c["tactics"]:
            e = {"name": r["name"], "single_no": r["single_no"], "via": r["via"], "pattern": None}
            if not r["single_no"]:
                sid = am.get(norm(r["name"]))
                if sid in by_sid:
                    e.update(single_no=by_sid[sid]["single_no"], via="alias_map")
                    newly[r["name"]] += 1
                elif sid in pat_by_sid:
                    p = pat_by_sid[sid]
                    url = next((pb_url(x) for x in [p] + pp[p]["live_entries"] if pb_url(x)), None)
                    if url:
                        e.update(via="playbook_pattern", pattern={"name": p, "url": url})
                        newly[r["name"]] += 1
                    else:
                        rest[r["name"]] += 1
                else:
                    rest[r["name"]] += 1
            ch.append(e)
        chains[c["combo_id"]] = ch

    # ---- Fractal links: sector chapter + per-stage anchors that exist ----------------------------------------------
    me = next((s for s in reg["sectors"] if (s.get("id") or "").upper() == d["sector"]), {})
    chap = me.get("fractal_chapter")
    if chap and not (ROOT / "library" / (chap.strip("/") + ".html")).exists():
        chap = None
    lens, freq = ids_in(ROOT / "library/fractal/the-spiritual-lens.html"), ids_in(ROOT / "library/fractal/the-frequency.html")
    fr_stages = {}
    for s in d["stages"]:
        k = "stage-%s-" % FRACTAL_STAGE.get(s, s.lower())
        L = sorted(i for i in lens if i.startswith(k + "divine-principle-"))
        F = sorted(i for i in freq if i.startswith(k + "what-existed-before-"))
        fr_stages[s] = {"lens": "/fractal/the-spiritual-lens#" + L[0] if len(L) == 1 else None,
                        "frequency": "/fractal/the-frequency#" + F[0] if len(F) == 1 else None}

    (b / "links.json").write_text(json.dumps({
        "tactics": tac_links, "chains": chains,
        "fractal": {"chapter": chap, "stages": fr_stages},
        "unresolved_before": sum(newly.values()) + sum(rest.values()),
        "now_linked": sum(newly.values()), "still_unresolved": dict(rest.most_common())}, ensure_ascii=False, indent=1))

    # ---- settings -----------------------------------------------------------------------------------------------
    rules = nav["settings"]
    settings = {c["combo_id"]: [s["key"] for s in rules if set(c["tags"]) & set(s["tags"])] for c in d["combos"]}
    coverage = {s["key"]: sum(s["key"] in v for v in settings.values()) for s in rules}
    no_setting = [k for k, v in settings.items() if not v]

    # ---- positions, shared tactics, reading times ------------------------------------------------------------------
    uses = collections.defaultdict(list)
    tset = {}
    for c in d["combos"]:
        ch = chains[c["combo_id"]]
        tset[c["combo_id"]] = {e["single_no"] for e in ch if e["single_no"]}
        for i, e in enumerate(ch):
            if e["single_no"]:
                uses[e["single_no"]].append({"combo_id": c["combo_id"], "pos": i + 1, "of": len(ch)})
    for t in d["tactics"]:   # the author's reverse index always wins: keep combos it names even without a position
        have = {u["combo_id"] for u in uses[t["single_no"]]}
        for k in t["combos"]:
            if k not in have:
                uses[t["single_no"]].append({"combo_id": k, "pos": None, "of": None})
    name = {c["combo_id"]: c["name"] for c in d["combos"]}
    combos = {}
    for c in d["combos"]:
        k = c["combo_id"]
        sh = sorted(((len(tset[k] & tset[o]), name[o], o) for o in tset if o != k and tset[k] & tset[o]),
                    key=lambda x: (-x[0], x[1].lower()))[:6]
        qw = sum(words(reader_text(c["sections"].get(h, ""))) for h in QUICK)
        combos[k] = {"settings": settings[k], "shared": [{"combo_id": o, "n": n} for n, _, o in sh],
                     "quick_words": qw, "quick_min": max(1, math.ceil(qw / 220)),
                     "full_min": max(1, math.ceil(c["reader_words"] / 220))}

    # ---- map tables -------------------------------------------------------------------------------------------
    tcount = collections.Counter(e["single_no"] for ch in chains.values() for e in ch if e["single_no"])
    top_t = [{"single_no": n, "n": k} for n, k in sorted(tcount.items(), key=lambda x: (-x[1], by_no[x[0]]["name"]))[:15]]
    pairs = collections.defaultdict(set)
    for k, ch in chains.items():
        for a, z in zip(ch, ch[1:]):
            if a["single_no"] and z["single_no"]:
                pairs[(a["single_no"], z["single_no"])].add(k)
    top_p = [{"a": a, "b": z, "combos": sorted(v, key=lambda x: name[x])}
             for (a, z), v in sorted(pairs.items(), key=lambda x: (-len(x[1]), by_no[x[0][0]]["name"], by_no[x[0][1]]["name"]))
             if len(v) >= 2]

    (b / "derived.json").write_text(json.dumps({
        "stage_display": {s: STAGE_DISPLAY.get(s, s.title()) for s in d["stages"]},
        "settings": [{"key": s["key"], "label": s["label"], "n": coverage[s["key"]]} for s in rules],
        "no_setting": no_setting, "combos": combos,
        "tactic_uses": {k: sorted(v, key=lambda u: name[u["combo_id"]].lower()) for k, v in uses.items()},
        "map": {"top_tactics": top_t, "pairs": top_p}}, ensure_ascii=False, indent=1))

    # ---- audit ------------------------------------------------------------------------------------------------
    L = ["", "## Navigation data (derive.py)", "",
         f"- Unresolved tactic names in combos before: {sum(newly.values()) + sum(rest.values())} occurrences; "
         f"now linked: {sum(newly.values())} (alias map to a sector tactic page, or a Decoder pattern page); still plain text: {sum(rest.values())}.",
         "- Still unresolved (no exact alias, or the alias points to a standard id with no sector tactic and no Decoder page):", ""]
    L += [f"  - {n} ({k}x)" for n, k in rest.most_common()] or ["  - none"]
    L += ["", f"- Decoder links for tactics: {sum(1 for v in tac_links.values() if v['decoder'])} of {len(tac_links)}",
          f"- Fractal chapter: {chap or 'none'}; stage anchors found: "
          + ", ".join(f"{s.title()} {'lens' if v['lens'] else '-'}/{'frequency' if v['frequency'] else '-'}" for s, v in fr_stages.items()),
          "", "- Settings coverage (combos per setting):", ""]
    L += [f"  - {s['label']}: {coverage[s['key']]}" for s in rules]
    L += [f"  - combos with no setting: {len(no_setting)}" + (" (" + ", ".join(name[k] for k in no_setting) + ")" if no_setting else "")]
    if "C144" in name:
        L += ["", "- C144: the combo page uses the tag counts from the script file (the file has 2 [REQUIRES SUBJECT-MATTER REVIEW]; "
              "the author's index says 0). The warning above stays until the index is corrected."]
    with open(b / "audit.md", "a") as f:
        f.write("\n".join(L) + "\n")
    print(f"derive: {sum(newly.values())} of {sum(newly.values()) + sum(rest.values())} unresolved tactic names now link; "
          f"{len(no_setting)} combos with no setting; {len(top_p)} recurring pairs")
    for s in rules:
        print(f"  {s['label']:<34}{coverage[s['key']]:>4}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "ent"))

#!/usr/bin/env python3
"""Fractal sector importer + audit.  python3 design/fractal-sector/ingest.py ent

Reads   content/fractal/<sector>/source/   (the author's files, never written to)
        content/fractal/<sector>/review_state.json   (owner-maintained, created if missing)
Writes  content/fractal/<sector>/build/sector.json     derived data the generator reads
        content/fractal/<sector>/build/review_queue.json   every tag + every Credibility Audit, as a to-do list
        content/fractal/<sector>/build/audit.md       the human report (read this after every import)

Nothing here changes a word of a script. Stripping production cues and the Credibility Audit happens
in the derived copy only. combo_id stays the key of every record so other sectors can link the same
combo later. Exit code 1 only on STRUCTURAL failures (a missing section, a missing safety note, a
broken file), never on credibility tags: those are tracked by review_state, not treated as errors.
"""
import collections
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# --- the credibility vocabulary (the project's own system) ----------------------------------------
TAGS = {
    "REQUIRES SUBJECT-MATTER REVIEW": "review",
    "VERIFIED SOURCE NEEDED": "source",
    "HISTORICAL EXAMPLE TO VERIFY": "source",
    "LEGAL CLAIM — JURISDICTION-SPECIFIC": "legal",
    "LEGAL CLAIM": "legal",
    "COMMON INDUSTRY PATTERN": "pattern",
    "HYPOTHETICAL COMPOSITE": "composite",
}
CUES = {"SPEAK", "HARD CUT"}                   # video directions: stripped from web, kept in source
SLOTS = {"X", "Y", "N", "date", "name", "amount"}  # reader fill-in blanks inside Safer Response Language
REQUIRED = ["Cold Open", "The Name", "Definition", "Verbal Breakdown", "Why This Order", "Individual Level",
            "Institutional Echo", "Civilizational Echo", "Observable Indicators", "Evidence To Preserve — Additions",
            "False-Positive Check — Specific", "Recognition Cue Cards", "Chain Breakers",
            "Escalation Triggers — Specific", "Safer Response Language", "Reflection", "Credibility Audit"]
NEVER_DROP = ["Escalation Triggers — Specific", "Safer Response Language"]
STATES = ["unreviewed", "expert_reviewed", "sources_verified"]
STAGES = ["IDEALIZE", "HOOK", "DEVALUE", "CONFUSE", "ISOLATE", "CONTROL", "DISCARD", "REPLACE"]


def slug(s):
    s = s.lower().replace("&", " and ").replace("’", "").replace("'", "")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def frontmatter(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}, text
    meta, key = {}, None
    for line in m.group(1).splitlines():
        if re.match(r"\s+- ", line) and key:
            meta.setdefault(key, []).append(line.split("- ", 1)[1].strip())
        elif ":" in line:
            key, v = line.split(":", 1)
            key, v = key.strip(), v.strip()
            if v.startswith("[") and v.endswith("]"):
                v = [x.strip() for x in v[1:-1].split(",") if x.strip()]
            meta[key] = v if v != "" else []
    return meta, text[m.end():]


def sections(body):
    """'## Heading' -> text. Order kept."""
    out = collections.OrderedDict()
    parts = re.split(r"^## (.+)$", body, flags=re.M)
    for i in range(1, len(parts), 2):
        out[parts[i].strip()] = parts[i + 1].strip("\n")
    return out


BRACKET = re.compile(r"\[([^\[\]\n]{1,120})\]")


def tag_parts(tok):
    """'[LEGAL CLAIM — JURISDICTION-SPECIFIC; REQUIRES SUBJECT-MATTER REVIEW]' is two tags."""
    parts = [p.strip() for p in tok.split(";")]
    return parts if all(p in TAGS for p in parts) else []


def classify(tok):
    if tok in CUES:
        return "cue"
    if tag_parts(tok):
        return "tag"
    if tok in SLOTS or re.fullmatch(r"[A-Z]|[a-z ]{2,20}", tok):
        return "slot"
    return "unknown"


def sentence_around(text, i, j):
    a = max(text.rfind(". ", 0, i), text.rfind("\n", 0, i)) + 1
    b = min([x for x in (text.find(". ", j), text.find("\n", j)) if x != -1] or [len(text)])
    return text[a:b + 1].strip()


def words(s):
    """Same rule as verify.mjs. Bare list numbers ('1.') are not words, wherever they sit."""
    return len([w for w in re.findall(r"[A-Za-z0-9][A-Za-z0-9'’.,%$-]*", s) if not re.fullmatch(r"\d+\.", w)])


def reader_text(md):
    """What a reader will see, as plain text, for the word-count round trip."""
    md = BRACKET.sub(lambda m: "" if classify(m.group(1)) in ("cue", "tag") else m.group(0), md)
    md = re.sub(r"^\s*(?:[-*]|\d+\.)\s+", "", md, flags=re.M)
    md = re.sub(r"^\s*>\s?", "", md, flags=re.M)
    return md.replace("**", "").replace("__", "")


def main(sector):
    base = ROOT / "content/fractal" / sector
    src, out = base / "source", base / "build"
    out.mkdir(parents=True, exist_ok=True)
    readable = src / "readable"
    up = sector.upper()
    tbook = json.loads((readable / f"{up}_tactic_book_335.json").read_text())
    cindex = json.loads((readable / f"{up}_combo_index.json").read_text())
    top10 = json.loads((src / f"{up}_top10.json").read_text())

    state_path = base / "review_state.json"
    state = json.loads(state_path.read_text()) if state_path.exists() else {}
    fail, warn, queue = [], [], []

    # ---- tactics ----------------------------------------------------------------------------------
    tactics = tbook["tactics"]
    by_no = {t["single_no"]: t for t in tactics}
    name_ix = {}
    for t in tactics:
        keys = {t["name"]} | set(re.split(r"\s*/\s*", t["name"])) | {re.sub(r"\s*\(.*?\)", "", t["name"])}
        if t.get("also_called"):
            keys |= set(re.split(r"\s*[;,/]\s*", t["also_called"]))
        for k in keys:
            k = k.strip().strip('"“”').lower()
            if k:
                name_ix.setdefault(k, set()).add(t["single_no"])
    for t in tactics:
        t["anchor"] = slug(t["name"].split("/")[0])
        t["stage_slug"] = t["stage"].lower()
    reverse = collections.defaultdict(set)
    for t in tactics:
        for s in t["seen_in_combos"]:
            reverse[s["combo_id"]].add(t["single_no"])

    # ---- category intros + standards ---------------------------------------------------------------
    cats = {}
    for f in sorted(src.glob("scripts/*_CAT*_intro.md")):
        meta, body = frontmatter(f.read_text())
        sec = sections(body)
        cats[meta["category_id"]] = {"category_id": meta["category_id"], "name": meta["category_name"],
                                     "slug": slug(re.sub(r"\s*Composites?$", "", meta["category_name"])),
                                     "intro_md": sec.get("Category Introduction", ""), "combos": []}
    std_meta, std_body = frontmatter((src / f"scripts/{up}_00_SECTOR_STANDARDS.md").read_text())
    standards = sections(std_body)

    # ---- combos: the audit passes ------------------------------------------------------------------
    combos, used_slugs = [], {}
    counts = collections.Counter()
    for row in cindex["combos"]:
        cid, f = row["combo_id"], src / "scripts" / row["file"]
        if not f.exists():
            fail.append(f"{cid}: file {row['file']} missing")
            continue
        raw = f.read_text()
        meta, body = frontmatter(raw)
        sec = sections(body)

        # Pass 1 - structure
        for h in REQUIRED:
            if h not in sec:
                fail.append(f"{cid}: missing section '{h}'")
        for h in NEVER_DROP:
            if not sec.get(h, "").strip():
                fail.append(f"{cid}: '{h}' is empty (must never be dropped)")
        # Pass 2 - safety note matches the index
        has_note = "Safety Note (read first)" in sec
        if has_note != bool(row.get("has_safety_note")):
            fail.append(f"{cid}: safety note in file={has_note} but index says {row.get('has_safety_note')}")
        # Pass 3 - bracket inventory (tags -> queue, slots listed, unknown flagged)
        slots, tagc = [], collections.Counter()
        for h, txt in sec.items():
            if h == "Credibility Audit":
                continue
            for m in BRACKET.finditer(txt):
                tok, kind = m.group(1), classify(m.group(1))
                if kind == "tag":
                    for part in tag_parts(tok):
                        tagc[part] += 1
                        queue.append({"combo_id": cid, "section": h, "tag": part, "kind": TAGS[part],
                                      "text": sentence_around(txt, m.start(), m.end()), "status": "open"})
                elif kind == "slot":
                    slots.append({"section": h, "slot": tok, "text": sentence_around(txt, m.start(), m.end())})
                elif kind == "unknown":
                    warn.append(f"{cid} / {h}: unrecognised bracket [{tok}]")
        counts.update(tagc)
        # Pass 4 - the Credibility Audit, kept as the reviewer's to-do list
        audit = sec.get("Credibility Audit", "")
        for item in re.findall(r"^\d+\.\s+\*\*(.+?):\*\*\s*(.+)$", audit, re.M):
            queue.append({"combo_id": cid, "section": "Credibility Audit", "tag": item[0], "kind": "audit",
                          "text": item[1].strip(), "status": "open"})
        # Pass 5 - tactic resolution: reverse index first, then exact name/alias; never fuzzy
        resolved = []
        for nm in row["tactics"]:
            key = nm.strip().strip('"“”').lower()
            hits = name_ix.get(key, set())
            via_rev = hits & reverse[cid]
            if len(via_rev) == 1:
                resolved.append({"name": nm, "single_no": via_rev.pop(), "via": "reverse_index"})
            elif len(hits) == 1:
                resolved.append({"name": nm, "single_no": next(iter(hits)), "via": "exact_name"})
            else:
                resolved.append({"name": nm, "single_no": None, "via": "unresolved" if not hits else "ambiguous"})
        # Pass 6 - index consistency
        idx_tags = row.get("review_tags", {})
        whole = collections.Counter(p for m in BRACKET.finditer(body) for p in tag_parts(m.group(1)))
        for k, v in idx_tags.items():
            mine = sum(n for t, n in whole.items() if t.startswith(k))  # the index counts the whole file
            if mine != v:
                warn.append(f"{cid}: index says {v}x [{k}], file has {mine}")

        s = slug(row["name"])
        if s in used_slugs:
            s = f"{s}-{slug(row['category'])}"
        used_slugs[s] = cid
        st = state.get(cid, "unreviewed")
        if st not in STATES:
            fail.append(f"{cid}: review_state '{st}' is not one of {STATES}")
        reader = {h: v for h, v in sec.items() if h != "Credibility Audit"}
        combos.append({
            "combo_id": cid, "sector": up, "slug": s, "name": row["name"], "category_id": row["category_id"],
            "tier": row["tier"], "status": row.get("status", meta.get("status")), "review_state": st,
            "tags": meta.get("tags", []), "definition": row.get("definition", ""), "tactics": resolved,
            "has_safety_note": has_note, "sections": reader, "slots": slots, "tag_counts": dict(tagc),
            "reader_words": sum(words(reader_text(v)) for v in reader.values()),
            "source_file": row["file"], "source_words": row.get("words"),
        })
        cats.setdefault(row["category_id"], {"category_id": row["category_id"], "name": row["category"],
                                             "slug": slug(row["category"]), "intro_md": "", "combos": []})
        cats[row["category_id"]]["combos"].append(cid)

    # tactic -> combos, rebuilt from the RESOLVED links (one truth for both directions)
    for t in tactics:
        t["combos"] = sorted({c["combo_id"] for c in combos for r in c["tactics"] if r["single_no"] == t["single_no"]})
        missing = {s["combo_id"] for s in t["seen_in_combos"]} - set(t["combos"])
        t["combos"] = sorted(set(t["combos"]) | missing)  # the author's reverse index always wins

    sector_json = {
        "sector": up, "slug": "entertainment", "title": "Entertainment & Music Industry",
        "book_title": tbook.get("title", ""), "stages": STAGES,
        "tactics": tactics, "combos": combos, "categories": [cats[k] for k in sorted(cats)],
        "standards": standards, "top10": top10["top10"], "top10_method": top10.get("method", ""),
    }
    (out / "sector.json").write_text(json.dumps(sector_json, ensure_ascii=False, indent=1))
    (out / "review_queue.json").write_text(json.dumps(queue, ensure_ascii=False, indent=1))
    if not state_path.exists():
        state_path.write_text(json.dumps({c["combo_id"]: "unreviewed" for c in combos}, indent=1) + "\n")

    # ---- report --------------------------------------------------------------------------------------
    res = collections.Counter(r["via"] for c in combos for r in c["tactics"])
    unres = collections.Counter(r["name"] for c in combos for r in c["tactics"] if not r["single_no"])
    st = collections.Counter(c["review_state"] for c in combos)
    L = [f"# {up} import audit", "",
         f"- Combos: {len(combos)} (tier A {sum(c['tier']=='A' for c in combos)}, B {sum(c['tier']=='B' for c in combos)}); "
         f"tactics: {len(tactics)}; categories: {len(cats)}; safety notes: {sum(c['has_safety_note'] for c in combos)}",
         f"- Review state: " + ", ".join(f"{k} {st.get(k, 0)}" for k in STATES),
         f"- Structural failures: {len(fail)}; warnings: {len(warn)}", "",
         "## Credibility tags (tracked, not errors)", ""]
    L += [f"- [{k}]: {v}" for k, v in counts.most_common()]
    L += [f"- Credibility Audit items kept for reviewers: {sum(q['kind']=='audit' for q in queue)}",
          f"- review_queue.json items: {len(queue)}", "",
          "## Reader fill-in blanks (rendered as visible blanks, not defects)", ""]
    L += [f"- {c['combo_id']} {c['name']} / {s['section']}: [{s['slot']}] in “{s['text'][:140]}”"
          for c in combos for s in c["slots"]] or ["- none"]
    L += ["", "## Tactic links", "",
          f"- via author reverse index: {res['reverse_index']}; via exact name or alias: {res['exact_name']}; "
          f"unresolved: {res['unresolved']}; ambiguous: {res['ambiguous']}",
          "- Unresolved names render as plain text (no link). Add them to the author's reverse index to link them:", ""]
    L += [f"  - {n} ({k}x)" for n, k in unres.most_common()]
    L += ["", "## Structural failures", ""] + ([f"- {x}" for x in fail] or ["- none"])
    L += ["", "## Warnings", ""] + ([f"- {x}" for x in warn] or ["- none"])
    (out / "audit.md").write_text("\n".join(L) + "\n")
    print("\n".join(L[:8]))
    print(f"report: {out / 'audit.md'}")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "ent"))

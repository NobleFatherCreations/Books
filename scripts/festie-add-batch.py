#!/usr/bin/env python3
"""Merge scenario batches from content/festie-gap-scenarios/*.py into the data.

Each batch file exposes ADD = [(slug, scenario_dict), ...]. Validates the full
fourteen-field card contract, the acronym check line, and the guide's outline
before anything is written; appends in file order. Idempotent -- a scenario
whose hook already exists in that guide is skipped.

A scenario may introduce a section the guide's outline does not list, so the
outline is extended automatically and the new key is reported, since
festie-check.py treats an unlisted section as a finding.
"""
import glob
import importlib.util
import json
import re
import sys

DATA = "content/festie-bible-data.json"
SRC = "content/festie-gap-scenarios"
FIELDS = ["section", "hook", "archetype", "clinical", "who", "scene", "tells",
          "happening", "check", "darkTitle", "dark", "move", "say", "truth"]

OUTLINE_DESC = {
    "CAPTURE": "How access and trust get established",
    "CONDITION": "How the situation is shaped once you are in it",
    "CONTROL": "How leverage is held and used",
    "TOOLS": "Practical structures, scripts and kit",
    "COMMUNITY": "The real version versus the counterfeit",
    "ACCOUNTABILITY": "What you owe when the power is yours",
    "EMERGENCY": "What to do when it is already happening",
    "SUPPORT": "Holding the line for yourself and others",
}


def load(path):
    spec = importlib.util.spec_from_file_location("m", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.ADD


def main():
    files = sorted(glob.glob(f"{SRC}/*.py"))
    if not files:
        raise SystemExit("no batch files found")
    d = json.load(open(DATA, encoding="utf-8"))
    by_slug = {g["slug"]: g for g in d["guides"]}
    added = skipped = 0
    new_sections = []

    for path in files:
        for slug, sc in load(path):
            g = by_slug.get(slug)
            if g is None:
                raise SystemExit(f"{path}: no guide with slug {slug!r}")
            for f in FIELDS:
                if f not in sc:
                    raise SystemExit(f"{path}: {slug}/{sc.get('hook')}: missing {f}")
                v = sc[f]
                if isinstance(v, str) and not v.strip():
                    raise SystemExit(f"{path}: {slug}/{sc['hook']}: {f} is empty")
                if f == "tells" and len(v) < 3:
                    raise SystemExit(f"{path}: {slug}/{sc['hook']}: only {len(v)} tells")
            if not sc["check"].startswith(g["acronym"]):
                raise SystemExit(f"{path}: {slug}/{sc['hook']}: check must open with {g['acronym']}")
            letters = {c for c in g["acronym"] if c.isalpha()}
            m = re.search(r'—\s*[“"]?([A-Z])[”"]?\s*CHECK', sc["check"])
            if not m or m.group(1) not in letters:
                raise SystemExit(f"{path}: {slug}/{sc['hook']}: check letter not in {g['acronym']}")
            if any(x["hook"] == sc["hook"] for x in g["scenarios"]):
                skipped += 1
                continue
            if sc["section"] not in {o["key"] for o in g["outline"]}:
                g["outline"].append({"key": sc["section"],
                                     "desc": OUTLINE_DESC.get(sc["section"], sc["archetype"])})
                new_sections.append(f"{g['acronym']}/{sc['section']}")
            g["scenarios"].append({f: sc[f] for f in FIELDS})
            added += 1

    if added:
        json.dump(d, open(DATA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        open(DATA, "a", encoding="utf-8").write("\n")
    if new_sections:
        print("outline extended:", ", ".join(new_sections))
    tot = sum(len(g["scenarios"]) for g in d["guides"])
    print(f"{added} added, {skipped} already present — {len(d['guides'])} guides, {tot} scenarios")
    return 0


if __name__ == "__main__":
    sys.exit(main())

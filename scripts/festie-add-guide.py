#!/usr/bin/env python3
"""Merge a new guide from content/festie-new-guides/ into the Bible's data.

Usage: festie-add-guide.py <slug> [--after <slug>]

Each new guide lives as <slug>.py (the GUIDE skeleton) plus one or more
<slug>_scenarios*.py files (SCENARIOS lists), split only so they stay
readable. This assembles them, validates the shape before touching anything,
and inserts the guide into content/festie-bible-data.json.

Idempotent: re-running replaces the guide in place rather than duplicating
it, so a guide can be revised by editing its source files and re-running.
"""
import argparse
import glob
import importlib.util
import json
import sys

DATA = "content/festie-bible-data.json"
SRC = "content/festie-new-guides"

SCENARIO_FIELDS = ["section", "hook", "archetype", "clinical", "who", "scene",
                   "tells", "happening", "check", "darkTitle", "dark",
                   "move", "say", "truth"]


def load(path, attr):
    spec = importlib.util.spec_from_file_location("m", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return getattr(m, attr)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--after", help="insert after this guide slug (default: append)")
    a = ap.parse_args()

    guide = dict(load(f"{SRC}/{a.slug}.py", "GUIDE"))
    parts = sorted(glob.glob(f"{SRC}/{a.slug}_scenarios*.py"))
    if not parts:
        raise SystemExit(f"no scenario files found for {a.slug}")
    scenarios = []
    for p in parts:
        scenarios.extend(load(p, "SCENARIOS"))
    guide["scenarios"] = scenarios

    # --- validate before writing ----------------------------------------
    letters = [c for c in guide["acronym"] if c.isalpha()]
    if letters != [c["letter"] for c in guide["checks"]]:
        raise SystemExit(f"acronym {guide['acronym']} does not match its checks")
    promised = {o["key"] for o in guide["outline"]}
    delivered = {sc["section"] for sc in scenarios}
    if promised - delivered:
        raise SystemExit(f"outline promises {sorted(promised - delivered)} "
                         f"but no scenario delivers it")
    if delivered - promised:
        raise SystemExit(f"scenarios use sections {sorted(delivered - promised)} "
                         f"not in the outline")
    hooks = [sc["hook"] for sc in scenarios]
    if len(set(hooks)) != len(hooks):
        raise SystemExit("duplicate hooks within the guide")
    for n, sc in enumerate(scenarios, 1):
        for f in SCENARIO_FIELDS:
            if f not in sc:
                raise SystemExit(f"#{n} {sc.get('hook')}: missing field {f}")
            if isinstance(sc[f], str) and not sc[f].strip():
                raise SystemExit(f"#{n} {sc['hook']}: {f} is empty")
        if not sc["check"].startswith(guide["acronym"]):
            raise SystemExit(f"#{n} {sc['hook']}: check does not open with the acronym")
        if len(sc["tells"]) < 3:
            raise SystemExit(f"#{n} {sc['hook']}: only {len(sc['tells'])} tells")

    # --- insert ----------------------------------------------------------
    d = json.load(open(DATA, encoding="utf-8"))
    existing = [g["slug"] for g in d["guides"]]
    if a.slug in existing:
        d["guides"][existing.index(a.slug)] = guide
        where = "replaced"
    elif a.after:
        if a.after not in existing:
            raise SystemExit(f"--after {a.after}: no such guide")
        d["guides"].insert(existing.index(a.after) + 1, guide)
        where = f"inserted after {a.after}"
    else:
        d["guides"].append(guide)
        where = "appended"

    # sectionOf is the guide's 1-based position and must be renumbered
    for i, g in enumerate(d["guides"], 1):
        g["sectionOf"] = i

    json.dump(d, open(DATA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    open(DATA, "a", encoding="utf-8").write("\n")
    words = sum(len(str(v).split()) for sc in scenarios for v in sc.values())
    print(f"{guide['acronym']} ({guide['role']}): {len(scenarios)} scenarios, "
          f"~{words:,} words, {where}")
    print(f"the Bible is now {len(d['guides'])} guides, "
          f"{sum(len(g['scenarios']) for g in d['guides'])} scenarios")
    return 0


if __name__ == "__main__":
    sys.exit(main())

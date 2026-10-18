#!/usr/bin/env python3
"""Append scenarios from content/festie-new-guides/gapfill.py to existing guides.

Used for filling sections a guide's own outline promised but never delivered.
Idempotent: a scenario whose hook is already present is skipped.
"""
import importlib.util
import json
import sys

DATA = "content/festie-bible-data.json"
SRC = "content/festie-new-guides/gapfill.py"
FIELDS = ["section", "hook", "archetype", "clinical", "who", "scene", "tells",
          "happening", "check", "darkTitle", "dark", "move", "say", "truth"]


def main():
    spec = importlib.util.spec_from_file_location("m", SRC)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    d = json.load(open(DATA, encoding="utf-8"))
    added = 0

    for slug, sc in m.FILL.items():
        g = next((x for x in d["guides"] if x["slug"] == slug), None)
        if g is None:
            raise SystemExit(f"no guide with slug {slug}")
        for f in FIELDS:
            if f not in sc or (isinstance(sc[f], str) and not sc[f].strip()):
                raise SystemExit(f"{slug}/{sc.get('hook')}: missing or empty {f}")
        if not sc["check"].startswith(g["acronym"]):
            raise SystemExit(f"{slug}: check does not open with {g['acronym']}")
        letters = {c for c in g["acronym"] if c.isalpha()}
        import re
        mm = re.search(r'—\s*[“"]?([A-Z])[”"]?\s*CHECK', sc["check"])
        if not mm or mm.group(1) not in letters:
            raise SystemExit(f"{slug}: check letter not in {g['acronym']}")
        if any(x["hook"] == sc["hook"] for x in g["scenarios"]):
            continue
        g["scenarios"].append({f: sc[f] for f in FIELDS})
        added += 1
        print(f"  {g['acronym']:12} + {sc['hook']}  [{sc['section']}]")

    if added:
        json.dump(d, open(DATA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        open(DATA, "a", encoding="utf-8").write("\n")
    print(f"{added} scenario(s) added; "
          f"{len(d['guides'])} guides, {sum(len(g['scenarios']) for g in d['guides'])} scenarios")
    return 0


if __name__ == "__main__":
    sys.exit(main())

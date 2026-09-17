#!/usr/bin/env python3
"""Inject content/festie-bible-data.json into library/festival/index.html.

The sidecar JSON is the single source of truth for The Festie Bible's content,
the way chapters.json is for the books. The page carries two derived blobs:

  FESTIE_DATA    — the content itself
  SCENARIO_INDEX — the per-guide jump index, derivable from the data exactly
                   ({slug: {section: [{hook}, ...]}}), so it is regenerated
                   here rather than hand-maintained.

Run this after any edit to the JSON, then scripts/festie-check.py --inline.
"""
import json
import sys

DATA = "content/festie-bible-data.json"
PAGE = "library/festival/index.html"


def span(src, marker):
    """Byte span of the JS object literal following `marker`."""
    i = src.find(marker)
    if i < 0:
        raise SystemExit(f"marker not found: {marker}")
    i += len(marker)
    depth = 0; j = i; instr = False; esc = False
    while j < len(src):
        c = src[j]
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
                    return i, j + 1
        j += 1
    raise SystemExit(f"unterminated object after {marker}")


def build_index(d):
    idx = {}
    for g in d["guides"]:
        by_section = {}
        for sc in g["scenarios"]:
            by_section.setdefault(sc["section"], []).append({"hook": sc["hook"]})
        idx[g["slug"]] = by_section
    return idx


def main():
    d = json.load(open(DATA, encoding="utf-8"))
    src = open(PAGE, encoding="utf-8").read()
    before = src

    # SCENARIO_INDEX first: rewriting FESTIE_DATA would move its offsets.
    i, j = span(src, "const SCENARIO_INDEX = ")
    src = src[:i] + json.dumps(build_index(d), ensure_ascii=False, separators=(",", ":")) + src[j:]

    i, j = span(src, "const FESTIE_DATA = ")
    src = src[:i] + json.dumps(d, ensure_ascii=False, separators=(",", ":")) + src[j:]

    if src == before:
        print("festie-build: page already matches the data")
        return 0
    open(PAGE, "w", encoding="utf-8").write(src)
    n = sum(len(g["scenarios"]) for g in d["guides"])
    print(f"festie-build: injected {len(d['guides'])} guides / {n} scenarios "
          f"-> {PAGE} ({len(src):,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

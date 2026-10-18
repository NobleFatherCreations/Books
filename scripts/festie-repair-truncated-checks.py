#!/usr/bin/env python3
"""Apply the 78 hand-written check completions from
scripts/festie-check-completions.py to content/festie-bible-data.json.

Idempotent: a check that's already closed is left alone, so re-running after
festie-build.py is a no-op. Validates every completion against the same
rules festie-check.py enforces (opens with the acronym, closes its quote,
cites a letter the acronym actually has) before writing anything, and
refuses to run unless the file supplies exactly the 78 known truncated
cards -- if that count ever changes, the completions dict needs revisiting,
not a silent partial apply.
"""
import importlib.util
import json
import re
import sys

DATA = "content/festie-bible-data.json"
COMPLETIONS_FILE = "scripts/festie-check-completions.py"


def load_completions():
    spec = importlib.util.spec_from_file_location("festie_check_completions", COMPLETIONS_FILE)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.COMPLETIONS


def is_truncated(chk):
    return not re.search(r'CHECK:\s*["“](.+?)["”]', chk, re.S) and chk.rstrip().endswith("...")


def main():
    COMPLETIONS = load_completions()
    d = json.load(open(DATA, encoding="utf-8"))
    truncated = []
    for g in d["guides"]:
        for sc in g["scenarios"]:
            if is_truncated(sc["check"]):
                truncated.append((g["slug"], sc["hook"]))

    missing_completions = [k for k in truncated if k not in COMPLETIONS]
    if missing_completions:
        raise SystemExit(f"{len(missing_completions)} truncated card(s) have no "
                         f"completion written: {missing_completions}")

    applied = 0
    for g in d["guides"]:
        letters = {c for c in g["acronym"] if c.isalpha()}
        for sc in g["scenarios"]:
            key = (g["slug"], sc["hook"])
            if key not in COMPLETIONS:
                continue
            if not is_truncated(sc["check"]):
                continue  # already fixed
            new = COMPLETIONS[key]
            if g["acronym"] not in new:
                raise SystemExit(f"{key}: completion doesn't open with {g['acronym']}")
            qm = re.search(r'CHECK:\s*["“](.+?)["”]', new, re.S)
            if not qm:
                raise SystemExit(f"{key}: completion still doesn't close its quote")
            lm = re.search(r'["“]([A-Z])["”]\s*CHECK', new)
            if not lm or lm.group(1) not in letters:
                raise SystemExit(f"{key}: completion cites a letter not in {g['acronym']}")
            sc["check"] = new
            applied += 1

    if applied:
        json.dump(d, open(DATA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        open(DATA, "a", encoding="utf-8").write("\n")
    print(f"{applied} check field(s) completed ({len(truncated)} were truncated before this run)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

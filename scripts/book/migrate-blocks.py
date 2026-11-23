#!/usr/bin/env python3
"""One-time migration: wrap existing parts of the chapters in ::: blocks without changing a word.

  python3 scripts/book/migrate-blocks.py --book longafter            dry run: what would be wrapped
  python3 scripts/book/migrate-blocks.py --book longafter --write    rewrite the NN-*.md files

What gets wrapped (heading included, up to the next "## " heading, Sources or the end of the chapter):
  ::: scene    a section whose first line is the "This example is made up" note
  ::: honest   a section that opens with the honest-check line ("An honest check, just for you")
  ::: action   the last section of a reading chapter (Parts I to XI) when it is short (70 words or under) and not
               already a scene or honest check: the closing "do one thing" step
Only lines are added (":::" fences). Prove it with scripts/book/text-diff.py, which compares the rendered words.
"""
import re, sys
from pathlib import Path

sys.argv, WRITE = [x for x in sys.argv if x != "--write"], "--write" in sys.argv
from common import load, words

SCENE = "*This example is made up"
HONEST = "*An honest check, just for you."
ACTION_MAX = 70


def sections(body):
    """(start, end) line ranges of each "## " section before Sources."""
    lines = body.split("\n")
    heads = [i for i, l in enumerate(lines) if l.startswith("## ")]
    out = []
    for n, h in enumerate(heads):
        if lines[h].strip() == "## Sources":
            break
        end = heads[n + 1] if n + 1 < len(heads) else len(lines)
        while end > h + 1 and not lines[end - 1].strip():
            end -= 1
        out.append((h, end))
    return lines, out


def plan_wraps(c):
    if "\n::: " in "\n" + c["body"]:
        return None, []
    lines, secs = sections(c["body"])
    wraps = []
    for h, e in secs:
        first = next((l for l in lines[h + 1:e] if l.strip()), "")
        if first.startswith(SCENE):
            wraps.append((h, e, "scene"))
        elif first.startswith(HONEST):
            wraps.append((h, e, "honest"))
    if c["part"] not in ("start", "tools") and secs:
        h, e = secs[-1]
        if not any(w[0] == h for w in wraps) and len(words("\n".join(lines[h:e]))) <= ACTION_MAX:
            wraps.append((h, e, "action"))
    return lines, wraps


def apply(lines, wraps):
    for h, e, kind in sorted(wraps, reverse=True):
        lines[e:e] = [":::"]
        lines[h:h] = [f"::: {kind}"]
    return "\n".join(lines)


def main():
    a, d, cfg, plan, chs = load(desc=__doc__)
    total, no_action, already = {"scene": 0, "honest": 0, "action": 0}, [], []
    new_body = {}
    for c in chs:
        lines, wraps = plan_wraps(c)
        if lines is None:
            already.append(c["slug"]); continue
        for w in wraps:
            total[w[2]] += 1
        if c["part"] not in ("start", "tools") and not any(w[2] == "action" for w in wraps):
            no_action.append(c["slug"])
        if wraps:
            new_body[c["slug"]] = (c["body"], apply(lines, wraps))
    print("would wrap" if not WRITE else "wrapped", total)
    print("reading chapters with no short closing step:", len(no_action), ", ".join(no_action))
    if already:
        print("already migrated, skipped:", len(already))
    if WRITE:
        by_file = {}
        for c in chs:
            if c["slug"] in new_body:
                by_file.setdefault(c["file"], []).append(new_body[c["slug"]])
        for name, pairs in by_file.items():
            f = d / name
            t = f.read_text(encoding="utf-8")
            for old, new in pairs:
                assert t.count(old) == 1, (name, old[:60])
                t = t.replace(old, new)
            f.write_text(t, encoding="utf-8")
        print("files rewritten:", len(by_file))


if __name__ == "__main__":
    main()

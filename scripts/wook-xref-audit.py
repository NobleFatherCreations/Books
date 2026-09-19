#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify every "(ChN)" callout in the book's appendices against reality.

The seven-chapter expansion renumbered the book, and the renumber pass
updated prose references ("Chapter 12") but not the parenthesised chapter
tags in the appendix indexes, which use a different shape -- "(Ch7/Ch21)".
This finds every one of those, resolves the named Track or Counter-Drop to
the chapter(s) it actually lives in, and reports the mismatches.

    python3 scripts/wook-xref-audit.py          # report
    python3 scripts/wook-xref-audit.py --fix    # rewrite the stale tags
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WOOK = ROOT / "library/wook/index.html"


def load():
    raw = WOOK.read_text(errors="surrogateescape")
    raw = re.sub(r'(src="data:[^"]{200,}")', 'src="data:..."', raw)
    starts = {int(m.group(1)): m.start() for m in
              re.finditer(r'<div class="chwrap s\d" data-ch="(\d+)">', raw)}
    ends = {int(m.group(1)): m.start() for m in
            re.finditer(r'<i class="ch-end" data-ch="(\d+)">', raw)}
    return raw, starts, ends


def build_index(raw, starts, ends):
    """name -> set of chapters it actually appears in (Track titles and
    Counter-Drop names, matched on the rendered text)."""
    flat_spans = []
    for n in sorted(starts):
        seg = raw[starts[n]:ends[n]]
        flat_spans.append((n, re.sub(r"<[^>]+>", "", seg)))
    return flat_spans


def chapters_containing(flat_spans, name):
    key = name.lower().replace("’", "'")
    out = set()
    for n, text in flat_spans:
        if key in text.lower().replace("’", "'"):
            out.add(n)
    return out


def main():
    fix = "--fix" in sys.argv
    raw, starts, ends = load()
    flat_spans = build_index(raw, starts, ends)

    # appendix entries look like:  The Pattern Map (Ch21/Ch25)
    pat = re.compile(r"(The [A-Z][^<>()·\n]{2,55}?)\s*\((Ch\d+(?:/Ch\d+)*)\)")
    findings, fixes = [], []
    seen = set()
    for m in pat.finditer(raw):
        name = m.group(1).strip()
        claimed = {int(x) for x in re.findall(r"Ch(\d+)", m.group(2))}
        if (name, tuple(sorted(claimed))) in seen:
            continue
        seen.add((name, tuple(sorted(claimed))))
        actual = chapters_containing(flat_spans, name)
        if not actual:
            findings.append(("UNRESOLVED", name, claimed, actual))
            continue
        # A tag points at where the thing is DEFINED. Appearing in later
        # chapters too is a callback, not a defect -- so only a claimed
        # chapter where the name appears nowhere is wrong.
        bogus = claimed - actual
        if bogus:
            findings.append(("STALE", name, claimed, actual))
            keep = sorted(claimed & actual) or sorted(actual)[:1]
            new_tag = "/".join(f"Ch{c}" for c in keep)
            fixes.append((m.group(0), f"{name} ({new_tag})"))

    print(f"{len(seen)} parenthesised chapter callouts checked\n")
    for kind, name, claimed, actual in findings:
        c = "/".join(f"Ch{x}" for x in sorted(claimed))
        a = "/".join(f"Ch{x}" for x in sorted(actual)) or "nowhere"
        print(f"  {kind:11} {name:44} says {c:16} actually {a}")
    print(f"\n{len(findings)} problem(s); {len(fixes)} auto-fixable")

    if fix and fixes:
        for old, new in fixes:
            if raw.count(old) >= 1:
                raw = raw.replace(old, new)
        # restore the stripped data URIs by writing from the original file
        original = WOOK.read_text(errors="surrogateescape")
        for old, new in fixes:
            original = original.replace(old, new)
        WOOK.write_text(original, errors="surrogateescape")
        print(f"applied {len(fixes)} fix(es)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

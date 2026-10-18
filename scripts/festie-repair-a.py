#!/usr/bin/env python3
"""Festie Bible, repair pass A — mechanical defects and the version/ledger fix.

Idempotent. Content edits go to content/festie-bible-data.json; renderer and
head edits go to library/festival/index.html. Run scripts/festie-build.py
afterwards to inject the data, then scripts/festie-check.py --inline.
"""
import json
import re
import sys

DATA = "content/festie-bible-data.json"
PAGE = "library/festival/index.html"

# Eight check lines lost their leading acronym characters somewhere in the
# original build -- "S.O.U.N.D. — " became "O.U.N.D. — ", "M.A.R.K.E.T. — "
# became "R.K.E.T. — ". Same class of garbling the v2 notes describe fixing.
TRUNCATED = {"S.O.U.N.D.": "O.U.N.D.", "M.A.R.K.E.T.": "R.K.E.T."}

# Two cards cite a letter their guide's acronym does not contain, so the
# check pointed at nothing. Re-pointed at the check that actually covers the
# card's subject.
RELETTER = {
    # "Do I know what is in what I am taking" -> D, Don't Assume Safe Spaces
    ("P.R.I.D.E.", 9): ("A", "D"),
    # "What does my wellbeing need, not the tour schedule" -> N, No Is A Full Sentence
    ("S.O.U.N.D.", 15): ("B", "N"),
}


def repair_data():
    d = json.load(open(DATA, encoding="utf-8"))
    n_trunc = n_letter = 0

    for g in d["guides"]:
        ac = g["acronym"]
        bad = TRUNCATED.get(ac)
        for n, sc in enumerate(g["scenarios"], 1):
            if bad and sc["check"].startswith(bad + " "):
                sc["check"] = ac + sc["check"][len(bad):]
                n_trunc += 1
            swap = RELETTER.get((ac, n))
            if swap:
                old, new = swap
                pat = f'— “{old}” CHECK'
                alt = f'— "{old}" CHECK'
                if pat in sc["check"]:
                    sc["check"] = sc["check"].replace(pat, f'— “{new}” CHECK', 1); n_letter += 1
                elif alt in sc["check"]:
                    sc["check"] = sc["check"].replace(alt, f'— "{new}" CHECK', 1); n_letter += 1

    # --- version + changelog -------------------------------------------
    # The page rendered a hardcoded 'v6' while sites.json said v7, and the
    # changelog was seven bare strings with no version or date attached, so
    # the two ledgers could not be reconciled by anything but eye. Give the
    # data a version field and dated entries; the renderer now reads both.
    n_ver = 0
    if "version" not in d:
        d["version"] = "v7"; n_ver += 1
    if d["changelog"] and isinstance(d["changelog"][0], str):
        dated = [
            ("v7", "2026-09-01",
             "Added THE HOUSE — the shared catalogue drawer in the top bar, so you "
             "can get to everything else Noble Father Creations makes without leaving "
             "the way you came in. This page had no cross-project navigation before."),
        ]
        # the seven existing strings, newest first, are v6 down to v1
        versions = [("v6", "2026-08-12"), ("v5", "2026-08-11"), ("v4", "2026-08-11"),
                    ("v3", "2026-08-11"), ("v2", "2026-08-10"), ("v1", "2026-08-10"),
                    ("v1", "2026-08-10")]
        for (v, dt), text in zip(versions, d["changelog"]):
            dated.append((v, dt, text))
        d["changelog"] = [{"version": v, "date": dt, "summary": t} for v, dt, t in dated]
        n_ver += 1

    json.dump(d, open(DATA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    open(DATA, "a", encoding="utf-8").write("\n")
    return n_trunc, n_letter, n_ver


def repair_page():
    s = open(PAGE, encoding="utf-8").read()
    before = s
    notes = []

    # 1. the version badge, derived instead of hardcoded, with dated entries
    old_footer = ("'<details class=\"fb-updates\"><summary>v6 — '+FESTIE_DATA.updated+'</summary><ul>'+\n"
                  "      FESTIE_DATA.changelog.map(function(c){ return '<li>'+esc(c)+'</li>'; }).join('')+")
    new_footer = ("'<details class=\"fb-updates\"><summary>'+esc(FESTIE_DATA.version)+' — '+FESTIE_DATA.updated+'</summary><ul>'+\n"
                  "      FESTIE_DATA.changelog.map(function(c){\n"
                  "        /* entries are {version, date, summary}; the older bare-string\n"
                  "           form is still rendered so the page degrades rather than breaks. */\n"
                  "        if (typeof c === 'string') return '<li>'+esc(c)+'</li>';\n"
                  "        return '<li><strong>'+esc(c.version)+'</strong> · '+esc(c.date)+' — '+esc(c.summary)+'</li>';\n"
                  "      }).join('')+")
    if old_footer in s:
        s = s.replace(old_footer, new_footer, 1); notes.append("version badge now derived from the data")

    # 2. copyright line in the visible footer
    old_disc = ("'<div class=\"fb-disclaimer\">For educational purposes only • Noble Father Creations "
                "• In immediate danger? Contact emergency services.</div>'+")
    new_disc = (old_disc + "\n    '<div class=\"fb-disclaimer\">Copyright © 2026 Shae Stovell. "
                "All rights reserved. The Festie Bible and Noble Father Creations are works of "
                "Shae Stovell.</div>'+")
    if old_disc in s and "Copyright © 2026 Shae Stovell" not in s:
        s = s.replace(old_disc, new_disc, 1); notes.append("copyright line added to the footer")

    # 3. machine-readable attribution in <head>, matching the wook book's v11
    if '<meta name="author"' not in s:
        anchor = '<meta name="description"'
        i = s.find(anchor)
        if i >= 0:
            s = (s[:i] + '<meta name="author" content="Shae Stovell">\n'
                 '<meta name="copyright" content="Copyright © 2026 Shae Stovell. All rights reserved.">\n'
                 + s[i:])
            notes.append("author/copyright meta tags added")

    if s != before:
        open(PAGE, "w", encoding="utf-8").write(s)
    return notes


def main():
    t, l, v = repair_data()
    print(f"data: {t} truncated check prefixes, {l} mis-lettered checks, "
          f"{v} version/changelog change(s)")
    for n in repair_page():
        print("page:", n)
    if not (t or l or v):
        print("(data already clean)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

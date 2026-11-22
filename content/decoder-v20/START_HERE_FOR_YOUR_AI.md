# Start here: playbook update for noblefathercreations.com/playbook

**Task:** replace the live playbook's tactic list with the standard list of 335 single tactics, in the page's own data format.

1. **Read first:** `1_DROP_IN_DATA/README.md` (what each file is, what changes), then `3_BRIEFS_AND_RULES/PLAYBOOK_SITE_PROMPT.md` (how the page shows the 335).
2. **The data to upload:** `1_DROP_IN_DATA/playbook_singles.json`. It is `{theme: {tactic name: {21 fields}}}`, 10 themes (people, wear, pressure, control, systems, blame, truth, society, online, hook), exactly one entry per standard single tactic (335, all 21 fields filled, checked). Each live page block `<script type="application/json" id="L-<theme>">` is replaced by the matching theme object.
3. **What happened to each of the 310 live entries:** `1_DROP_IN_DATA/LIVE_ENTRY_CHANGES.csv` (keep 'as is', rename, merge, move to patterns, remove 3 out-of-scope entries, add 110 new). Entries that leave the single list (umbrellas, built-in combos, effects) are in `playbook_patterns.json` for an optional "patterns" section.
4. **Search names:** `standard_index.json` carries each entry's standard id, T-number, stage, definition and "also called" names so old names still find the right entry.
5. **Review document:** `PLAYBOOK_UPDATE.pdf` / `.html` shows every change in readable form; `PLAYBOOK_REDESIGN_AND_METHOD.pdf` explains the method.
6. **Source of truth for names:** `2_STANDARD_LIST/SINGLE_TACTICS.csv` (335 rows: T001-T335, name, definition, stage, also called). `alias_map.json` resolves any other name. `CANONICAL_TACTICS.json` has all 383 entries (including umbrellas, built-in combos and effects); do NOT use it as the page list.
7. **The 110 new entries** were written in the live entries' style and safety posture; their sources are in `4_NEW_ENTRY_SOURCES/` (do not edit outputs by hand; changes go through decisions and `5_TOOLS/playbook_package.py`).

**Rules that apply to anything you write:** recognition and safe routing, never a playbook; observable behavior separate from inferred intent; no unverified statistics, laws or named organizations/people as fact; children, threats, medical and crisis matters route to professionals and emergency services; never advise confronting a danger. Noble Father wording must not be copied into our own lists (the drop-in file keeps the site's own entries only on the site's own list).

**Access note:** the playbook site's code is not reachable from the Claude session that built this package, so the update is for upload, not an automatic deploy.

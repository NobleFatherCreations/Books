# Playbook update package (noblefathercreations.com/playbook)

The live page keeps its data in 10 blocks, `<script type="application/json" id="L-<theme>">{name: {21 fields}}</script>`
(people, wear, pressure, control, systems, blame, truth, society, online, hook). This package keeps that exact format, so each block
can be replaced in one step. This session cannot reach the site's code (only this repository is connected), so the package is for upload.

## Files
| File | What it is |
|---|---|
| `playbook_singles.json` | **The drop-in list.** `{theme: {name: {21 fields}}}` with exactly one entry per standard single tactic (335). Replace each `L-<theme>` block with the matching theme object. |
| `LIVE_ENTRY_CHANGES.csv` | What happens to each of the 310 live entries, and to each added one: keep, rename to the standard name, merge into another entry, move to patterns, remove, or add. |
| `playbook_patterns.json` | The umbrellas, built-in combos and effects that leave the single list (for example Gaslighting, FOG, DARVO, Trauma Bonding), each with what it is made of and its live text, for a separate "patterns" section if wanted. |
| `standard_index.json` | A sidecar per entry: standard id, T-number, stage, standard definition, also-called names. The 21-field schema itself is untouched. |

## What changes on the live list
- **Kept as is:** live entries whose name is already the standard name. Their 21 fields are unchanged.
- **Renamed:** the entry keeps its fields under the standard name (the live name stays searchable through `standard_index.json` also-called).
- **Merged:** where two live entries are now one tactic, the one carrying the standard name keeps its fields, and the other is listed in `LIVE_ENTRY_CHANGES.csv` as merged.
- **Moved to patterns:** live entries that are umbrellas, built-in combos or effects leave the single list.
- **Removed:** 3 out-of-scope entries (MICE, Cognitive Warfare, Adversarial Machine Learning).
- **Added:** 110 standard single tactics the live list lacked, each with all 21 fields written in the live entries' style and safety posture.

Rebuild: `python3 13_TACTICS_FRACTAL/tools/playbook_package.py` (from `Combo_Clusters_MASTER`). It reports any entry with a missing field.

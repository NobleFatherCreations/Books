# Task brief: apply every discrepancy for one volume (substitute {RID} and {PFX})

Repo: /home/user/Books, branch `claude/sacred-divide-v5-redesign`. Do NOT commit, push or deploy. Touch only this volume's files (see Deliverables). Another agent may be working on a different volume in parallel; never edit `_all.json`, `scripts/`, `DISCREPANCIES.md` or another volume's files.

## Goal
The language pass is done. The owner has now authorised fixing every item in `docs/sacred-divide-v5/discrepancies/{RID}.md` (and, for catholicism, `docs/sacred-divide-v5/DISCREPANCIES.md`), including items that touch the frozen layer: numbers, grades, tallies, sources, case tags. Apply them as reversible edits, verified against sources, and leave a fix log.

## Worked example to copy
`content/sacred-divide/edits/protestant-evangelical.json`, entries PE-D001 to PE-D042, and `docs/sacred-divide-v5/protestant-evangelical-FIXLOG.md`. Read both first. Read `docs/sacred-divide-v5/PLAYBOOK-volume-to-pdf-and-tiktok.md` section 2.

## Method
1. Read the volume's discrepancy list, fact-check log (`logs/fact-check/{RID}.md`) and proposals (`docs/sacred-divide-v5/proposals/{RID}.md`). Work item by item, P1 then P2 then P3.
2. For each item decide: FIX (apply an edit), FIX-WITH-NEW-SOURCE, or DEFER. Defer only when (a) it needs a decision across all volumes (house style), (b) it needs new research the owner has not asked for (new sections, new cases not in the proposals), or (c) you cannot establish the correct fact. Say why in the fix log. Everything else is fixed.
3. Append entries to `content/sacred-divide/edits/{RID}.json` with ids `{PFX}-D001`, `{PFX}-D002`, ... (`status: proposed`, a `reason` naming the item). Use the same entry format as the existing ones; `before` must match the current exported text exactly, count 1 unless intentionally more. Run `python3 scripts/sacred-divide-export-md.py` and confirm every `{RID}` entry shows `applied` in `logs/edits-status.json` (none FAILED); then run `build_sections('{RID}')` from `scripts/sacred-divide-pdf-expanded.py` to confirm narration edits apply.
4. **Facts**: before replacing a claim, check the primary source (WebSearch/WebFetch). Replace overstated or wrong claims with what the source supports. Never soften a claim the source supports. If a claim cannot be verified, remove or qualify it ("not recorded on this page") instead of asserting it.
5. **Sources**: add new numbered sources at the END of §26 (after the last existing entry, in the existing format), cite them where used. Never renumber existing sources.
6. **Grades**: where an item says a grade does not match its entry, regrade to the grade the entry's own basis supports and rewrite the `**Evidence grade.**` line. Remove `*(sourced)*` from any technique that names no document. Then recompute the §1 Evidence row (counts of each grade; number "sourced to a named document") so it matches the §12 chips exactly (count with grep on `^\*\*Evidence grade.\*\* \[\[Grade\]\]`; for table-format §12 count the grade cells). Update any other place that repeats the tally.
7. **Case tags**: change `- **tactics:**` lines when a tag is unsupported by the case text; make sure every number exists in §12.
8. **Loops**: where a loop summary describes something the volume never records, rewrite the summary to match what the steps record, or mark the gap ("not recorded on this page"); never move text between cards.
9. **Template leaks**: for non-theistic traditions rewrite "attributed to God" (stage 8 and technique 30) to name the tradition's own authority. For shared §9 pipeline cards that do not fit the tradition, remove the false claim or the card's unsupported lines; do not invent replacements.
10. **Help lines**: if the discrepancy file lists a wrong number or missing hours for this volume only, fix it. Global help-line corrections (ALL-F01 to F06) already exist; do not repeat them.
11. **Meta**: set `checked:` and the "Last checked" glance row to 2026-10-03, and add a dated bullet at the top of §27 describing, in plain reader language, what changed (no file paths, no jargon).
12. Narration: edits with `scope: narration` only where a narration sentence is wrong after your changes. The case-count sentence is now generated correctly; do not add a patch for it.

## Deliverables
- `content/sacred-divide/edits/{RID}.json` (all applied, 0 FAILED).
- `docs/sacred-divide-v5/{RID}-FIXLOG.md`: table mapping every discrepancy item (by its number) to FIXED / FIXED WITH NEW SOURCE / DEFERRED, the edit ids, and for deferred items the reason. Also list any new sources added and the new grade tally.
- Update `docs/sacred-divide-v5/discrepancies/{RID}.md`: append a line "Resolved: see {RID}-FIXLOG.md" under each fixed item heading is NOT needed; instead add one line at the top: `Status 2026-10-03: fixes applied, see {RID}-FIXLOG.md (deferred items remain open).`

## Final report (short)
Items fixed / deferred (counts), the new grade tally, new sources added, any claim you could not verify, and any problem for the owner. Do not paste large text.

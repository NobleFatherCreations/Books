# Audit: The Weighing v5, before design (2026-11-24)

Done in a Claude Code session with npm and Playwright working, to re-check the work from `docs/HANDOFF-WEIGHING-2026-11-24.md` (branch `claude/nice-ride-fqzura`). That session had package installs turned off. Its branch was fast-forwarded into `claude/hopeful-brahmagupta-yzhqr6`. Nothing was lost (244 commits ahead, 0 behind). Nothing deployed; no text changed.

Note: the uploaded `handoff-2026-11-23.zip` is the older Long After handoff, written before The Weighing was chosen. The Weighing handoff replaces it.

## 1. Re-checked and confirmed

| Check | Result here |
|---|---|
| Source checks (rewrite-check, 15 files) | clean |
| Build | 68 pages + index, contents, search, all; sitemap 70 URLs |
| Manifest, beacon, findability, on-page, Decoder links, seal menu | all pass |
| Screenshots 375/1440 + reduced motion (10 pages) | no overflow, errors or stuck content |
| Numbers in the handoff | match: 109,144 words, 0 paragraphs over 90, 0 chapters over grade, 67/68 handoffs |
| Reports (readability, meso, taxonomy) | rebuild identically (no diff) |
| AI-tell scan of the text | 2 "not X, but Y" shapes and 2 em dashes in 122,850 words: clean |
| Live site | still v4. Live index matches the repo byte for byte. Contents differs only by the known menu count (310 vs 335) |

## 2. What couldn't be done, or was done only partly

1. **Accessibility scan (axe) was never run.** It has now run here on **all 70 pages**: **26 pages fail**. Both faults come from the comparison tables (`::: compare`):
   - **Serious, 16 pages:** the table's scroll box (`<div class="tbl">`) can't be reached by keyboard. Fix: `tabindex="0" role="region" aria-label="…"` on the wrapper.
   - **Minor, 10 pages:** the first header cell is empty (`<th></th>`). Fix: give it visually hidden text, or make it a `<td>`.
   - The fix belongs in `scripts/book/shell.py`, which The Long After shares. Changing it changes The Long After's built pages too, so that needs a yes, or a Weighing-only switch.
2. **The pipeline's axe step is weak.** It checks only 10 pages, which would have missed 16 of the 26 failures. When it installs axe itself, it also loses track of Playwright (`NODE_PATH` is replaced, not added to). Both are small fixes in `scripts/scale-pipeline.sh`.
3. **No text snapshot yet.** Flow rule 4 says the words stay frozen during design (`scripts/book/text-diff.py snap`). No snapshot exists, so nothing yet enforces the freeze.
4. **Design hasn't started.** The R1 gate run was interrupted and thrown away. There's no `design/scale-v5/` yet: no contact sheets, comps or guards.
5. **Speed problems confirmed:** `when-weighing-stops` CLS 0.3 (limit 0.1), cover LCP 2.5s (limit 2.5s).
6. **Records slightly stale:** `FACTS-TO-CHECK.md` still marks the SEARCH-DEMAND item OPEN, but commit `2964b35d` says it was done (check it, then relabel). Citation details are still missing (for example the Kelly and Johnson 2008 DOI). None of them changes a claim.
7. **Content-freeze step:** BOOK-FLOW-V3 says to send the owner two rendered chapters at freeze. The freeze answers are recorded, but there's no record that rendered pages were shown.

## 3. Still needs the owner (no action without a yes)

- Fix the table accessibility in the shared shell (affects The Long After's next deploy too), or only for The Weighing?
- Inbound links from other books (13-link plan in `content/scale-v2/CROSS-LINKS.md`). Each one needs that site deployed by name.
- Pattern Decoder rebuild (picks up about 95 v5 links), and the homepage `hub/llms.txt` fix (tagline repeated 4 times).
- Person JSON-LD `url` (homepage vs /about), which is shared by every book.

## 4. Order from here

1. **Tooling (no owner needed):** fix the pipeline's axe step so it adds to `NODE_PATH` and scans every page.
2. **Accessibility fix** for the comparison tables (needs the owner's answer above). Re-run axe until all 70 pages are clean.
3. **Snapshot the words:** `text-diff.py snap library/scale <scratch>/scale-v5-text.json` after a fresh build.
4. **R1:** design gates on cover, `the-gradient`, `field-card`, `when-weighing-stops` × phone-dark, phone-reduced, desktop-dark. Run one page at a time in the background. Record the faults in `content/scale-v2/DESIGN-STATE.md`.
5. **R2:** concept sentence and budget.
6. **Three comps, phone A | B | C sheets.** One message to the owner with at most 4 questions: pick by picture, discreet mode, and two rendered chapters to look at (this covers the step 7 gap in section 2). Bundle the section 3 decisions here if there's room.
7. **Build the pick into `build_scale_v2.py`:** style all 15 blocks and fix the CLS 0.3 and LCP.
8. **Gates, then one critic** (`impeccable-finish-reviewer`), then the fix round. Each fix gets a failing-first guard in `design/scale-v5/check-*.mjs`.
9. **Final checks:** full pipeline including axe on every page = 0, `text-diff.py check` = only new UI strings, then perf.
10. **Release only on "deploy The Weighing"** (handoff section 3, Phase 5). Restore the v4 copy after every pipeline run until then: `git checkout -q library/scale && git clean -fdq library/scale`.

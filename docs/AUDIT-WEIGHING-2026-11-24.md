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

## 3b. Skill-by-skill recheck (second pass, same day)

The 11-23 handoff names the skills for each stage. The repo shows only `no-ai-slop` (in the writing brief), schema work and screenshots were used, so every pre-design audit skill was run here on the built v5 pages.

| Skill or tool | Result | Action |
|---|---|---|
| `seo-audit` | Canonicals, single H1, heading order, alt text, broken links, orphans, keyword overlap, sitemap: all clean. **All 68 descriptions were cut mid-sentence with "…"**, and 19 dropped the page's main phrase | Builder now ends on a whole sentence when that gives 110+ chars (34 of 68). 22 hand-written lines drafted in `content/scale-v2/DESC-DRAFTS.md` for the owner to approve; the builder reads a `desc:` header |
| `schema` | **The shared validator never scanned The Weighing** (`scale` missing from its list). Added: 72 pages valid against schema.org; all 38 FAQ answers match visible text. Google retired FAQ rich results in May 2026, so FAQ markup now serves AI readers only | Fixed `scripts/seo/validate_schema.py` |
| `ai-seo` | 68/68 short answers are 50-60 words and lead the page; dateModified, author, llms.txt and robots (all AI crawlers allowed) good. Sources sit in a closed details block, with **all 91 links as plain text** | Optional: make source links clickable (shared renderer, so also The Long After) |
| Citations (Crossref, DataCite, browser) | **All 44 DOIs are real and match their authors, titles and years.** The 12 web sources are live (FTC and BWSS block bots but exist) | None |
| `information-architecture`, `site-architecture` | Every page is 1 click from the cover; no orphans; the 56 sister-book pages and 99 Decoder pages linked to are all live; **all 40 live v4 addresses still exist in v5** | None |
| `no-ai-slop` (detect) | 121k words: 0 banned words used as filler, 0 puffery, 0 weasel attribution, 2 em dashes. About 26 "isn't X, it's Y" shapes, mostly real distinctions | Optional, text is frozen: "Intuition isn't mysticism. It's...", "Night-time thinking isn't worthless. It's..." |
| `copy-editing` | No typos or broken markup. **Spelling mix:** "judgment" 24 vs "judgement" 19 in the text; links show "weaponized" while prose says "weaponised" (Decoder page names) | Owner yes needed (text frozen) |
| `cognitive-design` | Every chapter has a handle, worked case and recall moment; only the two safety chapters skip the closing "try" (right for crisis pages). 16 recall sorts have 7-15 items | Design: show sorts in batches |
| `better-accessibility`, `web-accessibility` | Skip link first, focus ring at every stop, all controls named, sorts work by keyboard, 320px reflow, 200% text, reduced motion, pinch zoom. **Focus hides under the phone dock** (2.4.11). 38 FAQ "Read more" links had no context | "Read more" named after its question (fixed); dock padding is a design item |
| axe (all 70 pages x 2 themes) | 26 pages failed (tables), then 0 after the builder fix | Fixed in `build_scale_v2.py` only, so The Long After is unchanged |
| `web-perf` | **The layout shift is the web-font swap** (text drops 31-39px when Fraunces arrives; headings use unpreloaded weights; 6 font files, about 420KB). Cover image 96KB | Design items, written into DESIGN-STATE.md |
| `ux-heuristics` (Trunk Test) | Passes: book name, movement and "chapter 12 of 14", title, Search, Contents, Leave on every chapter. Header plus dock take about 17% of a phone screen | Design item |
| Ubersuggest MCP | The earlier research never checked main-keyword volumes. "how to tell if someone is lying" 8,100/mo, "am i overreacting" 1,900, "is it manipulation" 170, "am i the toxic one" 90 (the "...in the relationship" form is 210). **"gut feeling or anxiety" is 0**, and the whole cluster is at most 30/mo, so it's kept as a coverage chapter. Free plan: 3 reports a day, 3 phrases each, so the other ~60 phrases are unchecked | Check the rest on later days if wanted |
| Windsor (Search Console) | 0 Google rows for /scale in 28 days (chapter pages went live 11-21) | Re-check a month after v5 ships |
| `ponytail` | Fixes kept to a few lines in the Weighing builder and the pipeline; no new dependencies | |

Also done: the pipeline's axe step now scans every page and keeps Playwright on `NODE_PATH`; the words-frozen snapshot was taken (`design/scale-v5/text-before.json`, git-ignored, rebuild with `text-diff.py snap`); the stale SEARCH-DEMAND item in FACTS-TO-CHECK is relabelled resolved.

## 4. Order from here

1. ~~Tooling~~ DONE: the pipeline scans every page with axe.
2. ~~Accessibility fix~~ DONE in the Weighing builder only (no owner decision needed, since The Long After is untouched). axe: 0 on all 70 pages.
3. ~~Snapshot the words~~ DONE: `design/scale-v5/text-before.json`.
4. **R1:** design gates on cover, `the-gradient`, `field-card`, `when-weighing-stops` × phone-dark, phone-reduced, desktop-dark. Run one page at a time in the background. Record the faults in `content/scale-v2/DESIGN-STATE.md`.
5. **R2:** concept sentence and budget.
6. **Three comps, phone A | B | C sheets.** One message to the owner with at most 4 questions: pick by picture, discreet mode, two rendered chapters to look at (covers the step 7 gap in section 2), and one yes/no for the text-level items (the 22 descriptions in DESC-DRAFTS.md and judgement/weaponised spelling).
7. **Build the pick into `build_scale_v2.py`:** style all 15 blocks, then the DESIGN-STATE inputs (font swap, cover srcset, dock padding, batched sorts).
8. **Gates, then one critic** (`impeccable-finish-reviewer`), then the fix round. Each fix gets a failing-first guard in `design/scale-v5/check-*.mjs`.
9. **Final checks:** full pipeline including axe on every page = 0, `text-diff.py check` = only new UI strings, then perf.
10. **Release only on "deploy The Weighing"** (handoff section 3, Phase 5). Restore the v4 copy after every pipeline run until then: `git checkout -q library/scale && git clean -fdq library/scale`.

## 5. Steelman: could the writing and SEO be better? (owner asked, 2026-11-24)

Method: argue the strongest case that it falls short, then test it. Close reads of the gradient, am-i-the-one-doing-it (longest), and the crisis pages; repetition measured across all 59 chapters; live search results for the two biggest phrases.

**Verdict: the writing meets the goal and is good, with four improvable points. The SEO on the page is close to the ceiling; the remaining gap is off the page.**

Writing, improvable:
1. **"Dial" means two things in the central chapter.** The seven-step gradient is "a dial", and the three factors (freedom, repetition, response) are also "the three dials below". Rename the factors ("three tests") so the core model is unambiguous. Text change, needs the owner.
2. **The gradient's recall sort runs in order** (rude to abusive), so answers can be guessed from position. Shuffle the eight items. Other sorts should be checked for the same.
3. **The safety refrain appears in 47 of 59 chapters** ("reread This book in the wrong hands", 17 of them "If someone hands you this chapter to..."). Each is tailored and each chapter must stand alone for search visitors, so it stays, but as prose it becomes wallpaper for a front-to-back reader. Fix in design (no text change): render it as one recognisable small guard block so it's instantly identified and easy to skip.
4. **Spelling mix** (judgment/judgement; weaponized/weaponised in link text).

Writing, tested and holds: voice matches the brief (blunt, funny away from safety: "a light switch with a comments section", "what people type at 1am, though, so here we are"); concrete images carry each idea (the dashcam, the dial); research is named, not "studies show"; section lengths (70-600 words) are substantial rather than padded; the 109k length is mitigated by standalone chapters, 50-60 word short answers, Start here routing, the 60-second weigh and the field card.

SEO, steelmanned:
- **"how to tell if someone is lying" (8,100/mo):** page one is Time, NBC, Scientific American, Simply Psychology, Psychology Today, Inc. A new domain with no backlinks won't outrank them on content alone. Realistic wins are the long tail ("over text" 390/mo, "about cheating" 110/mo, both have headings) and AI citations, where the book's research-honest answer (54% accuracy across 206 studies) is more citable than most of page one.
- **"am i overreacting in my relationship":** page one is generic advice blogs and forums. Winnable; the chapter is stronger than what ranks.
- **The real gap is authority, not content:** no inbound links yet. The owner-gated 13-link plan from the sister books (CROSS-LINKS.md) is the cheapest fix; outside links need the `link-building` skill and owner-approved outreach.
- Descriptions: 22 hand-written lines await approval (DESC-DRAFTS.md).

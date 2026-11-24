# Handoff: The Weighing v5 (2026-11-24)

Branch `claude/nice-ride-fqzura` (repo NobleFatherCreations/Books). Last commit before this file: `17db1d65`. Everything is committed and pushed. **Nothing has been deployed.** Live /scale is still v4.

## 0. Paste this to start the next chat

> Read `CLAUDE.md`, then `docs/HANDOFF-WEIGHING-2026-11-24.md` and follow section 3 exactly for **The Weighing** (`content/scale-v2/`, builder `scripts/seo/build_scale_v2.py`). The writing is finished and frozen. Next is Phase 4 design (docs/BOOK-FLOW-V3.md), run with the `design-director` skill, Rescue track. Don't deploy anything unless I say "deploy The Weighing".

## 1. Where things stand

| Phase (docs/BOOK-FLOW-V3.md) | State |
|---|---|
| 0 Intake | DONE. Answers in `content/design/OWNER-TASTE.md` (2026-11-23 Weighing entries). |
| 0.5 Shared tooling | DONE. `scripts/book/shell.py` (Long After still rebuilds byte for byte), `scripts/book/jsbook-to-v2.py`, rewrite-check and accept-pass take a book, `site_manifest.json` has scale. |
| 1 Source | DONE. `content/scale-v2/`: 15 files `00-start.md` … `07-tools.md`, `plan.json` (68 pages, keywords set), `book.json`, `old_routes.json`. |
| 2 Measure | DONE. READABILITY / MESO / TAXONOMY / WORKLIST reports. |
| 3 Writing | DONE and frozen. One agent per file, steelman + fact check (`STEELMAN-1.md`), SEO pass. |
| 3.6 Every check | DONE except axe (see section 4). `bash scripts/scale-pipeline.sh` runs all of them. |
| 4 Design | **NEXT.** Only the start notes exist (`content/scale-v2/DESIGN-STATE.md`). An R1 gate run was interrupted and cleaned up; nothing from it was kept. |
| 5 Release | Not started. |

**The book now:** 59 chapters in six movements, plus 2 Start here pages and 7 Toolbox pages. About 109,000 words (Sources excluded), up from 38 chapters and 21,692 words.
- Every chapter has a unique shape and a `::: handle` (memory line). Every chapter also has a recall moment (tap-to-reveal `::: sort`), worked cases opening with the owner's label "*Made up, but you've met these people.*", reader-language search headings, a closing `::: try`, a handoff link, and Sources where research is stated.
- Checks: 0 paragraphs over 90 words, 0 chapters over grade, 67/68 handoffs, 38 FAQ questions in schema, 48 A to Z terms.
- The heavy chapters, with no humour: `this-book-in-the-wrong-hands`, `before-you-test-is-testing-safe`, `when-weighing-stops`. Their floor rules and the five danger conditions match each other and the field card.

## 2. Owner decisions (binding, all in OWNER-TASTE.md)

- **Book:** The Weighing was chosen over The Silence.
- **Goal:** full coverage, not a word count (up to 100k fine). Every idea fully discussed, SEO, a web of links to the other books, a unique design per chapter with retention tricks.
- **Voice:** "Sharp thinking partner with more than normal humor that's blunt and no filter." No jokes near safety.
- **Example label:** "Made up, but you've met these people."
- **No bridge** from the-gradient to /feminine/the-harm-ladder.
- **Deploy scope:** The Weighing alone, with what's already waiting in its repo (Sacred Divide rename, menu count, meta-description fix). Only on the words "deploy The Weighing".
- **Phone first** (2026-11-21 rule): every effect needs a phone form; critics lead with phone.
- **House rules for this book:** no gamification, streaks, progress or tracking. A plain "N of M" locator is fine.

## 3. Next steps, in order

### Phase 4 design (`design-director` skill, Rescue track; BOOK-FLOW-V3 section 4)
1. **R1.** Build, serve and run the gates on 4 pages (cover, a chapter, a tool page, the crisis page) × phone-dark, phone-reduced and desktop-dark. Then read the contact sheets yourself and write the faults into `content/scale-v2/DESIGN-STATE.md`:
   ```
   python3 scripts/seo/build_scale_v2.py && python3 scripts/nf-catalogue-sweep.py && python3 scripts/visit-counter.py library/scale
   python3 scripts/seo/serve.py &      # serves library/ at http://localhost:8765 (/scale works without .html)
   node scripts/design-gates.mjs http://localhost:8765/scale/<page> design/scale-v5/r1/<name> --profiles phone-dark,phone-reduced,desktop-dark --max 25 --no-motion
   ```
   Pages: `` (cover), `the-gradient`, `field-card`, `when-weighing-stops`. The first run was interrupted by the owner, so run it in the background or one page at a time.
2. **R2.** Write one concept sentence and the budget: one lead style, one signature move, two fonts, one accent per movement, at most 3 effects per screen.
3. **Three comps without touching the builder.** Copy the method in `design/longafter-v6/` (`make-comps.py` injects variant CSS into built pages; `serve-comps.py`, `shoot-comps.mjs`, `make-sheets.py`). Show phone A | B | C sheets of the cover, a chapter, a `::: sort` / `::: tree` page and a printable sheet. **The owner picks by picture**; ask about discreet mode in the same question (The Long After has it as an off-by-default toggle).
4. **Build the pick into `build_scale_v2.py`.** The current skin is interim: The Long After's v6 CSS recoloured to v4 brass, plus two wrap fixes. Every Weighing block needs real styling: `handle`, `scene`, `try`, `warn` / `warn danger`, `tree`, `sort` (details reveal), `myth`, `script`, `check`, `compare`, `gradient`, `bridge`, `sheet` (print), `aside`, `pull`. LA-only CSS (blk-action, blk-honest, blk-decoder labels such as "One small step") can go. Skills: `frontend-design`, `cognitive-design`, `emil-design-eng`, `apple-design`. Reduced motion is designed, not stripped.
5. **Gates, then ONE critic** (`impeccable-finish-reviewer` agent) with phone, reduced-motion, desktop and late-movement shots. Then a fix round: every fix gets a guard in `design/scale-v5/check-*.mjs` that fails first.
6. **Known design faults to fix:** CLS 0.3 on `when-weighing-stops` (perf.js; likely font swap or the dock); cover LCP 2.4s.

### Phase 5 release (only on "deploy The Weighing")
1. Bump `BOOK["version"]` in `build_scale_v2.py` to v5, add the v5 line to the on-page Updates (in `index_html()`), and add `sites.json` scale `version` and `changelog` in the same commit.
2. Rebuild, then commit `library/scale/` (built pages are deliberately not committed until release; library/scale is the v4 copy).
3. Stage a copy of `library/scale/` without `*.md` or `qa.js`, Netlify MCP `deploy-site` with siteId `27ab9f53-5850-4fb1-8bed-6513b33ee11f`, then run the returned `npx … --proxy-path …` from the staging folder. Compare live md5 against the repo on 6 pages, on both noble-the-weighing.netlify.app and noblefathercreations.com/scale.
4. Then `python3 scripts/seo/indexnow.py scale`, update `sites.json` lastDeploy, BOOKS.md and MEMORY.md, and send the phone card (at most 4 yes/no device checks).

## 4. Open items

- **axe accessibility scan not run.** `axe-core` isn't installed and package installs were off. Run it where npm works (the pipeline skips with a message otherwise). It must be 0 before release.
- **Inbound links from other books (owner decision, each needs that site deployed by name):** the 13-link plan is in `content/scale-v2/CROSS-LINKS.md`. It also covers a Pattern Decoder rebuild (picks up about 95 v5 Decoder links) and the homepage `hub/llms.txt` fix (The Weighing's line repeats the tagline 4 times, from the build_jsbook book_meta bug).
- **Citation details left out rather than guessed:** see `content/scale-v2/FACTS-TO-CHECK.md` (for example the Kelly and Johnson 2008 DOI). None changes the text's claims.
- **Two on-page warnings that are fine:** "weaponized"/"apologize" keywords vs the book's British spelling, and 38 "Read more" anchors (needed by the FAQ format).
- **Carried from The Long After:** Facebook and Instagram links, the feedback box, and Person JSON-LD `url` pointing to the homepage rather than /about (shared `seo_common.PERSON`; changing it affects every book).

## 5. Map of files

- **Source:** `content/scale-v2/NN-*.md` (`=== slug` / headers title, question, seo, short / `---` / body), `plan.json`, `book.json`, `old_routes.json`.
- **Plans:** `COVERAGE-MAP.md` (gap audit), `CHAPTER-DESIGN.md` (shape, handle, image and links per chapter, plus the block palette), `V5-WRITING-BRIEF.md`, `INBOUND-ANCHORS.txt` (no heading anchors are linked from outside; page addresses must keep resolving).
- **Records:** `STEELMAN-1.md`, `FACTS-TO-CHECK.md`, `CROSS-LINKS.md`, `DESIGN-STATE.md`, `research/SEARCH-DEMAND.md` (+ raw Ubersuggest JSON; Search Console had 0 rows for /scale).
- **Builder:** `scripts/seo/build_scale_v2.py`. It writes index, 68 pages, contents, search, all, sitemap and `llms.txt`. Labels box headings, adds h3 anchors and the Decoder section (via `build_jsbook.decoder_block`), and forwards old `#/c/N`, `#/card` and `#/limits`. `--og` re-renders the share card.
- **Shared:** `scripts/book/shell.py` (block renderer incl. `- q || a` sort reveals, shell CSS and JS, Leave, discreet mode, rail/dock).
- **One-command checks:** `bash scripts/scale-pipeline.sh [--fast]`. It builds, so restore the v4 copy afterwards with `git checkout -q library/scale && git clean -fdq library/scale` until release.
- **Per-file writing gate (if any text changes):** `bash scripts/book/accept-pass.sh <file> <part> "<msg>" scale`.

## 6. Lessons from this run (add to the flow)

- **visit-counter `--all`** only covers each book's index.html. Run `python3 scripts/visit-counter.py library/<book>` too (the redirect page loses its beacon).
- **The 5-hour usage cap hit twice.** Both times the work was on disk: check `git status` and rewrite-check, then resume the same agent with SendMessage.
- **The review pass caught a real safety gap.** The safety gate was missing "cut off from help / leaving made hard". Always cross-check danger lists across chapters.
- **Writers propose keywords in their reports.** Put them in plan.json straight away (the on-page audit needs them).
- **Book home links without a trailing slash** (`/faith`, not `/faith/`): proxy routing.
- **Don't run build_jsbook.py** to fix links in other books (MEMORY 2026-11-23). It was only edited here (a decoder_index title regex fix), not run.

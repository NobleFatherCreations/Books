# Handoff: finish The Long After (for a new Claude Code session)

Written 2026-11-23. **Read this first**, then CLAUDE.md, then MEMORY.md (the last 30 lines), then `docs/BOOK-PIPELINE-V2.md`, which is the method. For history only: `docs/LONGAFTER-PROCESS-MAP.md`.

**Branch:** `claude/modest-keller-vgex1c`. Commit and push there only. No PR unless asked.

---

## 1. Where things stand (exactly)

### The book
- `content/longafter-v2/*.md`: 97 pages, about 107,000 words.
- The writing passed: content audit, AI audit v2, tone audit, steelman 2, fact checks, a sources appendix (263 sources, 104 linked) and 17 honest checks.
- **Built** by `scripts/seo/build_longafter_v2.py` into `library/longafter/`. **Checked** by `bash scripts/longafter-pipeline.sh`.

### Live as of 2026-11-23 (deployed in this session)
| Site | Netlify deploy | Note |
|---|---|---|
| Pattern Decoder v21 | 6b03b699e4e7d11b8f6a4b7c | Verified byte-identical. See `docs/DECODER-V21-PLAN.md`. |
| The Long After v5 | 6b03b6d110f3161d30bc3743 | **The book is now live in its v5 design.** Finishing it means a v6 redeploy. |
| The Sovereign Divine Feminine | 6b03b6deaeb5b4f2eadf3b4c | 121 direct Decoder links (shared with the next three), plus the menu count |
| The Festie Codex | 6b03b71fcb96c6ed3d945aa2 | same |
| The Fractal | 6b03b7368c50e003878f7473 | same (`sectors/` left out on purpose) |
| The Fracture | 6b03b74224201276e70a9d58 | same |
| Playground Protectors | 6b03b6ea228437162c3fc7e3 | **Went beyond what the owner asked for** (menu count only). The owner may want it rolled back in Netlify. |

### The repo is ahead of live, NOT deployed. Do not deploy without the owner naming each site.
- **Menu count 310 → 335 only:** The Sacred Divide, The Festie Bible, The Silence, At Will, The Repair, The Slow Take, The Loop, The Weighing, Portals, Seals, the NFC guide, Root, the Listening Room, Fractal², Fractal entertainment, the reaction map.
- **The homepage and hub files:** robots.txt now lists 17 sitemaps; llms.txt and topics updated. The owner said "deploy the homepage" in the same message, but the deploy was stopped before it ran.
  - The homepage was rebuilt with `build_home.py`. Its only change is the drawer count.
  - It deploys from a staging folder: `catalogue-redesign.html` becomes `index.html`, `catalogue-redesign._redirects` becomes `_redirects`, plus `sites.json` `hub.siteFiles`.

### Owed after the 2026-11-23 deploys
- **`sites.json` lastDeploy:** recorded for the 7 sites above.
- **IndexNow ping** for those 7 (`python3 scripts/seo/indexnow.py ...`). Not run yet: ask first.
- **Search Console and Bing:** the owner's accounts.

### Lesson from this session (binding)
"Deploy X" means only X. When a shared component changes (the menu or the drawer), list every site it touches and **ask about each one** before any deploy. Never treat a sweep's site list as approved.

---

## 2. Ask the owner first, in one message
1. **Composite stories.** Tag each one "A composite story" and explain once in How to use this book? Or keep the current "made up" line?
2. **AI-use disclosure.** Is there a line on how the book was written and checked? The Decoder's About page waits on the same answer.
3. **Voice sample.** Paste 1 or 2 pieces of your own unedited writing for the voice fingerprint pass.
4. **Root and Listening Room links in heavy chapters.** Links only, no autoplay: yes or no?
5. **Which design direction.** Keep Dusk to first light and add the shell mechanics (recommended), or redesign more widely?
6. **Pending sites.** Leave as they are, or deploy which ones? Playground Protectors: keep or roll back?

---

## 3. The order to finish The Long After
Each step ends with a commit, a tracker note (`python3 scripts/longafter-progress.py --phase ... --note ...`) and a short report to the owner: done, changed, still to do.

### Step 1. Tooling the finish needs (no book text changes)
From BOOK-PIPELINE-V2 section 4. Build these as `scripts/book/*` with `--book longafter` where cheap, otherwise extend the Long After scripts:
1. **`site_manifest.json` and `scripts/manifest-check.py`.** One source for book titles, taglines and the Decoder count.
   - `nf-catalogue.py`, `build_site.py`, `build_home.py` and the books' "related" lines read from it.
   - The check fails on any disagreement.
2. **Audit additions for 2am readability:**
   - paragraphs: warn over 60 words, fail over 90
   - no more than 350 words without an anchor
   - reading grade per chapter: crisis chapters 8 or under, others 9, legal 11
   - jurisdiction words in legal and medical lines
   - a handoff line at the end of each chapter
3. **`meso.py`:**
   - the end of chapter N next to the start of N+1
   - the shape sequence
   - concepts defined in more than one chapter
4. **`taxonomy.py`:** bolded terms and A to Z entries checked against Decoder names and aliases.
5. **Block syntax** (`::: short | scene | honest | decoder | action | safety | sheet | bridge | steps`) in `build_longafter_v2.py`, plus a one-time migration script.
   - The script wraps existing honest checks, examples and closing sections in blocks **without changing their words**.
   - Prove it with a word-for-word diff of the rendered text before and after.

Run everything and save the reports in `content/longafter-v2/` as MESO.md, READABILITY.md and TAXONOMY.md. Report the numbers before changing any text.

### Step 2. Writing fixes, in this order (each through the insert gate)
1. **Meso pass.**
   - Fix dead-end chapter endings with handoff lines.
   - Concepts explained more than once (DARVO, grey rock, money untangling, documentation): one full explanation plus links.
   - Check that the part order reads Stabilise, Recognise, Defend, Rebuild.
2. **Rhythm.**
   - Assign each chapter a shape: scenario, question, myth or tool.
   - Change the about 20 chapters needed so no more than two in a row share one.
   - Move honest checks to where resistance peaks.
3. **Readability.** Split long paragraphs. Add anchors (lists, a decoder or a subheading) where a stretch runs over 350 words. Bring crisis chapters to grade 8 or under.
4. **Micro-decisions.** Rewrite each closing section as one physical step of 3 minutes or less.
5. **Dialogue decoders** in the communication, court, co-parenting, hoovering and narrative-campaign chapters. Link each to its Decoder page.
6. **GEO definitions.** Key terms inside chapters get a 40 to 60 word definition directly under a question heading.
7. **Legal jurisdiction.** Every legal or medical line names where it applies, or links to the country page.
8. **Weaponization audit.** For every script, checklist and boundary, ask: could the abuser use this page against the reader?
   - Add counter-notes where needed ("If they copy this wording …").
   - Soften scripts that could read as uncooperative in court.
9. **Voice fingerprint** against the owner's sample. Restore the flattened sharp lines.
10. **Taxonomy lock.** Use the Decoder's names, with everyday synonyms in brackets on first mention.
11. **Cross-book bridges**: At Will (job), The Silence (fathers, children), The Repair (guilt, own behaviour), The Slow Take (later life), Root (grounding). This needs the owner's answer to question 4.
12. **Composite tags**, according to the owner's answer to question 1.
13. **Print-sheet content.** Tag what goes into three sheets: Documentation checklist, Court hearing prep, Safety exit steps.
14. **Light steelman 3 and a fact check** of every new claim. Add new DOIs with `scripts/longafter-sources.py`.
15. **Content freeze.** The owner confirms.

### Step 3. Design (only after the freeze)
- Run the `/design-director` skill and follow `docs/design-catalogue/13-html-books-playbook.md`. Keep Dusk to first light unless the owner says otherwise.
- Build the shared shell mechanics (BOOK-PIPELINE-V2 section 6):
  - triage toggle
  - on-this-page menu, reading time and progress bar
  - block styles, including the honest check (warm, recessed, never alarming)
  - decoder bubbles with Copy
  - inline citations
  - print CSS and field sheets
  - section anchors and share links
  - desktop rail and phone dock
  - part emblems as inline SVG
  - DARVO and cycle diagrams
- **No storage, no outside requests**, and fonts self-hosted.
- Prototype `the-trauma-bond` and `family-court-honestly` first. Screenshot at 375 and 1440, get the owner's look, then roll out to all 97 pages.
- Run the checks: the pipeline (axe, overflow, reduced motion, perf), text-to-speech readout of two chapters, and the OpSec check (beacon is the only outside request, nothing stored, Leave overwrites history).

### Step 4. Release
1. Rebuild in this order:
   1. `python3 scripts/longafter-sources.py --no-lookup`
   2. `python3 scripts/seo/build_longafter_v2.py`
   3. `python3 scripts/nf-catalogue-sweep.py`
   4. `python3 design/build-decoder-v15.py`, so the Decoder's "Where this comes up" sees the new chapters
   5. `python3 scripts/decoder-relink.py --check`
   6. `bash scripts/longafter-pipeline.sh`
2. Version v6: the `sites.json` changelog and the on-page notes together (CLAUDE.md).
3. Ask the owner to deploy, naming the sites. Usually that's The Long After, plus the Decoder if its book mentions changed. Stage, deploy, verify live bytes, IndexNow, then record lastDeploy.

---

## 4. Commands and facts a new session needs
- **Deploy.** Call `netlify-deploy-services-updater` with deploy-site and the `siteId` from `sites.json`. Run the returned `npx … --proxy-path …` command from a staging copy of the site folder.
  - Leave out `*.md` and `qa.js`, and `sectors/` for The Fractal.
  - Each command works only once.
- **Decoder test.** `node scripts/decoder-verify.js instruments/playbook/site/index.html` (it must be given that path; the default is an old draft). 106 of 106. The section-tap check sometimes fails on timing.
- **Never** run `scripts/seo/build_<book>.py` just to fix links. It also rewrites menus, fonts and share images. Use the sweep scripts.
- **The homepage builder** is `scripts/seo/build_home.py` (`build_hub.py` is retired). The pipeline no longer reverts the homepage.
- axe-core lives in `/tmp/longafter-pipeline/node_modules`. The pipeline installs it if it's missing.
- Agents: one at a time (CLAUDE.md). For long text, prefer scripts in the main session.

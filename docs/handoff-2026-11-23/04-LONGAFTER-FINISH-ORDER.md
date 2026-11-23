# Finish The Long After: the optimal order (v5 live, v6 to come)

The full detail of each step is in `reference/HANDOFF-LONGAFTER-FINISH.md` section 3 and `reference/BOOK-PIPELINE-V2.md`. This page puts them in the best order and folds in everything new from 2026-11-23.

**Why this order.** Each phase only touches what the next one depends on.
- **Text before design:** the design has to fit the final text, and a late text change means a second design round.
- **Measurement before rewriting:** the reports tell us which roughly 20 chapters need changes, rather than touching all 97.
- **One release at the end:** one rebuild chain and one deploy.

---

## 0. Session start (one message to the owner, then wait)
Ask, all at once:
1. composite-story wording
2. AI disclosure
3. voice sample
4. Root and Listening Room links
5. design direction
6. Facebook and Instagram links
7. whether to build the feedback box

Default if there's no answer: keep going with steps 1 and 2, which need none of these.

## 1. Tooling first (no book text changes)
Each tool is built so it can be reused for every later book (`scripts/book/*` with `--book <slug>`).
1. **`site_manifest.json` and `scripts/manifest-check.py`.**
   - One source for titles, taglines, counts (335 tactics, 14 books), the author line and the About link.
   - Every builder reads it, and the check fails on any disagreement.
   - *New:* it also holds the "Who made this" one-liner (06), so the colophon line is the same everywhere.
2. **Readability audit:** paragraph length, anchors every 350 words, reading grade per chapter type, jurisdiction words, and a handoff line at the end of each chapter.
3. **`meso.py`:** chapter N's ending next to N+1's opening, the shape sequence, concepts defined twice.
4. **`taxonomy.py`:** bolded terms and A to Z entries against the Decoder's names and aliases.
5. **Block syntax plus a one-time migration.** Prove it with a word-for-word diff that no text changed.

**Output:** MESO.md, READABILITY.md and TAXONOMY.md in `content/longafter-v2/`. **Report the numbers to the owner before changing any text.**

## 2. Writing fixes (in this order; each through the insert gate)
1. **Meso:** dead-end endings, concepts repeated (DARVO, grey rock, money, documentation), and the part order Stabilise, Recognise, Defend, Rebuild.
2. **Rhythm:** chapter shapes, never more than two of the same in a row, and honest checks placed where resistance peaks.
3. **Readability:** split paragraphs, add anchors, crisis chapters at grade 8 or under.
4. **Micro-decisions:** each closing section becomes one physical step of 3 minutes or less.
5. **Dialogue decoders**, each linked to its Decoder page.
6. **GEO definitions** under question headings.
7. **Legal jurisdiction** on every legal or medical line.
8. **Weaponization audit:** could the abuser use this page against the reader?
9. **Voice fingerprint** against the owner's sample. *New:* `content/about.md` is now a strong sample of his raw voice. Use it if he doesn't send another.
10. **Taxonomy lock.**
11. **Cross-book bridges:** At Will, The Silence, The Repair, The Slow Take, Root.
12. **Composite tags.**
13. **Print-sheet content tags.**
14. **Steelman 3 and a fact check** of every new claim (`scripts/longafter-sources.py`).
15. **Content freeze.** The owner confirms.

## 3. New ideas folded in (2026-11-23)
| Idea | Where it goes in the order |
|---|---|
| **"Who made this" line** on every page (06) | Built into the shell in step 4. Text from the manifest (step 1.1). |
| **The bio's "My only ask"** (share it on) | One quiet share line at the end of each chapter, beside the handoff line. Uses the native share sheet (`navigator.share`, nothing stored) with copy-link as fallback. Step 4. |
| **Feedback box** (03 B1) | One link in the book's About section and the colophon: "Tell me how it helped". Only after the box is live on the homepage. |
| **Brand share cards** | `build_longafter_v2.py --og` already has them. Re-run at release. |
| **Decoder v21 names and aliases** | The taxonomy lock (step 2.10) uses v21 data. |
| **Person and Organization schema** | Add `author` → Person (Shae Stovell, with `sameAs` once the links arrive) to the Book and Chapter JSON-LD. Step 4. |

## 4. Design (only after the freeze)
- **Process:**
  - `/design-director`, following `docs/design-catalogue/13-html-books-playbook.md`.
  - Keep Dusk to first light unless the owner says otherwise.
- **Shell mechanics:**
  - triage toggle
  - on-this-page menu, reading time and progress bar
  - block styles (the honest check warm and recessed)
  - decoder bubbles with Copy
  - inline citations
  - print CSS and field sheets
  - section anchors and share links
  - desktop rail and phone dock
  - part emblems
  - DARVO and cycle diagrams
  - *new:* the author strip and the share line (06)
- **Prototype first:** `the-trauma-bond` and `family-court-honestly`. Screenshot at 375 and 1440. The owner looks. Then roll out to all 97 pages.
- **Checks:**
  - the pipeline (axe, overflow, reduced motion, perf)
  - text-to-speech readout of two chapters
  - OpSec: the beacon is the only outside request, nothing is stored, and Leave overwrites history

## 5. Release
1. **Rebuild in this order:**
   1. `python3 scripts/longafter-sources.py --no-lookup`
   2. `python3 scripts/seo/build_longafter_v2.py` (plus `--og`)
   3. `python3 scripts/nf-catalogue-sweep.py`
   4. `python3 design/build-decoder-v15.py`
   5. `python3 scripts/decoder-relink.py --check`
   6. `python3 scripts/visit-counter.py --all`
   7. `bash scripts/longafter-pipeline.sh`
2. **v6:** the `sites.json` changelog and the on-page notes, in the same commit.
3. **Deploy:** ask the owner, naming each site. Usually that's The Long After, plus the Decoder if its book mentions changed. Then deploy, verify the live bytes, run IndexNow, record lastDeploy and write a MEMORY line.

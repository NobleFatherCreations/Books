# Book flow v3: start to finish (proven on The Long After v6, 2026-11-23)

The Long After went from audit to live v6 in one session, using this flow. Run the next book the same way. The recommended next book is **The Silence** (reasons in `docs/handoff-2026-11-23/05-NEXT-BOOK-PLAN.md`). The runners-up, in order, are At Will, The Repair and The Slow Take.

---

## 0. Paste this to start the next chat

> Read `CLAUDE.md`, the last 40 lines of `MEMORY.md`, then `docs/BOOK-FLOW-V3.md` and follow it exactly for **The Silence** (`library/silence/`). Plan with sequential thinking first. Then ask me the Phase 0 questions in one message. Don't deploy anything unless I say "deploy The Silence".

---

## 1. Rules that cost us time (binding)

1. **One background agent at a time.** Wait for its real report before the next. The 5-hour usage cap hit twice this session. When it does:
   - commit what's on disk as WIP and push
   - check the reset time in the error
   - schedule one `send_later` for after it (use today's date, so check `now`)
   - resume the same agent with SendMessage (its work is saved), not a new one
   - send one agent as a canary before continuing
2. **Check every agent's work with a script, never on trust.** Use `scripts/book/rewrite-check.py` (links, Sources, blocks, keyword and crisis links against HEAD) and the content audit. Commit after each file.
3. **A fresh build must reproduce the live pages byte for byte** before any change. That's the baseline. Run build, then `nf-catalogue-sweep.py`, then `visit-counter.py`, then `git status`.
4. **Words stay the same during design:** `scripts/book/text-diff.py snap|check`. Only new UI strings may differ.
5. **Inbound anchors.** List the links from other sites into the book (the `INBOUND-ANCHORS.txt` pattern) and keep those headings word for word. Most `#chapter`/`#crumbs` ids are JSON-LD, not section anchors.
6. **Gate false positives exist.** For example, closed `<details>` content counted as "text over text". Open it and look before "fixing".
7. **Deploy only the named site.** The book deploys alone. If the Decoder's links into the book still resolve (`decoder-relink --check`), the Decoder doesn't need redeploying.
8. **The owner is asked only what only they can answer:** at most 4 questions, by picture where possible, and recorded in `content/design/OWNER-TASTE.md`.

---

## 2. The phases, with skills and commands, in order

### Phase 0. Intake (owner questions, one message)
- **Read:** the book's `BOOK-MAP.md` and `AUDIT.md`, BOOKS.md, `content/about.md` (the owner's voice), and `05-NEXT-BOOK-PLAN.md` (the Silence outline).
- **Ask:**
  - target depth (05 suggests 55-65k words)
  - voice for this book (The Long After got "best friend"; The Silence's brief says plain, short, never "brave")
  - composite-story wording
  - deploy scope
- **Skills:** `sequential-thinking`, `grill-me` if the scope is fuzzy.
- **Search demand:** Ubersuggest and Windsor (Search Console) for the seed phrases in 05.

### Phase 0.5. Make the tooling shared (do this first, once)
The Long After's tools are partly book-specific. Before writing the new book:
1. **Shared shell.** Move the shared part of `scripts/seo/build_longafter_v2.py` into `scripts/book/shell.py`: the `:::` block renderer (decoder structure, Copy), the reading toggle, progress bar, on-this-page menu, byline and author strip, share line, discreet mode, Leave on Escape twice, print sheets, rail and dock, and real checkboxes. Each book keeps its own skin (palette, fonts, cover, part names). Prove The Long After is unchanged with `text-diff.py` plus an md5 of the rebuilt pages. Follow `ponytail`: no framework, plain functions.
2. **Parameterise the checkers.** `scripts/book/rewrite-check.py` and `accept-pass.sh` still hardcode `content/longafter-v2`, so give them `--book`. `readability`, `meso`, `taxonomy` and `worklist` already take `--book` and read `content/<book>-v2/book.json`.
3. **Manifest.** Add the book to `site_manifest.json` and run `manifest-check.py --book <slug>`.

### Phase 1. Source in the book format
- Put the book in `content/<book>-v2/`: `plan.json` (parts, chapters, keyword, keywords2, decoder, heavy) and `NN-*.md` files using the `=== slug` / header / `---` / body format, plus `book.json` (copy The Long After's and adapt: concepts, chapter classes, reference pages, gate thresholds).
- If the book is thin (The Silence is about 11k words), write the expansion outline first, then write part by part, **one agent per file**, the same way as Phase 3.
- Keep any book-specific hard gate. For The Silence, that's `qa.js` AUDIT 6: no comparative grievance; "alongside the book for women, not instead of it".

### Phase 2. Measure (no text changes)
```
python3 scripts/book/readability.py --book <slug>   # paragraphs, unanchored runs, grade by class, place-less legal claims, handoffs
python3 scripts/book/meso.py --book <slug>          # seams, opening-shape runs, concepts defined twice
python3 scripts/book/taxonomy.py --book <slug>      # names against the Pattern Decoder
python3 scripts/book/worklist.py --book <slug>      # per-chapter fix list (fill book.json "step2" first: concept homes, decoder chapters, bridges)
```
Report the numbers to the owner before changing any text.

### Phase 3. The writing pass (the core)
1. **Brief:** copy `content/longafter-v2/V6-WRITING-BRIEF.md` to `content/<book>-v2/` and change only the voice section and any book-specific hard rules. Section 5 of the brief is the worker's procedure.
2. **Pilot one file with one agent.** Read its samples yourself, then tune the brief. For The Long After the pilot was "clean but reserved", so the brief got a nudge toward friend-talk.
3. **One agent per file, in reading order, then the start pages, then the tools.** The prompt can be short, because the brief carries the rules. Name the file, its part id, its concept homes, decoder chapters, bridges, chapters with no closing step, and any headings that must stay word for word.
4. **After each file:** `bash scripts/book/accept-pass.sh <file> <part> "<summary>"` (verifies, commits and pushes).
5. **Then one steelman and fact-check agent** over `git diff <pre-rewrite>..HEAD`. It looks for new claims, safety regressions, gags repeated across chapters (we found 9 copies of the same joke), and humour near safety content. It fixes clear-cut problems and writes `STEELMAN-3.md`. You fix the accuracy items it hands back.
6. **Rebuild and run every check:** content audit, verify_seo, onpage, manifest, decoder-relink, seal-nav, inbound anchors, shoot.js, a11y.js (axe), perf.js. Ask the owner for the **content freeze**, sending two rendered chapters.

### Phase 4. Design (`design-director` v3, Rescue/evolve track)
1. **R1:** `node scripts/design-gates.mjs` on the cover, a chapter, a tool page and the crisis page (phone-dark, phone-reduced, desktop-dark). Read the contact sheets yourself and record the faults in `library/<book>/DESIGN-STATE.md`.
2. **R2:** one concept sentence and the budget (one lead style, one signature move, two fonts, one accent per part, at most 3 effects per screen).
3. **Three comps** without touching the builder: inject variant CSS into built pages, as in `design/longafter-v6/make-comps.py` (with `serve-comps.py`, `shoot-comps.mjs` and `make-sheets.py`). Show phone A | B | C sheets of the cover, a chapter, a decoder block and a checklist. **The owner picks by picture**, and you ask about discreet mode in the same question.
4. **Build the pick into the generator,** using the shared shell from Phase 0.5. Use `frontend-design` and `cognitive-design` for type, colour and hierarchy, and `emil-design-eng` and `apple-design` for touch and motion. Reduced motion is designed, not stripped.
5. **Gates, then ONE critic** (`impeccable-finish-reviewer`). Give it the screenshots it needs: phone, reduced motion, desktop and a late part. Only take findings that help the reader. Owner-approved choices stay (The Long After kept its block labels and both Leave buttons).
6. **Fix round:** every fix gets a guard in `design/<book>-v6/check-*.mjs` that fails first, then passes. Regenerate the phone shots and add a Part I vs late-part side-by-side.

### Phase 5. Release
1. **Versioning:** bump the version in the builder's BOOK dict, add the on-page Updates line (plain language), and add the `sites.json` version and changelog in the same commit.
2. **Deploy,** only on "deploy <book>":
   - Stage a copy of `library/<book>/` without `*.md` or `qa.js`.
   - Netlify MCP `deploy-site` with the site's `netlifySiteId` from `sites.json`, then run the returned `npx … --proxy-path …` from the staging folder.
   - Compare live md5 against the repo on 6 key pages, on both `<name>.netlify.app` and `noblefathercreations.com/<book>`.
3. **Search engines:** `python3 scripts/seo/indexnow.py <book>`, after checking the key file returns 200 and robots.txt lists the book's sitemap. Google has no IndexNow, so the owner can optionally resubmit the sitemap in Search Console.
4. **Log it:** `sites.json` lastDeploy and the changelog marked deployed, the BOOKS.md entry, a MEMORY.md line and DESIGN-STATE. Then send the phone card (at most 4 yes/no device-only checks).

---

## 3. What it took for The Long After (for planning)
- **Agents:** 16 rewrite agents (one per file), 1 steelman, 1 comp builder, 1 design builder (resumed once after the cap), 1 critic and 1 fixer. Two usage-cap pauses.
- **Results:**

  | Measure | Before | After |
  |---|---|---|
  | Paragraphs over 90 words | 2 | 0 |
  | Chapters over grade | 4 | 0 |
  | Place-less legal claims | 54 | 2 |
  | Handoffs | 8/96 | 92/96 |
  | Decoder name drift | 16 | 0 |
  | FAQ questions in schema | 0 | 38 |

  axe 0, CLS 0 to 0.069, live bytes equal to the repo, IndexNow 99 URLs.
- **Key files:**
  - writing: `content/longafter-v2/V6-WRITING-BRIEF.md`, `WORKLIST.md`, `STEELMAN-3.md`
  - tools: `scripts/book/*`
  - design: `design/longafter-v6/*`, `library/longafter/DESIGN-STATE.md`

## 4. Open items carried forward (owner decisions, don't act without a yes)
1. The meta descriptions repeat the tagline on loop, scale, silence, atwill, repair and slowtake. It shows in the live `llms.txt`. The fix is in 02 incident 6. It needs a rebuild of those six and a deploy of each by name.
2. The `/about` page is live, but its source isn't on this branch. Find it before editing.
3. The 16 sites with the 310 → 335 menu count change are in the repo but not live (02 incident 1).
4. Facebook and Instagram links, the feedback box, and the Root and Listening Room links in heavy chapters.

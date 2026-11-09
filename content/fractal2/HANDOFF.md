# Fractal² — hand-off (start here in a new chat)

Repo: NobleFatherCreations/Books · branch `claude/great-keller-jkjz8c` · updated 2026-11-09.
Everything from the 2026-11-09 working thread is in this repo. Nothing for Fractal² has been lost in chat.

## What exists, and where

| What | Path |
|---|---|
| **The prompt for the next stage** (final prose + scroll page) | `content/fractal2/FABLE-PROMPT.md` |
| The owner's own words from the thread (binding intent) | `content/fractal2/owner-source/E-owner-messages-this-thread.md` |
| Owner scripts, verbatim: Spiritual Lens interlude (Part 1) | `content/fractal2/owner-source/A-spiritual-lens-interlude-script-part1.md` |
| Owner scripts, verbatim: Part III The War Map | `content/fractal2/owner-source/B-part-III-the-war-map.md` |
| Owner scripts, verbatim: inner techniques 17–30, Cage & Intent, Full Mirror, Challenge, Empowerment, Practice | `content/fractal2/owner-source/C-inner-techniques-17-30-cage-intent-mirror-practice.md` |
| Owner transcript: Enlighten (closing monologue) | `content/fractal2/owner-source/D-enlighten-closing-monologue-transcript.md` |
| Current intro draft (v4, long form, prose) | `content/fractal2/intro-v4.md` |
| Earlier mission drafts 1–3 | `content/fractal2/mission-draft.md` |
| Three structures steelmanned + critique + fusion | `docs/FRACTAL2-STORY-BLUEPRINT.md` |
| Full series index, all tables, analysis (MD + PDF) | `docs/FRACTAL-SERIES-INDEX.md`, `.pdf` |
| Entertainment sector source (never edit): tactic book (335), combo index, top 10, 153 combo scripts + 10 family intros + standards | `content/fractal/ent/source/` (`readable/*.md`, `scripts/*.md`, `ENT_top10.md`) |
| ENT audit, review queue, review states | `content/fractal/ent/build/audit.md`, `review_queue.json`, `content/fractal/ent/review_state.json` |
| Sector site generator (one command per sector) | `design/fractal-sector/` (`README.md`, `run.sh`) |
| Built ENT site | `library/fractal/sectors/ent/site/` |
| The published Fractal (interludes, sectors) | `library/fractal/` |
| Cross-session notes | `MEMORY.md` (end), `docs/AI-QUICKSTART.md` |

## State of play

- **Direction:** a new witty-titled section at **/fractal2** (working name *Fractal²*), featured on the homepage, opening with one long scroll-driven intro page; sector field guides follow, starting with Entertainment & Music.
- **Intro:** v4 written (prose, owner's lens). Next step is the final prose + the single-page scroll experience: see `FABLE-PROMPT.md`.
- **ENT sector site:** built (174 pages, field-guide look of the PDFs, 16/16 checks). **It is currently public at `fractal-entertainment.netlify.app/fractal/entertainment`** (Netlify site `fractal-entertainment`, id 194814a7-0e80-4b68-b314-0c07911af55a), deployed on 2026-11-09 after the owner's "can launch it live" was read too broadly; the owner had understood it as a prototype. It is not linked anywhere, not on the main domain, and not submitted to search; pages have no `noindex`. Owner said "you can fix it and make it live", but its final address is now expected to sit under **/fractal2** — **confirm with the owner before changing or deploying anything.**
- **Hub routing** for `/fractal/entertainment` and a robots sitemap line: committed in `hub/catalogue-redesign._redirects` and `hub/robots.txt`, **not deployed** (`sites.json` → `hub.pendingDeploy`). Likely to be replaced by `/fractal2` routing; do not deploy as is.
- **Not done:** PDFs on site; a link from the Fractal's Entertainment & Culture chapter; Decoder "seen in these combos" links (alias data is in `content/decoder-v20/`); MUS and SPR sector packages were never received in this thread.

## Rules learned the hard way (binding)

1. "Prototype" means private. Confirm what "live" means before any deploy. Only deploy what the owner names in the current conversation.
2. Explain routing and technical consequences in plain language before asking the owner to decide.
3. At the start of every session: fetch all branches and run `node scripts/verify-deployed.mjs`; another chat's work can be live on another branch (this happened: homepage v17 and Decoder v20).
4. Never edit the owner's scripts or source files; never change wording inside books (connectors/links only, ask first).
5. Patterns, never people. Keep a short safety line on every page.

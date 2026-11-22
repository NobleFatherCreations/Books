# Fractal² — status for the owner and for any AI picking this up

**Date:** 2026-11-10 · **Repo:** `NobleFatherCreations/Books` · **Branch:** `claude/peaceful-planck-k0df08` (everything below is committed and pushed there)
**Deployed:** nothing. The old public prototype (`fractal-entertainment.netlify.app`), the homepage and every published book are untouched.

This file is written to be handed to another AI. Paths are relative to the repo root. Read this, then `content/fractal2/HANDOFF.md`, then the owner's own words in `content/fractal2/owner-source/E-…` and `F-…` (they win every conflict).

---

## A. Fully done (built, tested, committed)

| # | What | Where | Evidence |
|---|---|---|---|
| A1 | **"What I understood" note** and the owner's answers saved word for word | `content/fractal2/WHAT-I-UNDERSTOOD.md`, `owner-source/F-owner-answers-2026-11-09-build-session.md` | — |
| A2 | **Shared design system** ("Deep field"): colours, two typefaces (Newsreader, Hanken Grotesk, self-hosted), spacing, motion, light and dark | `design/fractal2/tokens.css`, `fonts/`, `content/fractal2/DESIGN-SPEC.md` | used by both builds |
| A3 | **Intro page engine**: one fixed stage, one field of 30,151 points, 20 figures driven by scroll, phone and desktop layouts, reduced-motion and no-JavaScript fallbacks, WebGL with Canvas fallback | `design/fractal2/intro.js`, `intro.css`, `build_intro.py` → `library/fractal2/site/fractal2.html` | `node design/fractal2/verify_intro.mjs` → **31 of 31 passed** (run after the first zoom-out change) |
| A4 | **Narration kit**: spoken script generated from the page text (12 takes, about 42 min), plain recording guide, tool that syncs the owner's recording to the page and writes captions (self-tested), player in the page (never autoplays), silent placeholder track | `content/fractal2/narration-script.md`, `RECORDING-GUIDE.md`, `design/fractal2/sync_audio.py`, `library/fractal2/site/fractal2/_a/au/` | player covered by the 31 checks |
| A5 | **Sector site generator v2** and the **Entertainment & Music site: 518 pages**. Home with six "where are you right now" doors and a mini-map; the ten that matter most with score bars; all 153 patterns with filter, sort and narrow; 335 tactic pages; 8 stage chapters; 10 family pages; each pattern in three reading modes over the same words (two-minute, sequence stepper, full); method page; take-it-with-you page; A to Z; search; sector switcher (all thirty sectors); breadcrumbs; quick exit; THE HOUSE drawer; version note | `design/fractal-sector/` → `library/fractal2/site/fractal2/entertainment/` | `design/fractal-sector/run.sh ent`; see section D for the latest count |
| A6 | **"What are you noticing?"** (private, in-page, nothing stored or sent), **three reader paths** (in it now, worried about someone, before you sign), **the living map** (pointer, lists and keyboard; text tables beneath) | `design/fractal-sector/pages_paths.py`, `notice.js`, `map.js` | covered by a dedicated check |
| A7 | **Connections by id, none guessed**: 335 of 335 tactics link to their Pattern Decoder page; every stage links to The Spiritual Lens and The Frequency anchors; sector links to its Fractal chapter; intro links to the Origin, Mirror, Chain, Spiritual Lens and Frequency pages | `content/fractal/ent/build/links.json` | check "every /playbook and /fractal link (15,608) points at a file and anchor in this repo" |
| A8 | **Base path is configurable** (`/fractal2` comes from one file); redirect plan from the old prototype addresses; hub rules written out (not applied) | `content/fractal2/sectors.json`, `library/fractal2/redirects/` | — |
| A9 | **Known defects handled**: stage 6 shown as "Extract · Control"; C144 tag count taken from the script; the Practice numbering and Enlighten spelling errors are not quoted anywhere on the new pages (owner files untouched) | `NAV-SPEC.md` §13, `audit.md` | — |
| A10 | **Docs**: architecture, decisions log (D1–D17), navigation spec, tag policy, rubrics with the director's own scores, three work packets, hand-off, MEMORY entry, `sites.json` registration as undeployed | `content/fractal2/*.md`, `MEMORY.md`, `sites.json` | — |

| A11 | **The series logo**: a gold core named Fractal², eight rings in the original artwork's colours, each stage named once, all 335 tactics evenly spaced and upright, drawn from data so every word is spelled correctly. Plus an emblem without the small names for small sizes | `design/fractal2/logo.py`, `logo_render.mjs`; `design/fractal2/art/fractal2-logo.svg`, `fractal2-emblem.svg`, `fractal2-logo-1600.webp`, `fractal2-logo.json`; renders in `library/fractal2/review/` | looked at full size, top, side and bottom |

## B. Very close to done (works; one named step left)

| # | What | State | The one step left |
|---|---|---|---|
| B1 | **Intro text** (`content/fractal2/intro-final.md`): 11 parts, about 4,700 words; name line "The closer you look, the more there is"; Part VI is exactly the owner's account and is locked by a test (`owner-account.txt`) | Written and revised once by the director | Owner reads it; independent writing review (`work-packets/04-independent-review.md`) not yet run |
| B2 | **Zoom-out figure** in the intro: the original Fractal artwork at the centre, 335 tactic names in rings around it | First version built and working on phone and desktop | Being replaced by the finished logo image (section C1) |
| B3 | **Credibility tag resolution** (ENT): tool, policy and ledger; **1,186 of 1,370 items decided** (718 labels kept; 407 no change; 23 conditional; 23 softened; 8 kept with a fetched source; 2 generalised; 5 safety sentences from the author's own notes added; 0 removed). Pages show the result: honest banner, resolved labels, sources list. Method page shows the totals | Applied in the build | **184 items still open** (118 "sector accuracy" notes, 64 review/source lines, 2 pattern lines). 11 of 45 research topics have sources. The research worker stopped on a usage limit. To finish: follow `work-packets/03-…md` from `content/fractal/ent/resolution/` (ledger entries with `"by": "pending"`), then `resolve.py ent check --final`, `summary`, rebuild. Then the owner approves the 5 added safety sentences and the rewordings once (`resolution/SUMMARY.md`) |
| B4 | **Review material for the owner** | Zoom-out still and sector screenshots exist in `library/fractal2/review/`; a phone scroll recording exists from before the zoom change | Re-record phone and desktop (`node design/fractal2/record.mjs <dir> phone|desktop`) after the logo is in |
| B5 | **Owner report** in plain language with the 22-item "next" list and recommended order | Drafted: `content/fractal2/OWNER-REPORT.md` | Update numbers when B3 and B4 are finished |

## C. Not done

| # | What | Notes |
|---|---|---|
| C1 | **Put the finished logo to work** (the logo itself is done: see A11). Use it in the intro's zoom figure in place of the first version (B2), and adapt it as the sector site's interactive map (owner asked "if possible"). `design/fractal2/art/fractal2-logo.json` already holds the angle and radius of every tactic name for that | Not started: the owner asked to stop after the image |
| C2 | **Independent review** against the rubrics (writing, experience, navigation) and a second iteration | Packet written; not dispatched |
| C3 | **Test on a real phone** | Only headless browser tests so far. Needs a private preview link (a deploy: owner's decision) |
| C4 | **PDFs in "take it with you"** | `ENT_combo_book.pdf` (39 MB) is in the owner's Drive, not in the repo; labels inside not checked. The page currently explains printing |
| C5 | **Owner decisions still open** | name line; "Extract · Control"; shared same-site files for fonts, audio and search data (decision D9); private preview link; approval of tag changes; whether to redirect the public prototype |
| C6 | Everything on the "next" list in `OWNER-REPORT.md` §6 (posting plan, legal pass, crisis resources, share kit, clips, translations, and so on) | Not started by design |

## D. Test results on record

- Intro: **31 of 31** (`node design/fractal2/verify_intro.mjs`).
- Sector site: **27 of 27** on the current build, with the tag ledger applied (`node design/fractal-sector/verify.mjs ent`, 2026-11-10).
- Author word-count round trip: exact on all 153 pattern pages, plus only the changes logged in the ledger.

## E. How to run

```
python3 design/fractal2/build_intro.py && node design/fractal2/verify_intro.mjs
npm i --no-save axe-core && design/fractal-sector/run.sh ent
python3 design/fractal-sector/resolve.py ent check|summary|decisions      # never run "classify" again: it would reset pending work
python3 design/fractal2/serve.py 8802        # http://127.0.0.1:8802/fractal2  and  /fractal2/entertainment
```

## F. Rules that bind any AI working here

1. Deploy nothing unless the owner names it in the current conversation. A preview must be private.
2. Never edit `content/fractal/*/source/` or `content/fractal2/owner-source/`. Never change wording inside published books. Never touch the homepage without asking.
3. Part VI of the intro is the owner's account, exactly. Add nothing.
4. Patterns, never people. Every scene is labelled a composite. A safety line on every page. No page claims expert review.
5. One background worker at a time; on a usage-limit error stop, save, and continue directly.
6. Commit and push after every meaningful step.
7. Text lives in `intro-final.md`; design values in `tokens.css`; interface lines in `design/fractal-sector/strings.json`. Keep them easy to change: the owner will give feedback.

## G. What the owner asked for most recently (2026-11-10)

1. "Pause, save everything to a repo and memory… give me a summary… in a Md file" → this file.
2. "Work solely on the image… being fully fixed and beautifully rendered, and then stop until further notice." The image: the completed original in the middle; outer rings in colours that match the original, so it looks like one image zoomed out; the eight stages named once; tactics spaced evenly around every ring; "this will be the entire series logo". Reference images the owner attached are described in `design/fractal2/art/README.md`.

## H. Value-and-impact assessment (2026-11-10, after the logo)

The owner asked for analysis only, before any writing: what the original Fractal can do, what Fractal² can do, missed opportunities, how the spiritual lens compares to the traditions, and a conclusion on value and impact, delivered as a PDF. "From THAT perspective we will rewrite the intro one last time."

- **Report:** `library/fractal2/review/Fractal2-Value-and-Impact.pdf` (25 pages). Source: `design/fractal2/reports/value-and-impact.html`; render with `node design/fractal2/reports/render_pdf.mjs <in.html> <out.pdf> "<footer title>"`.
- **The owner's message, word for word:** `content/fractal2/owner-source/G-owner-message-2026-11-10-value-and-impact-brief.md` (includes the pasted audit of draft 4 and other AI material; the owner said some of the audit was wrong).
- **Not done, on purpose:** the intro has NOT been rewritten. The next step is the owner's reaction to the report, then one last rewrite of `content/fractal2/intro-final.md` from section 11 of the report ("the ground the final intro should stand on").
- **Key conclusions to carry into the rewrite:** the original's invention is a transfer of a literacy people already have; a list of tactics explains the past, a sequence predicts the future; "not their names, their methods" has a tested parallel in security practice (kill chain, ATT&CK); the false-positive check and safety apparatus are the most valuable quiet parts; say "documented across", never "proved"; do not claim immunity or that a map ends the cycle; tradition line should read "every tradition has a word for the covering and a word for what is under it" (maya belongs to the Hindu line, avidya and Mara to the Buddhist; pair fana with baqa).

## I. Later on 2026-11-10: images, and the plan to read the whole library

- **Series logo redone as asked** (`design/fractal2/logo.py`): all lettering in the bold cut, and each ring's letters enlarged until its rows are full. Letter height by ring, at 4096 px: Idealize 36, Hook 33, Devalue 33, Confuse 34, Isolate 31, Extract 27, Discard 49, Replace 56 (it was 27 everywhere). Files: `library/fractal2/review/fractal2-logo-4096.jpg`, `-2048.jpg`, `fractal2-emblem-2048.png`; `design/fractal2/art/fractal2-logo.svg`, `-1600.webp`, `fractal2-logo.json`.
- **The original Fractal image, new (second version, after the owner asked for fuller rings):** eight rings, each stage named once at the top, the 30 techniques in bold capitals with equal gaps, spelled from `library/fractal/the-pattern.html`. Each ring's letters are as large as its circle allows and each ring is as tall as its letters need; the two outer rings, which hold two names each, have larger and wider-spaced letters. Lettering covers 81 to 83% of six rings, 69% of Hook, 52% of Discard and Replace. Same colours and core as the logo so one can open into the other. Files: `library/fractal2/review/fractal-original-4096.jpg`, `-2048.jpg` (centre reads "The Fractal") and `fractal-original-fractal2-centre-4096.jpg` (centre reads "Fractal²"); `design/fractal2/art/fractal-original.svg`, `fractal-original-f2.svg`, `fractal-original-1600.webp`.
- Neither image is on a page yet (C1 still open).
- **Report corrected:** its "What I read" line now says the sector chapters were read by structure and sample, not all in full, and its limits now note the 26-versus-30 sector count.
- **Finding:** the published Fractal holds 26 sector chapters. Technology, Dating, Surveillance and Child Welfare are on the thirty-sector list (`content/fractal2/sectors.json`) but have no page in `library/fractal/`. The public number 2,700 assumes thirty.
- **Plan to read everything and extend the report:** `content/fractal2/work-packets/05-library-review.md`. New conversation, same repository. Not started.


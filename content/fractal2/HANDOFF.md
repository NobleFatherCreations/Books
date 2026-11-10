# Fractal² — hand-off (start here in a new chat)

Repo: NobleFatherCreations/Books · working branch **`claude/peaceful-planck-k0df08`** (started identical to `claude/great-keller-jkjz8c`) · updated 2026-11-10.
**Nothing in this project is deployed.** The old prototype at `fractal-entertainment.netlify.app` is untouched.

**Fastest way in: read `content/fractal2/STATUS.md` (2026-11-10). It lists what is done, nearly done and not done.**

## Read in this order

1. This file.
2. `content/fractal2/owner-source/E-…` and `F-owner-answers-2026-11-09-build-session.md` (the owner's own words; they win every conflict).
3. `content/fractal2/DECISIONS.md`, `ARCHITECTURE.md`, `NAV-SPEC.md`, `TAG-POLICY.md`, `RUBRICS.md`.
4. `CLAUDE.md` (house rules).

## State of the build

| Piece | State | Where |
|---|---|---|
| Intro text | Revised draft (11 parts, about 4,700 words). Part VI is locked to the owner's exact account by a test. Awaiting the independent writing review | `content/fractal2/intro-final.md`, `owner-account.txt` |
| Intro page | Built: 20 figures from one field of points, phone and desktop, light and dark, reduced-motion and no-JS fallbacks, narration player. The zoom figure starts on The Fractal's own artwork and draws back to show 335 tactic names in rings around it (owner request) | `design/fractal2/` → `library/fractal2/site/fractal2.html` |
| Intro checks | `node design/fractal2/verify_intro.mjs`: 31 of 31 passed before the zoom change; re-run after it (see session end) | |
| Narration | Script generated from the page text (about 42 minutes, 12 takes); recording guide; sync tool (self-tested); silent placeholder track | `narration-script.md`, `RECORDING-GUIDE.md`, `design/fractal2/sync_audio.py` |
| Sector site (ENT) | 518 pages. Home with six doors and a live mini-map, the ten, all patterns (filter, sort, narrow), 335 tactic pages, 8 stage chapters, 10 families, 153 patterns with three reading modes and a sequence stepper, "What are you noticing?" (private), three reader paths, the living map (SVG; pointer, lists, keyboard), method, take-it-with-you, A to Z, search, sector switcher | `design/fractal-sector/` → `library/fractal2/site/fractal2/entertainment/` |
| Sector checks | `design/fractal-sector/run.sh ent`: 27 checks (the original 16 plus 11). Last full run 26 of 27, the one miss being social cards wiped by a rebuild (fixed); re-run to confirm | |
| Tag resolution | Tool, policy and ledger in place. 1,186 of 1,370 items decided (866 by rule, 320 by the model, 29 escalations decided by the director). 184 still open (66 research, 118 sector accuracy): a research worker is on them. Director's review of rewordings recorded in `director-decisions.json`; **apply with `python3 design/fractal-sector/resolve.py ent decisions` once the worker has stopped writing the ledger**, then `check --final`, `summary`, rebuild | `content/fractal/ent/resolution/` |
| Review material | Zoom-out still, sector screenshots (packet 01), phone scroll recording made before the zoom change (re-record) | `library/fractal2/review/`, `design/fractal2/record.mjs` |
| Docs | DECISIONS, ARCHITECTURE, NAV-SPEC, DESIGN-SPEC, TAG-POLICY, RUBRICS, work packets 01, 03, 04 | `content/fractal2/` |
| Not done yet | Independent review (packet 04) and rubric scores; fresh recordings; the owner report and the "next" list; ENT PDFs (one found in the owner's Drive: `ENT_combo_book.pdf`, 39 MB; not in the repo; labels inside not checked) | |

## How to run things

```
python3 design/fractal2/build_intro.py && node design/fractal2/verify_intro.mjs     # intro
npm i --no-save axe-core && design/fractal-sector/run.sh ent                          # sector site (import, derive, build, cards, verify)
python3 design/fractal-sector/resolve.py ent classify|check|summary                   # tag resolution
python3 design/fractal2/serve.py 8802    # then open http://127.0.0.1:8802/fractal2
```

## Rules learned (binding, on top of CLAUDE.md)

1. "Prototype" means private. Only deploy what the owner names in the current conversation.
2. Never edit the owner's scripts or the author's source files; never change wording inside published books; never touch the homepage without asking.
3. The owner's account in the intro (Part VI) is exactly what the owner wrote. Add nothing.
4. One background worker at a time. On a usage-limit error, stop dispatching, save, and carry on directly.
5. Commit and push after every meaningful step: sessions can be cut off.
6. The owner said (2026-11-10): no need to stop for approval mid-build as long as the script and the design stay easy to adjust. Keep them adjustable: text lives in `intro-final.md`, design values in `tokens.css`.

## Open questions for the owner (ask in one batch, plain language)

- The name line: *Fractal²* — "The closer you look, the more there is." (D2)
- Stage 6 shown as "Extract · Control" with one explanatory line. (D6)
- Shared same-site files for fonts, audio and search data. (D9)
- A private preview link (unlisted, noindex, optional password) so the scroll experience can be felt on the owner's own phone; today the review is screenshots and a screen recording.
- Tag resolution: approve the high-risk changes once the model step is done.
- Whether to redirect the public prototype's addresses to `/fractal2` when the new site goes live.

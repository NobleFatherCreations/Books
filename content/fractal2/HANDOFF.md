# Fractal² — hand-off (start here in a new chat)

Repo: NobleFatherCreations/Books · working branch **`claude/peaceful-planck-k0df08`** (started identical to `claude/great-keller-jkjz8c`) · updated 2026-11-10.
**Nothing in this project is deployed.** The old prototype at `fractal-entertainment.netlify.app` is untouched.

## Read in this order

1. This file.
2. `content/fractal2/owner-source/E-…` and `F-owner-answers-2026-11-09-build-session.md` (the owner's own words; they win every conflict).
3. `content/fractal2/DECISIONS.md`, `ARCHITECTURE.md`, `NAV-SPEC.md`, `TAG-POLICY.md`, `RUBRICS.md`.
4. `CLAUDE.md` (house rules).

## State of the build

| Piece | State | Where |
|---|---|---|
| Intro text | Full draft v1 written; needs the independent writing review and one revision pass | `content/fractal2/intro-final.md` |
| Intro page | Built: 20 figures, phone and desktop, narration player, reduced-motion and no-JS fallbacks | `design/fractal2/` → `library/fractal2/site/fractal2.html` |
| Intro checks | `node design/fractal2/verify_intro.mjs` (31 checks) | see last run in the session log / rerun |
| Narration | Script generated; recording guide written; sync tool written and self-tested; placeholder is a silent timing track | `content/fractal2/narration-script.md`, `RECORDING-GUIDE.md`, `design/fractal2/sync_audio.py` |
| Sector site (ENT) | Generator v2 built by a worker: 518 pages (home, start, patterns, tactics, 8 stages, 10 families, 153 combos with 3 reading modes, 335 tactic pages, method, take-it-with-you, a-z, search, sector switcher). Worker reported 26/26 checks passing before its usage limit; **re-run `design/fractal-sector/run.sh ent` to confirm** | `design/fractal-sector/`, `library/fractal2/site/fractal2/entertainment/` |
| Packet 02 (notice, 3 reader paths, living map) | Static stubs exist; interactive versions **not yet built** | NAV-SPEC §8–10 |
| Tag resolution | Tool written; mechanical pass done: 866 of 1,370 items resolved by rule; **504 need the model step** (84 research, 141 overstatement, 141 overapplication, 128 sector accuracy, 10 note checks); ledger not yet applied to pages; reader banners not yet changed | `design/fractal-sector/resolve.py`, `content/fractal/ent/resolution/` |
| Docs | DECISIONS, ARCHITECTURE, NAV-SPEC, TAG-POLICY, RUBRICS, work packet 01 | `content/fractal2/` |
| Not started | DESIGN-SPEC.md write-up; rubric scoring by an independent reviewer; `sites.json` registration; screenshots + scroll recording for the owner; the owner report; the "next" list presentation; redirects review; PDFs check (not in repo; look in the owner's Drive) |

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

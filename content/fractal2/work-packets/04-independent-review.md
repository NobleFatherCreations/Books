# Work packet 04 — Independent review against the rubrics

**For:** a reviewer model starting cold. You are an editor and design critic, not a builder. **Change no files** except the one report named below. Do not commit, push or deploy.

## Goal

Score three things against `content/fractal2/RUBRICS.md`, with evidence, and list the fixes that would raise any score below 3 (and the two or three changes that would most raise the whole).

1. **The writing:** `content/fractal2/intro-final.md` (ignore HTML comments; they are build markers). Rubric A.
2. **The experience:** the built intro at `http://127.0.0.1:8802/fractal2`. Rubric B.
3. **The navigation:** the sector site at `http://127.0.0.1:8802/fractal2/entertainment`. Rubric C.

## What to read for context (in this order, and no more than needed)

- `content/fractal2/owner-source/E-owner-messages-this-thread.md` and `F-owner-answers-2026-11-09-build-session.md`: what the owner asked for, in the owner's words. These outrank the rubrics where they differ.
- `content/fractal2/RUBRICS.md`.
- For rubric A7 only: `content/fractal2/owner-account.txt` is the approved wording of Part VI.
- For rubric C: `content/fractal2/NAV-SPEC.md` section 1 (the seven readers).

Do **not** read `DECISIONS.md`, `DESIGN-SPEC.md` or any earlier scores before you have written your own; your value is an uninfluenced view.

## How to look

- Start the preview if it is not running: `python3 design/fractal2/serve.py 8802 &` (stop it when you finish if you started it).
- Use Playwright (pre-installed; `require('playwright')`; never run `playwright install`; launch Chromium with `args: ['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist']`). Take your own screenshots at 390×844 and 1440×900 and **look at them** before scoring. Scroll the intro in steps and capture at least: the title, three figures with step text, the 30→335→30,000 figure, the combination sequence and its breaking, the frequency, the closing door and call to action. Also capture the intro with `reducedMotion: 'reduce'` and once with JavaScript disabled.
- For rubric C1, walk each of the seven readers from the sector home and write down the taps it took.
- On the sector site also open: a pattern in each of its three reading modes (`#quick`, `#sequence`, default), a tactic page, `patterns` with a filter applied, `notice` (tick a few signs), `map` (choose a pattern), `in-it-now`.
- Existing automated checks: `node design/fractal2/verify_intro.mjs` and `node design/fractal-sector/verify.mjs ent`. You may run them (the second takes several minutes) or rely on reading them; either way, judge with your own eyes too.

## What to write

One file: `content/fractal2/reviews/independent-review-1.md`, containing

1. Three score tables (A1–A12, B1–B12, C1–C12): score 0–4 and one or two sentences of evidence each. Quote the line or name the screenshot.
2. Any hard fail from the rubrics, stated first and plainly.
3. **Writing notes:** the five weakest sentences or passages, each with a concrete rewrite; any place the text states a belief as a proven fact; any place it could be read as accusing an identifiable person; anything that reads as stock AI phrasing; whether the combinations section is truly the strongest and most foreboding part, and if not, what is missing. Do not propose changes to Part VI other than reporting a mismatch with `owner-account.txt`.
4. **Experience notes:** anything janky, illegible, overlapping, meaningless or merely decorative, by figure name, phone and desktop separately.
5. **Navigation notes:** dead ends, unclear labels, anything a frightened or hurried reader would misread.
6. The ten fixes you would make first, in order, each tagged writing / experience / navigation and small / medium / large.

Be direct. Praise only what is specifically good. If something is excellent, say why in one line and move on.

## Done when

The report file exists and your final message gives the three average scores, the hard fails (or "none"), and the top ten fixes.

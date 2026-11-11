# DESIGN-NOTES: Fractal² intro v7 (2026-11-11). NOT deployed.

Built by running the project's own process (`.claude/skills/design-director`, `docs/design-catalogue/PROMPT-MASTER.md`) end to end. This file records what each step did and changed, so the system can be judged on evidence. Source: `design/fractal2/redesign/v6/` (`python3 build.py [BASE]`). Text (`content/fractal2/intro-story.md`) and artwork (`design/fractal2/art/*.svg`, drawn by `logo.py`) are unchanged.

## Process record (what actually ran)
| Phase | What was done | Evidence |
|---|---|---|
| 0 Interview | AskUserQuestion round: reader (all of the above), feel (cinematic, awe, complete clarity), device (phone first), motion (rich but safe). Other answers taken from the owner's earlier messages | this file, `OWNER-TASTE.md` |
| 1 Research | 10 reference sites tried at 390 and 1440; 6 read (Apple AirPods Pro, BBC, NASA Eyes, The Pudding, Stripe Press, NASA Webb); 4 blocked or empty (neal.fun x2, Eames office, Scale of the Universe); read `09-award-winners-data.md` (Persepolis, Oryzo, Primland: camera through depth, fixed camera path, continuity from first frame) | `references/shots/scale-zoom-story/`, `references/NOTES.md` |
| 2 Coverage and selection | 56-category `COVERAGE.md`, the obvious answer named and rejected, three directions scored (`DESIGN-CHOICES.md`) | `content/fractal2/design/` |
| 3 Hero comps | Three phone and desktop comps (A Survey Plate, B Title Sequence, C Field Guide); owner chose "cinematic, dramatic, while also easy to read" = A's clarity + B's letterbox opening | `library/fractal2/review/v6/comps-*.jpg` |
| 4 Build | Camera engine kept; chrome rebuilt (see changes) | `design/fractal2/redesign/v6/` |
| 5 Critique loop | 4 rounds: gates every round (5 profiles); impeccable critique (A design review + B detector, isolated); better-accessibility; web-perf; emil-design-eng; apple-design; refactoring-ui; frontend-design; impeccable audit; 3 independent critic passes (fresh agent, screenshots only) | below |
| 6 Hand-off | this file, `PHONE-CHECK.md`, ASSET-REGISTER rows, blind A/B page for the owner | `library/fractal2/review/v6/bakeoff/` |

## What each skill or check changed
- **design-director (selection, F1-F14):** found that my own page chrome was F4/F10 (dark/gold "premium", glow, rings): gold chrome removed; chose Source Serif 4 for reading after a five-face comparison (Fraunces too soft and quirky, Newsreader and Spectral too thin on dark, Plex Sans too cold).
- **impeccable critique:** page was not yet the chosen direction (gold ring highlights, cream button the brightest object, phone art too small in the reveal, letterbox too heavy on phone, text over art on phone). Fixed: ring highlights recoloured, Leave outlined, phone reveal fills the width, phone letterbox 6%, stronger phone scrim; added skip-to-end link; neutral quick-exit page; camera drift through the personal section. Detector: 1 finding (`layout-transition`), judged a false positive (SVG `stroke-width`); the browser overlay could not run (needs puppeteer): not run, not clean.
- **better-accessibility:** tab order, 2 px focus rings, skip links land below the header (`scroll-padding-top`), contrast measured (smallest accent 5.2:1), label-in-name on Leave. Not verified: real screen reader, forced-colors.
- **web-perf:** phone, 4x CPU, slow 4G: FCP 0.43 s, LCP 4.6 s -> 2.7 s (tiny blurred preview, second image deferred, font preload, q70 core image), CLS 0.001, TBT 0, scroll frames median 16.7 ms.
- **emil-design-eng:** letterbox and reticle now animate `transform` only; hover gated to real pointers; press feedback `scale(.97)`; transitions under 300 ms; removed a lagging opacity transition on a scrubbed value.
- **apple-design:** body text in rem (respects text size); `prefers-contrast` and `prefers-reduced-transparency`; same-path enter and exit of the zoom kept; interruptible damped camera confirmed.
- **refactoring-ui:** diagnostic 7/8 -> 8/8: everything moved onto the 8 px grid.
- **frontend-design:** flagged my own tells (all-caps tracked labels, middle-dot strings, monospace data labels, arrow glyphs, a single vermilion accent): all removed, Plex Mono dropped, caption now sentence case ("Figure 1: The Fractal"), the artwork carries all colour.
- **Gates (every round):** 0 FAIL on phone/desktop/reduced. Found two real regressions I introduced (title contrast 2.5-2.7:1 when the scrim faded; "Down through" list 3.6-4.3:1): fixed. Final: 0 FAIL, 0 contrast warnings.
- **Independent critic rounds:** r1 (before direction) continuity 3; r2 continuity 4, legibility 3.5/3; r3 (final chrome) hierarchy 4, type 4, craft 4, distinctiveness 5, space 3, phone 3, text-over-art 2, continuity 3. r3's five fixes were applied (scrim, centred camera in beats, soft letterbox, brighter dots, simpler caption); **not re-scored after them**.

## impeccable audit (technical)
| Dimension | Score | Key finding |
|---|---|---|
| Accessibility | 3 | AA mostly met; screen reader and forced-colors untested |
| Performance | 3 | LCP 2.7 s on the throttled profile; `will-change` left on 5 elements at rest |
| Responsive | 4 | 8 sizes, landscape and tablet layouts, no overflow, 44 px targets |
| Theming | 3 | tokens exist; `rgba(10,15,30,.x)` and `#000` repeated; dark only by design |
| Implementation integrity | 3 | coherent; ambient dots outside the count beat look like data but are decorative (P2: mislabel risk) |
| **Total** | **16/20 (Good)** | |

## Known weak points
- Not tested on a real phone. Safari with a fixed canvas and three large images is the biggest unknown.
- Two screens least sure about: the count beat (quiet, dots over a dimmed diagram) and the phone letterbox beat.
- "The room again" differs from the opening by glow only; meaning needs a line of new copy (owner's call).
- No part navigation on a ~19,000 px page (skip links only).
- Claims (335, 203, 153, 2,700) have no sources on the page; the text is fixed, so this is the owner's call.

## Update (owner idea, same day): clean rings first, then the words fill in
The owner supplied the clean "Fractal², 8 Stages. One Cycle." frame (it is `art/fractal2-emblem.svg`, same ring geometry as the full tactic map). The pull-back now reveals that clean frame ("Figure 2: Fractal², the same eight stages"); a silent beat (150svh, after "The true map has more than three hundred.") then spreads the 335 tactic words outward ring by ring from the centre (radial mask on the words layer, parameter `w`) until the rings are full; the caption then reads "335 tactics, one sector". The slow rotation of the outer map was removed so labels and words stay aligned. Gates: 0 FAIL, 0 contrast warnings after the change. Frames: `library/fractal2/review/v6/words-fill.jpg`.

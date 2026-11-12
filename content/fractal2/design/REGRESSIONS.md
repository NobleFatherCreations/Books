# REGRESSIONS: every fault the owner has reported, and the automated check that now guards it.
Rule: a reported fault is not fixed until a check FAILS on the old behaviour and PASSES on the new. Add a row before writing the fix.

| Date | Owner's words | Root cause | Guard (in `scripts/film-check.mjs` unless noted) |
|---|---|---|---|
| 11-12 | "kicked me back to the beginning... it crashed" | DOM images at 320% under a will-change parent: ~4,000 px layers on a 3x phone | `budget` (no forced layers; canvases no larger than the screen). Device-only risk: decoded image memory |
| 11-12 | "It still crashes before the end" | 1,000+ word spans each with will-change | `budget` |
| 11-12 | "words don't move up as you scroll" / "appearing 40% above the bottom" | captions were positioned by script inside a pinned box | `pace` (caption moves 1:1 with scroll) |
| 11-12 | "speed of words is too high, flying from the bottom" | caption travel was longer than its scroll window (1.6x) | `pace` |
| 11-12 | "words appear twice (myself, my body)" | a sequence value snapped back to 0 and the damped camera replayed it backward | `once` |
| 11-12 | "zooming jumps and isn't smooth" | re-layout every time the browser toolbar moved | `toolbar`, `smooth`, `settle` |
| 11-12 | circles drawn as ovals (owner's screenshots) | canvas sized by CSS percent, buffer by innerHeight | `round` |
| 11-12 | "don't dim the background to black then back to bright" | per-caption dimming | `flicker` |
| 11-12 | "got stuck not being able to scroll back up" (at the old grid ending) | not reproduced; the grid ending was removed | `end` (reach the end, scroll back) |
| 11-12 | "words too dim in the fly-bys" | alpha 0.4-0.7 on small type | NOT automated yet: add a contrast sample for canvas text |
| 11-11 | gates "passed" on a design they hated | gates never pressed Begin: 2 screens of 66 checked | `--click` on gates; film-check fails if the probe is missing |

## Device-only risks (no check here can see them; they go on the owner's four-question phone card)
1. Memory pressure on iOS (reload or crash). 2. Real toolbar behaviour. 3. Frame rate while scrolling. 4. Touch scrolling feel and Play.

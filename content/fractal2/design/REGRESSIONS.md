# REGRESSIONS: every fault the owner has reported, and the automated check that now guards it.
See also `FAILURE-LOG.md` for failures no check can catch (not reading what was sent, answering a different question).
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

## Film (clock-driven, 2026-11-16). Guards live in `scripts/film2-check.mjs`.
| Date | Source | Finding | Guard |
|---|---|---|---|
| 11-16 | critic round 1 | Section 1 was one picture for 60 s; captions small | captions enlarged; light wanders; not automatable (critic re-score) |
| 11-16 | critic round 1 | Entry footer and Play button sat on bright ring words | dark well widened; footer on its own band; `caption contrast` covers film captions only: entry contrast is by eye |
| 11-16 | critic round 1 | Bloom burned the labels it announced | ring front and sweep light cut ~55%; by eye |
| 11-16 | critic round 1 | Colour fringing 3-4 px in the launch | capped at 0.0055 of the frame |
| 11-16 | critic round 1 | Desktop was a phone layout centred | wide screens: picture left, words right |
| 11-16 | own check | Begin click was swallowed by the stage tap handler (film paused at once) | `begin starts the film` |
| 11-16 | own check | Screenshot taken before the GPU frame was presented | gate waits two animation frames |
All earlier scroll-era rows that still apply are covered by: `round picture`, `layer budget`, `zero layout shift`, `same time gives the same frame` (nothing twice, no jumps), `caption time on screen`, `caption contrast` (the previously unguarded "too dim" fault), `no banding`.
| 11-16 | own check of preview 01 | Outgoing caption still fading while the next arrived on top of it ("I looked for a single sector" under "I am still looking") | `one caption at a time` |
| 11-16 | critic, sections 3-11 | Desktop window/sun: the light was cut off by the dark pool behind the caption column | the light now spreads under the words; the finish pass caps highlights there (soft knee, 0.34) instead of the DOM pool. Guards: `window light reaches the caption column (no cut)` (gutter ratio was 0.01-0.07, now 0.19+) and `caption contrast` |
| 11-16 | critic, sections 3-11 | Window block labels washed out by the bloom | labels cream, larger (12 px desktop), and the blocks hold the bloom and rays off their faces (scene alpha mask). Guard: `GPU label contrast` (with/without engine text, from pixels) |
| 11-16 | critic, sections 3-11 | Blocks read as flat rectangles | thirty slabs with their own size, angle, soft edge, grain and rim light; they lift, grow and blur as they leave. By eye (frames) |
| 11-16 | critic, milestone 1 | Section 1: about 90 s of one light | the light walks one loop lap after lap through one point; stops at "It must be me"; one lap the other way at "I turned the question around"; every lap lights at "What if it isn't me?". By eye; `same time gives the same frame` covers the closed-form path |
| 11-16 | critic, sections 3-11 | Section 11 chain: separate rings, a flat flower under the most personal lines | ten interlocking links (face-on and edge-on in turn), tightening to a collar that breathes, one breaking open. By eye |
| 11-16 | own check of frames | Phone marker labels "THE DAWN" and "THE LIFTING OF THE VEILS" were pushed back over their own markers (no room at the screen edge) | label moves above (or below) its marker when it does not fit beside it. Guard: `GPU labels: 12 px or more, on screen, not overlapping` (markers count as boxes) |
| 11-16 | own check | Window block labels on phone measured 8.9 px | blocks a little wider, label floor 9.5 px. Guard: same label check (phone block labels are texture and have a 9 px floor; every other label 12 px) |
| 11-16 | blueprint item | Refraction at the glass was not built | the mirror line in table 4 is a glass lens (refraction per channel on full and reduced tiers, single index on low, a drawn lens line in the 2D fallback). Guards: `glass refracts inside the lens only` (with/without, nothing changes outside the lens), `tiers show the same picture at 412.6 s` |

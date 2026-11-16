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
| 11-16 | critic round 3, section 11 | 1030-1119 s: about 90 s of the ring with one orbiting highlight, no caption at 1105 and 1119, and the end button never appeared by seek (it only showed when the clock ran out while playing) | "I am giving it away" lights the thirty rooms one by one and they stay lit; at "It started with a question" every room is lit and the whole map turns slowly; the camera steps in on the last line (phone: the map drops to fill the portrait frame). The last line now stays to the end of the film and "Enter the map" arrives under it 3.4 s later, from the clock (`shots.endAt`), so seek and playback agree. Guards: `"Enter the map" is there at the end (by seek), under the last line`, `playing to the end shows "Enter the map"`, `"Enter the map" opens the hub` |
| 11-16 | critic round 3, ~400/470 s | Caption words fading in over bright ring lettering before the dark ground behind them had arrived (frames 470.0 vs 471.5 s: unreadable at the first instant, readable 1.5 s later; the critic's still was the first instant). The faded original word in table 3 (alpha 0.55) sat over the ring | the dark ground now arrives 0.45 s before the first word and leaves with the last; table 3 keeps the original at 0.86. Guards: `the dark ground is in place before any word shows` (every caption at +0.02, +0.12, +0.25 s); GPU label contrast now counts text from alpha 0.35 up (was 0.6) |
| 11-16 | critic round 3, 610-695 s desktop | "THE LIFTING OF THE VEILS" and "THOU ART THAT" ran into the caption column | marker labels are limited to the picture side of the caption column (`F.COL`); a label with no room beside its marker sits above or below it. Guard: GPU label check fails any label inside the caption's place (desktop: right of the column edge; phone: overlapping the caption box) |
| 11-16 | critic round 3, ~500 s | Table 6 words sat over the ring on phone and centred on the map on desktop with the right side empty | the words take the caption's place: the caption column on desktop, under the ring on phone. Guard: same label check (frames added at +4 s and +10 s into table 6) |
| 11-16 | critic round 3, ~830 s | Combination name ("The Trauma Bond Engine") collided with the map's top ring words | the map steps back and down while the names show. Guard: `GPU labels ... clear of the caption and the map rim` (name box must end above the map's outer words) |
| 11-16 | critic round 3, phone | Portrait frames 195, 330, 756, 930, 1105 s used the middle third only; window block labels 9.5 px | the ring of thirty reaches the screen edges (ZF 0.84 -> 0.97); the chain is 1.85x larger; the window is three blocks across and ten high in portrait; the ending map fills the frame. Block labels 12 px or more; the 9 px phone exception is removed from the label check |
| 11-16 | critic round 3, section 1 | The star read as a stock lens flare on black | three layers of stars at different depths come in after the first lap and slide against the walking light (the camera leans after it), so the laps happen in a space. By eye; `same time gives the same frame` and the tier check cover it |
| 11-16 | critic round 3, hub | 28 identical "IN PRODUCTION" pills, "TECHNIQUE" on every pair card, "12 OF 30" kicker; an open pair card made its row ragged; the hub did not feel like the film; on phones a list row did not update the card | one status line for the group; pair cards turn over in place (technique and inversion share one cell, so the card height never changes); kicker dropped; film grain and one gold glow; each list row name is a button that updates the card (and brings it into view). By the hub gate (`scripts/design-gates.mjs`) and the hub stills |

# Fractal² redesign: proof-of-concept record (vertical slice, Direction A "The Survey")

Built and measured 2026-11-10/11. **Not deployed.** Files: `design/fractal2/redesign/` (`build.py`, `template.html`, generated `index.html`, `fonts/`); review images and the openable zip in `library/fractal2/review/v2/`. Rebuild: `python3 design/fractal2/redesign/build.py`; run the gates: serve the folder (`python3 -m http.server 8810` inside it) then `node scripts/design-gates.mjs http://127.0.0.1:8810/index.html <outdir>`.

## 1. What exists
Title plate (emblem as a survey instrument, Fraunces wordmark, one action) · Part I and Part II reading screens (the owner's exact text) · **Plate 1**: the eight-stage cycle (the stage rings light in order, one at a time) · **Plate 2**: the same ring at three scales, scroll-scrubbed zoom · "door" screen (30 sectors, one mapped in full, linking to the live site) · light and dark themes, Leave button and Esc-twice, no-JavaScript and reduced-motion versions. Every ring, tick and label is generated from the data (8 stages, 30 techniques) so nothing can be misspelled. Not in the slice: the other plates, Part VI, narration, the sector site, a real-iPhone test.

## 2. What changed structurally (the causes of the original failure)
| Original problem | Fix in the slice | Evidence |
|---|---|---|
| Text drawn over the figure; "Idealize" label over a paragraph | Stage and text never share pixels: figure region and caption region are separate grid rows (phone) or columns (desktop) | gates: 0 figure/text and 0 text/text overlaps on 5 profiles (old build: FAIL) |
| Body text 2.7–3.1:1 on rendered pixels | Text sits only on flat paper/ink grounds | gates: 0 contrast failures (old: 12 blocks) |
| Dim specks, no focal point | Bands with body, tick scale, hairline guides, crosshair | focal dominance 0.34–0.68 (gate target ≥ 0.28); read by two independent critics |
| Gold-on-black cosmic default; Newsreader + Hanken | Paper/ink and chart-blue-black grounds, one vermilion accent, Fraunces + Plex Mono | critics: "ownable", type 4/5 |
| No title moment | Title plate in plain HTML/SVG, instant | read at full size on phone and desktop |
| Non-deterministic scroll state | Scene is a pure function of scroll position | gates: scroll determinism 0% difference (old: up to 10%) |
| Token sprawl | 1 corner radius, 0 shadows, 2 families, 4 text colours, 9 type sizes | gates token report |

Measured (headless Chromium, software rendering, 4× CPU throttle: relative numbers only): frame time p50 16.7 ms, p95 16.7–16.8 ms, 0 long tasks, full page reached; page 41 KB + 114 KB of subset fonts, no external requests, no JavaScript needed to read the text.

## 3. Process actually followed (honest)
| Phase of the design skill | Done? |
|---|---|
| 0 Interview with the owner | **No.** I worked from the owner's stated words (`content/design/OWNER-TASTE.md`). The owner has not been asked the questions or chosen between directions. |
| 1 Research with real references | Partly: existing reference captures (`references/`), award-winner data, and the old build's gate results |
| 2 Coverage matrix, obvious-answer rejection, three directions | **Partly**: the schematic compared three directions on paper; the 56-row matrix was not formally filled; only Direction A was built |
| 3 Hero comps and owner choice | **No comps for B and C; no owner choice** |
| 4 Build | Yes (vertical slice) |
| 5 Critique loop | Yes: 7 build rounds with gates; **2 independent critic reviews** (fresh agent, screenshots only) |
| 6 Hand-off | Prototype zip + evidence; no private preview, no real-phone test yet |

## 4. Independent critic scores (1–5 vs real reference screenshots)
| Measure | Review 1 (round 5 build) | Review 2 (final build) |
|---|---|---|
| Hierarchy | 3 | 3 |
| Type | 3 | **4** |
| Space | 2 | 3 |
| Craft | 3 | 3 |
| Distinctiveness | 2 | **4** |
| Feeling | 3 | 3 |
| Restraint | 2 | 3 |
| Accessibility as visible | 4 | 3 (critic wants Leave filled; now done) |
| Verdict | "partly award-level" | "partly award-level" |

The benchmark target in the acceptance criteria was ≥ 4 on every measure. **It is not met.** Both critics name the same missing piece: **the zoom does not yet make one scale visibly turn into the next** ("three static diagrams in a row").

## 5. Defects found and how each was caught (this is the proof-of-concept for the system)
1. **Gates found real problems in the live build** (overlap, 2.7:1 contrast, non-deterministic scroll, heavy under throttle) that the earlier 31/31 checks never measured.
2. **A human read caught a defect the gates missed**: the zoom label garbled by passing rings. The gate was extended (labels inside figures vs the figure's own shapes), proven to FAIL on the broken page, then the page was fixed and the gate passed.
3. **Calibrating the gates on a real book (The Silence) removed false alarms**: element-box overlaps (now text line boxes), anti-aliased pixels counted as background, content scrolling under an opaque bar.
4. **A late false positive (contrast 1.07:1)** traced to smooth scrolling and text hidden under the header; the gate now disables smooth scroll and ignores text under an opaque bar.
5. **The second critic found a regression I introduced** (sector 12 vanished from the list) and a weak safety control; both fixed.

## 6. What it does and does not prove
**Proved:** the tooling measures real defects, drives specific fixes, and prevents the original failure classes (collision, low contrast, specks, default look); a measurably cleaner, more distinctive design can be produced from the system in one session.
**Not proved:** that this is award-level (critics say partly; the zoom, the title ring's full-colour cover, the empty band between ring and caption, and the unbuilt plates remain); that the owner prefers it (no choice made); that it works on a real iPhone; that the full 20-figure intro and the 518-page site can be rebuilt to this standard.

## 7. Remaining work to reach the stated bar (priority order)
1. **A real zoom** (the signature): the inner ring visibly shrinks into one segment of the next, with a scale label beside each ring; no bullseye.
2. **Colour restraint at the cover**: ink-only hairline emblem on the title, colour arrives on Plate 1.
3. **Dock the caption** nearer the ring on phones; remove the empty band.
4. **Build the remaining plates** (origin, chain, gates, sequence/break, descent, atlas) in the same grammar; the eleven marginal figures as small inline SVG.
5. **The sector site** (ring map home, pattern plates) in the same system.
6. **Owner steps**: answer the interview, choose among three comps, run `PHONE-CHECK.md` on a real iPhone with a private preview, run the blind comparison against the live version.

# Fractal² — design spec (v1, 2026-11-10)

One design language for the intro and every sector site: **"Deep field."** Source of truth for values: `design/fractal2/tokens.css`. Change a value there and both builds follow.

## 1. The idea

**Every point of light is one thing that was mapped.** The intro is a single field of points. 2,700 of them are the examples of *The Fractal*. They grow to 1,005 for one sector and to more than 30,000 for thirty. Every figure on the page is the same points re-formed, so no figure is decoration. Point zero is **you**: the page opens on that one light and returns to it.

Gold means **the original**: the signal, the thing that is yours, the thing you can act on. Stage colours run from warm to cold, because the cycle cools. Nothing else is coloured.

## 2. Tokens

| Group | Dark (default) | Light |
|---|---|---|
| Ground | `--bg #0B0C0F`, `--bg-1 #111319`, `--bg-2 #191C24` | `#F5F0E6`, `#FBF8F2`, `#ECE5D7` |
| Lines | `--line #2B2F3A`, `--line-2 #3A3F4D` | `#D6CDBD`, `#BDB29F` |
| Ink | `--ink #EEE9DE`, `--ink-2 #B9B4A8`, `--ink-3 #8D897F` | `#16171B`, `#45443F`, `#66645D` |
| Accent (one) | `--gold #E9B949`, `--gold-2 #F4D58A`, `--on-gold #0B0C0F` | `#8A5E00`, `#6E4B00`, `#FFFDF8` |
| Function | `--warn #F2906F` (safety notes only) | `#A53A1E` |
| Stages 1–8 | `#F2C14E #F09A3E #E8683F #D9486A #B061B4 #7B83E0 #58A3D6 #8FB3C2` | darker set, same order |

**Type.** Two families, self-hosted: **Newsreader** (serif, optical sizes) for every word that is read; **Hanken Grotesk** (sans) for interface, labels and numbers. Scale: display `clamp(4rem, 1rem + 14vw, 8.5rem)` on the intro title; h1 `clamp(2.25rem, …, 4.25rem)`; h2 to 2.5rem; body 19px at 1.6; interface 15px; kickers 11px, tracked .16em, capitals. Measure about 38rem (62 to 68 characters).

**Space.** 8px grid: `--1` 8 · `--2` 16 · `--3` 24 · `--4` 32 · `--6` 48 · `--8` 64 · `--12` 96 · `--16` 128. Radius 10 and 16. Hairlines, not shadows.

**Motion.** `--ease: cubic-bezier(.16,1,.3,1)`; `--d1 .2s` (hover, press), `--d2 .32s` (panels, steps), `--d3 .7s` (reveals). On the stage, nothing is timed: every point chases a target set by the scroll position (critically damped, rate 5.2/s with ±40% variation per point for an organic stagger). Reverse the scroll and the figure reverses. Ambient drift is under 1% of the stage and stops under reduced motion.

## 3. Intro layout

- **Wide screens (≥ 960px, landscape):** text in a left column (33rem); the stage centred at 71% of the width. During a figure that has no step text, the stage eases toward the centre and enlarges.
- **Narrow screens:** the stage sits behind the text, centred at 36% of the height, at 20% brightness during prose and full brightness during figures. Step text rides in a card held at 62% of the height; only the current card is visible.
- **Top bar:** mark, Listen, Contents, Leave; a 1px gold reading-progress line.
- **Reduced motion:** every figure is a still at its final state with its description shown in words; steps are an ordinary list. **No JavaScript or no WebGL:** full text, descriptions in place of figures (Canvas 2D fallback when only WebGL is missing).

## 4. Storyboards (20 figures)

Scroll progress through a figure is `p` from 0 to 1. "Accept" is what must be true to ship.

| # | Scene | What the points do | Labels | Accept |
|---|---|---|---|---|
| 0 | `signal` (title) | One gold point, breathing | none | The first thing seen is one light |
| – | `room` | 260 dim points drifting; you slightly off centre | none | Reads as a quiet room, not a starfield effect |
| 1 | `cycle` · 8 steps | 2,700 points on a ring in eight arcs sized 2-2-4-5-6-7-2-2 (the techniques per stage); arcs light in order with the steps | stage name in the centre, "n of 8" | Step k lights arc k exactly; reversing un-lights it |
| 2 | `levels` · 4 steps | Three rings (one life, institution, civilization) light inward to outward; then 15% of the points form the same three rings, tiny and gold, inside the centre | ring names; "the pattern, inside the person" | The nesting is visible without reading |
| 3 | `count` · hold | Points pour from a cloud into 30 columns × 90 (two rows of 15 on a phone) | a counter rising to 2,700 | Counter and columns arrive together |
| 4 | `gates` · hold (long) | 30 arches around you; one turns gold at a time | sector name and "your relationship with …", "07 / 30" | All thirty names can be read at normal scroll speed |
| 5 | `origin` · 3 steps + tail | Three circles light in turn, then overlap; a small eight-colour ring appears in the overlap on its own | the three conditions; "it installs itself" | Nothing "places" the ring: it forms from points already there |
| 6 | `mirror` · 3 steps | The large ring draws in until it circles you | none | Ends with the ring inside the area of one fingertip |
| 7 | `chain` · hold | Four linked ovals light in order; the last is gold and holds you | great-grandmother … you | Links visibly interlock; the last is unmistakably different |
| 8 | `zoom` · hold (long) | The published artwork of *The Fractal* fills the view (8 stages, 30 techniques). It draws back to a small disc at the centre; around it the 335 tactics of one sector appear as new rings of names, stage by stage, at one letter size, each stage titled as on the original. Then the whole disc draws back and becomes one of thirty tiles: 30,150 points | "30" → "335" → "30,000+" | The original stays visible inside the larger map, so the scale is read in one image; names are legible at 2× on desktop; no dropped frames |
| 9 | `altitudes` · 3 steps | One tactic as three gold points, one above the other on the three rings | the three levels | Each step lights one point |
| 10 | `names` · steps | The 30,150-point field, grey, turns gold a few at a time | none | Ends fully gold on "a thing with a name can be refused" |
| – | `witness`, `threshold` | Everything gone but you | none | Part VI is read against darkness |
| 11 | `roster` · hold | 153 short chains appear, one bead per tactic, coloured by its real stage | combination names rising one by one | Every bead count and colour comes from the data |
| 12 | `multiply` · 6 steps | You inside a ring of five open doors; each step closes one; then the ring tightens and warms | your guard / way out / worth / certainty / witnesses, struck through as they close | Door k closes on step k |
| 13 | `sequence` · 6 steps | Six links join in the order of The Debt Prison's tactics; a mass around you doubles with each link | 1 to 6 | The mass grows faster each step |
| 14 | `break` · hold | The fourth link turns gold and opens; the mass drifts away; the chain falls slack; you brighten | "break one" | One link, not all, is what changes |
| 15 | `inversion` · 8 steps | Eight bars in stage colours turn gold in order | each stage name turns into its original | Name and colour change together |
| 16 | `frequency` · hold | You, sending slow rings outward | none | Calm, continuous, never flashing |
| 17 | `descent` · 5 steps | Five strata pass upward as you go down; you arrive from below | the sectors, the techniques, the mirror, the body, the chain | Direction of travel is unmistakably down |
| – | `ground` | You, alone, steady | none | The same light as the title |
| 18 | `horizon` · hold | Lights appear outward from you until the field is full | none | Spreads from the centre, one person at a time |
| 19 | `atlas` · hold | Thirty tiles; Entertainment lit in full, twenty-nine outlined | sector names; "1 of 30 mapped at full resolution" | The unbuilt sectors read as waiting, not missing |
| 20 | `door`, `enter` | A doorway drawn in points opens; light falls through it | none | The call to action sits in that light |

## 5. Sector site components

Top bar (mark, sector switcher, search, Leave) · breadcrumbs · numbered cards (the ten, the stages, the families) · score bars (five segments, number as text) · tactic chain (stage dot + number, linked) · safety note (warn rule, wash, icon, always first) · reading-mode control (three-part segmented, sticks under the bar on a phone) · sequence stepper · credibility chips (outlined, sans) · filter sheet · search dialog · the living map (SVG: ring of tactics in two lanes, families clustered inside, gold path with numbered stops) · "what are you noticing" (chips, checklist in the author's words, results with the caveat always above them).

Rules: gold only where the reader can act; stage colour only as an 8px dot or 2px rule and always beside the stage number or name; no drop shadows; touch targets 44px; one accent.

## 6. Performance budget

Engine work per frame under 4× CPU throttle: average under 6 ms, worst under 34 ms (measured: 2.2 ms and 21.7 ms). Heavy formations are built ahead of time in idle slices. Device pixel ratio capped at 2. One draw call. No layout reads inside the frame except cached positions.

## 7. How to change things

- A word on the intro: `content/fractal2/intro-final.md`, then `python3 design/fractal2/build_intro.py`.
- Where a figure sits or how long it holds: the `<!--fig:NAME hold=N | …-->` line in the same file.
- A colour, a size, a duration: `design/fractal2/tokens.css`.
- A figure's shape: its `S.<scene>` block in `design/fractal2/intro.js`.
- An interface line on the sector site: `design/fractal-sector/strings.json`.

# Fractal² redesign — schematic (design only; nothing is built or deployed)

Written 2026-11-10 by applying `docs/design-catalogue/` (rules in `07`, process in `PROMPT-MASTER.md`) to the intro (`/fractal2`) and the Entertainment & Music site (`/fractal2/entertainment`). **This is a hypothesis to be tested by comps, not a claim of quality.** Section 8 separates evidence from hypothesis.

---

## 1. Diagnosis (what is wrong, from evidence, not taste)

Evidence: the owner's iPhone screenshots; `design-gates.mjs` run on the live intro (2026-11-10); `references/` captures; `DESIGN-SPEC.md`.

| # | Finding | Evidence | Failure mode (07) |
|---|---|---|---|
| D1 | Text drawn over the figure canvas; the ring label "Idealize" prints over a paragraph | owner screenshots; gates: text-over-text FAIL | F2 collision |
| D2 | Body text measures 2.7–3.1:1 against what is rendered behind it | gates, pixel contrast | F11 readability |
| D3 | The figures are 1–2 px dim points with no mass and no focal point; large empty beige/black areas on phones | owner screenshots | F3 specks, F7 dead space |
| D4 | Dark field + gold glow + serif body is the cosmic-mystical default; light mode is generic beige; Newsreader + Hanken is a default pairing | catalogue anti-cliché list | F4 template, F10 cliché |
| D5 | No signature move: 20 figures use one grammar at one intensity | `DESIGN-SPEC` §4 | F5 flat hierarchy, F8 fatigue |
| D6 | The first screen is "one gold point, breathing" | spec scene `signal` | no title moment (Stripe Press lineage) |
| D7 | Same scroll position looks different after scrolling away and back; scroll pass reached only 16% of the page under CPU throttle (software-rendered headless: treat as relative) | gates | F6 |
| D8 | Never checked on a real iPhone | status file | F12 |
| D9 | The intro states 2,700 examples; the published Fractal has 26 sector chapters (2,340 written) | `STATUS.md` §I | trust |

**What is genuinely strong and must be kept:** every point is a real, countable thing (the "field of 30,150 points" idea is true to the data); one draw call, measured about 2.2 ms average per frame; the owner's account (Part VI) is locked; safety scaffolding (Leave, labels, "patterns not people", composites labelled); the data-generated figures that cannot misspell.

**"The obvious answer" (rejected):** dark cosmic starfield, gold glow, serif text over it, a point-cloud for every figure, a floating pill nav. That is the current build.

---

## 2. Concept, Budget and three directions

**Concept sentence.** *One continuous zoom: the page is a single camera moving from one person's kitchen to a whole civilisation and back down, and each time it lands, the same eight-part shape is already there.*

**Budget (07 §2):** 1 concept · 1 lead style · 1 supporting influence · 1 signature move · 2 type families · 1 UI accent · 1 motion language · at most 3 decorative effects per screen · at least 30% Quiet screens.

**Three genuinely different directions** (built as comps before anything else; the owner picks):

| | A. The Survey (recommended) | B. The Slow Film | C. The Specimen Sheet |
|---|---|---|---|
| Lead style | Cartographic / field-guide atlas (S-36, S-35) | Cinematic essay (S-37) | Scientific plate, white and quiet (S-35, S-44) |
| Supporting | Editorial long-read measure (Aeon lineage) | Serif title cards | Gov-grade plain clarity |
| Signature move | **The Zoom**: the eight-stage ring is one persistent object; scale changes, shape does not; a map **scale ruler** at the left edge | **The match cut**: cut between scenes on the same shape | **The plate flip**: each figure is a numbered plate with a caption |
| Ground | warm paper / chart-blue-black, both designed | near-black, film grain once | white, hairlines |
| Risk | reads as "just a map" if the ring is weak | effect-heavy; dark-default cliché | cold; may feel clinical |
| Why it fits | the brand idea is literally scale-invariant structure | emotional pacing | trauma-safe calm |

**Recommendation: A for the intro, with C's plate captions and quietness in the sector site.** Rejected on purpose: B as lead (reintroduces the dark-cosmic default and costs the most), glassmorphism (reduces contrast), cursor effects (phone-first), kinetic text for body, marquee, glow halos.

---

## 3. Identity system (Direction A, proposed; verify in comps)

| Element | Proposal | Reason / test |
|---|---|---|
| Type | One serif superfamily with optical sizes for display **and** text (candidates: Fraunces, Newsreader; open licence; self-hosted subset) + one mono (IBM Plex Mono, already the library's UI voice) for annotation. **Two families total** | Annotation in mono is the "survey label" voice; test the pair in comps at 390 px |
| Scale | Title 15vw plate; h1 4rem; h2 2.5rem; body 19px/1.6; mono labels 12–13px (never below 12) | gates: ≤ 9 distinct sizes, none under 12 px |
| Ground | Light "bone paper" `#EFEBE1` with ink `#14181F`; dark "chart blue-black" `#0E1420` with chalk `#ECE8DC`; both fully designed, user-switchable, follows OS by default | contrast measured on pixels ≥ 4.5:1 for all body text |
| UI accent (one) | Signal vermilion (light `#C73E24`, dark `#FF6A4A`): only where the reader can act | replaces gold-as-default; semantics kept ("you / act") |
| Data colours | The eight stage hues from the owner's original artwork (unchanged, per the owner's request), used **only** in figures, always beside a stage name or number | the logo/original image already match |
| Marks | Points become **survey marks**: three sizes (dot, tick, cross) with minimum feature size 5–6 px; ring arcs have body (10–18 px dense bands) plus hairline guides and a tick scale | fixes D3; gate: focal dominance ≥ 0.28 |
| Motion | `--ease: cubic-bezier(.16,1,.3,1)`; 180 ms UI, 700 ms scene; spring for press; scene motion scrubbed by scroll with damping; **no** autoplay, marquee, glow, or cursor effects | `prefers-reduced-motion` = designed stills |
| Shape | hairlines, 4 px radius on UI, no shadows | token sprawl gate |

---

## 4. Layout schematic (separates text and figure by construction)

**Rule: text never sits on the stage.** On phones the stage and the text take turns in time; on desktop they take turns in space.

```
PHONE 390x844                         DESKTOP 1440x900
STAGE SCREEN (figure owns it)         ┌───────────────┬──────────────────────┐
┌──────────────────────┐              │ bar (Leave,   │                      │
│ bar 56: mark | Listen│              │ Listen, menu) │                      │
│ ruler│               │              ├───────────────┤   STAGE (sticky,     │
│  │   figure region   │              │ TEXT COLUMN   │   55% width, own     │
│  │   62% height      │              │ 33rem, opaque │   background, full   │
│  │   ◯ ring ◯        │              │ measure 62ch  │   height; the zoom   │
│  │                   │              │               │   ruler on its left) │
├──┴───────────────────┤              │ steps scroll  │                      │
│ CAPTION CARD 28%     │              │ here          │                      │
│ opaque, safe zone    │              │               │                      │
└──────────────────────┘              └───────────────┴──────────────────────┘
READING SCREEN (no figure)            Full-width plates (Zoom peaks) hide the
┌──────────────────────┐              text column; caption is a bottom band.
│ bar                  │
│ text 18px, 36-40ch   │              Reduced motion / no JS: each figure is
│ pure typography      │              a still plate with its caption in words.
└──────────────────────┘
```

Safe-zone contract (tested by the gates): stage region and text region never intersect; the header is opaque or blurred; no heading hides under the bar; `100svh`, safe-area insets, 44 px targets.

---

## 5. The intro: pacing and intensity map

Twenty figures become **nine plates** (full-attention moments built to the highest standard) and **eleven marginal figures** (small inline SVG inside reading screens, no WebGL). This cuts spectacle fatigue while keeping every figure's data and meaning.

| Part | Purpose | Screen type | Figure(s) | Intensity |
|---|---|---|---|---|
| Title | Threshold | Title plate (HTML + inline SVG, instant) | The eight-ring emblem as a survey instrument; wordmark "Fractal²", name, tagline "The closer you look, the more there is."; one vermilion cue "Begin" | **Loud (once)** |
| I The feeling without a name | Recognition | Reading, type only | none (silence is the design) | Quiet |
| II What The Fractal saw | Show the cycle | **Plate 1**: `cycle`, eight arcs light in order; stage cards | `room` (marginal), `cycle` (plate) | Medium |
| III The pattern without a hand | Why no villain is needed | Plate 2: `origin` three circles overlap and the ring forms | `origin` (plate), `levels` preview | Medium |
| IV The mirror and the chain | Inheritance | Plate 3: `chain` four interlocking links, last one different; marginal `mirror` | `mirror`, `chain` | Medium |
| V The closer you look | **The signature** | **Plate 4: The Zoom (peak)**: person to institution to civilisation, the ring recurs; ruler marks scale; then `levels` nesting | `levels`, `zoom` | **Loud** |
| VI Why I can draw this | The owner's account (locked) | Reading, type only, near-black or plain ground | none | Quiet |
| VII The sequence | Combination and order | Plate 5: `multiply`+`sequence`+`break` as one plate (doors close, links join, one link opens) | `roster` (marginal) | Medium-Loud |
| VIII What it was built from | Evidence | Plate 6: `gates` thirty arches; marginal `count`, `names`, `inversion` | `gates` | Medium |
| IX Down | Descent and return | Plate 7: `descent` five strata; the Zoom runs in reverse | `descent` | **Loud** |
| X What this is for | Purpose | Reading; marginal `frequency`, `horizon` | quiet | Quiet |
| XI The door | Handoff | Plate 8: `atlas` (thirty tiles, one lit) then Plate 9: the camera zooms into the lit tile; cross-document view transition to the sector home where the same ring persists | `atlas`, `door` | Medium |

Intensity check: Loud = 3 of 12 stops (Title, V, IX), never two in a row; Quiet = I, VI, X plus every reading screen, comfortably over 30%.

**Narration and audio:** the existing player stays (never autoplays); captions highlight the current sentence; silence by default.

**Truth fix (D9):** the `count` plate shows what exists (26 sector chapters, 2,340 written examples) and labels the remainder as planned, unless the owner supplies the missing four sectors. Owner decision.

---

## 6. The sector site (Entertainment & Music): same identity, different job

| Page | Redesign |
|---|---|
| Home | **The ring map as hero**: the eight-stage ring with the 335 tactic names laid out evenly on its bands (data from `design/fractal2/art/fractal2-logo.json`), tap a stage to open it; six "where are you right now" doors beneath as large, plain, tappable plates; the ten that matter as numbered plates with score bars |
| Pattern page | A **plate**: title plate; a scene inside a labelled composite box; the chain diagram of beads (real stage colours) as the hero figure; three reading modes over the same words; the safety note first, always |
| Tactic page | A specimen card: name, stage number, definition, three levels, "seen in these patterns", link to the Pattern Decoder page |
| Stage chapters | One per stage; the stage's arc of the ring is the page header |
| Navigation | Slim bar (mark, atlas switcher of thirty sectors, search, **Leave**); Esc twice also leaves; breadcrumbs; every page stands alone |
| Reader paths | Three large doors: in it now / worried about someone / before you sign. "In it now" page: calm, short, no motion |
| Method / take it with you | Plain reference pages in Direction C's quiet plate style |
| Quiet default | Follows OS; a **discreet mode** (neutral tab title, no accent colour, no emblem) behind the Leave menu. Owner decision pending (also noted for the books) |
| Continuity from the intro | the ring and ruler persist; same type, ground, accent, motion grammar |

---

## 7. Additions and enhancements

1. Shareable **plate cards** (generated OG images per pattern from data; no personal data).
2. Printable one-page plates ("take it with you") per pattern.
3. "What are you noticing?" selects a **stage on the ring** and walks to the pattern (private, in-page, nothing stored).
4. A **scale ruler** as navigation and as progress (no tracking).
5. Discreet mode and quick exit everywhere; `#/help` route (category of help + a search string, no invented numbers).
6. Reduced-motion and no-JS ladder: WebGL → Canvas 2D → still plates with descriptions → plain text.
7. Asset strategy: all figures generated in code from data (no commissioned art needed); typographic fallback for every plate.
8. Later (not in this build): legal pass, regional crisis resources, translations, independent expert review (no page may claim it).

---

## 8. Audit: how this was steelmanned, and what is and is not established

### 8.1 Failure-mode audit (design against F1–F14 and D1–D9)

| Problem | Mechanism in this design | How it will be checked |
|---|---|---|
| F1 effect soup | Budget; plates only 9; no glow/cursor/marquee | gates: animations at once ≤ 14; hues ≤ 4.5 |
| F2 collision (D1) | Text and stage never share pixels (time on phone, space on desktop) | gates: figure/text and text/text overlap = 0 on 5 profiles |
| F3 specks (D3) | Marks have size classes, bands with body, hairline instrument, focal rule | gates: focal dominance ≥ 0.28; contact sheet read by a human |
| F4/F10 default (D4) | Obvious answer rejected; cartographic concept; type pair tested; accent changed | substitution test on hero; blind comp |
| F5/F8 (D5) | Signature move; intensity map; 9 plates + 11 marginals | contact sheet shows rhythm; scorecard |
| F6 | Every motion has a job (scale, order, recurrence) | explain-test on each plate |
| F7 | Figures own their region; reading screens are type only | gates: dead-space warnings |
| F11 (D2) | Opaque text columns; contrast on rendered pixels | gates ≥ 4.5:1 body |
| F12 (D8) | Private preview + `PHONE-CHECK.md` | owner on a real iPhone |
| D6 | Title plate in HTML, instant, with the emblem | LCP target under 1.5 s on throttled mobile |
| D7 | Scene state is a pure function of scroll position | gates: determinism < 2% difference |
| D9 | Count plate shows what exists | owner decision, then check against data |

### 8.2 Steelman (strongest case for)
1. **It keeps what is true and strong** (data-true points, one draw call, locked testimony) and replaces only what the evidence shows is failing.
2. **It fixes causes structurally.** Collision and contrast are solved by layout, not by tweaking opacity; the gates can verify it mechanically.
3. **One hard idea, executed with restraint.** The top-winner data (`09`) shows recurring wins from a single metaphor structuring a page (Pioneer's seed-to-harvest loop), one signature interaction (Igloo's particle footer), a single object with weight (Oryzo), continuity from the first frame (Persepolis). The Zoom is that idea, native to the brand concept.
4. **Fits the reader.** Reading screens are calm and type-only; spectacle is rationed; Leave and discreet mode are always present; nothing autoplays.
5. **Cheap to build.** The Zoom is a 2D log-scale transform over instanced points, not a 3D camera; no library is required (Option A), so no policy decision blocks it.

### 8.3 Strongest objections and answers
| Objection | Answer |
|---|---|
| Separating stage and text loses the elegance of one integrated field | On desktop they are side by side and stay linked by the ruler; on phones, time-separation is what real-device screenshots show is necessary. Compare in comps. |
| Paper and vermilion is just another style | It is a hypothesis; Direction B and C are built too; the owner chooses by looking. |
| Dense marks may still read as specks | Minimum feature size, banded arcs, hairline guides, and a measured focal-dominance gate; the independent critic is shown only screenshots. |
| A scroll-driven zoom is scroll-jacking | Native scroll position drives the scene; nothing intercepts the wheel or touch; reduced-motion shows stills. |
| Cutting 20 figures to 9 plates disrespects the work | None is deleted: eleven become marginal inline figures; data and meaning remain. |
| Cross-document view transitions may fail on iOS | They are progressive: fallback is a plain fade; tested on the real phone. |
| Heavy frames on weak phones | Existing budget (avg 2.2 ms, worst 21.7 ms measured earlier); gates measure under 4× throttle; points capped; plates pause offscreen. |
| The owner may hate the type | Pair is tested in comps; swap is a token change. |

### 8.4 Evidence vs hypothesis (honest status)

| Established now (evidence) | Not established (hypotheses to test) |
|---|---|
| The current build has collisions, low contrast, non-deterministic scroll (gates) | That The Zoom is memorable and clear |
| The engine meets a frame budget (earlier measurement in `DESIGN-SPEC`) | That paper/vermilion + the chosen type pair feels right for this subject |
| Winners' recurring patterns and the benchmark captures exist | That 9 plates feel less fatiguing than 20 figures |
| The tooling to measure the redesign exists (gates v2, scorecard, blind compare) | That stage/text alternation feels good on a real iPhone |
| Reading-first and care references are captured for comparison | That view transitions work on iOS Safari |

**Nothing here has been built, so nothing here can yet be called successful or best-possible.** "Highest quality" is a claim the process earns, not one this schematic can make.

### 8.5 Acceptance criteria (what "successful and working" means, in advance)
1. `design-gates.mjs`: **0 FAIL** on all five profiles; every WARN explained or fixed; pixel contrast ≥ 4.5:1 for body text; determinism < 2%; no unexplained token sprawl.
2. **Benchmark** (`SCORECARD.md`): ≥ 4/5 on hierarchy, type, space, craft, distinctiveness, feeling, restraint and accessibility against the matching reference sets (reading-first and showcase-story for the intro; care-public-service for safety pages).
3. **Blind judging** (`blind-compare.mjs`): the owner and two others prefer the redesign over the current build on at least 4 of the 5 questions.
4. **Five-second test** with three people on phones: at least two can say what it is ("a map of how manipulation works"), and recall the ring.
5. **Real-device**: `PHONE-CHECK.md` passes on a real iPhone (10 steps, plus screen reader).
6. Reduced-motion and no-JS versions are designed and checked; the Leave control works; no external requests; text and data unchanged (Part VI byte-identical; test in repo).
7. Independent critic's five points addressed; owner says "deploy".

### 8.6 Kill criteria (pre-committed)
- If the owner picks B or C from the comps, rebuild around that direction.
- If frame time or iOS stability fails after two rounds, reduce plates to stills with scroll-linked crossfades (no live field) and keep the identity.
- If three critique rounds leave the same defect, stop and ask the owner with two options.

### 8.7 Build order (when approved)
1. Interview + `OWNER-TASTE.md` read. 2. `COVERAGE.md`, `DESIGN-CHOICES.md`, `REFERENCES.md`. 3. Three comps of the **title plate + one reading screen + one stage screen** (390 and 1440). 4. Owner chooses. 5. Hero in the chosen direction, gates, show owner. 6. Plates in priority order: Title, V (Zoom), II (cycle), XI (door), then the rest. 7. Sector home ring map, pattern plate, tactic card. 8. Critique loop, benchmark, independent critic. 9. Private preview and phone check. 10. Owner says "deploy".

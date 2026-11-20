# Manipulation-chain sector sites: design record (Corporate & Consulting, v1, 2026-11-20)

Build: `python3 design/chains/build.py corp` then `python3 design/chains/verify.py corp`. Output: `library/fractal2/site/fractal2/corporate.html` (landing) and `corporate/` (138 chains, `categories/` 10). Source: the owner's package, verbatim, `content/fractal/_packages/combo_clusters_markdown_v2/CORP/`. Not deployed.

## The brief (owner, 2026-11-20)
Each sector its own site; build Corporate; call combos "manipulation chains"; each chain one scroll from start to finish; left and right to the previous and next chain; a menu to the categories; a landing page with all the setup information; clean UI, a nice font, designed boxes with unique visuals that help inside sections; audit with every skill and server; award-level; steelman and critique every step; justify the final design and say why it could not be better.

## Process actually run
1. design-director skill (New track): OWNER-TASTE read; reference sets (`references/shots/reading-first`, `care-public-service`); award data (`09-award-winners-data.md`) plus a web check of 2026 editorial winners (Long Lead, Webby Best Individual Editorial Feature 2026; Emergence Magazine).
2. Three directions built from the same generator and real text: A (Newsreader + Plex Mono, dark, gold), B (Bricolage Grotesque + Source Serif 4, light, rust), C (dossier: paper sheet on a dark desk). Screenshots at 390 and 1440, light and dark.
3. Critic 1 (independent) scored A/B/C. C cut (paper sheet unreadable on a phone, dark panels on paper). Chosen: D = A's dark chassis and gold + B's type, two families only.
4. Round 2 applied; design gates (`scripts/design-gates.mjs`, five profiles) run; one false positive found (Chrome keeps closed `<details>` content laid out) and made impossible.
5. Full build; verifier written (every author word per section, order, headings, safety note under the title, list numbering, links, outside requests).
6. Critic 2: 13 defects; 12 fixed, 1 rejected (see below). Critic 3: 11 confirmed fixed, 6 new; all 6 fixed. A step-numbering bug (each Corporate step parsed as its own list) was found by reading frames after critic 3, fixed, and turned into a check.
7. axe (WCAG) on chain, landing and category pages, dark and light: 0 violations. Gates: 0 failures on chain (short, long, safety), landing and category pages in all five profiles. The gate's in-figure label test run on all 276 chain figures: 0 crossings.

## Final choices and why
| Choice | Why this and not the alternatives |
|---|---|
| Dark ground, gold accent, light mode on system setting | House rule "preserve the dark theme"; the reader often arrives at night on a phone; continuity with the film and hub. Light mode is a cool off-white, not the cream + serif + terracotta AI default critics flagged in B. |
| Bricolage Grotesque (display, labels) + Source Serif 4 (reading) | Critic 1: B's serif was the most legible text on a phone; A's thin display collapsed at 390 px; two families only (house rule). Mono labels dropped (9 px, illegible). |
| Title set huge and condensed (12.4 vw on phones) | Owner: "big type that uses the screen", "a bold first impression with good lettering". |
| The chain's shape (eight stage rings, steps joined in order; open ring start, gold end) | A signature drawn from real data (stage of each tactic via the standard index), so 138 different shapes; reused at four sizes (title plate, chain section, cards and doors, end cards, desktop margin). Stage names placed on their own ring, clear of every dot and path line (checked on all 276 figures). |
| Safety note directly under the title, as a full-width band with one Leave line | Author's "read first"; critics 2 and 3 both pushed it to be designed and never squeezed. |
| Each box has its own form: cue cards (question as the hero line), escalation as a three-step track, analogies unboxed with a rule, response lines as speech bubbles with Copy, evidence with clips, chain breakers with broken links, the timeline for Where Each Tactic Happened | Owner: "design boxes with unique visuals that help within sections"; critic 1: "everything is a rounded bordered box" is the template tell. |
| The name reveal as one sentence in the author's words, name in gold | The story builds to it; critic 3 found it scattered across three styles. |
| Prev/next in the top bar, at the end (with the next chain's shape), and on the arrow keys; Menu with the chain's sections and all ten categories | The brief's left/right and category menu; one fixed layer while reading. |
| Desktop margin: the chain's shape, the current step lit as you read | Critic 2: the empty right third; critic 3: make the duplicate a reading aid and hide it while a larger shape is on screen. |
| No numbers except chain steps (and the author's own numbered lists) | Plan rule; critic 2 caught category ordinals and "7 of 13", removed. |

## Rejected suggestions and why
- Gold for escalation instead of the warm peach (critic 2): the peach is a semantic safety/risk colour used only on Leave, safety notes and escalation; semantic colour is not a second decorative accent.
- Section numbers in gold (critic 1): numbers mean chain steps only.
- A four-step escalation track (critic 1): the author wrote three transitions; a fourth would invent one.
- Removing THE HOUSE from reading pages (critic 1): house rule; it sits in the bar instead of floating over text.
- Renaming the jump links "Jump to what to do" (critic 1): it would rename the author's headings.

## What could not be done better here, and why
- Real-device check: Chrome on an iPhone with Reduce Motion on cannot be run in this container (only Chromium). Phone card below.
- Typefaces are limited to the open-licence fonts already in `tools/fonts/`; a commissioned or licensed face (the route most Site-of-the-Day winners take) is outside the no-external-request rule and the budget.
- The scores of the last critic round (hierarchy 4, typography 4, space 3, craft 3, distinctiveness 4, feeling 4, restraint 4, phone readability 4, navigation 4) were given before round 4; round 4 fixed every item it named, but no further independent round was run after the step-numbering fix.
- 93 of 858 steps are umbrella patterns (Gaslighting, FOG, DARVO…) that span several stages; they sit at the centre of the shape, dashed, because placing them on one ring would be untrue.
- Interface wording (landing page, labels, the Leave line) is mine and needs the owner's approval; the author's text is untouched (verified word by word).

## Phone card (owner, real iPhone, Chrome)
1. Does the first screen of a chain show the title, and on chains with a safety note, the start of the note?
2. Do the left and right arrows and the Menu work with one thumb, and does Leave work at once?
3. With Reduce Motion on, does anything move that should not?
4. Is the body text comfortable to read for a full chain (about 20 minutes)?

## Round 5 (2026-11-20): every design skill, impeccable critique
Skills run: design-director, impeccable (critique with two isolated assessments: A design review, B detector + browser overlay; craft-floor, typeset, animate playbooks), frontend-design, emil-design-eng, apple-design, find-animation-opportunities and review-animations standards, better-accessibility (motion and zoom). Servers: playwright (all screenshots and checks), sequential reasoning inline. The Figma, Canva and Adobe connectors were not used: the site must be self-contained and every visual is drawn in code from the data, so an exported design asset would have broken the no-outside-request rule or duplicated the figures.
- Motion thesis: "the chain forms as you read". The Verbal Breakdown figure stays in view while its steps scroll past; its path draws to the step being read, the steps behind light up, a gold thread runs down the step list, the desktop margin names the step. Scroll-driven only, so Reduce Motion keeps it (instant); nothing plays on its own. Supporting motion: press feedback (scale .97), the menu sheet slides in (320 ms, ease-out) and out faster (200 ms), view transitions carry the title and shape from chain to chain (off under Reduce Motion), the reveal's gold underline follows the scroll.
- Craft floor applied: eyebrow labels removed everywhere; sentence-case labels; no middle-dot meta strings; display capped at 6rem; Unicode icon stand-ins replaced with drawn SVG; the landing's card grids replaced by composed lists; category grid replaced by editorial rows.
- Typography: curly quotes and apostrophes (glyphs only, verified word for word), old-style numerals in prose and tabular lining numerals in figures, hanging punctuation.
- One accent: the stage rainbow on step circles removed (stages named in words; gold marks the current step); warm peach stays semantic (safety, Leave, escalation).
- Rhythm: the practical sections (Observable Indicators to Safer Response Language) share a full-width tonal band; rail and menu space the story, the analysis and the practical part apart, with no invented labels.
- Safety note: first sentence set large, the Leave line directly under it.
- Landing hero: all 138 chain paths drawn over the eight rings, one traced in gold.
- Phone: the bar wraps instead of overflowing; below 360 px the arrows move into the menu's previous/next cards. 320 px reflow and 200% text: no overflow.
- Checks: verify PASS (every author word), gates 0 failures on chain (short, long, dense, safety) and landing and category pages, axe 0 violations, in-figure label test 0 crossings on all 276 figures with the path fully drawn (stricter than the gate), every figure carries all eight stage names.
- Owner decisions still open: the chain's name in the title versus the story's promise to withhold it (author's own file puts the name first; kept); neutral tab titles for watched phones (kept normal for search).

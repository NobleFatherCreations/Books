---
name: Pattern Decoder
description: A metro-at-night sign system for a frightened reader, in Midnight Matte (v17+): ten lettered lines, stations, champagne gold to press, red only for danger, a green exit. (amber-* tokens hold the safety red.)
colors:
  bg: "#050507"
  panel: "#0E0E12"
  panel-2: "#17171D"
  rule: "#25252D"
  rule-hi: "#383842"
  fg: "#F2F0EA"
  fg-2: "#A8A69E"
  fg-3: "#8B8982"
  blade: "#E5C158"
  blade-ink: "#050507"
  gold-line: "#E5C158"
  day-blade: "#E5C158"
  day-blade-ink: "#14161A"
  day-gold-line: "#9A7414"
  amber: "#FF6B5E"
  amber-fill: "#F04438"
  amber-fill-ink: "#050507"
  exit: "#00B864"
  exit-ink: "#04140B"
  toward: "#9CD9BC"
  away: "#AFB8E8"
  day-bg: "#FBFAF7"
  day-panel: "#F3F1EB"
  day-panel-2: "#E8E5DC"
  day-rule: "#DAD6CB"
  day-rule-hi: "#BDB8AA"
  day-fg: "#14161A"
  day-fg-2: "#4B5159"
  day-fg-3: "#5C636B"
  day-amber: "#B42318"
  day-exit: "#007A40"
  day-toward: "#1D6B4A"
  day-away: "#3B4A9A"
  line-truth: "#4A82FF"
  line-pressure: "#9469FF"
  line-control: "#1AA9DE"
  line-hook: "#F05BA0"
  line-wear: "#C06BE0"
  line-blame: "#B07A52"
  line-people: "#FF8A4C"
  line-systems: "#8FA3BD"
  line-online: "#17BDB0"
  line-society: "#A2C23A"
  day-line-truth: "#1F55D6"
  day-line-pressure: "#6A3FE0"
  day-line-control: "#0B7AA6"
  day-line-hook: "#C2316F"
  day-line-wear: "#8E3BB0"
  day-line-blame: "#8A5534"
  day-line-people: "#B4501A"
  day-line-systems: "#5A6F8A"
  day-line-online: "#0A7F76"
  day-line-society: "#5E7A12"
typography:
  display:
    fontFamily: "Overpass, system-ui, sans-serif"
    fontSize: "clamp(2.25rem, 1.3rem + 4.4vw, 3.75rem)"
    fontWeight: 800
    lineHeight: 1.02
    letterSpacing: "-0.025em"
  station:
    fontFamily: "Overpass, system-ui, sans-serif"
    fontSize: "clamp(2rem, 1.3rem + 3.2vw, 3.25rem)"
    fontWeight: 800
    lineHeight: 1.04
    letterSpacing: "-0.025em"
  headline:
    fontFamily: "Overpass, system-ui, sans-serif"
    fontSize: "clamp(1.875rem, 1.2rem + 3vw, 2.75rem)"
    fontWeight: 800
    lineHeight: 1.08
    letterSpacing: "-0.02em"
  title:
    fontFamily: "Overpass, system-ui, sans-serif"
    fontSize: "1.375rem"
    fontWeight: 800
    lineHeight: 1.2
    letterSpacing: "-0.01em"
  sign:
    fontFamily: "Overpass, system-ui, sans-serif"
    fontSize: "1.1875rem"
    fontWeight: 800
    lineHeight: 1.15
    letterSpacing: "-0.01em"
  body:
    fontFamily: "'Atkinson Next', 'Atkinson Hyperlegible', system-ui, sans-serif"
    fontSize: "1.125rem"
    fontWeight: 400
    lineHeight: 1.6
  lede:
    fontFamily: "'Atkinson Next', 'Atkinson Hyperlegible', system-ui, sans-serif"
    fontSize: "1.1875rem"
    fontWeight: 400
    lineHeight: 1.5
  label:
    fontFamily: "Overpass, system-ui, sans-serif"
    fontSize: "0.9375rem"
    fontWeight: 700
    lineHeight: 1.1
rounded:
  none: "0"
  grab: "1rem"
  full: "50%"
spacing:
  s1: "8px"
  s2: "16px"
  s3: "24px"
  s4: "32px"
  s5: "48px"
  s6: "64px"
  top-h: "56px"
  bar-h: "68px"
  side-w: "240px"
  tap: "44px"
components:
  blade:
    backgroundColor: "{colors.panel}"
    textColor: "{colors.fg}"
    rounded: "{rounded.none}"
    padding: "16px 16px 16px 20px"
    height: "72px"
  blade-primary:
    backgroundColor: "{colors.blade}"
    textColor: "{colors.blade-ink}"
  blade-safety-pictogram:
    backgroundColor: "{colors.amber-fill}"
    textColor: "{colors.amber-fill-ink}"
    rounded: "{rounded.full}"
  button:
    backgroundColor: "{colors.panel}"
    textColor: "{colors.fg}"
    rounded: "{rounded.none}"
    padding: "0 16px"
    height: "44px"
  button-primary:
    backgroundColor: "{colors.blade}"
    textColor: "{colors.blade-ink}"
  button-hover:
    backgroundColor: "{colors.panel-2}"
  leave:
    backgroundColor: "{colors.exit}"
    textColor: "{colors.exit-ink}"
    rounded: "{rounded.none}"
    padding: "0 14px"
    height: "44px"
  line-bullet:
    backgroundColor: "{colors.line-truth}"
    textColor: "{colors.bg}"
    rounded: "{rounded.full}"
    size: "28px"
  safety-plate-band:
    backgroundColor: "{colors.amber-fill}"
    textColor: "{colors.amber-fill-ink}"
    padding: "10px 16px"
  exit-plate-band:
    backgroundColor: "{colors.exit}"
    textColor: "{colors.exit-ink}"
    padding: "10px 16px"
  search-field:
    backgroundColor: "{colors.blade}"
    textColor: "{colors.blade-ink}"
    height: "56px"
  panel:
    backgroundColor: "{colors.panel}"
    textColor: "{colors.fg}"
    padding: "24px"
---

# Design System: Pattern Decoder

## Overview

**Creative North Star: "The Metro at Night"**

A frightened reader needs to know where they are and where to go next. The Decoder answers with the sign system of a metro after dark: near-black panels, enamel-white lettering, ten coloured lines each with its own letter, every tactic a station on a line, look-alike tactics in other lines shown as "change here for". The Leave control is exit green and sits in the top bar on every screen. The build refuses the support-site pastel and the moving sky of the previous version (v14).

The system is square-cornered and calm. Since round four it is also coloured: each line's colour is its identity and fills tiles, heroes and the selected step (see the addendum), with a quieter option one tap away. Signs are rectangles with square corners; lines and stations are circles; triangles appear only for safety. Colour never carries meaning alone: every line colour has a letter, every state has a word or shape. Nothing moves unless the reader tapped something. Reading is the job, so body text is large (18px), measured (about 42-44rem), and set in a face designed for low-vision legibility.

Evidence note: the first viewport in the build matches the contract (headline at 36px on a phone, three blades with the white "Help me figure it out" first, ten-line index, Private status and green Leave in the top bar, four doors on the thumb edge).

**Key Characteristics:**
- Night is default; day is a full second theme (and follows the system preference unless the reader chose).
- Ten line colours in two values each, always paired with a letter.
- Two reserved signal colours: amber (danger) and exit green (leaving).
- Overpass 800 for signs, Atkinson Next for reading.
- Sharp rectangles for signs and controls, circles for lines and stations.
- Tonal panels, hairline rules, inset rings. Round four adds two soft glows (a line-colour wash behind Home and each station, and a glow on the station's colour bar); there are still no card drop shadows.
- Motion only in response to a tap, transform and opacity only.

## Colors

A near-black neutral ladder, white-on-black "blade" signs for the primary action, ten line hues, and exactly two signal colours.

### Primary
- **Enamel White** (`blade`, #F2F4F1; day: #111416 ink-on-white inverted): the primary sign. Primary blade, primary button, selected tab/segment, search field, toast, version badge. It is the only "accent" for action: the strongest thing on screen is the thing to press.

### Secondary
- **Ten Line Colours** (`line-*`, night values in the frontmatter, day values as `day-line-*`): Truth (T), Pressure (G), Control (C), Hook (L), Wear (W), Blame (B), People (P), Systems (S), Online (O), Society (M). Each is set as `--lc` on an element via `[data-g=...]` and consumed by line bullets, the strip map, the line diagram, the network map, step progress, and the quote mark in "what it sounds like". Bullet text uses `bullet-ink` (dark in night, white in day). Letters are mandatory.

### Tertiary
- **Warning Amber** (`amber` #FFB020 night, `day-amber` #9A5B00): danger only. Text and icons use `amber`; the safety band and the safety pictogram use `amber-fill`, which stays #FFB020 in both themes with `amber-fill-ink` text.
- **Exit Green** (`exit` #00B864 night, `day-exit` #007A40): Leave only: the top-bar Leave button and the exit plate band.
- **Toward / Away** (`toward`, `away`): the two directions of a "checks both ways" comparison; they are tints, not statuses.

### Neutral
- **Platform Black** (`bg`), **Sign Panel** (`panel`), **Raised Panel** (`panel-2`): page, resting surface, hover/selected-quiet surface. Day: white, #F3F5F6, #E6EBED.
- **Hairline** (`rule`), **Hairline High** (`rule-hi`): dividers and outlined ("quiet"/"line") controls.
- **Text 1/2/3** (`fg`, `fg-2`, `fg-3`): primary, secondary/meta, and non-text marks only (bullets, underline colour). `fg-3` is not for running text.

### Named Rules
**The Letter Rule.** A line colour is never used without its letter or its name beside it. Colour is the second channel.
**The Danger-Only Amber Rule.** Amber means "slow down, this is about safety". Never use it for emphasis, highlights of ordinary content, or decoration. In the build, `mark` highlights use a neutral underline, not amber.
**The Exit-Only Green Rule.** Green means "leave". It is never a success, "saved" or "done" colour.
**The Two-Values Rule.** Every line colour has a night and a day value tuned for contrast on that ground; add a new line by adding both.

## Typography

**Sign Font:** Overpass, weights 600-800 (system-ui fallback), self-hosted and inlined.
**Reading Font:** Atkinson Next 400-700 plus 400 italic (Atkinson Hyperlegible, then system-ui), self-hosted and inlined.

**Character:** Overpass 800 is the lettering on a station wall: tight, heavy, confident, used for every heading, label, button and number. Atkinson is the plain-spoken voice for definitions and scripts. Two faces, a strong scale jump between them.

### Hierarchy
- **Display** (800, clamp 2.25rem to 3.75rem, 1.02): home headline only; max-width 13ch.
- **Station name** (800, clamp 2rem to 3.25rem, 1.04): the tactic title beside its line bullet.
- **Headline** (800, clamp 1.875rem to 2.75rem, 1.08): page titles (`h-page`).
- **Title** (800, 1.375-1.625rem, 1.15-1.2): section and step headings.
- **Sign / row name** (800, 1.0625-1.1875rem, 1.15-1.25): blade titles, row names, sub-headings (`k`).
- **Body** (Atkinson 400, 1.125rem, 1.6): all reading. Lede is 1.1875rem in `fg-2`, max 38rem; answer text max 42rem.
- **Label** (Overpass 700, 0.8125-0.9375rem): buttons, tabs, meta, counts. Sizes below 0.8125rem are not used.

### Named Rules
**The Sign-vs-Read Rule.** If the reader scans it, it is Overpass 800; if they read it, it is Atkinson. Never set paragraphs in Overpass or headings in Atkinson.
**The Reader-Sized Rule.** Root size can be raised to 112.5% or 125% by the reader (`data-size`), and a roomy spacing mode raises line-height to 1.8. Everything is in rem so it all scales; do not add px type.
**The Quiet Caps Rule.** Uppercase tracked text appears in exactly two places: the sidebar "Lines" group title and the fact-list terms. Do not extend it to new eyebrows or labels.

## Layout

Mobile first. A sticky top bar (56px) holds brand, Private status, and Leave. Four "doors" (Help, Search, Map, Saved) form a bottom sign bar (68px) on phones and a 240px left rail from 56.25em (900px), where the rail also lists the ten lines. Content is a single `view` column (max 44rem) or `view wide` (72rem). From 70em the station page becomes two columns (content plus an 18rem sticky "change here" side).

Spacing is an 8px ladder (`s1` 8, `s2` 16, `s3` 24, `s4` 32, `s5` 48, `s6` 64) with a handful of 4px, 6px, 10px and 14px micro-gaps inside components. Every tap target is at least 44px (2.75rem), most blades 72px. Safe-area insets are honoured on every fixed edge. Sections are separated by hairlines and generous vertical space, not boxes.

### Named Rules
**The Thumb Rule.** The four doors, and anything the reader needs mid-panic, sit in the lower half of a phone. Leave is always in the top bar, never moved.
**The 44 Rule.** No interactive element is shorter than 44px, including inline links and chips.

## Elevation & Depth

Flat and tonal. Depth is a step on the ladder `bg` to `panel` to `panel-2`, plus one pixel `rule` lines. Selection and emphasis use inset rings (`box-shadow: inset 0 0 0 1px/2px`), never drop shadows. The only floating things are the toast, the station sheet (with a 60% bg backdrop) and the breath-break box; they are distinguished by colour (white toast) or backdrop, not shadow. Focus is a 3px `fg` outline with 3px offset and a 6px `bg` halo.

### Named Rules
**The No-Shadow Rule.** No blur or offset shadows. Separate by tone, rule, or ring.
**The Visible Focus Rule.** Focus ring is 3px, `fg`, offset 3px, on every control including map stations and the segmented radios.

## Shapes

Two form families with fixed meaning. **Circle** (50%) means line or station: line bullets (28px, 24px small, 48px large), strip-map and diagram stations, step numbers, pictograms, check dots. **Rectangle** (0 radius) means sign or control: blades, buttons, tabs, rows, panels, plates, fields. **Triangle** means safety only (the warning glyph in rows and the safety plate). The one soft exception is the pill behind the active door icon on phones (2.75rem by 1.75rem, 1rem radius) and the sheet grab handle. In forced-colors mode bullets become outlined Canvas circles.

### Named Rules
**The Shape-Means Rule.** Circle = line/station, rectangle = sign/control, triangle = safety. Do not round a button or square a station.

## Components

### Blades (directional signs)
Full-width, 72px minimum, panel-coloured rectangles with a pictogram circle, a bold title, a muted one-line, and a trailing arrow. **Primary** blade is enamel white with dark ink (one per screen, first). **Safety** blade swaps the pictogram circle to amber fill. **Quiet** blade is transparent with a 1px high rule ring and 56px height.

### Buttons and Segments
44px rectangles in panel colour, Overpass 700 15px. Primary is white blade; "line" variant is a 1px ring; pressed/selected inverts to white blade. Hover (fine pointers only) steps to `panel-2`. Segments, tabs, and the settings choice groups follow the same invert-on-selected rule. Disabled is 50% opacity.

### Leave
Exit green rectangle with a door-arrow icon in the top bar. The one place green is used for an action.

### Line bullet and Station Strip
Circle with the line letter (Overpass 800). The strip shows the station on its line: a 4px line in `--lc`, open ringed stations, a larger filled "here" with a thick ring, a bar for the line end, then previous/next names and "n of N".

### Rows (departures board)
Hairline-separated rows: bullet, station name, one-line description, optional "change here" chip and triangle if safety-sensitive. Line index rows add a tabular count.

### Four steps (tabs) and Answer panel
Four equal tabs with numbered circles, selected tab becomes white blade, visited tabs fill their number circle; a 4px progress bar in the line colour sits under them. Panel content slides in from the side of travel. The answer is a `panel` with the summary, "it sounds like" quotes (line-coloured quote mark), and a checklist.

### Safety plate and Exit plate
Panel with a full-width band: amber with a triangle and dark ink (safety), or exit green with the exit ink (leaving). Always placed before the answer on safety-sensitive entries.

### Search field
White blade-coloured bar, 56px, dark ink text, clear button 44px, focus via a 3px outline around the whole field.

### Network map and station sheet
An SVG of ten lines (6px strokes, ringed stations 3px). Selected station fills `fg`; unrelated stations dim to 32% when a line is chosen. Tapping opens a bottom sheet (full width on phones, 24rem card from 56.25em) with a grab handle. Cross-links draw in with a 0.32s dash animation.

### Toast, term definition, breath break
Toast is a white blade bar above the sign bar. Terms are dotted underline with an inline `panel-2` definition. The breath break is a calm panel on a 82% bg veil, offered after long reading and permanently dismissible.

### Motion (all gated by reduced-motion preference and a reader setting)
Exactly five motions, all transform/opacity and all caused by a tap: press-scale to 0.97 on controls; step panel slide-in (24px, 0.22s); station-link draw (0.32s); bottom sheet rise (0.28s; fade on desktop); page cross-fade view transition (0.12-0.18s). Plus toast fade and progress-bar scale. Nothing loops, parallaxes, or starts by itself.

## Do's and Don'ts

### Do:
- **Do** put one white primary blade or button per screen, and make it the first thing.
- **Do** pair every line colour with its letter, and every state with a word or shape.
- **Do** use `amber-fill` for the band and `amber` for text and icons; both stay on danger.
- **Do** keep Leave in the top bar in exit green on every screen.
- **Do** build new styles from tokens inside the existing layer order: reset, tokens, base, layout, components, pages, motion, print. A new rule goes in the right layer, not on top.
- **Do** set sizes in rem so reader text-size settings scale them.
- **Do** gate any new motion behind `prefers-reduced-motion: no-preference` and `data-motion` not set to reduce, and animate transform/opacity only.
- **Do** run `node scripts/decoder-verify.js` after any change; it is the regression net (below).

### Don't:
- **Don't** use amber for anything but safety, or green for anything but leaving.
- **Don't** use colour alone to separate lines or states.
- **Don't** round buttons, blades, or panels, or square the circles of lines.
- **Don't** add card drop shadows, decorative gradients, or motion that starts without a reader action. (The line-colour washes and tile fills are identity, not decoration, and switch off under Quiet colours, contrast and forced-colors modes and print.)
- **Don't** add `!important` to the stylesheet. The existing 7 are `[hidden]`, the print hide list, and the shared House seal override; that is the full allowance.
- **Don't** write type smaller than 0.8125rem or tap targets under 44px.
- **Don't** restyle the shared House menu from inside this system.

## Regression net and known gaps

`/home/user/Books/scripts/decoder-verify.js` (Playwright; axe-core optional) is the regression net. It checks every one of the 310 stations at 390px and 1440px (no sideways scroll, name fits, answer on first phone screen, safety note before answer on sensitive entries, four steps present), private-by-default storage, neutral title, axe-core on every page type in both themes, measured text contrast in both themes, and load timing at 4x CPU slowdown. Run it against `instruments/playbook/_undeployed/v15/index.html`.

Known gaps, stated honestly:
- No real-device pass and no real screen-reader pass yet; the suite does not replace them.
- The shared House menu (`.nf-seal`, `#nf-chrome`) is outside this system; its unlayered rules and the seal override are the only unlayered CSS.
- Light mode `mark` highlight and `--mark` token are defined but the current build's `mark` uses a neutral ring; `--mark` is unused.

Not canonized (defects or one-offs the build carries, not rules for future surfaces): the `!important` seal override (a compatibility patch for the shared menu); the `?` and curly-quote glyph markers used as list decoration (typographic stand-ins, not an icon system); the unused `--mark` token.


## Additions after the first review (2026-10-25)

Seven techniques from v14 came back, each caused by the reader (a tap or a scroll), none moving on its own, all safe under Reduce motion.

- **Reading line.** A 3px line in the station's line colour under the top bar, filled by scrolling itself (`animation-timeline: scroll()`, behind `@supports`). It is the only scroll-driven element; absent in browsers without support. It is a station-page device: `body[data-page=station]`, with the line colour carried on `body[data-g]`.
- **Sign band.** `.sname::before`, 8px, full width, in `--lc`. After a tap it draws in once (`.sweep`, 0.3s, `--ease`).
- **Search reach.** Results add "Lines and pages" (lines by name, blurb or letter; pages by title and keywords; three characters minimum) and, with saving on, "Recently read". Page rows use a neutral circle bullet (`.b.n`), never a line colour.
- **Map flight.** "Show on the map" (`data-showmap`) selects a station (larger white node), draws its interchange links, and scrolls it to the middle (`scrollIntoView`, instant under Reduce motion).
- **More contrast and forced colours.** `prefers-contrast: more` lifts `--fg-2`, `--fg-3` and the hairlines to full strength and gives every control a 2px inset outline; `forced-colors: active` gives controls a 2px `CanvasText` border and keeps the selected state in `Highlight`.
- **Off-screen rows.** `.rows>.row{content-visibility:auto}`. Not applied to the line diagram, because paint containment would clip the focus rings of its links.
- **Quotes.** The list draws one quote mark. Lines the data already quotes are stripped of their own; lines that open with a quote and then narrate (`.says li.nq`) keep their text and lose the drawn mark.

Regression net: `scripts/decoder-verify.js`, 43 checks, including a same-machine comparison against live v14.


## Round three addendum (2026-10-26)

Added: line emblems (shape identity beside colour), enamel rim on sign panels, tactile-paving dots on the safety band, a Home
network thumbnail (a sketch, labelled as one), pictograms for "where", a greyscale printed station card, departure-board code
plates (G 01) with search by code, directional arrows on Previous/Next, a faint subway-tile wall on Home, and four-point stars
at line termini only. Cut in review: the headline star. Safety: one scrambled `ui-state` entry (numbers only, no timestamps,
described as scrambled not secret), rested lines excluded from search, codes, Saved, Continue, routes and station pages,
Leave destination chosen in Settings with depth kept in history.state, no referrer. Print hides the route strip and app chrome.


## Round four addendum (2026-10-27)

**Colour and depth.** The first build read as flat dark grey. Colour now appears wherever a line appears, because a line's colour is its identity:
- Home lists the ten lines as ten solid colour tiles (dark ink on the night colours, white ink on the day colours, both at 4.5:1 or better).
- A thin ten-colour stripe runs under the top bar.
- A soft glow sits behind the Home headline and behind each station in that line's colour. It is the body's own background image, because a pseudo-element behind the body background is invisible.
- Line pages open with a full block of the line's colour; on a station the selected step tab, the answer panel's top edge and the sign bar take the line colour.
- Night is a deep ink (`#0A0E16` family); Day is warm paper (`#FBFAF7` family).
- **Quiet colours** (`data-color=quiet`, a Settings choice and a link on Home) shrinks colour back to small marks for a calmer look or a shared screen. It is not saved while saving is off. Vivid is the default because the owner asked for the build to stand out; the independent review recommended Quiet as the default. That is an open owner decision.

**Ten phone upgrades.** Back to top (appears only when scrolling up); a slim step bar above the sign bar once the four tabs scroll away (placed at the bottom so it can never sit under Leave); Paste in search; the sign bar steps aside when the keyboard is up; a Text size button; opt-in tap buzz (off by default, never on Leave); a one-time swipe tip; read-aloud with on-device voices only (first tap warns that it plays out loud, it reads the safety note first, and it stops on any step change or Leave); touch-feel CSS (no tap delay, no pull-to-refresh, pinch-zoom kept); a short pop on Save.

**Review fixes shipped.** Resting-line tiles stay readable; print drops colour fills and glows so nothing prints white on white; forced-colors gives the new surfaces borders; the dock moved off the top; the pause card sits above the dock but below the top bar so Leave stays on top; a CSS `:has()` rule was replaced by a variable because it slowed the A to Z page.

**Plain wording.** Every entry was re-read in 26 batches plus a six-list second pass and a repeated-phrasing fix: 4,101 of 18,819 passages changed, mean reading grade 8.7 to 7.8, sentences over 24 words 2,573 to 138, no dashes. Guards refused any rewrite that changed a number, a named term, quoted words, a negation or a hedge. Named people and works were checked (Freyd, Lippmann, Herman and Chomsky, Lifton, the RAND firehose research); one study description was corrected and two unsupported jargon labels were removed. Medical symptom lists and safeguarding notes are unchanged and still need clinical review.


## v17 addendum: Midnight Matte (2026-10-27, owner decision)

The owner chose a matte black and champagne gold look, with safety moved off amber so gold and danger never meet.
Token names are unchanged; their values are not. **Read the frontmatter above as v15 history for these tokens.**

- **Ground:** `bg` #050507, `panel` #0E0E12, `panel-2` #17171D, `rule` #25252D, `rule-hi` #383842; text #F2F0EA / #A8A69E / #8B8982.
- **The one accent is champagne gold** (`blade` #E5C158 with #050507 ink; day #6B500F with white ink): the primary blade,
  pressed and selected states, step tabs, the version badge. The search field is an obsidian panel with a 2px gold ring,
  not a gold bar. The home glows and the enamel rim are faint gold.
- **Safety is red** (the `--amber*` tokens): text #FF6B5E (day #B42318), band fill #F04438 with #050507 ink. The
  Danger-Only rule now reads "red means danger": never use red for emphasis or decoration. It is always paired with
  the triangle (now on the plain pages too).
- **Exit green is unchanged.** Green still means leave and nothing else.
- **People line moved from coral to orange** (#FF8A4C, day #B4501A) so no line colour reads as a warning.
- All of it measured: 1,344 text runs at ≥4.5:1 in both themes, axe-core clean; suite 109/109.


## v18 addendum: room to read (2026-10-27)

From an independent critique (Nielsen 29/40) and the owner's pasted v18 brief (checked line by line in
`docs/DECODER-V18-PASTE-CHECK.md`). Content is unchanged.

- **Reading mode on phones.** On a station, once the four tabs scroll away, `body.reading` hides the four doors and the step
  dock takes the bottom edge alone (with the safe-area inset). Scrolling up removes `reading`: the doors and Back to top
  return. Desktop is unchanged (the doors are the left rail). This cut about 64px of chrome while reading.
- **The step dock and Back to top are obsidian, not gold slabs.** The dock is a `panel` bar with a 3px line-colour top edge
  and gold arrows. Back to top is a `panel` disc with a 2px gold ring. Gold stays the accent for the one thing to press,
  not for chrome over the text.
- **Four choices before the steps.** Save · Listen · Text size · More (`details.moreacts`), with Share link and Print under
  More. Listen stays visible because its Stop must never be hidden.
- **Compare on phones** (below 600px) stacks the two sides into one column, and each block carries a small label
  (`.cmp-who`: bullet plus name).
- **Day gold is champagne.** `blade` #E5C158 with #14161A ink; `--gold-line`/`--blade-edge` #9A7414 draws the 1px edge on
  gold fills and the 2px search ring (≥3:1 non-text contrast on paper). Night has `--blade-edge: transparent`.
- **The map sheet's backdrop mutes the map** (`backdrop-filter: blur(6px)`), turned off under
  `prefers-reduced-transparency`.
- **Tap targets:** the Compare links and the compare name links are now at least 44px.
- **Sentence splitting fixed** (app `sentences()` and `decoder_pages.sentences`): `. ! ?` plus closing quotes end a
  sentence only before a space or the end, so `'did this happen at all?', you are…` stays one sentence. This was a
  rendering bug that left a stray quote mark at the start of a paragraph; no text changed.
- **Considered, not adopted:**
  - grain texture: Assessment A found the stripe and tile wall already slightly decorative; the paste's SVG was broken.
  - one-card PREV / MATRIX / NEXT deck: it would drop the four steps, search results and compare.
  - tracked 9–11px capitals, `user-scalable=no`, `user-select:none`, crimson exit: see the paste check for why.
- **Regression net:** `scripts/decoder-verify.js` now has 112 checks (three new v18 checks).


## v19 addendum: one scroll, no map, Apple manner (2026-10-27, owner brief; candidate build, not deployed)

The owner asked for the single-scroll station, no clutter or tabs, the "tracks with small circles" replaced by an easier way to
navigate, and an Apple feel. Content is unchanged. This answers two of the open owner questions: **one page, not four tabs**,
and **Quiet colours is the default** (the calm look the brief asks for; Vivid is opt-in in Settings).

- **A station is one scroll.** The four steps are four sections (`#sec-0..3`, `.panelx`): Is this it? / Understand / What to do /
  Go deeper. A sticky section index (`.secnav`, four buttons, 44px, 13px labels) sits under the top bar, follows the reader down
  (scroll-spy sets `aria-current`) and jumps on tap. Keys 1 to 4 jump too. Old `/entry/slug/3` and `/s/5/4` addresses scroll to that
  section. Gone: the tabs, the step bar, Next buttons, the swipe and its hint, the step dock, the line strip with its track of dots.
- **Phone reading mode, v19.** Going down the page the sign bar slides away (`body.reading`, set by scroll direction, not by a
  threshold); scrolling up brings it and Back to top back. The section index stays. Honours reduced motion.
- **No map.** The network map, the station sheet, the Home thumbnail, the line page's track and the route strip are removed, with
  `Show on the map` and `See them on the map`. The third door is now **Browse** (`#/lines`): ten lines as an inset grouped list, a
  two-way segmented control (By line / A to Z), and "Other ways in" rows (where it happens, most common, patterns). `#/map` and
  old sky/constellation links redirect to Browse. "Change here for" and Compare, which carried the map's real value, stay.
- **Home** is: headline, gold Help blade, a search field (a link to Search, cursor lands in the box), the safety blade, then the ten
  lines as a grouped list. No brick wall, no stripe, no glow, no colour toggle (Settings has it).
- **Apple manner, within the tokens.** Frosted top bar, section index and sign bar (`backdrop-filter`, solid under
  `prefers-reduced-transparency`); inset grouped lists with hairlines inset to the text and a chevron; capsule buttons and
  segmented controls; one radius scale (`--r` 14px, `--r-s` 10px); large tight-tracked titles; the line's colour is a short
  pill above the title and the letter bullet. Fonts, gold, safety red and exit green are unchanged. Shape rules live in one block.
- **Quiet is the default.** `data-color=vivid` (opt-in) restores the colour tiles, stripe, glow and coloured line headers. A saved
  `co:"quiet"` is simply the default; the head script now only sets `vivid`.
- **Top bar** no longer overlaps at the Largest text size (the name truncates).
- **Not done / still open:** Help Q2 wording ("they say it never happened") needs the owner's yes; "the 13 gates" undefined; the
  grain texture stays rejected. `docs/DECODER-REVIEW-PACK-v17.md` still describes tabs and the map (see the note at its top).
- **Regression net:** `scripts/decoder-verify.js` is now 105 checks: the map, sheet, tab, dock, swipe, route-strip, thumbnail and
  colour-toggle checks were removed or rewritten for the new structure; new checks cover the section index (pinned, marks where
  you are, jumps), keys and deep links, the sliding sign bar, Browse rows, Quiet default and Vivid opt-in, the Home search
  field, and the top bar at 320px. Axe: no serious or critical findings (64 scans). LCP 572 to 624 ms on the 4x slowdown.

### v19 final audit (2026-10-27): attacks made, and what changed

Each area was attacked as an opponent would, then fixed or kept with a reason.
- **Navigation.** Attack: the section index is not on the first screen. Kept: the answer must come first; the index becomes
  sticky as soon as it is reached, and keys 1 to 4 work. Attack: the sign bar hiding while reading hides escape routes. Kept:
  Leave lives in the always-sticky top bar; the sign bar returns on any scroll up. Fixed: the A to Z letter bar was a stretched pill;
  it is now plain chips.
- **Readability.** Fixed: the reading measure was about 75 characters; sections are now capped at 38rem (about 65). Body stays 18px,
  labels 13px or more, secondary text at 4.5:1 or better in both themes. Frosted bars are 95 to 96 percent opaque so text never
  ghosts through behind the Leave button.
- **Consistency.** Fixed: the plain pages (where search visitors land first) wore the old slab look. They now share the radii, the
  short colour pill, the frosted top bar and the quiet answer card. Fixed: the House seal overlapped text on plain pages.
- **Presentation.** Added a 1200 by 630 link-preview image (`scripts/make-decoder-og.js`), used by every page.
- **Findability.** Already in place from v16 and kept: descriptive titles, canonicals, `DefinedTerm`, `BreadcrumbList`, 322-address
  sitemap, robots naming the AI crawlers, crawlable plain pages. Added: `robots` meta with `max-snippet:-1,
  max-image-preview:large`, `og:image` and a large Twitter card, `dateModified` on every plain page, and `/playbook/llms.txt`.
  Not added, on purpose: FAQ markup (rich results restricted and the entries are not FAQs), a root `llms.txt` (the hub is a
  separate site), `hreflang` (one language).
- **Known limits.** The suite runs a software browser, so real-phone feel is unmeasured; ranking and AI citation take weeks and
  depend on outside links; both sitemaps still need submitting in Search Console and Bing Webmaster Tools by the owner.


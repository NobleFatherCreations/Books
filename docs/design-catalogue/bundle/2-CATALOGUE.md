# Design Catalogue: the vocabulary of everything

> **File names inside this bundle.** The sources refer to numbered files in the repo folder `docs/design-catalogue/`. In this bundle they live here: **00 README, 01-05, 06 names bible, 07 rules, 09 winners, 10 gaps, 11 resources, 12 v2 improvements, 13 books playbook** are sections of documents 2-5 (see each document's contents). `COVERAGE-TEMPLATE`, `templates/*` and `PROMPT-MASTER` are inside documents 1 and 3. Scripts are in `code/`. In the repository the originals are separate files and are the editable source.

Contents: How to use the catalogue (00) · 01 Styles, movements, brands, genres · 02 Foundations · 03 Motion, interaction, navigation · 04 Experience, content, safety, accessibility, performance · 05 Techniques · 06 Master names bible (56 categories).


---

## 00 How to use the catalogue

### Design catalogue — how to use it (read this first)

A master vocabulary of visual design, interaction and experience choices, so a build starts by **choosing deliberately from the full menu** instead of defaulting to "dark, serif, beige, cards".

**Honest limits.** This is compiled from the model's knowledge (cut-off mid-2026). "Current" trends move monthly and brand sites change without notice. Treat every brand entry as a lead to verify by opening the live site and screenshotting it (see Refresh protocol). Nothing here is a substitute for looking at real screens.

#### Files

| File | Covers |
|---|---|
| `01-styles-and-brands.md` | Named visual styles and movements; what major brands, publishers, studios and design systems are known for; award-site genres |
| `02-foundations.md` | Layout, grids, type, colour, imagery, illustration, icons, surfaces and effects, density, theming |
| `03-motion-interaction-navigation.md` | Motion principles and techniques, scroll storytelling, interaction models, gestures, navigation, components, feedback, sound and haptics |
| `04-experience-content-quality.md` | Mental models, emotional tone, content and voice, onboarding, search, forms, errors, trauma-informed and safety design, accessibility, performance, evaluation |
| `06-master-names-bible.md` | **Start here for "what exists".** 56 categories of pure names: site genres, section types, hero types, nav, scroll techniques, page transitions, text effects, cursor and hover effects, 3D/shader effects, backgrounds, motion vocabulary, cinematic techniques, data-viz forms, design laws, dark patterns, tools, inspiration sources, 2025–26 emerging items |
| `07-choosing-and-combining.md` | **The intelligence layer.** Why outputs burn out (failure modes F1–F14), the Budget (1 lead, 1 signature, ≤3 feature effects), selection procedure, compatibility rules, composing and pacing, recipes, anti-cliché list, acceptance criteria |
| `PROMPT-MASTER.md` | The reusable prompt to start any design session (phases, tools, hard rules). Also invokable as the `/design-director` skill |
| `DESIGN-SYSTEM-GUIDE.md` | **Give this to another AI (and read it yourself).** How the whole system works, the steelman and objections, the opening interview question bank, the operating script, and what the owner must do |
| `COVERAGE-TEMPLATE.md` | One row per category of the names bible; the AI must mark every row USE / REJECTED / N/A so nothing is silently skipped |
| `09-award-winners-data.md` | **Raw data:** verified Awwwards Site of the Year winners 2017–2025, 2024–25 scores, and component profiles of the winners with evidence labels (what each was actually made of), recurring patterns, and a research queue for what is still missing |
| `10-system-gaps-and-improvements.md` | The ten biggest weaknesses of this design system and how to fix them, in suggested order |
| `11-free-resources-directory.md` | Free fonts, images, 3D, audio, libraries (with verified licences), MCP servers and skills, testing and learning resources |
| `12-system-v2-improvements.md` | What was built for each of the ten gaps and how to run it; library-policy options; iOS plan; security, rollback, retrospective |
| `13-html-books-playbook.md` | Everything specific to the owner's HTML books: constraints, 24 components, per-book design seeds, book gates, paste-ready prompt |
| `recipes.html` | 13 tested, dependency-free technique recipes |
| `templates/` | OWNER-TASTE, DESIGN-STATE, ASSET-REGISTER, PHONE-CHECK, SCORECARD |
| `bundle/` | Compiled bundle (5 documents + all-in-one + zip), built by `scripts/build-design-bundle.py` |
| `05-techniques.md` | Concrete web techniques (CSS, JS, SVG, canvas, WebGL, fonts, media) with a self-containment rating for this repo |

Every item has an ID (`S-12`, `T-07`, `M-31`). Cite IDs in your design-direction document so choices are traceable.

#### Constraint tags (this repo, from `CLAUDE.md`)

- **[SC]** self-contained: fine as is (plain HTML/CSS/JS/SVG, inline or local files).
- **[LIB]** needs a library copied in as a local file (permissive licence, state size). Ask the owner before adding anything heavy.
- **[NET]** needs a network request at run time. **Not allowed** (only the Cloudflare beacon is sanctioned).
- **[SAFE]** relevant to safety-sensitive pages (coercive-control, abuse, minors): see file 04, section Q.
- **[IOS]** known iOS Safari pitfalls; test on a real phone.

#### The selection method (do this in order)

1. **Write the brief in 8 lines.** Who is the reader, what state are they in (calm, curious, stressed, in danger, on a shared device), what must they do or feel, on what device, how long a session, what the content is (chapters, tools, data, stories), what must never happen, what the owner has already said.
2. **Choose a position on each axis** (see Axes below). Write one sentence per axis. Do not skip axes; a skipped axis defaults to generic.
3. **Pick from the catalogue, three candidates per category that matters** (style, type, colour, layout, motion, navigation, imagery). For each, note why it fits and the one risk. Reject on purpose, and write why.
4. **Compose a coherent set**, not a collage. Two strong styles clash unless one leads. Limit: one lead style, one supporting influence, one signature move.
5. **Run the constraint filter**: tags above, accessibility minimums (file 04 section R), performance budget (file 04 section S), the project rules, anything the owner forbade.
6. **Prototype one hero screen on a phone-size and a desktop-size canvas**, screenshot, read the image, critique against file 04 section T. Only then scale.
7. **Record the choices** in `DESIGN-CHOICES.md` for that project using the template at the end of this file.

#### Axes (choose a position on each, in words)

Quiet ↔ loud · Warm ↔ cool · Human/handmade ↔ engineered/precise · Dense ↔ spacious · Text-led ↔ image-led ↔ figure-led · Static ↔ choreographed · Playful ↔ grave · Familiar ↔ novel · Intimate ↔ monumental · Dark ↔ light (and whether both) · Flat ↔ dimensional · Editorial ↔ product ↔ cinematic ↔ tool · Guided linear ↔ free exploration · Reassuring ↔ provocative · Timeless ↔ of-the-moment.

#### Refresh protocol (do before trusting "current")

1. Open 8–12 live reference sites for the job with Playwright; screenshot at 390 and 1440; read the images.
2. Search recent design-trend write-ups and award-site (Awwwards, FWA, CSS Design Awards, Site Inspire, Godly, Lapa Ninja, Mobbin, Page Flows, Dribbble/Behance trends, Typewolf, Fonts In Use, Pentagram/Collins case studies); note what changed since this file's date.
3. Add what you learned to the catalogue with date and source. Never delete an entry; mark it dated.

#### Template: `DESIGN-CHOICES.md`

```
Brief (8 lines):
Axes (one sentence each):
Lead style: [ID] why / risk
Supporting influence: [ID]
Signature move: [ID]
Type: display [ID], text [ID], mono/aux [ID]; scale; measure
Colour: [ID], tokens (light/dark), contrast table
Layout & grid: [IDs]
Imagery / illustration / icons: [IDs]
Motion: principles [IDs], durations/easings, reduced-motion plan
Navigation & interaction: [IDs]
Content voice & safety: [IDs]
Rejected (with reasons):
Constraint filter results:
Hero-screen screenshot paths and critique notes:
```


#### Gates script
`node scripts/design-gates.mjs <url> <outdir> [--profiles phone-light,desktop-dark,...] [--max 60]` screenshots every scroll step on phone and desktop (light, dark, reduced motion) and fails on figure/text collisions, text over text, page errors, external requests, overflow and reduced-motion violations; warns on tiny text, small tap targets, translucent headers, background-figure legibility, unloaded fonts and too many simultaneous animations. Always read the screenshots it saves.


---

## 01 Styles, movements, brands, genres

### 01 — Styles, movements, brands, genres

Dates are approximate. "Known for" = what the brand is widely recognised for; **verify on the live site before borrowing**.

#### A. Named visual styles and movements

**Classical and modernist lineage**
- S-01 Swiss / International Typographic Style: grids, flush-left ragged-right, neutral grotesque, asymmetry, objective photography.
- S-02 Bauhaus / constructivist: primary colour, geometry, diagonals, bold rules, photomontage.
- S-03 Modernist editorial (mid-century): big type, white space, restraint (Rand, Vignelli, Lubalin influences).
- S-04 Art Deco: symmetry, geometric ornament, gold and black, stepped forms.
- S-05 Art Nouveau: organic line, botanical ornament, flowing lettering.
- S-06 Arts and Crafts / William Morris pattern: dense repeating nature pattern.
- S-07 Mid-century modern: flat shapes, atomic motifs, warm palette.
- S-08 Vintage print: letterpress, woodcut, engraving, halftone, risograph, mimeograph, duotone, spot colour overprint.
- S-09 Poster / psychedelic (1960s): vibrating colour, melted lettering, hand-drawn ornament.
- S-10 Punk / zine / photocopy collage: cut-and-paste, torn paper, tape, xeroxed texture.
- S-11 Postmodern / Memphis: clashing pattern, squiggles, saturated pastels.
- S-12 Cyberpunk / retro-futurism: neon on dark, scanlines, HUDs, glitch.
- S-13 Y2K / frutiger aero: glossy, aqua, bubbles, translucent plastic, lens flares.
- S-14 Vaporwave / synthwave / outrun: gradients, grids, statues, palm silhouettes.
- S-15 Skeuomorphism (and its return as "soft skeuo"): real-material metaphors, depth, realistic shadows.
- S-16 Flat design (2013 on) and its descendants: solid colour, no depth.
- S-17 Material Design (Google, 2014 on) and Material 3 / Material 3 Expressive (2025): elevation, dynamic colour, expressive shape and motion.
- S-18 Neumorphism / soft UI: extruded same-colour surfaces (poor contrast, avoid for accessibility).
- S-19 Glassmorphism / "liquid glass": translucent blur layers, light refraction (Apple's Liquid Glass design language, 2025: translucency that responds to content and motion).
- S-20 Neo-brutalism / web brutalism: hard borders, offset hard shadows, raw system fonts, loud flat colour, visible structure.
- S-21 Brutalist-editorial: monospaced type, stark grids, default-looking HTML as aesthetic.
- S-22 Minimalism / "quiet luxury": restraint, one accent, enormous margins, excellent type.
- S-23 Maximalism: dense layering, clashing pattern and type, abundance by design.
- S-24 Dark-mode "developer product" look (Linear/Vercel era): near-black, thin borders, glow, gradient text, grid lines, monospaced accents.
- S-25 Aurora / mesh gradient / grainy gradient: blurred colour fields with noise grain.
- S-26 Bento grid: modular rounded tiles of mixed size, each a mini-story (popularised by Apple keynotes, adopted widely).
- S-27 Claymorphism / 3D clay: soft inflated 3D shapes, pastel, rounded.
- S-28 Isometric / low-poly 3D illustration.
- S-29 Organic / blob / fluid shapes; paper-cut layered depth; "kirigami".
- S-30 Hand-drawn / sketch / marker / doodle (human, informal, approachable).
- S-31 Collage / mixed media / cut-out photography with painterly overlays.
- S-32 Risograph / duotone print look with misregistration.
- S-33 Pixel art / 8-bit / dot-matrix / LED-display (also as a modern product aesthetic, e.g. dot-matrix on tech hardware brands).
- S-34 Technical / blueprint / schematic / data-sheet aesthetic: callouts, crosshairs, annotation lines, measurement ticks.
- S-35 Scientific illustration / natural-history plate / specimen-label style.
- S-36 Cartographic / atlas / topographic: contour lines, grid references, legend boxes.
- S-37 Cinematic / film title: letterbox, grain, anamorphic flare, big serif, slow dissolves.
- S-38 Kinetic typography-led: type as the main animated object.
- S-39 Immersive 3D / WebGL spectacle: full-viewport scenes, shaders, particles, camera moves on scroll.
- S-40 Generative / algorithmic art: noise fields, flow fields, L-systems, particle systems, reaction-diffusion.
- S-41 Data-humanism / data-art: charts as expressive drawings, hand-feel data.
- S-42 Scrollytelling / "visual essay": a long-form narrative where scroll drives graphics.
- S-43 Calm / wellness: soft gradients, rounded type, slow breathing motion, low contrast tone (watch accessibility).
- S-44 Gov-grade plain: maximum clarity, one column, high contrast, large type, no decoration (GOV.UK lineage).
- S-45 Modern serif revival / "literary tech": high-contrast display serifs on product sites, warm paper tones.
- S-46 Grotesque revival / big-sans: oversized neutral sans headlines, tight tracking.
- S-47 Retro-computing / terminal / TUI: monospace, box-drawing characters, green/amber on black.
- S-48 Memphis-meets-web "playful pop": bright flats, sticker shapes, rotated labels, emoji-adjacent.
- S-49 Sticker / label / stamp / ticket / receipt metaphors; wax seal and archival-document metaphors.
- S-50 "Analogue warmth" digital: paper textures, tape, handwritten notes, polaroids (use with restraint).
- S-51 Spatial / visionOS-style depth: floating panels, parallax layers, ornaments, hover glow.
- S-52 Ambient / "aura" UI: UI colour derived live from content (album art, image palette).
- S-53 Monochrome / duotone-only systems; single-hue systems; black-and-white + one spot colour.
- S-54 Ornamental revival: borders, flourishes, engraved frames, filigree (gold-on-dark, manuscript).
- S-55 Sacred / ceremonial geometry: mandala, sacred-geometry grids, concentric rings (fits ring-based concepts; easy to cliché).

#### B. Brand and studio design languages (what each is known for)

**Platform and system owners**
- B-01 Apple: huge confident type, product as hero, scroll-driven product reveals, bento grids, spring physics, Liquid Glass (2025), SF Pro with optical sizing, restraint with colour, accessibility settings respected. Pattern: *pinned sticky stage with scroll-scrubbed video or canvas*.
- B-02 Google Material 3 Expressive: dynamic colour from wallpaper, tonal palettes, bolder shapes, spring-based motion.
- B-03 Microsoft Fluent 2: acrylic/mica materials, rounded corners, clear iconography, cross-platform.
- B-04 IBM Carbon, Atlassian, Shopify Polaris, Salesforce Lightning: enterprise systems, density, tokens, documentation excellence.
- B-05 GOV.UK Design System / US Web Design System: accessibility benchmark, plain language, one-thing-per-page patterns, tested components.

**Product-design leaders (web)**
- B-06 Stripe: animated gradient hero, precise grids, clean docs layout, refined illustration, motion on interactive diagrams. Stripe Press: each book gets its own bespoke identity and typographic cover moment.
- B-07 Linear: dark UI, thin low-contrast borders, subtle glow, gradient text, tight grids, small precise motion, "crafted" feel.
- B-08 Vercel / Geist: black-and-white, grid lines, mono accents, sharp, developer-credible.
- B-09 Notion: warm minimal, illustration characters, serif accents for headlines, friendly.
- B-10 Figma: bold colour, playful illustration, confident big type, community-first.
- B-11 Airbnb: photography-led, rounded friendly UI, 3D illustrated icons (2022–24 relaunch), generous imagery.
- B-12 Spotify: bold duotone colour, huge type, Wrapped-style storytelling cards, ambient colour from album art.
- B-13 Nike / Adidas / Aesop-style retail: full-bleed photography, condensed bold type, editorial layouts, quiet-luxury restraint (Aesop: warm, typographic, literary).
- B-14 Arc / The Browser Company: playful colour, bespoke illustration, personality-forward product marketing.
- B-15 Framer, Webflow, Readymag, Squarespace showcase templates: contemporary landing-page grammar (hero, logo wall, bento, testimonial, CTA).
- B-16 Teenage Engineering and similar hardware-led brands: industrial grid, orange/gray palettes, mono labels, playful precision.
- B-17 Rive / Lottie-heavy product pages: character-driven interactive state machines.
- B-18 Superhuman, Raycast, Arc, Things: keyboard-first, speed as brand, command-palette idiom.
- B-19 Ableton, Native Instruments, Resident Advisor, Bandcamp, Pitchfork: music culture — technical-plus-expressive, strong type, tactile, scene-credible.
- B-20 A24, MUBI, Criterion, film-studio sites: cinematic, type-led, still-frame art direction.

**Editorial and storytelling**
- B-21 New York Times interactive / "Snow Fall" lineage; Guardian Visual Stories; Washington Post graphics: scroll-triggered full-bleed media, annotated charts.
- B-22 The Pudding, Reuters Graphics, Bloomberg Graphics, Financial Times Visual Journalism: data-driven scrollytelling, explanatory graphics.
- B-23 Aeon, The Marginalian, Quanta, Nautilus, Works in Progress: long-read typography, 60–70 character measure, restrained illustration, reading comfort.
- B-24 Bloomberg Businessweek print: loud typographic brutalism, collisions as intent.
- B-25 The Verge / Polygon / Vox: neon-on-black and loud colour blocks, tag-like labels.
- B-26 Wait But Why / explainer blogs: hand-drawn figures as the voice; long single-page arguments.
- B-27 Pentagram, Collins, Wolff Olins, Base Design, Studio Dumbar, Locomotive, Active Theory, Immersive Garden, Resn, Lusion, Makemepulse, Cuberto, Unseen Studio, Basic/Dept, Hello Monday, Merci Michel, Obys, Monopo: identity and award-winning web studios; browse their case studies for current state of the art in motion, WebGL, cursor, preloaders, kinetic type.

**Care, wellbeing and sensitive-topic services** (study for tone and safety patterns) [SAFE]
- B-28 Calm, Headspace: soft illustration, slow motion, reassurance; watch contrast and motion sickness.
- B-29 Domestic-abuse and crisis services (e.g. national hotlines, shelters, women's aid orgs): quick-exit button, neutral appearance, no tracking, plain language, safe-browsing guidance, discreet colours.
- B-30 Health systems (NHS digital service manual, CDC): clarity, plain language, evidence-linked, accessibility-first.
- B-31 Trauma-informed design guidance (SAMHSA principles; practitioner writing): safety, choice, collaboration, trust, empowerment, no surprise.

#### C. Award-site and contemporary web genres (as of 2025–26)

- G-01 Pinned-stage product storytelling (sticky canvas + scroll-scrubbed frames).
- G-02 Kinetic-type heroes: oversized headline splitting into letters/lines, masks, wipes, variable-font weight shifts.
- G-03 Full-bleed WebGL hero: shader gradient, fluid distortion, particle field, 3D object turning on scroll.
- G-04 Smooth-scroll + parallax + horizontal-scroll sections (Lenis/Locomotive-style inertia).
- G-05 Custom cursor and magnetic buttons (desktop only; no touch equivalent).
- G-06 Preloader sequences and page transitions (View Transitions API, curtain wipes).
- G-07 Bento and modular tile layouts with hover micro-interactions.
- G-08 Interactive diagrams / explorable explanations (Bret Victor lineage, Nicky Case).
- G-09 Marquee / ticker text, oversized footers, "mega" footers as brand moments.
- G-10 Text-as-image: cropped giant type masking video or photography.
- G-11 Variable and "living" fonts: weight/width/optical-size animated; fonts with built-in ornament.
- G-12 Grain, noise, halftone and film texture overlays on digital surfaces.
- G-13 AI-product aesthetics: soft gradients with glows, orbs, conversational UI, streaming text, "thinking" shimmer.
- G-14 Documentation-grade product sites: sidebars, command-K search, code blocks with copy, versioning.
- G-15 Anti-design / "ugly-on-purpose" and neo-brutalist portfolios.
- G-16 Scroll-driven CSS animation sites (native `animation-timeline`), view-transition navigation.
- G-17 Interactive maps and spatial navigation (map as primary navigation).
- G-18 Audio-reactive and sound-led experiences.
- G-19 Zine-style and print-inspired digital publications.
- G-20 Retro-OS / desktop-metaphor portfolios.

#### D. Cutting-edge ingredient shortlist (what is hot enough to consider; test each against the brief)

Liquid-glass surfaces; scroll-driven animations; view transitions; mesh and shader gradients; bento; variable fonts; dark-first systems with true light variant; oklch/P3 colour and `color-mix`; container queries; spring physics; blur-and-depth layering; generative backgrounds; kinetic type; cursor interactions; haptics on touch; micro-copy personality; ambient colour from content; 3D product turning; text-reveal masks; SVG filter effects (turbulence, displacement); canvas particle fields; audio-reactive visuals; "soft brutalism" hybrids.


---

## 02 Foundations: layout, type, colour, imagery, icons, surfaces

### 02 — Foundations: layout, type, colour, imagery, icons, surfaces, density, theming

#### L. Layout and structure
- L-01 Single column long-read (50–75 character measure).
- L-02 12-column grid; L-03 modular grid; L-04 baseline grid; L-05 asymmetric Swiss grid; L-06 broken/overlapping grid (intentional collision).
- L-07 Bento / tile mosaic; L-08 masonry; L-09 card grid; L-10 list/table (dense); L-11 split screen (50/50); L-12 sidebar + content; L-13 holy-grail (header, sidebar, content, footer); L-14 full-bleed sections with contained text; L-15 centered hero stack; L-16 poster layout (one big idea per screen); L-17 horizontal-scroll rail; L-18 carousel/deck; L-19 stacked cards (sticky stack); L-20 pinned stage with scrolling captions; L-21 timeline / vertical rail with nodes; L-22 radial / ring layout; L-23 map-as-layout; L-24 canvas / infinite pan-zoom; L-25 dashboard panels; L-26 magazine spread; L-27 sidenotes/marginalia (Tufte); L-28 table of contents rail; L-29 "one thing per page" (GOV.UK); L-30 sheet/drawer over content; L-31 center-stage focus with dimmed context.
- Spacing systems: 4px, 8px, modular scale, fluid `clamp()` spacing; vertical rhythm; optical alignment; safe areas; thumb zones; minimum tap target 44×44 px (Apple) / 48 dp (Material); max line length; gutter and margin tokens; container widths per breakpoint; aspect-ratio tokens.
- Breakpoint strategy: mobile-first; container queries; fluid type; orientation; foldables; large-screen (≥1920) and ultra-wide behaviour; print.
- Whitespace as design: density tiers (airy / comfortable / compact), and where each belongs.

#### T. Typography
**Classifications:** humanist sans; neo-grotesque; geometric sans; grotesque (Akzidenz-style); transitional serif; Didone / modern; old-style (Garamond-type); slab; blackletter; script (formal, casual, brush); monospaced; display / decorative; condensed; wide / extended; rounded; pixel / bitmap; variable (weight, width, slant, optical size, grade); colour fonts (COLR/SVG); ornament / dingbats; stencil; inline; handwritten; "ink-trap" grotesques; transitional-sans hybrids.
- T-01 Pairing strategies: serif display + neutral sans text; sans display + serif text; mono accent for labels; single superfamily across weights; contrast through scale not through many families (max two families).
- T-02 Scale systems: modular scale (1.2 minor third → 1.5 perfect fifth), fluid scale (`clamp`), dramatic hero scale (8–20 vw), fixed vs relative.
- T-03 Text treatments: tight display tracking (−2% to −5%), loose caps tracking (+8% to +30%), small caps, old-style numerals, tabular numerals for data, hanging punctuation, drop caps, pull quotes, marginal notes, running heads, footnote systems, end-notes, hyphenation, `text-wrap: balance/pretty`, ragged-right vs justified, optical margin alignment, ligatures, swashes, stylistic sets.
- T-04 Hierarchy tools: size, weight, colour, case, spacing, position, rule lines, numbering, labels, icons.
- T-05 Reading comfort: measure 45–75 characters, line-height 1.4–1.7 for text, ≥16 px base on mobile (prefer 17–19 for long reading), contrast ≥ 4.5:1 body, avoid pure-white-on-black long reading (use off-white, slightly reduce weight in dark mode), avoid light weights for small sizes, respect user font-size settings (rem).
- T-06 Kinetic and expressive type: per-letter/per-word reveal, variable-axis animation, text on a path, type masks over video, scroll-linked weight/width, text scramble/decode, marquee, 3D extruded type, outline/stroke type, text-as-texture. Always keep a static readable fallback and reduced-motion variant.
- T-07 Loading and fallback: self-hosted WOFF2 subsets, `font-display` strategy (swap vs optional), size-adjust fallback metrics to prevent layout shift, preload the primary face, limit to ≤ 4 files.
- T-08 Web-safe system stacks: San Francisco / Segoe UI Variable / Roboto / system-ui; "native feel" stack; serif system stacks (Charter, Iowan Old Style, Georgia).
- T-09 Voice in type: formal / literary / technical / playful / neutral / authoritative; match to content and reader state.
- Foundry and typeface lineages to explore (look up current releases; licences vary): Grilli Type, Klim, Commercial Type, Pangram Pangram, Displaay, Colophon, Dinamo, Sharp Type, Lineto, Production Type, ABC Dinamo, Collletttivo (open licence), Fontshare, Google Fonts (open licence, self-host allowed), Velvetyne (open), The League of Moveable Type (open), Open Foundry. Prefer open-licence families for self-hosting.

#### C. Colour
- C-01 Models: HSL/HSB, OKLCH/OKLab (perceptual; preferred for scales), Display-P3 wide gamut, CIELAB, sRGB; `color-mix()`, relative colour syntax, `light-dark()`.
- C-02 Schemes: monochrome; analogous; complementary; split-complementary; triadic; tetradic; neutral + one accent; duotone; tonal (Material) palettes; triad of semantic colours (success/warn/danger/info); gradient families; "earth/ink/paper" palettes; "neon on dark"; "pastel soft"; "high-key / low-key".
- C-03 Systems: design tokens (primitive → semantic → component); 10–12 step neutral scale; accent ramps; surface elevation tints in dark mode; border and divider opacity tokens; overlay and scrim tokens; focus ring token; selection and highlight tokens.
- C-04 Accessibility: WCAG 2.2 contrast (4.5:1 text, 3:1 large text and UI components); APCA as a guide not law; do not rely on colour alone; colour-blind safe palettes (check protanopia/deuteranopia/tritanopia); dark-mode contrast limits; forced-colors / high-contrast mode support.
- C-05 Theming: light, dark, auto (`prefers-color-scheme`), user override, high-contrast, reduced-transparency, "quiet/low-visibility" mode (for privacy-sensitive readers [SAFE]), time-of-day themes, content-derived accent (ambient).
- C-06 Meaning and culture: red (danger, urgency), gold (value, ceremony), green (safety, growth), blue (trust, calm), purple (spiritual, luxury), black (gravity, premium), warm cream (paper, humane), saturated neons (energy, nightlife). Check cultural variation and the reader's state; for crisis audiences prefer calm and non-alarming.
- C-07 Gradients: linear, radial, conic, mesh, noise-grain, animated gradient, text gradient, border gradient; banding avoidance (dither/noise).
- C-08 Rules of thumb: one accent; 60-30-10 distribution; reserve the strongest colour for the single most important action; avoid pure #000 / #fff backgrounds for long reading; test greyscale.

#### I. Imagery, illustration, iconography
- I-01 Photography: documentary; editorial portrait; still life; macro; aerial; architectural; cinematic film-still; archival/found; duotone-treated; cutout (background removed); grain-treated. Art-direction rules: consistent light, crop, colour grade.
- I-02 Illustration styles: flat vector; line art / monoline; hand-drawn ink; woodcut/linocut; watercolour; gouache; collage; paper-cut; 3D render; clay; isometric; low-poly; pixel; scientific plate; comic/panel; infographic icons; abstract geometric; generative; textural risograph; blueprints; botanical.
- I-03 Diagrams and figures: annotated figure; exploded view; cutaway; flow diagram; network graph; radial/sunburst; Sankey; chord; treemap; small multiples; timeline; map; matrix/heatmap; ring/orbit diagram; scatter field; isotype/pictogram; waffle; beeswarm; ridgeline; slope chart; stream graph.
- I-04 Iconography: outline (Lucide, Feather, Heroicons, Phosphor), filled, duotone, 3D, pictographic, hand-drawn, emoji-adjacent; stroke width consistency (1.5–2 px at 24 px), optical alignment, 24 px grid, labelled icons beat unlabelled ones. Inline SVG only in this repo [SC].
- I-05 Logo/brand marks: wordmark, monogram, emblem, seal, glyph system, responsive logo, animated logo; favicon and app-icon set; social card system.
- I-06 Patterns and textures: grain, halftone, grid, dots, topographic lines, hatching, paper fibre, noise, scanlines, mesh, moiré, guilloché, ornamental borders, tessellation.
- I-07 Image delivery: AVIF/WebP, responsive `srcset`, art-direction with `<picture>`, aspect-ratio boxes to prevent shift, blur-up/LQIP, lazy loading, SVG for line art, inlined critical imagery.
- I-08 Ethics: no real people's likeness without rights; label composites; avoid stereotyping; AI-generated imagery must be disclosed and rights-checked.

#### F. Surfaces, depth and effects
- F-01 Elevation systems: shadow scales (ambient + key), tonal elevation, border-only elevation, layered glass.
- F-02 Materials: paper, glass (blur + refraction + specular edge), metal, ink, stone, fabric, plastic, light/neon, smoke, water, foil, wax.
- F-03 Effects: backdrop blur, gradient glow, inner shadows, bevels, outlines, grain, vignette, chromatic aberration, halftone, duotone, displacement, bloom, glitch, scanlines, depth-of-field blur, parallax layers, reflections, caustics, refractive glass, lens flare.
- F-04 Shape language: sharp rectilinear; rounded (4–8 px, 12–16 px, pill); superellipse (squircle); organic blobs; hand-drawn wobble; circular/radial; diagonal cuts; notched/ticket edges.
- F-05 Borders and rules: hairline (0.5–1 px), double rule, dashed, dotted, offset hard shadow, gradient border, ornamental border.
- F-06 Density tiers and component sizing: airy / comfortable / compact; tap-target floor.
- F-07 Use-with-care effects: heavy blur (battery/GPU), animated filters on large areas, many overlapping transparencies (iOS paint cost), `backdrop-filter` stacking [IOS].
- Always provide: reduced-transparency and forced-colors fallbacks; solid-colour fallback where blur is unsupported.


---

## 03 Motion, interaction, navigation, components, feedback

### 03 — Motion, scroll storytelling, interaction, navigation, components, feedback

#### M. Motion
**Principles:** purpose (explain, orient, confirm, delight; never decorate without intent); continuity (objects keep identity across states); hierarchy (move the important thing first); causality (motion starts from the cause); restraint; consistency; interruptibility (user input always wins); performance (transform/opacity only on hot paths); accessibility (reduce, never remove meaning).
- M-01 Easing families: linear; ease-in/out/in-out; cubic-bezier custom (e.g. expo-out for entrances, quint-in for exits); spring (stiffness/damping/mass; critically-damped for UI, under-damped for playful); overshoot/back; elastic (rare); steps; `linear()` CSS multi-point curves that emulate springs and bounces.
- M-02 Timing guides: micro 100–200 ms; standard 200–350 ms; large/complex 350–600 ms; narrative sequences 600 ms–2 s; stagger 30–80 ms per item, cap total at ~600 ms; exits faster than entrances.
- M-03 Patterns: fade; slide; scale; mask/reveal (clip-path, wipe, iris); shared-element transition; morph (SVG path, FLIP); stagger; cascade; parallax (layers at different rates); pin-and-scrub; reveal-on-scroll; counter/odometer; typewriter/scramble; draw-on SVG stroke; skeleton shimmer; pulse/breathe; shake (error); bounce (success); ripple; magnetic pull; tilt/3D hover; marquee; crossfade between states; page transitions (View Transitions API); number tickers; progress/loader choreography; ambient idle motion (slow drift, breathing).
- M-04 Choreography: orchestrate who moves first (hierarchy), direction consistent with spatial model (new things enter from where they live), maintain object permanence, rhythm and beat across a sequence, "hold" frames (stillness for reading), settle times.
- M-05 Motion systems: duration/easing tokens; named recipes (enter, exit, emphasise, reorder, expand, shared, ambient); per-component specs; motion spec doc.
- M-06 Accessibility and comfort: `prefers-reduced-motion` (replace parallax/zoom/auto-play with fades or static); avoid flashing (>3/s), large parallax, spinning, scroll-jacking that disables native behaviour; vestibular triggers (zoom, large translations, rotating backgrounds); pause/stop for anything moving >5 s; no autoplay audio; scroll-linked motion must degrade to readable static.
- M-07 Tools: CSS transitions/animations; `@starting-style`; scroll-driven animations (`animation-timeline: scroll()/view()`); View Transitions API; Web Animations API; GSAP (+ScrollTrigger) [LIB]; Motion/Framer Motion [LIB]; Lenis smooth scroll [LIB]; Rive/Lottie [LIB, heavy]; Three.js/OGL/regl [LIB]; Canvas 2D; WebGL/WebGPU; SVG SMIL (limited). Prefer native first.

#### O. Scroll storytelling and long-form structure
- O-01 Pinned stage (sticky container) with scroll-scrubbed progress; O-02 scroll-triggered chapter swaps; O-03 horizontal pinned journeys; O-04 scrubbed video/frame-sequence (canvas) ; O-05 zoom-through / continuous camera move; O-06 layered parallax narrative; O-07 step-based "scrollama"-style (steps trigger figure states); O-08 reading-progress bar and chapter rail; O-09 end-of-chapter handoffs; O-10 "interludes" (full-screen pause moments, a single line, silence); O-11 act structure (open → build → turn → resolve → leave); O-12 sticky marginal figures beside text (desktop) vs interleaved figures (phone); O-13 anchored deep links per section; O-14 return-to-place memory without storage (hash + scroll restoration).
- Phone rules [IOS]: use `100svh/dvh/lvh`, not `100vh`; sticky inside overflow containers breaks; address-bar resize triggers; momentum scroll; avoid scroll-jacking; keep pinned stages ≤ one screen tall with captions in a separate safe zone; no text over busy figures without a solid or blurred scrim; never let a figure and text compete for the same pixels.

#### X. Interaction models and gestures
- X-01 Direct manipulation (drag, pinch, rotate); X-02 swipe (cards, sheets, dismiss); X-03 long-press menus; X-04 pull-to-refresh/reveal; X-05 bottom sheets (modal, non-modal, detents); X-06 drawers/side panels; X-07 popovers/tooltips (hover is not available on touch); X-08 command palette (Cmd/Ctrl-K); X-09 keyboard shortcuts (documented, discoverable); X-10 drag-and-drop with accessible alternatives; X-11 scrubbers/sliders; X-12 toggles/segmented controls; X-13 steppers; X-14 accordions/disclosure; X-15 tabs; X-16 carousels (use sparingly; provide controls and pause); X-17 filters/facets/sorting; X-18 live search with highlighting; X-19 multi-select/batch; X-20 undo/redo and soft delete; X-21 inline editing; X-22 hover/focus previews; X-23 cursor effects (desktop); X-24 gyro/tilt (permission-gated); X-25 voice (optional); X-26 haptics (Vibration API limited on iOS).
- Touch ergonomics: thumb-reach maps (primary actions lower third), ≥ 44 px targets with 8 px spacing, avoid edge-swipe conflicts with OS gestures (iOS back swipe), avoid hover-only affordances, make press state immediate (<100 ms), prevent accidental destructive taps.
- State model for every control: default, hover, focus-visible, active/pressed, disabled, loading, selected, error, success, empty.
- Feedback loop: acknowledge within 100 ms; show progress for >1 s; never lose user input; make recovery cheap.

#### N. Navigation and information architecture
- N-01 Global patterns: top bar; sticky/condensing header; hamburger/overflow (hides, use carefully); bottom tab bar (mobile); side rail; mega menu; command palette; breadcrumb; mini-map/rail (progress); table of contents; "you are here" highlighting; footer sitemap; skip links.
- N-02 Structure: hub-and-spoke; linear sequence; faceted collection; hierarchical tree; network (links between ideas); timeline; map; matrix; "paths" (curated journeys); search-first; chooser/wizard ("tell us where you are"); A–Z index; tag/topic cloud (use as an index, not decoration).
- N-03 Orientation devices: persistent title/context, progress indicators, prev/next with labels, section anchors, "back to where I was", scroll-spy, breadcrumbs for deep content, visible stage/chapter numbering, consistent labels.
- N-04 Findability: site search (instant, forgiving, synonyms, typo-tolerant), filters, related content, "what next" modules, consistent URLs, canonical, sitemap, structured data.
- N-05 Entry points: multiple doors for different reader states (in it now / worried about someone / curious / professional); "start here" chooser; returning-reader shortcuts.
- N-06 Exits and safety: Quick Exit (fixed, one tap, replaces history entry, keyboard shortcut) [SAFE]; leave-no-trace guidance; discreet title/favicon option [SAFE].
- N-07 Error and dead ends: helpful 404 with search and paths; broken-link handling; offline page.
- N-08 Cross-site continuity: shared header/footer idiom, shared tokens, "THE HOUSE" cross-project map, consistent transition language between intro and sub-site.

#### K. Components (inventory — cover states, sizes, density, themes for each)
Buttons (primary/secondary/tertiary/ghost/destructive/icon/FAB/split), links, inputs (text/area/number/date/time/file/OTP/search/password), selects/combobox/autocomplete, checkbox/radio/switch/slider/range, chips/tags/filters, badges/labels (e.g. credibility labels), cards (media/text/stat/link), lists, tables (sortable, sticky headers, responsive), accordions, tabs, modals/dialogs, sheets/drawers, popovers/tooltips/toasts/snackbars, banners/alerts/callouts/notices, menus/dropdowns/context menus, pagination/infinite scroll/load more, progress (bar/ring/steps), skeletons/spinners, avatars, breadcrumbs, steppers/wizards, calendars, carousels, galleries/lightbox, video/audio players, code blocks, quotes/pull-quotes/epigraphs, figures with captions, footnotes/marginalia, timelines, maps, charts, search dialogs, empty states, error states, onboarding tours/hints, feedback widgets, share/print/export affordances, cookie/consent (avoid when no cookies), language/theme switchers.

#### E. Feedback, sound and haptics
- E-01 Visual: state colour change, micro-motion, progress, toast, inline validation, success check draw-on, error shake (reduced-motion safe).
- E-02 Sound: UI sounds (opt-in, subtle, short); ambient/narration players (never autoplay; clear controls; captions/transcripts); audio-reactive visuals only after user gesture; mute persistence without cookies is limited (consider none).
- E-03 Haptics: tactile confirm on supported devices; never rely on it.
- E-04 Notifications: avoid pushing; if any, strictly opt-in and discreet [SAFE].


---

## 04 Experience, content, safety, accessibility, performance, evaluation

### 04 — Experience, content, safety, accessibility, performance, evaluation

#### P. Experience design and emotional tone
- P-01 Emotional registers to choose consciously: calm, awe, curiosity, gravity, warmth, urgency, play, intimacy, solemnity, defiance, relief, trust. Specify the intended feeling for each act or page, and what the reader should be able to *do* after.
- P-02 Reader state model: new/curious; engaged; overwhelmed; in danger; grieving; professional/skeptic; returning; skimming on a bus; reading at night in bed; sharing a device with someone unsafe. Design the default for the most vulnerable plausible reader.
- P-03 Mental models and metaphors: map, field guide, atlas, library, workshop, instrument, ritual, journey, house/rooms, deck of cards, ledger, lens. Pick one metaphor and keep it coherent through nav, language and motion.
- P-04 Pacing: opening moment (title, thesis, threshold), acts, interludes, payoffs, quiet endings, "leave the reader with a next step". Vary density: spectacle sections alternate with reading sections.
- P-05 Progressive disclosure: summary → detail → depth; three reading levels (quick / sequence / full); optional depth never blocks the main path.
- P-06 Agency and choice: reader chooses depth, order, theme, motion, audio; no forced modes; always reversible.
- P-07 Trust signals: sources, dates, method, versioning/changelog, authorship, limits ("what this is not"), honest labels (e.g. composite, depends on the terms, source checked), no false authority ("expert-reviewed" only if true).
- P-08 Shareability and keepsakes: share cards (OG images), printable one-pagers, copyable phrases, downloadable PDFs, deep links, citations.
- P-09 Delight, used sparingly: easter eggs, personality in microcopy, small rewards (not gamification where the content argues against it), well-made empty and loading states.
- P-10 Anti-patterns to avoid: dark patterns, nagging modals, autoplay, scroll-jacking that traps, infinite scroll without landmarks, hidden primary navigation, carousels hiding key content, text over busy imagery, tiny tap targets, mystery icons, cookie banners where none needed, fake urgency, fake scarcity, gamification that contradicts the subject.

#### V. Content design and voice
- V-01 Voice dimensions: formal↔casual; warm↔detached; plain↔literary; authoritative↔humble; urgent↔calm. State the voice in three adjectives and three "never" phrases.
- V-02 Plain language: short sentences, active voice, one idea per paragraph, define terms at first use, reading age target (e.g. grade 8–9 for public safety content), avoid jargon and idioms.
- V-03 Structure: scannable headings that carry meaning, lead with the point, numbered steps for procedures, tables for comparisons, callouts for safety and key terms, summaries at top for long pages.
- V-04 Microcopy: buttons as verbs, helpful errors (what happened, why, how to fix), placeholders as examples not labels, empty states that guide, confirmations that state what changed.
- V-05 Labels and taxonomy: consistent names for the same thing; a glossary; reading-time and update-date labels; chapter numbering.
- V-06 Tone for hard topics: describe patterns not people; name the harm without sensationalism; avoid blaming the reader; offer next steps and resources; content notes before distressing material; avoid graphic detail unless necessary.
- V-07 Localisation readiness: avoid text in images, allow 30–40% text expansion, RTL support, locale-aware dates and numbers, translated alt text.
- V-08 Alt text, captions, transcripts, audio description for every non-text asset; figure captions that state what the figure shows and why it matters.

#### Q. Safety, privacy and trauma-informed design [SAFE]
Applies to anything on coercive control, abuse, health, minors, or any reader who may be monitored.
- Q-01 Quick Exit: fixed, always visible, one tap/keyboard (Esc ×2 is a common idiom, declare it), navigates with `location.replace` to a neutral site so Back doesn't return; consider clearing in-page state; explain it once, neutrally.
- Q-02 Quiet default: neutral, low-visibility visual identity by default; bright or distinctive themes are opt-in; neutral `<title>` and favicon option; no revealing share previews by default.
- Q-03 No tracking/cookies/storage; no third-party calls (this repo already forbids) ; no push notifications; no accounts; no emailed reminders that could be seen.
- Q-04 Safe-browsing guidance page: private browsing, history, shared devices, clearing, "leave no trace" limits stated honestly.
- Q-05 Trauma-informed principles in UX: safety, trustworthiness, choice, collaboration, empowerment, cultural humility. Concretely: content notes before heavy content; user control over motion/audio/images; no surprise autoplay or sudden movement; clear exits from every state; gentle error language; no forced disclosure; no countdowns or urgency.
- Q-06 Crisis resources: visible, region-aware list; verified numbers; "if you are in immediate danger" line placed first on relevant pages; never claim the site is a substitute for help.
- Q-07 Minors: no interactions that collect data; age-appropriate language; reporting and help routes; separate audience-language rules per book (project rule: never change a book's own audience language).
- Q-08 Claims: no promise of safety, immunity or cure; "documented across", never "proved" unless proved; label composites; no named living people; patterns not people.

#### R. Accessibility (WCAG 2.2 AA minimum; aim for AAA where cheap)
- R-01 Perceivable: text alternatives; captions/transcripts; contrast 4.5:1 / 3:1; resize to 200% and 400% reflow; text spacing override; no information by colour alone; orientation not locked; `prefers-color-scheme`, `prefers-contrast`, `forced-colors`, `prefers-reduced-motion`, `prefers-reduced-transparency`, `prefers-reduced-data` honoured.
- R-02 Operable: full keyboard operation; visible `:focus-visible` rings (≥ 3:1, not clipped); logical focus order; skip links; no keyboard traps; target size ≥ 24×24 CSS px minimum (44 preferred); dragging has alternatives; no time limits or provide controls; pause/stop/hide for moving content; no flashing; focus not obscured by sticky headers (`scroll-padding`).
- R-03 Understandable: language attribute; consistent navigation and labels; predictable behaviour; error identification and suggestion; no unexpected context change.
- R-04 Robust: semantic HTML first; landmarks; headings in order; ARIA only to fill gaps; names/roles/values; live regions used sparingly; test with VoiceOver (iOS/macOS), TalkBack, NVDA.
- R-05 Cognitive accessibility: plain language, chunking, consistent patterns, minimal distractions, undo, clear progress, no memory demands.
- R-06 Testing: axe-core, Lighthouse a11y, keyboard-only pass, screen-reader pass, zoom pass, reduced-motion pass, high-contrast pass, grayscale pass, colour-blind simulation.

#### S. Performance and resilience (budgets; IDs PF-xx)
- PF-01 Targets (mid-range phone, throttled 4G): LCP ≤ 2.5 s (aim ≤ 1.5 s); CLS ≤ 0.1 (aim ~0); INP ≤ 200 ms; total initial transfer ≤ 200 KB for text pages (heavier for showcase pages, but progressive); JS ≤ 100 KB gzip initial where possible.
- PF-02 Tactics: inline critical CSS; defer non-critical; subset and preload fonts; responsive images; lazy-load below the fold; avoid layout thrash; `content-visibility: auto`; `will-change` sparingly; GPU-friendly animation (transform/opacity); cap particle counts and canvas resolution by device; pause offscreen animation (IntersectionObserver); frame-budget aware loops; 60 fps target, 30 fps graceful fallback.
- PF-03 Resilience: works without JS (readable content); works offline (self-contained); progressive enhancement; graceful WebGL → Canvas → static fallback; print stylesheet; low-power mode and `prefers-reduced-data` variants.
- PF-04 Device realism: test on a real iPhone (Safari) and a mid-range Android; account for address-bar collapse, safe areas, notch, dynamic island, keyboard overlays, landscape, text-size settings, battery saver.

#### T. Evaluation: how to critique a screen (use after every round)
Look at the screenshot, then answer in writing:
1. **First 3 seconds:** what is this, whose is it, what do I do? Cover the logo: could it belong to anyone?
2. **Hierarchy:** one clear focal point? Does the eye path follow intent?
3. **Type:** scale contrast, measure, leading, weight discipline, orphans/widows, fallback flash.
4. **Space:** rhythm, alignment to grid, dead zones, crowding, collisions (text over figure, label over text, anything under a sticky header).
5. **Colour:** accent discipline, contrast, dark/light parity, greyscale test.
6. **Imagery/figures:** compositional focus, quality at 2×/3×, consistency of style.
7. **Motion:** purpose per animation, timing, interruptibility, reduced-motion plan, jank on a throttled CPU.
8. **Interaction:** all states present, targets, one-handed reach, gesture conflicts.
9. **Navigation:** can I tell where I am, go back, leave, find something specific?
10. **Content:** is every line necessary, true, kind, plain? Are safety lines present and first where required?
11. **Craft details:** pixel snapping, icon alignment, consistent radii, focus rings, selection colour, scrollbar styling, overscroll, favicon, tab title, social card, 404, print.
12. **Delight vs noise:** what would a ruthless art director cut?
Automated gates (necessary, not sufficient): axe, console errors, overflow at 375/1440, nothing stuck at opacity 0, reduced-motion run, bounding-box overlap checks between figure stage and text, Lighthouse, real-phone checklist.


---

## 05 Techniques (web platform and tools, rated for this repo)

### 05 — Techniques (web platform and tools), rated for this repo

Rating: **[SC]** native/self-contained; **[LIB]** copy a local library file; **[NET]** needs network at run time (not allowed). Support notes are as of mid-2026 knowledge; check caniuse and test on iOS Safari. **[IOS]** marks known iOS caveats.

#### Native CSS (preferred)
- Custom properties and design tokens; `@layer`; `@scope`; nesting; `:has()`; `:is()/:where()`; container queries and units; `clamp()/min()/max()` fluid sizing; `aspect-ratio`; logical properties; subgrid; `grid` / `flex` / `gap`; `inset`; `dvh/svh/lvh` units [IOS]; `env(safe-area-inset-*)` [IOS]; `scroll-snap`; `scroll-padding/margin`; `overscroll-behavior`; `position: sticky` [IOS pitfalls inside overflow]; `text-wrap: balance/pretty`; `hanging-punctuation` (Safari); `font-variant-*`, `font-optical-sizing`, `font-variation-settings`; `font-size-adjust`; `size-adjust` & `ascent-override` for fallback metrics; `color-mix()`, relative colour syntax, `oklch()`, `display-p3`; `light-dark()`; `accent-color`; `field-sizing`; `@starting-style`; `transition-behavior: allow-discrete`; `linear()` easing; `animation-timeline: scroll()/view()` and `animation-range` (Chromium; check Safari) [IOS]; View Transitions API (same-document widely; cross-document check support); `@property` typed custom properties for animatable gradients; `clip-path`, `mask`, `mask-image` (with `-webkit-` prefix) [IOS]; `mix-blend-mode`, `isolation`; `filter`, `backdrop-filter` (needs `-webkit-` prefix; costly) [IOS]; `contain`, `content-visibility`; `@media (prefers-reduced-motion | prefers-color-scheme | prefers-contrast | prefers-reduced-transparency | forced-colors | hover | pointer | any-pointer | orientation | display-mode)`; `@supports`; `::selection`, `::marker`, `::backdrop`, `::view-transition-*`; popover API and `<dialog>`; `interpolate-size` (check); anchor positioning (check support).
#### Native JS / platform APIs
IntersectionObserver; ResizeObserver; `requestAnimationFrame` loops with delta-time; Web Animations API; Pointer Events (unify mouse/touch/pen) with `touch-action`; Visual Viewport API [IOS keyboard]; Page Visibility; `matchMedia` for preference queries; Clipboard (user-gesture); Web Share (mobile); Fullscreen; Screen Wake Lock (reading mode); Web Audio (after gesture); Media Session; Intl (dates, numbers, plurals, list formatting, segmenter); History API with `location.replace` for exits; `inert` attribute; `AbortController`; Service Worker for offline (caution: caching bugs); `structuredClone`; `navigator.vibrate` (not iOS).
#### SVG
Inline SVG icons and figures; `<use>` sprites; stroke-draw animation (`stroke-dasharray/offset`); `<mask>`/`<clipPath>`; gradients and patterns; filters (`feTurbulence` grain, `feDisplacementMap` distortion, `feGaussianBlur` glow, `feColorMatrix`); path morphing (matching point counts); text on path; SMIL (limited; prefer CSS/JS); generate figures from data at build time (as already done for the logo).
#### Canvas 2D and WebGL
- Canvas 2D: particle fields, flow fields, hand-drawn effects, image sequences scrubbed by scroll; cap resolution by `devicePixelRatio` and device class; offscreen canvases; `OffscreenCanvas` where supported.
- WebGL/WebGL2: shader backgrounds (gradients, fluid, noise), instanced points (tens of thousands), 3D objects; write minimal raw WebGL or vendor a tiny helper [LIB] (OGL ~ small; regl; Three.js is large); always provide a Canvas 2D or static fallback; test context-loss; iOS memory limits [IOS].
- WebGPU: emerging; feature-detect; do not require.
- Shaders to know: value/simplex/curl noise, fbm, domain warping, metaballs, voronoi, reaction-diffusion, signed-distance-field text, chromatic aberration, bloom approximation, grain, dithering, halftone, displacement by mouse/scroll.
#### Libraries (only as local copies; state licence and size) [LIB]
GSAP + ScrollTrigger (free, widely used; check current licence terms before bundling); Lenis (smooth scroll; weigh against native scroll feel and a11y); Motion (Framer Motion's vanilla core); Anime.js; Lottie/dotLottie and Rive (runtime weight); Three.js / OGL / regl / PixiJS; D3 (modules like d3-scale, d3-shape, d3-force; modular and tree-shakeable); Observable Plot; Scrollama; Splitting.js/SplitType (text splitting); Fuse.js / MiniSearch / Lunr (client search; MiniSearch is small); Floating UI (positioning); Tippy; Swiper (carousels; heavy); Howler (audio). Always ask: can native do this in 30 lines?
#### Fonts and type tech
Self-host WOFF2; subset with `pyftsubset`/`glyphhanger`; variable fonts (axes: wght, wdth, opsz, slnt, ital, custom); `unicode-range` splits; preload; `font-display: swap|optional` tradeoffs; metric-matched fallbacks; OpenType features (`liga`, `calt`, `ss01..`, `onum`, `tnum`, `smcp`, `swsh`, `case`, `zero`); COLRv1 colour fonts; text shaping for non-Latin scripts; avoid faux bold/italic (load real styles).
#### Media
Video: H.264 + HEVC/AV1 where supported, `playsinline muted loop` for ambient, poster images, `preload="none"`, no autoplay with sound; frame-sequence alternative (WebP/AVIF sequence) for scrubbing; audio: AAC/MP3 with captions and transcript; lazy loading; `loading="lazy"` and `decoding="async"` for images; `fetchpriority="high"` on the LCP image.
#### Build and tooling
Static generators in Python/Node (as in this repo); design tokens as a single source (CSS custom properties generated from JSON); visual regression via Playwright screenshot diffs; automated overlap tests (bounding-box intersections); axe-core; Lighthouse CI; font subsetting scripts; image pipelines (sharp, squoosh-cli); link checkers; HTML validators; size budgets in CI.
#### Design tooling (for exploration, not source of truth)
Figma (boards, comps), Canva (quick mood boards), image generators for mood only, Playwright screenshots of real references, Awwwards/Godly/Mobbin/Page Flows for reference browsing, Typewolf/Fonts In Use for type, Coolors/Huetone/oklch.com for colour, Realtime Colors, Contrast checkers (WebAIM, APCA), Stark/colour-blindness simulators.

#### Known iOS Safari pitfalls checklist [IOS]
`100vh` vs dynamic toolbar → use `svh/dvh`; `position: fixed` + keyboard; sticky inside transformed/overflow parents; `backdrop-filter` needs `-webkit-`; `mask` needs `-webkit-`; `100vw` includes scrollbars (not on iOS, but desktop); rubber-band overscroll revealing background; tap highlight colour; 300 ms delay gone but `touch-action` matters; autoplay restrictions; audio unlock on gesture; `input` zoom if font-size < 16 px; safe-area insets for notch/home indicator; scroll-linked animations support lags; WebGL memory and context loss; `scroll-behavior: smooth` inconsistencies; `position: sticky` + `transform` bugs; viewport-meta `viewport-fit=cover`; PWA display-mode differences.


---

## 06 Master names bible (everything that exists, by name)

### 06 — The master names bible (everything that exists, by name)

**Purpose.** A pure vocabulary: the names of styles, techniques, patterns, effects, components, structures, principles and resources used by top-tier sites and scroll pages. It exists so a designer (human or AI) can *see what is possible* and then look up, search for, screenshot and borrow from each thing by its name. It is deliberately not curated or ranked. Selection happens afterwards using `00-README.md`.

**How to use it.** Read every category once. For a job, circle 5–15 names per relevant category, then search each name (Awwwards, Codrops, CodePen, Godly, Mobbin, MDN) to see real examples and code, and screenshot the best. Cite names in your design direction.

**Honest limits.** Compiled from knowledge to mid-2026 plus a short search in Nov 2026 (sources at the end). It is long but not literally complete; the field invents names constantly. Add to it. Glosses are one-liners to identify the thing, not tutorials. `[SC]` = doable with native HTML/CSS/JS/SVG; `[LIB]` = normally uses a library; `[GPU]` = needs WebGL/WebGPU/canvas power; `[DESK]` = desktop-only (needs hover/cursor); `[IOS]` = test carefully on iPhone.

---

#### 1. Kinds of sites and pages (genres)
Marketing/landing page; product page; brand site; campaign microsite; launch site; portfolio (designer, developer, photographer, architect, artist); agency site; studio site; case study page; editorial/magazine; long-read/feature; visual essay; scrollytelling piece; interactive documentary; explorable explanation; data story; newsletter archive; blog; documentation site; API reference; changelog/release notes page; roadmap page; pricing page; comparison page; about/manifesto page; team page; careers page; press kit; media kit; annual report microsite; impact report; ESG report; event/festival site; conference site; ticketing page; album/music-release microsite; artist EPK; film/series promo site; game site; app store-style product tour; hardware product launch page; automotive configurator; fashion lookbook; e-commerce storefront; PDP (product detail page); collection/lookbook page; checkout flow; cart drawer; membership/club site; community hub; forum; wiki; encyclopedia; atlas/map site; museum/collection site; archive site; digital exhibition; virtual gallery; online course/lesson page; reference tool; calculator/tool page; configurator; quiz/assessment; wizard/chooser; dashboard; admin; status page; 404/error page; offline page; "coming soon"/waitlist page; one-pager; zine-style site; book companion site; reading app; field guide; playbook; checklist page; printable resource page; resource hub; library/catalogue; directory; marketplace; social feed; profile page; link-in-bio page; donation page; petition/campaign page; crisis/help-service site; public-service site.

#### 2. Landing-page anatomy (section names)
Announcement bar; header/nav; hero; sub-hero; logo wall / trust bar; social proof strip; metrics/stats band; feature grid; bento features; feature deep-dive (alternating rows); product tour; interactive demo; use-case tabs; integrations grid; comparison table; testimonial wall; testimonial carousel; case-study cards; press quotes; awards row; pricing table; pricing toggle; FAQ accordion; objection handling; how-it-works steps; timeline; roadmap; team; founder letter; manifesto; values; mission band; gallery; showreel; video section; download/app badges; newsletter signup; contact form; CTA band; mega footer; sitemap footer; legal row; back-to-top; cookie/consent bar (avoid if no cookies); chat widget; exit-intent modal (avoid); sticky CTA bar; progress/chapter rail; "scroll for more" cue; marquee band; giant wordmark footer; easter-egg section.

#### 3. Hero types
Typographic hero (type only); oversized headline hero; split-screen hero; full-bleed image hero; full-bleed video hero; looping-background-video hero; product-render hero (3D turntable); WebGL scene hero; shader-gradient hero; particle-field hero; interactive-cursor hero; pinned scroll-scrubbed hero; zoom-through hero; masked-video-in-text hero; image-trail hero (cursor leaves image trail) [DESK]; marquee hero; collage hero; sticker/cutout hero; illustration hero; animated-diagram hero; app-screenshot hero in device frame; floating UI cards hero; dashboard-preview hero; search-box hero; configurator hero; countdown hero; story-opening/“title card” hero; quiet-text hero with slow fade; horizontal-scroll hero; preloader-into-hero reveal; split-letter reveal hero; curtain-open hero; split-door hero; lens/spotlight hero (follows cursor) [DESK]; time-of-day aware hero; map hero; audio-reactive hero; 3D scroll-through-a-world hero.

#### 4. Navigation and header patterns
Fixed header; sticky header; condensing header (shrinks on scroll); hide-on-scroll-down/show-on-scroll-up; transparent-to-solid header; floating pill nav (centered capsule); dock nav (macOS-style magnification); full-screen overlay menu; side-drawer menu; slide-over menu; mega menu; hover-dropdown; click-dropdown; split nav (logo center); vertical side nav (fixed rail); bottom tab bar; floating action button; command palette (Cmd-K); search-first nav; sticky section anchors / scroll-spy; breadcrumb; table-of-contents rail; progress bar nav; dot/step indicator nav (side dots); chapter slider; number-index nav (01 02 03); mini-map nav; radial/circular nav; menu-morph (hamburger to X); text-swap hover on nav items (roll-over text); "menu" word button; language/theme switchers; skip link; quick-exit button (safety sites).

#### 5. Footer patterns
Mega footer; minimal footer; giant wordmark footer; footer reveal (content slides up to reveal footer beneath, "curtain footer"); footer with live local time; footer with CTA band; footer sitemap grid; footer newsletter; footer marquee; footer easter egg; sticky footer; footer with legal line and version/update note.

#### 6. Layout structures and compositions
Single column; two-column; split screen; asymmetric grid; 12-column; modular grid; baseline grid; Swiss grid; bento grid; masonry; card grid; list view; table view; magazine spread; broken grid; overlapping layers; diagonal sections; sticky split (one side pins, other scrolls); pinned stage; horizontal scroll track; carousel/slider; filmstrip; stacked sticky cards; accordion stack; tabbed panels; sidebar + content; holy grail; dashboard grid; radial layout; orbit layout; circular menu layout; spiral layout; map layout; infinite canvas (pan/zoom board); node graph layout; timeline (vertical/horizontal); floating islands; collage/scrapbook layout; poster layout; full-bleed sections; contained text on full-bleed; centered-hero stack; left-aligned editorial; marginalia/sidenotes (Tufte); drop-in figure with caption; offset/staggered grid; "column-count" flow; sticky headings in long tables; parallax columns (columns scrolling at different speeds); scroll-snapping sections; viewport-height sections ("100svh" panels); "slide-deck" web; "stack of cards" mobile; dual-axis layout.

#### 7. Scroll techniques and scroll-linked effects
Smooth scrolling / inertia (Lenis, Locomotive); native scroll with scroll-driven CSS (`animation-timeline: scroll()/view()`) [SC]; scroll-triggered reveals (fade, slide, clip, scale); staggered reveals; scroll-scrubbing (animation progress tied to scroll position); pinning (`position: sticky`/ScrollTrigger pin); parallax (multi-layer, background, mouse-parallax); horizontal scrolling inside vertical scroll; scroll-snap (mandatory/proximity); scroll hijacking (taking over scroll; usually avoid); scroll-jacked slide decks (avoid for a11y); scroll-linked video scrubbing / frame sequences on canvas; scroll-linked 3D camera path; scroll-driven number counters; scroll-driven color/theme changes (background shifts per section); scroll-driven text highlight (words light up as read); scroll-progress bars; scroll-spy; scroll-triggered sound (opt-in); scroll-velocity effects (skew/stretch by speed); infinite scroll; infinite loop scroll (seamless wraparound); scroll-to-zoom; scroll-through-portal; scroll-driven morph; scroll-driven path drawing (SVG stroke); scroll-driven mask reveal; scroll-driven sticky stack ("card stacking"); scroll-timeline named timelines; scroll-driven `view()` ranges (entry/exit/cover/contain); overscroll effects; scroll hints (mouse icon, chevron); "scrollytelling" step triggers (Scrollama-style); anchor-jump smooth scroll; scroll restoration; scroll-padding for sticky headers.

#### 8. Page transitions and navigation transitions
Fade/crossfade; slide; push; curtain wipe; clip-path wipe; iris/circle reveal; SVG-mask reveal; blind/stripe transition (grid or blinds patterns); image-expand shared-element transition (thumbnail grows into hero); morph transition; text-slide transition; counter-wipe; overlay panel; persistent-scene transition (one WebGL/WebGPU scene persists while DOM pages swap, driven by a router such as Barba.js or a tiny custom router); shader-mix transition (blend two textures by a uniform); displacement-map transition; pixelate/dissolve transition; View Transitions API (same-document and cross-document) [SC]; FLIP technique (First-Last-Invert-Play); route preloading; skeleton-state transitions; "loading counter" transition; page-peel; door/split transition; cover-then-uncover (loader as transition).

#### 9. Preloaders and loading states
Percentage counter; progress bar; logo draw-on; logo morph; split-text intro; curtain intro; counting-up to 100 then reveal; asset-weighted real progress; skeleton screens; shimmer; blur-up/LQIP image loading; progressive JPEG/AVIF; spinner (minimal); looping brand animation; typewriter loader; "enter" button gate (doubles as audio-unlock); intro film; no-preloader (fast sites; often best).

#### 10. Text and typography effects
Split text (by chars/words/lines); staggered letter reveal; line mask reveal (text slides up from clipped line); word-by-word highlight on scroll; text scramble / decode; typewriter; marquee/ticker; infinite marquee with direction change on scroll; variable-font weight/width animation; font-axis hover; text on a path; curved text; circular text; outlined/stroke text; filled-on-hover outline; gradient text; animated gradient text; clipped-image text (image/video fill in letters); mix-blend text; text with distortion (displacement/wave); liquid text; magnetic text; hover letter-swap (roll-over); odometer/slot-machine counters; kinetic type grids; stretched/squashed type (scale-Y/X); giant background type; vertical type; rotated labels; text stacking; underline draw-on; strike-through reveal; highlight-marker effect; blinking cursor; text shadow glow; 3D extruded text; reflective/chrome text; glitch text; split-flap/airport board; LED/dot-matrix text; ASCII art text; bitmap/pixel font; ransom-note type; collage type; font mixing within a word; ligature play; drop caps; initial-cap illuminated letters; pull quotes; epigraphs; footnotes/sidenotes; small caps; tabular numerals; hanging punctuation; optical sizing; `text-wrap: balance/pretty`; tracking-in/out; leading-compress headline (tight lines); type scale jump (hero at 15vw); "type as UI" (words as buttons); fluid type with `clamp()`.

#### 11. Typeface and typesetting vocabulary
Neo-grotesque; grotesque; geometric sans; humanist sans; rounded sans; mono; slab; transitional serif; Didone; old-style; Scotch; Clarendon; wedge serif; blackletter; script; brush script; display; condensed; extended; ink-trap; stencil; pixel; variable; colour font; optical-size family; text vs display cuts; superfamily; "grotesk + serif" pairing; "mono accent" pairing; all-serif editorial; all-sans product; oversized-numerals style; tracking scale; baseline grid; vertical rhythm; measure; leading; kerning; ligatures; alternates; swashes; stylistic sets; small caps; figures (lining/old-style/tabular/proportional); case (all caps, small caps, title, sentence); rag; justified with hyphenation; hanging indent; widows/orphans; river; rule lines; ornaments/dingbats.

#### 12. Cursor and pointer effects [DESK]
Custom cursor (dot, ring, blob); cursor follower with lag; magnetic cursor (snaps to buttons); cursor label ("view", "drag", "play"); cursor blend-mode (difference/invert); cursor trail; image trail; spotlight/flashlight reveal; cursor-reactive particles; cursor distortion on image (liquid, ripple); cursor-driven parallax; cursor-driven 3D tilt; hover-to-preview; drag cursor on sliders; cursor scale on hover; cursor hide on text; touch alternative (tap states) required.

#### 13. Hover and interaction effects (links, buttons, cards, images)
Underline slide/draw; text roll-over swap; fill sweep; circle expand from pointer; magnetic pull; ripple; glow follow (radial gradient follows pointer on card); border-gradient sweep; spotlight card; 3D tilt (vanilla-tilt style); shadow lift; scale/zoom; image zoom inside frame; grayscale-to-colour; RGB split; duotone swap; image reveal on hover (list rows reveal image); row-expand; accordion hover; arrow slide; arrow diagonal swap; icon morph; label slide; blur-others (dim siblings); stretch/squish; elastic; shine/sheen sweep; border-draw; shadow-drop offset (neo-brutalist press); press-down; focus ring animation; `:hover` only on `(hover: hover)` devices.

#### 14. Buttons and calls to action
Primary solid; secondary outline; ghost/text; pill; capsule; rounded-rect; sharp-corner; icon button; split button; FAB; gradient button; glow button; glass button; neo-brutalist button (hard border + offset shadow); 3D pressable button; liquid button; magnetic button [DESK]; arrow button; label-roll button; loading-state button; success-morph button (turns into a check); toggle button; segmented control; swipe-to-confirm; hold-to-confirm; sticky mobile CTA bar; inline text CTA; CTA band; floating chat/help button.

#### 15. Imagery, photography and art direction
Documentary; editorial portrait; still life; macro; aerial; architectural; fashion; product cutout; floating product; flat-lay; film still; archival/found image; duotone; tritone; halftone; grain-treated; high-contrast black-and-white; colour-graded; double exposure; collage cutouts; sticker cutouts; mixed media (photo + drawing); rotoscope; stock-avoiding custom shoots; moodboard-driven art direction; consistent crop/aspect language; full-bleed; framed/matted; polaroid/contact-sheet; film-strip; split-tone; lens flare; depth-of-field blur; tilt-shift; long-exposure; light-leak; scan/photocopy texture; AI-generated imagery (rights/disclosure; avoid uncanny).

#### 16. Image presentation effects
Reveal on scroll (clip, mask, curtain); parallax inside frame; ken-burns; zoom-on-hover; image distortion on hover/scroll (WebGL displacement) [GPU]; ripple/liquid image; image-trail; image sequences; image sliders (fade, slide, coverflow, 3D carousel, stacked, "fan" cards); lightbox; image-to-page expand; gallery grids (justified, masonry, mosaic, bento); horizontal gallery; infinite gallery (drag in 2D) [GPU]; image roll/cylinder; image tunnel; blur-up; LQIP; progressive; shared-element hero; before/after slider; hotspot annotations; zoom/pan; magnifier lens; 360 spin; contact sheet; mosaic assembly.

#### 17. Video and motion media
Ambient background loop (muted, playsinline); scroll-scrubbed video; frame-sequence on canvas; masked video in shapes/text; video hover-play; video modal; video chapter markers; looping cinemagraph; transparent video (WebM alpha / HEVC alpha); Lottie/dotLottie animation; Rive interactive animation; animated SVG; animated WebP/AVIF; GIF (avoid; use video); live camera/mic (permission); picture-in-picture; showreel hero; interactive film (choose-your-path); audio-visual loop; kinetic motion graphics.

#### 18. 3D, WebGL, WebGPU and shader effects [GPU]
Three.js scene; React Three Fiber; Babylon.js; OGL (small WebGL lib); regl; PixiJS; Spline embeds; Rive; model-viewer; WebGPU; TSL (Three Shading Language); GLTF/GLB models; Draco/meshopt compression; KTX2 textures; HDRI environment lighting; PBR materials; physically based glass; refractive glass / transmission; iridescence; chrome/metal; frosted glass; subsurface scatter fake; fresnel rim light; matcap; toon/cel shading; outline shader; wireframe; point clouds; instanced meshes (thousands of objects); particles (GPU particles, FBO particles); flow fields; curl noise; simplex/perlin/value noise; fbm (fractal Brownian motion); domain warping; voronoi/worley; reaction-diffusion; metaballs; raymarching / signed distance fields; volumetric light / god rays; fog and haze; bloom; glow; chromatic aberration; depth of field; motion blur; film grain; vignette; CRT/scanline; dithering (ordered, blue-noise); halftone shader; pixelation; ASCII shader; kaleidoscope; mirror/tiling; fluid simulation (Navier–Stokes); smoke; ink in water; displacement maps; ripple/wave; water surface; caustics; shader gradients (animated mesh/noise gradients); gradient blobs; liquid metal; magnetic field lines; grid distortion (warping grid); cloth; soft-body; physics (Cannon/Rapier/Matter.js); ragdoll toys; 3D text; 3D scroll-through tunnel; camera paths (spline) on scroll; orbit controls; parallax camera by pointer/gyro; portal/window effect; render targets and post-processing passes (EffectComposer); persistent scene across pages; scroll-synced uniforms (a single uniform driven by GSAP); texture-mix transitions; hover-distortion planes (images as WebGL planes synced to DOM); DOM-to-WebGL syncing; "gooey" SVG filter (metaball effect without WebGL) [SC]; SVG turbulence/displacement filters [SC]; CSS paint/houdini effects (limited).

#### 19. Backgrounds and ambient effects
Mesh gradient; aurora gradient; animated gradient; noise gradient with grain; radial glows; spotlight; grid lines (fading grid); dot grid; isometric grid; topographic lines; contour map; halftone; scanlines; starfield; nebula; particles; floating shapes; floating orbs/blobs; bokeh; light rays; lens flares; waves; liquid distortion; film grain overlay; paper fibre; concrete; marble; fabric; wood; metal; glass blur; "frosted" panels; animated SVG patterns; Perlin-noise ink; pixel-sorting; glitch; blueprint grid; constellation lines (connecting particles); fireflies; rain/snow/dust; smoke; heat haze; parallax layers; video loops; code-rain; maps as backgrounds; photographic blur backdrop; ambient colour derived from current content (album-art style).

#### 20. Gradients, colour and light
Linear; radial; conic; mesh; noise-grain; animated; text gradient; border gradient; gradient mask; gradient mapping; duotone; tritone; glow; neon; bloom; halation; chromatic fringe; iridescent/holographic; pearlescent; metallic gradient (gold, chrome, silver); sunset/aurora palettes; "dopamine" colour; earthy/natural palette; quiet luxury neutrals; jewel tones; pastel; monochrome; two-colour; black + one accent; paper + ink; candy; terminal green/amber; acid/neon accent on dark; high-key; low-key; tonal palette (Material); OKLCH ramps; P3 wide-gamut; `color-mix()`; `light-dark()`; harmony types (complementary, analogous, triadic, split-complementary, tetradic, monochromatic); dark mode; high-contrast mode; forced-colors; quiet/low-visibility mode; contextual theming (time of day, content-derived).

#### 21. Surfaces, materials and depth
Flat; soft shadow; layered shadow; hard offset shadow (neo-brutalism); inner shadow; neumorphism (avoid for contrast); glassmorphism; Liquid Glass (Apple 2025: translucent, light-responsive, refractive layers); frosted glass; acrylic/mica (Fluent); paper; cardboard; wax seal; leather; metal; ceramic; fabric; plastic; "tactile brutalism" (chunky borders, tactile textures, physical feel); clay/3D soft; embossed/debossed; gradient borders; sheen; specular highlights; bevel; stroke outlines; backdrop blur layers; depth stacking; z-axis parallax; floating cards; spatial/visionOS depth (ornaments, hover glow, layered panels); elevation scales; surface tint; scrims; vignettes.

#### 22. Shapes, masks and geometry
Rounded rectangle; squircle (superellipse); pill; circle; blob; organic; polygon; diagonal cut; notched/ticket; scalloped/wavy edge; torn paper edge; stamp edge; arches; sacred geometry; concentric rings; orbits; spirals; fractals; tessellation; Truchet tiles; Voronoi cells; hex grids; clip-path shapes; CSS shape(); SVG masks; blend-mode masks; text masks; gradient masks; morphing paths; stroke-dash drawing; guilloché patterns; ornament borders; frames/matting; brackets/crop marks; registration marks; crosshairs; measurement ticks; callout lines; leader lines; arrows (hand-drawn, technical).

#### 23. Illustration and icon styles
Flat vector; monoline; duotone; outline; filled; glyph; 3D icon; isometric; low-poly; clay; claymorphism; pixel; hand-drawn/sketch; marker/doodle; ink/woodcut/linocut; engraving/etching; watercolour; gouache; paper-cut; collage; cut-out; risograph; comic/panel; zine; scientific plate; botanical; anatomical; blueprint/patent drawing; map/atlas; infographic pictograms; isotype; abstract geometric; generative; mascot/character; sticker; emoji-adjacent; icon sets (Lucide, Feather, Phosphor, Heroicons, Tabler, Material Symbols, SF Symbols); icon animation (draw-on, morph, bounce); animated stickers; illustration systems (consistent stroke, palette, perspective).

#### 24. Data visualisation and figures
Bar; line; area; stacked; scatter; bubble; heatmap; calendar heatmap; treemap; sunburst; radial/ring; chord; Sankey; alluvial; network/force graph; arc diagram; dendrogram; tree; flow chart; org chart; timeline; Gantt; gauge; radar/spider; parallel coordinates; small multiples; ridgeline; violin; box; beeswarm; strip plot; waffle; isotype/pictogram; dot matrix; slope chart; dumbbell; lollipop; bump chart; streamgraph; horizon chart; cartogram; choropleth; hex-bin map; flow map; proportional-symbol map; contour map; 3D terrain; globe; annotated charts; scrollytelling charts (step-triggered states); explorable explanations; interactive filters; brushing & linking; tooltips; direct labelling; sparklines; ring/orbit diagrams; field/particle visualisations (each point = a data item); generative data art ("data humanism"); hand-drawn data; unit charts (one icon = one thing); "counting-up" hero stats; comparison sliders.

#### 25. Maps and spatial navigation
Interactive map as navigation; map with story steps (fly-to on scroll); globe (Three.js/Mapbox/Globe.gl); vector tiles; stylised/custom map styles; atlas plates; topographic; heat map overlay; route lines animated; isometric city; floor plans; star charts; mind-map; constellation navigation; concept map; ring map; node-link map of ideas; zoomable-canvas map (Figma-like); mini-map; "you are here".

#### 26. Microinteractions and feedback
Button press; toggle slide; checkbox draw; like/heart burst; success check draw; error shake; field validation pulse; copy-to-clipboard confirm; tooltip pop; toast slide; skeleton shimmer; pull-to-refresh; swipe actions; reorder drag; haptic tap; pop-in; counter tick; progress fill; loading dots; breathing pulse (idle); hover-to-wake; "peek" affordances; spring overshoot; rubber-band; snap-to-grid; magnetic snap; long-press hold ring; confetti (use sparingly; fits celebration only); sound blips (opt-in); notification badge; focus ring animate; scroll cue bounce.

#### 27. Gestures and mobile-native patterns [IOS]
Tap; double-tap; long-press; swipe (left/right/up/down); edge-swipe; pinch; rotate; drag; pull-down; pull-up sheet; bottom sheet with detents; modal sheet; full-screen cover; page-curl; card stack swipe (Tinder-style); carousel snap; pull-to-reveal; shake; tilt/gyro (permission); haptics; safe-area handling; dynamic island; home indicator spacing; keyboard avoidance; thumb-zone layout; one-handed layouts; bottom nav; large titles collapsing (iOS large-title nav); segmented controls; context menus; share sheet; widgets; Live Activities-style; Stories format (vertical tappable cards); vertical video feed; "reels"-style snap scroll; haptic-like animation timing; momentum scroll; overscroll bounce.

#### 28. Forms, inputs and data entry
Floating labels; inline labels; stacked labels; inline validation; progressive disclosure; multi-step form; single-question-per-screen; conversational form; chat-style form; stepper; progress bar; autosave; autocomplete/combobox; masked inputs; OTP input; date pickers; range sliders; dual sliders; toggles; segmented; chips/tag inputs; file drop zone; rich text; code input; voice input; address lookup; password strength; passkeys; magic links; undo; smart defaults; "choose where you are" chooser patterns; checkboxes as cards (selectable cards); radio tiles; swatch pickers; quantity steppers; sticky submit bars.

#### 29. Search, filtering and discovery
Instant search; command palette; typo-tolerant/fuzzy; synonyms; highlighted matches; faceted filters; tag filters; sort controls; saved filters; "narrow" controls; A–Z index; topic index; tag cloud (as index); related items; "what next" modules; random/serendipity button; recommendations; recently viewed (needs storage; avoid on safety sites); search scopes; search suggestions; zero-result states; query-from-URL (shareable filters); semantic/natural-language search; chatbot search; "describe what happened" search (scenario search).

#### 30. Cards and content blocks
Media card; text card; stat card; quote card; link card; profile card; product card; pricing card; feature card; case-study card; testimonial card; tile (bento); poster card; flip card; expanding card; stack/deck card; swipe card; hover-reveal card; glass card; paper card; ticket card; receipt card; sticker card; label card; index card; field-note card; accordion card; timeline node card; map popup card; notice/callout card; checklist card; sidebar widget.

#### 31. Lists, tables and dense information
List rows with hover-reveal images; expanding rows; sortable tables; sticky headers/columns; responsive tables (stack/scroll/prioritise); zebra rows; grouped rows; inline sparklines; tree lists; nested accordions; definition lists; glossary; index with leaders (dot leaders); table of contents; numbered steps; checklists; comparison tables; spec sheets; data cards; "A–Z" jump bars; pagination; load more; infinite lists with landmarks; virtualised lists.

#### 32. Overlays, modals and layered UI
Modal dialog; bottom sheet; side drawer; popover; tooltip; toast; snackbar; banner; inline alert; callout; lightbox; command palette; dropdown; context menu; mega menu; full-screen overlay; cookie/consent (if needed); onboarding coach marks; spotlight tour; non-modal panel; picture-in-picture; sticky panels; "peek" panels; focus-trap behaviour; Esc to close; scrim styles; blur-behind.

#### 33. Onboarding, empty states and guidance
Welcome screen; progressive onboarding; product tour; coach marks; checklist; sample data; empty-state illustration + action; first-run chooser ("tell us where you are"); contextual hints; tooltips; inline help; guided paths ("start here"); reading paths; recommended order; returning-reader shortcuts; skip options; "what is this?" explainer; progress memory without cookies (URL/hash).

#### 34. Editorial and narrative devices (for long pages)
Cold open; title card; epigraph; thesis statement; chapter title; chapter number; interlude; pull quote; sidebar/box; marginal note; footnote; endnote; callout; timeline; before/after; case study vignette; composite scene (labelled); second-person address; direct address; refrain/anaphora; countdown/count-up; "turn" (reversal); evidence block; counterargument block; limits ("what this is not"); safety box; summary/key takeaways; "how to use this"; reading time; update note; glossary; index; bibliography/sources; credits; colophon; dedication; acknowledgements; "next in series"; share/print; letter to the reader; manifesto; call to action; closing image; silence (blank screen) as punctuation.

#### 35. Structures for scroll-driven stories
Linear chapters; hub-and-spoke; braided (two threads alternating); nested zoom (macro → micro); scale journey (powers of ten); time-lapse; before/after; compare/contrast; build-up (add one element per step); reveal (hide then show); peel (layers removed); funnel; spiral (return with new meaning); journey/map; case-file; field guide; ritual/liturgical (repeated formula); countdown; "day in the life"; rewind; parallel tracks; question-answer; claim–evidence–implication; problem → pattern → exit; open loop → payoff; act structure (setup, confrontation, resolution); three-reader paths.

#### 36. Cinematic techniques applied to the web
Establishing shot (wide first frame); close-up (zoom into a detail); dolly-in/out (scale/z-translate on scroll); pan/tilt (translate on scroll); tracking shot (camera follows subject); crane/rise; whip pan (fast transition); match cut (shape continuity across scenes); morph cut; cross-dissolve; fade to black/white; iris in/out; wipe; split screen; picture-in-picture; rack focus (blur shifts); depth of field; lens flare; letterbox; aspect-ratio switching; slow motion / time ramp (easing); smash cut; J-cut/L-cut (audio leads/trails); title sequence; credits roll; cold open; leitmotif (repeating visual motif); colour script (palette per act); montage; long take (continuous scroll with no cuts); freeze frame; time-lapse; jump cut; dissolve through white; silhouette; golden-hour grade.

#### 37. Sound and haptics
Ambient bed; UI sound set; hover blips; click sounds; scroll-synced soundscape; narration player; voice-over with captions; audio-reactive visuals (Web Audio analyser); generative music; spatial audio; mute toggle; volume ducking; gesture-unlocked audio; transcripts; haptic taps (Vibration API; Android); iOS haptic via switch input hack (unreliable); sound off by default.

#### 38. Motion principles and vocabulary
Easing (ease-in, ease-out, in-out, cubic-bezier, spring, overshoot/back, elastic, bounce, steps, `linear()`); duration scales; delay; stagger; cascade; choreography; sequencing; anticipation; follow-through; secondary action; squash and stretch; arcs; timing; spacing; staging; exaggeration; appeal (the 12 principles of animation applied to UI); object permanence; continuity; focus shift; direction/spatial model; hierarchy of motion; idle/ambient motion; interruptibility; reduced-motion variants; frame budget; jank; layout thrash; FLIP; will-change; GPU compositing; motion tokens; motion specs; animation curves libraries; physics-based motion (springs, inertia, friction); gravity; magnetism; drag; momentum; snap.

#### 39. Layout, spacing and rhythm vocabulary
Grid; gutter; margin; padding; whitespace/negative space; density; rhythm; proximity; alignment; baseline; optical alignment; axis; symmetry/asymmetry; balance; contrast; scale; hierarchy; emphasis; repetition; pattern; variety; unity; focal point; reading path (Z, F, gutenberg diagram); visual weight; figure-ground; framing; layering; overlap; bleed; safe area; golden ratio; rule of thirds; modular scale; 8-pt grid; 4-pt grid; container; fluid vs fixed; breakpoint; container queries; aspect ratio.

#### 40. Design principles, laws and psychology (names)
Gestalt (proximity, similarity, continuity, closure, figure/ground, common fate, symmetry, uniform connectedness, past experience); Fitts's law; Hick's law; Miller's law (7±2, chunking); Jakob's law; Doherty threshold; Postel's law; Tesler's law; Parkinson's law; Zeigarnik effect; Serial position effect; Von Restorff (isolation) effect; Peak–end rule; Aesthetic–usability effect; Pareto principle; Occam's razor; Law of Prägnanz; Goal-gradient effect; Paradox of choice; cognitive load (intrinsic/extraneous/germane); progressive disclosure; recognition over recall; affordance; signifier; feedback; mapping; constraints; discoverability; mental model; conceptual model; Norman's 7 stages; Nielsen's 10 heuristics; Shneiderman's 8 golden rules; Krug's "don't make me think"; Dieter Rams's 10 principles; Tufte (data-ink, chartjunk, small multiples); Swiss/International principles; WCAG POUR (perceivable, operable, understandable, robust); inclusive design principles; universal design; trauma-informed principles (safety, trustworthiness, choice, collaboration, empowerment, cultural humility); Kano model; Jobs-to-be-done; persona; empathy map; journey map; service blueprint; Atomic Design; Design tokens; BEM; ITCSS; Jacobs/Alexander pattern languages; "Hooked" model (avoid on safety/care content); dual-process thinking; priming; framing; anchoring; default effect; nudging (ethical use).

#### 41. Identity and brand systems
Logo (wordmark, monogram, emblem, symbol, combination, responsive, animated); favicon set; app icon; colour system; type system; imagery system; illustration system; icon system; motion identity; sound identity (sonic logo); voice and tone; brand architecture; naming; tagline; brand story; brand book/guidelines; design tokens; component library; pattern library; documentation site; brand archetypes (Creator, Sage, Explorer, Caregiver, Ruler, Magician, Hero, Outlaw, Jester, Lover, Everyman, Innocent); sub-brand systems (e.g. one identity per book in a series); series logo/emblem; share-card system (OG images); sticker/stamp marks; seals.

#### 42. Design systems and component libraries (to study)
Material 3 / Material 3 Expressive (Google); Apple Human Interface Guidelines (Liquid Glass); Fluent 2 (Microsoft); Carbon (IBM); Polaris (Shopify); Atlassian Design System; Lightning (Salesforce); Spectrum (Adobe); Primer (GitHub); Geist (Vercel); Radix UI / Radix Themes; shadcn/ui (copy-paste components); Tailwind UI/Catalyst; Chakra; Mantine; Ant Design; Bootstrap; Bulma; Polymer; Base Web (Uber); Gestalt (Pinterest); Paste (Twilio); Clarity (VMware); GOV.UK Design System; US Web Design System (USWDS); NHS Service Manual; Government Digital Service patterns; Mailchimp content style guide; Shopify Polaris content guide; Atomic Design (Brad Frost); Open Props (CSS tokens); Every Layout; Utopia (fluid type/space); Modern CSS Reset.

#### 43. Responsive and adaptive techniques
Mobile-first; progressive enhancement; fluid type/space (`clamp()`); container queries; media queries (width, height, orientation, hover, pointer, resolution, prefers-*); `dvh/svh/lvh`; safe-area insets; viewport-fit cover; responsive images (`srcset`, `sizes`, `<picture>`, art direction); responsive video; responsive tables; adaptive layouts (distinct mobile and desktop compositions); foldable support; large-screen/TV layouts; print styles; low-power/low-data modes (`prefers-reduced-data`); orientation locks (avoid); text-size scaling (rem); zoom to 400%; right-to-left layouts; vertical writing modes; localisation expansion.

#### 44. Accessibility features and inclusive patterns
Semantic HTML; landmarks; heading hierarchy; skip links; focus-visible; focus management; roving tabindex; ARIA (only as needed); live regions; accessible names; alt text; captions; transcripts; audio description; sign-language option; reduced motion; reduced transparency; high contrast; forced colours; dark mode; text-resize; line-spacing override support; dyslexia-friendly options (open fonts, spacing); plain language; reading level indicators; content notes; error summaries; accessible drag alternatives; target size; colour-blind safe palettes; screen-reader-tested figures (text alternatives to charts: data tables); keyboard shortcuts; voice-control labels; touch alternatives for hover; cognitive accessibility (chunking, consistency); neurodiversity-aware (no autoplay, stop motion); safe-reader options (discreet mode, quick exit).

#### 45. Performance techniques (names)
Critical CSS; inlining; code splitting; tree shaking; preload/prefetch/preconnect; `fetchpriority`; lazy loading; `content-visibility`; image formats (AVIF, WebP); responsive images; font subsetting; `font-display`; fallback metrics matching; HTTP caching; CDN; compression (Brotli); minification; HTML streaming; island architecture; partial hydration; SSG; edge rendering; service workers; offline-first; web workers; OffscreenCanvas; requestIdleCallback; scheduler APIs; debouncing/throttling; passive listeners; `will-change`; compositing layers; avoiding layout thrash; virtual lists; GPU instancing; LOD (levels of detail); texture compression (KTX2/Basis); Draco/meshopt; adaptive quality (DPR capping, FPS-based degrade); pausing offscreen animation; `prefers-reduced-motion`/`reduced-data` degrade; performance budgets; Core Web Vitals (LCP, CLS, INP); Lighthouse; WebPageTest; real-device testing.

#### 46. Personalisation, context and state
Time-of-day theming; local time display; weather-aware styling; location-aware (permission); device-aware (touch vs pointer); preference-aware (`prefers-*`); returning-visitor memory (storage; avoid on safety sites); content-derived colour; adaptive reading modes (quick/sequence/full); user-chosen depth; language preference; accessibility profile; "paths" by reader intent; session-less state via URL/hash; local-only notes (in-page, never stored/sent); private modes.

#### 47. AI-native and conversational patterns
Chat UI; streaming text; typing indicator; "thinking" shimmer; reasoning steps disclosure; citations/footnotes; inline suggestions; command bar with natural language; generative UI (components assembled from model output); AI orb/blob avatars; voice mode visuals; prompt suggestions chips; regenerate/variations; side-by-side compare; canvas/artifact panels; agent progress timelines; tool-call cards; memory controls; confidence/uncertainty display; human-in-the-loop approval; undo for AI actions; transparent sources; safety rails and disclaimers.

#### 48. Spatial, AR/VR and device-extending
visionOS-style windows/ornaments; WebXR; AR quick look (USDZ/GLB); model-viewer AR; 360 photo/video; photogrammetry; Gaussian splats; NeRF-style captures; LiDAR scans; gyro parallax; camera-based effects (face/hand tracking; permission); webcam art; microphone-reactive; geolocation experiences; NFC/QR touchpoints; wearable/glance UIs; car/TV UIs; kiosk modes.

#### 49. E-commerce and product patterns
PDP gallery (zoom, 360, video); variant swatches; size guides; sticky add-to-cart; mini-cart drawer; quick view; recommendation rails; reviews with photo; comparison; bundle builder; configurator; try-on; wishlist; stock indicators; delivery estimator; checkout steps; express pay; order tracking; membership; subscriptions; collection storytelling; lookbooks; editorial commerce; drop/launch countdown; waitlist; scarcity (use honestly); trust badges; returns policy surfacing.

#### 50. Social, sharing and virality devices
Share cards (OG/Twitter images); shareable result cards; "Wrapped"-style year summaries; quote-share; copy-link per section; deep links; print/PDF export; embed codes; remix kits; clip-friendly layouts (vertical); caption-safe zones; watermarking; citations; "send to a friend" (privacy-aware); community walls; UGC galleries (moderation needs); badges (avoid when contradictory to subject).

#### 51. Gamification mechanics (name them to decide whether to avoid them)
Points; levels; badges; streaks; leaderboards; progress bars; quests; unlockables; easter eggs; collectibles; mini-games; quizzes; scoring; combos; daily challenges; loot/rewards; avatars; social comparison; scarcity timers; variable reward. Many are inappropriate for care/safety content; some books argue against them explicitly.

#### 52. Dark patterns and anti-patterns (so Claude can recognise and avoid them)
Confirmshaming; roach motel; forced continuity; hidden costs; sneak into basket; misdirection; trick questions; disguised ads; privacy zuckering; bait-and-switch; fake urgency/scarcity/countdowns; nagging; obstruction; forced registration; infinite scroll traps; autoplay; scroll-jacking; carousel-hiding; hamburger-everything; mystery icons; tiny tap targets; low-contrast text; text over busy imagery; hover-only affordances; modal on arrival; cookie walls; fake loading; hidden unsubscribe; notification begging; skeuomorphic clutter; walls of centred text; auto-advancing sliders; unlabelled form fields; placeholder-as-label; disabled-submit mystery; layout shift on load; fonts flashing; scroll-linked motion with no off switch.

#### 53. Process and design-ops vocabulary
Brief; audience; reader state; jobs-to-be-done; moodboard; reference audit; style tiles; element collage; wireframe; low-fi/hi-fi comps; prototype; interactive prototype; motion prototype; storyboard; design critique; heuristic evaluation; cognitive walkthrough; usability test; five-second test; first-click test; card sort; tree test; A/B test; diary study; accessibility audit; performance audit; design QA; visual regression; design tokens; component spec; handoff; design system governance; versioning/changelog; documentation; retrospectives; design principles statement; "design direction document"; art direction; creative direction; hero-first prototyping; vertical slice.

#### 54. Tools, libraries and platforms (names to look up)
Design: Figma (incl. shaders/Make), Framer, Webflow, Spline, Rive, Blender, Cinema 4D, After Effects, Procreate, Illustrator, Photoshop, Affinity, Canva, Penpot, Sketch, Protopie, Principle, Lottie, Linearity, Midjourney/Firefly/image generators (mood only), Adobe Express, Figma Make, v0/Lovable/Bolt/Claude artifacts (generation tools; review output critically).
Code (motion/graphics): GSAP (+ScrollTrigger, ScrollSmoother, SplitText, Flip, MorphSVG, DrawSVG), Motion (Framer Motion/vanilla), Anime.js, Lenis, Locomotive Scroll, Scrollama, Barba.js, Swup, Three.js, React Three Fiber, drei, Babylon.js, OGL, regl, PixiJS, p5.js, Matter.js, Rapier, Cannon-es, D3, Observable Plot, Chart.js, Vega, Deck.gl, Mapbox GL, MapLibre, Leaflet, Lottie, Rive, Howler, Tone.js, Web Audio, Splitting.js/SplitType, Fuse.js/MiniSearch/Lunr/Pagefind, Floating UI, Embla, Swiper, Glide.
Code (frameworks): vanilla HTML/CSS/JS, Astro, Next.js, Nuxt, SvelteKit, Remix, 11ty, Hugo, Vite, WebC; CSS: Tailwind, UnoCSS, Open Props, Sass, PostCSS, Lightning CSS.
Testing: Playwright, axe-core, Lighthouse, WebPageTest, BrowserStack/real devices, Chrome DevTools (rendering, performance, layers), Safari Web Inspector, Percy/Chromatic (visual regression), Pa11y.
Colour/type: Coolors, Huetone, oklch.com, Realtime Colors, Contrast checkers, Fontshare, Google Fonts, Velvetyne, Collletttivo, Fonts In Use, Typewolf, Wakamai Fondue, Font Squirrel generator, glyphhanger.

#### 55. Inspiration sources and places to study (browse these to see "top tier")
Awwwards (Site of the Day/Month/Year, Developer Award, Honorable Mentions); FWA (Favourite Website Awards); CSS Design Awards (CSSDA); Godly; Siteinspire; Minimal Gallery; Land-book; Lapa Ninja; One Page Love; Httpster; SaaS Landing Page; Landingfolio; Dark Mode Design; Refero; Mobbin (apps); Page Flows (flows); Screenlane; Pttrns; UI Garage; Muzli; Behance; Dribbble; Savee; Are.na; Pinterest boards; Codrops (tutorials and demos); CodePen (search by effect); Shadertoy; The Book of Shaders; Three.js examples; Three.js Journey (Bruno Simon); Bruno Simon's portfolio; Awwwards "Collections"; Active Theory, Immersive Garden, Resn, Lusion, Makemepulse, Locomotive, Obys, Cuberto, Monopo, Hello Monday/DEPT, Unseen Studio, Merci Michel, Studio Freight/Darkroom (Lenis authors), Basement Studio, Cappen, 14islands, Zajno, Bureau Cool-style editorial studios; Pentagram, Collins, Base Design, Wolff Olins, Studio Dumbar, Order, Sagmeister & Walsh (identity/art direction); NYT Graphics, Guardian Visuals, Washington Post, Reuters Graphics, Bloomberg Graphics, FT Visual Journalism, The Pudding, Quanta, Aeon, The Marginalian, Nautilus, Works in Progress, Vox, The Verge; Stripe, Stripe Press, Linear, Vercel, Apple (product pages), Framer, Notion, Figma, Arc, Raycast, Superhuman, Spotify (Wrapped), Airbnb, Nike, Aesop, Teenage Engineering, Nothing, Ableton, Resident Advisor, Bandcamp, A24, MUBI, Criterion; GOV.UK, USWDS, NHS (clarity benchmarks); Calm, Headspace (soft tone); crisis-service sites (quick exit patterns).
Educators and teachers of the craft: Josh W. Comeau, Kevin Powell, Jhey Tompkins, Cassie Evans, Adam Argyle, Una Kravets, Bramus (scroll-driven animations), Rachel Andrew, Lea Verou, Chris Coyier, Ahmad Shadeed, Stephanie Eckles (Modern CSS Solutions), Heydon Pickering (Every Layout), Miriam Suzanne, Steve Schoger/Adam Wathan (Refactoring UI), Emil Kowalski, Rauno Freiberg, Paco Coursey, Brad Frost, Val Head (UI animation), Sarah Drasner, Jen Simmons (layout), Tobias Ahlin, Matt Perry (Motion), Bruno Simon, Yuri Artiukh (Yuriy), Georgi Nikoloff, Daniel Velasquez, Nicky Case, Bret Victor (explorable explanations), Edward Tufte, Alberto Cairo, Giorgia Lupi (data humanism), Mike Bostock, Amanda Cox, Nadieh Bremer, Shirley Wu.

#### 56. Emerging and recent (2025–26) items worth knowing by name
Apple **Liquid Glass** (iOS 26 / macOS Tahoe 26); **Material 3 Expressive**; **scroll-driven animations in CSS** now in major browsers (Chrome, Edge, Firefox, Safari per recent guides; verify on caniuse); **View Transitions** (same and cross-document); **WebGPU** page transitions with a persistent GPU scene + DOM tracking + lightweight router; **TSL/WebGPU shaders**; **shader gradients** and shader-based UI (shaders arriving in Figma, per a 2026 roundup); **clip-path wipe transitions** driven by GSAP; **render-target compositing**; **kinetic typography as structure** (headlines that sequence value points, weight/width shift on scroll, particle-dispersing text); **tactile brutalism / cyberbrutalism**; **bento grids**; **dark-mode-first**; **3D hero objects**; **variable fonts**; **soft/“blurred” glow becoming shader-driven**; **anchor positioning**; **popover API**; **`@starting-style`**; **`linear()` easing**; **container queries**; **`light-dark()`**; **oklch/P3**; **`text-wrap: balance`**; **agent-driven / AI-generated UI**; **AI orbs and streaming interfaces**; **Gaussian splats on the web**; **WebXR**; **local-first apps**; **“invisible architecture”** (infrastructure-quiet UX, per one 2026 trend article; treat as a label, not a method).

---

##### Sources consulted for the 2025–26 items (secondary commentary; verify against primary pages)
- [Web Design Trends 2026: The Definitive Guide (Line25)](https://line25.com/articles/web-design-trends-2026/)
- [Web Design Trends 2026: Tactile Brutalism & Invisible Architecture (Fireart)](https://fireart.studio/blog/the-best-web-design-trends/)
- [Website Design Trends 2026 (Lovable guide)](https://lovable.dev/guides/website-design-trends-2026)
- [webdesign trends 2026 (StudioMeyer)](https://studiomeyer.io/en/blog/webdesign-trends-2026)
- [Why are immersive experiences dominating the 2026 Awwwards](https://digitalstrategyforce.com/journal/why-are-immersive-experiences-dominating-the-2026-awwwards/) (its statistics are unverified; not relied on)
- [From Shader Uniforms to Clip-Path Wipes: How GSAP Drives My Portfolio (Codrops, May 2026)](https://tympanus.net/codrops/2026/05/06/from-shader-uniforms-to-clip-path-wipes-how-gsap-drives-my-portfolio/)
- [Codrops archive, 2026](https://tympanus.net/codrops/2026/06/) (WebGPU page transitions, Barba.js + Three.js transitions, SVG-mask scroll reveals)
- [Awwwards inspiration search](https://www.awwwards.com/inspiration_search/single-page/)

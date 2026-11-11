# COVERAGE: Fractal² intro (2026-11-11). Every category of `docs/design-catalogue/06-master-names-bible.md`, marked.

Brief (from the owner's words + interview): a scroll story for a mixed readership (some may be in danger, some skeptical, some relaxed); feel = **cinematic, awe, complete clarity**; **phone first**; rich but safe motion; fixed text (`content/fractal2/intro-story.md`) and fixed artwork (the owner's Fractal drawn by `logo.py`).
Concept sentence: *One unbroken camera pull-back (a "powers of ten" scale journey) makes the reader feel how large one pattern is, and labels exactly what they are looking at on the way, so the awe arrives with complete clarity.*

| # | Category | USE | REJECTED (reason) | N/A |
|---|---|---|---|---|
| 1 | Genres | scrollytelling / narrative explainer | portfolio, product landing (not a pitch) | |
| 2 | Landing anatomy | cold open, thesis, evidence, turn, door | pricing, testimonials (nothing sold) | |
| 3 | Hero types | zoom-through hero; story-opening title card | particle-field (F1), full-bleed video (no footage), shader gradient (F4) | |
| 4 | Navigation/header | opaque thin bar, Quick Exit "Leave" | hamburger mega-menu (one page) | |
| 5 | Footer | one-line safety/credit | link farms | |
| 6 | Layout | camera layer + safe text zone; phone: art above, text below | split screen on phone (collides) | |
| 7 | Scroll techniques | scroll-scrubbing, pinning (fixed stage), scroll-driven highlight | scroll hijack, scroll-jacked decks (a11y), velocity skew (F6) | |
| 8 | Transitions | match cut (original becomes the centre of the map) | page transitions (single page) | |
| 9 | Preloaders | glow placeholder then fade-in | counter preloader (hides the story) | |
| 10 | Type effects | direct line reveal only | scramble, typewriter, kinetic type (F1, F6) | |
| 11 | Type vocabulary | display serif + mono caption accent; measure 60-66; small caps labels | blackletter/script (register) | |
| 12 | Cursor effects | none | all (phone first, F6) | DESK-only |
| 13 | Hover | button focus/hover states | magnetic, image trails (F1) | |
| 14 | Buttons/CTA | one CTA (Enter the first sector) | competing CTAs (audit item) | |
| 15 | Imagery | the owner's vector diagram only | stock photography, AI imagery (no licence, off-brand) | |
| 16 | Image presentation | disc mask, ghosting behind text, deep crop | parallax tilt (F6) | |
| 17 | Video | none | looped video (weight, safety) | |
| 18 | 3D/WebGL [GPU] | none (2D transforms only) | WebGL (phone cost, no-GPU CI, F12) | |
| 19 | Backgrounds/ambient | starfield from the art; 2,700-point field with a data meaning | mesh/aurora gradients (F10), grain (F1) | |
| 20 | Colour and light | art colours only inside the figure; page chrome ink + paper white + one vermilion | gold chrome and glows on the page (F4, F10) | |
| 21 | Surfaces/depth | real depth = scale (z), no glass | glassmorphism (F9) | |
| 22 | Shapes/masks | concentric rings (the content), crosshair, ticks, leader lines | sacred-geometry decoration (F10) | |
| 23 | Illustration/icons | none beyond the figure | icon sets | |
| 24 | Data viz | ring/orbit diagram, unit field (1 point = 1 example), annotated chart with direct labels | pie/bar (no data to compare) | |
| 25 | Maps | atlas of 30 sector glyphs with the live one marked | geographic maps | |
| 26 | Microinteractions | ring highlight per stage, focus rings | confetti, haptics (register) | |
| 27 | Gestures [IOS] | native scroll only | swipe hijack, pull-to-refresh tricks (F12) | |
| 28 | Forms | none | newsletter capture (no tracking) | |
| 29 | Search/filter | none on the intro (lives on the sector site) | | |
| 30 | Cards | none | card grids (template look) | |
| 31 | Lists/tables | the eight-stage list as the scroll driver | long tables | |
| 32 | Overlays | none | modals (safety) | |
| 33 | Onboarding | one "Begin" cue | tours | |
| 34 | Editorial devices | cold open, title card, composite scene (labelled), turn, safety box, silence as punctuation, closing image | epigraph pile | |
| 35 | Scroll story structures | scale journey (powers of ten), nested zoom, spiral (return with new meaning), problem->pattern->exit | hub-and-spoke | |
| 36 | Cinematic | establishing shot, close-up, dolly-out, match cut, long take, letterbox (option), title sequence, leitmotif (the ring) | whip pan, lens flare (F1) | |
| 37 | Sound/haptics | none (no autoplay; narration is a separate decision) | autoplay audio (safety) | |
| 38 | Motion principles | damped easing, continuity, interruptibility, reduced-motion variant | bounce/elastic (register) | |
| 39 | Spacing/rhythm | 8 px grid, 4 silent beats = Quiet >= 30% | uniform density (F8) | |
| 40 | Principles/psychology | Gestalt continuity, peak-end, progressive disclosure, Von Restorff (the live sector) | dark patterns | |
| 41 | Identity | emblem + wordmark from the brand kit | new logo | |
| 42 | Design systems | tokens in one `:root` | component library (nothing to compose) | |
| 43 | Responsive | phone-first, landscape mode, tablet | desktop-only effects | |
| 44 | Accessibility | skip link, reduced motion, no-JS reading, 44 px targets, quick exit, text alternatives | | |
| 45 | Performance | 2048 px phone images, deferred outer art, damped rAF only when needed | video, WebGL | |
| 46 | Personalisation | none (no tracking) | | |
| 47 | AI-native | none | chat widgets | |
| 48 | Spatial/AR | none | | N/A |
| 49 | E-commerce | none | | N/A |
| 50 | Social/sharing | share card only (brand kit) | share counters (tracking) | |
| 51 | Gamification | none | all (grave register; this work refuses it) | |
| 52 | Dark patterns | none | scarcity, urgency, confirm-shaming | |
| 53 | Process vocabulary | gates + critic + benchmark | | |
| 54 | Tools | Playwright, design-gates, vendored nothing | GSAP/Lenis (new dependency: owner's yes) | |
| 55 | Inspiration | Stripe Press (stack/identity), Apple AirPods Pro (one idea per screen), NASA Webb (title + mono labels), Eames Powers of Ten (concept) | | |
| 56 | Emerging 2025-26 | CSS scroll-driven animation (kept as option) | WebGPU showpieces | |

## The obvious answer (rejected on purpose)
A default generator would produce: dark navy page, gold serif headings, a glowing gold ring graphic with a particle field, gold buttons, fade-in paragraphs and a parallax hero. That is F4 + F10 and is **what my v6 page chrome currently does**. The art is the owner's (fixed); the *page around it* must not be that.

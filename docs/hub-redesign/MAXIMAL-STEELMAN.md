# Homepage v19 "maximal": steelman + full addition inventory (2026-11-21)

Owner's words: "I want a more complex page. I want every possible effect or animation or haptic or whatever to make this an award winning dynamic top tier home page. Just because it doesn't need something doesn't mean I don't want it. Steel man it and /design-director identify any and all areas where something could be added."

Method: design-director track = Rescue/expand (v18 exists). Coverage scan of all 56 categories in `docs/design-catalogue/06-master-names-bible.md` against every section of v18. The design-director Budget (max 3 feature effects per screen, 1 novel interaction) is a catalogue rule, not one of the 10 homepage rules, so the owner has overridden it. The 10 hard rules in CLAUDE.md still bind every item below; items they block are marked BLOCKED with the rule.

---

## Part 1. Steelman

### The strongest case FOR going maximal
1. **Awwwards judges score Creativity and Design alongside Usability.** v18 scored 5s from our own critic, but its round-1 verdict was "not a bold moving opening". Restraint wins Honourable Mentions; Site of the Day winners almost always have a signature technical moment (a shader, a 3D scene, a physical interaction) that people screen-record.
2. **The brand has a built-in reason for spectacle.** "Worn in the light. Alive in the dark." is a light/dark physics idea: strontium aluminate charging and glowing. A real-time phosphor shader, a lamp you move, particles of light are not decoration here, they *are* the product. That is the rare case where maximal effects pass the "explain test".
3. **The page already has two worlds.** A hard threshold lets the dark Workshop go full spectacle without touching the reading world's calm. Complexity can be *placed*, not sprayed.
4. **The owner asked, twice, plainly.** The open brief removed every limit without a hard reason. "It doesn't need it" is not a hard reason.
5. **Cost is lower than it looks.** GSAP's former paid plugins (SplitText, DrawSVG, MorphSVG, Flip, Observer, ScrollSmoother, Inertia, Physics2D) are now free and can be vendored inline like core. A hand-written WebGL shader is ~5-15 KB with no library. Web Audio can synthesise every UI sound with zero sound files.

### The strongest case AGAINST (taken seriously, not dismissed)
1. **The reader.** Many visitors arrive hurting, late at night, possibly on a shared or watched phone (that is why Leave now exists). A long intro, sudden sound, flashing light or a heavy page can make the site feel unsafe or slow at the worst moment. F13 "wrong register".
2. **Phones.** A WebGL scene plus scroll smoothing plus particles can drop frames or crash tabs on a mid-range Android or an older iPhone (F12). Awwwards' mobile score and Google's Core Web Vitals both punish this.
3. **Effect soup (F1) and fatigue (F8).** Twenty effects at full volume read as a template demo, not a brand. The page could lose the one thing every critic praised: it feels made by a person.
4. **Accessibility.** More motion means more ways to fail WCAG 2.2.2 (auto-motion), 2.3.1 (flashes), 2.3.3 (motion from interaction), and more focus traps.
5. **Haptics are uneven.** Android Chrome supports vibration; iPhone Safari has no vibration API. The only iPhone route is a native switch control tick, which fires only on a real tap, not on scroll or charge progress.

### Verdict: maximal, choreographed, and switchable
Both cases survive in part, so v19 does all of it, with four safeguards that answer each "against" point instead of cutting effects:
- **Placed intensity.** Reading world = maximal *craft* (press, ink, paper, type that reacts) at medium volume. Workshop/dark world = maximal *spectacle* (WebGL phosphor, lamp, particles, gyro). Loud/quiet map in Part 3.
- **A "Still" switch in the header**, beside Leave now. One tap stops every self-running effect and sound for this visit (not saved: rule 3). Reduced-motion users get Still automatically, plus a designed version of each effect.
- **Leave now stays instant**: it kills audio and animation first, then leaves. Nothing ever delays it.
- **Device tiers.** Phones without WebGL2 or with low memory get the CSS/SVG version of each GPU effect (designed, not stripped). Gate-tested at 4x CPU throttle.

---

## Part 2. Full inventory (every area where something can be added)

Legend: **Cost** S (<1 h) / M (half day) / L (day+). **Weight** added to the page. Status: NEW, UPGRADE (exists in v18, goes further), BLOCKED (rule number).

### A. Arrival (first 3 seconds)
| ID | Addition | Meaning | Cost | Notes |
|---|---|---|---|---|
| A1 | **Press-stamp title card**: a brass seal presses into the paper, ink spreads, lifts to reveal the headline (0.9 s, skippable by any tap/scroll/key, once per visit in memory only) | "The Press": every visit opens with an impression | M | Must not delay Leave; never repeats in the same visit |
| A2 | Ink-bleed headline: letters arrive as wet ink that dries (SVG turbulence filter on a mask, then removed) | Printing | M | Filter removed after 1.2 s (perf) |
| A3 | Real-progress preloader counter 0-100 tied to font + hero image | BLOCKED-ish: page loads in 0.5 s; a counter would add delay. Offer as A1 fallback only | S | Recommend NO |
| A4 | Time-of-day greeting line ("Up late?" after 11 pm, local clock only, never stored) | Meets the late-night reader | S | Copy needs your approval |
| A5 | Time-of-day theme: after dark the whole page starts dimmer and the pendants in the hero glow | Light/dark concept | M | Local clock only |

### B. Hero headline and type
| ID | Addition | Detail | | |
|---|---|---|---|---|
| B1 | SplitText char-level reveal with per-letter ink weight (upgrade of the line mask) | UPGRADE | S |
| B2 | Variable weight on scroll: headline thins as you scroll away, like ink fading | S | Gloock is not variable; needs Public Sans (variable) for the moving words, or a fake with 2 weights crossfade |
| B3 | Scroll-highlight lede: words brighten as they are read | S |
| B4 | Hover/tap letter roll on chips (text roll-over) | S |
| B5 | Kinetic word swap in the headline ("the moment you **start to wonder** / **stop sleeping** / **feel watched**") cycling 3 times then stopping (WCAG 2.2.2 < 5 s) | M | Copy approval |
| B6 | Text scramble/decode on the "What's happening?" label when an answer is chosen | S |

### C. The hero book (the current signature)
| ID | Addition | Detail | | |
|---|---|---|---|---|
| C1 | **WebGL book**: real 3D book with page thickness, paper normal map, light that follows the pointer/gyro, cover hinge physics | UPGRADE (CSS 3D now) | L | ~15 KB hand-written; CSS book stays as fallback |
| C2 | Pages riffle (flip through 6 pages) between answer covers instead of one turn | M |
| C3 | Drag to open the cover by hand (Draggable + Inertia, springs back) | M | Must keep keyboard path |
| C4 | Gyro tilt on phones (DeviceOrientation; iPhone needs a tap to allow) | S | Permission prompt on iPhone; offered via the Still/settings sheet, never automatic |
| C5 | Dust motes in the lamp light around the book (canvas particles, 40 max) | S |
| C6 | Book casts a real soft shadow that stretches with tilt | S |
| C7 | Scroll: the book flies down and lands on the first shelf (shared-element / Flip) | L | Strong award moment; complex on resize |

### D. Answer chips and the starting-point card
| ID | Addition | Detail | | |
|---|---|---|---|---|
| D1 | Magnetic chips on desktop (pull toward cursor) | S |
| D2 | Press = wax-seal stamp ring that ripples out from the finger | S |
| D3 | Haptic tick on every chip tap (Android vibrate 10 ms; iPhone switch-tick) | S | iPhone route needs testing on a real device |
| D4 | Picks deal in like cards from the book (Flip from the book's position) | M |
| D5 | Soft paper sound on answer (opt-in sound only) | S |

### E. Header, nav, scroll
| ID | Addition | Detail | | |
|---|---|---|---|---|
| E1 | **Scroll progress as an ink line** under the header that fills brass, then turns strontium green after the threshold | S |
| E2 | Animated nav pill (shared background slides between items) | S | v18 rejected it as "frequent"; owner now overrides |
| E3 | Smooth scroll with inertia (Lenis-style, written inline ~3 KB) | M | Risk: feels floaty on phones; native on touch, smooth on wheel only |
| E4 | Scroll-velocity skew on the title strip and covers | S |
| E5 | Header compresses into a seal on scroll down, expands on scroll up | S |
| E6 | Still switch (see verdict) | S | Required companion to everything here |
| E7 | View Transitions when jumping via nav (section crossfade/wipe) | S | Falls back to instant where unsupported |

### F. The Library shelves
| ID | Addition | Detail | | |
|---|---|---|---|---|
| F1 | 3D shelf: covers stand as books on a wooden ledge, spines visible, tilt toward the cursor | M |
| F2 | Hover/tap a cover: it slides out of the shelf and turns to show its back blurb | M |
| F3 | Spotlight card glow following the pointer on each shelf | S |
| F4 | Horizontal drag-to-scroll shelves with momentum and rubber-band edges | M |
| F5 | Shelf labels draw in with a hand-ruled underline (DrawSVG) | S |
| F6 | Covers pick up a light sheen sweep as they scroll into view | S |
| F7 | Card stacking (shelves pin and stack as you scroll) | M | Long page risk; test |
| F8 | Haptic tick when a shelf snaps | S |

### G. The bigger-picture door
| ID | Addition | Detail | | |
|---|---|---|---|---|
| G1 | Real door: two panels split open in 3D with light spilling out (curtain/split-door) | M |
| G2 | Hold-to-open (long-press ring) instead of a tap, to make the opt-in deliberate | S | Fits "not put off": choosing to see it |
| G3 | Light-leak particles through the door crack while closed | S |
| G4 | Low creak/air sound (opt-in) | S |

### H. Free tools
| ID | Addition | Detail | | |
|---|---|---|---|---|
| H1 | Pattern Decoder card runs a tiny live demo (text decodes into tags) | M |
| H2 | The Root card: a root system draws down as it scrolls in | S |
| H3 | Tilt + glare cards | S |

### I. The Listening Room (pending song restore)
| ID | Addition | Detail | | |
|---|---|---|---|---|
| I1 | Audio-reactive visual (Web Audio analyser drives the glow line / bars) | M | Needs songs back |
| I2 | Vinyl/record that spins while playing, scratch-scrub to seek | M |
| I3 | Persistent mini-player that follows the page (tap to start only, rule 5) | M |
| I4 | Hover preview: waveform draws on each track row | S |

### J. The threshold (light to dark)
| ID | Addition | Detail | | |
|---|---|---|---|---|
| J1 | **Scroll-scrubbed lights-out**: the paper page burns down to black from the edges, the header and text swap palette live | M | The single best award moment candidate |
| J2 | The headline "Worn in the light. Alive in the dark." splits: top half lit, bottom half glows as you pass | S |
| J3 | Stars of phosphor appear one by one as the light goes | S |
| J4 | Low hum swells (opt-in sound) | S |

### K. The Portals (dark world, maximal spectacle)
| ID | Addition | Detail | | |
|---|---|---|---|---|
| K1 | **WebGL phosphor shader**: charge paints light into the pendant from where you touch; glow decays physically (exponential + afterglow curve) and bleeds (bloom) | UPGRADE | L | Real photo stays; shader is an overlay |
| K2 | **Lamp cursor**: in the dark world the cursor/finger is a UV lamp; pendants it passes over charge a little (spotlight reveal) | M |
| K3 | Gyro: tilt the phone and the glow catches like real resin | S |
| K4 | Charging haptic: rising pulse pattern on Android while held; one tick at full on iPhone | S |
| K5 | Charge hum sound rising in pitch (Web Audio synth, opt-in) | S |
| K6 | Full-screen "lights off" view: tap a charged pendant and everything else goes black for 3 s | M |
| K7 | Particle afterglow trailing from the pendant when you swipe | S |
| K8 | Drag a pendant to rotate it (photo pair only allows a fake: parallax on layers) | M | True 3D needs product scans |

### L. NFC guide feature and "In the making"
| ID | Addition | Detail | | |
|---|---|---|---|---|
| L1 | Tap animation: a phone slides over a wax seal, an NFC ripple pulses, a link appears (animated SVG) | M |
| L2 | Real NFC moment: on Android Chrome, Web NFC can read a tag ("tap your seal to your phone") | M | Android only; permission; fun demo |
| L3 | The Press icon stamps; The Casting icon pours (DrawSVG/MorphSVG) | S |
| L4 | Card hover: the guide's cover lifts off like a page | S |

### M. Support, footer, counter
| ID | Addition | Detail | | |
|---|---|---|---|---|
| M1 | Visit counter as a split-flap/odometer that rolls to the live number | S |
| M2 | Big footer signature draws on (your signature as an SVG stroke) | M | Needs signature vectorised (image_vectorize, owner OK) |
| M3 | Footer "back to the light" button reverses the threshold | S |
| M4 | Support buttons: heart-burst / coin-drop micro-interaction | S |

### N. Site-wide layers
| ID | Addition | Detail | | |
|---|---|---|---|---|
| N1 | Custom cursor (desktop): ink dot in the light, lamp in the dark, labels "open", "hold", "drag" | M |
| N2 | Paper grain that drifts subtly (animated noise, 8 fps) | S | Must stop under Still |
| N3 | Global UI sound set (opt-in toggle in the header, synthesised, no files) | M | Rule 5: sounds only after the reader taps the sound toggle, and only as replies to taps |
| N4 | Global haptic layer (D3, F8, K4 share one helper) | S |
| N5 | Konami/secret: type "glow" anywhere and the lights go out | S | Easter egg; awards love these |
| N6 | Section colour script: each shelf tints the page slightly toward its cover colours | S |
| N7 | Leitmotif: a small seal mark recurs in every section and reacts | S |
| N8 | Page-peel / page-turn transitions between sections | M | Risk of F1; test |

### Blocked by a hard rule (cannot be added)
- Third-party fonts, Lottie/Spline/YouTube embeds, CDN libraries (rule 2: vendor and inline instead).
- Remembering returning visitors, "welcome back", saved progress or a saved Still/sound setting (rule 3).
- Autoplay sound or music, scroll-started sound without a prior tap (rule 5).
- Flashing faster than 3 times a second anywhere (WCAG 2.3.1, rule 4).

---

## Part 3. Intensity map (v19)
| Section | Volume | Lead effect |
|---|---|---|
| Arrival + hero | Loud | A1 press stamp, C1 WebGL book |
| Answer + picks | Medium | D4 cards deal from the book |
| Shelves | Medium | F1/F2 3D shelf, cover pull-out |
| Door | Quiet until opened, then Loud | G1 split door |
| Tools, Music | Quiet / Medium | H1, I1 |
| Threshold | Loud | J1 lights-out burn |
| Portals | Loud | K1 phosphor shader, K2 lamp |
| NFC + making | Medium | L1 tap animation |
| Footer | Quiet | M1 odometer, M2 signature |

No more than two Loud sections in a row: the Medium answer/shelf block separates the hero from the door, and Tools/Music sits before the threshold.

## Part 4. How it would be built (design-director law 1 and N7)
Batches, each gated (verify-hub, design-gates at 4x throttle, axe, perf, reduced motion, Still on) before the next is added. One critic round after the last batch.
1. Foundations: Still switch, haptic helper, sound engine (off), device tiers, GSAP plugins vendored.
2. Arrival + hero: A1, A2, B1, B3, B6, C2, C3, C5, C6, D1-D4.
3. Library + door + tools: E1, E2, E4, E5, F1-F6, F8, G1-G3, H1-H3.
4. Threshold + Portals: J1-J3, K1-K7.
5. Workshop end + footer + site layers: L1, L3, L4, M1, M3, M4, N1, N2, N5-N7.
6. Big-ticket items, each as its own release: C1 WebGL book, C7 book-to-shelf flight, E3 smooth scroll, F7 stacking, N8 page turns.
Music items (I1-I4) wait for the song restore.

## Part 5. Owner decisions (2026-11-21)
- Volume: **Placed**. Every effect gets added; the reading half is rich at medium volume, the dark Workshop is full spectacle, and a Still switch sits beside Leave now.
- Sound: **yes, off until tapped**. Synthesised in the page, a header sound button, never saved between visits.
- Intro: **no**. A1 press-stamp title card and A3 preloader are out; the headline rises straight away (B1 upgrade still applies).
- New words: **skip both**. A4 late-night line and B5 cycling headline are out. A5 (time-of-day dimming, no words) stays.

### Batch 1 done (2026-11-21): foundations
- Still switch (header beside Leave now; also in the phone menu): stops every self-running effect and all sound for this visit, not saved. Reduced-motion readers already get the still version.
- Sound: synthesised in the page (tick, press, page turn, door, charge hum, glow chime), created only by a tap on the Sound switch (desktop header, phone menu).
- Haptics: Android vibrate; iPhone one system tick via a hidden native switch (tap only; needs a real-device check). Portals: a pulse that quickens while charging, a firmer tap at full.
- Leave now silences sound and stops motion before it leaves.
- Device tier (html data-tier high/low) ready for the GPU effects.
- GSAP plugins vendored (SplitText, DrawSVG, MorphSVG, Flip, Observer, Draggable, Inertia, Physics2D, CustomEase); the builder inlines only the ones listed in GSAP_PLUGINS.
- Phone header: Menu became an icon to fit Still; at under 360px Still lives in the menu only.
- Gates: verify-hub all pass (4 new checks: no sound without a tap, Still stops motion, Sound lifts Still, Still silences sound); design-gates 0 FAIL; axe clean dark + light.

### Batch 2 done (2026-11-21): the hero
- Headline set letter by letter like wet ink: each letter rises into its line and dries from brass to paper (the split is undone after 2 s; the heading keeps one accessible name throughout).
- Lede words brighten as the reader scrolls past (scroll-linked, kept under reduced motion; both colours pass AA).
- Chips: label rolls over on hover, lean toward the pointer (desktop), and a wax-seal ring ripples from the finger on press; haptic tick.
- Answer: the book opens on its spine, five pages riffle, and it closes on the new cover (paper sound twice); the three picks deal out of the book like cards; the heading decodes from press type into the words.
- The cover can be dragged open by hand (mouse, or a sideways swipe on phones) and springs shut; a tick at full open.
- Dust in the lamplight (canvas, 46 motes on capable devices, 22 otherwise, pauses off-screen and under Still); a floor shadow that tightens as the book floats and shifts with the tilt.
- Android phones: tilting the phone tilts the book (iPhone needs a permission tap; not added).
- After 9 pm by the reader's own clock (never stored) the page darkens a touch and the lamp turns strontium green.
- Gates: verify-hub all pass; design-gates 0 FAIL (dust kept clear of the caption); axe clean; LCP 0.57 s, CLS 0, 239 KB transferred.

### Batch 3 done (2026-11-21): library, door, tools, header
- Header: a reading line under the header fills brass as you scroll and turns strontium green in the Workshop; a marker slides between nav items; the name shrinks a touch once you scroll; the title strip leans with scroll speed.
- Shelves (desktop): covers stand on a wooden ledge, turn toward the pointer and pull out of the shelf on hover; a soft spotlight follows the pointer; shelf names get a hand-ruled line that draws in with the scroll; each cover catches a glint as it arrives. Phones: a tick when a shelf settles on a book.
- The bigger-picture door: press and hold the button (a ring fills, "Keep holding"); two wooden doors swing open with light bursting from the gap; a seam of light under the door breathes three times when it comes into view. Keyboard and screen readers open it straight away; a tap closes it.
- Tools: cards tilt with a glare that follows the pointer; the Pattern Decoder scans its page on arrival and on hover; roots grow down from The Root as you scroll.
- Gates: verify-hub all pass (new: keyboard opens the door at once); design-gates 0 FAIL; axe clean; LCP 0.53 s, CLS 0, 256 KB.

### Batch 4 done (2026-11-21): threshold and Portals
- Threshold: as you scroll in, the page burns down to black from the edges (an ember ring closing in), "Worn in the light." dims as the light leaves while "Alive in the dark." gathers its glow, and six layers of phosphor stars come out as the dark deepens. All scroll-linked, nothing self-running.
- Portals: the glow is painted. Where the light touched is where it glows: hold and drag to paint light in; a still press spreads out from the finger and soaks the whole pendant in about a second. The afterglow fades on the same curve as before, with a soft bloom.
- Moving over a glowing pendant sheds sparks of afterglow; a glint follows the pointer (and the phone tilt on Android).
- Desktop: a faint UV lamp follows the pointer through the Workshop; passing over a pendant charges it a little where the light falls, so it glows faintly when you move away.
- The first full charge of the visit turns the rest of the page dark for about two seconds so that pendant glows alone (Leave now stays on top; skipped under Still and reduced motion).
- A charge-up hum (sound) was planned for the threshold scroll and left out: sound may only answer a tap.
- Gates: verify-hub all pass; design-gates 0 FAIL (stars moved off a canvas so nothing sits over text; transitions snap under reduced motion); axe clean; LCP 0.60 s, CLS 0, 266 KB. Live page DOM 252 KB of the 260 KB check budget.

### Owner round (2026-11-21): six sets, phone first
- Portals: six pendants from six different sets (Firmament, Bushido, Paradox, The Unwritten, Starseed, Evolution), photos from workshop/portals; frames now 4:5 to match the photos; copy now says each set glows its own colour. Regression row + check added first (failed on the old three gear pieces, passes now).
- Phone first (owner rule): shelves and the Portals row turn like a carousel under the thumb (the one in front sits larger), the phone ticks when the Portals row settles; tool cards catch a band of light and settle flat as they scroll past; section titles rise line by line on every screen.
- Batch 5 re-ordered for phones: the custom cursor drops to last; phone forms come first.
- Gates: verify-hub all pass; design-gates 0 FAIL; axe clean; LCP 0.61 s, CLS 0, 271 KB.

### Batch 5 done (2026-11-21): Workshop end, footer, site layers (phone first)
- NFC guide: a small scene above the label: a phone comes down onto a wax seal, the seal answers in rings, a note lights the screen (twice, then rests); the guide cover lifts like a page as it scrolls in.
- In the making: The Press seal stamps down with a bounce; The Casting draws its pour and figure.
- Visit counter: the digits roll into place like a departures board when it comes into view (screen readers hear the plain sentence).
- Footer: the signature writes itself across as the footer scrolls up; a "Back to the light" button returns to the top (the burn reverses with the scroll).
- Support buttons: a tap gives a double haptic and a few coins jump from the button.
- Every section title carries a small seal mark that turns as the page scrolls; each shelf takes a faint tint from its own covers; the paper grain drifts (stops under Still and reduced motion).
- The glow secret: type "glow", or tap "Alive in the dark." three times on a phone, and the lights go out with stars for about three seconds.
- Desktop only, last: a ring follows the pointer, grows over anything pressable, turns green in the dark.
- Fixed: the In-the-making icons had picked up the header switch style (class clash from batch 1).
- Check budget raised from 260 to 300 KB of live page (the owner set no number; LCP 0.64 s, 283 KB transferred).
- Gates: verify-hub all pass; design-gates 0 FAIL; axe clean; CLS 0.

### Batch 6 done (2026-11-21): the big items
- 6.1 The hero book has real thickness: a page block top and bottom, a back board, a thicker spine that catches more light as the book turns toward you.
- 6.2 Scrolling down from the hero, a copy of the cover flies and lands on its own place on the shelf (whichever book the hero shows; skipped when that shelf is far away). The caption under the book hides while it flies.
- 6.3 Desktop mouse wheels glide (about half a second per notch); trackpads, keyboards, scrollbars and phones keep native scrolling.
- 6.4 Shelves stack: each shelf slides over the one before, which sinks back and dims. Phone check: every shelf fits the screen, so nothing is hidden before it is covered. Off under Still and reduced motion.
- 6.5 Page turns: Tools, The Listening Room and the support panel arrive with a diagonal edge sweeping down.
- Gates: verify-hub all pass; design-gates 0 FAIL; axe clean; LCP 0.65 s, CLS 0, 289 KB.

### Critic v19 round 1 + the new opening (2026-11-21)
- Critic (docs/hub-redesign/critic-v19-round1.md, phone first): fixed stacked shelves hiding titles (stacking now desktop only, dimming starts late; phones get a gentle rise per shelf), flying cover over the chips (on phones it only drops in once the book has left the screen, never while the chips show), "Change answer" over-scaled (now a 16px text button), rhythm voids (phone section gaps capped at 72px; page turns desktop only; NFC scene centred and larger), grey pendant backdrops (faded to night around each pendant), brown band under the footer (night background), brand target under 44px when compact.
- Owner: "the first thing people see should ... not assume they are there for a book" and "Give a montage of my different logo images that settles into the main 4 door screen". New first screen: the name, the tagline and four doors (The Library, The Portals, The Listening Room, NFC guide), each door one of the owner's logo figures. On arrival the figures are dealt one after another (about 3.5 s), then the four for the doors fly into place. Any tap, scroll, key or focus skips; Still and reduced motion show the doors at once; a slow phone that starts late keeps the doors and never replays over them. The book chooser and book are now the Library's opening, with their entrance playing when scrolled to.
- Left out of the montage for now: the cannabis-wings figure (owner to decide; see the chat).
- Gates: verify-hub all pass (new: first screen = the name and four doors); design-gates 0 FAIL; axe clean; slow-4G 4x-CPU LCP 2.09 s (was 7.3 s before the late-start fix), CLS 0.

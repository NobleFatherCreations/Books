# 07 — Choosing and combining (the intelligence layer)

The names bible (06) tells you what exists. This file tells you **how to choose some and reject most, and how to combine them so the result looks designed, not burnt out.** Rules here are binding for any build that uses the catalogue.

## 1. Why outputs burn out (named failure modes)

Know these by name. Every critique round checks for each.

| # | Failure mode | What it looks like | Cause |
|---|---|---|---|
| F1 | **Effect soup** | Gradient + glass + grain + glow + particles + kinetic type on one screen | Choosing many "cool" items with no lead |
| F2 | **Collision** | Figure over text, label over text, anything under a header | Layers designed separately; no safe zones |
| F3 | **Specks for art** | Thin dots/lines as the "illustration", tiny, low contrast | No focal point, no mass, no colour weight |
| F4 | **Template default** | Cream/serif or dark/gold "premium" look any site could have | Picked a vibe, not a concept |
| F5 | **Hierarchy flatness** | Everything the same size and weight; nothing to look at first | No scale drama, no single focal point |
| F6 | **Motion without meaning** | Things drift/fade/parallax for decoration; nothing explains or orients | Animation added to "feel premium" |
| F7 | **Dead space** | Huge empty areas that read as unfinished, not as intentional silence | Empty stage with no anchor, no rhythm |
| F8 | **Fatigue** | Same intensity on every screen; the reader's eye never rests | No pacing; no quiet sections |
| F9 | **Style clash** | Brutalism next to Liquid Glass next to ornament | Two lead styles competing |
| F10 | **Cliché** | Obsidian-and-gold, sacred-geometry rings, neon-on-black because the topic "feels" mystical | Choosing the obvious semantic match |
| F11 | **Readability sacrificed** | Pretty but hard to read: low contrast, light weights, text on texture | Beauty prioritised over the reader |
| F12 | **Only works on the dev machine** | Fine in Chromium, broken on iPhone Safari | No real-device testing |
| F13 | **Wrong register** | Playful where grave, loud where the reader is stressed | Ignored reader state |
| F14 | **Inconsistent craft** | Radii, shadows, spacing, icon strokes vary screen to screen | No tokens |

## 2. The core rule: a design is a **small set of strong decisions** (the Budget)

Every finished design has exactly:
- **1 concept** — one sentence of *meaning*, not mood. ("A field guide drawn by someone who walked the territory." not "dark and premium.") Style choices must serve it.
- **1 lead style** (from 01 §A, or a named genre from 06 §1/§35). It owns the overall look.
- **1 supporting influence** (optional) — borrowed for texture or type, never competing structurally.
- **1 signature move** — the single memorable, repeatable gesture (a transition, a reveal, a type behaviour, a figure language). The reader should be able to describe it afterwards.
- **1 type system** — max two families (or one superfamily), a defined scale, one measure.
- **1 colour system** — neutrals + exactly one accent + semantic colours; dark and light both designed.
- **1 motion language** — 2–3 durations, 2 easings, 1 spring; named recipes.
- **A restraint budget**: at most **3 simultaneous "feature effects"** per screen (feature effect = anything decorative that draws the eye: gradient glow, blur glass, grain, particles, kinetic type, parallax, 3D, cursor effect, marquee…). Utility motion (focus, press, state change) does not count. Anything over 3 needs a written reason.
- **A novelty budget**: ≤ 1 genuinely unfamiliar interaction per page, surrounded by familiar patterns. Familiar nav, familiar controls, new *story* moves.
- **An intensity map** across the page: mark each section Loud / Medium / Quiet. A long page must have at least 30% Quiet sections and never more than two Loud in a row. Spectacle needs rest to read as spectacle.

## 3. The selection procedure (do in order; write it down)

1. **Brief → axes** (README). Write the reader's state first: the most vulnerable plausible reader sets the floor for calm, contrast, motion and safety.
2. **Concept sentence.** If you can't write one, stop and re-read the content.
3. **Derive constraints before browsing the catalogue**: platform (phone-first?), safety tags [SAFE], repo rules [SC]/[LIB]/[NET], performance budget, accessibility floor, content type, who it must NOT resemble.
4. **Long-list by category.** For each relevant category in 06, circle 5–10 names that *could* fit. Then **screenshot a real example of each** (Playwright on live reference sites or a CodePen/Codrops demo) and read the images. Never choose from a name alone.
5. **Score each candidate** 0–2 on: Meaning (serves the concept), Reader (fits reader state), Feasibility (in budget and constraints), Distinctiveness (not the default), Cohesion (works with the current lead). Drop anything scoring 0 on Meaning or Reader. Keep the highest totals.
6. **Reject on purpose.** For every strong-looking candidate you drop, write a one-line reason. This is as important as what you keep and is what stops effect soup.
7. **Assemble the set** using the compatibility rules below. Re-check the Budget (§2).
8. **Hero-first prototype** (one screen, phone size) → screenshot → critique → only then scale.
9. **Record** in `DESIGN-CHOICES.md` (template in README) with IDs, scores and rejections.

### Selection heuristics (quick tests)
- **Substitution test:** swap in a different brand's logo. If nothing feels wrong, the design is generic (F4).
- **Squint test:** blur the screenshot. One focal area should survive; if two compete, you have F5/F1.
- **Greyscale test:** hierarchy must survive without colour.
- **Remove-one test:** delete each decorative element in turn; keep it only if the screen is worse without it.
- **Explain test:** can you say what each motion *tells* the reader? If not, cut it.
- **Reader-state test:** would this be okay for someone stressed, tired, on a bad connection, or watched over their shoulder?
- **Real-device test:** iPhone Safari, mid Android, throttled network.

## 4. Compatibility rules (what combines, what clashes)

**Pairing a lead with a supporting influence**
| Lead | Pairs well with | Avoid pairing with |
|---|---|---|
| Swiss / International (S-01) | Editorial serif accents, mono labels, one bold colour, subtle motion | Ornament revival, glass, maximalism |
| Quiet-luxury minimal (S-22) | Modern serif revival (S-45), grain, slow fades, large photography | Neo-brutalism, loud gradients, bouncy motion |
| Editorial / long-read (B-23) | Annotated figures, marginalia, restrained colour, scroll-reveals | Heavy WebGL, kinetic everything |
| Cinematic (S-37) | Dark-first, film grain, slow camera moves, serif title cards | Bento grids, cute illustration |
| Scientific / cartographic (S-35/36) | Technical mono, thin rules, annotation lines, measured motion | Glassmorphism, neon |
| Neo-brutalism (S-20) | Mono, hard shadows, flat colour, snappy motion | Soft shadows, glass, slow fades |
| Liquid Glass / spatial (S-19/51) | Large-radius shapes, SF-like sans, spring motion, layered depth | Hard borders, grain, dense type |
| Dev-product dark (S-24) | Thin borders, mono accents, glow *used once*, tight grids | Warm paper, ornament |
| Kinetic-type-led (S-38) | Plain backgrounds, one accent, 1–2 images, big sans | Many other effects (F1) |
| Immersive WebGL (S-39) | Minimal UI chrome, strong typographic caption system, real fallbacks | Dense text, many cards |
| Sacred/ceremonial geometry (S-55) | Restraint; flat or ink-like line; slow motion | Gold-on-black default (F10), glow clichés |
| Calm/wellness (S-43) | Soft shapes, slow breathing motion, high-enough contrast | Fast kinetic type, hard cuts |
| Gov-grade plain (S-44) | Almost anything *quiet*; one distinctive type or colour decision | Spectacle |

**Structural clashes (never both as co-leads):** brutalism × glass; ornament × technical; maximalism × minimalism; playful illustration × solemn subject; skeuomorphic realism × flat; neon × calm.

**Layering order of authority** (when they conflict, higher wins): 1 safety and accessibility → 2 reader state and content → 3 concept → 4 lead style → 5 signature move → 6 decoration.

**Type × style:** serifs with high contrast suit editorial/cinematic/luxury; neutral grotesques suit Swiss/product; mono suits technical/brutalist; rounded sans suits calm/playful; avoid decorative display faces beyond one headline role. Max 2 families; one expressive, one workhorse.

**Colour × style:** choose the accent from the *concept*, not the genre. Defaults to avoid unless justified: gold-on-black, purple-blue neon, teal-orange. Use tinted neutrals (warm/cool) rather than pure grey. Dark mode is a separate design: lower saturation, lift surfaces by tint, reduce white weight.

**Motion × reader:** stressed or vulnerable readers get less motion, slower, no flashing, no sudden change; add a visible motion toggle; `prefers-reduced-motion` is a separate designed version, not "off".

## 5. Composing a screen (the layer cake)

Plan each screen top-down and check each layer is clear:
1. **Purpose** — what the reader does or understands here.
2. **Focal point** — one thing. Size and contrast establish it.
3. **Text zone** — designed first (measure, size, contrast), protected from collisions.
4. **Figure/visual zone** — has its own region, its own mass; it either owns the screen or sits beside/above the text, never beneath it. If a figure must sit behind text, add a scrim or reduce figure contrast in the text region, and verify by reading the screenshot.
5. **Navigation/utility** — fixed elements get opaque or blurred backgrounds; keep clear of safe areas.
6. **Motion** — what moves, why, in what order; stillness is a choice.
7. **Texture/atmosphere** — only last; grain/glow subtract from clarity if added early.

## 6. Pacing the whole page
- Map the arc: open (threshold) → build → turn → resolve → leave. Assign an intensity (Loud/Medium/Quiet) to every section.
- Alternate **statement screens** (one big idea, little text) with **reading screens** (calm, text-forward).
- Place the **signature move** at the opening and one other peak; don't repeat it every section.
- Give figures **a consistent visual language** across the page (same line weight, palette, shape grammar) — variety comes from composition and scale, not from changing styles.
- Plan the **ending** deliberately (handoff, next step, silence).

## 7. Proven combination recipes (starting points, not templates)
Each states concept-fit, ingredients, and the main risk. Verify with real reference screenshots before using.

- **R1 "Field guide":** Scientific plate (S-35) + editorial long-read (B-23) + hand-annotated figures (I-03) + marginalia (L-27). Calm, trustworthy. *Risk:* beige default (F4) → give it a distinctive ink colour and a strong type pairing.
- **R2 "Instrument":** Swiss grid (S-01) + technical/blueprint (S-34) + mono labels + precise micro-motion + dark/light parity. For tools/decoders. *Risk:* coldness → warm the accent and copy.
- **R3 "Cinematic essay":** Cinematic (S-37) + scrollytelling pinned stages (O-01) + serif title cards + film grain used once + slow dolly-style scale on scroll. *Risk:* over-long spectacle → intensity map, quiet reading screens.
- **R4 "Quiet crisis-safe":** Gov-grade plain (S-44) + one distinctive type decision + neutral default theme + Quick Exit + no motion by default. *Risk:* feeling bland → invest in typography and writing.
- **R5 "Atlas":** Cartographic (S-36) + map-as-navigation (L-23/N-02) + ring/orbit diagrams (I-03) + step-triggered fly-to (O-07). For maps of ideas. *Risk:* clutter → progressive disclosure, strong legend.
- **R6 "Monument":** Poster layout (L-16) + oversized grotesque (S-46) + one accent + minimal motion (kinetic type once). For manifestos/openers. *Risk:* shouting → quiet screens between statements.
- **R7 "Gallery":** Quiet-luxury (S-22) + photography/art-directed images + slow reveals + generous space. For work/portfolio. *Risk:* sameness → one surprising crop or interaction as signature.
- **R8 "Living figure":** One hero visualisation as the signature (particle/shader/3D) + restrained editorial type + captions in a safe zone. *Risk:* F3 specks, F2 collisions → give the figure mass, colour and a focal point; keep it out of the text zone; fallbacks.

## 8. Anti-cliché list (justify or avoid)
Gold-on-black "premium"; sacred-geometry-as-decoration; purple/blue gradient glow; floating glass cards on dark; centred hero + three feature cards; stock photo of a person with a laptop; generic "particles" backgrounds; fake 3D blobs with no meaning; uniform parallax on everything; cursor effects on a phone-first audience; AI-orb avatars for non-AI content; kinetic type for body copy; scroll-jacked slideshows; emoji as icons; arbitrary use of every trending style.

## 9. Acceptance criteria (a design is done when ALL are true)
1. The concept sentence and the choice record exist and match what is on screen.
2. `node scripts/design-gates.mjs <url> <outdir>` shows **0 FAIL**; every WARN is explained or fixed.
3. The screenshots were **read** (not just generated): at each of 10+ representative scroll positions on phone and desktop, in light and dark, you can describe what is there, and none shows F1–F14.
4. The substitution, squint, greyscale and remove-one tests pass on the hero screen and two others.
5. Reduced-motion and no-JS versions are designed and checked.
6. A real-device checklist (`PHONE-CHECK.md`) has been given to the owner, or a private preview exists for it.
7. Lighthouse/axe pass the budgets in 04 (Q, R, S).
8. The owner has seen the hero screen and approved the direction *before* the full build.

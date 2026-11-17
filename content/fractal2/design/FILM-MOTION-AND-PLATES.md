# Fractal² film: word motion and image plates

Date: 2026-11-17. Status: decision made, spec ready to build. Nothing here is wired into the film yet.
Owner request: make the words enter and leave "more cinematic throughout the video". Research award-level work first,
audit and steelman the ideas, then pick the one that adds the most visual value and feeling.

Scope of this document:
1. Research notes, with sources.
2. Five candidates, each steelmanned and audited.
3. The decision.
4. The implementation spec (timings, curves, variants, line assignments, reduced motion, low tier, MSDF match, machine checks).
5. The image plates: what was made, where each goes, how the shader uses it.
6. The opening emblem recommendation.
7. What was rejected and why.

---

## 1. Research notes

What the best title and web work does with words, and why it works.

**Saul Bass, Vertigo (1958).** Simple motion only: rotation, scale, repetition, timed tightly to the score.
Straight type set against slanted moving bars that wipe on and off. Lesson: restraint, and motion that carries the
film's idea (the spiral is the obsession). The type itself barely moves; the world around it does.
Sources: [Criterion, "The Father of the Title Sequence"](https://www.criterion.com/current/posts/6937-credit-where-it-s-due-the-father-of-the-title-sequence),
[Art of the Title, Saul Bass](https://www.artofthetitle.com/designer/saul-bass),
[Motion Archive, Vertigo](https://luckydumpling.github.io/motion-archive/entries/vertigo-title-sequence/).

**Kyle Cooper, Se7en (1995).** Jittery, scratched, hand-made type that puts the viewer inside a mind.
Lesson: the texture of the type's arrival is itself the meaning. Also a warning: that energy is wrong for a calm,
first-person confession. Source: [Art of the Title, Kyle Cooper lecture](https://www.artofthetitle.com/news/kyle-cooper-the-film-inside-the-film-lecture/).

**Patrick Clair with Elastic and Antibody, True Detective (2014, Emmy).** Double exposures, footage slowed to 10 to 20
percent so the titles feel "like living photographs", a slow build from light to dark. Lesson: slowness and
layering read as gravity. Words should feel like they surface out of the picture, not get stamped on it.
Sources: [Art of the Title, True Detective](https://www.artofthetitle.com/title/true-detective),
[Motionographer](https://motionographer.com/2014/01/24/patrick-clair-elastic-hbos-true-detective).

**Danny Yount (Six Feet Under, Sherlock Holmes, Iron Man).** Emmy-winning restraint on Six Feet Under: a few
held images and plain type with long, quiet dissolves. Lesson: a dissolve with a long tail can carry grief better
than any move. Sources: [Art of the Title, Danny Yount](https://www.artofthetitle.com/designer/danny-yount),
[Mental Floss interview](https://www.mentalfloss.com/article/77629/art-movie-titles-explained-designer-danny-yount).

**GSAP SplitText mask reveals (the web standard).** Split by lines or words, wrap each in a clip, slide the text up
from under the clip edge. Common staggers: about 80 to 100 ms per line, 50 to 60 ms per word, 10 ms per letter.
Lesson: staggering by phrase reads as speech; per-letter staggering reads as a gimmick and hurts reading.
Sources: [GSAP SplitText docs](https://gsap.com/docs/v3/Plugins/SplitText/),
[Osmo masked text reveal](https://www.osmo.supply/resource/masked-text-reveal).

**Blur-to-sharp focus reveals (Awwwards-level sites).** Text comes into focus instead of fading in: blur plus opacity,
staggered. Codrops' write-up of the Trionn site notes that pairing blur with opacity makes text "read as coming into
focus rather than just fading in". Sources: [Codrops, the architecture behind Trionn](https://tympanus.net/codrops/2026/07/15/the-architecture-behind-trionn-coordinating-gsap-three-js-lenis-and-web-audio/),
[Awwwards element, text blur reveal (Dolsten)](https://www.awwwards.com/inspiration/text-blur-reveal-dolsten-co).

**Tracking settle (trailer titles).** Letters start slightly wide and close to their set spacing while blur clears.
Codrops' trailer-style tutorial starts wide and sharpens at the midpoint. Lesson: a small settle feels like a lens
finding the plane; a big one feels like a movie trailer cliche.
Sources: [Codrops, text opening sequence](https://tympanus.net/codrops/2013/04/30/text-opening-sequence-with-css-animations/),
[21st.dev "Tracking In" component](https://21st.dev/@kapishdima/components/tracking-in.md).

**Light sweep / gradient mask reveal (Apple product pages).** A moving gradient mask reveals or brightens a headline
from one side. Observed on Apple pages by developers; Apple has not documented it.
Sources: [GreenSock forum, gradient reveal](https://greensock.com/forums/topic/27371-gradient-reveal-on-scroll/),
[SVGator, advanced masking](https://www.svgator.com/tutorials/advanced-svg-masking).

**Dissolve to dust / particles (WebGL).** MSDF text eaten by a noise threshold while particles leave the edge.
Lesson: powerful for a single moment, costly per frame, and the word is unreadable while it happens.
Sources: [Codrops, Gommage effect, MSDF text into dust](https://tympanus.net/codrops/2026/01/28/webgpu-gommage-effect-dissolving-msdf-text-into-dust-and-petals-with-three-js-tsl/),
[Codrops, dissolve effect with shaders and particles](https://tympanus.net/codrops/2025/02/17/implementing-a-dissolve-effect-with-shaders-and-particles-in-three-js/).

**Active Theory (Halo 5 visualizer).** Kept readable text in a crisp DOM overlay because 3D canvases render at reduced
resolution on most devices, then handed off to 3D text for the effect moment. This is exactly our split: DOM captions
for reading, MSDF words in the picture. Source: [Active Theory on Medium](https://medium.com/@activetheory/xbox-halo-5-guardians-visualizer-5b9afcb542f1).

**Lusion and Immersive Garden (storytelling WebGL studios).** Their story sites keep text plain and let the picture
carry the effect. Sources: [Codrops, Lusion profile](https://tympanus.net/codrops/2026/04/13/lusion-where-digital-craft-meets-ambitious-experimentation/),
[Awwwards, Immersive Garden case study](https://www.awwwards.com/case-study-immersive-gardens-new-website.html).

**Accessibility.** WCAG 2.3.3 (Animation from Interactions) and technique C39: honor `prefers-reduced-motion`.
Sources: [W3C Understanding 2.3.3](https://w3c.github.io/wcag/understanding/animation-from-interactions.html),
[W3C technique C39](https://www.w3.org/WAI/WCAG22/Techniques/css/C39.html).

What the research agrees on: the best serious work moves the type very little and very slowly, ties the move to the
film's idea, staggers by phrase rather than letter, and saves the big effect for a few moments.

### How words move now (audited from `engine.js` and `template.html`)
- Captions: two DOM slots alternate. Each phrase group (`.g`) rises 16 px and fades in over 700 ms with a cubic
  ease-out, staggered by `clamp((t1 - t0) * .5 / n, 160, 500)` ms.
- Exit: the whole caption fades over 600 ms (220 ms for one-word captions), rises 34 px and shrinks 5 percent.
- The dark pool arrives 450 ms before the words.
- It is clean and readable. It is also the default web reveal: every word arrives the same way, the exit rises the
  same direction as the entrance (it reads like a slide being dismissed), and nothing in the motion says anything
  about this story.

---

## 2. Five candidates

Fixed constraints for all: one caption at a time, readable for the required time (`need = .35 n + 1.2` s), 4.5:1
contrast while held, reduced motion gets a plain fade, runs on a phone, frames are a pure function of the film clock,
DOM captions animate only transform, opacity, filter, clip-path or mask. MSDF words may use shader effects.

### A. Focus pull (blur to sharp, small rise, tracking settle; exit racks out of focus)
- **Steelman.** It is what an eye does when it finds something. The film is about attention: "It does not need your
  belief. It only needs your attention", "finally seeing clearly", "the end of not-seeing", "the signal showed beneath
  the noise". Every caption arriving as a focus pull says that sentence without a word. It is the language of real
  cinema (a rack focus), not of web UI. It reads early: text is legible once blur is under about 2 px, roughly 300 ms
  in. It costs one filter per phrase group for under a second. The exit as a rack out of focus gives a real handoff:
  one plane goes soft, the next sharpens.
- **Audit.** Cost: CSS `filter: blur()` on large serif text is a GPU pass per element; on a weak phone six blurred
  groups at once can drop frames. Fix: blur only during entry and exit, cap at six filtered elements, drop blur on the
  low tier. Cliche risk: medium. Blur reveals are fashionable; at 10 px or more with letter-by-letter staggering they
  look like a template. Fix: phrase-level only, radius tied to font size (0.16 em), short. Legibility: good once
  settled; the risk is a long blur tail, so the curve must be fast-out. Fit: the strongest of the five.

### B. Mask line reveal (SplitText style: text slides up from under a clip edge)
- **Steelman.** The proven award-site standard. Crisp at every frame, no blur cost, deterministic, cheap on phones.
  Reads as precise and editorial.
- **Audit.** Our groups are phrases, not lines, and captions use `text-wrap: balance`, so per-line clips need a layout
  pass on every resize and can cut descenders of the serif. The hard edge reads as interface, a product page, not a
  confession. It says nothing about this story. Cliche risk: high (it is on most agency sites). Fit: weak.

### C. Light sweep (the film's one light passes across the words)
- **Steelman.** The film has one light and it is the Frequency. Words lit by that light echo the whole argument: the
  light was always there; the words become visible as it reaches them. Apple uses the same idea for its biggest
  headlines. At the three PEAK anchors it could land exactly on the music.
- **Audit.** Animating `mask-position` or a gradient repaints every frame (not compositor-only), which is the most
  expensive DOM option on a phone. Each caption is only fully readable after the sweep passes the last word, which
  costs reading time on every one of 171 captions. The light sits in a different place in each shot, so the sweep
  direction would change or lie. Over 18 minutes it becomes a gimmick. Fit: excellent for three moments, poor as the
  base system.

### D. Words form from dust and return to dust
- **Steelman.** Echoes the dust plate and the opening black-with-one-light. "Dissolve into who you think you are",
  "The thread sinks into the light and disappears inside it", "I shed it one inversion at a time" are literal dust
  lines. Award-level WebGL work does this beautifully with MSDF text.
- **Audit.** DOM captions cannot do it; the words would have to be drawn twice (MSDF effect over DOM text), which risks
  double images and breaks screen-reader parity rules. Each word is unreadable for about 800 ms during formation, which
  eats the readable-time budget. Particle count per caption is heavy on phones. Over 171 captions it would exhaust the
  viewer. Fit: right for a few MSDF moments in the picture, wrong for captions.

### E. Depth rack (caption arrives from in front of the lens and recedes behind)
- **Steelman.** Gives true depth: the incoming caption starts slightly large and soft as if in the foreground, settles
  on the plane; the outgoing one shrinks and softens into the distance. Strong sense of a camera.
- **Audit.** Scaling large serif text 4 to 8 percent shimmers and re-rasterizes on phones, and big scale moves read as a
  zoom transition from presentation software. It doubles the cost of A (scale plus blur). Its best part, the exit
  receding while the next arrives sharp, can live inside A. Fit: medium.

---

## 3. Decision

**Chosen: A, the Focus Pull, as one system with six small variants tied to meaning.** Every caption comes into focus
phrase by phrase and leaves by going out of focus and drifting a few pixels toward the light. The three PEAK lines get
one pass of the light (C) across the settled words, landing on the music anchor. Inversion lines arrive as a pair:
the gold original rises into focus, the grey copy arrives after it, from the opposite side, with a flat mechanical
curve. The STOP line does not move at all.

Why A won: it says the film's thesis (attention, seeing clearly) in every caption, it is real cinema grammar, it reads
in about 300 ms, and it costs nothing once a caption is settled.

Why the others lost:
- **B, mask reveal:** generic, reads as product UI, needs per-line layout we do not have, says nothing about the story.
- **C, light sweep (runner-up):** the most meaningful single idea, but too slow to read and too costly to run on 171
  captions, and the light moves between shots. Kept as the PEAK variant only, where its cost and delay are worth it.
- **D, dust:** wrong medium for DOM captions and too slow to read. Kept for MSDF words at four named moments (below).
- **E, depth rack:** shimmer and cost on phones; its useful half (the receding exit) is folded into A's exit.

---

## 4. Implementation spec

All motion is computed in `captions(t)` from the film clock, as now. No CSS transitions or animations on captions.
Times below are in ms from the named event. `em` means the caption's computed font size in px (read once per layout,
cache it on the element with the existing `capBuild`).

### 4.1 Curves (implement as a deterministic cubic-bezier solver, 8 Newton steps, no lookups by wall time)
| Name | cubic-bezier | Used for |
|---|---|---|
| `focus` | (.16, 1, .3, 1) | blur clearing, rise, settle (fast start, long soft landing) |
| `fade` | (.33, 0, .2, 1) | opacity in |
| `out` | (.5, 0, .75, 0) | exit blur and opacity (slow start, then gone) |
| `copy` | (.45, 0, .55, 1) | the grey counterfeit groups (flat, mechanical) |
| `sweep` | (.45, 0, .55, 1) | the PEAK light pass |

Rounding: translate to device pixels (as now), blur to 0.25 px, opacity to 3 decimals. When blur rounds to 0, set
`filter: none` (never leave `blur(0px)` on a span; it keeps a GPU layer alive).

### 4.2 Variant O, ordinary lines (the default; about 140 of the 171 captions)
Per phrase group k (0-based), entry starts at `g0 = t0 + k * stag`, with
`stag = clamp(550 * say / n, 120, 420)` ms, where `say` is the caption's spoken seconds and `n` its group count
(the words keep pace with the voice).

| Property | From | To | Duration | Curve |
|---|---|---|---|---|
| opacity | 0 | 1 | 520 | fade |
| filter blur | 0.16 em (about 9 px at 56 px type) | 0 | 720 | focus |
| translateY | 0.30 em | 0 | 900 | focus |
| scaleX (the tracking settle, origin center) | 1.035 | 1 | 900 | focus |

Hold: no motion at all. The words sit still while read.

Exit, applied to the whole caption element (one filter, not per span), starting at `t1`, lasting `out` = 560 ms:
| Property | From | To | Curve |
|---|---|---|---|
| opacity | 1 | 0 | out |
| filter blur | 0 | 0.10 em | out |
| translate | 0 | 0.14 em toward the light (see below) | out |
| scale | 1 | 0.985 | out |

"Toward the light": unit vector from the caption's center to the film light on screen (`S.lx`, `S.ly`, already in
the shot state), clamped so the vertical part is never downward; when `S.light` is 0 use straight up. This makes every
exit drift to the one light, a quiet echo of the ending.

Handoff: captions never overlap. The exit must end at least 80 ms before the next caption's first group starts
(the current build already sets `t1 = min(next.t0 - out - .08, ...)`; change `out` from .6 to .56). The pool (dark
ground) holds between two captions when the gap is under 1200 ms, so the ground does not pump. Read as one move: the
old plane goes soft, a breath of nothing, the new plane sharpens.

### 4.3 Variant W, one-word captions (section 2: "Idealize." "Hook." "Devalue." "Confuse." "Isolate." "Extract." "Discard." "Replace.")
One group. Opacity 0 to 1 in 300 ms (fade), blur 0.12 em to 0 in 380 ms (focus), translateY 0.18 em to 0 in 480 ms
(focus), no scaleX. Exit 220 ms opacity only, no blur (the next word follows in about 1.2 s). The matching ring in
the picture lights on the same frame the word's opacity crosses 0.5.

### 4.4 Variant Q, quoted inversion lines (caption has `qn > 0`; gold groups `.q`, grey groups `.x`)
Section 6: "“I will never leave you” becomes Discard.", "“You are loved.” And then it extracts.",
"“You are safe.” And then it watches.", "“You belong.” And then it isolates.",
"“You are whole.” And then it sells you the missing piece.", "“Come home.” And then it charges rent."
Section 11: "“It made me who I am.”" (all gold, no grey groups; it is his own voice, so it uses the gold half only).
- Gold groups: exactly variant O, rising from below (+0.30 em).
- Grey groups: start `220 ms` after the last gold group reaches readable (blur at or under 1.5 px and opacity at or
  above 0.9). Opacity 0 to 1 in 420 ms with `copy`; blur 0.10 em to 0 in 420 ms with `copy`; translateY from
  **minus** 0.30 em to 0 (it arrives from above, the mirror of the gold); no scaleX settle (a copy does not breathe).
- Exit: as O, but the grey groups start their exit 120 ms before the gold groups, so the original is the last thing
  seen.

### 4.5 Variant P, the three PEAK lines (focus pull plus one pass of the light)
- Section 5, PEAK1: "That is when I understood the size of it."
- Section 7, PEAK2: "So I stopped trying to climb out, and I went down."
- Section 10, PEAK3: the second half of the split line, "one block at a time, and let the light through."
  (the first half, "I only moved what had been stacked against the window,", stays variant O).

Entry as O with `stag` times 1.3. Then a light pass: a second, absolutely positioned copy of the caption
(`aria-hidden`, color `#FFF6E2`, `text-shadow: 0 0 .35em rgba(255,214,140,.55)`), masked by
`mask-image: linear-gradient(90deg, transparent 0, #000 42%, #000 58%, transparent 100%)` with `mask-size: 40% 100%`,
`mask-repeat: no-repeat`. `mask-position-x` runs from minus 40 percent to 140 percent over 900 ms with `sweep`. The
pass is timed so its center crosses the caption's center on the exact music mark (`marks.PEAK1/2/3`). Direction:
from the side the film light is on, toward the far side. The copy's opacity is 0 outside the 900 ms window. Exit as O.
This is the only place the mask animates; three times in the film.

### 4.6 Variant S, the STOP line (section 4: "Then the map turned around and looked at me.")
Everything stops. No blur, no translate, no scale, no stagger. Whole caption opacity 0 to 1 over 900 ms, linear,
starting on `marks.STOP`. Exit as O but without blur and without drift (opacity only, 700 ms). The stillness is the
effect, and it only works because every other line moves.

### 4.7 Variant F, the first and last lines
- Section 1: "It started with a question." (the first words of the film)
- Section 11: "It started with a question." and "Now the map is yours."

Slow focus: blur from 0.22 em to 0 over 1150 ms (focus), opacity in over 800 ms (fade), translateY 0.30 em over
1300 ms, `stag` times 1.5. Section 11's "It started with a question." exits into the light: over 1400 ms, blur 0 to
0.30 em, `filter: brightness(1)` to `brightness(1.35)`, opacity 1 to 0 (out). "Now the map is yours." never exits; it
stays with the Enter button to the end, as now.

### 4.8 BIG lines (`.big`: "Why do I keep living...", "It must be me.", "What if it isn’t me?", "I am still looking.", "That is the fractal.", "My original frequency.")
Variant O. Because blur and rise are in em, they scale with the type. No other change.

### 4.9 Reduced motion (`prefers-reduced-motion: reduce`)
No blur, no translate, no scale, no stagger, no light pass. Whole caption opacity 0 to 1 over 400 ms (linear) at
`t0`; exit opacity 1 to 0 over 300 ms at `t1`. Variant S, W and F use the same plain fade. MSDF words: opacity only,
same 400/300 ms.

### 4.10 Low tier (engine `tier === 2`, and any device where the frame-time monitor drops a tier)
Drop all `filter` use (blur and brightness). Keep opacity, translateY and scaleX per group, same timings. Light pass
replaced by nothing (the PEAK line is variant O on the low tier). Reduced tier (`tier === 1`): keep blur but cap at
four filtered spans at once (the fifth and later groups enter without blur).

### 4.11 MSDF in-picture words (tables in sections 3 to 11), matched through the existing per-word fx
Use the same curves and the same em ratios, mapped to `fx = {dx, dy, a, s, sy, soft}`:
- Entry, per word, 720 to 900 ms: `a` 0 to 1 (fade, 520 ms), `soft` 1 to 0 (focus, 720 ms; `soft` already widens the
  distance-field edge, so it is the blur), `dy` 0.30 em to 0 (focus, 900 ms), `s` 1.035 to 1 with `sy` 1 (the settle).
  Stagger 60 ms per word inside a row, 140 ms between rows.
- Exit, 560 ms: `a` to 0, `soft` to 0.6, `dy` minus 0.14 em (up, toward the light), all with `out`.
- Inversion tables (section 6, TABLE 3, 4, 5): gold word enters as above; grey word enters from the opposite side
  (`dy` sign flipped) with `copy`, no settle. In TABLE 4 the grey word slides to the seam and stops exactly at the
  glass (see the seam split plate below).
- Lit by the light: in the text fragment shader, add `col.rgb *= 1. + .12 * smoothstep(1.4, 0., dist(glyph, light) / lightRadius)`.
  Words nearest the one light are a little brighter. Cheap and always on (off on low tier).
- Dust (candidate D) is used only here, at four moments: section 6 NAMES ("the false god, the devil, the adversary,
  the matrix, the machine, the system": each name dissolves to dust as the next forms in the same spot); section 7
  "I shed it one inversion at a time" (the falling words dissolve); section 11 "The thread sinks into the light and
  disappears inside it"; section 11 "And then it dissolves into who you think you are." Dust words hold readable for
  their full need time before the dissolve starts; dissolve 900 ms, noise threshold driven by the clock.

### 4.12 Machine checks (add to the film gate; all run from the pure caption state at sampled clock times)
1. **Readable time.** Export `capState(i, t)` from the engine. For each caption, `readable_at` is the first t where
   every group has blur at or under 1.5 px and opacity at or above 0.9. Assert `t1 - readable_at >= need`. Fail lists
   the slug.
2. **Readable fast.** Assert `readable_at - (t0 + last group start) <= 420 ms` for variants O, Q, P; 1300 ms for F.
3. **Contrast during hold.** In capture mode, at `(readable_at + t1) / 2`, read the canvas under the caption box,
   take the 95th percentile luminance with the pool applied, and assert ink `#F3ECD9` against it is at least 4.5:1.
   Same check for grey groups `#BFC4D2` and gold `#F1CF8D`.
4. **No overlap.** Sample every 1/60 s across the whole film: at most one caption element with opacity above 0.02;
   the incoming caption's first group stays at opacity 0 until the outgoing caption reaches 0.
5. **Determinism.** Render frames at 40 fixed times twice, once seeking forward and once seeking backward; caption
   inline styles and canvas hashes must match exactly.
6. **Reduced motion.** With `reducedMotion: 'reduce'`, every caption span in every sampled frame has `filter: none`
   and no translate or scale in its transform.
7. **Filter budget.** No frame has more than six elements with a `filter` set; no caption has a `filter` set during
   its hold.
8. **PEAK sync.** The light pass center crosses the caption center within one frame (16.7 ms) of `marks.PEAK1/2/3`.
9. **Exit direction.** Exit translate never has a downward component.

---

## 5. Image plates

All plates live in `design/fractal2/film/plates/`. None are wired into the build yet. They are 3072 px masters;
the build should make webp copies (2048 px for desktop, 1024 px for phones and the reduced tier) rather than ship the
PNGs. The film draws every word; no plate contains text.

### 5.1 New this round
| File | What it is | Verdict |
|---|---|---|
| `fractal-8.png` (3072 sq) | Dark twin of the map as a wordless engraved medal: exactly eight bands (five deep crimson enamel inside, three midnight blue outside) separated by tarnished gold hairlines, guilloche texture, plain outer rim, a dark hollow at the center with one faint gold point. | Good. The best plate in the set. Ring count verified by a radial scan. Band 4 is smooth where the others are engraved; acceptable. |
| `frequency-8.png` (3072 sq) | The light twin, made as an edit of `fractal-8` so the geometry matches: polished ivory and pearl bands, bright pale-gold hairlines, a soft glowing center, warm cream ground. Exactly eight bands, no dots. | Good, slightly flat: the center glow is soft, more ceiling medallion than sun. The shader's own light should supply the radiance on top. Registration with `fractal-8` checked by edge correlation: best fit is scale 0.998, zero offset. The rings line up at a hard seam (preview below). |
| `city.png` (3072 sq) | 4K upscale of the old city plate. Same composition, sharper line work. | Good and faithful. Mean luminance 39.1 vs 38.4 before. Original kept as `city-1k.png`. |
| `shaft.png` (1714 x 3072, 9:16) | 4K upscale of the old shaft plate. Same composition, finer strata. | Good. About 14 percent brighter than the original (mean 34.9 vs 30.5) and a touch warmer; multiply by 0.87 in the shader to match. Original kept as `shaft-1k.png`. |

Ring geometry for `fractal-8` and `frequency-8` (shared). Center in texture UV (y down): (0.500, 0.513). Radii as a
fraction of half the image width, measured on the gold hairlines:
`0.157 (edge of the central hollow), 0.232, 0.322, 0.404, 0.488, 0.572, 0.645, 0.755, 0.860 (outer hairline)`,
rim to 0.905. Band k (1 to 8, inside out) is between edge k and edge k+1. Tolerance about 0.005.

### 5.2 Where each plate goes and how the shader uses it
- **`fractal-8`, section 2 ("One map").** Behind the ring-lighting: all bands at 25 percent brightness, band k rises
  to 100 percent on the frame its stage word (variant W) crosses 0.5 opacity. In the shader: radial mask from the radii
  above, `smoothstep` 0.004 wide at each edge. Lit by the light: multiply by a falloff from the light position so the
  side nearest the light catches a little more.
- **`fractal-8`, section 6 TABLE 3 ("Each ring shows the gold original, then turns over to the grey stage").** Per band:
  start with the band tinted toward gold (mix with `frequency-8` at 35 percent inside that band only), then turn it
  over: a 600 ms horizontal squash (`uv.x` scaled about the center, 1 to 0 to 1) during which the band's color swaps to
  desaturated pewter (mix 80 percent toward luminance, times 0.85). No new art needed; the grey is the same plate,
  drained.
- **Seam split, section 4 ("Then the map turned around and looked at me") and section 6 TABLE 4 (the mirror).**
  Live in the shader, not a separate image: left of a vertical seam sample `fractal-8`, right sample `frequency-8`,
  same UV. Seam: 1.5 px core of `#FFF6E2` with a gaussian glow (sigma 5 px at 1024 px plate size), color `(1, .92, .75)`.
  In TABLE 4 the grey counterfeit word walks toward the seam and stops at it; the gold word sits in the light half.
  Because the twins register, every ring crosses the seam unbroken, which is the point: it is the same structure,
  inverted.
- **`fractal-8` to `frequency-8` dissolve, section 10 ("The window") into section 11.** As the thirty dark blocks lift,
  dissolve band by band from the center outward: band k flips when `t` passes block-lift k times 30 / 8 of the way
  through. Inside each band, a soft radial wipe 0.02 wide, not a flat crossfade (flat crossfades of light and dark
  through grey look muddy; see `preview-dissolve-50`). On PEAK3 the last band flips and the shader's light blooms.
- **`frequency-8`, sections 8 and 9 (the light holds; "you're right").** A very low (12 to 18 percent) layer behind
  the light, rotating 0.5 degrees per second, pulsing 4 percent brighter on each "you're right" beat. Captions stay on
  the dark pool, so contrast is unchanged.
- **`city`, section 5 ("The architecture").** The far larger map the first one becomes the hub of: parallax layer at
  0.6 of camera speed during the pull back.
- **`shaft`, section 7 ("The descent").** Vertical parallax, scrolling upward as the camera falls; multiply by 0.87
  for the brightness match; fades to black as the descent slows.
- **Single ring textures for stage pairs:** not separate images. Crop band k from either twin in the shader
  (annulus mask from the radii) and unwrap it with `atan` to a strip if a straight bar is needed.

### 5.3 Older plates, status
- `frequency.png` (the earlier light plate, about nine bands and scattered dots): superseded by `frequency-8` anywhere
  rings must match. Keep only as a soft background glow if wanted; do not dissolve between it and the map.
- `frequency-draft.png`: retire.
- `dust`, `mirror`, `rings`, `sky`, `basalt`: unchanged this round.

### 5.4 Viewing copies (scratch, about 1024 px JPEG; may be cleared by a restart)
In `/tmp/claude-0/-home-user-Books/8b9d7146-764b-5ea4-b071-28c59584ded5/scratchpad/ad/`:
`view-fractal-8.jpg`, `view-frequency-8.jpg`, `view-city.jpg`, `view-shaft.jpg`, and the shader previews
`preview-seam-split.jpg`, `preview-dissolve-50.jpg`, `preview-grey-counterfeit.jpg`.

---

## 6. Opening emblem

The entry screen shows "Fractal²" over the live map emblem (the real rings and words, drawn in WebGL and slowly
turning), "Begin here", and the play ring.

- **Steelman for a new emblem.** The first five seconds are busy: thousands of tiny red and blue words sit behind the
  title and compete with it. A simple seal (eight rings, one bright point) would be calmer, more iconic, and could
  double as the share image and favicon. `fractal-8` is in fact a ready candidate.
- **Steelman for keeping the current one.** It is the real map, the film's actual subject, not a picture of it. It is
  alive (it turns), it is already wired into the launch (the title breaks into points that become stars), and it is
  the same object the viewer will see built ring by ring in section 2. A raster seal cannot do any of that, and it
  would give the project two different "maps" in the first minute.
- **Recommendation: keep the current emblem.** Do not generate new candidates. Fix the busyness instead: during the
  entry, draw the word rings at 55 percent of their current brightness inside a radius of 1.3 times the title width,
  and keep the single moving bright point. Optionally, use `fractal-8` (cropped to the disc, on black) as the share
  image only, where a still is all you get.

---

## 7. Rejected, and why
- **A separately generated split plate (dark half, light half).** Made live in the shader instead from the two
  registered twins: free, sharper, and the seam can move.
- **A matched pair of single-ring textures.** Cropped from the twins in the shader; a separate pair would not match
  the radii.
- **Eight stage illustrations or thirty technique illustrations.** Against the brief and against the film's look; the
  words are the picture.
- **New opening emblem candidates.** The audit favored keeping the live emblem (section 6), so no credits were spent.
- **Per-letter staggers, large tracking moves, glitch or chromatic aberration on captions.** Read as trailer or
  template cliches and hurt reading in a serious first-person story.
- **Mask line reveals as the base system.** Generic, and reads as product UI (section 2, B).

## Credits (Artlist)
Spent 800 of a 3,000 budget: two 4K upscales (city, shaft) and two plates (fractal-8, frequency-8), 200 each.
No call needed a cost confirmation; nothing was skipped for cost. Account balance after this round: 10,300 credits
(11,100 before).

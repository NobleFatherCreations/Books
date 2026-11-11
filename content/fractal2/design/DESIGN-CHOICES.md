# DESIGN-CHOICES: Fractal² intro. Three directions (all share the camera engine and fixed text/art)

Scores 0-2 (Meaning, Reader, Feasibility, Distinctiveness, Cohesion).

| Direction | Concept | Lead style | Signature move | <=3 feature effects | Score |
|---|---|---|---|---|---|
| **A. Survey Plate** | The reader is looking through an instrument. Every zoom level is a labelled "figure". | Annotated scientific plate (04 chart annotation: crosshair, ticks, leader lines, direct labels), ink + paper white + one vermilion; Plex Mono captions | A live HUD caption that names what is in view and the scale ("FIG. 1 THE FRACTAL, 30 techniques, x4.8" ... "FIG. 3 ATLAS, 30 sectors") | camera zoom; HUD caption; stage-ring highlight | M2 R2 F2 D2 C2 = 10 |
| **B. Title Sequence** | A film that happens as you scroll. | Cinematic letterbox, subtitle-style lower-third captions, big title card; white on black, no gold | Letterbox bars that open on the "Then I looked closer" beat | camera zoom; letterbox open; caption fades | M2 R1 F1 D2 C2 = 8 (phone reading in subtitles for 1,400 words is a strain) |
| **C. Field Guide** | A long essay with a diagram beside it (current v6). | Editorial column + diagram; Fraunces + Cormorant, gold accent | The camera pull-back | camera zoom; point field; atlas | M2 R2 F2 D0 C2 = 8 (F4/F10: this is the default look) |

Recommendation: **A**, because it adds the one thing the brief asks for that v6 lacks ("complete clarity": labelling what is in view) and removes the gold-chrome default. B is the strongest single moment but weakest for reading; its letterbox-open can be borrowed into A as a one-time beat if wanted.

Rejected on purpose: gold buttons/kickers on the page (F4/F10); particle dust with no meaning (F1); WebGL (F12, cost); sound (safety).
Intensity map target: Quiet >= 30% (the four text-free beats are Quiet; the reading stretches are Calm; the pull-back and plunge are the only Loud).

---

# v9 (2026-11-11): "One light". Merge of the original Fable intro (v1) into the v8 camera

Owner direction: get one beautiful intro finished by adapting the original intro into the fractal-background idea; cinematic; push live. No interview and no three-comp round this time: the direction was given, and the owner has said not to ask design questions.

**What the two builds each had (read from frame walks of both, `scripts/frame-walk.mjs`):**

| | v1 (original Fable intro) | v8 (live before this) |
|---|---|---|
| Strong | One gold point = you, present in every figure. Figures that MEAN something (defenses struck out one by one, a chain with one link broken, counterfeit beside original). A closing return to the first room. | The owner's own art, one continuous camera, locked black-circle opening, large word-by-word captions, the fall to black. |
| Weak | Paper-white essay, 4,700 words, 108 screens, figures small and dotted (F3 specks). | Captions on top of ring lettering (F2). One static picture for 45% of the scroll (F7, F8). Faint spark. Narrator's ending had no callback. |

**Concept (one sentence of meaning):** the whole map is drawn around one small light, and the last thing left when everything else is gone is that same light.

**The Budget (07 section 2):**
- Lead style: cinematic scale journey on the owner's art (06 section 35 "scale journey (powers of ten)", section 36 "dolly-in/out"). Unchanged from v8.
- Supporting influence: v1's figure language, redrawn as lines of light in the map's own coordinates (06 section 35 "build-up: add one element per step").
- Signature move: **the one light.** It is placed at the center on the line "Now put one person at the center of it", every figure is built around it, and at the fall to black it is what remains and grows. v8's spark was an effect; in v9 it is the payoff of a thing the reader has watched for three minutes.
- Type: Cormorant (captions) + Source Serif (door). Unchanged.
- Colour: the art's own colours; overlays in paper white only; warm light reserved for the person, the open gate and the old-words rings. No new accent.
- Motion: one damped camera (160 ms time constant); words rise 14 px with 3 px blur; figures draw with scroll. No timers except the breathing of the light.
- Feature effects per screen: camera + caption + at most one figure. The star field is the only ambient effect.
- Novelty budget: the Play button (auto-scroll at reading pace) is the one unfamiliar control; any touch hands the scroll back.
- Intensity map: Quiet (room) / Medium (stages) / Quiet (hold at fit) / Loud (pull-back) / Medium (danger figures) / Quiet (old words, why, work) / Loud (descent) / Quiet (black, the light) / Medium (atlas). Quiet is about 45%.

**Figures and what each one says (each is tied to one caption; none is decoration):**
| Cue | Figure | Borrowed from v1 |
|---|---|---|
| "A tactic alone is only a move. What gives it force is the combination." | Eight single points appear on eight rings, then one line joins them in order | The chain |
| "Now put one person at the center of it." | The light appears; a ring with five openings forms around it | "You" + the defenses |
| "Warmth..." / "A deadline..." / "Isolation..." / "This is how a person is unmade" | The openings close one at a time; a second wall seals; the light dims | Defenses struck out one by one |
| "Two hundred and three so far" | 203 threads cross the rings | The list of combination names (kept as words in the caption) |
| "an order can be read backward" | The lit thread is retraced from its last link to its first and returns to the light | "Break one" |
| "It gives you a place to start." | One opening returns, with light through it | new |
| "Grace becomes flattery..." | The eight rings light in order as each original is named | Counterfeit beside original |
| "Your original frequency." | Everything is black; the same light grows | The gold point at the end of v1 |
| Last two captions | The return to the room ("That tightening was never your weakness") | v1's closing passage, shortened |

**Layout decision (the fix for text-over-art):** while the camera is inside the original (opening, stages) words sit in a soft dark pool at the center, which is where the art's own black circle is. From the large map onward the map moves up (phone) or right (desktop) and words stand beside it, so figures stay fully lit while their caption is read. At the end the light owns the center and words drop below it.

**Rejected on purpose:** labels on the defenses ("your guard", "your witnesses"): the owner's rule is that the background is not for reading. A lens-flare streak on the light (tried, read as a cheap line, removed). Sound. Colour-coding the harm in red (a second accent). Showing the light from the first frame (it would sit on the title lettering as a blemish; it enters when the script gives it meaning).

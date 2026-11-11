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

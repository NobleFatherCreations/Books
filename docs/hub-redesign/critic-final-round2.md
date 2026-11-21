# Critique, round 2

Tests were run again at 1440x900, at 390x844 (touch) and with reduced motion (`scratchpad/crit2/`).

- No page errors.
- No link or button under 44px.
- After tapping an answer the page moves 100px on desktop, 177px on phone and 0 with reduced motion.
- The title strip moves for about 4s and then stops (pixel diff once per second). It does not move with reduced motion.
- The header is solid. Nothing shows through it at 200px or 400px of scroll (dscr.jpg, ph.jpg).

| Area | Score | Evidence, and the exact change still needed |
|---|---|---|
| First impression | 4 | The entrance plays, but most of it has finished by about 150ms (dent.jpg, frame 1 is nearly final), so it reads as tidy rather than bold. Change: lengthen it to about 1.1s total. Space the headline lines about 140ms apart with an expo-out ease, and start the book drop about 500ms in. |
| Hierarchy | 5 | The answer opens inside the hero and the book changes to the right title (dscr.jpg, frame 3). |
| Typography | 5 | Muted text is now readable on both screen sizes (ph.jpg). Gloock is used well. |
| Colour | 4 | See (a). Change: add a caption under the Portals row, such as "Photographed glowing. Strontium glows blue or green depending on the pigment.", so the blue reads as true rather than off-brand. |
| Composition/rhythm | 4 | The shelves alternate now (desktop-strips, columns 1–2). New problem: on desktop the answer card squeezes three picks into narrow columns. "335 tactics…" wraps to 7 lines and the titles break after one or two words (desktop-strips, column 1). Change: at 1024px and wider, stack the picks as three full-width rows inside the card, or set each column to at least 220px. |
| Imagery | 5 | I accept (b): the guide's real cover is the honest image. |
| Interaction & motion | 4 | The page now moves only far enough to show the card. The answer that turns the book is the best moment on the page. The cover swing is still desktop only. Same fix as First impression. |
| Phone ergonomics | 5 | All targets are 44px or more, the whole question fits the first screen, and nothing collides with the header (ph.jpg). |
| Brand specificity | 5 | "176 songs, back soon" is honest. |
| Emotional fit | 5 | The small, short page move and full-contrast text suit a tired reader. |
| Finish | 4 | The cramped answer card on desktop is the remaining visible flaw. |

## Calls (a)–(c)

- **(a) Agree.** Truthful product photos matter more than accent matching. Add the caption above.
- **(b) Agree.**
- **(c) Agree.** Fitting the whole question on the first screen matters more on phone. The entrance now gives the phone its book moment, but only once it is slowed down as described under First impression.

## Remaining, in priority order

1. Desktop answer card layout: stack the picks or set each column to at least 220px.
2. Slow the entrance to about 1.1s, with staggered headline lines and a later book drop.
3. Add the glow caption under the Portals row.

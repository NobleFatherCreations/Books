# Critique, round 3

Tests: Playwright at 1440x900 and 390x844. Frames captured at 0.2, 0.5, 0.9, 1.4 and 2.2 s, then an answer tapped and the Portals intro checked (`scratchpad/crit3/`). No page errors.

| Area | Score | Evidence |
|---|---|---|
| First impression | 5 | The entrance now reads as a real event (crit3/dent.jpg, ph.jpg). The headline lines unmask one after another and the book arrives out of darkness. By 1.4 s it settles with no jump. |
| Colour | 5 | The intro now says "Every photo shows the real glow: blue or green, depending on the pigment" (crit3/p-portal.png). So the blue reads as true, not off-brand. |
| Composition/rhythm | 4 | The stacked picks in qa/card.png are clean and easy to scan. **Still wrong:** after an answer on desktop, the hero grows. The book centres low (about y 400–870) and leaves the top-right quarter empty, while the picks fall below the fold (crit3/d-ans.png). Change: in the hero grid, set the book column to `align-self:start` with `position:sticky; top:96px`, so the book stays level with the headline. |
| Interaction & motion | 4 | The entrance timing is right, and changing the answer turns the book. **Still wrong:** the 100 px nudge on desktop shows only the card's heading line, and the first pick stays below the fold (crit3/d-ans.png). Change: scroll so the first pick row is fully in view, by targeting the first pick with `scroll-margin-bottom: 24px` rather than the card's top. Keep the move under 250 px, and keep it at 0 under reduced motion. |
| Finish | 5 | The card spacing, type and row highlight are polished (qa/card.png). The headline mask shows no artifacts after 0.9 s. |

## Remaining (both on desktop, after an answer)

1. Pin the book to the top of its column with sticky positioning, so it does not centre low in the grown hero.
2. Scroll the answer just far enough to show the first pick, not only the card heading.

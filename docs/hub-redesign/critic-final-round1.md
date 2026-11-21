# Independent critique: Noble Father homepage (final)

Tests: Playwright at 1440x900 and 390x844 (touch), and reduced motion. Screenshots in `scratchpad/crit/`. No page errors, no overflow, nothing stored in localStorage or cookies, and the only external requests were the Cloudflare beacon.

## Scores

| Area | Score | Evidence |
|---|---|---|
| First impression | 3 | fold-d1440: the Gloock headline is big and confident and the 3D book is good. But on load nothing moves except a slow idle sway of the book (entr.jpg, t3: the title strip does not move). This is not a bold moving opening. |
| Hierarchy | 4 | The order headline, then question, then chips, then answer reads correctly. On phone (p-ans) the answer card lands at the bottom of the screen, with the chips still taking most of it. |
| Typography | 4 | Gloock at display size is good lettering. Body text in #b3a68e is the most common colour (49 nodes) and reads dim at 14px on phone (phone-strips). |
| Colour | 4 | Brass on lamp-black is restrained. The crossing to strontium green works (desktop-strips col 3). But the charged pendant glows **blue** (d-gl300, p-gl300) while the brand green is #86ecd2, so the payoff colour contradicts the brand. |
| Composition/rhythm | 3 | Shelves repeat as identical left-label plus cover rows for 5 screens (desktop-strips col 1-2). The title strip under the nav is cut off at both edges and never moves (fold-d1440 "he Long After"), so it reads as a mistake. |
| Imagery | 4 | Real covers and real pendant photos. The NFC card's noir figure clashes in style (desktop-strips col 4). |
| Interaction & motion | 3 | The cover swings open well on desktop scroll (dhero.jpg). On phone the book is small and leaves the screen within about 150px, so the moment is lost (phone.jpg). Tapping an answer auto-scrolls 437–612px, a jump the owner dislikes. The charge then glow then fade over about 5s works and stops under reduced motion (pportal.jpg). |
| Phone ergonomics | 3 | Tap targets are 44px or more, except "Skip to the books" at 43px and the licence link at 17px. The translucent sticky header lets the headline show through behind the logo (hdr.png, phone.jpg col 3-5): a text collision. |
| Brand specificity | 4 | The press language, "Worn in the light", and the pendant charge belong to this brand. The music list shows "All 176 songs" while the songs are off, which overpromises. |
| Emotional fit | 4 | "Leave now" is always present, the copy is plain and nothing asks you to sign up. The auto-jump on answer and the dim body text work against a tired reader. |
| Finish | 3 | Headline bleed under the header, the clipped static strip, the blue glow, the 43px skip link. |

## To reach 5 everywhere (priority order)

1. **Header:** give the sticky header an opaque `--lamp-black` background, or fade the content under it, at every width. Nothing should show behind the logo.
2. **Answer tap:** remove the auto-scroll. Expand the answer card in place directly under the chips, or scroll smoothly only to the card's top with `scroll-margin-top` equal to the header height, and only under `prefers-reduced-motion: no-preference`.
3. **Opening motion:** stage a bold load entrance of about 1.2s, played once: headline lines rise and unmask one after another, then the book drops in and its cover cracks open about 15°. The scroll-linked opening then continues from there.
4. **Title strip:** either make it a real slow marquee (stopped under reduced motion) with masked faded edges, or delete it. A static clipped row is not acceptable.
5. **Phone book moment:** pin the hero book for about 60vh on phone (or make it larger, about 55vw), so the cover swing actually plays before it leaves the screen.
6. **Glow colour:** re-grade or tint the glow-state photos toward #86ecd2 strontium green (or use a green phosphor overlay), so the payoff matches "Alive in the dark."
7. **Body contrast:** raise #b3a68e to about #cdbea2 for body copy below 16px, and set phone body text to 16px.
8. **Shelf rhythm:** break the five identical shelf rows. Give one shelf a featured large cover, and vary the cover count and alignment.
9. **Music:** change "All 176 songs" to "176 songs, returning soon", or remove the link until playback is back.
10. **Small targets:** skip link to 44px or more. Pad the CC BY-NC-ND link to a 44px hit area.
11. **NFC card art:** replace the noir figure with a pendant or wax-seal photo in the Workshop's lighting.

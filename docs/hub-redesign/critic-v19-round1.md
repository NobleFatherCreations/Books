# Critic, v19 round 1 (independent, phone first)

Frames: `qa/v19/crit/` (phone-NN, rm-NN, desk-NN, phone-portal-*; contact sheets sheet-*.png). Only the Cloudflare beacon left the origin. No overflow, nothing stuck at opacity 0, no page errors.

## Scores (phone)
| Area | Score | Evidence |
|---|---|---|
| First impression | 3 | Confident serif, but the cover is a ~70px thumbnail (phone-00). Calm, not maximal. |
| Hierarchy | 3 | "Change answer" is set in display serif, louder than the result heading (phone-03). |
| Typography | 4 | Serif display plus grotesk body, good measure (phone-00, phone-15). |
| Colour | 4 | Warm library to teal night carries the concept (phone-14 to phone-15). Gold and teal accents are restrained. |
| Composition/rhythm | 2 | Dead voids: ~500px between The Root and The Listening Room (phone-12), and NFC phone icon floating off-centre in space (phone-18). |
| Imagery | 3 | Covers are strong. Pendant photos keep their grey cloth backdrop against the black night (phone-16). |
| Interaction & motion | 4 | Portal hold works: ring fills (phone-portal-1/2), green glow on release (phone-portal-3), fades back (phone-portal-4). The book swap on answer reads (phone-00 to phone-01). |
| Phone ergonomics | 3 | Leave now and Still always reachable (all frames). Brand link is 108x39, under 44px. |
| Brand specificity | 4 | "Worn in the light. Alive in the dark." with the charge mechanic is ownable (phone-15, portal frames). |
| Emotional fit | 4 | Plain lede, a gentle question, a Leave now button. |
| Finish | 2 | Overlaps and clipped titles (defects 1 and 2). Brown strip under the footer (phone-23). |
| Effect cohesion | 3 | Light/dark gives one story. Shelf-stack dimming and the drifting cover read as separate effects (phone-03, phone-07). |
| Performance feel | 3 | Instant scroll to 0 landed at y=66 (phone-02) but at 0 under reduced motion (rm-02): smoothing lag. Stacking leaves covers half-dark mid-scroll (phone-07). |

Reduced motion is designed: shelves lie flat with titles visible (rm-07). Desktop: a chapter page flips out of the cover (desk-03), but it has the same shelf overlap (desk-06) and the cursor ring sits over content (desk-15).

## Defects, most severe first
1. **Stacked shelves hide book titles** (phone-07, desk-06). The next sticky shelf covers "At Will / The Slow Take" labels while the covers are dimmed. "Playground Protectors" is a clipped third card at the right edge. Fix: give each shelf card enough bottom padding (or a sticky offset) that the next card stops below the title row. No dimming until a shelf is fully covered.
2. **Hero cover flies over the chips** (phone-03). It covers "My kids or my parents" and "At a festival", and it is cropped under the header in phone-02. Fix: hide or settle the flying cover once the chips enter the viewport, and give it a z-index below the header and the chips.
3. **"Change answer" over-scaled** (phone-03). Fix: make it a 16px underlined text button beside the heading, still 44px tall.
4. **Rhythm voids** (phone-12, phone-04, phone-18). Fix: cap phone section padding at about 96px. Centre and enlarge the NFC demo.
5. **Pendant photos have grey backgrounds** (phone-16, desk-12). Fix: cut the pendants out, or grade the backdrops to near black so the glow sits in the night.
6. **Footer ends on a brown band** (phone-23, desk-16). Fix: night-coloured html background under the footer.
7. **Footer is ~2.5 screens; brand link only 39px tall.** Fix: two-column footer, one "Back to the light", and min-height 44px on the brand link.
8. **Scroll smoothing on touch** (phone-02 versus rm-02). Fix: native scroll on touch; smoothing only on desktop.

## Five changes most likely to lift every phone score to 5
1. **Give the phone hero one real moment.** A full-width cover (60% of the viewport) that tilts with scroll and turns on answer.
2. **Rebuild the shelf stack for phones.** Each shelf is a full-screen card: title, a cover row that swipes sideways, and the next card arriving only after the labels clear.
3. **Tighten the vertical rhythm.** One phone spacing scale for section gaps, no gap over 1/3 screen, and a shorter footer.
4. **Unify the effect grammar around "charge and glow".** Use the Portal hold language (ring, glow, fade) for the door button, the chips and the NFC demo, and cut the effects that are neither (cover drift, shelf dimming).
5. **A finishing pass on the night half.** Black-graded pendant photos, a looping NFC tap demo, and no brown band.

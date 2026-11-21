# Critic round 2

| Criterion | R1 | R2 | Evidence |
|---|---|---|---|
| First impression | 4 | 4 | Larger headline and book carry the fold (desktop-strips.jpg col 1). |
| Hierarchy | 4 | 4 | After a tap, the answer panel is now in view on desktop (fix-states.jpg frame 4). |
| Typography | 4 | 4 | Phone pick text reads cleanly (fix-states.jpg frame 2). Song rows are legible (phone-strips.jpg col 4). |
| Colour | 4 | 4 | The brass-to-green threshold holds (desktop-strips.jpg col 3). |
| Composition/rhythm | 3 | 4 | The Listening Room two-column list and full-width Free tools fill the width (desktop-strips.jpg col 3). The desktop answer panel is still airy: three small covers in a wide band (fix-states.jpg frame 4). |
| Imagery | 4 | 4 | The NFC feature cover is strong (desktop-workshop.png). The door spines are tiny and dim at top-left, so they barely read (fix-states.jpg frame 3). |
| Phone ergonomics | 3 | 4 | The gutter is fixed (fix-states.jpg frame 2). The peeking next cover hints that shelves scroll (phone-strips.jpg col 2). |
| Brand specificity | 4 | 4 | The "In the making" line with its own icons is quiet and specific (desktop-workshop.png). |
| Emotional fit | 4 | 4 | Unchanged and right (phone-strips.jpg col 1). |
| Finish | 3 | 4 | Secondary actions are now serif text links ("See every Portal", "All 176 songs") (desktop-workshop.png, phone-strips.jpg col 4). I accept the hover explanation for the brass Close button. |

**Nothing is under 4.**

## The 3 fixes most likely to lift scores to 5

1. **Door art.** Scale the cover-cut spines to about 120px tall on phone and 160px on desktop. Raise their opacity to at least 0.85. Fan them so a sliver of each title shows (fix-states.jpg frame 3). The reveal should look like a payoff, not a smudge.
2. **Desktop answer panel.** Covers at 96px or more. Put the intro paragraph under the heading, not floated right (fix-states.jpg frame 4). Optionally run the three picks as a numbered 1-2-3 path with a thin brass rule between them.
3. **Phone shelves.** Add `scroll-padding-inline:16px`, matching padding on the track and scroll-snap. Add a small "1 / 4" count or a right-edge fade under each shelf heading (phone-strips.jpg cols 2-3). The peeking cover alone hints at scroll but does not count what is left.

A minor point: the NFC feature card has an unbalanced inner margin, with the cover inset about 90px and the text block floating mid-right. Tighten it to a 5/7 split with the text vertically centred (desktop-workshop.png).

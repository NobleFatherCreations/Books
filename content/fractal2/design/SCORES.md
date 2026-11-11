# SCORES: Fractal² intro (fixed rubric, threshold 4). Exit gate: node scripts/design-exit.mjs content/fractal2/design/SCORES.md design/fractal2/redesign/v6/template.html design/fractal2/redesign/v6/build.py design/fractal2/redesign/v6/index.html

```json
{
 "threshold": 4,
 "rounds": [
  {
   "round": 1,
   "date": "2026-11-11",
   "sha": "429aa5560687dfa01c5495ef3b0fe69d16ee79afa6e377a35c25b07167905298",
   "scores": {
    "hierarchy": 4,
    "type": 4,
    "space": 3,
    "craft": 3,
    "distinctiveness": 5,
    "feeling": 4,
    "phone": 3,
    "legibility": 2,
    "continuity": 3
   },
   "weaknesses": [
    {
     "id": "W1",
     "text": "Body text over bright busy art; safety paragraph for the in-danger reader sits on the art",
     "status": "open"
    },
    {
     "id": "W2",
     "text": "30-column dot field and plunge not seen by the critic (checking: beat-0 is the dot field; capture set must label beats by name)",
     "status": "open"
    },
    {
     "id": "W3",
     "text": "Atlas grid cropped at the right edge on phone and desktop; labels inconsistent; live sector overlaps neighbour labels",
     "status": "open"
    },
    {
     "id": "W4",
     "text": "Atlas ending weak: identical glyphs, ghost grid behind the list, door panel box",
     "status": "open"
    },
    {
     "id": "W5",
     "text": "Letterbox bars uneven (phone shows bottom only), soft, text cut by bar edge",
     "status": "open"
    },
    {
     "id": "W6",
     "text": "Phone header heavy: Leave dominates, caption wraps and shifts",
     "status": "open"
    },
    {
     "id": "W7",
     "text": "Phone title screen cramped and murky; byline over a ring label",
     "status": "open"
    },
    {
     "id": "W8",
     "text": "Tactic words unreadable at phone size (texture, not information)",
     "status": "open"
    }
   ]
  },
  {
   "round": 2,
   "date": "2026-11-11",
   "sha": "unrecorded (scored before the per-round hash habit; superseded by round 3)",
   "scores": {
    "hierarchy": 4,
    "type": 4,
    "space": 3,
    "craft": 3,
    "distinctiveness": 4,
    "feeling": 4,
    "phone": 3,
    "legibility": 2,
    "continuity": 3
   },
   "weaknesses": [
    {
     "id": "W1",
     "text": "Body text over bright word-ring art; text struck by ring labels (Down through list, safety paragraph)",
     "status": "open"
    },
    {
     "id": "W2",
     "text": "Count beat: faint dots, dead left half",
     "status": "open"
    },
    {
     "id": "W3",
     "text": "Atlas transition untidy: orphan ring, enlarged glyph over neighbours, vignette dims left column",
     "status": "open"
    },
    {
     "id": "W4",
     "text": "Atlas labels ambiguous and tiny",
     "status": "open"
    },
    {
     "id": "W5",
     "text": "Letterbox too heavy; ring words sliced",
     "status": "open"
    },
    {
     "id": "W6",
     "text": "Phone hero dim; header crowded",
     "status": "open"
    },
    {
     "id": "W7",
     "text": "Caption not tied to visible state; art at middle brightness behind text",
     "status": "open"
    },
    {
     "id": "W8",
     "text": "Phone atlas payoff missing in sampled frames (critic had no phone beat frames)",
     "status": "open"
    }
   ]
  }
 ]
}
```

## Low-score protocol, round 1 (three candidates each, from different sources)
**Legibility 2 (W1, W7):** A) a solid 90% navy panel behind every text block that overlaps art (benchmark: NASA Eyes, The Pudding keep text on flat ground); B) dim the art to under 30% whenever any copy is on screen, bright only in text-free beats (catalogue 36 cinematic: beats; Apple "dim to focus"); C) subtitle-style fixed caption card in the lower third on phone (direction B comp). CHOICE: B for all body text, plus A for the safety notes (they must never sit on art), plus a local radial scrim behind the phone title. C rejected: too big a change to reading flow for 1,400 words.
**Space 3 / phone 3 (W3, W4, W7):** A) 5-column atlas that fits the width, with the camera landing on the live slot (catalogue 25 maps, 36 match cut); B) horizontal snap-scroll atlas; C) show only the mapped glyph lit, others as dots. CHOICE: A (whole map visible, live sector in its true slot, no crop); B rejected (hidden content), C rejected (the 30 glyphs are the point). Remove the ghost grid behind the phone door list.
**Craft 3 (W5, W6):** A) symmetric crisp bars starting below the header; B) drop bars on phone; C) replace bars with edge vignettes. CHOICE: A with 12px soft edge. Header: left-aligned single-line caption on phone, smaller Leave (still 44 px target).
**Continuity 3 (W2):** check the capture set before changing the page: name beats (count, pull-back, words, plunge, final) so the critic can see them.
**W8 (words unreadable on phone):** A) hero callouts with leader lines naming 5 real tactics at readable size; B) a slow close-up pass; C) accept as texture and say so in the caption. CHOICE deferred to round 2 evidence (A is the strongest; costs new layout).

## Round 2 diagnosis (what the critic and my own reading agreed on)
Scores did not move after round 1's fixes (legibility still 2). Root cause found by looking at frames: the art brightened from the reading line, while text was still on screen above that line, so lists scrolled across fully bright rings. Contrast gates cannot see this (busy texture, not a ratio). Fix chosen: art stays dim whenever ANY text block is within 0.3 viewport of the screen (`tv`), bright only in text-free beats. Also: dots centred and brighter, atlas drawn only when the camera has arrived, label size up, scrim narrowed, bars 8svh, hero boost, caption threshold, capture set now names beats and captures phone beats.

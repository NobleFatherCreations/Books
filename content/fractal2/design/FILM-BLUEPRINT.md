# Fractal² intro film: redesign blueprint (2026-11-15). Blueprint only; nothing built.

Track: Rescue/rebuild under design protocol v3. Script: `content/fractal2/intro-v15-draft.md` (draft 2, awaiting final approval).
Self-audit question asked at every choice: can this be more advanced, look better, run smoother, or add something that raises the final product?

## Concept (one sentence)
One light, and everything that was built on top of it; the film pulls back to show the size of what covers it, then goes down through it and uncovers the light.

## Budget
- Lead style: dark, astronomical, engraved. The map is the only picture.
- Signature move: one unbroken camera through scales. Out (the map grows), then down (the fall), then the light opens.
- Type: Instrument Serif for his voice; one small-caps sans for labels and table headings. Nothing else.
- Colour grammar, used in every table: gold = the original, cool grey = the counterfeit. One accent.
- At most three effects on screen at once.

## 1. The engine: a clock, not a scroll bar
| Choice | Why it is the better option |
|---|---|
| The film is driven by one master clock. Every picture and word is a pure function of time `t`. The page does not scroll at all. | Scroll-driving caused most of the v10-v14 faults (toolbar resize, damped camera replaying, caption speed). A clock removes that whole class. It also makes every frame reproducible, so a machine can check any moment exactly. |
| Timeline written as shots: start, length, camera from/to, easing curve, caption cues, table cue. | Speed changes become deliberate: slow holds, hard accelerations, a full stop. This is what the owner asked for ("speeding up and slowing down for dramatic zoom and word effects"). |
| The clock can follow an audio file later. | Narration or music can be added without rebuilding. |
| Fixed stage of `100lvh`, canvases sized in pixels once. | Carries forward the "ovals" and "toolbar jump" fixes. |
| Considered and rejected for release one: WebGL shaders. | They would add bloom and depth blur, but they are the most likely cause of a crash on an iPhone, and the owner has already lost rounds to crashes. The same richness comes from camera easing, layered parallax and pre-drawn glow. Can be added later on desktop only. |

## 2. Camera and pace
- Every move eases in and out; nothing starts or stops at full speed. Holds are never frozen: a slow drift and a breathing light keep the frame alive.
- Three speed peaks, each tied to a line: the pull-back at "It was never only people" (largest move, one full rotation, upright at the end); the fall at "I went down" (fastest, slowing line by line to black); the window at "let it through" (the light opens to fill the screen).
- One full stop: "Then the map turned and looked at me." Everything halts for one second. Stillness is the effect.
- Depth: three star layers move at different rates so the zoom reads as travel, not as a picture being scaled.
- Length about 10.5 minutes at 1,130 words. A thin progress line with eleven chapter ticks shows where you are.

## 3. Words
- One caption at a time, large, in the lower third on phones and centred or beside the map on desktop.
- Words arrive in phrase groups, rising a short distance and settling; they leave by drifting toward the map and thinning out. Nothing appears or disappears in place (owner taste).
- Time on screen is set by a rule a machine checks: at least 0.35 seconds per word plus 1.2 seconds.
- A soft dark band travels with every caption so text is readable over bright art. This closes the open "two captions over bright art" fault, and a new contrast check samples real pixels behind every caption and every canvas label.
- Emphasis lines (the question, "I went down", "My original frequency") get the full screen and a longer hold.
- No per-word layers or filters (banned mechanics).

## 4. The table moments (all tables are in; each appears and leaves as one choreographed move)
Shared grammar: items arrive one at a time on curved paths around the rings, never as a list scrolling up and never as a grid of identical boxes. The first few are slow enough to read; then the pace quickens so the viewer feels the count; then the whole set holds as a complete figure for two seconds before it dissolves. Every table is also in the plain transcript and on the hub, in full.

| # | Table | Where | How it appears and leaves |
|---|---|---|---|
| A | Eight stages | 2. One map | Rings light one by one, name set on the ring. |
| B | Thirty techniques | 2. One map | Names write themselves into the rings until the first Fractal is whole. |
| 1 | Thirty sectors + "your relationship with..." | 3. Thirty | Sector name flies in from depth; its relationship line resolves under it; both fall into the ring. A count runs 1 to 30. Ends as thirty points around the map. |
| 2 | Three nested levels | 5. Architecture | Three rings draw outward: a face, a logo, the sky. Then the outer ring folds back into the centre on "the pattern is inside the person". |
| 3 | Eight divine principles and their inversions | 6. Inversion | Each ring shows the gold original, then turns over to the grey stage. |
| 4 | Thirty faculties and their inversions | 6. Inversion | A vertical mirror line. The gold word crosses it and comes out grey, reversed in meaning. Three slow, then a stream, then all thirty pairs held as two columns (stacked on phones). |
| 5 | "It says... and then it..." | 6. Inversion | Gold sentence writes on; the grey ending cuts across it. |
| N | The names (false god, devil, adversary, matrix, machine, system) | 6. Inversion | Same spot, same size, each dissolving into the next: one thing, many words. |
| 6 | Thirty original impulses | 6. Inversion | Each sector label lifts and the impulse beneath it glows gold, like lights under water. |
| T | The traditions | 8 | Tradition name in small caps, its line under it, both drift into the light. |
| W | The window | 10 | The thirty inversions sit over the light as dark blocks and lift away one by one; the light widens to fill the screen. |

## 5. "Begin here" entry screen and launch
- Full-screen living emblem: eight rings turning slowly in alternate directions, one light travelling the gold ring, the 335 tactic words drifting faintly in the dark behind, a slow breath in the glow.
- Lettering: "Fractal²" large in the serif; "Begin here" under it; one round Play control whose ring draws itself as the art finishes loading (the film cannot start half-loaded).
- Launch (about 2.5 seconds): the Play ring expands and becomes the first ring of the map; the title letters drift apart into stars; the camera falls into the black centre; one light remains. The film starts on that light.
- Ambient motion is calmed under Reduce Motion. Pressing Play is the viewer's own choice to watch a film, so the film itself plays in full. A "Read it instead" link gives the whole script and all tables as plain text.

## 6. Controls and comfort
Tap or Space pauses. Progress line with chapter ticks. Skip to the map. Replay. Controls fade after 2.5 seconds. The screen is kept awake during play. The film pauses when the tab is hidden. Desktop: arrow keys jump chapters.

## 7. Phone and desktop
- Phone portrait: map in the upper two thirds, caption below; pairs stack gold over grey. Images at 2048 px, canvas pixel ratio capped at 2.
- Desktop and landscape: map centred, captions centred large or beside it from the big map onward; pairs sit left and right of the mirror line.
- A frame-time governor lowers star count before it lets the frame rate drop.

## 8. The hub
The map is the menu: thirty sectors placed around the ring in life order (birth to death), each with its "relationship" line and original impulse. Entertainment is lit and open; Corporate is marked next; the rest are dim and labelled "in production". A plain list sits below for keyboards and screen readers. Designed in detail after the film passes its gate.

## 9. Machine checks before the owner sees anything
`film-check` is rebuilt for a clock: same frame at the same time on every run; caption time-on-screen; contrast behind every caption and label (new); round picture; nothing plays twice; no brightness pumping; layer and canvas budget; pause, resume, hidden tab; end button works; each of the six tables fully shown and fully cleared. Every row in `REGRESSIONS.md` gets its time-based equivalent. Runs on phone, phone with Reduce Motion, and desktop. Then contact sheets are read, then one critic round, no score under 4.

## 10. Build order
1. Engine and clock with the existing art; check harness first.
2. Entry screen and launch.
3. Sections 1-5 (the question to the architecture).
4. Sections 6-10 (tables, descent, traditions, window).
5. Section 11 and the hub.
6. Gate, critic, phone card. Nothing is deployed without the owner's word.

## Known limits (stated up front)
- Thirty pairs cannot all be read at film pace. The design lets the first few be read and the rest be felt, and holds the full table for two seconds.
- Frame rate and memory on a real iPhone can only be confirmed on the owner's phone.
- Silent until the owner decides on narration or music.

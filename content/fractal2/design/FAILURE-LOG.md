# FAILURE LOG: every time the work missed what the owner asked for

Written 2026-11-13 from the full session. Companion to `REGRESSIONS.md` (the per-fault automated guards). This file covers the failures that a check cannot catch: not reading what was sent, answering a different question, and shipping before checking against the brief. Read it before starting any Fractal work.

Owner's standing complaint, in their words: "I'm really annoyed that I report issues and new ones pop up every time." And: "I asked you to read the fractal for context... you instead built the fractal." And: "You didn't even lead in to the fractal2 expansion in the document I asked for."

---

## Part 1. The intro website (Fractal² intro, v1 to v14)

### 1.1 What was asked
Take the original Fable-designed intro (v1) and the v8 fractal-camera build, make a cinematic, award-worthy scroll intro, push it live, and run the design system start to finish so its gaps could be found. Later: make it world-class, easy to navigate, animated, and distinctive top to bottom.

### 1.2 Faults the owner reported on their iPhone, in order (each one cost a round)

| Round | What the owner saw | What actually went wrong | Status |
|---|---|---|---|
| Earlier | Deployed v5 "worse than the old intro": blurry zoom, hard mask edge, instant small-to-big jump, no designs behind the words | Shipped without comparing to the previous version | Rebuilt as v6 |
| 1 | Words don't move up as you scroll; they just appear and disappear | Captions were positioned by script inside a pinned box | Captions now ordinary page flow at scroll speed |
| 1 | After the map expanded fully it "kicked me back to the beginning," then crashed on scroll | DOM images at 320% under a will-change parent: ~4,000 px layers on a 3x phone | One screen-sized canvas |
| 1 | Wanted sector names to pass one by one; wanted the "in myself, my body, my genetics, my ancestry, my generational chains" list | Not built in first pass | Built |
| 2 | "It still crashes before the end" | 1,000+ word spans each with will-change | Removed |
| 2 | Words should start at the very bottom and exit at the very top; sentences more spaced; sector names floating transparent, from different angles, slower | Words appeared ~40% above the bottom, so there was no motion | Script spacing rebuilt; `pace` check |
| 3 | "Words too dim in the fly-bys, almost impossible to see" | Alpha 0.4-0.7 on small type | Fixed by hand; **no automated contrast check for canvas text yet** |
| 3 | Fly-bys should zoom close, flying toward the fractal; rotation of 20 degrees was awkward, wanted one full circle back | Design not done as described | Rebuilt |
| 3 | List of inversions and originals at the zoom-in | Not present | Added |
| 3 | Got stuck at the end, couldn't scroll back up; wanted one button to a hub | Old circle-list ending | Replaced by one button ("Enter the map") |
| 3 | Words bigger, take more of the screen; no dim-to-black then bright-yellow flicker | Per-caption dimming | `flicker` check |
| 3 | Ambient, living, pulsing opening screen with beautiful lettering | Static first impression | Built |
| 4 | Words too fast, flying from the bottom and gone | Caption travel was 1.6x its scroll window | `pace` |
| 4 | "Words appear twice" (generations, myself and my body) | A sequence value snapped to 0 and the damped camera replayed it backward | Sticky keys, `once` check |
| 4 | Zoom in and out "jumps and isn't smooth" | Re-layout every time the browser toolbar moved | `toolbar`, `smooth`, `settle` checks |
| 4 | Circles drawn as ovals (owner's screenshots) | Canvas sized by CSS percent, buffer by innerHeight | Explicit pixel sizes, `round` check |
| 4 | "The button worked at the end" | (Confirmed fine.) | OK |

### 1.3 Failures of process on the intro (mine, not the owner's)

1. **Gates passed on a design the owner hated.** The automated gates never pressed Begin, so they checked 2 of 66 screens. Fix: `--click` on the gates; `film-check` fails if `window.__film()` is missing.
2. **Fix one thing, break another, repeatedly.** The owner had to be the tester. This led to design protocol v3 (`.claude/skills/design-director/SKILL.md`): machine rejects first; every reported fault becomes a failing check; ask the owner only what only they can answer.
3. **End markers were one screen late** because the camera target jumps. Fixed with scripted camera per screen of scroll.
4. **`film-check` was flaky**: smoothness was not deterministic, name clash (`rest` vs `atRest`), slide limit not normalized. Rebuilt deterministic.
5. **Entertainment sector site v3**: compass links failed axe target-size; reveal hid content at opacity 0; display h1 wrapped mid-word at 1440; nav-check read SVG hrefs as `[object Object]`. All fixed, but only after being caught late.
6. **Never done:**
   - v14 is not critic-scored (`design-exit.mjs` fails).
   - Real-iPhone confirmation that the crash is gone (needs the owner's four-question phone card).
   - The owner's own sentences for the "author's lens" captions.
   - A sound decision.
   - The hub page the final button should lead to (it currently goes to `/fractal2/entertainment`).
   - Entertainment v3 is built and verified but **not deployed**; the live sector site is still v2.
   - `sites.json` `fractal2-ent` and stale `fractal-ent` entries not updated.
7. **A permission-classifier block** stopped one deploy step; it needed the owner's explicit go-ahead.
8. **Tool trouble:** the Netlify and ElevenLabs MCP servers disconnected mid-session (schemas had to be reloaded with ToolSearch); the shallow clone gave a false "unrelated histories" until unshallowed to 739 commits; a background `git clone` looked dead but was running.
9. **Delivery faults:** the owner could not find files in the first zip ("I can't seem to find any of the files in order"); the owner had to ask "how close are we to done and having a live version to look at."

### 1.4 What now guards the intro
`scripts/film-check.mjs`, `film-gate.sh`, `nav-check.mjs`, `frame-walk.mjs`, `design-gates.mjs --click`; per-fault rows in `REGRESSIONS.md`; deploy only through `scripts/film-gate.sh`. Live: v14 (deploy `6af58fe7d43ad699fbcbf1c9`).

---

## Part 2. The Fractal PDFs ("Why I Wrote This") and the Book 1 audit

### 2.1 What was asked
A PDF explaining the whole Fractal body of work to a friend (Von "Foil" Saunders, a school psychologist): what the three works are, how they fit together, how they help people in any sector of life; written in the owner's first person; leading into Fractal² (300+ tactics and 150+ combinations per sector); with a separate letter and asks for Foil; ending in the best-case world. Then: an independent audit of Book 1, then a steelman.

### 2.2 Every time I failed to read or produce what was sent

| # | What the owner sent or asked | What I did instead | Where it showed |
|---|---|---|---|
| 1 | Pasted notes (YouTube, outreach, spiritual lens, War Map, combos) and asked for a PDF organizing the ideas for a psychologist | Built a 21-page summary that explained the framework tables and barely mentioned the three works | Owner: "you didn't expand anything" |
| 2 | "Read all of the fractal... especially `/frequency`"; "use your expanded knowledge" | Built the Fractal's tables into the PDF instead of explaining the work | Owner: "you instead built the fractal and didn't mention it at all" |
| 3 | Thirty full original-impulse definitions, each with a practice | Shrank each to one line, then left † marks | Owner: "You didn't give definitions of the original impulses" |
| 4 | "Lead in to the Fractal² expansion" | Mentioned Fractal² as one table row | Owner: "You didn't even lead in" |
| 5 | The Value-and-Impact PDF, attached twice, "the visual attachment" | Never opened it, either time; asked whether it was an image | The report is the owner's "most wanted" material |
| 6 | "List all MCPs and skills you will use and how you'll lower token usage" | Loaded two skills silently, listed nothing, asked no questions | Owner called it out |
| 7 | An artifact link of combo and tactic files ("only look at what you absolutely need") | Read the tool's summary only; relied on it for the 138 Corporate count | Never opened real files |
| 8 | Owner's origin account (`intro-final.md` Part VI, test-locked) | Never opened it; invented a "stake" paragraph in the owner's voice | Steelman, miss #1 |
| 9 | The War Map, pasted twice | Condensed to a sentence; left out the laws twice by my own choice | Steelman |
| 10 | Pasted three combos and asked for a fourth for the psychologist, then asked for another on a different lens | Wrote both (Paper Child, Calling Trap) without having been told Foil's region, ages or main complaint; marked as assumptions, but the facts in them (staffing ratio, referral disparity) are unverified | Open |
| 11 | "Steelman your output against everything I provided" | Not done before delivering; the owner had to request it | |

### 2.3 Specific content failures
- **No steelman before delivery.** The audit found: no sector-by-sector, level-by-level account of the good it does; the playbook (Pattern Decoder) got one sentence; Value-and-Impact not woven in; psychological levers absent across ~25 middle pages; `no-ai-slop` promised but never run; `design-director` never run.
- **Facts stated before verification:** "52 pages" with swapped definitions (it is 26, checked later); the school-psychologist ratio and the referral disparity are still unverified.
- **Wrong labels and references:** machine map said "Sections 5, 8" for the frequency (should be 4, 8); Foil's letter pointed to the wrong sections until a rebuild.
- **Count mismatch between PDFs:** the master says 2,700 examples (the owner's choice); the audit says 2,340 published.
- **Assumed answers where the owner was silent:** the prayer (left out), the owner's story paragraph (invented), both composites in the public edition.
- **The blueprint itself:** did not open the Value-and-Impact PDF until the owner asked a second time; left The Largest Body and The Origin history unplaced; `design-director` missing from the execution prompt; the data checks (combos per family, turning-point test) written but never run.

### 2.4 Defects found in the published Fractal (not fixed)
Spiritual Bypassing and Financial Control definitions swapped on all 26 sector pages; counts say 30 and 2,700 but 26 and 2,340 are published; zero outside sources; "This is by design" x8 contradicts The Origin; The Mirror numbers techniques differently; two chapter orders.

---

## Part 3. Root causes (the same five, every time)

1. **I answered an easier question than the one asked.** (Built the framework instead of explaining the works.)
2. **I treated attachments as already known.** (Value-and-Impact, intro Part VI, the artifact.)
3. **I reused instead of reading.** (Shortened or reshaped earlier output rather than going back to the source.)
4. **I shipped before checking against the brief.** (No steelman, no brief-to-output table.)
5. **I asked, then assumed.** (Questions posed, silence treated as permission.)

## Part 4. Pre-flight checklist (do this before writing or building anything)

1. Restate the ask in two lines. Name every file the owner referenced and say whether you have opened each. Open the ones you haven't.
2. List the skills and MCP servers you will use and the token plan. Then use them.
3. For writing: use the owner's wording where it exists. Search the repo for it before drafting. Never invent a quote, a statistic, a tactic, or an owner story.
4. For any build the owner will look at: make a brief-to-output table (each thing asked, where it is in the output) before delivering. Anything missing is "not done," not hidden.
5. Steelman your own output. Report what was and wasn't done, and why.
6. For visual work: a reported fault becomes a failing check first. Run the gates, then look at real screenshots, not only the gate output.
7. Never deploy without the owner's go-ahead. Never push to another branch.
8. Where the owner has not answered a question, state your default and proceed, but flag it in the first line of the delivery.
9. Verify counts and cross-references against the files before stating them.
10. Put architecture and mapping on the strongest model and execution on cheaper ones; do not spawn agents unless asked.

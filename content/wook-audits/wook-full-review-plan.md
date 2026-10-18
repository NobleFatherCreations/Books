# Wook in Sheep's Clothing — Full Review Plan

**Written 2026-09-14.** The brief: every section of every chapter reviewed
for proofreading, continuity, and writing enhancement within the book's own
tone, slang and information. Nothing deploys between now and the end of that
work; one final version ships when all of it is done.

This document is the map and the contract. `wook-full-review-ledger.md` is
the running state. Read both before starting any pass.

---

## 0. Where things stand, verified not assumed

Live as of today is **v9**, byte-identical to `library/wook/index.html`,
confirmed by fetching the live page and comparing bytes.

The thing worth knowing before anything else: **before today's deploy, live
was v7.** Versions 8 and 9 were committed, versioned in `sites.json`, and
given on-page patch notes, and none of it was on the internet. `sites.json`
is the ledger of what was *built*, not of what is *live*. Every future round
verifies the live bytes, not the ledger.

**How this site deploys.** Not from git. The Netlify MCP connector issues a
one-shot proxy command, run from `library/wook/`, which uploads the
directory and builds it in Netlify's system:

```
npx -y @netlify/mcp@latest --site-id <siteId> --proxy-path "<token>"
```

The payload is 157 MB because `audio/` and `video/` ride along. A deploy
takes a few minutes. Afterwards, verify: live bytes equal repo bytes, the
proxied `noblefathercreations.com/wook` path still resolves, and the audio
and video still return 206 on a range request.

---

## 1. The inventory — what "everything" actually is

### Scale

| | Words |
|---|---|
| Whole book | 263,844 |
| Front matter | 5,172 |
| The 26 chapters | 246,376 |
| Back matter and appendices | 11,770 |
| Median chapter | 9,873 |
| Longest / shortest chapter | 12,888 / 5,204 |

### The repeating chapter machine

Every chapter is built from the same parts. Reviewing a chapter means
reviewing each of these *against its own job*, not against one house style.

| Component | Count | What review means for it |
|---|---|---|
| THE DROP (cold open) | 26 | Scene integrity, POV vernacular, does it resolve |
| THE SOUNDBOARD QUOTE | 26 | Voice, and the résumé line where the comedy lives |
| THE REAL F*CKING SETLIST | 26 | Does the list match the Tracks that follow |
| Tracks | 139 | The play named and dissected; one idea per Track |
| THE BEHAVIOR | 139 | Observable, concrete, not restating THE READ |
| THE READ | 140 | One per Track — and ch10 has six for five Tracks |
| VIBE CHECK | 139 | Body-level tell, not argument |
| MIRROR SET | 139 | The play turned on the reader |
| REFRACTIONS | 139 | The play in a different register |
| RUNS IN EVERY DIRECTION | 139 | Three named people minimum, one universality line max |
| SOBER TUESDAY | 139 | Default-world translation; cap the office at one in three |
| Counter-drops | ~170 | Executable, named, correctly chapter-tagged |
| POCKET SCRIPTS | 24 | Memorizable sentence; missing in ch25 and ch26 |
| Pocket Script chips | 169 | Under about 18 words or it is reference material |
| FIELD SPECIMEN | 26 | Fragments plus kicker; the book's sharpest comic device |
| THE TAPERS' SECTION | 25 | Cited thinkers, real claims; missing in ch25 |
| THE TEST | 6 | Only six chapters have one — decide whether that is right |
| Tales From … The Save | 26 | Somebody gets out; pairs with that chapter's DROP |
| THE FANNY PACK | 26 | Reference card |
| THE SOUNDCHECK | 26 | Chapter close |
| THE SUNRISE SET | 26 | The sermon beat |
| THE KANDI TRADE | 26 | The vow |
| Bridge | 25 | Must tease chapter N+1 |
| Poster (part, title, keys, meta) | 26 | Metadata must match the chapter's real contents |

### The non-chapter material

- Front matter: the disclosure, the map, THE LINEUP and THE SOUND tutorials,
  the dedication, the content disclosure, A NOTE ON METHODOLOGY.
- A NOTE ON SAFETY, and INTERMISSION — BEFORE THE ENCORE.
- Standalone sections split out in v7: the Capacity Spectrum, the Bystander
  Interruption Kit, the Morning-After Reckoning, the Author's Wook Confession.
- All 26 appendices, A through Z, including the Glossary and the Master
  Track Index.
- The colophon, the Patch Notes section, the Real Ones section and its
  soundtrack, the THE HOUSE nav drawer and the Setlist drawer.

### The non-prose assets

Twelve MP3s, one MP4, every inline SVG including the 19 field-tag icons
added in v8, and the whole nav and anchor system.

---

## 2. The three lenses

**Proofreading** is the surface: typography, quotation marks, apostrophes,
glyphs, doubled words, spacing, markup that stopped matching its siblings.
Mostly mechanizable. `scripts/wook-proofread.py` already covers eight
classes of it and currently reports zero.

**Continuity** is the claims: chapter counts, cross-references, rosters,
enumerated lists, poster metadata, who appears where. Also mostly
mechanizable. `scripts/wook-continuity-check.py` covers eight classes and
currently reports zero errors.

**Enhancement** is the only one that cannot be mechanized, and it is the
bulk of the work: does this Track earn its length, is this SOBER TUESDAY
the fourth office joke in a row, is this slang still current, does this
RUNS card name people or recite a disclaimer, is the information correct
and current, does the argument escalate across the chapter. This requires
reading every word.

The rule that governs all three: **a checker finds the class, a person
finds the instance.** Every round so far has proved the same thing — reading
finds real defects, and then a checker written from what reading found
discovers more of the same family hiding in sections nobody opened.

---

## 3. What has already been reviewed, and how deeply

| Material | Last real pass | Depth | What remains |
|---|---|---|---|
| Cold opens | v4 | Deep read, all 26 | Re-read in chapter context |
| Bridges | v5 | Mechanical + read | Spot-check only |
| Recurring cast, cross-refs | v6 | Mechanical | Covered by checker |
| RUNS cards, ch9–24 | v7 | Rewritten to rule | ch1–8 never re-read |
| Field Specimens | v7, art v8 | Written to format | Read for slang currency |
| SOBER TUESDAY | v7 | One card rotated in 14 chapters | ~40 cards still office-bound |
| Appendices A–Z | v8 | Chapter tags verified | Prose never read |
| Colophon | v8 | Rewritten | Done |
| Whole book, surface | v9 | Mechanical, 8 checks | Clean |
| **Tracks, READ, BEHAVIOR, VIBE, MIRROR, REFRACTIONS** | **never** | **none** | **all of it** |
| **Counter-drops, Fanny Pack, Soundcheck, Sunrise Set, Kandi Trade** | **never** | **none** | **all of it** |
| **Front matter and standalone sections** | **never** | **none** | **all of it** |

That bottom block is roughly 70 percent of the book's words and has never
had a line-level read.

---

## 4. The pass plan — thirteen passes

### Stage A — mechanical sweeps, book-wide (3 passes)

**A1 — Proofreader extension.** Add the rules the current eight do not
cover: number and time formats, dash and ellipsis style, component-label
capitalisation, heading hierarchy, duplicate section titles, chip length by
section type. Fix what it finds.

**A2 — Continuity extension.** Add: Track numbering versus the Setlist that
promises them, one READ and one BEHAVIOR per Track, appendix-to-chapter
round trips, counter-drop name uniqueness, agreement between any two lists
claiming the same content. This is the check that would have caught ch10's
sixth READ and Appendix Q's missing item.

**A3 — Vernacular and slang currency sweep.** Build the per-POV word banks
the tone audit sketched, measure which chapters share one vocabulary, and
flag slang that has dated. Produces a word bank the chapter passes then use,
rather than each pass inventing its own.

### Stage B — chapter deep reads (7 passes)

Grouped by movement so each pass has one argument to hold in mind. Every
section of every chapter in the group, in reading order, all three lenses at
once.

| Pass | Chapters | Movement |
|---|---|---|
| B1 | 1–5 | Set One — Know the Pattern |
| B2 | 6–9 | Set Two — Read the Room |
| B3 | 10–13 | Set Two |
| B4 | 14–17 | Set Two |
| B5 | 18–20 | Set Two |
| B6 | 21–23 | Encore — Protect the Magic |
| B7 | 24–26 | Encore |

Roughly 35,000 to 50,000 words per pass. Each produces: applied fixes, a
list of enhancements made, and a queue of anything that is an authorial
call rather than a correction.

### Stage C — everything that is not a chapter (1 pass)

Front matter, the safety and methodology notes, the intermission, the four
standalone v7 sections, all 26 appendices read as prose rather than
checked as tags, the glossary, the colophon, the Real Ones section.

### Stage D — book-wide coherence, then ship (2 passes)

**D1 — Cross-chapter.** Recurring cast consistency across 26 chapters,
callback integrity, redundancy between chapters that cover adjacent ground,
the escalation of the argument from chapter 1 to 26, and the standing
contradiction between chapter 23's and chapter 25's lists of the sixteen
moves.

**D2 — Ship.** Re-run both checkers, regenerate the cold-open reel document,
full visual verification at both widths against a baseline, update
`sites.json`, `MEMORY.md`, `BOOKS.md` and the on-page patch notes, deploy,
then verify live bytes and the proxied path.

**Thirteen passes.** A and C could each be split if a pass runs long; the
chapter groups should not be merged.

---

## 5. How each pass runs

1. Run both checkers first. A pass never starts on a red book.
2. Read every section in scope, in reading order, top to bottom.
3. Apply corrections directly. Apply enhancements that are clearly within
   the book's established voice and rules.
4. Anything that changes what the book *argues*, or that picks between two
   defensible authorial choices, goes in the author-decision queue. It does
   not get guessed at.
5. Re-run both checkers, plus a targeted browser check if markup changed.
6. Update the ledger. Commit. **Do not deploy.**
7. Where a defect turns out to be a class rather than an instance, write the
   check for it and add it to the proofreader or the continuity checker
   before moving on.

---

## 6. The ledger

`content/wook-audits/wook-full-review-ledger.md` carries one row per pass and
per chapter, its status, the date, and a pointer to the commit. It exists
because this work spans sessions and a fresh session has no memory of
anything outside the repo. A pass is not finished until its ledger row says
so.

---

## 7. Seed list — already found, not yet addressed

Carried into the passes above so nothing gets rediscovered from scratch.

- **ch10 has six THE READ blocks for five Tracks.** Structural. Pass A2/B3.
- **ch25 and ch26 have no POCKET SCRIPTS; ch25 has no TAPERS' SECTION.**
  Decide whether that is deliberate given those chapters' different shape.
  Pass B6/B7.
- **THE TEST appears in six chapters only.** Pattern or accident. Pass A2.
- **Chapter 23 and chapter 25 both list "the sixteen moves"**, in different
  orders with different item names. Appendix Q follows chapter 23. Pass D1,
  and it is an authorial call.
- **About 40 SOBER TUESDAY cards are still office-bound** after v7's partial
  rotation. Passes B1–B7.
- **RUNS cards in chapters 1–8** were never re-read against the three-named-
  people rule. Pass B1, B2.
- **Every page in this repo loads Cloudflare Web Analytics from a CDN** —
  438 files. A real external request on books whose architecture forbids
  one. Needs a decision, not a unilateral deletion.
- **`BOOKS.md`'s wook entry is stale**, still describing a file discrepancy
  as blocking design work. Pass D2.
- **`[address]` in ch14** reads like an unfilled placeholder but is the
  book's own bracketed fill-in device, used 50+ times. Left as is,
  allowlisted with a reason. Revisit in B4 if it still reads wrong in context.

---

## 8. What could go wrong

- **A scripted content pass introduces a typographic regression.** It has
  happened twice: v7 and v8 wrote 190 straight apostrophes into a curly
  manuscript and nobody proofreads generated text. Any pass that writes
  content by script ends with the proofreader, every time.
- **A fix keyed on a string instead of a structure misses a section.** v7's
  chip reclass matched "SAFETY APPENDIX" and never saw the one block called
  "RESOURCES APPENDIX". Match on structure where structure exists.
- **The ledger drifts from reality.** Same failure mode as `sites.json`
  saying v8 while v7 was live. Verify, do not trust.
- **Enhancement turns into homogenisation.** Several of this book's
  components make deliberate anti-pattern choices. Read the component's own
  job before applying a rule to it.

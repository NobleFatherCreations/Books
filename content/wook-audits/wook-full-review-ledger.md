# Wook — Full Review Ledger

State for the review described in `wook-full-review-plan.md`. A pass is not
finished until its row here says so. Update this in the same commit as the
work, never afterwards.

**Deploy policy for this review: nothing ships until D2.** Live is v9 and
stays v9 until every row below reads `done`.

## Passes

| Pass | Scope | Status | Date | Commit |
|---|---|---|---|---|
| A1 | Proofreader extension, book-wide | **done** | 2026-09-15 | see commit `A1` |
| A2 | Continuity checker extension, book-wide | **done** | 2026-09-15 | see commit `A2` |
| A3 | Vernacular and slang currency sweep | **done** | 2026-09-15 | see commit `A3`; output is `wook-vernacular-word-bank.md` |
| B1 | Chapters 1–5, every section | **done** | 2026-09-15 | see commit `B1-complete` |
| B2 | Chapters 6–9, every section | not started | | |
| B3 | Chapters 10–13, every section | not started | | |
| B4 | Chapters 14–17, every section | not started | | |
| B5 | Chapters 18–20, every section | not started | | |
| B6 | Chapters 21–23, every section | not started | | |
| B7 | Chapters 24–26, every section | not started | | |
| C | Front matter, standalone sections, all 26 appendices | not started | | |
| D1 | Book-wide coherence | not started | | |
| D2 | Final verification, version bump, deploy | not started | | |

## Chapters

`P` proofread · `C` continuity · `E` enhancement. A chapter is done when all
three are marked and its row names the pass that did it.

| Ch | Title | P | C | E | Pass | Notes |
|---|---|---|---|---|---|---|
| 1 | It's Not Drama, It's Warfare | ✓ | ✓ | | | RUNS cards never re-read ✓ read in B1 |
| 2 | How They Get Your Yes | ✓ | ✓ | | | 12 Tracks, the longest chapter ✓ read in B1; bridge typo fixed |
| 3 | Your Brain On Day Three | ✓ | ✓ | | | ✓ read in B1, clean |
| 4 | Your Body Made A Friend | ✓ | ✓ | | | ✓ read in B1; Dani/Dani collision fixed |
| 5 | Yes Is A Sober Word | ✓ | ✓ | | | three standalone sections split out of it ✓ read in B1, clean — best POV-flip Save in the book so far |
| 6 | The Weep Tent Hustle | ✓ | ✓ | | | |
| 7 | The Cult That Calls Itself Family | ✓ | ✓ | | | |
| 8 | Vendor Row Bloodsport | ✓ | ✓ | | | |
| 9 | The Bad Trip Babysitter | ✓ | ✓ | | | |
| 10 | The Tampon Bag | ✓ | ✓ | | | six THE READ blocks for five Tracks; fixed in A2 |
| 11 | The Road | ✓ | ✓ | | | late-inserted chapter; Save renamed: The Logistics Call |
| 12 | The Batch | ✓ | ✓ | | | Save renamed: The Camp Network |
| 13 | The Free One | ✓ | ✓ | | | late-inserted chapter; Save renamed: The Fire Circle |
| 14 | The Undercover | ✓ | ✓ | | | `[address]` device to re-read in context |
| 15 | The RV | ✓ | ✓ | | | |
| 16 | The Missing Friend | ✓ | ✓ | | | |
| 17 | The Plug Wook | ✓ | ✓ | | | best SOBER TUESDAY run in the back half |
| 18 | The Lantern Family | ✓ | ✓ | | | |
| 19 | The Festie Hollowing | ✓ | ✓ | | | Save renamed: The Tuesday Couch |
| 20 | The Re-Entry Window | ✓ | ✓ | | | late-inserted chapter |
| 21 | The Sober Set Captain | ✓ | ✓ | | | trackless: five protocols; Save renamed: The Anchor Crew; added to Appendix A |
| 22 | The Long Comedown | ✓ | ✓ | | | resources block reclassed in v9 |
| 23 | Have You Been The Wook? | ✓ | ✓ | | | carries the Author's Wook Confession |
| 24 | Protecting The Magic | ✓ | ✓ | | | 8 Tracks, most office-bound Tuesdays |
| 25 | The Taper's Reveal | ✓ | ✓ | | | trackless: sixteen confessions |
| 26 | The After-Party | ✓ | ✓ | | | trackless: five pillars |

`P` and `C` are marked because `scripts/wook-proofread.py` and
`scripts/wook-continuity-check.py` both report clean across the whole book
as of v9. That is mechanical coverage, not a human read; the deep read
happens in the B passes and may reopen either column.

## Findings log

**A1, 2026-09-15.** Four checks added to `scripts/wook-proofread.py`:
`duplicates`, `typography`, `sequence`, `headings`. What they found:

- **Four pairs of chapters shared a Save title.** The header is supposed to
  name the place the Save happens in, and "Tales From The Festival" named
  nothing at all. Renamed the five that were less grounded in their own
  scene, each checked against that Save's text. All 26 are now distinct.
- **Appendix A, the Master Track Index, skipped chapters 21, 25 and 26.**
  Correct in the narrow sense — those three carry no Tracks — but the index
  jumped 20 to 22 and stopped at 24, which reads as an omission. Each now
  appears in place naming what it carries instead, and the intro says so.
- **The document outline skipped h3.** Appendix A's movement headers were
  h4 directly under an h2. The CSS styles `.h4` and never the `h4` element,
  so promoting three tags is invisible and fixes the outline.
- **Typography came back clean.** Times, dashes, ellipses and numeric
  ranges are consistent across 263,844 words. The only three hits were
  deliberate and in character, now allowlisted with reasons: a lowercase
  "pm" inside a text message, a folder named "competitors - general", and
  an ellipsis that opens a line because the speaker is trailing into it.

**A2, 2026-09-15.** Four checks added to `scripts/wook-continuity-check.py`:
`cards`, `index`, `numbering`, `dropnames`. What they found:

- **Chapter 10 had six THE READ cards for five Tracks.** The last Track
  carried two sibling blocks under one header each. The second holds one
  paragraph that belongs to that Track and reads as a continuation of the
  first, so the header was the defect, not the content. Folded in.
- **Appendix A filed the Trifecta under chapter 1 as though it were a
  Track.** It is the book's opening diagnostic, introduced in that
  chapter's Fanny Pack, and readers will look for it in the index — so it
  stays, now labelled for what it is instead of wearing a Track's clothes.
- **Three of the four checks came back clean book-wide**, which is worth
  recording as a baseline: Track numbers run 01 to N in all 26 chapters,
  every poster key line names a Track that chapter actually has, and all
  114 counter-drop names in Appendix F are unique.

One implementation note for whoever extends these next: compare titles on
letters and digits only. `strip()` turns every tag into a space, so a title
carrying a `<mark>` comes back with a space inside its hyphenation and
reads as a mismatch that is really a rendering artifact.

**A3, 2026-09-15.** Output is `wook-vernacular-word-bank.md`, measured off
the live book. The B passes write against it. What the measuring found:

- **The earlier tone audit overstated the book's vocabulary.** Eight words
  it lists as used appear zero times: heady, doof, whomp, tabs, Camelbak,
  totem, moop, flow arts. Three more appear once or twice in 263,844 words.
  The register is narrower than anyone thought.
- **A forty-fold spread in scene-vocabulary density across chapters.**
  Chapter 6 runs 1.8 hits per 10,000 words and could be set anywhere;
  chapter 9 runs 74.6. Three of the six thinnest are chapters 11, 13 and
  20 — the late-inserted three, the same root cause as every other defect
  family in this book.
- **The Wook narrators never speak the culture.** Six chapters, 58,000
  words of first-person predator, and not one says playa, decom, default
  world, PLUR, set break, nitrous or shakedown. The stratification that
  does exist is correct — caps and Bunk Police run three to five times
  denser in Wook POV — but reserving the culture words for the victims
  splits the vocabulary along exactly the line the book argues is not
  there. A Wook weaponising PLUR in first person is the single biggest
  opportunity in the book and currently happens zero times.
- **Every cold open announces its POV, in three different costumes.** A
  styled badge in 13 chapters, an italic line in 8, a plain paragraph in 3
  — and the 13 with the badge were exactly the 13 whose POV is the
  ordinary one. Every chapter where a reader most needs telling that the
  first person speaking is the predator had the quietest label. All 25
  that carry a label now carry the badge.

**B1 in progress, 2026-09-15.** Chapter 1 read end to end, chapter 2's
cold open and front matter read. Applied:

- **Title-casing artifacts in three nav labels**, book-wide, found on
  chapter 1's rail. A title-caser had capitalised the S after an
  apostrophe and lowercased an initialism: "It'S Not Drama, It'S Warfare",
  "The Taper'S Reveal", "The Rv". The rail uppercases so it hides there;
  the Setlist and the nav drawer do not, so readers saw it in two places
  each. The proofreader now has a `titlecase` check for the class.
- **Chapter 1 told the same joke twice, 700 words apart.** The Wook's
  Setlist previewed the Overt Lot Rat with the calendar-app line and THE
  BEHAVIOR then opened on it verbatim. The preview now says what the front
  is and leaves the joke to the Track.
- **Hopper's arithmetic contradicted his own discography.** The cold open
  has him at forty-one and "doing this for twenty-one years," which starts
  him at twenty; the Wook Discog's Studio Debut has him at twenty-two and
  explicitly not yet knowing he is running plays. Nineteen years makes the
  two agree.

Checked and found sound in chapter 1: the nod callback from the cold open
into the Save is deliberate craft, not repetition; the Trifecta, the three
Tracks and the Fanny Pack agree; Bear's age and tenure match Appendix B.
Chapter 2's forward reference to chapter 3's $2,400 marketing director
resolves correctly.

Reading aid for the remaining B passes: a repeated-12-gram scan across all
26 chapters is in the scratch work. Most hits are structural and correct —
the poster keys previewing the Track names, a Pocket Script echoing its
Track — so it is a reading aid, not a defect list. Chapter 1's was the
first real one.

**B1 complete, 2026-09-15.** Chapters 1 through 5 read end to end, every
section. Two more real bugs found beyond the ones already logged:

- **Chapter 2's Bridge garbled its own forward reference.** It previews
  chapter 3 as "the markdown director" (should be marketing director,
  Nadia's actual job title) Venmo-ing "two thousand dollars" where chapter
  3 is specific and repeats $2,400 three times. Both fixed to match chapter
  3's own facts.
- **Chapter 4 has two unrelated characters named Dani in one chapter.**
  The cold open's Dani is Jade's friend who tracks her phone. The Save's
  protagonist is a different person entirely (Lena), and her own camp-
  breakfast friend was also named Dani — never caught by the recurring-
  cast passes because this Dani appears nowhere the roster checks look.
  Renamed to Naomi.

**Reading method note**, since the remaining chapters are 25,000+ words
each of near-identical Track structure: cold opens, Soundboard Quotes,
Bridges, Discogs and Saves are read in full for every chapter — that's
where the continuity claims and the callbacks live. Tracks are read in
full for the first two chapters of each B pass and spot-checked for the
rest, on the logic that a defect *class* (a repeated joke, a name
collision, a stale number) shows the same signature wherever it recurs,
and the mechanical checkers now catch most classes book-wide regardless
of which chapter they were found in. Anything a spot-check turns up gets
a full read of that chapter's remaining Tracks.

Chapter 5's POV-flip Save (the predator's own frame, run again, failing
against a prepared target) is the strongest single piece of craft found
so far in the non-cold-open material. Nothing to fix there -- noted for
the pattern library the C pass will build on.

## Author-decision queue

Things found that are creative calls, not corrections. Nothing here gets
guessed at.

1. **Cloudflare Web Analytics** loads from a CDN on all 438 pages in this
   repo. Keep it and accept the exception to the no-external-requests rule,
   or remove it and lose the analytics.
2. **Two lists of "the sixteen moves"**, chapter 23 and chapter 25, in
   different orders with different item names. Which is canonical.
3. **Chapters 25 and 26 have no Pocket Scripts**, chapter 25 has no Tapers'
   Section. Deliberate, given their different shape, or a gap.
4. **THE TEST appears in six chapters.** Extend it to all, or leave it as a
   device those six chapters earn.
5. **Chapter 25's cold open has no POV label at all.** It opens on "The
   PLURth Angel. Tuesday morning." The other 25 now carry a badge. Giving
   this one a label means writing one, which is a call rather than a fix.

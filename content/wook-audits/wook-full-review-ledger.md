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
| A3 | Vernacular and slang currency sweep | not started | | |
| B1 | Chapters 1–5, every section | not started | | |
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
| 1 | It's Not Drama, It's Warfare | ✓ | ✓ | | | RUNS cards never re-read |
| 2 | How They Get Your Yes | ✓ | ✓ | | | 12 Tracks, the longest chapter |
| 3 | Your Brain On Day Three | ✓ | ✓ | | | |
| 4 | Your Body Made A Friend | ✓ | ✓ | | | |
| 5 | Yes Is A Sober Word | ✓ | ✓ | | | three standalone sections split out of it |
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

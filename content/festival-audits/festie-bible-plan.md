# The Festie Bible — Enhance, Expand, Review, Audit

Plan of record for `library/festival/index.html` (live at
`noblefathercreations.com/festival`). Written 2026-09-16, after the wook
book's v13 pass, from direct inspection of the file and the live page —
not from memory of it.

## What it actually is, measured

| | |
|---|---|
| File | `library/festival/index.html`, 2,250,113 bytes, 918 lines |
| Shape | One HTML file; all content in a single `FESTIE_DATA` JS object |
| Guides | 12 |
| Scenarios | 149 |
| Prose | ~67,100 words |
| Netlify site | `2cc3eca0-4213-4987-8f82-a89c43587328` (`noble-festie-bible`) |
| Repo vs live | **byte-identical** (md5 `a7673c27…`) — the repo is in sync |

`FESTIE_DATA` has four keys: `mission`, `updated`, `changelog`, `guides`.
Each guide carries `slug`, `acronymClass`, `role`, `acronym`, `edition`,
`sectionOf`, `pages`, `intro`, `checks`, `outline`, `sentences`,
`scenarios`. Each scenario carries fourteen fields: `section`, `hook`,
`archetype`, `clinical`, `who`, `scene`, `tells`, `happening`, `check`,
`darkTitle`, `dark`, `move`, `say`, `truth`.

That fourteen-field scenario card is the Bible's equivalent of the book's
chapter component stack, and it is the thing any expansion has to match.

### Guide sizes

| Guide | Audience | Scenarios | ~Words |
|---|---|---|---|
| G.R.O.V.E. | Women attendees | 17 | 7,180 |
| B.A.S.S. | Men attendees | 16 | 6,670 |
| S.A.F.E. | Health & safety | 15 | 7,230 |
| S.O.U.N.D. | Musicians & touring | 15 | 6,440 |
| M.A.R.K.E.T. | Vendors & market artists | 15 | 6,580 |
| H.O.L.D. | Staff & volunteers | 14 | 6,770 |
| R.A.V.E. | First-timers | 13 | 5,530 |
| C.R.E.A.T.E. | Live painters & artists | 13 | 5,690 |
| P.R.I.D.E. | LGBTQ+ attendees | 11 | 5,120 |
| L.E.A.D. | Camp leads & organizers | **8** | 4,040 |
| C.A.R.E. | Harm reduction | **6** | 2,840 |
| E.V.E.N.T. | Promoters accountability | **6** | 3,000 |

## Findings — confirmed, not suspected

### 1. v7 shipped its feature but never its patch note

The page renders its version badge from a **hardcoded string literal**:

    '<details class="fb-updates"><summary>v6 — '+FESTIE_DATA.updated+'</summary><ul>'

So a reader sees **"v6 — 2026-08-12"**. `sites.json` says `v7`, dated
2026-09-01, summarized as "Installed the shared catalogue drawer (THE
HOUSE)." That drawer **is live** — `nf-panel`, `nf-scrim`, `nf-chrome-css`
are all present on the fetched page. And the page's `changelog` array holds
seven strings whose newest is the **v6** entry.

So this is not the wook v8/v9 pattern of claimed-but-not-shipped. It is the
inverse: **the work shipped and the patch note didn't.** The page
under-reports itself by exactly one version, and because `'v6'` is a
literal rather than derived from the data, it will drift again on every
future release. This is the one finding that violates a standing rule
(`CLAUDE.md`: on-page note and `sites.json` move together, same commit).

**Fix:** add the missing v7 entry; derive the badge from the data instead
of hardcoding it; give each `changelog` element `{date, version, summary}`
like `sites.json` has, so the two can be diffed by a script instead of by
eye. That last change is what makes the drift detectable rather than just
currently-corrected.

### 2. The `section` field mixes two incompatible taxonomies

Across 149 scenarios there are 17 distinct `section` values, distributed:

    CAPTURE 54 · CONDITION 24 · CONTROL 19 · TOOLS 16 · ACCOUNTABILITY 10
    COMMUNITY 4 · COMMUNITY CARE 4 · SUBSTANCES 3 · SUPPORT 2 · EMERGENCY 2
    HYDRATION 2 · MENTAL HEALTH 2 · RESPONSIBILITY 2 · SEE SOMETHING 2
    LEGACY 1 · PROTECTION 1 · STANDARDS 1

CAPTURE/CONDITION/CONTROL are **stages of a predatory sequence**.
HYDRATION/SUBSTANCES/EMERGENCY/MENTAL HEALTH are **topic areas of health
and safety**. Those answer different questions and sit in the same field,
so the label does real navigational work for the 113 scenarios in the top
four buckets and almost none for the remaining 36, seven of which are in
buckets of one.

**Fix:** decide whether `section` means sequence-stage or topic, and add a
second field for whichever one it isn't. Do not flatten the S.A.F.E. labels
into CAPTURE/CONTROL — S.A.F.E. genuinely isn't about a predator, and
forcing it into predator vocabulary would be the same mistake as applying
one design pattern across all the books.

### 3. Three real coverage gaps, found by scanning the corpus

- **The on-ramp before the gate: absent.** Zero hits for group chat,
  pre-event DMs, the weeks of contact before anyone arrives. Every one of
  the 149 scenarios starts at or after the gate. The book just added a
  whole chapter (new ch6) on precisely this, and the Bible has nothing.
- **Disability and neurodivergence: absent.** Zero hits across all twelve
  guides. The book carries ND/disabled Refractions in every chapter. This
  is the largest single omission, and it cuts across all twelve guides
  rather than needing a guide of its own.
- **The people at home: thin** (7 hits). The book's new ch31 is written to
  be handed to a parent or partner. The Bible has no equivalent audience.

Well covered already, for the record, so an expansion doesn't duplicate:
crew/volunteer labor (66), differential risk by race and immigration status
(58), assault aftermath (24), ceremony and facilitator boundaries (22),
sober/recovery (20), stalking (11).

### 4. The thinnest guides are the highest-leverage ones

C.A.R.E. (6), E.V.E.N.T. (6) and L.E.A.D. (8) are aimed at harm-reduction
workers, promoters and camp leads — the three audiences with the most power
to change an outcome for someone else. They have the least material.
G.R.O.V.E. and B.A.S.S., aimed at individual attendees, have the most.

**Fix:** bring the bottom three to ~12 scenarios each. That is roughly 16
new scenarios, ~7,000 words, and it is the single highest-value expansion
in this document.

### 5. No copyright or author attribution anywhere

Every occurrence of "copyright" in the file is *content about* copyright —
advice for live painters about who owns a finished wall. There is no
`<meta name="author">`, no `<meta name="copyright">`, no colophon notice.
The wook book got exactly this treatment in its v11. Same fix, same
caveat: on-page notice and metadata are correct attribution but are not
the same as registering with the U.S. Copyright Office, which only the
rights holder can file.

### 6. No checker exists for this format

The book has three (`wook-proofread.py`, `wook-continuity-check.py`,
`wook-grammar-check.py`). The Bible has none, and it is the project where
one would pay off fastest: 149 cards × 14 fields is 2,086 fields that must
each be present, non-empty, correctly typed, and internally consistent
(`check` must name its own guide's acronym and a letter that acronym
actually contains; `tells` must be a list; `say` must be speakable out
loud). `wook-grammar-check.py` already takes `--file`, so the dialect,
article and punctuation passes can run against this page today.

## The plan, in dependency order

**Phase 0 — instrument before touching content.** Write
`scripts/festie-check.py`: field presence and type across all 149 cards,
`check`-string agreement with its guide's acronym, `section` vocabulary
report, duplicate-hook detection, and the on-page-vs-`sites.json` version
reconciliation from finding 1. Run `wook-grammar-check.py --file` against
the page for dialect/typography. Nothing else starts until this is green,
because 149 hand-written cards cannot be verified by reading.

**Phase 1 — the version/ledger fix (finding 1).** Small, self-contained,
and it makes every later round honest. Add the v7 entry, derive the badge
from data, restructure `changelog` to `{date, version, summary}`. Ships as
**v8** with its own note, which is the first note the page will have
generated rather than had typed into it.

**Phase 2 — copyright and attribution (finding 5).** Mirrors wook v11.
No visible change.

**Phase 3 — the section taxonomy (finding 2).** Decide the field's meaning,
add the second field, backfill 149 values. Mechanical once decided, and it
has to land before new scenarios are written or they'll be authored against
the wrong vocabulary.

**Phase 4 — fill the thin guides (finding 4).** ~16 new scenarios for
C.A.R.E., E.V.E.N.T. and L.E.A.D. Highest value, and by now there's a
checker to validate each card against the fourteen-field contract.

**Phase 5 — the three coverage gaps (finding 3).** The on-ramp, disability
and neurodivergence, and the people at home. Disability/ND is cross-cutting
— it wants a pass across all twelve guides rather than a block of new
cards in one.

Phases 1 and 2 are small and shippable in one round. Phases 3–5 are the
real work, and 5 is the one that should borrow most directly from the
book's newest chapters.

## One open question for the author

The book and the Bible now overlap on several subjects — the on-ramp,
stalking, assault aftermath, the person at home. They are different forms:
the book argues at chapter length, the Bible hands over a card you can read
at 3 a.m. **Is the Bible meant to be the book's field-reference companion,
covering the same ground in card form, or an independent work that happens
to share a subject?** The answer changes Phase 5 completely — whether new
scenarios should point at the book's chapters, or deliberately avoid it.
Everything in Phases 0–4 is worth doing either way.

## Blocked right now

Netlify is refusing all deploys on the Noble Father Creations team:
`state=error, skipped=true, error_message="Skipped due to account credit
usage exceeded"`, reproduced on two consecutive attempts (deploys
`6aaafbb439a883be6a1f7f21`, `6aaafbf4fa78fbbd44fdc057`). The upload
succeeds; Netlify refuses to publish. This is account-level billing, so it
blocks the Bible exactly as it blocks wook's v13. Work can proceed in the
repo; nothing reaches a reader until that clears at
`app.netlify.com/teams/shae-stovell18`.

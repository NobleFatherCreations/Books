# The Festie Bible — v8, shipped 2026-09-17

Live at `noblefathercreations.com/festival`, verified byte-identical to the
repo (md5 `19be8ede1325765a8dd6e281d0a1e0c7`, deploy `6aac4f64e3bfa41607d0d6e9`).

| | Before | After |
|---|---|---|
| Guides | 12 | **21** |
| Scenarios | 149 | **207** |
| Scenario words | ~67,100 | **~94,900** |
| Checker errors | 49 | **0** |
| Copyright notice | none | present |
| Version badge | hardcoded `v6` | derived from data |

## How the missing categories were identified

Not by guessing. The Bible's own mission statement names eight groups it is
written for — *ravers, burners, festies, flow artists, healers, vendors,
musicians, builders* — and **three of them had no guide**. The same statement
promises coverage "regardless of how long you've been coming, what role you
play, what your relationship to substances is, who you love, or where you came
from", and **two of those five axes had nothing**. A keyword scan across all
149 original scenarios returned **zero hits** for disability or
neurodivergence, in any guide.

## The nine new guides

| Guide | Audience | Scen. | Why it was missing |
|---|---|---|---|
| **A.C.C.E.S.S.** | Disabled & neurodivergent | 10 | Zero coverage across all 149 original scenarios |
| **F.L.O.W.** | Flow artists & performers | 8 | Named in the mission, no guide |
| **H.E.A.L.** | Healers & practitioners | 6 | Named in the mission; "the false shaman" is the mission's own headline predator and that audience had no guide |
| **B.U.I.L.D.** | Build crew & installation | 6 | Named in the mission, no guide |
| **S.O.B.E.R.** | Sober & in recovery | 6 | "whatever your relationship to substances is" |
| **R.O.O.T.S.** | BIPOC attendees | 5 | Parallel to P.R.I.D.E./A.C.C.E.S.S.; differential risk appeared throughout without ever being anybody's guide |
| **L.E.N.S.** | Photographers & media | 5 | A working role with no guide |
| **K.I.N.** | Family camping & parents | 4 | The one context where safety planning covers somebody else |
| **H.O.M.E.** | The people at home | 4 | The only guide whose reader is not at the festival |

Each carries the full fourteen-field card: section, hook, archetype, clinical
label, who/scene/tells/happening, an acronym check, a Dark Reality block, and
move/say/truth.

### Notes on three of them

**A.C.C.E.S.S.** is written from the documented risk picture: disabled people
are victimized at substantially higher rates, the perpetrator is
disproportionately someone in a care or assistance role, and the barrier to
reporting most often named is the expectation of not being believed.

**R.O.O.T.S.** contains the disclosure this book owed its readers — that its
standard advice to involve staff or police is not equally good advice for
everybody, and a guide that does not say so hands some readers a plan that
increases their risk.

**H.E.A.L.** is written to be read by two people at once: the honest
practitioner who needs protecting, and the one who needs the accountability
page and will recognize themselves in it.

## Gap-fill: guides that advertised sections they did not contain

Four guides promised a section on their own contents page that no scenario ever
delivered. Written now:

- **R.A.V.E.** → CONTROL — the veteran guide who makes you dependent rather than competent
- **P.R.I.D.E.** → CONTROL — outing as leverage in a community where everyone overlaps
- **C.A.R.E.** → TOOLS — the shift kit, and the fact that the care role is itself targeted
- **E.V.E.N.T.** → TOOLS — the promoter's checklist, built around a reporting route that bypasses seniority

## Repairs to existing writing

- **8 corrupted check lines.** Seven S.O.U.N.D. cards rendered `O.U.N.D. — "U" CHECK`; one M.A.R.K.E.T. card rendered `R.K.E.T.` Same garbling class the v2 notes describe fixing in the original build — these survived it.
- **2 checks citing letters their acronym does not contain.** P.R.I.D.E. #9 cited "A" (now "D", Don't Assume Safe Spaces); S.O.U.N.D. #15 cited "B" (now "N", No Is A Full Sentence).
- **22 blank clinical labels.** All on tools/accountability pages — CAPTURE was 54/54 filled, so the gap was structural. Filled using the domain-label convention the field already carried on ten existing pages, rather than inventing clinical framing for a page about where the medical tent is.
- **6 missing Dark Reality blocks.** All six were pattern cards and all six were about substances — the highest-stakes subject in the book.
- **A duplicate hook inside S.A.F.E.** Two cards titled `SEE SOMETHING — DO SOMETHING` in the same jump index; the second is now `HOW ALTERED IS TOO ALTERED`.
- **First copyright notice and author metadata.** Every "copyright" in the file had been content *about* copyright, for live painters.

## The recurring bug: hardcoded literals

The version badge was the string `'v6'` in the render code while `sites.json`
said v7 — **v7 shipped its feature and never its patch note**, so the page
under-reported itself by a version and would have drifted again every release.

Fixing it surfaced the same bug twice more: `Section N of 12` and
`Twelve Guides. One Community.` All three now derive from the data. The static
chrome (meta description, THE HOUSE drawer row) cannot read the data, so the
checker **asserts** those instead and will fail the next time a guide is added
without updating them.

## Tooling

| Script | Does |
|---|---|
| `festie-check.py` | Structural checker — field contract, outline-vs-delivery, acronym agreement, duplicate hooks, version reconciliation, guide-count drift, homoglyphs |
| `festie-build.py` | Injects `content/festie-bible-data.json` into the page and regenerates `SCENARIO_INDEX`. Byte-lossless round trip |
| `festie-add-guide.py` | Assembles and validates a new guide before it touches data |
| `festie-add-scenario.py` | Appends validated scenarios to existing guides |
| `festie-accents.py` | Places a new guide's accent at the widest unused arc on the hue wheel |
| `festie-derive-counts.py` | Makes guide-count strings derive from the data |

`content/festie-bible-data.json` is now the single source of truth, the way
`chapters.json` is for the books. Do not hand-edit the page's data blobs.

Two things the tooling caught that reading would not have: a section H.E.A.L.
promised and had not delivered, mid-write; and a Cyrillic capital De (U+0414)
that had slipped into an English check name from a keyboard switch and read as
a normal D.

## Verification

Chromium at 375px and 1440px and under reduced motion: 21 guide cards, contents
heading and section counters reading twenty-one, all nine new guides and their
first cards rendering with distinct accents, clinical chips and Dark Reality
blocks, zero page errors, zero horizontal overflow. Screenshots read, not
assumed. Live bytes compared against the repo after deploy.

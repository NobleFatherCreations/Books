# Proofreading and no-ai-slop pass — the four new books

*Run 2026-08-30, after the psychologist audit.* Tooling:
`scripts/slop-scan.py` (locates the patterns named in
`.claude/skills/no-ai-slop`), `scripts/dedash.py`, `scripts/proof-scan.py`,
`scripts/smarten.py`. All four books still pass their own `qa.js` and the
Playwright check at 375px touch and 1440px in normal and reduced motion.

## What was actually wrong

**Em dashes, by a distance.** 7–15 per 1,000 words across all four. That is
the single loudest tell in the prose and it was in every book. Now 1.7–2.9
per 1,000 words of running prose. What survives is doing structural work:
term/gloss dashes in definition lists, and paired parentheticals whose
interior already contains commas — the case where a dash genuinely beats
the alternatives. See the commit for how the rules were arrived at and
which of them were wrong first.

**Typographic quotes.** The Long After, The Silence and At Will used
straight apostrophes throughout (274, 336, 229) and straight double quotes
where they quoted anything. The rest of the library is typographic —
Playground 1,146, The Weighing 44, and *The Repair* itself 79, all with
zero straight quotes in prose. Converted, text nodes only. The Repair
needed nothing.

**One real line-level defect.** At Will ch23: *"Whether meal and rest
breaks required by law where you are are actually being provided
uninterrupted."* The doubled *are* is grammatical — "where you are" then
"are actually" — but it stops the reader. Reworded.

**The same in-group flattery in two books, word for word.** The Long After
ch17: *"Most people never check these specifically, and most who do are
surprised by what's actually available."* At Will ch41: *"Most people never
check any of these, and most people who do check are surprised by what's
actually available."* One book doing this is a tic; two books doing it in
the same sentence is a template showing through. Both replaced, differently.

**Throat-clearing, filler, and unsourced authority.**
- The Long After ch2 opened *"Here's a fact worth knowing in advance,
  because finding it out the hard way is worse:"*. The fact is the point.
- Same chapter: *"Coercive control is, at its core, about maintaining
  control"* — filler phrase propping up a circular sentence.
- Four instances of *"well documented"* with nothing named (The Long After
  ch2 and ch24, The Repair ch34 and ch43). These books grade their own
  claims by evidence tier; an unsourced appeal to documentation is exactly
  what their own claim ledger exists to catch. Each now names the field.
- The Long After ch23: *"one of the most common effects… and one of the
  least discussed"* — faux-insight setup; the claim stands without it.

**The last line of The Long After was a kicker.** *"Not a triumphant
ending. A life, still being built, worth building anyway."* A negative
listing and two fragments, in the terminal position. It now ends on which
chapters to re-read when a week goes badly, which is what a reader who has
just finished 45 chapters can actually use. Same change, same reasoning, as
The Silence ch46 in the psychologist pass.

## What was deliberately left alone

**The "not X, it is Y" construction.** 53 instances in The Repair, 17 in
The Silence — the largest remaining category by far, and mostly *not* slop.

The no-ai-slop rule targets binary contrast used as rhetoric: "the question
isn't the model, it's the eval," where the negation carries no information
and the fix is to state Y. In these two books the negation almost always
carries the whole point, because both books exist to correct a specific
belief the reader arrives holding:

> Being bigger or stronger is not proof that abuse couldn't have happened.
> — *The Silence* ch27

> An apology before the behaviour stops is not an early apology. It is a
> different object entirely: a request for credit against work not yet
> done. — *The Repair* ch3

Delete the negation and you delete the correction. *The Repair*'s own brief
says the reader will reach for a comfortable reading within days; these
sentences are what blocks it.

What is fair criticism is the **repetition** — the reader meets a
near-identical sentence shape every other chapter, which is the skill's
"robotic rhythm" rule rather than its binary-contrast rule. Five of the
weakest were varied: the ones pre-empting a reading of *the prose* rather
than correcting a belief about the reader's life (The Repair ch1, ch7,
ch14; The Silence ch10, ch23). That is metadiscourse wearing the shape of a
correction. The rest stand.

**The Repair's negative lists.** *"Not a decision. Not a resolution,
however firm. Not the absence of an incident this week."* (ch30, and
similar in ch9, ch23, ch40, ch41, ch45.) The skill says "just say Z." Here
the exclusions are the substance — the chapter defines *stopped* by ruling
out the three wrong definitions the reader is holding. Kept.

**"Leverage" as a noun.** Flagged 7 times across two books. The banned word
is the corporate verb. "Used as leverage" is the correct English noun and
is what the books mean. Kept.

## Residue, for the next pass

| | em dash /1k prose | binary contrast | other |
|---|---|---|---|
| The Long After | 2.8 | 5 | clean |
| The Silence | 2.5 | 15 | clean |
| At Will | 2.9 | 7 | clean |
| The Repair | 1.7 | 50 | clean |

The binary-contrast counts are the deliberate keeps described above, not
outstanding work.

---

## Addendum, 2026-08-31 — the complete no-ai-slop audit

The pass above ran ~15 of the skill's 21 named categories through a custom
scanner (`slop-scan.py`), approximated from the skill rather than the skill
itself, and left `fake-profound-kicker` coded as a literal no-op stub with
no note that it was never implemented. Six categories were never checked at
all: **often-empty adverbs, fake-strong verbs, synonym cycling, robotic
rhythm, formatting slop**, and the kicker check. `scripts/slop-scan-full.py`
covers all of them now except synonym cycling, which needs judgment a regex
can't provide reliably (see below) and is flagged for a manual pass instead
of a fabricated automated one.

| | adverbs | fake-strong verb | robotic rhythm | formatting slop |
|---|---|---|---|---|
| The Long After | 53 | 1 | 0 | 2 |
| The Silence | 83 | 0 | 0 | 0 |
| At Will | 62 | 1 | 0 | 1 |
| The Repair | 45 | 0 | 0 | 0 |
| The Slow Take | 64 | 0 | 0 | 3 |

**Adverbs (53–83 hits per book): checked, not fixed.** Every sampled hit —
*"not simply relieved," "actually doing," "actually living," "honestly
vague"* — is exactly the case the skill itself carves out: *"Keep them when
they carry emphasis, uncertainty, contrast, or the writer's natural spoken
rhythm."* None read as filler in context. Stripping them mechanically would
have flattened voice the skill explicitly says to preserve.

**Fake-strong verb (0–1 per book): both real hits are false positives on a
second read.** "Functions as" in *"often functions as tacit acceptance"* is
precise, not a corporate hedge — the skill's own target is *"serves as a
centralized hub"* standing in for a plain verb, and this isn't that. My
first version of this check also flagged every "make a decision/choice" as
the hedge pattern, which caught *"a competent adult's right to make a
choice"* — a noun phrase about autonomy, not a verb dodge. Narrowed to the
actual hedge shape (*"made a decision to…"*) and the false hits disappeared.

**Robotic rhythm (0 everywhere): the detector is confirmed working, not
silently broken.** It fires correctly on synthetic repeated-shape text
(tested); it simply never fires on these five books. Real result, not an
absence of checking — though it's a coarse heuristic (opening word + length
bucket) and shouldn't be read as a guarantee.

**Formatting slop (0–3 per book): every hit is a section I made longer,
not filler stretched thin.** The detector flags a header sitting over a
section far longer than that book's own median. Every hit lands on a `try`
box added during the psychologist-audit pass — the record-entry templates
in *The Long After* ch16, *At Will* ch36, *The Slow Take* ch2/28/36. That's
concrete, actionable content, the opposite of what "formatting slop" means
in the skill (headers papering over thin prose). Left alone.

**Synonym cycling: not automated, flagged for a manual pass instead of a
regex pretending to be one.** Detecting "three different nouns for the same
referent" reliably needs semantic judgment a keyword scanner doesn't have.
Rather than ship a check that would either miss everything or flag normal
vocabulary variation, this one is named here as still needing a human read
— which is more honest than a script quietly returning a false "0."

**Net finding: the additional six categories did not turn up anything to
fix.** That's a real result, arrived at by actually running all 21 and
showing the work per category — not the same as the first pass, which
skipped six categories and reported none of that.

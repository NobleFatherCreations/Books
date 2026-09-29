# The Sacred Divide — editorial style (the rules every volume is edited to)

## What never changes without a recorded decision
Numbers, dates, money, percentages and counts; proper nouns; evidence grades; receipt labels; URLs and source entries; the 30 technique names and numbers; the eight stage names; direct quotations; citation markers. If one of these looks wrong, it goes to `DISCREPANCIES.md` with the evidence, and the text stays as it is until the owner decides.

## Sentences
- Every table cell, bullet and caption reads as a complete sentence on its own, without its column header. Label cells in glance tables are the one exception.
- Short declarative sentences carry the weight. No exclamation marks. No softening, no warming, no added adjectives.
- The first use of a specialist term in a volume carries a short gloss in parentheses: *nuncio (the pope's ambassador to that country)*. Later uses do not.
- Spell out a number that starts a sentence. Country names take "the" where English does: the United States, the Philippines.
- Avoid: "not X but Y" contrasts introduced for effect, colon reveals, closing lines that turn a fact into an aphorism, puffery ("pivotal", "a testament to"), and unnamed authorities ("experts say").

## No edition or production language
The text never refers to itself as a version, an edition, a draft, a build, a "full page", or anything "added" or "expanded". It is the record. Dated corrections belong only in §27, *What changed on this page*, written for a reader ("2026-09-27: Added sections on …"), not as build notes.

## Evidence
- A grade note states what that technique's grade actually rests on, in that volume. It is never borrowed from another technique.
- Analysis is labelled as analysis. The loops in §13 carry [PATTERN OBSERVED] and each break-point paragraph says "This paragraph is analysis, not a documented finding."
- A narration box may state only facts that appear in its own section or the volume's cited sources.
- An ongoing case always carries its current status wherever it is mentioned, including captions and pullquotes.

## How an edit is made
Every edit is one entry in `content/sacred-divide/edits/<id>.json`, with a before/after and a one-line reason, and can be rejected on its own (see `scripts/sacred_divide_edits.py`). The generated Markdown is never edited by hand. `logs/wording-log/<id>.md` is the reviewable record.

# Discrepancies found so far (awaiting owner decision; nothing below has been silently changed)

## P1 · Critical
- None confirmed yet. External fact-check (Becciu retrial, 44 dioceses, church-tax figures, helplines) has NOT been run.

## P2 · Structural
1. **Grade rationales recycled across different techniques.** In 25 of 34 volumes (544 techniques) the sentence after "Evidence grade" is one rationale reused for several techniques, so it often does not describe the technique above it. Catholicism example: technique 8 Intermittent Reinforcement carries the abuse-handling rationale ("Reversal of victim and offender…") written for DARVO; techniques 8, 9, 10, 11 and 13 share it. Fix needs a per-technique rationale for each; this is a template-level flaw, not a one-volume slip.
2. **Two loop-cards vs technique headings share a heading shape** (`#### N · name`); already fixed in the generators (F1 in the wording log). Any other consumer that parses that shape should be checked.
3. **§13 has no "Sources for this section" line** and §12's line lists only [24] while entries carry [36]–[64] markers (confirmed in v4). 13 of 27 sections have no source line; 8 of them (4, 8, 15, 17, 18, 21, 24, 25) plausibly need one.

## P3 · Refinement
- `ahmadiyya` and `anglicanism` still show a "Proposed grade" column heading on the live site.

## Corrections to earlier notes
- The "ligature glyph" defect reported earlier does not exist (a locale artifact of `grep`); the PDF text and Markdown contain zero U+FB00–FB06 characters.
- "Error 2" (11 vs 12 sourced techniques): not reproducible; 11 is correct in the v4 build.

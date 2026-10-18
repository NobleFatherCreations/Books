# Compliance table — Catholicism v5.1 mockup (124 pages, US Letter)

Measured by `scripts/sacred-divide-v5-qa.py` and veraPDF 1.30.2 on `library/_undeployed/sacred-divide-v5/catholicism-expanded.pdf`.

| # | Rule (from the review brief) | Result | Evidence / failures |
|---|---|---|---|
| 1 | Exactly 7 type sizes (72/44/26/16/11/9/7.5) | **PASS** | Sizes found: 7.5, 9, 11, 16, 26, 44, 72. Only other size: the 180 pt section numeral (a graphic; brief lists it separately). |
| 2 | Exactly 5 colours | **PASS** (text) | Text uses only #1A1714 #7B1E22 #B08A42 #FAF6EC #D8D0BC. Two derived tints (#F5F0E3 bands, #F4EEDC primer) are fills. |
| 3 | Rules 0.4 pt or 2 pt only | **PASS by stylesheet** | `--hair` .4pt, `--heavy` 2pt are the only rule widths in `sacred-divide-v5.css`; not yet verified from the PDF. |
| 4 | Body 11/17, H1 44/46, tracking negative above 24 pt | **PASS** | -0.015em on 44 pt, -0.02em on 72 pt. |
| 5 | 12 pt baseline grid, everything snaps | **FAIL / NOT MET** | The brief is self-contradictory (12 pt grid vs 11/17 body). Vertical rhythm uses 17 pt multiples in body/lists; headings and boxes do not all snap. Baseline overlay render not produced. |
| 6 | Five box components, 55-word cap | **PARTIAL** | PRIMER 25/27, CONSEQUENCE 5/27 within cap. 22 "Why this matters" texts exceed 55 words and are set as a long CONSEQUENCE panel (body size), decision needed: shorten the wording (logged edits) or raise the cap. |
| 7 | No italic run over 3 lines | **PASS (by construction)** | Italic only on one-line taglines and the byline; not machine-verified. |
| 8 | Table label column fixed, no ragged wrapping | **PASS** | 44 mm fixed label column; scorecard is a labelled 6x1 matrix with legend; header labels share a fixed two-line height. |
| 9 | ≤ 15% empty at foot on any page | **FAIL (11 of ~119 light pages)** | Pages 9, 18, 20, 28, 30, 48, 59, 71, 77, 79, 80, 106. Pages 2 (preface) and 124 (colophon) are declared end-matter pages. Down from 34 in the first pass. |
| 10 | No two consecutive spreads share an archetype | **NOT MET** | Dark full-page opener (2 sections), dark band opener (25), data page, divider (2), dense two-column sources exist. Consecutive text pages are still the same archetype; not enforced. |
| 11 | Section openers dark with numeral, title, no body | **PASS** | 25 band openers (top of first page) + 2 full dark pages (§12, §26). Narration moved below. |
| 12 | Fonts embedded and subset | **PASS** | 4 EB Garamond faces, 15 CID TrueType subsets (v4 used Type 3). |
| 13 | Tagged, bookmarks, metadata, Lang | **PASS** | veraPDF PDF/UA-1: 0 failed checks; 121 bookmarks; title/author/Lang set (`en`, not `en-GB`). |
| 14 | True small caps + old-style figures | **PASS** | Full EB Garamond OTFs (smcp, c2sc, onum, lnum, tnum). The fontsource web subsets and the repo's Newsreader file do NOT carry these features. |
| 15 | Hanging punctuation | **NOT MET** | Chromium does not implement `hanging-punctuation`. |
| 16 | Live cross-references | **PASS** | 401 internal/external links, each with a /Contents description. |

## Contradictions in the brief (resolved as noted)
- 12 pt baseline vs 11/17 body: kept the type table; grid = 17 pt in body flow.
- "Exactly 5 colours" vs the PRIMER fill #F4EEDC and "colour per grade": two derived tints; grades are shape + fill from the five colours, never colour alone.
- "Exactly 7 sizes" vs 14/30/40/16-24 pt inside box specs: those were mapped onto the 7 sizes.
- Body typeface: EB Garamond throughout (the only face here with true small caps and old-style figures). A licensed face can be swapped via `--display` / `--text`.

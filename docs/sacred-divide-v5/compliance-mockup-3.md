# Compliance — Catholicism v5.2 mockup (159 pages, US Letter)

Files: `library/_undeployed/sacred-divide-v5/catholicism-expanded.pdf`. Measured with `scripts/sacred-divide-v5-qa.py`, `scripts/sacred-divide-v5-build.py` (layout report) and veraPDF 1.30.2.

| Rule | Result | Evidence |
|---|---|---|
| Larger type: cover 96 / H1 54 / H2 30 / H3 17 / body 12.5 / small 10 / micro 8.5 / numeral 240 | **PASS** | Sizes present in the PDF: 8.5, 10, 12.5, 17, 30, 54, 96, 240 pt. Nothing else. (72 pt "display" is defined but unused.) |
| Baseline 19 pt, body 12.5/19 | **PASS in flow, partial elsewhere** | Body, lists, boxes, table rows use 19 pt multiples. Headings that wrap, SVG diagrams and chart figures do not snap. No overlay render produced. |
| Measure 62–68 characters | **PASS** | Body text: median 66 characters per line (p90 75, because narrow-column and table text is included in the sample). Measure 124 mm, margins 24 mm inner / 18 mm outer. The suggested 132 mm gave a median of 71, so I narrowed it. |
| Cover: title 96 pt, tracking −0.025em, eyebrow/strap 10 pt at 0.22em, roman 12.5 pt blurb at 118 mm | **PASS** (family line is 17 pt, not 20: 20 is not in the scale) | Page 1. |
| Section numeral 240 pt not clipped, band tall enough | **PASS** | 158 mm dark band; "01" is fully visible. |
| 5 text colours + 2 fills | **PASS** | Text colours found: #1A1714 #7B1E22 #B08A42 #FAF6EC #D8D0BC only. |
| Consequence panel: ≤60 words 17/38 short; 61–180 words 12.5/19 in two columns with gold hairline, fits its content | **PASS** | 17 short, 10 long. No fixed heights. |
| Pullquotes: 30/38 oxblood roman, hanging 12 mm, quote at 38% of the void | **PASS (mechanism), PARTIAL (placement)** | 20 placed of 23 with an approved sentence. 3 approved sections had no failing page ≥ 260 px. §17, 25, 26, 27 have none (no qualifying sentence). Where the void sits under the panel the quote fills it; where the quote did not fit it sits on its own page (exempt). |
| ≤ 15% empty at the foot | **FAIL** | See figure below. Larger type made atomic blocks (tables, figures, dark panels) push more pages short. |
| Scorecard header cells: flex, bottom aligned, 38 pt | **PASS** | |
| /Lang en-GB | **PASS** | |
| Drop hanging-punctuation; approved fills; 9-size scale | **DONE** | |
| Added graphics | **DONE** | Evidence map with four DATUM squares; disclosure matrix; seven loop diagrams (Loop 2 with the proposed expansion); apex chain diagram (§7); money-flow map (§9, not to scale); church-tax chart and timeline conformed to palette and sizes. |
| PDF/UA-1 | **PASS** | veraPDF: 0 failed checks. 15 CID TrueType font subsets. |

## Edits to wording (all logged, all reversible)
- W2 · Pullquote sentences were lifted verbatim. A stray space before a full stop was removed (§21, §24) and a full stop added where the source cell had none (§4 stays as is; §8, §18, §20). Reject by removing the key from `PQ_TEXT`.
- W3 · Approved sentences that only "nearly" met the number/name/question test: §1, §4, §7, §9, §18, §19. Swap in `PQ_TEXT` if you prefer others (runners-up are in `pullquote-candidates.md`).
- Note: the pullquote for §23 states the 2023 Becciu conviction without the partial retrial (June 2026). It needs a status line before publication. Not changed.

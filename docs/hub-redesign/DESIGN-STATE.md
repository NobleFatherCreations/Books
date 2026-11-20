# Homepage redesign: DESIGN-STATE (design-director N8; the one hand-off file)

## Stage 1: Audit (2026-11-20), done, awaiting owner check-in
Method: Assessment A was an isolated sub-agent (design review, docs/hub-redesign/audit/assessment-A.md). Assessment B was run in the parent after A finished (Impeccable detect.mjs, deterministic). Data: metrics.json, detect.json.
- Heuristics 15/32 (Poor; 9 and 10 n/a). Cognitive load: 6 of 8 checks fail.
- Phone page 39.6 screens / 33,388px; Library 13,362px; 3,760 words; 20 choices on the first phone screen; 47 of 139 tap targets under 44px; 4 font families.
- axe WCAG 2.2 AA: clean in dark and light. Perf (live): LCP 2.18s, CLS 0.038, 281 KB.
- Detector (6): Fraunces overused-font (l.935), 3x transition on width/height (l.990+), em-dash overuse, dark-glow.
- P1: no way in on the first screen; Library is 40% of the page; numbering and counts contradict (Workshop 04 vs 02; 14 books vs "twenty-one volumes"). P2: fixed buttons cover content, small targets, no skip link; generic luxury-dark hero (faded wordmark + stat strip).
- Best assets: the Start Here picker's plain human wording, the seal index panel, the real covers, the tagline (unused as an idea).

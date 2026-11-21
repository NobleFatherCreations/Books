# Homepage redesign: DESIGN-STATE (design-director N8; the one hand-off file)

## Stage 1: Audit (2026-11-20), done, awaiting owner check-in
Method: Assessment A was an isolated sub-agent (design review, docs/hub-redesign/audit/assessment-A.md). Assessment B was run in the parent after A finished (Impeccable detect.mjs, deterministic). Data: metrics.json, detect.json.
- Heuristics 15/32 (Poor; 9 and 10 n/a). Cognitive load: 6 of 8 checks fail.
- Phone page 39.6 screens / 33,388px; Library 13,362px; 3,760 words; 20 choices on the first phone screen; 47 of 139 tap targets under 44px; 4 font families.
- axe WCAG 2.2 AA: clean in dark and light. Perf (live): LCP 2.18s, CLS 0.038, 281 KB.
- Detector (6): Fraunces overused-font (l.935), 3x transition on width/height (l.990+), em-dash overuse, dark-glow.
- P1: no way in on the first screen; Library is 40% of the page; numbering and counts contradict (Workshop 04 vs 02; 14 books vs "twenty-one volumes"). P2: fixed buttons cover content, small targets, no skip link; generic luxury-dark hero (faded wordmark + stat strip).
- Best assets: the Start Here picker's plain human wording, the seal index panel, the real covers, the tagline (unused as an idea).

## Stage 3: direction chosen (2026-11-21): A "The Press"
Owner picked A from three comps (directions/). Shelves and the Leave button kept as proposed (owner did not object). Portals = portfolio, no shop yet. Music = later (layout designed; songs need restoring).

## Stage 4: tokens + full-page blueprint (blueprint/full.html, strips); awaiting owner check-in
frontend-design review changed A: one-colour headline (no single-phrase accent), sentence-case labels (no all-caps), no arrows on buttons, no middle-dot strings.
- Colour: ink #16110d (page), ink-2 #1f1812, line #33291f, paper #ece2cf (text), muted #b3a68e, brass #c9a24a / #e7c77d (the one accent), oxblood #9a3a2c (Leave only), glow #86ecd2 + night #07090a (the Workshop only).
- Type: Instrument Serif (display, h1 clamp 48-108px, h2 40-72, h3 24-32), Public Sans (body 17px/1.6, small 15). Fraunces retired (detector: overused).
- Space: 8px grid (8,16,24,32,48,64,96,128); sections 128px desktop / 96px phone.
- Motion plan: hero book turns with scroll and swaps cover on each situation answer (the one orchestrated moment); covers lift 6px on press; the Portals day/dark slider follows the finger; nothing else moves on its own. Reduced motion: the book holds still, the slider still works.
- Page length: 10.7 phone screens (was 39.6), 8.3 desktop. Overflow 0.
- Detector: dark-glow kept only where it is literal (strontium line, slider handle); the decorative glow was removed.

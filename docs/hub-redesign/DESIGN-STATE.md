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

## Stage 5: built (2026-11-21), NOT deployed
Sources: design/hub-v18/{data.json,home.css,home.js,img/}; builder scripts/seo/build_home.py (replaces build_hub.py); GSAP 3.13.0 vendored in tools/vendor and inlined. Output 165 KB HTML; covers/Portals as WebP in hub/media/v18; fonts subset in hub/f.
Owner changes applied: NFC guide before Press/Casting; Press/Casting use drawn seal/casting icons (no pendant photos).
Audits run, with what each changed:
- design-gates (5 profiles): figure/text overlap (pendant labels) moved to a legend; 8 radii down to 4; type sizes onto one scale; footer targets 44px; glow-line start contrast raised. Final: 0 FAIL; motion p95 16.7ms, 0 dropped frames at 4x CPU throttle.
- find-animation-opportunities: press feedback on covers/picks/tools/Leave/Menu; ribbon made scroll-linked (was an endless loop, WCAG 2.2.2); book float limited to under 5s; one-time Portals slider hint; door spines tip back. Rejected: nav pill animation (frequent), cover fade-in on load, counter tick-up, cursor-tilt on covers, parallax text.
- axe WCAG 2.2 AA: hero text fade removed (failed contrast mid-fade). Final: clean dark + light.
- keyboard: found the hidden phone menu was focusable (fixed); every control shows a focus ring; Esc closes the menu; Esc twice = Leave.
- perf (local): LCP 0.5s, CLS 0.003, 156 KB first load.
- Impeccable detector: Instrument Serif "overused" kept (owner chose A by picture); the strontium glow kept (literal glow).
- verify-hub.mjs rewritten for v18: all checks pass at 375 and 1440. REGRESSIONS.md lists the guards.
Open: music songs (owner: later); the live counter needs the deploy (CF_API_TOKEN already set in Netlify by the owner).
- Critic round 1: 3 scores under 4 (composition, phone ergonomics, finish). All fixed. Round 2: all ten at 4, none under 4 (critic-round1.md, critic-round2.md). Round-2 refinements applied (door spines, answer panel layout, phone shelf edge fade, NFC 40/60). Final: verify-hub all pass; design-gates 0 FAIL.
- Owner picked Gloock (2026-11-21) as the display face (OFL, self-hosted, 15 KB subset). Instrument Serif retired. Gloock has no italic, so italics became upright (font-synthesis:none). h1 resized for its width; question fits the first screen at 1440x900, 1366x768, 1280x720, 390x844 and 375x667.

## Push-to-5 round (2026-11-21), owner: "use all of the not yet used things"
Used this round: Adobe font_recommend + suggest_type_palettes (Adobe Fonts can't be self-hosted, so used as a brief; OFL candidates IM Fell, Bodoni Moda, Gloock rendered on the real page, owner to pick); emil-design-eng + apple-design (stronger curves, interruptible motion, press-on-pointerdown, scroll-edge header, reduced transparency/contrast, display tracking); Figma (file "Noble Father Creations: homepage v18" in the owner's drafts via html_to_figma); signature: strontium charge-and-glow Portals (replaces the slider) and an opening hero book with light sheen; paper grain.
Review batch 1 (impeccable polish/typeset/bolder/delight/overdrive/audit, taste-skill, refactoring-ui, web-design-guidelines): 4 must + 8 nice, all applied (review-batch1.md).
Review batch 2 (review-animations, improve-animations, gsap-scrolltrigger/performance/core/timeline, ux-heuristics, cognitive-design, better-accessibility, web-accessibility, webapp-testing): 9 must + 6 nice, all applied (review-batch2.md). Motion layers rebuilt (book-in / book-tilt / book3d / face / leaf). Verified: no book jump, no shelf blink, the turn is seen before the scroll, Just looking lands on the library, Esc-twice leaves.
Gates after both batches: verify-hub all pass; design-gates 0 FAIL, p95 16.7 ms, 0 drops; axe clean.
Not used, on purpose: Artlist hero art/video (credits; no need found: the real covers and pendant photos carry the page); higgsfield (not connected).

## Final (2026-11-21): all 11 critic areas at 5, NOT deployed
Fresh independent critic, 4 rounds: R1 seven 4s and four 3s; R2 six 5s; R3 nine 5s; R4 eleven 5s. Applied: solid header; the answer card opens under the answers and the page moves only enough to show the first pick (176/321/336 px at 1440x900/1280x720/390x844; instant under reduced motion, agreed by the critic); bold staggered entrance (masked line rise, book drop, settle tilt); drifting title strip; alternating shelves; brighter muted text; an honest music line; 44px skip and licence targets; stacked answer picks; a sticky desktop book; an honest glow line. Declined with reasons and agreed by the critic: recolouring the real blue pendant glow, replacing the NFC guide's real cover, a bigger phone book.
Gates: verify-hub all pass; design-gates 0 FAIL; axe clean; perf LCP 0.54s, CLS 0.
To deploy (owner's words "deploy the homepage"): build with sites.json hub.buildCommand, then a folder with hub/catalogue-redesign.html as index.html + catalogue-redesign._redirects as _redirects + robots.txt, sitemap.xml, llms.txt, og.png, the IndexNow key, topics.html, media/ (incl. media/v18), f/, netlify.toml, netlify/functions/visits.mjs; Netlify MCP deploy-site with hub.netlifySiteId; then node scripts/verify-deployed.mjs hub and check /api/visits returns a number.

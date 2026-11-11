# Fractal² intro v6: audit record (2026-11-11). NOT deployed.

Source: `design/fractal2/redesign/v6/` (`python3 build.py [BASE]` -> `index.html`; for the live copy use BASE `/fractal2/_a/v6/` and copy `img/`, `fonts/`, `emblem-64.png`, `favicon.ico` there). Text: `content/fractal2/intro-story.md`, unchanged.

## What it is
One fixed full-screen camera over vector art drawn by `design/fractal2/logo.py` (30-technique original; 335-tactic map behind it at 3.2x, so the pull-back reveals it continuously). Four text-free scroll beats, damped camera, 2,700-point canvas field (30 x 90), 30-sector atlas ending, gold pulse on the return. Phone and landscape get their own layouts; phones get 2048 px images.

## Checks run
- Design gates (5 profiles incl. reduced motion): 0 FAIL. Warnings: software-rendered frame time under 4x throttle; gate's short settle time on "determinism" (settled positions measured identical: diff 0.0 to 0.003).
- Devices (screenshots): 375x667, 390x844, 430x932, 844x390 landscape, 768x1024, 1280x720, 1440x900, 1920x1080. No horizontal overflow, no console errors. 320 px width and 200% text: no overflow.
- No JavaScript: text readable, stage hidden. Reduced motion: beats shrink to 24svh, camera and parallax stop.
- Structure: one h1, h2 per part, skip link target exists, 0 images without alt, canvas aria-hidden, Leave button labelled, first Tab stop is the skip link.
- Load (slow 4G emulation): text paints at once; 0.9 MB (phone) / 1.3 MB (desktop) before the late-loaded outer-ring image; hero shows a soft glow until the art arrives.
- Two independent critic passes (fresh agent, screenshots only). Pass 1: crispness 4, continuity 3, legibility 4/3, pacing 3, polish 4, originality 3, phone 3. Pass 2 (after fixes): crispness 4, continuity 4, legibility 3.5 desktop / 3 phone, pacing 3.5, polish 3.5, originality 4, phone 3. Fixes after pass 2 (atlas label, phone hero, footer gradient, larger rest zoom, brighter dots) have NOT been re-scored.
- Skills: design-director process, design gates, critics. The impeccable, apple-design and emil sub-skills were NOT run.

## Known gaps / owner decisions
- Not a real-phone test (no device); Safari behaviour of a fixed canvas plus three large images is untested.
- "The room again" differs from the opening by glow and a pulse only; making it mean more needs new copy (owner's call).
- Hook finding on Fraunces awaits owner confirmation. Live site still shows v5 (deploy 6af479b2...).

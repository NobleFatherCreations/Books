# Design ideas parked for later (logged 2026-10-04)

Owner request: log these, explore after the content/PDF work is finished and the design pass resumes.

## Inspiration sites (for design ideas)
- Savee.com
- Landdddding.com (spelled with extra d's in the owner's screenshot)
- Motionin.design

(Screenshot: `inspiration-sites.jpg`)

## HyperFrames skills (installed globally 2026-10-04)
- Command run: `npx skills add heygen-com/hyperframes --full-depth -g -a claude-code -s '*' -y` with `DISABLE_TELEMETRY=1 DO_NOT_TRACK=1`.
- Source: github.com/heygen-com/hyperframes (Apache 2.0), installed through the `skills` CLI (vercel-labs/skills). It copies 30 skill folders into `~/.claude/skills/` (hyperframes, hyperframes-core/cli/animation/audio/creative/keyframes/registry/studio, slideshow, talking-head-recut, embedded-captions, faceless-explainer, general-video, media-use, motion-graphics, music-to-video, pr-to-video, product-launch-video, remotion-to-hyperframes, plus block skills such as canopy-part-title, code-slice-hero, cuboid-carousel, frost-sequence-camera-orbit, glass-shard-title, orbit-card, wireframe-portal-title). Inspected first: no hooks, no daemons, no install scripts; the CLI has an install-telemetry event, which we disabled. Rendering needs Node 22+ and FFmpeg (Node 22 is present; FFmpeg ships with Playwright at /opt/pw-browsers/ffmpeg-1011).
- Skills run with full agent permissions: review one before using it.

## The example the owner showed (two screenshots)
A TikTok ("Your Chief AI Officer") shows asking Claude (Opus 5.5) to storyboard a 12-second motion piece, then having the HyperFrames skill render it:
- A beat sheet by time range (0.0–2.8, 2.8–6.4, 6.4–9.6, 9.6–12.0 s) with columns HUD / On screen / What moves / Seam out. Beats: the trick, how it works, your job, the model.
- Concept: "Opus 5.5 doesn't make videos. It makes flipbooks." One HTML file; real GSAP line types itself; a playhead sweeps a film strip of real proof frames; a 6x4 contact sheet with a flagged frame swapped for a fixed one; the grid folds back into the flipbook. Rendered 13.5 s video in 13.3 s on an M3 Pro. The skill "isn't prompting. It's taste + review."
- Screenshots: `flipbook-example-1-playback.png`, `flipbook-example-2-beat-sheet.png`.
- Idea to explore: use the same storyboard-then-render workflow for the Sacred Divide (animated section openers, the 30-technique cycle, loop diagrams, promo clips), and the three sites above for the PDF/site/TikTok design pass.

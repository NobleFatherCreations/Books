# The Weighing: design state

## Before design (2026-11-24, interim skin = v4 brass on dark, built by scripts/seo/build_scale_v2.py)
- Pipeline (bash scripts/scale-pipeline.sh): source checks, manifest, findability (70 pages), on-page, Decoder links, seal menu, screenshots (375/1440, reduced motion): all pass.
- Fixed: sister-book bridge links didn't wrap (nowrap inherited from Long After); printable blank lines (____) overflowed phones.
- perf.js: /scale LCP 2.4s (cover image), CLS 0.043; the-gradient CLS 0.055; **when-weighing-stops CLS 0.3 (fix in design: likely font swap or the dock)**.
- axe accessibility scan NOT run (axe-core not installed; package installs are off in this session). Run before release.
- New blocks needing real design: handle, scene (label "Made up, but you've met these people."), try, warn/warn danger, tree, sort (tap to reveal), myth, script, check, compare, gradient, bridge, sheet, aside, pull.

## Design inputs from the skill audit (2026-11-24, docs/AUDIT-WEIGHING-2026-11-24.md)
- **Layout shift is the font swap, not the dock.** With the fallback font the text starts 31px (cover) to 39px (chapters) higher; Fraunces arrives and pushes it down. Only the 400 weight is preloaded but headings use 600/700, and six font files load (about 420KB). Fix in design: two fonts, preload the weights used above the fold, and a size-adjusted fallback (or font-display: optional for the display face). Re-check with perf.js (slow 4G, 4x CPU).
- **Cover LCP 2.5s:** cover.webp is 96KB at 720px. Add a phone-sized variant (srcset) when the cover is restyled.
- **Focus hidden under the dock (WCAG 2.4.11):** on phones about 9 focus stops per chapter land under the fixed bottom dock and Leave button. Add `scroll-padding-bottom` equal to the dock height (and top for the header).
- **Header plus dock take about 17% of a phone screen** for the whole read. Consider letting the header hide on scroll down (Leave stays reachable in the dock).
- **Recall sorts are long:** 16 sorts have 7 to 15 items, past what a stressed reader holds. Show them in batches of 4 or 5 ("show more") instead of one long list. No text change.
- **Breadcrumbs exist only in structured data.** The "Movement IV ..., chapter 12 of 14" line already orients readers; keep it visible in every design.
- **Already fixed in the builder (keep when restyling):** table scroll boxes are keyboard-reachable regions with numbered labels, no empty header cells, FAQ "Read more" links are named after their question.
- **Words frozen:** snapshot at design/scale-v5/text-before.json (not committed; rebuild it from the audit commit with `python3 scripts/book/text-diff.py snap library/scale design/scale-v5/text-before.json`). After design, `text-diff.py check` must show only new UI strings.

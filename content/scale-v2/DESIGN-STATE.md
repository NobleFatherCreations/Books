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

## R1 (2026-11-24): gates on cover, the-gradient, field-card, when-weighing-stops x phone-dark, phone-reduced, desktop-dark
All four PASS (0 failing checks). Contact sheets in design/scale-v5/r1/<page>/<profile>/contact.jpg (per-frame shots git-ignored). Gate warnings: 4 font families (Fraunces, ui-monospace, Georgia, system-ui; rule max 2), 12-16 text colours (aim 6), 6 cover screens over 70% empty.

Faults read from the phone sheets (F-numbers from docs/design-catalogue/07-choosing-and-combining.md):
- **Bug, fixed:** all 57 `::: bridge` blocks printed their link data ("longafter:if-youre-not-safe-right-now") as a visible label, including twice in "Help, now" on the crisis page. The builder now keeps it as `data-to` only; text-diff confirms nothing else changed. Snapshot retaken after the fix.
- **Cover, F5 + F8:** the cover image is a small thumbnail (about a third of the phone width), so there's no title moment; then about 11 phone screens of identical contents rows with only a small brass label per movement. Needs a real cover moment and movements as visual chapters (collapsible or card-grouped).
- **Cover (corrected 2026-11-24):** the crisis notice appears once (`p.safe`); in the R1 sheet it straddled two overlapping frames, which read as a duplicate. No change needed.
- **F4:** brass on navy is The Long After's interim skin recoloured, not a Weighing concept.
- **The gradient, F5:** the book's central idea (seven positions, rude to abusive) renders as a plain bullet list, twice. It's the strongest candidate for the signature move (a dial or scale that holds still, readable in reduced motion and print).
- **Field card, F5:** promises "one page, screenshot it, print it", but is about 11 phone screens of 59 underlined numbered links. Needs a compact screenshot and print form (two columns on paper, grouped by movement, links not underlined).
- **Recall sorts:** render as a long "▸" list (see the cognitive-design note above: batch them).
- **Crisis page:** reads calmly and the five conditions come first, which is right (F13 avoided). The emergency instruction is body text inside the short-answer box; consider one clear "Find help where you live" action near the top. No humour, no effects; keep it that way.
- **F14:** 5 radii and 5 shadow styles on the cover; tokenise in the build.

Next: R2 (concept sentence and budget), then three comps for the owner to pick by picture.

## R2 (2026-11-24): concept and budget
- **Concept:** an instrument you can trust at 2am: quiet, exact and blunt, with one moving part (the gradient).
- **Budget:** one lead style per comp; one signature move (the seven-step gradient as a drawn scale, reused wherever a case is placed); two type families; one accent per movement on a calm dark ground; at most 3 effects per screen; reduced motion designed (the scale stands still, nothing self-runs); print and screenshot forms for the kit.
- **Three directions for the owner to pick by picture** (catalogue IDs, docs/design-catalogue/01):
  - **A "The Instrument":** S-34 technical/data-sheet (ticks, callouts, measurement) + S-53 single-hue. The gradient is a calibrated scale; tool cards read like instrument labels.
  - **B "Plain Speech":** S-44 gov-grade plain + S-46 big-sans. Maximum clarity at 2am, oversized blunt headings (the deadpan voice in type), tool cards as hard-edged signs.
  - **C "The Ledger":** S-49 receipt/label/ticket + S-45 modern serif. The book's own receipts, price list and logbook become the visual language; tool cards are tags, the kit is a receipt.
- Comps are built on the v5.1 pilot chapters (01-i-b) so the owner sees the new tool and ask blocks, the new cases and the new voice in one review. Faults from R1 that every comp must fix: the cover moment, movement cards instead of the 11-screen list, the gradient drawn rather than bulleted, one crisis notice, the kit as one screen or one page, batched sorts, 2 fonts.

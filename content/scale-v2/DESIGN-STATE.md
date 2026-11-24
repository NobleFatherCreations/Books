# The Weighing: design state

## Before design (2026-11-24, interim skin = v4 brass on dark, built by scripts/seo/build_scale_v2.py)
- Pipeline (bash scripts/scale-pipeline.sh): source checks, manifest, findability (70 pages), on-page, Decoder links, seal menu, screenshots (375/1440, reduced motion): all pass.
- Fixed: sister-book bridge links didn't wrap (nowrap inherited from Long After); printable blank lines (____) overflowed phones.
- perf.js: /scale LCP 2.4s (cover image), CLS 0.043; the-gradient CLS 0.055; **when-weighing-stops CLS 0.3 (fix in design: likely font swap or the dock)**.
- axe accessibility scan NOT run (axe-core not installed; package installs are off in this session). Run before release.
- New blocks needing real design: handle, scene (label "Made up, but you've met these people."), try, warn/warn danger, tree, sort (tap to reveal), myth, script, check, compare, gradient, bridge, sheet, aside, pull.

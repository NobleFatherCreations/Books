#!/usr/bin/env bash
# The Weighing: one command, every check (the Long After pipeline, adapted). Built pages are NOT committed until release.
#   bash scripts/scale-pipeline.sh [--fast]
set -euo pipefail
cd "$(dirname "$0")/.."
FAST=0; [[ "${1:-}" == "--fast" ]] && FAST=1
OUT="${TMPDIR:-/tmp}/scale-pipeline"; mkdir -p "$OUT"
step() { printf '\n== %s\n' "$1"; }
step "1 source checks";   for f in content/scale-v2/0*.md; do python3 scripts/book/rewrite-check.py "$f" | tail -1 | grep -q " 0 problem" || { echo "rewrite-check: $f"; exit 1; }; done; echo "rewrite-check: all files clean"
step "1a reports (not a gate)"; for r in readability meso taxonomy; do python3 scripts/book/$r.py --book scale; done
step "2 build";           python3 scripts/seo/build_scale_v2.py
python3 scripts/nf-catalogue-sweep.py >/dev/null
python3 scripts/manifest-check.py --book scale || { echo "a page disagrees with site_manifest.json"; exit 1; }
step "3 beacon";          python3 scripts/visit-counter.py library/scale | tail -1
step "5 SEO";             python3 scripts/seo/verify_seo.py scale | tail -2
python3 scripts/seo/onpage_longafter.py scale | tail -1
python3 scripts/decoder-relink.py --check || { echo "book links point at old Decoder addresses: run python3 scripts/decoder-relink.py"; exit 1; }
step "6 seal menu";       python3 scripts/audit-seal-nav.py | tail -2
[[ $FAST == 1 ]] && { echo; echo "fast run complete (browser checks skipped)"; exit 0; }
step "7 browser checks"
if ! curl -fs -o /dev/null http://localhost:8765/scale; then
  python3 scripts/seo/serve.py >"$OUT/serve.log" 2>&1 & SERVER=$!; trap 'kill $SERVER 2>/dev/null' EXIT
  for _ in $(seq 20); do curl -fs -o /dev/null http://localhost:8765/scale && break; sleep 0.3; done
fi
B=http://localhost:8765/scale
PAGES="$B $B/this-book-in-the-wrong-hands $B/the-gradient $B/when-you-both-say-victim $B/when-weighing-stops $B/questions-people-ask $B/field-card $B/weighing-sheet $B/contents $B/search"
node scripts/seo/shoot.js "$OUT/shots" $PAGES | python3 -c '
import sys, json
bad = 0
for l in sys.stdin:
    try: d = json.loads(l)
    except ValueError: continue
    if d["overflow"] or d["stuck"] or d["errs"] or d["failed"]:
        bad += 1; print("  FAIL", d["url"], d["w"], d["rm"], d["errs"], d["failed"])
print("  screenshots:", "problems found" if bad else "no overflow, errors or stuck content")
sys.exit(1 if bad else 0)'
AXE_DIR="$(dirname "$(node -p "require.resolve('axe-core/package.json')" 2>/dev/null || true)")"
if [[ -z "$AXE_DIR" || "$AXE_DIR" == "." ]]; then (cd "$OUT" && npm i --silent --no-save axe-core >/dev/null 2>&1) || true; export NODE_PATH="$OUT/node_modules"; fi
if node -e "require('axe-core')" 2>/dev/null; then
  node scripts/seo/a11y.js $PAGES | tail -1 | tee "$OUT/a11y.txt"
  grep -q 'TOTAL {}' "$OUT/a11y.txt" || { echo "accessibility issues found"; exit 1; }
else echo "  axe-core not installed and package installs are off here: accessibility scan SKIPPED (run it where npm works)"; fi
node scripts/seo/perf.js $B $B/the-gradient $B/when-weighing-stops
echo; echo "pipeline complete. Screenshots: $OUT/shots. Restore the v4 copy with: git checkout -q library/scale && git clean -fdq library/scale"

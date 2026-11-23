#!/usr/bin/env bash
# The Long After: one command from edited Markdown to a checked build.
# Each stage feeds the next and the run stops at the first failure, so a later check never runs on a broken build.
#
#   bash scripts/longafter-pipeline.sh            content + build + SEO + browser checks
#   bash scripts/longafter-pipeline.sh --fast     content + build + SEO only (no browser)
#
# Stages
#   1 content    scripts/longafter-audit.py        voice, keywords, links, safety rules, readability (all 96 pages)
#   1a manifest  scripts/manifest-check.py         counts and titles agree with site_manifest.json; READABILITY/MESO/TAXONOMY reports
#   2 build      scripts/seo/build_longafter_v2.py  Markdown -> library/longafter (pages, search, sitemap)
#   3 beacon     scripts/visit-counter.py          Cloudflare beacon on every page (owner rule)
#   4 hub files  scripts/seo/build_site.py         llms.txt, topics, robots (homepage files only change on purpose)
#   5 SEO        verify_seo.py + onpage_longafter.py + validate_schema.py
#   6 seal menu  scripts/audit-seal-nav.py         every page lists all 21 books
#   7 browser    shoot.js (overflow, errors, reduced motion) + a11y.js (axe WCAG 2.2 AA) + perf.js (lab vitals)
# Nothing here deploys. Deploys happen only on the owner's words.
set -euo pipefail
cd "$(dirname "$0")/.."
FAST=0; [[ "${1:-}" == "--fast" ]] && FAST=1
OUT="${TMPDIR:-/tmp}/longafter-pipeline"; mkdir -p "$OUT"
step() { printf '\n== %s\n' "$1"; }

step "1 content audit";   python3 scripts/longafter-audit.py | tail -3
python3 scripts/longafter-audit.py | tail -1 | grep -q " 0 failing" || { echo "content audit failed"; exit 1; }
step "1a manifest";        python3 scripts/manifest-check.py --book longafter || { echo "a page disagrees with site_manifest.json"; exit 1; }
step "1a reports (not a gate)"; for r in readability meso taxonomy; do python3 scripts/book/$r.py --book longafter; done
step "1b AI-writing report (not a gate)"; python3 scripts/longafter-ai-audit.py 2>/dev/null | head -1 || true
python3 scripts/longafter-sources.py --no-lookup | tail -1
step "2 build";           python3 scripts/seo/build_longafter_v2.py
python3 scripts/nf-catalogue-sweep.py >/dev/null   # the menu borrowed from another book, brought to the one canonical catalogue
step "3 beacon";          python3 scripts/visit-counter.py library/longafter/*.html >/dev/null && echo "beacon checked"
step "4 hub files";       python3 scripts/seo/build_site.py | tail -2
git checkout -- hub/og.png 2>/dev/null || true   # build_site re-renders the share image; the homepage itself is built by build_home.py and must not be reverted here
step "5 SEO";             python3 scripts/seo/verify_seo.py longafter | tail -2
python3 scripts/seo/onpage_longafter.py | tail -1
python3 scripts/decoder-relink.py --check || { echo "book links point at old Decoder addresses: run python3 scripts/decoder-relink.py"; exit 1; }
SCHEMA="${SCHEMAORG:-$OUT/schemaorg.jsonld}"
if [[ ! -s "$SCHEMA" ]]; then curl -fsSL -o "$SCHEMA" https://schema.org/version/latest/schemaorg-current-https.jsonld || true; fi
if [[ -s "$SCHEMA" ]]; then python3 scripts/seo/validate_schema.py "$SCHEMA" | tail -1; else echo "schema vocabulary not reachable: schema check skipped"; fi
step "6 seal menu";       python3 scripts/audit-seal-nav.py | tail -2
[[ $FAST == 1 ]] && { echo; echo "fast run complete (browser checks skipped)"; exit 0; }

step "7 browser checks"
if ! curl -fs -o /dev/null http://localhost:8765/longafter; then
  python3 scripts/seo/serve.py >"$OUT/serve.log" 2>&1 & SERVER=$!; trap 'kill $SERVER 2>/dev/null' EXIT
  for _ in $(seq 20); do curl -fs -o /dev/null http://localhost:8765/longafter && break; sleep 0.3; done
fi
B=http://localhost:8765/longafter
PAGES="$B $B/if-youre-not-safe-right-now $B/the-trauma-bond $B/if-you-go-back $B/questions-people-ask $B/contents $B/search"
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
if [[ -z "$AXE_DIR" || "$AXE_DIR" == "." ]]; then (cd "$OUT" && npm i --silent --no-save axe-core >/dev/null 2>&1) ; export NODE_PATH="$OUT/node_modules"; fi
node scripts/seo/a11y.js $PAGES | tail -1 | tee "$OUT/a11y.txt"
grep -q 'TOTAL {}' "$OUT/a11y.txt" || { echo "accessibility issues found"; exit 1; }
node scripts/seo/perf.js $B $B/the-trauma-bond $B/if-youre-not-safe-right-now
echo; echo "pipeline complete: content, build, SEO, seal menu, screenshots, accessibility and speed all checked. Screenshots: $OUT/shots"

#!/usr/bin/env bash
# Run impeccable's deterministic detector across every audit view and emit a
# summary table. Mechanical, no LLM, no API key — cheap to re-run any time.
#
# Usage: design/run-detector.sh [audit-view-dir]
# Run design/prep-audit.py first to generate the views.
set -uo pipefail
DIR="${1:-.audit-view}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DET="$ROOT/.claude/skills/impeccable/scripts/detect.mjs"

[ -d "$DIR" ] || { echo "no audit views at $DIR — run design/prep-audit.py first" >&2; exit 1; }

printf "%-32s %-6s %s\n" "PAGE" "COUNT" "BREAKDOWN"
total=0
for f in "$DIR"/*.html; do
  n=$(basename "$f" .html)
  res=$(timeout 180 node "$DET" "$f" 2>&1)
  count=$(echo "$res" | grep -oE "^[0-9]+ anti-patterns found" | grep -oE "^[0-9]+")
  if [ -z "$count" ]; then count="ERR"; else total=$((total + count)); fi
  tags=$(echo "$res" | grep -oE "\[[a-z-]+\]" | sort | uniq -c | sort -rn | tr '\n' ' ' | tr -s ' ')
  printf "%-32s %-6s %s\n" "$n" "$count" "$tags"
done
echo
echo "TOTAL RAW FINDINGS: $total"
echo "NOTE: filter known-deliberate tags before acting — see ENHANCEMENT-PLAN.md."
echo "  [overused-font] Fraunces = pinned brand face, intended"
echo "  [em-dash-overuse] = the author's voice, intended"
echo "  [gradient-text] = the gold-leaf gilt identity, intended"
echo "  [dark-glow] candle/lamp glows = literal light sources in the world, intended"

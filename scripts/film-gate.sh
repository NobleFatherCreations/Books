#!/bin/sh
# FILM GATE: the one command that decides whether a scroll film may be shown to the owner or deployed.
#   scripts/film-gate.sh <url> [click-selector] [script.md]        -> exit 0 only if everything passes
#   scripts/film-gate.sh <url> '#begin' content/x/script.md -- <deploy command ...>   -> runs the deploy command ONLY after a pass
# Runs: story lint (if a script is given), film-check on phone, phone with reduced motion, and desktop, then writes contact sheets to read.
# Sheets land in $FILM_OUT (default ./.film-gate). READ THEM: the gate proves the mechanics, not the beauty.
URL="$1"; CLICK="${2:-}"; SCRIPT="${3:-}"; OUT="${FILM_OUT:-.film-gate}"; HERE="$(cd "$(dirname "$0")" && pwd)"
[ -z "$URL" ] && { echo "usage: film-gate.sh <url> [click] [script.md] [-- deploy command]"; exit 2; }
shift; [ $# -gt 0 ] && [ "$1" != "--" ] && shift; [ $# -gt 0 ] && [ "$1" != "--" ] && shift; [ "$1" = "--" ] && shift
C=""; [ -n "$CLICK" ] && C="--click=$CLICK"; FAIL=0
if [ -n "$SCRIPT" ] && [ "$SCRIPT" != "--" ]; then node "$HERE/story-lint.mjs" "$SCRIPT" | tail -1 | grep -q "PASS" && echo "PASS  story lint" || { echo "FAIL  story lint"; FAIL=1; }; fi
for P in "--vp=390x844" "--vp=390x844 --rm" "--vp=1440x900 --speed=30"; do
  node "$HERE/film-check.mjs" "$URL" $C $P > "$OUT.tmp" 2>&1 || FAIL=1; grep -v "^PASS" "$OUT.tmp"; done; rm -f "$OUT.tmp"
node "$HERE/frame-walk.mjs" "$URL" "$OUT/phone" --n=96 $C --settle=550 >/dev/null 2>&1 && echo "sheets: $OUT/phone/sheet-*.jpg (read them)"
if [ $FAIL -ne 0 ]; then echo "FILM GATE FAIL: fix and rerun. Nothing was deployed."; exit 1; fi
echo "FILM GATE PASS"
if [ $# -gt 0 ]; then echo "running: $1 ..."; "$@"; fi

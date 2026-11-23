#!/usr/bin/env bash
# Verify a writing-pass rewrite of one file and commit it.
#   bash scripts/book/accept-pass.sh 02-ii ii "summary" [book]      (book defaults to longafter)
# Runs rewrite-check against HEAD, then the book's content audit if book.json names one ("audit": "<command> {part}"),
# refuses if any other tracked file changed, then commits and pushes.
set -euo pipefail
cd "$(dirname "$0")/../.."
BOOK=${4:-longafter}
D=content/$BOOK-v2
F=$D/$1.md
python3 scripts/book/rewrite-check.py "$F" | tail -1
AUDIT=$(python3 -c "import json,sys;print(json.load(open('$D/book.json')).get('audit',''))")
[[ -z "$AUDIT" && "$BOOK" == longafter ]] && AUDIT="python3 scripts/longafter-audit.py {part}"
if [[ -n "$AUDIT" ]]; then
  ${AUDIT//\{part\}/$2} | tail -1 | grep -q " 0 failing" || { echo "audit failing"; exit 1; }
fi
git checkout -q "$D/AI-AUDIT.md" "$D/AI-AUDIT.json" 2>/dev/null || true
[[ -z "$(git status --short | grep -v "$F" | grep -v '^??')" ]] || { echo "other files changed:"; git status --short; exit 1; }
TITLE=$(python3 -c "import json;print(json.load(open('$D/book.json')).get('title','$BOOK'))")
git add "$F" && git commit -qm "$TITLE writing pass: $3

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_013rW7RC1Kr6aUmdeRwP2FgS"
for i in 1 2 3 4; do git push -q origin HEAD 2>/dev/null && break || sleep $((2**i)); done
git log --oneline -1

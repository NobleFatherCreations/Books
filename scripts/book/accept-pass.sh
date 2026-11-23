#!/usr/bin/env bash
# Verify a step 2 rewrite of one file and commit it.  bash scripts/book/accept-pass.sh 02-ii ii "summary"
set -euo pipefail
cd "$(dirname "$0")/../.."
F=content/longafter-v2/$1.md
python3 scripts/book/rewrite-check.py "$F" | tail -1
python3 scripts/longafter-audit.py "$2" | tail -1 | grep -q " 0 failing" || { echo "audit failing"; exit 1; }
git checkout -q content/longafter-v2/AI-AUDIT.md content/longafter-v2/AI-AUDIT.json 2>/dev/null || true
[[ -z "$(git status --short | grep -v "$F" | grep -v '^??')" ]] || { echo "other files changed:"; git status --short; exit 1; }
git add "$F" && git commit -qm "Long After v6 step 2: $3

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_013rW7RAwkFpGQfHy4oSeC93"
for i in 1 2 3 4; do git push -q origin HEAD 2>/dev/null && break || sleep $((2**i)); done
git log --oneline -1

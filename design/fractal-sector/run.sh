#!/usr/bin/env bash
# One command per sector: import + audit, build, social cards, verify.
#   design/fractal-sector/run.sh ent [preview|production]
set -euo pipefail
cd "$(dirname "$0")/../.."
S="${1:-ent}"; T="${2:-preview}"
python3 design/fractal-sector/ingest.py "$S"
python3 design/fractal-sector/build.py "$S" --target "$T"
node design/fractal-sector/og.mjs "$S"
node design/fractal-sector/verify.mjs "$S"

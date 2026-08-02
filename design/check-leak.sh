#!/usr/bin/env bash
# Deploy-hygiene check: run before publishing any page.
# Greps for the build-instructions leak pattern and any stray/unclosed
# comment markers. Exit code 1 = leak found, do not ship.
set -euo pipefail
found=0
for f in "$@"; do
  if grep -qa "set data-here on the button\|#REPLACE\|THE HOUSE TAB" "$f"; then
    echo "LEAK: $f"
    found=1
  fi
done
if [ "$found" -eq 0 ]; then
  echo "clean: no leak markers in $# file(s)"
fi
exit $found

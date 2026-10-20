#!/usr/bin/env bash
# Run all solution test harnesses.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ok=0
fail=0
for sol in "$ROOT"/solutions/*; do
  [[ -d "$sol" ]] || continue
  slug="$(basename "$sol")"
  if (cd "$sol" && bash ./test.sh >/dev/null 2>&1); then
    echo "OK  $slug"
    ok=$((ok + 1))
  else
    echo "FAIL $slug"
    (cd "$sol" && bash ./test.sh) || true
    fail=$((fail + 1))
  fi
done
echo "Passed $ok; failed $fail"
[[ "$fail" -eq 0 ]]

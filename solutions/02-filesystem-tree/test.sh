#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

pass=0
fail=0
assert_eq() {
  local got=$1 want=$2 msg=${3:-}
  if [[ "$got" == "$want" ]]; then
    pass=$((pass + 1))
  else
    echo "FAIL ${msg}: got='$got' want='$want'" >&2
    fail=$((fail + 1))
  fi
}
assert_contains() {
  local hay=$1 needle=$2 msg=${3:-}
  if [[ "$hay" == *"$needle"* ]]; then
    pass=$((pass + 1))
  else
    echo "FAIL ${msg}: missing '$needle' in '$hay'" >&2
    fail=$((fail + 1))
  fi
}
assert_file() {
  if [[ -f "$1" ]]; then pass=$((pass+1)); else echo "FAIL missing file $1" >&2; fail=$((fail+1)); fi
}

# shellcheck disable=SC1091
source "$ROOT/solution.sh"

run_tests() {
  assert_eq "$(abs_join /home/ada docs/a)" "/home/ada/docs/a" join
  assert_eq "$(abs_join /home/ada/ docs/a)" "/home/ada/docs/a" join2
  assert_eq "$(basename_of /home/ada/docs)" "docs" base
}

run_tests

echo "Passed $pass failed $fail"
[[ "$fail" -eq 0 ]]

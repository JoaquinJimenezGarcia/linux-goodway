#!/usr/bin/env bash
safe_dir_or_die() {
  local d=${1:-}
  # TODO: return 1 if empty else echo d
  echo "$d"
}
assert_nonempty() {
  # TODO: return 1 if empty
  return 0
}

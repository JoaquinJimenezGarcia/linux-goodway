#!/usr/bin/env bash
safe_dir_or_die() {
  local d=${1:-}
  [[ -n "$d" ]] || return 1
  echo "$d"
}
assert_nonempty() {
  [[ -n "${1:-}" ]] || return 1
  return 0
}

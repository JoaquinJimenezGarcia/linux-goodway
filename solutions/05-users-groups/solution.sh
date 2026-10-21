#!/usr/bin/env bash
parse_uid() {
  [[ "$1" =~ uid=([0-9]+) ]] && echo "${BASH_REMATCH[1]}"
}
parse_user() {
  # Prefer a variable so ) in the class does not confuse [[ =~ ]]
  local re='uid=[0-9]+[(]([^)]+)[)]'
  [[ "$1" =~ $re ]] && echo "${BASH_REMATCH[1]}"
}

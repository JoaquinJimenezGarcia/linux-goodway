#!/usr/bin/env bash
parse_uid() {
  [[ "$1" =~ uid=([0-9]+) ]] && echo "${BASH_REMATCH[1]}"
}

#!/usr/bin/env bash
abs_join() {
  local root=${1%/}
  local rel=${2#/}
  echo "$root/$rel"
}
basename_of() {
  local p=${1%/}
  echo "${p##*/}"
}

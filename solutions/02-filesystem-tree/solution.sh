#!/usr/bin/env bash
abs_join() {
  local root=${1%/}
  local rel=${2#/}
  echo "$root/$rel"
}

#!/usr/bin/env bash
require_one_arg() {
  [[ $# -ge 1 ]] || return 2
  echo ok
}
arg_count() { echo $#; }

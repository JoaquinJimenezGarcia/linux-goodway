#!/usr/bin/env bash
digit() {
  case "$1" in
    7) echo rwx ;; 6) echo rw- ;; 5) echo r-x ;; 4) echo r-- ;;
    3) echo -wx ;; 2) echo -w- ;; 1) echo --x ;; 0) echo --- ;;
  esac
}
octal_to_human() {
  local o=$1
  echo "$(digit ${o:0:1})$(digit ${o:1:1})$(digit ${o:2:1})"
}

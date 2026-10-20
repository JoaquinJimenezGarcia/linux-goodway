#!/usr/bin/env bash
signal_num() {
  case "$1" in TERM) echo 15 ;; KILL) echo 9 ;; *) echo 0 ;; esac
}

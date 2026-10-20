#!/usr/bin/env bash
link_kind() {
  case "$1" in
    soft) echo symbolic ;;
    hard) echo hard ;;
    *) echo unknown ;;
  esac
}

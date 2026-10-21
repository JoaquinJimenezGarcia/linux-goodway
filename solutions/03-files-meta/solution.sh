#!/usr/bin/env bash
link_kind() {
  case "$1" in
    soft) echo symbolic ;;
    hard) echo hard ;;
    *) echo unknown ;;
  esac
}
same_inode_possible() {
  case "$1" in hard) echo yes ;; soft) echo no ;; *) echo unknown ;; esac
}

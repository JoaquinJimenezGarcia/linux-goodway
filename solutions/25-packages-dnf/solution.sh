#!/usr/bin/env bash
map_install_cmd() {
  case "$1" in debian|ubuntu) echo apt ;; rhel|fedora) echo dnf ;; alpine) echo apk ;; *) echo unknown ;; esac
}
map_query_cmd() {
  case "$1" in debian|ubuntu) echo apt ;; rhel|fedora) echo rpm ;; *) echo unknown ;; esac
}

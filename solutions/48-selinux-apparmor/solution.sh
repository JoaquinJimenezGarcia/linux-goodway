#!/usr/bin/env bash
mac_for_distro() {
  case "$1" in rhel|fedora|centos) echo selinux ;; ubuntu) echo apparmor ;; *) echo unknown ;; esac
}
mac_enforcing_word() { echo enforcing; }

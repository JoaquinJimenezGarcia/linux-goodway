#!/usr/bin/env bash
higher_nice_means() { echo "lower-priority"; }
# Use printf: echo "-n" is treated as echo's -n flag
ulimit_nofile_flag() { printf '%s
' '-n'; }

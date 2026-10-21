#!/usr/bin/env bash
load_busy() {
  local cpus=$1 load=$2
  awk -v c="$cpus" -v l="$load" 'BEGIN{print (l>c)?"yes":"no"}'
}
load_idle() {
  local cpus=$1 load=$2
  awk -v c="$cpus" -v l="$load" 'BEGIN{print (l<c)?"yes":"no"}'
}

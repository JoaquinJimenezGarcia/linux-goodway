#!/usr/bin/env bash
hello() {
  local name=${1:-world}
  echo "Hello, $name"
}
shout() { echo "HELLO, $1"; }

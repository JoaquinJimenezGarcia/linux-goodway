#!/usr/bin/env bash
match_todo() {
  if [[ "$1" == *TODO* ]]; then echo yes; else echo no; fi
}
match_fixme() {
  if [[ "$1" == *FIXME* ]]; then echo yes; else echo no; fi
}

#!/usr/bin/env bash
success_code() { echo 0; }
failure_code() { echo 1; }
is_success() { [[ "$1" == "0" ]] && echo yes || echo no; }

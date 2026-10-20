#!/usr/bin/env bash
count_lines() {
  wc -l | awk '{print $1}'
}

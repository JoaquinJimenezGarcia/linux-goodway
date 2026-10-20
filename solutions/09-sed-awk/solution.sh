#!/usr/bin/env bash
sum_field2() {
  awk '{s+=$2} END{print s+0}'
}

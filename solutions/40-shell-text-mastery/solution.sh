#!/usr/bin/env bash
top_token() {
  sort | uniq -c | sort -nr | awk 'NR==1{print $2}'
}

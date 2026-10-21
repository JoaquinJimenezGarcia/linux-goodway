#!/usr/bin/env bash
count_lines() { wc -l | awk '{print $1}'; }
count_words() { wc -w | awk '{print $1}'; }

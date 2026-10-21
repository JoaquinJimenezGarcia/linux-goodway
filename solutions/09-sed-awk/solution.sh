#!/usr/bin/env bash
sum_field2() { awk '{s+=$2} END{print s+0}'; }
max_field2() { awk 'BEGIN{m=0} {if($2>m)m=$2} END{print m+0}'; }

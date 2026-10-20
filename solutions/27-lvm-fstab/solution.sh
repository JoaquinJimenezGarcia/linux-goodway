#!/usr/bin/env bash
fstab_field_uuid() { awk '{print $1}' <<<"$1"; }

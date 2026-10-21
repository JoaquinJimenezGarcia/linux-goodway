#!/usr/bin/env bash
fstab_field_uuid() { awk '{print $1}' <<<"$1"; }
fstab_mountpoint() { awk '{print $2}' <<<"$1"; }

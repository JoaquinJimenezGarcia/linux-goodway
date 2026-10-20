---
title: "27. LVM Intro and /etc/fstab"
---

# 27. LVM Intro and /etc/fstab

**Phase:** Phase 8 — Packages, disks, storage  
**Estimated time:** 1–2 days  
**Slug:** `27-lvm-fstab`

## Learning objectives

- Explain PV/VG/LV mentally
- Read fstab entries
- Add mounts safely with backups
- Use UUIDs over volatile device names

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

## LVM idea

Physical volumes → volume group → logical volumes (flexible resizing).

## fstab

```bash
UUID=...  /data  ext4  defaults  0  2
```

Always backup fstab before edits. Wrong fstab can fail boot — have rescue plan (VM snapshot).

## Common mistakes

- Using /dev/sdX names that reorder on reboot
- Editing fstab without reboot test in VM
- Shrinking filesystems without backups

## Exercises

Work in `exercises/27-lvm-fstab/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/27-lvm-fstab/` until you have an honest failing attempt.**

## Self-check

1. Why UUID in fstab?
2. PV vs LV?
3. How recover bad fstab?

## Further reading

- https://man7.org/linux/man-pages/man5/fstab.5.html

---
title: "26. Disks, Partitions, Filesystems, mount"
---

# 26. Disks, Partitions, Filesystems, mount

**Phase:** Phase 8 — Packages, disks, storage  
**Estimated time:** 2 days  
**Slug:** `26-disks-fs`

## Learning objectives

- List block devices
- Understand partitions vs filesystems
- Mount/umount carefully
- Check free space and inodes

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

```bash
lsblk
sudo fdisk -l
df -h
df -i
sudo mount /dev/sdb1 /mnt/data
sudo umount /mnt/data
```

Know **inode exhaustion** (df -i) — many tiny files can break services while `df -h` still looks fine.

Practice partitioning only on disposable VMs/disks.

## Common mistakes

- mkfs on the wrong disk
- umount busy filesystems without checking
- Ignoring inode usage

## Exercises

Work in `exercises/26-disks-fs/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/26-disks-fs/` until you have an honest failing attempt.**

## Self-check

1. lsblk shows what?
2. Why df -i?
3. mount purpose?

## Further reading

- https://man7.org/linux/man-pages/man8/lsblk.8.html

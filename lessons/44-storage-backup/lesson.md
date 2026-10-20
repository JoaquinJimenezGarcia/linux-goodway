---
title: "44. Backups, Snapshots, and Restore Drills"
---

# 44. Backups, Snapshots, and Restore Drills

**Phase:** Phase 8 — Packages, disks, storage  
**Estimated time:** 1–2 days  
**Slug:** `44-storage-backup`

## Learning objectives

- Define RPO/RTO simply
- Prefer tested restores
- Know snapshot vs backup
- Encrypt backups and manage keys

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

Untested backups are fiction.

Practice:

1. Take backup
2. Restore to a clean VM
3. Measure time and document gaps

Snapshots are not offsite backups. 3-2-1 rule still applies.

## Common mistakes

- Only on-disk snapshots in same AZ
- No restore rehearsal
- Unencrypted sensitive backups

## Exercises

Work in `exercises/44-storage-backup/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/44-storage-backup/` until you have an honest failing attempt.**

## Self-check

1. RPO vs RTO?
2. Why restore drills?
3. 3-2-1 idea?

## Further reading

- https://www.veeam.com/blog/321-backup-rule.html

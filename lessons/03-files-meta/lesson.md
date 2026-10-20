---
title: "03. Files, Links, and Metadata"
---

# 03. Files, Links, and Metadata

**Phase:** Phase 1 — Shell and filesystem  
**Estimated time:** 1–2 days  
**Slug:** `03-files-meta`

## Learning objectives

- Inspect files with file, stat, du, df
- Distinguish hard links vs symbolic links
- Understand inodes at a practical level
- Use touch, install, and install-like patterns

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

## Inspecting

```bash
file /bin/ls
stat myfile
du -sh *
df -h
```

## Inodes and links

A file name is a directory entry pointing to an **inode** (metadata + data blocks).

- **Hard link**: another name for the same inode (same filesystem only)
- **Symbolic link**: a pointer path (can dangle)

```bash
ln a.txt hard-a
ln -s a.txt soft-a
```

Deleting one hard link name does not remove data until the last link is gone.

## Common mistakes

- Assuming `rm` of a symlink deletes the target (it removes the link)
- Hard-linking directories (usually forbidden)
- Ignoring disk full (`df`) when services fail mysteriously

## Exercises

Work in `exercises/03-files-meta/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/03-files-meta/` until you have an honest failing attempt.**

## Self-check

1. Hard link vs symlink?
2. What does `stat` show that `ls -l` might not?
3. What does `df -h` report?

## Further reading

- https://man7.org/linux/man-pages/man1/ln.1.html

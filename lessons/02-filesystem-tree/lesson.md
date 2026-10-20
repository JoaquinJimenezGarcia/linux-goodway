---
title: "02. The Filesystem Tree: /, /etc, /var, /home, /proc"
---

# 02. The Filesystem Tree: /, /etc, /var, /home, /proc

**Phase:** Phase 1 — Shell and filesystem  
**Estimated time:** 1–2 days  
**Slug:** `02-filesystem-tree`

## Learning objectives

- Navigate with cd, pwd, ls
- Explain key FHS directories
- Create, move, copy, remove files carefully
- Use tab completion and wildcards

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

## Filesystem Hierarchy (FHS) highlights

| Path | Purpose |
|------|---------|
| `/` | root of the tree |
| `/bin`, `/usr/bin` | user commands |
| `/etc` | configuration |
| `/home` | user home directories |
| `/var` | logs, caches, variable data |
| `/tmp` | temporary (often cleared) |
| `/proc`, `/sys` | kernel/process info (virtual) |
| `/dev` | device nodes |

## Navigation and file ops

```bash
pwd
cd /etc
ls -la
mkdir -p ~/lab/linux-goodway
cp file.txt file.bak
mv oldname newname
rm file.txt          # careful
rm -r dirname        # careful; prefer trash tools when learning
```

## Wildcards

`*` any string, `?` one char, `[abc]` character class.

```bash
ls *.log
```

## Common mistakes

- Running `rm -rf /` or similar disasters
- Treating `/proc` files like normal disk files to edit casually
- Filling `/` by writing huge files to `/tmp` unchecked

## Exercises

Work in `exercises/02-filesystem-tree/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/02-filesystem-tree/` until you have an honest failing attempt.**

## Self-check

1. What lives in `/etc`?
2. What is special about `/proc`?
3. What does `mkdir -p` do?

## Further reading

- https://refspecs.linuxfoundation.org/FHS_3.0/fhs/index.html

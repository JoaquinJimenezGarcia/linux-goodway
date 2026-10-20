---
title: "06. Special Bits: setuid, setgid, sticky"
---

# 06. Special Bits: setuid, setgid, sticky

**Phase:** Phase 2 — Permissions and identity  
**Estimated time:** 1 day  
**Slug:** `06-special-perms`

## Learning objectives

- Explain setuid/setgid/sticky bit purposes
- Recognize them in `ls -l`
- Know security risks of setuid binaries
- Use sticky on shared directories like /tmp

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

## Sticky bit (directories)

On `/tmp`, sticky (`chmod +t`) means only file owner (and root) can delete their files —
even if others have write on the directory.

## setuid / setgid

- **setuid** on executable: runs as file owner (e.g. `passwd`)
- **setgid** on dir: new files inherit group

```bash
ls -l /usr/bin/passwd   # often looks like -rwsr-xr-x
```

setuid is powerful and dangerous — audit carefully; never ship custom setuid without review.

## Common mistakes

- Creating custom setuid root binaries casually
- World-writable setuid files (critical vulnerability)
- Ignoring sticky bit issues on shared drop folders

## Exercises

Work in `exercises/06-special-perms/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/06-special-perms/` until you have an honest failing attempt.**

## Self-check

1. What does sticky do on a directory?
2. Why does `passwd` use setuid?
3. Name one risk of setuid

## Further reading

- https://man7.org/linux/man-pages/man1/chmod.1.html

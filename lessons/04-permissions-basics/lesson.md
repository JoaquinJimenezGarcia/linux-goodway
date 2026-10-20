---
title: "04. Permissions Basics: rwx, chmod, chown"
---

# 04. Permissions Basics: rwx, chmod, chown

**Phase:** Phase 2 — Permissions and identity  
**Estimated time:** 1–2 days  
**Slug:** `04-permissions-basics`

## Learning objectives

- Read `ls -l` permission bits
- Change mode with chmod (symbolic and octal)
- Change owner/group with chown/chgrp
- Predict access for user/group/other

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

## Reading `ls -l`

```text
-rwxr-xr-- 1 ada dev 120 Mar 1 file.sh
│└─┬─┘└─┬─┘└─┬─┘
│  u    g    o
│ user group other
type: - file, d dir, l link
```

Bits: `r` read, `w` write, `x` execute (enter for dirs).

## chmod

```bash
chmod u+x script.sh
chmod 755 script.sh   # rwxr-xr-x
chmod 640 secret.txt  # rw-r-----
```

Octal: owner/group/other each as r=4,w=2,x=1 summed.

## Ownership

```bash
sudo chown ada:dev file
```

On shared servers, wrong group permissions are a common security bug.

## Common mistakes

- chmod 777 on everything "to make it work"
- Forgetting directories need `x` to be entered
- Running as root to avoid learning permissions

## Exercises

Work in `exercises/04-permissions-basics/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/04-permissions-basics/` until you have an honest failing attempt.**

## Self-check

1. What does 644 mean?
2. Why does a directory need execute?
3. When is 777 inappropriate?

## Further reading

- https://man7.org/linux/man-pages/man1/chmod.1.html

---
title: "31. ACLs and umask"
---

# 31. ACLs and umask

**Phase:** Phase 2 — Permissions and identity  
**Estimated time:** 1 day  
**Slug:** `31-permissions-acl`

## Learning objectives

- Explain umask defaults
- Read basic ACLs with getfacl
- Decide when ACLs are warranted
- Avoid ACL sprawl

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

```bash
umask -S
umask 022
touch /tmp/t; ls -l /tmp/t
getfacl file   # if ACL tools installed
```

umask subtracts permissions from defaults. ACLs add finer user/group rules beyond owner/group/other — powerful, easy to make unreadable systems. Prefer simple group ownership when enough.

## Common mistakes

- umask 000 creating world-writable files
- ACLs on every directory
- Forgetting defaults on shared project dirs

## Exercises

Work in `exercises/31-permissions-acl/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/31-permissions-acl/` until you have an honest failing attempt.**

## Self-check

1. What does umask 022 yield for files?
2. When use ACL vs groups?
3. getfacl purpose?

## Further reading

- https://man7.org/linux/man-pages/man1/umask.1p.html

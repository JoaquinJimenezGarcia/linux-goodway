---
title: "32. Capabilities, seccomp, and least privilege (intro)"
---

# 32. Capabilities, seccomp, and least privilege (intro)

**Phase:** Phase 9 — Security and SSH  
**Estimated time:** 1–2 days  
**Slug:** `32-capabilities-seccomp`

## Learning objectives

- Explain Linux capabilities vs all-powerful root
- Know seccomp exists for syscall filtering
- Apply least privilege to services
- Relate to container security defaults

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

Root is a bundle of **capabilities** (CAP_NET_BIND_SERVICE, CAP_SYS_ADMIN, ...).

Modern services drop capabilities; containers often start with reduced sets.
seccomp filters syscalls (Docker default profile).

You do not need to memorize every CAP — learn to ask: "does this process need full root?"

## Common mistakes

- Running containers --privileged by default
- Granting CAP_SYS_ADMIN casually
- Ignoring root in containers as "fine"

## Exercises

Work in `exercises/32-capabilities-seccomp/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/32-capabilities-seccomp/` until you have an honest failing attempt.**

## Self-check

1. What is a capability?
2. Why avoid --privileged?
3. seccomp filters what?

## Further reading

- https://man7.org/linux/man-pages/man7/capabilities.7.html

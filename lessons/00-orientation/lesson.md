---
title: "00. Orientation: What Linux Is and How to Practice"
---

# 00. Orientation: What Linux Is and How to Practice

**Phase:** Phase 0 — Orientation  
**Estimated time:** 1 day  
**Slug:** `00-orientation`

## Learning objectives

- Explain Linux vs Unix vs GNU userland at a beginner level
- Choose a practice environment (VM, cloud, WSL, or container)
- Open a shell and run your first commands safely
- Adopt the study method: attempt → struggle → solution → rewrite

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

## What is Linux?

**Linux** usually means the **kernel** (talks to hardware) plus a **userland**
(shells, coreutils, systemd, package manager) that makes a usable OS.

People say “Linux” for whole distributions: Ubuntu, Debian, Fedora, RHEL, Alpine.

| Layer | Role |
|-------|------|
| Hardware | CPU, disk, NIC |
| Kernel | processes, memory, drivers, networking stack |
| Userland | bash, ls, apt/dnf, sshd, your apps |

## Why learn Linux deeply?

Infrastructure, AI serving, containers, and cloud VMs almost all run Linux.
Copy-pasting Stack Overflow commands without understanding them causes outages.

## Practice environments

Pick one and stick with it for early lessons:

1. **Local VM** (UTM/VirtualBox) with Ubuntu Server
2. **Cloud VM** (small free-tier Linux instance)
3. **WSL2** on Windows
4. **Docker** (`docker run -it --rm ubuntu:24.04 bash`) for many CLI drills

macOS is Unix-like and fine for shell basics, but later lessons need real Linux
(systemd, apt/dnf, `/proc`). Prefer a Linux VM or container for those.

## Study method

1. Read the lesson PDF; type commands yourself.
2. Do exercises in `exercises/NN-slug/` — **no solutions first**.
3. Compare with `solutions/` only after an honest attempt.
4. Next day: rewrite scripts/commands from memory.

Track progress in `curriculum/PROGRESS.md`.

## Common mistakes

- Practicing only on macOS and skipping Linux-specific topics forever
- Running destructive commands as root without understanding them
- Skipping the rewrite-from-memory step

## Exercises

Work in `exercises/00-orientation/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/00-orientation/` until you have an honest failing attempt.**

## Self-check

1. What is the kernel vs userland?
2. Name two practice environments suitable for this course
3. Why avoid looking at solutions first?

## Further reading

- https://www.kernel.org/
- https://ubuntu.com/tutorials/command-line-for-beginners

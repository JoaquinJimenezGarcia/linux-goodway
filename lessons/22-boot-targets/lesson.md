---
title: "22. Boot Process, Targets, and Rescue Ideas"
---

# 22. Boot Process, Targets, and Rescue Ideas

**Phase:** Phase 7 — Services and boot  
**Estimated time:** 1–2 days  
**Slug:** `22-boot-targets`

## Learning objectives

- Describe BIOS/UEFI → bootloader → kernel → systemd
- List targets (multi-user, graphical, rescue)
- Change default target thoughtfully
- Know when to use recovery modes

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

## Simplified boot chain

Firmware → bootloader (GRUB) → kernel+initramfs → systemd (pid 1) → services

```bash
systemctl get-default
systemctl list-units --type=target
```

Rescue/emergency targets help recover broken systems — practice in a VM, not only in theory.

## Common mistakes

- Editing GRUB carelessly on the only laptop
- Setting graphical target on headless servers
- No backup before bootloader experiments

## Exercises

Work in `exercises/22-boot-targets/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/22-boot-targets/` until you have an honest failing attempt.**

## Self-check

1. What is pid 1?
2. multi-user.target meaning?
3. Why practice recovery in a VM?

## Further reading

- https://www.freedesktop.org/software/systemd/man/systemd.target.html

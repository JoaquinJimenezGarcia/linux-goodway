---
title: "48. SELinux/AppArmor Awareness"
---

# 48. SELinux/AppArmor Awareness

**Phase:** Phase 9 — Security and SSH  
**Estimated time:** 1–2 days  
**Slug:** `48-selinux-apparmor`

## Learning objectives

- Know which MAC system your distro uses
- Read basic denials from logs
- Avoid setenforce 0 as permanent fix
- Apply targeted policy changes properly

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

Mandatory Access Control (MAC) confines processes beyond chmod.

- RHEL family: SELinux
- Ubuntu: AppArmor

```bash
getenforce            # SELinux
sudo aa-status        # AppArmor
```

If a service fails only when confined, fix the policy — do not permanently disable MAC on prod.

## Common mistakes

- setenforce 0 forever
- Disabling AppArmor globally
- Ignoring AVC denial logs

## Exercises

Work in `exercises/48-selinux-apparmor/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/48-selinux-apparmor/` until you have an honest failing attempt.**

## Self-check

1. SELinux vs AppArmor typical distros?
2. Why not disable MAC?
3. Where see denials?

## Further reading

- https://www.selinuxproject.org/page/Main_Page

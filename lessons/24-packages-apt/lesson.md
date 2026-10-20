---
title: "24. Packages: apt/dpkg (Debian/Ubuntu)"
---

# 24. Packages: apt/dpkg (Debian/Ubuntu)

**Phase:** Phase 8 — Packages, disks, storage  
**Estimated time:** 1–2 days  
**Slug:** `24-packages-apt`

## Learning objectives

- Update and install with apt
- Query packages with dpkg/apt
- Clean caches thoughtfully
- Pin/version awareness

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

```bash
sudo apt update
sudo apt install curl
apt show curl
dpkg -L curl | head
apt-cache policy curl
```

Update package indexes before install. Prefer official repos; be careful with random PPAs.

RHEL family uses `dnf`/`rpm` — concepts transfer.

## Common mistakes

- disabling signature checks
- autoremoving blindly on prod
- mixing distro versions

## Exercises

Work in `exercises/24-packages-apt/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/24-packages-apt/` until you have an honest failing attempt.**

## Self-check

1. apt update vs upgrade?
2. How list files owned by a package?
3. Why official repos?

## Further reading

- https://ubuntu.com/server/docs/package-management

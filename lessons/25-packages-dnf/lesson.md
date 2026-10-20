---
title: "25. Packages: dnf/rpm (RHEL/Fedora) and Alpine apk"
---

# 25. Packages: dnf/rpm (RHEL/Fedora) and Alpine apk

**Phase:** Phase 8 — Packages, disks, storage  
**Estimated time:** 1 day  
**Slug:** `25-packages-dnf`

## Learning objectives

- Map apt concepts to dnf and apk
- Install/query/remove packages
- Know when distroless/minimal images help
- Read release notes before major upgrades

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

```bash
# RHEL/Fedora
sudo dnf install curl
rpm -ql curl | head

# Alpine
sudo apk add curl
```

Minimal images reduce attack surface for containers — but debugging tools may be absent (install temporarily or use sidecar debug patterns).

## Common mistakes

- Running untrusted RPM scripts without review
- Assuming package names identical across distros
- Upgrading major releases without backups

## Exercises

Work in `exercises/25-packages-dnf/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/25-packages-dnf/` until you have an honest failing attempt.**

## Self-check

1. dnf equivalent of apt install?
2. Why minimal images?
3. apk is for which distro?

## Further reading

- https://dnf.readthedocs.io/

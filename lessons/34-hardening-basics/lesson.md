---
title: "34. Host Hardening Checklist"
---

# 34. Host Hardening Checklist

**Phase:** Phase 9 — Security and SSH  
**Estimated time:** 1–2 days  
**Slug:** `34-hardening-basics`

## Learning objectives

- Apply a practical hardening baseline
- Disable unused services
- Enforce SSH key auth
- Keep patching cadence

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

## Baseline (servers)

- Updates installed regularly
- SSH: key-only, no root login, non-default port optional (not a real secret)
- Firewall default deny
- Only required packages
- Separate admin users + sudo
- Time sync on
- Disk encryption for laptops; careful key mgmt for servers

Hardening is continuous, not a one-time script from the internet blindly applied.

## Common mistakes

- Blindly running anonymous harden scripts
- Locking yourself out of SSH
- Assuming compliance checkbox equals secure

## Exercises

Work in `exercises/34-hardening-basics/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/34-hardening-basics/` until you have an honest failing attempt.**

## Self-check

1. Name five baseline items
2. Why disable unused services?
3. Risk of remote harden scripts?

## Further reading

- https://www.cisecurity.org/

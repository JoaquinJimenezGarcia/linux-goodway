---
title: "51. Building Your Persistent Linux Lab"
---

# 51. Building Your Persistent Linux Lab

**Phase:** Phase 0 — Orientation  
**Estimated time:** 1–2 days  
**Slug:** `51-lab-vm-practice`

## Learning objectives

- Create a disposable VM snapshot workflow
- Document lab IP/users
- Separate 'break glass' practice VMs
- Automate lab provisioning lightly

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

Your lab should let you:

- Snapshot before dangerous lessons (disks, boot, firewall)
- Reset quickly
- Take notes of what broke

Suggested: Ubuntu LTS VM + second Alpine container host for contrast.

## Common mistakes

- Practicing firewall on the only machine you own without console
- No snapshots
- Mixing prod credentials into lab

## Exercises

Work in `exercises/51-lab-vm-practice/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/51-lab-vm-practice/` until you have an honest failing attempt.**

## Self-check

1. Why snapshots?
2. What two distros to compare?
3. Prod creds in lab risk?

## Further reading

- https://ubuntu.com/download/server

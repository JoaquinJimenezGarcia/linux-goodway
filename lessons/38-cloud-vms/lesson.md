---
title: "38. Linux on Cloud VMs: metadata, identity, disks"
---

# 38. Linux on Cloud VMs: metadata, identity, disks

**Phase:** Phase 11 — Containers and cloud Linux  
**Estimated time:** 1–2 days  
**Slug:** `38-cloud-vms`

## Learning objectives

- Use instance metadata thoughtfully
- Attach/mount data disks
- Prefer IAM roles over long-lived keys
- Automate with cloud-init basics

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

Cloud VMs are Linux with extra APIs:

- Metadata service (IMDSv2 on AWS — hop limits matter)
- Identity via instance profiles/roles
- Ephemeral vs persistent disks
- cloud-init for first boot

```bash
# example pattern only — provider specific
curl -s http://169.254.169.254/ # know your cloud's secure usage!
```

Never expose metadata endpoints to containers/user workloads carelessly.

## Common mistakes

- IMDSv1 on exposed hosts
- Secrets baked into AMIs
- Data on ephemeral disks only

## Exercises

Work in `exercises/38-cloud-vms/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/38-cloud-vms/` until you have an honest failing attempt.**

## Self-check

1. What is cloud-init?
2. Why IAM roles over keys?
3. Metadata risk?

## Further reading

- https://cloudinit.readthedocs.io/

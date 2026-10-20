---
title: "45. Linux for AI Infrastructure"
---

# 45. Linux for AI Infrastructure

**Phase:** Phase 11 — Containers and cloud Linux  
**Estimated time:** 2 days  
**Slug:** `45-ai-infra-linux`

## Learning objectives

- Prepare GPU hosts at OS level (drivers/toolkit conceptually)
- Tune file limits and disk for datasets
- Isolate model servers with systemd/cgroups
- Observe GPU and host metrics

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

AI infra is still Linux ops:

- Drivers/toolkits (NVIDIA) + container runtimes
- Fast disks for datasets/checkpoints
- High nofile and process limits for many connections
- systemd units for inference servers
- Separating training noisy neighbors from latency-critical serving

Go/Python services you write eventually run here — OS skill multiplies app skill.

## Common mistakes

- Sharing one GPU host with zero isolation
- Datasets on tiny root disks
- No monitoring of GPU temp/utilization

## Exercises

Work in `exercises/45-ai-infra-linux/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/45-ai-infra-linux/` until you have an honest failing attempt.**

## Self-check

1. Why nofile for inference servers?
2. Where put large datasets?
3. Why cgroups/systemd isolation?

## Further reading

- https://docs.nvidia.com/datacenter/cloud-native/

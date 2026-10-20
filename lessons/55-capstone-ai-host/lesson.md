---
title: "55. Capstone: AI Inference Host on Linux"
---

# 55. Capstone: AI Inference Host on Linux

**Phase:** Phase 12 — Capstones  
**Estimated time:** 4–6 days  
**Slug:** `55-capstone-ai-host`

## Learning objectives

- Run an inference-friendly Linux host layout
- systemd + reverse proxy + TLS
- Resource limits and logs
- Load test and observe

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

## Mission

Prepare a Linux host (VM is fine without real GPU) as if serving a model API:

- App under systemd (can be a mock HTTP server)
- Reverse proxy with TLS (self-signed OK in lab)
- Limits: MemoryMax / CPUQuota in unit
- Logs + simple metrics endpoint or node exporter
- Firewall only 22/443
- Runbook for deploy/rollback
- Optional: containerized mock model with compose

## Rubric

- Least privilege unit
- Documented capacity limits
- Observability hooks
- Clean failure behavior under kill -TERM

## Common mistakes

- Privileged containers
- No memory limits
- No graceful shutdown testing

## Exercises

Work in `exercises/55-capstone-ai-host/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/55-capstone-ai-host/` until you have an honest failing attempt.**

## Self-check

1. How bound resources?
2. What happens on SIGTERM?
3. Which ports exposed?

## Further reading

- https://www.freedesktop.org/software/systemd/man/systemd.resource-control.html

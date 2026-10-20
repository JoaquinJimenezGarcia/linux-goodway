---
title: "46. Node Metrics and Exporters (ops intro)"
---

# 46. Node Metrics and Exporters (ops intro)

**Phase:** Phase 10 — Observability and troubleshooting  
**Estimated time:** 1–2 days  
**Slug:** `46-prometheus-node`

## Learning objectives

- Expose node metrics conceptually
- Know RED/USE for hosts
- Alert on disk/inode/memory
- Avoid high-cardinality labels

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

node_exporter + Prometheus/Grafana is a common Linux host monitoring stack.

Alert on:

- Disk >80–90%
- Inodes
- OOM events
- Systemd failed units
- Certificate expiry

Metrics without actionable alerts are wallpaper.

## Common mistakes

- Paging on noisy low-value alerts
- No runbooks
- Cardinality explosions

## Exercises

Work in `exercises/46-prometheus-node/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/46-prometheus-node/` until you have an honest failing attempt.**

## Self-check

1. Name three host alerts
2. USE method?
3. Why inode alerts?

## Further reading

- https://prometheus.io/docs/guides/node-exporter/

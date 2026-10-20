---
title: "29. Performance Basics: CPU, memory, iowait, OOM"
---

# 29. Performance Basics: CPU, memory, iowait, OOM

**Phase:** Phase 10 — Observability and troubleshooting  
**Estimated time:** 2 days  
**Slug:** `29-perf-basics`

## Learning objectives

- Read load average correctly
- Spot memory pressure and OOM
- Distinguish CPU-bound vs IO-bound
- Use vmstat/iostat at a basic level

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

```bash
uptime
free -h
vmstat 1 5
# iostat if sysstat installed
dmesg | grep -i oom
```

Load average must be compared to CPU count. High iowait → storage/network path, not always "need more CPU".

OOM killer murders processes when memory is exhausted — fix leaks/limits, don't only raise RAM forever.

## Common mistakes

- Misreading load average
- Disabling OOM killer
- Optimizing CPU while disk is the bottleneck

## Exercises

Work in `exercises/29-perf-basics/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/29-perf-basics/` until you have an honest failing attempt.**

## Self-check

1. Load 4 on 2 CPUs means?
2. How spot OOM?
3. iowait suggests what?

## Further reading

- https://www.brendangregg.com/linuxperf.html

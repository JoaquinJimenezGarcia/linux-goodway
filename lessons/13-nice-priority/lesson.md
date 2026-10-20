---
title: "13. Priority, nice, and resource limits (ulimit)"
---

# 13. Priority, nice, and resource limits (ulimit)

**Phase:** Phase 4 — Processes and jobs  
**Estimated time:** 1 day  
**Slug:** `13-nice-priority`

## Learning objectives

- Adjust niceness
- Inspect ulimit
- Explain why limits exist
- Connect to cgroups at a high level

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

## nice

```bash
nice -n 10 ./batch.sh
renice 5 -p <pid>
```

Higher nice value → lower priority (be nicer to others).

## ulimit

```bash
ulimit -a
ulimit -n 4096   # open files (session)
```

Production systems set limits via systemd (`LimitNOFILE=`) or `/etc/security/limits.conf`.

## cgroups

Modern Linux isolates CPU/memory via cgroups (containers use this heavily).

## Common mistakes

- Raising nofile without diagnosing fd leaks
- Assuming nice makes a slow disk fast
- Ignoring OOM killer symptoms

## Exercises

Work in `exercises/13-nice-priority/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/13-nice-priority/` until you have an honest failing attempt.**

## Self-check

1. Does higher nice mean more CPU?
2. Why limit open files?
3. What tech do containers use for limits?

## Further reading

- https://man7.org/linux/man-pages/man1/nice.1.html

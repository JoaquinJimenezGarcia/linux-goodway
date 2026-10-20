---
title: "23. Scheduling: cron and systemd timers"
---

# 23. Scheduling: cron and systemd timers

**Phase:** Phase 7 — Services and boot  
**Estimated time:** 1–2 days  
**Slug:** `23-cron-timers`

## Learning objectives

- Write crontab entries
- Prefer systemd timers for modern systems
- Handle environment differences in scheduled jobs
- Log scheduled task output

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

```bash
crontab -e
# m h dom mon dow command
0 3 * * * /usr/local/bin/backup.sh
```

## systemd timers

More observable than cron on systemd distros — pair `.timer` + `.service`.

Scheduled jobs often miss env vars available interactively — use absolute paths and explicit `Environment=`.

## Common mistakes

- Relative paths in cron
- Emailing root floods from cron noise
- Duplicate cron+timer doing same job

## Exercises

Work in `exercises/23-cron-timers/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/23-cron-timers/` until you have an honest failing attempt.**

## Self-check

1. Cron five fields meaning?
2. Why absolute paths?
3. Timer vs cron advantage?

## Further reading

- https://man7.org/linux/man-pages/man5/crontab.5.html

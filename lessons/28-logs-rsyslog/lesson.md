---
title: "28. Logging: journald, syslog, and log files"
---

# 28. Logging: journald, syslog, and log files

**Phase:** Phase 10 — Observability and troubleshooting  
**Estimated time:** 1–2 days  
**Slug:** `28-logs-rsyslog`

## Learning objectives

- Find logs under /var/log
- Use journalctl effectively
- Rotate logs conceptually
- Correlate time across hosts

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

```bash
sudo tail -f /var/log/syslog   # Debian-like
sudo journalctl -xe
sudo journalctl -u ssh -S today
```

Log rotation (logrotate) prevents disks filling. Centralize logs in real infra (Loki/ELK) — but master local logs first.

Keep clocks synced (chrony/ntp) or timelines lie.

## Common mistakes

- Deleting active log files to free space the wrong way
- No retention policy
- Ignoring permission on log dirs

## Exercises

Work in `exercises/28-logs-rsyslog/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/28-logs-rsyslog/` until you have an honest failing attempt.**

## Self-check

1. Where are traditional text logs?
2. journalctl -u meaning?
3. Why NTP for logs?

## Further reading

- https://www.freedesktop.org/software/systemd/man/journalctl.html

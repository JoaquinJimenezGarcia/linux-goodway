---
title: "21. systemd: Units, Services, Journals"
---

# 21. systemd: Units, Services, Journals

**Phase:** Phase 7 — Services and boot  
**Estimated time:** 2 days  
**Slug:** `21-systemd-units`

## Learning objectives

- Manage services with systemctl
- Read logs with journalctl
- Write a simple unit file
- Enable services on boot

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

```bash
systemctl status ssh
sudo systemctl restart nginx
sudo systemctl enable --now nginx
journalctl -u nginx -n 100 --no-pager
journalctl -S "1 hour ago"
```

## Unit sketch

```ini
[Unit]
Description=My Worker
After=network.target

[Service]
ExecStart=/usr/local/bin/worker
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Linux servers today are systemd-centric — this is mandatory knowledge for infra.

## Common mistakes

- kill -9 instead of systemctl stop
- Ignoring Restart= policy
- Not checking journal after failed start

## Exercises

Work in `exercises/21-systemd-units/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/21-systemd-units/` until you have an honest failing attempt.**

## Self-check

1. enable vs start?
2. How follow service logs?
3. WantedBy meaning?

## Further reading

- https://www.freedesktop.org/software/systemd/man/systemctl.html

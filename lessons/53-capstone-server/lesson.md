---
title: "53. Capstone: Harden and Operate a Linux Web Server"
---

# 53. Capstone: Harden and Operate a Linux Web Server

**Phase:** Phase 12 — Capstones  
**Estimated time:** 3–5 days  
**Slug:** `53-capstone-server`

## Learning objectives

- Provision a Linux VM
- Serve a simple site behind a reverse proxy
- Add firewall, SSH hardening, systemd unit
- Document runbook + restore notes

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

## Mission

Build a small but real server:

- Nginx (or Caddy) serving a static site or reverse-proxying an app
- systemd unit for the app
- ufw/firewalld with minimal ports
- SSH key-only
- journald/log rotation awareness
- Backup + restore drill of site content
- Short runbook (start/stop/debug)

## Rubric (excellent)

- Reproducible setup notes
- No password SSH
- Fails closed firewall
- Evidence of restore test
- Clean boot after reboot

## Common mistakes

- ClickOps without notes
- Ports 0.0.0.0 wide open
- No reboot test

## Exercises

Work in `exercises/53-capstone-server/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/53-capstone-server/` until you have an honest failing attempt.**

## Self-check

1. What ports are open and why?
2. How prove restore?
3. What happens after reboot?

## Further reading

- https://ubuntu.com/server/docs

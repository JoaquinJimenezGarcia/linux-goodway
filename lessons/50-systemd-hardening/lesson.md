---
title: "50. systemd Service Hardening Directives"
---

# 50. systemd Service Hardening Directives

**Phase:** Phase 7 — Services and boot  
**Estimated time:** 1–2 days  
**Slug:** `50-systemd-hardening`

## Learning objectives

- Apply ProtectSystem/NoNewPrivileges ideas
- Constrain WritablePaths
- Run as dedicated DynamicUser/User
- Read systemd-analyze security

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

```ini
[Service]
User=myapp
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
```

```bash
systemd-analyze security myapp.service
```

Hardened units reduce blast radius when the app is compromised.

## Common mistakes

- Running network services as root without need
- ProtectSystem without testing paths
- Ignoring analyze security suggestions forever

## Exercises

Work in `exercises/50-systemd-hardening/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/50-systemd-hardening/` until you have an honest failing attempt.**

## Self-check

1. NoNewPrivileges meaning?
2. PrivateTmp purpose?
3. Why dedicated User?

## Further reading

- https://www.freedesktop.org/software/systemd/man/systemd.exec.html

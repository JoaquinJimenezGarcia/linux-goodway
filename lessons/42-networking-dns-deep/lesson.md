---
title: "42. DNS Debugging and /etc/resolv.conf"
---

# 42. DNS Debugging and /etc/resolv.conf

**Phase:** Phase 6 — Networking  
**Estimated time:** 1 day  
**Slug:** `42-networking-dns-deep`

## Learning objectives

- Read resolv.conf and systemd-resolved
- Debug NXDOMAIN vs timeout
- Understand search domains
- Cache flush awareness

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

```bash
cat /etc/resolv.conf
resolvectl status   # systemd-resolved systems
dig +trace example.com
getent ahosts example.com
```

Symptoms: app "cannot connect" often starts as DNS. Split corporate DNS and split-horizon issues are common in infra.

## Common mistakes

- Hardcoding 8.8.8.8 breaking private zones
- Ignoring search domain effects
- Assuming dig failure equals network down

## Exercises

Work in `exercises/42-networking-dns-deep/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/42-networking-dns-deep/` until you have an honest failing attempt.**

## Self-check

1. NXDOMAIN meaning?
2. search domain effect?
3. Why dig +trace?

## Further reading

- https://man7.org/linux/man-pages/man5/resolv.conf.5.html

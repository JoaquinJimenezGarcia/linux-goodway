---
title: "18. Listening Sockets, ss, and Firewalls Intro"
---

# 18. Listening Sockets, ss, and Firewalls Intro

**Phase:** Phase 6 — Networking  
**Estimated time:** 1–2 days  
**Slug:** `18-ss-netstat-firewall`

## Learning objectives

- List listening ports with ss
- Map ports to processes
- Explain firewall purpose (nftables/ufw)
- Open only needed ports

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

```bash
ss -tulpn
sudo ss -tulpn | grep ':22'
```

## Firewalls

- **ufw** (Ubuntu simple wrapper)
- **firewalld** (RHEL family)
- **nftables/iptables** (underlying)

```bash
sudo ufw status
sudo ufw allow 22/tcp
```

Default deny inbound is a healthy posture for servers.

## Common mistakes

- Disabling firewall instead of opening one port
- Binding services to 0.0.0.0 unintentionally
- Forgetting IPv6 rules

## Exercises

Work in `exercises/18-ss-netstat-firewall/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/18-ss-netstat-firewall/` until you have an honest failing attempt.**

## Self-check

1. ss -tulpn meaning?
2. Why default deny?
3. How allow SSH on ufw?

## Further reading

- https://man7.org/linux/man-pages/man8/ss.8.html

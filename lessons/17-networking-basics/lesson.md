---
title: "17. Networking Basics: IP, DNS, Ports"
---

# 17. Networking Basics: IP, DNS, Ports

**Phase:** Phase 6 — Networking  
**Estimated time:** 1–2 days  
**Slug:** `17-networking-basics`

## Learning objectives

- Explain IP, CIDR, ports at a practical level
- Query DNS with dig/nslookup/getent
- Inspect addresses with ip
- Test connectivity with ping/curl

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

## Essentials

- **IP address**: host identity on a network
- **Port**: endpoint for a service (22 ssh, 80 http, 443 https)
- **DNS**: names → addresses

```bash
ip addr
ip route
dig example.com +short
getent hosts example.com
ping -c 3 1.1.1.1
curl -I https://example.com
```

On older systems you may see `ifconfig`/`route` — prefer `ip` on modern Linux.

## Common mistakes

- Assuming ping failure means everything is down (ICMP may be blocked)
- Hardcoding IPs without DNS strategy
- Opening all ports "temporarily"

## Exercises

Work in `exercises/17-networking-basics/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/17-networking-basics/` until you have an honest failing attempt.**

## Self-check

1. What is a port?
2. How resolve DNS from CLI?
3. ip addr shows what?

## Further reading

- https://man7.org/linux/man-pages/man8/ip.8.html

---
title: "49. Packet Filtering Mental Model (nftables)"
---

# 49. Packet Filtering Mental Model (nftables)

**Phase:** Phase 6 — Networking  
**Estimated time:** 1–2 days  
**Slug:** `49-networking-nft`

## Learning objectives

- Explain chains/tables conceptually
- Prefer high-level tools when enough (ufw/firewalld)
- Log drops thoughtfully
- Test rules remotely with care

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

nftables is the modern Linux packet filter framework.

For many servers, ufw/firewalld is enough. When you need custom:

- Default drop inbound
- Allow established/related
- Explicit allow SSH before enabling drop policies
- Keep a console/VMC session when testing remotely

## Common mistakes

- Locking yourself out mid-SSH
- Logging every accepted packet
- Contradictory overlapping rules

## Exercises

Work in `exercises/49-networking-nft/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/49-networking-nft/` until you have an honest failing attempt.**

## Self-check

1. Why allow established?
2. How avoid lockout?
3. ufw vs raw nftables?

## Further reading

- https://wiki.nftables.org/

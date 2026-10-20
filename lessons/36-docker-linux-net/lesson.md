---
title: "36. Containers, Namespaces, and Networking"
---

# 36. Containers, Namespaces, and Networking

**Phase:** Phase 11 — Containers and cloud Linux  
**Estimated time:** 2 days  
**Slug:** `36-docker-linux-net`

## Learning objectives

- Name major namespaces (pid, net, mnt, user)
- Explain bridge networking basics
- Debug DNS inside containers
- Use host networking knowingly

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

Linux containers = namespaces + cgroups + union filesystems.

```bash
docker network ls
docker run --rm busybox nslookup example.com
```

Network modes: bridge (default), host, none, overlay (swarm/k8s).

When networking "feels broken", check: DNS, published ports, firewall, and whether you expected localhost on host vs container.

## Common mistakes

- --network host as default habit
- Assuming localhost in container is the host
- Ignoring cgroup memory limits

## Exercises

Work in `exercises/36-docker-linux-net/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/36-docker-linux-net/` until you have an honest failing attempt.**

## Self-check

1. What do namespaces isolate?
2. Default docker network mode?
3. localhost confusion?

## Further reading

- https://docs.docker.com/network/

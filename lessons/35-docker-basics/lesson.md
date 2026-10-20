---
title: "35. Docker Basics on Linux"
---

# 35. Docker Basics on Linux

**Phase:** Phase 11 — Containers and cloud Linux  
**Estimated time:** 2 days  
**Slug:** `35-docker-basics`

## Learning objectives

- Run containers interactively
- Understand images vs containers
- Mount volumes and publish ports
- Read container logs

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

```bash
docker run --rm -it ubuntu:24.04 bash
docker run --rm -p 8080:80 nginx
docker ps -a
docker logs <id>
docker build -t myapp .
```

Containers share the host kernel — they are not VMs. Isolation is strong but not magic; harden accordingly.

Practice on Linux. Docker Desktop on Mac is OK for learning commands, but production semantics are Linux.

## Common mistakes

- docker.sock mounted into untrusted containers
- Running as root inside without need
- Storing secrets in images

## Exercises

Work in `exercises/35-docker-basics/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/35-docker-basics/` until you have an honest failing attempt.**

## Self-check

1. Image vs container?
2. What does --rm do?
3. Why shared kernel matters?

## Further reading

- https://docs.docker.com/get-started/

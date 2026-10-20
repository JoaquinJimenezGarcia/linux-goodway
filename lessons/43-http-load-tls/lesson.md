---
title: "43. Load Balancing and Reverse Proxy (Linux view)"
---

# 43. Load Balancing and Reverse Proxy (Linux view)

**Phase:** Phase 6 — Networking  
**Estimated time:** 1–2 days  
**Slug:** `43-http-load-tls`

## Learning objectives

- Explain reverse proxy role
- Read nginx/Caddy basics at config level
- Terminate TLS at proxy
- Health checks and upstreams

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

Linux hosts often run nginx/HAProxy/Envoy as edge or sidecars.

Concepts:

- Upstream pool
- Health checks
- TLS termination vs passthrough
- Access/error logs

You will configure these repeatedly in AI/gateway and microservice designs.

## Common mistakes

- Single upstream without health checks
- Weak TLS configs
- Logging secrets at info level

## Exercises

Work in `exercises/43-http-load-tls/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/43-http-load-tls/` until you have an honest failing attempt.**

## Self-check

1. What is TLS termination?
2. Why health checks?
3. Where find nginx error log?

## Further reading

- https://nginx.org/en/docs/

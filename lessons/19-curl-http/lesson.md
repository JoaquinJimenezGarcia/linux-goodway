---
title: "19. HTTP from the CLI: curl and friends"
---

# 19. HTTP from the CLI: curl and friends

**Phase:** Phase 6 — Networking  
**Estimated time:** 1 day  
**Slug:** `19-curl-http`

## Learning objectives

- Fetch URLs with curl
- Inspect headers and status codes
- POST JSON for APIs
- Follow redirects consciously

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

```bash
curl -I https://example.com
curl -sS -o body.txt -w "%{http_code}\n" https://example.com
curl -X POST -H 'Content-Type: application/json' -d '{"a":1}' https://httpbin.org/post
```

`-sS` silent but show errors. Prefer explicit timeouts in scripts:

```bash
curl --connect-timeout 2 --max-time 10 ...
```

## Common mistakes

- curl without timeouts hanging automation
- Leaking tokens in shell history
- Ignoring TLS verification permanently with -k

## Exercises

Work in `exercises/19-curl-http/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/19-curl-http/` until you have an honest failing attempt.**

## Self-check

1. What does -I do?
2. Why set max-time?
3. How send JSON POST?

## Further reading

- https://curl.se/docs/manual.html

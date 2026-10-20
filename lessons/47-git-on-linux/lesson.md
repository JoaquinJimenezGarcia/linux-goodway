---
title: "47. Git on the Server and Hooks (ops angle)"
---

# 47. Git on the Server and Hooks (ops angle)

**Phase:** Phase 5 — Shell scripting  
**Estimated time:** 1 day  
**Slug:** `47-git-on-linux`

## Learning objectives

- Use git safely on servers
- Understand deploy keys
- Avoid editing prod checkouts casually
- Know hook basics

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

Servers may pull release tags via CI, not humans SSH-editing `/opt/app`.

If git is used on hosts:

- Deploy keys read-only when possible
- Clean working trees
- Tagged releases

Prefer artifact images over "git pull on prod".

## Common mistakes

- git pull as root on live main
- Write-capable deploy keys broadly
- Uncommitted hotfixes on servers

## Exercises

Work in `exercises/47-git-on-linux/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/47-git-on-linux/` until you have an honest failing attempt.**

## Self-check

1. Why immutable artifacts?
2. Deploy key purpose?
3. Risk of prod git pull?

## Further reading

- https://git-scm.com/book/en/v2

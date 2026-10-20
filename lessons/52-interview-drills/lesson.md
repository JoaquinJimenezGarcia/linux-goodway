---
title: "52. Linux Interview and Oncall Drills"
---

# 52. Linux Interview and Oncall Drills

**Phase:** Phase 10 — Observability and troubleshooting  
**Estimated time:** 2 days  
**Slug:** `52-interview-drills`

## Learning objectives

- Explain debugging aloud with structure
- Solve timed scenarios
- Write clear handoff notes
- Prioritize user impact

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

Practice prompts:

- "Site is slow" — what do you check first 10 minutes?
- Disk full at 2am
- TLS expired
- One node NotReady in k8s
- SSH refused suddenly

Score yourself on: structure, evidence, communication, fix verification.

## Common mistakes

- Jumping to exotic theories first
- No communication during incident
- Fixing without verifying

## Exercises

Work in `exercises/52-interview-drills/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/52-interview-drills/` until you have an honest failing attempt.**

## Self-check

1. First 3 checks for 'slow'?
2. Why verify after fix?
3. Handoff note contents?

## Further reading

- https://sre.google/sre-book/managing-incidents/

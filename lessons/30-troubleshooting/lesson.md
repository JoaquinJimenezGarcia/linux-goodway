---
title: "30. Troubleshooting Method: REDUCE and Bisect"
---

# 30. Troubleshooting Method: REDUCE and Bisect

**Phase:** Phase 10 — Observability and troubleshooting  
**Estimated time:** 1–2 days  
**Slug:** `30-troubleshooting`

## Learning objectives

- Apply a systematic troubleshooting loop
- Capture evidence before rebooting
- Bisect recent changes
- Write short incident notes

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

## Habit loop

1. **Define** what "broken" means (symptom, since when, scope)
2. **Reproduce** or observe live
3. **Evidence**: logs, metrics, `ss`, disk, recent deploys
4. **Hypothesize** one change at a time
5. **Fix** + verify
6. **Notes** for future you

Rebooting loses evidence. Snapshot first when possible.

## "Did anything change?"

Configs, packages, certs, DNS, disks full, neighbor noisy tenant — change discipline beats heroics.

## Common mistakes

- Changing five things at once
- Reboot as first step always
- No notes after 3am fixes

## Exercises

Work in `exercises/30-troubleshooting/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/30-troubleshooting/` until you have an honest failing attempt.**

## Self-check

1. Why capture evidence first?
2. What is bisection?
3. Name three evidence sources

## Further reading

- https://sre.google/sre-book/

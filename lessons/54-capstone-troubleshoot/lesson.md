---
title: "54. Capstone: Broken Box Challenge"
---

# 54. Capstone: Broken Box Challenge

**Phase:** Phase 12 — Capstones  
**Estimated time:** 2–4 days  
**Slug:** `54-capstone-troubleshoot`

## Learning objectives

- Debug a deliberately broken VM
- Capture timeline and root cause
- Fix with minimal change
- Write postmortem

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

## Mission

Someone (you, earlier) breaks a snapshot on purpose: full disk, bad fstab, broken DNS, failed unit, wrong permissions, expired cert — pick 3+.

Restore service with a written postmortem:

- Impact
- Timeline
- Root cause
- Fix
- Prevention

## Rubric

- Structured troubleshooting
- Evidence preserved
- Minimal blast radius
- Clear prevention items

## Common mistakes

- Recreating VM instead of debugging
- Changing everything at once
- No postmortem

## Exercises

Work in `exercises/54-capstone-troubleshoot/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/54-capstone-troubleshoot/` until you have an honest failing attempt.**

## Self-check

1. What was root cause?
2. What evidence?
3. What prevention?

## Further reading

- https://sre.google/sre-book/postmortem-culture/

---
title: "40. Shell Text Mastery Drill Week"
---

# 40. Shell Text Mastery Drill Week

**Phase:** Phase 3 — Text, pipes, and discovery  
**Estimated time:** 2–3 days  
**Slug:** `40-shell-text-mastery`

## Learning objectives

- Combine grep/sed/awk/sort/uniq fluently
- Write one-liners you can explain line-by-line
- Profile slow pipelines
- Prefer clarity over golf

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

Drill pipelines on real logs (sample files in exercises).

Goals:

- Frequency counts
- Top-N talkers
- Field extraction
- Dedup and joins with `sort`/`join`

Clarity > cleverness. If you cannot explain it, do not ship it.

## Common mistakes

- Unreadable golf one-liners in prod
- Loading entire huge files into arrays unnecessarily
- Locale surprises in sort

## Exercises

Work in `exercises/40-shell-text-mastery/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/40-shell-text-mastery/` until you have an honest failing attempt.**

## Self-check

1. How top-N with sort|uniq -c?
2. Why LC_ALL=C sometimes?
3. When rewrite as a script?

## Further reading

- https://www.gnu.org/software/coreutils/manual/

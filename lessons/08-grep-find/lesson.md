---
title: "08. grep, ripgrep mindset, and find"
---

# 08. grep, ripgrep mindset, and find

**Phase:** Phase 3 — Text, pipes, and discovery  
**Estimated time:** 1–2 days  
**Slug:** `08-grep-find`

## Learning objectives

- Search file contents with grep
- Find files by name/type/time with find
- Combine find -exec / xargs safely
- Avoid unsafe parsing of filenames with spaces

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

## grep

```bash
grep -RIn "TODO" .
grep -E "error|warn" app.log
grep -v "^#" config   # invert
```

## find

```bash
find . -name "*.log" -mtime -1
find /var/log -type f -size +100M
find . -name "*.tmp" -delete   # careful
```

## Safe xargs

```bash
find . -name "*.txt" -print0 | xargs -0 wc -l
```

Null-delimited pipelines survive spaces/newlines in names.

## Common mistakes

- Parsing `ls` output in scripts
- `find | xargs` without `-print0`/`-0`
- Recursive grep on huge binary trees without limits

## Exercises

Work in `exercises/08-grep-find/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/08-grep-find/` until you have an honest failing attempt.**

## Self-check

1. Why `-print0`?
2. Find files modified in last day?
3. grep flag to show line numbers?

## Further reading

- https://man7.org/linux/man-pages/man1/find.1.html

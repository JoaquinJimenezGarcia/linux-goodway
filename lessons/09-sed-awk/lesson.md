---
title: "09. sed and awk for Text Engineering"
---

# 09. sed and awk for Text Engineering

**Phase:** Phase 3 — Text, pipes, and discovery  
**Estimated time:** 2 days  
**Slug:** `09-sed-awk`

## Learning objectives

- Perform common sed substitutions
- Use awk for column processing
- Choose the right tool (cut/sort/uniq vs awk)
- Write small one-liners you can explain

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

## sed

```bash
sed 's/foo/bar/' file
sed -i 's/foo/bar/g' file   # in-place (GNU); on macOS sed differs
sed -n '1,20p' file
```

## awk

```bash
awk '{print $1, $3}' file
awk -F: '{print $1}' /etc/passwd
awk '$3 > 1000' data
```

awk is a tiny programming language — excellent for logs and reports.

## Classic combo

```bash
cut -d: -f1 /etc/passwd | sort | uniq
```

## Common mistakes

- Blind in-place sed without backup
- Using awk where `cut` suffices (or vice versa for complex fields)
- Assuming GNU sed flags on BSD/macOS

## Exercises

Work in `exercises/09-sed-awk/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/09-sed-awk/` until you have an honest failing attempt.**

## Self-check

1. What does `s/a/b/g` mean?
2. How set awk field separator to `:`?
3. When prefer awk over cut?

## Further reading

- https://www.gnu.org/software/gawk/manual/

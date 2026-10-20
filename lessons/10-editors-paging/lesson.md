---
title: "10. Less, editors, and reading large output"
---

# 10. Less, editors, and reading large output

**Phase:** Phase 3 — Text, pipes, and discovery  
**Estimated time:** 1 day  
**Slug:** `10-editors-paging`

## Learning objectives

- Page output with less/more
- Edit files in nano or vim at a basic level
- Search inside less
- Avoid opening multi-GB logs in a GUI editor

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

## less

```bash
less huge.log
# /pattern  search
# n next, q quit, F follow (like tail -f)
```

## Editors

Learn **enough** vim or stick with nano while learning Linux:

```bash
nano file.txt
vim file.txt   # :wq save+quit, :q! discard
```

For infra work, vim/emacs fluency pays off over years — but do not block learning shell on editor mastery.

## Common mistakes

- cat-ing multi-GB files to the terminal
- Getting stuck in vim without knowing `:q!`
- Editing production configs without backups

## Exercises

Work in `exercises/10-editors-paging/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/10-editors-paging/` until you have an honest failing attempt.**

## Self-check

1. How search in less?
2. How quit vim without saving?
3. Why page instead of cat?

## Further reading

- https://www.vim.org/

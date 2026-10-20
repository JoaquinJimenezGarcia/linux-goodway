---
title: "01. The Shell: Prompts, Commands, Arguments, Exit Codes"
---

# 01. The Shell: Prompts, Commands, Arguments, Exit Codes

**Phase:** Phase 1 — Shell and filesystem  
**Estimated time:** 1 day  
**Slug:** `01-shell-basics`

## Learning objectives

- Run commands with arguments and flags
- Read exit codes (`$?`) and why they matter
- Use `--help` / man pages productively
- Distinguish absolute vs relative paths

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

## Anatomy of a command

```bash
ls -la /tmp
# ^   ^  ^
# |   |  argument (path)
# |   options/flags
# program name
```

## Exit codes

Every process returns an integer exit status:

```bash
true; echo $?    # 0 = success
false; echo $?   # non-zero = failure
```

Scripts and CI systems rely on this. **0 means success** by convention.

## Getting help

```bash
man ls
ls --help
whatis grep
```

Skim SYNOPSIS first, then EXAMPLES if present.

## Paths

- Absolute: `/home/ada/file` (starts at `/`)
- Relative: `./file`, `../sibling`, `docs/readme`

`.` is current directory; `..` is parent.

## Common mistakes

- Ignoring exit codes and assuming success
- Confusing flags that need spaces vs combined short flags
- Not reading man page SYNOPSIS

## Exercises

Work in `exercises/01-shell-basics/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/01-shell-basics/` until you have an honest failing attempt.**

## Self-check

1. What does exit code 0 mean?
2. Absolute vs relative path?
3. How do you open the manual for `cp`?

## Further reading

- https://man7.org/linux/man-pages/man1/bash.1.html

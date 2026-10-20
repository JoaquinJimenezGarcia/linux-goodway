---
title: "11. Processes: ps, top, /proc, signals"
---

# 11. Processes: ps, top, /proc, signals

**Phase:** Phase 4 — Processes and jobs  
**Estimated time:** 1–2 days  
**Slug:** `11-processes`

## Learning objectives

- List and interpret processes
- Read process state from /proc
- Send signals with kill
- Understand PID, PPID, zombie/orphan concepts

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

## Viewing processes

```bash
ps aux
ps -ef
top    # or htop if installed
```

Columns to care about: PID, USER, %CPU, %MEM, COMMAND.

## /proc

```bash
ls /proc/self
cat /proc/$$/status | head
```

Each PID has a directory under `/proc` with fds, environ, cmdline (Linux).

## Signals

```bash
kill -TERM <pid>   # polite stop (15)
kill -KILL <pid>   # force (9) — last resort
kill -HUP <pid>    # often reload config
```

Prefer TERM before KILL. Applications should handle SIGTERM for graceful shutdown.

## Common mistakes

- kill -9 as first resort
- Misreading CPU% in top
- Ignoring zombie processes as always urgent (often waitpid missing)

## Exercises

Work in `exercises/11-processes/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/11-processes/` until you have an honest failing attempt.**

## Self-check

1. TERM vs KILL?
2. What is PPID?
3. What does /proc contain?

## Further reading

- https://man7.org/linux/man-pages/man1/ps.1.html

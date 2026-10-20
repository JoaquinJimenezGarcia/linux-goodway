---
title: "12. Jobs, Background, nohup, screen/tmux intro"
---

# 12. Jobs, Background, nohup, screen/tmux intro

**Phase:** Phase 4 — Processes and jobs  
**Estimated time:** 1 day  
**Slug:** `12-jobs-background`

## Learning objectives

- Run jobs in background
- Use fg/bg/jobs
- Keep sessions with tmux
- Apply nohup carefully

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

## Job control

```bash
longcmd &
jobs
fg %1
Ctrl-Z   # suspend
bg
```

## tmux (learn early)

Remote work without losing sessions:

```bash
tmux new -s lab
# detach: Ctrl-b d
tmux attach -t lab
```

## nohup

```bash
nohup ./worker > worker.out 2>&1 &
```

Still prefer systemd units for real services.

## Common mistakes

- Leaving critical prod tasks only in a laptop terminal
- nohup without log rotation
- Detaching mentally but not from tmux

## Exercises

Work in `exercises/12-jobs-background/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/12-jobs-background/` until you have an honest failing attempt.**

## Self-check

1. How detach tmux?
2. What does & do?
3. When use systemd instead of nohup?

## Further reading

- https://github.com/tmux/tmux/wiki

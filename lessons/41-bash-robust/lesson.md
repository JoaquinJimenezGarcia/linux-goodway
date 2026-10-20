---
title: "41. Robust Bash: errexit, nounset, traps"
---

# 41. Robust Bash: errexit, nounset, traps

**Phase:** Phase 5 — Shell scripting  
**Estimated time:** 1–2 days  
**Slug:** `41-bash-robust`

## Learning objectives

- Use traps for cleanup
- Handle signals in scripts
- Create temp dirs safely
- Write scripts that fail loudly

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

```bash
set -euo pipefail
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

work() { ...; }
work
```

traps ensure cleanup on exit/signals. Combined with nounset, many silent bugs become loud.

## Common mistakes

- rm -rf unprotected tmp
- Ignoring ERR traps for critical scripts
- set +e hiding failures permanently

## Exercises

Work in `exercises/41-bash-robust/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/41-bash-robust/` until you have an honest failing attempt.**

## Self-check

1. What does trap EXIT do?
2. mktemp why?
3. nounset catches what?

## Further reading

- https://mywiki.wooledge.org/SignalTrap

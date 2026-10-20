---
title: "15. Functions, Arguments, and Exit Codes in Scripts"
---

# 15. Functions, Arguments, and Exit Codes in Scripts

**Phase:** Phase 5 — Shell scripting  
**Estimated time:** 1–2 days  
**Slug:** `15-bash-functions-args`

## Learning objectives

- Define functions and local variables
- Validate arguments
- Return meaningful exit codes
- Source libraries carefully

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

```bash
usage() {
  echo "Usage: $0 <input>" >&2
  exit 2
}

[[ $# -ge 1 ]] || usage
input=$1

greet() {
  local who=$1
  echo "Hi $who"
}

greet "$input"
```

Exit codes: 0 ok, non-zero failure; 2 often means misuse.

`source ./lib.sh` pulls definitions into current shell — know the blast radius.

## Common mistakes

- Using exit inside sourced files unexpectedly
- Global variables everywhere
- Swallowing errors with `|| true` habitually

## Exercises

Work in `exercises/15-bash-functions-args/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/15-bash-functions-args/` until you have an honest failing attempt.**

## Self-check

1. How require at least one arg?
2. local keyword purpose?
3. When source vs execute?

## Further reading

- https://mywiki.wooledge.org/BashFAQ

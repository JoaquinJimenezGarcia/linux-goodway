---
title: "16. Testing Shell Scripts and Safe Automation"
---

# 16. Testing Shell Scripts and Safe Automation

**Phase:** Phase 5 — Shell scripting  
**Estimated time:** 1–2 days  
**Slug:** `16-bash-testing`

## Learning objectives

- Structure scripts for testability
- Write simple assert helpers
- Use dry-run flags
- Avoid destructive defaults

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

## Testable design

- Put logic in functions
- Keep side effects at the edges
- Support `--dry-run`

```bash
assert_eq() {
  [[ "$1" == "$2" ]] || { echo "want $2 got $1" >&2; exit 1; }
}
```

This course uses small `test.sh` harnesses — same idea as unit tests.

## Safety

Never make `rm -rf $VAR/` if VAR can be empty. Guard:

```bash
[[ -n "${DIR:-}" ]] || exit 1
```

## Common mistakes

- Empty-variable rm -rf disasters
- Untested sed -i in prod
- Scripts that only work interactively

## Exercises

Work in `exercises/16-bash-testing/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/16-bash-testing/` until you have an honest failing attempt.**

## Self-check

1. What is a dry-run?
2. Why guard empty paths?
3. How assert equality in bash?

## Further reading

- https://www.shellcheck.net/

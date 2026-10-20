---
title: "14. Bash Scripting Fundamentals"
---

# 14. Bash Scripting Fundamentals

**Phase:** Phase 5 — Shell scripting  
**Estimated time:** 2 days  
**Slug:** `14-bash-scripting-intro`

## Learning objectives

- Write scripts with shebang and set -euo pipefail
- Use variables, quotes, and arrays basics
- Write if/for/while
- Make scripts executable and reusable

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

## Script skeleton

```bash
#!/usr/bin/env bash
set -euo pipefail

name="${1:-world}"
echo "Hello, ${name}"
```

## Quoting

- `"$var"` — expand but keep spaces together
- `'$var'` — literal
- Always quote expansions unless you intentionally word-split

## Conditionals and loops

```bash
if [[ -f "$file" ]]; then
  echo "exists"
fi

for f in *.txt; do
  echo "$f"
done
```

Prefer `[[ ]]` over legacy `[ ]` in bash.

## Common mistakes

- Unquoted variables causing word-splitting bugs
- Omitting set -e and missing failures
- Parsing ls in scripts

## Exercises

Work in `exercises/14-bash-scripting-intro/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/14-bash-scripting-intro/` until you have an honest failing attempt.**

## Self-check

1. What does set -euo pipefail do?
2. Why quote "$var"?
3. Shebang purpose?

## Further reading

- https://mywiki.wooledge.org/BashGuide

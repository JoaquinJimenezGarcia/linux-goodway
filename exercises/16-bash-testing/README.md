# Exercise: 16. Testing Shell Scripts and Safe Automation

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- Structure scripts for testability
- Write simple assert helpers
- Use dry-run flags
- Avoid destructive defaults

## Task

Implement safe_dir_or_die in exercise.sh. It takes one argument, the directory name. If the argument is missing or an empty string, the function must return 1 (you may write an error to stderr but print nothing to stdout). Otherwise it must print the argument unchanged on stdout and return 0. Do not check whether the directory exists; this exercise only guards against empty input. Quote the variable everywhere. Run ./test.sh, then try the function in a script that uses set -u to confirm it never touches an unset variable.

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/16-bash-testing/` | Reference only **after** a real attempt |

## Examples / expected behavior

safe_dir_or_die /tmp       -> prints: /tmp          status 0
safe_dir_or_die "my dir"   -> prints: my dir        status 0
safe_dir_or_die ""         -> prints nothing        status 1
safe_dir_or_die            -> prints nothing        status 1

Typical use: target=$(safe_dir_or_die "$1") || exit 1

With set -u a plain $1 on an empty call aborts the script, so the ${1:-} default inside the function is what makes the guard safe. A caller can combine it with the strict form: d=$(safe_dir_or_die "$1") || exit 1; rm -rf -- "${d:?}"/old.

## How to work

1. Skim this README, then re-open `lessons/16-bash-testing/lesson.md` (or the PDF).
2. Run `./test.sh` once to see what fails — failures are a checklist.
3. Implement one function at a time; re-run tests after each change.
4. When stuck, re-run the **lab commands** from the lesson on a real shell and compare.
5. After all tests pass: explain each function out loud in one sentence.

## Hints

- Prefer the simplest correct shell that matches the lesson vocabulary.
- Quote variables; check exit codes the way the lesson showed.
- If output has extra spaces/newlines, trim with the same patterns used in the lesson.

## Done when

- `./test.sh` prints all passes and exits 0
- You can redo the exercise tomorrow without looking at your first solution

**Do not open the solutions folder until you have struggled for a real attempt (15+ minutes).**

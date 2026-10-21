# Exercise: 15. Functions, Arguments, and Exit Codes in Scripts

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- Define functions and local variables
- Validate arguments
- Return meaningful exit codes
- Source libraries carefully

## Task

Implement require_one_arg in exercise.sh. If the function receives at least one argument it must print the word ok and return 0. If it receives no arguments it must return 2 and should not print ok. You may print a usage message to stderr (use >&2) but nothing on stdout in the failure case. Count arguments with `$#` and compare numerically with `[ "$#" -ge 1 ]`. Use return, not exit, so the sourcing shell is not killed. After ./test.sh passes, call the function by hand and read $? right after each call.

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/15-bash-functions-args/` | Reference only **after** a real attempt |

## Examples / expected behavior

require_one_arg foo        -> prints: ok      status 0
require_one_arg a b c      -> prints: ok      status 0
require_one_arg            -> prints nothing  status 2
require_one_arg ""         -> prints: ok      status 0  (one argument, even if empty)

Check the status immediately: require_one_arg; echo "rc=$?" shows rc=2.

In a script: if require_one_arg "$1" >/dev/null; then echo proceed; else echo usage; fi
Capture: msg=$(require_one_arg x) gives msg=ok. Exit codes: 0 success, 2 means bad usage by convention. Remember return ends the function, exit ends the whole script.

## How to work

1. Skim this README, then re-open `lessons/15-bash-functions-args/lesson.md` (or the PDF).
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

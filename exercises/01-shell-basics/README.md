# Exercise: 01. The Shell: Prompts, Commands, Arguments, Exit Codes

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- Run commands with arguments and flags
- Read exit codes (`$?`) and why they matter
- Use `--help` / man pages productively
- Distinguish absolute vs relative paths

## Task

Implement two small functions. success_code() returns the exit code that conventionally means a command succeeded. failure_code() returns a typical generic failure exit code. Both return integers, not strings. success_code must be 0. failure_code must be a non-zero integer in the range 1..255; use 1, the general error code used by shell builtins and most tools. No arguments and no side effects are needed. The exercise checks that you know the convention behind "0 is success, non-zero is failure" that the shell relies on for && and ||.

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/01-shell-basics/` | Reference only **after** a real attempt |

## Examples / expected behavior

success_code() -> 0
failure_code() -> 1

Shell equivalents:
true; echo $?     prints 0
false; echo $?    prints 1

A test may check: success_code() == 0 and 1 <= failure_code() <= 255.
Both values are ints, so success_code() == "0" would be False.
Rule used by the shell: "cmd1 && cmd2" runs cmd2 only when cmd1 returned 0;
"cmd1 || cmd2" runs cmd2 only when cmd1 returned non-zero.

## How to work

1. Skim this README, then re-open `lessons/01-shell-basics/lesson.md` (or the PDF).
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

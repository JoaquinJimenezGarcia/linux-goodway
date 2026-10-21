# Exercise: 11. Processes: ps, top, /proc, signals

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- List and interpret processes
- Read process state from /proc
- Send signals with kill
- Understand PID, PPID, zombie/orphan concepts

## Task

Implement signal_num(name). The input is a signal name as a string, with or without the "SIG" prefix and in any letter case, for example "TERM", "SIGKILL" or "int". Return the standard Linux signal number as an int: HUP=1, INT=2, QUIT=3, KILL=9, TERM=15. Specifically TERM must return 15 and KILL must return 9. For any other name return -1. Strip surrounding whitespace first. These numbers are the same ones printed by kill -l NAME, and they help you read exit statuses such as 137 (128 + 9) and 143 (128 + 15).

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/11-processes/` | Reference only **after** a real attempt |

## Examples / expected behavior

signal_num("TERM") -> 15
signal_num("SIGTERM") -> 15
signal_num("KILL") -> 9
signal_num("sigkill") -> 9
signal_num("INT") -> 2
signal_num("HUP") -> 1
signal_num("FOO") -> -1

Shell: kill -l TERM prints 15, kill -l KILL prints 9.
Exit status 143 means the process ended by SIGTERM (128+15).
signal_num("  term ") -> 15   (whitespace and case are ignored)
signal_num("") -> -1

## How to work

1. Skim this README, then re-open `lessons/11-processes/lesson.md` (or the PDF).
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

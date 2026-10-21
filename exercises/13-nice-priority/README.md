# Exercise: 13. Priority, nice, and resource limits (ulimit)

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- Adjust niceness
- Inspect ulimit
- Explain why limits exist
- Connect to cgroups at a high level

## Task

Implement higher_nice_means(). It takes no arguments and returns the short string "lower-priority", describing what a higher niceness value means for a process: the process is nicer to others, so the scheduler gives it a smaller share of CPU time when there is contention. Return exactly "lower-priority" in lowercase with a hyphen. Niceness ranges from -20 (highest priority) to 19 (lowest priority), the default is 0, and only root may decrease a niceness value. This is the key idea behind nice and renice.

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/13-nice-priority/` | Reference only **after** a real attempt |

## Examples / expected behavior

higher_nice_means() -> "lower-priority"

Examples in the shell:
nice -n 10 backup.sh      runs with lower priority than default
renice -n 19 -p 4321      make PID 4321 the politest process
nice -n -5 cmd            needs root: higher priority

Niceness 19 -> lowest priority, niceness -20 -> highest priority.

## How to work

1. Skim this README, then re-open `lessons/13-nice-priority/lesson.md` (or the PDF).
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

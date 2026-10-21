# Exercise: 29. Performance Basics: CPU, memory, iowait, OOM

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- Read load average correctly
- Spot memory pressure and OOM
- Distinguish CPU-bound vs IO-bound
- Use vmstat/iostat at a basic level

## Task

Implement `load_busy CPUS LOAD` in `exercise.sh`. It must print `yes`
when the load average is strictly greater than the CPU count and `no`
otherwise (equal means not busy). Load values can be decimals such as 2.5,
so use `awk` rather than shell integer math. Run `./test.sh`, then try your
function with the real values from `nproc` and `uptime` on your machine. Keep the function body to one line; the goal is recall of the lesson vocabulary, not cleverness. Finish by re-reading the Decision guide table and noting one failure mode you could have caused yourself.

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/29-perf-basics/` | Reference only **after** a real attempt |

## Examples / expected behavior

Expected behavior:

```
$ load_busy 2 4
yes
$ load_busy 4 1
no
$ load_busy 4 4
no
$ load_busy 2 2.5
yes
```

Hint: `awk -v c="$1" -v l="$2" 'BEGIN{print (l>c)?"yes":"no"}'` compares
numbers, not strings, because of the `-v` numeric strings.

Self-check: run `bash -c 'source exercise.sh; load_busy 2 4'` from the exercise directory (replace load_busy 2 4 with your function name) and compare by eye, then run `./test.sh`. Also confirm there is no trailing whitespace in the output.

## How to work

1. Skim this README, then re-open `lessons/29-perf-basics/lesson.md` (or the PDF).
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

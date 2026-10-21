# Exercise: 35. Docker Basics on Linux

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- Run containers interactively
- Understand images vs containers
- Mount volumes and publish ports
- Read container logs

## Task

Implement `docker_rm_flag_meaning` in `exercise.sh` so it prints a short
hyphenated phrase describing what `docker run --rm` does when the
container's main process ends. Use the exact phrase from the lesson, all
lowercase with hyphens. Once the test passes, run the `keep` versus `gone`
experiment from the Worked examples on a machine with Docker and write down
which container remained and why. Keep the function body to one line; the goal is recall of the lesson vocabulary, not cleverness. Finish by re-reading the Decision guide table and noting one failure mode you could have caused yourself.

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/35-docker-basics/` | Reference only **after** a real attempt |

## Examples / expected behavior

Expected behavior:

```
$ docker_rm_flag_meaning
remove-on-exit
```

What the real flag does:

```
$ docker run --rm alpine echo hi
hi
$ docker ps -a
(no exited alpine container is listed)
```

Do not print `delete`, `remove on exit` with spaces, or the flag itself; the
test compares to `remove-on-exit` exactly.

Self-check: run `bash -c 'source exercise.sh; docker_rm_flag_meaning'` from the exercise directory (replace docker_rm_flag_meaning with your function name) and compare by eye, then run `./test.sh`. Also confirm there is no trailing whitespace in the output.

## How to work

1. Skim this README, then re-open `lessons/35-docker-basics/lesson.md` (or the PDF).
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

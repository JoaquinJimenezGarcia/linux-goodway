# Exercise: 32. Capabilities, seccomp, and least privilege (intro)

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- Explain Linux capabilities vs all-powerful root
- Know seccomp exists for syscall filtering
- Apply least privilege to services
- Relate to container security defaults

## Task

Implement `avoid_docker_flag` in `exercise.sh` so it prints the single
Docker run flag that grants a container nearly all host privileges and
disables most sandboxing. Print the long option exactly as typed on the
command line, including both leading dashes. When the test passes, write one
paragraph in your notes explaining what safer pair of flags (drop and add)
you would use instead and why the flag you printed is dangerous.

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/32-capabilities-seccomp/` | Reference only **after** a real attempt |

## Examples / expected behavior

Expected behavior:

```
$ avoid_docker_flag
--privileged
```

Safer pattern to remember (not part of the test):

```
docker run --cap-drop ALL --cap-add NET_BIND_SERVICE \
  --security-opt no-new-privileges IMAGE
```

The test compares the exact string, so do not add quotes, a trailing space,
or the word docker.

Self-check: run `bash -c 'source exercise.sh; avoid_docker_flag'` from the exercise directory (replace avoid_docker_flag with your function name) and compare by eye, then run `./test.sh`. Also confirm there is no trailing whitespace in the output.

## How to work

1. Skim this README, then re-open `lessons/32-capabilities-seccomp/lesson.md` (or the PDF).
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

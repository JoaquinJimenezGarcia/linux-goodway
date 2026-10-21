# Exercise: 45. Linux for AI Infrastructure

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- Prepare GPU hosts at OS level (drivers/toolkit conceptually)
- Tune file limits and disk for datasets
- Isolate model servers with systemd/cgroups
- Observe GPU and host metrics

## Task

Open `exercise.sh` and implement `inference_limit_knob`. It prints the name
of the one resource-limit knob, written exactly as the lowercase `ulimit`
resource name, that a busy inference server most commonly exhausts first
because it holds many sockets and files. Print only that word. The test does
not touch the system. After it passes, perform mini-lab steps 1 to 5 and keep
the output of `grep 'open files' /proc/PID/limits` in your notes. Then write
the systemd directive that raises the same limit for a service and say why
`limits.conf` alone does not change it for services.

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/45-ai-infra-linux/` | Reference only **after** a real attempt |

## Examples / expected behavior

Run from the exercise folder:

    source ./exercise.sh
    inference_limit_knob

Expected single line of output:

    nofile

Related lab checks (not graded):

    ulimit -n
    1024
    grep 'open files' /proc/self/limits
    Max open files            1024                 1048576              files

systemd directive for the same knob: LimitNOFILE=65536 inside [Service].

## How to work

1. Skim this README, then re-open `lessons/45-ai-infra-linux/lesson.md` (or the PDF).
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

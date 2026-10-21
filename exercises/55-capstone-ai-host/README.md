# Exercise: 55. Capstone: AI Inference Host on Linux

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- Run an inference-friendly Linux host layout
- systemd + reverse proxy + TLS
- Resource limits and logs
- Load test and observe

## Task

Open `exercise.sh` and implement `graceful_stop_signal`. It prints the name
of the signal, written in uppercase without the `SIG` prefix, that systemd and
`kill` send by default to ask a service to shut down cleanly so it can drain
in-flight work. One line only. After it passes, finish the capstone: build
the mock model server with a handler for that signal, set limits in the unit,
and prove with logs that a stop during load lets requests complete. Compare
with `kill -KILL` and note the difference. Record limits shown by
`systemctl show` and the firewall ports you allow.

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/55-capstone-ai-host/` | Reference only **after** a real attempt |

## Examples / expected behavior

Run from the exercise folder:

    source ./exercise.sh
    graceful_stop_signal

Expected single line of output:

    TERM

Related lab check (not graded):

    sudo systemctl stop model
    journalctl -u model -n 3 --no-pager
    model[812]: TERM received, draining
    model[812]: clean exit
    systemd[1]: Stopped Mock model API.

KILL cannot be caught; seeing no drain message means the app was killed.

## How to work

1. Skim this README, then re-open `lessons/55-capstone-ai-host/lesson.md` (or the PDF).
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

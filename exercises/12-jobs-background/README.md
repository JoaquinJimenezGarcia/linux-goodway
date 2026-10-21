# Exercise: 12. Jobs, Background, nohup, screen/tmux intro

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- Run jobs in background
- Use fg/bg/jobs
- Keep sessions with tmux
- Apply nohup carefully

## Task

Implement tmux_detach_keys(). It takes no arguments and returns the default key sequence used to detach from a tmux session, as the lowercase string "ctrl-b d". That means pressing Ctrl-b (the tmux prefix), releasing it, and then pressing d. The session and everything running in it continue in the background; you can come back later with "tmux attach -t NAME". Return exactly that text: lowercase, a hyphen in ctrl-b, and a single space before d. Do not return the tmux command line (like "tmux detach"), only the keystroke description.

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/12-jobs-background/` | Reference only **after** a real attempt |

## Examples / expected behavior

tmux_detach_keys() -> "ctrl-b d"

Workflow:
tmux new -s work       start a session
(press ctrl-b d)       detach, programs keep running
tmux ls                work: 1 windows ...
tmux attach -t work    return to the session

The returned value is 8 characters long.
The result is lowercase text, not the tmux command "tmux detach".
Other tmux keys use the same prefix: ctrl-b c makes a new window.

## How to work

1. Skim this README, then re-open `lessons/12-jobs-background/lesson.md` (or the PDF).
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

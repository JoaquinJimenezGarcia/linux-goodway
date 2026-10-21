# Exercise: 54. Capstone: Broken Box Challenge

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- Debug a deliberately broken VM
- Capture timeline and root cause
- Fix with minimal change
- Write postmortem

## Task

Open `exercise.sh` and implement `postmortem_required_section`. It prints
the name of the one postmortem section the lesson calls mandatory because it
explains the underlying reason an incident happened, not just the symptom or
trigger. Output is lowercase, hyphenated, one line, no extra text. After it
passes, run the capstone: break three things in a snapshot, fix them one at a
time with evidence, and write the postmortem with all five sections. Use at
least three "why" steps for each fault and list prevention items with an owner
and a date. Keep the timeline file you started at the first minute.

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/54-capstone-troubleshoot/` | Reference only **after** a real attempt |

## Examples / expected behavior

Run from the exercise folder:

    source ./exercise.sh
    postmortem_required_section

Expected single line of output:

    root-cause

Example "why" chain (not graded):

    503 errors            <- app cannot write state
    cannot write state    <- disk 100 percent full
    disk full             <- logs not rotated since the config edit
    root cause            -> rotation disabled, and no disk alert existed

A root cause names a missing guardrail you can fix, not a person.

## How to work

1. Skim this README, then re-open `lessons/54-capstone-troubleshoot/lesson.md` (or the PDF).
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

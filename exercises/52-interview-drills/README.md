# Exercise: 52. Linux Interview and Oncall Drills

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- Explain debugging aloud with structure
- Solve timed scenarios
- Write clear handoff notes
- Prioritize user impact

## Task

Open `exercise.sh` and implement `incident_first_10m`. It prints a single
hyphenated token that summarizes, in three ordered verbs or nouns, what to do
in the first ten minutes of an incident before proposing a fix. Use lowercase
and hyphens only, one line, no spaces. After it passes, run a timed drill from
the lesson: choose a scenario, write the one-sentence problem, list scope
questions, and run only read-only commands. Save the transcript and a
handoff note in the format shown in Example 5. Rate yourself from 1 to 5 on
structure, evidence, communication, and verification.

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/52-interview-drills/` | Reference only **after** a real attempt |

## Examples / expected behavior

Run from the exercise folder:

    source ./exercise.sh
    incident_first_10m

Expected single line of output:

    define-scope-gather-evidence

Related drill output (not graded), a good first-minute transcript:

    $ uptime
     02:11:05 up 41 days, load average: 9.12, 8.80, 7.40
    $ nproc
    4

Load of 9 on 4 CPUs is saturation evidence; now find what is waiting.

## How to work

1. Skim this README, then re-open `lessons/52-interview-drills/lesson.md` (or the PDF).
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

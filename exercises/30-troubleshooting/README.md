# Exercise: 30. Troubleshooting Method: REDUCE and Bisect

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- Apply a systematic troubleshooting loop
- Capture evidence before rebooting
- Bisect recent changes
- Write short incident notes

## Task

Implement `first_troubleshooting_step` in `exercise.sh` so it prints the
name of the very first step in the method from this lesson. Use the
exact hyphenated token from the table (lowercase, with a hyphen, no spaces).
Run `./test.sh` until green. Then write the six steps from memory in your
notes and apply them to one real problem you have had recently. Keep the function body to one line; the goal is recall of the lesson vocabulary, not cleverness. Finish by re-reading the Decision guide table and noting one failure mode you could have caused yourself.

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/30-troubleshooting/` | Reference only **after** a real attempt |

## Examples / expected behavior

Expected behavior:

```
$ first_troubleshooting_step
define-symptom
```

Not accepted: `Define symptom`, `define_symptom`, `gather`, or `restart`.
The test compares the output exactly, so no extra spaces or newline tricks.

Self-check: run `bash -c 'source exercise.sh; first_troubleshooting_step'` from the exercise directory (replace first_troubleshooting_step with your function name) and compare by eye, then run `./test.sh`. Also confirm there is no trailing whitespace in the output.

## How to work

1. Skim this README, then re-open `lessons/30-troubleshooting/lesson.md` (or the PDF).
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

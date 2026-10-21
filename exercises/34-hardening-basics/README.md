# Exercise: 34. Host Hardening Checklist

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- Apply a practical hardening baseline
- Disable unused services
- Enforce SSH key auth
- Keep patching cadence

## Task

Implement `count_baseline_items` in `exercise.sh` so it prints the
number of items in the hardening baseline from this lesson: ssh-keys,
firewall, updates, sudo, and ntp. Print just the number, no words. Do the
counting in your head from the table, not from the host. Afterwards, write
a one-line check for each item on your own VM and record which ones fail. Keep the function body to one line; the goal is recall of the lesson vocabulary, not cleverness. Finish by re-reading the Decision guide table and noting one failure mode you could have caused yourself.

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/34-hardening-basics/` | Reference only **after** a real attempt |

## Examples / expected behavior

Expected behavior:

```
$ count_baseline_items
5
```

The five items, in lesson order:

```
1 ssh-keys   2 firewall   3 updates   4 sudo   5 ntp
```

The test expects exactly the digit `5`. Printing `5 items` or `five` fails.
You may optionally verify by counting the words in a list with `wc -w`.

Self-check: run `bash -c 'source exercise.sh; count_baseline_items'` from the exercise directory (replace count_baseline_items with your function name) and compare by eye, then run `./test.sh`. Also confirm there is no trailing whitespace in the output.

## How to work

1. Skim this README, then re-open `lessons/34-hardening-basics/lesson.md` (or the PDF).
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

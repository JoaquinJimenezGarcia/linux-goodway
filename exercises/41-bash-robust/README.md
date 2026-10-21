# Exercise: 41. Robust Bash: errexit, nounset, traps

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- Use traps for cleanup
- Handle signals in scripts
- Create temp dirs safely
- Write scripts that fail loudly

## Task

Implement `cleanup_phrase` in `exercise.sh` so it prints the two-word
Bash idiom that guarantees a cleanup handler runs when a script ends by any
route. Print the exact phrase with a single space, no punctuation, and the
signal name in capital letters. Then write a short script that creates a
temp file, fails with `false`, and use `trap` so the temp file is removed;
verify it is gone afterwards. Keep the function body to one line; the goal is recall of the lesson vocabulary, not cleverness. Finish by re-reading the Decision guide table and noting one failure mode you could have caused yourself.

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/41-bash-robust/` | Reference only **after** a real attempt |

## Examples / expected behavior

Expected behavior:

```
$ cleanup_phrase
trap EXIT
```

Idiom in context:

```
tmp=$(mktemp)
trap 'rm -f "$tmp"' EXIT
```

The test compares the exact string `trap EXIT`. Writing `trap exit`, `EXIT trap`,
or including a command after it will fail.

Self-check: run `bash -c 'source exercise.sh; cleanup_phrase'` from the exercise directory (replace cleanup_phrase with your function name) and compare by eye, then run `./test.sh`. Also confirm there is no trailing whitespace in the output.

## How to work

1. Skim this README, then re-open `lessons/41-bash-robust/lesson.md` (or the PDF).
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

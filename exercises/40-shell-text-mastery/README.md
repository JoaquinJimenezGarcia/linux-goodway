# Exercise: 40. Shell Text Mastery Drill Week

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- Combine grep/sed/awk/sort/uniq fluently
- Write one-liners you can explain line-by-line
- Profile slow pipelines
- Prefer clarity over golf

## Task

Implement `top_token` in `exercise.sh`. It reads tokens from standard input,
one per line, and prints only the most frequent token. Use the recipe from
the lesson: sort, count with `uniq -c`, sort by count descending, then
print the token column. Do not print the count. For ties, whichever token
comes first after the numeric sort is acceptable. Test with piped input using
`printf`, as `test.sh` does. Keep the function body to one line; the goal is recall of the lesson vocabulary, not cleverness. Finish by re-reading the Decision guide table and noting one failure mode you could have caused yourself.

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/40-shell-text-mastery/` | Reference only **after** a real attempt |

## Examples / expected behavior

Expected behavior:

```
$ printf 'a\nb\na\n' | top_token
a
$ printf 'x\nx\ny\nz\nz\nz\n' | top_token
z
```

Intermediate stage, to help you debug:

```
$ printf 'a\nb\na\n' | sort | uniq -c | sort -nr
      2 a
      1 b
```

Hint: `awk 'NR==1{print $2}'` extracts the second column from the first line.

Self-check: run `bash -c 'source exercise.sh; top_token'` from the exercise directory (replace top_token with your function name) and compare by eye, then run `./test.sh`. Also confirm there is no trailing whitespace in the output.

## How to work

1. Skim this README, then re-open `lessons/40-shell-text-mastery/lesson.md` (or the PDF).
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

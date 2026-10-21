# Exercise: 07. Pipes, Redirection, and Exit Status in Pipelines

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- Redirect stdout/stderr to files
- Connect commands with pipes
- Use tee, here-docs, and process substitution ideas
- Understand pipeline exit status (`pipefail`)

## Task

Implement count_lines(text). It receives the full stdin content as one string and returns the number of lines as an int, behaving like wc -l applied to a stream. A line is counted for each newline-terminated line; but if the text is non-empty and does not end with a newline, the last partial line should still be counted (a friendlier variant than wc, which counts only newline characters). An empty string has 0 lines. A string that is only "\n" has 1 line. Do not read files or the real stdin; only use the argument. Blank lines count as lines.

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/07-pipes-redirects/` | Reference only **after** a real attempt |

## Examples / expected behavior

count_lines("") -> 0
count_lines("a\n") -> 1
count_lines("a\nb\nc\n") -> 3
count_lines("a\nb") -> 2      (last line has no newline)
count_lines("\n\n") -> 2      (two blank lines)
count_lines("one line only") -> 1

Shell equivalent: printf 'a\nb\nc\n' | wc -l prints 3.
Blank lines count: count_lines("a\n\nb\n") -> 3.
Windows line endings are not special; only the newline character splits.

## How to work

1. Skim this README, then re-open `lessons/07-pipes-redirects/lesson.md` (or the PDF).
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

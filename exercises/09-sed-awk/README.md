# Exercise: 09. sed and awk for Text Engineering

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- Perform common sed substitutions
- Use awk for column processing
- Choose the right tool (cut/sort/uniq vs awk)
- Write small one-liners you can explain

## Task

Implement sum_field2(text). The input is multi-line text where each line has whitespace-separated fields. Return the sum of the second field ($2 in awk) across all lines, as a number (int when all values are integers is fine, or float). Lines with fewer than two fields are skipped, as are lines whose second field is not a number (like a header). Blank lines are skipped. An empty input gives 0. This is the Python equivalent of awk '{s += $2} END {print s}' with a little extra safety for headers and short lines.

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/09-sed-awk/` | Reference only **after** a real attempt |

## Examples / expected behavior

sum_field2("a 10\nb 20\nc 5\n") -> 35
sum_field2("x 1.5\ny 2.5\n") -> 4.0
sum_field2("name qty\napple 3\npear 5\n") -> 8   (header skipped)
sum_field2("onlyone\nb 7\n") -> 7
sum_field2("") -> 0
sum_field2("a    4\n\nb\t6\n") -> 10   (extra spaces and tabs ok)

Shell: awk '{s+=$2} END{print s}' file
sum_field2("a 1\nb notnum\nc 2\n") -> 3   (non-numeric field is skipped)
sum_field2("a -4\nb 10\n") -> 6   (negative numbers are allowed)

## How to work

1. Skim this README, then re-open `lessons/09-sed-awk/lesson.md` (or the PDF).
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

# Exercise: 08. grep, ripgrep mindset, and find

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- Search file contents with grep
- Find files by name/type/time with find
- Combine find -exec / xargs safely
- Avoid unsafe parsing of filenames with spaces

## Task

Implement match_todo(line). It takes one line of text and returns True if the line contains the marker TODO as a whole word, uppercase exactly, and False otherwise. "TODO: fix" and "# TODO fix this" match; "todo" in lower case does not, and neither do words that merely contain the letters such as "TODOS" or "AUTODOC". Word boundaries mean the characters on each side of TODO are not letters, digits or underscores (start/end of line counts as a boundary). This mimics grep -w TODO and is a good use of a small regular expression.

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/08-grep-find/` | Reference only **after** a real attempt |

## Examples / expected behavior

match_todo("TODO: fix") -> True
match_todo("# TODO fix this") -> True
match_todo("x = 1  // TODO") -> True
match_todo("todo later") -> False
match_todo("TODOS list") -> False
match_todo("AUTODOC") -> False
match_todo("") -> False
match_todo("(TODO)") -> True

Shell equivalent: grep -w TODO file
match_todo("TODO") -> True    (whole line is the marker)
match_todo("TODO_ITEM") -> False   (underscore is a word character)

## How to work

1. Skim this README, then re-open `lessons/08-grep-find/lesson.md` (or the PDF).
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

# Exercise: 00. Orientation: What Linux Is and How to Practice

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- Explain Linux vs Unix vs GNU userland at a beginner level
- Choose a practice environment (VM, cloud, WSL, or container)
- Open a shell and run your first commands safely
- Adopt the study method: attempt → struggle → solution → rewrite

## Task

Implement greet(name). It takes a single string NAME and returns the greeting text "Hello, NAME!" exactly, with a comma, one space and an exclamation mark at the end. Do not print extra whitespace or a trailing newline inside the returned value. If NAME is an empty string, return "Hello, world!" instead. Keep the function pure: no input from the keyboard, no file access. This mirrors what a shell function would do with echo "Hello, $1!" and warms you up for editing and running scripts.

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/00-orientation/` | Reference only **after** a real attempt |

## Examples / expected behavior

greet("Ada") -> "Hello, Ada!"
greet("Linus") -> "Hello, Linus!"
greet("world") -> "Hello, world!"
greet("") -> "Hello, world!"
greet("Mary Ann") -> "Hello, Mary Ann!"

The returned text has no leading or trailing spaces and no newline character.
Typical use: greet("Ada") is printed by the caller, which adds its own newline.
The name is inserted as given; do not change its letter case.

## How to work

1. Skim this README, then re-open `lessons/00-orientation/lesson.md` (or the PDF).
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

# Exercise: 14. Bash Scripting Fundamentals

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- Write scripts with shebang and set -euo pipefail
- Use variables, quotes, and arrays basics
- Write if/for/while
- Make scripts executable and reusable

## Task

Open exercise.sh and finish the hello function. It must print exactly "Hello, <name>" on one line, using the first argument as the name. When no argument is given (or it is empty), the name must be "world". Keep the local name variable that is already there and use the ${1:-world} default style from the lesson. Quote the variable when you print it, so a name with spaces such as "Ada Lovelace" is kept intact. Do not print anything else: no extra spaces, no trailing text. Run ./test.sh until every check passes, then run the function by hand with no argument, one argument, and a two-word quoted argument.

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/14-bash-scripting-intro/` | Reference only **after** a real attempt |

## Examples / expected behavior

hello            -> Hello, world
hello Ada        -> Hello, Ada
hello "Ada L"    -> Hello, Ada L
hello ""         -> Hello, world

Only one line of output per call, ending with a newline. The function returns 0. The text is exactly "Hello, " followed by the name, with a comma and one space.

Try also: ./hello.sh with no file mode set -> use bash hello.sh. Syntax check: bash -n hello.sh prints nothing when fine. Trace: bash -x hello.sh Ada shows + name=Ada then + echo 'Hello, Ada'.

## How to work

1. Skim this README, then re-open `lessons/14-bash-scripting-intro/lesson.md` (or the PDF).
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

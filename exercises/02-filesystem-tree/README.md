# Exercise: 02. The Filesystem Tree: /, /etc, /var, /home, /proc

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- Navigate with cd, pwd, ls
- Explain key FHS directories
- Create, move, copy, remove files carefully
- Use tab completion and wildcards

## Task

Implement abs_join(base, rel). Both arguments are strings. base is an absolute POSIX path such as "/var/log". Return a single absolute path made of base and rel joined by exactly one slash, with no duplicate slashes. If rel itself starts with "/", return rel unchanged because an absolute path overrides the base. Treat "/" as base correctly: abs_join("/", "etc") is "/etc". Do not touch the real filesystem and do not resolve "." or ".." segments; just join cleanly. Trailing slashes on base must not produce "//".

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/02-filesystem-tree/` | Reference only **after** a real attempt |

## Examples / expected behavior

abs_join("/var", "log") -> "/var/log"
abs_join("/var/", "log") -> "/var/log"
abs_join("/", "etc") -> "/etc"
abs_join("/home/student", "docs/a.txt") -> "/home/student/docs/a.txt"
abs_join("/var/log", "/etc/hosts") -> "/etc/hosts"

Edge: abs_join("/usr//", "bin") -> "/usr/bin"  (extra trailing slashes removed).

## How to work

1. Skim this README, then re-open `lessons/02-filesystem-tree/lesson.md` (or the PDF).
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

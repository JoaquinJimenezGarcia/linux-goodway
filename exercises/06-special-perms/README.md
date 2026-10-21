# Exercise: 06. Special Bits: setuid, setgid, sticky

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- Explain setuid/setgid/sticky bit purposes
- Recognize them in `ls -l`
- Know security risks of setuid binaries
- Use sticky on shared directories like /tmp

## Task

Implement describe_sticky(mode). The input is a string, either an octal mode with four digits like "1777" or a symbolic string like "drwxrwxrwt". Decide whether the sticky bit is set. If it is set, return the string "owner-delete-only", describing its effect on a directory: only the owner of an entry (or the directory owner or root) may delete or rename it. If the sticky bit is not set, return "normal". In octal the sticky bit is the 1 in the leading digit of four digits; in symbolic form it is a "t" or "T" as the last character of the mode.

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/06-special-perms/` | Reference only **after** a real attempt |

## Examples / expected behavior

describe_sticky("1777") -> "owner-delete-only"
describe_sticky("0755") -> "normal"
describe_sticky("drwxrwxrwt") -> "owner-delete-only"
describe_sticky("drwxrwxrwx") -> "normal"
describe_sticky("drwxr-xr-T") -> "owner-delete-only"
describe_sticky("2775") -> "normal"   (setgid only, no sticky)
describe_sticky("3775") -> "owner-delete-only"  (setgid + sticky)

## How to work

1. Skim this README, then re-open `lessons/06-special-perms/lesson.md` (or the PDF).
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

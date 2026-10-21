# Exercise: 04. Permissions Basics: rwx, chmod, chown

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- Read `ls -l` permission bits
- Change mode with chmod (symbolic and octal)
- Change owner/group with chown/chgrp
- Predict access for user/group/other

## Task

Implement octal_to_human(mode). The input is a three-digit octal permission string such as "755" or "640" (digits 0-7). Return the nine-character symbolic form without the file-type character, like "rwxr-xr-x". Each digit expands to three characters: 4 gives r, 2 gives w, 1 gives x, and missing bits are "-". Digits are in order user, group, others. Do not use the filesystem. You may assume the input is valid three digits; for anything else return an empty string. This is the same mapping chmod and ls -l use.

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/04-permissions-basics/` | Reference only **after** a real attempt |

## Examples / expected behavior

octal_to_human("755") -> "rwxr-xr-x"
octal_to_human("644") -> "rw-r--r--"
octal_to_human("600") -> "rw-------"
octal_to_human("777") -> "rwxrwxrwx"
octal_to_human("000") -> "---------"
octal_to_human("640") -> "rw-r-----"
octal_to_human("12") -> ""   (not three digits)
octal_to_human("789") -> ""   (8 and 9 are not octal digits)
Check: chmod 750 f then ls -l f shows -rwxr-x---, i.e. "rwxr-x---".

## How to work

1. Skim this README, then re-open `lessons/04-permissions-basics/lesson.md` (or the PDF).
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

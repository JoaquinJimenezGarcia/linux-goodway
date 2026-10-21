# Exercise: 05. Users, Groups, sudo, and /etc/passwd

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- Explain passwd/shadow/group files at a high level
- Use id, whoami, groups
- Apply least-privilege with sudo
- Create users/groups on a lab system (carefully)

## Task

Implement parse_uid(id_output). The input is a single line produced by the id command, for example "uid=1000(student) gid=1000(student) groups=1000(student),27(sudo)". Return the numeric user id as an int, taken from the "uid=" field (the digits right after "uid=", before the parenthesis or space). Ignore gid and groups. If there is no uid= field, return -1. The input may have leading or trailing whitespace. This is the same extraction you would do with grep -o or cut in a script.

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/05-users-groups/` | Reference only **after** a real attempt |

## Examples / expected behavior

parse_uid("uid=1000(student) gid=1000(student) groups=1000(student),27(sudo)") -> 1000
parse_uid("uid=0(root) gid=0(root) groups=0(root)") -> 0
parse_uid("  uid=33(www-data) gid=33(www-data) groups=33(www-data)  ") -> 33
parse_uid("gid=1000(student)") -> -1
parse_uid("") -> -1

Note: the result is an int, not a string.

## How to work

1. Skim this README, then re-open `lessons/05-users-groups/lesson.md` (or the PDF).
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

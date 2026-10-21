# Exercise: 50. systemd Service Hardening Directives

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- Apply ProtectSystem/NoNewPrivileges ideas
- Constrain WritablePaths
- Run as dedicated DynamicUser/User
- Read systemd-analyze security

## Task

Open `exercise.sh` and implement `nonewprivileges_directive`. It prints the
exact systemd unit-file line, including the directive name, an equals sign, and
the value, that stops a service and its children from gaining privileges
through setuid or capabilities. Case matters because systemd directives are
case sensitive. Print one line, nothing else. After it passes, apply the
directive to a throwaway unit in your lab VM and verify with
`systemctl show UNIT -p NoNewPrivileges`. Record the before and after exposure
from `systemd-analyze security` and list one thing that stopped working when
you added `ProtectSystem=strict`.

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/50-systemd-hardening/` | Reference only **after** a real attempt |

## Examples / expected behavior

Run from the exercise folder:

    source ./exercise.sh
    nonewprivileges_directive

Expected single line of output:

    NoNewPrivileges=true

Related lab check (not graded):

    systemctl show myapp.service -p NoNewPrivileges
    NoNewPrivileges=yes

    systemd-analyze security myapp.service | tail -1
    -> Overall exposure level for myapp.service: 6.9 MEDIUM

systemctl show prints yes for the boolean you wrote as true.

## How to work

1. Skim this README, then re-open `lessons/50-systemd-hardening/lesson.md` (or the PDF).
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

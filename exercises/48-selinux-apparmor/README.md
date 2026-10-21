# Exercise: 48. SELinux/AppArmor Awareness

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- Know which MAC system your distro uses
- Read basic denials from logs
- Avoid setenforce 0 as permanent fix
- Apply targeted policy changes properly

## Task

Open `exercise.sh` and implement `mac_for_distro`. It takes one argument,
a distro family name, and prints the Mandatory Access Control system that
family uses by default. Handle at least `rhel` and `ubuntu`. Output exactly
one lowercase word per call: no spaces, no extra text. Think about the lesson's
distro table and keep the function a simple case statement. After the tests
pass, run the status command appropriate to your lab VM and record the mode in
your notes. Also write one sentence on why `setenforce 0` is a diagnostic
step and not a fix.

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/48-selinux-apparmor/` | Reference only **after** a real attempt |

## Examples / expected behavior

Run from the exercise folder:

    source ./exercise.sh
    mac_for_distro rhel
    mac_for_distro ubuntu

Expected output, one line each:

    selinux
    apparmor

Related lab checks (not graded):

    getenforce
    Enforcing
    sudo aa-status | head -2
    apparmor module is loaded.

Only one of these two commands is normally meaningful on a given host.

## How to work

1. Skim this README, then re-open `lessons/48-selinux-apparmor/lesson.md` (or the PDF).
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

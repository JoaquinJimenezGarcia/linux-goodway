# Exercise: 22. Boot Process, Targets, and Rescue Ideas

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- Describe BIOS/UEFI → bootloader → kernel → systemd
- List targets (multi-user, graphical, rescue)
- Change default target thoughtfully
- Know when to use recovery modes

## Task

Implement pid1_name in exercise.sh so it prints the name of the init system that runs as process ID 1 on a modern mainstream Linux distribution. No arguments, no extra text, lowercase. The test compares the exact output. To make it real, run ps -p 1 -o comm= on a Linux VM or container, and note that in a minimal Docker container PID 1 can be your own command instead; write one sentence on why that differs.

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/22-boot-targets/` | Reference only **after** a real attempt |

## Examples / expected behavior

pid1_name    -> systemd

On a real host:
ps -p 1 -o comm=    -> systemd
cat /proc/1/comm    -> systemd
In a plain Docker container PID 1 is whatever the container started (often sh or your app), not systemd.

Check default target: systemctl get-default -> multi-user.target. Check boot time: systemd-analyze -> Startup finished in ... Older init systems were SysV init and Upstart, so the name is not init on current Debian, Ubuntu, Fedora or RHEL. Print lowercase letters only.

## How to work

1. Skim this README, then re-open `lessons/22-boot-targets/lesson.md` (or the PDF).
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

# Exercise: 51. Building Your Persistent Linux Lab

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- Create a disposable VM snapshot workflow
- Document lab IP/users
- Separate 'break glass' practice VMs
- Automate lab provisioning lightly

## Task

Open `exercise.sh` and implement `lab_safety_tool`. It prints the single
lowercase word naming the feature the lesson says to use before every risky
lab experiment so you can return to a known good state quickly. The test is a
recall check and does not touch a hypervisor. After it passes, do the mini-lab
for real: create a VM, take a snapshot, break `/etc/fstab` on purpose, recover
through the console, and restore. Write down the commands or UI steps you used
and the time the reset took. Note one rule you will follow about credentials
in the lab.

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/51-lab-vm-practice/` | Reference only **after** a real attempt |

## Examples / expected behavior

Run from the exercise folder:

    source ./exercise.sh
    lab_safety_tool

Expected single line of output:

    snapshots

Related lab check (not graded):

    VBoxManage snapshot lab-ubuntu list
    Name: clean-install (UUID: 6c1e...) *
    Name: pre-firewall (UUID: 02ab...)

A good habit is naming each snapshot after the module it protects.

## How to work

1. Skim this README, then re-open `lessons/51-lab-vm-practice/lesson.md` (or the PDF).
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

# Exercise: 53. Capstone: Harden and Operate a Linux Web Server

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- Provision a Linux VM
- Serve a simple site behind a reverse proxy
- Add firewall, SSH hardening, systemd unit
- Document runbook + restore notes

## Task

Open `exercise.sh` and implement `checklist_min_ports`. It prints the
comma-separated list of TCP port numbers, in ascending order and without
spaces, that a hardened web server with remote administration should expose
to the internet: one for SSH, one for plain HTTP, and one for HTTPS. One line,
nothing else. After it passes, build the capstone and produce an evidence
folder with the listening ports, firewall status, `sshd -T` excerpt,
certificate dates, restore diff, and post-reboot checks. Any port beyond
these three needs a written reason.

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/53-capstone-server/` | Reference only **after** a real attempt |

## Examples / expected behavior

Run from the exercise folder:

    source ./exercise.sh
    checklist_min_ports

Expected single line of output:

    22,80,443

Related lab check (not graded):

    sudo ss -tlnp
    LISTEN 0 511 0.0.0.0:80    ... nginx
    LISTEN 0 511 0.0.0.0:443   ... nginx
    LISTEN 0 128 0.0.0.0:22    ... sshd
    LISTEN 0 128 127.0.0.1:8080 ... app

Port 8080 is fine because it is loopback only and not in the firewall allow set.

## How to work

1. Skim this README, then re-open `lessons/53-capstone-server/lesson.md` (or the PDF).
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

# Exercise: 18. Listening Sockets, ss, and Firewalls Intro

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- List listening ports with ss
- Map ports to processes
- Explain firewall purpose (nftables/ufw)
- Open only needed ports

## Task

Implement ss_listening_flags in exercise.sh. It takes no arguments and must print the exact flag string most admins use to list listening TCP and UDP sockets with owning process and numeric addresses. The test compares the output exactly, so print only the flags with the leading dash and no extra text. Before finishing, run sudo ss with those flags on a real host and write one sentence in your notes for each letter t, u, l, p and n, describing what it adds to the output.

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/18-ss-netstat-firewall/` | Reference only **after** a real attempt |

## Examples / expected behavior

ss_listening_flags    -> -tulpn

Used as: sudo ss $(ss_listening_flags)
The letters mean: t=TCP, u=UDP, l=listening only, p=process, n=numeric.
Do not print ss itself or any explanation, only the flag string.

Example on a host:
sudo ss -tulpn | head -3 shows Netid, State, Local Address:Port and a users:(("sshd",pid=801,fd=3)) column. Without p you lose the process; without n names such as ssh replace 22. Output of the function itself is just the dash and five letters.

## How to work

1. Skim this README, then re-open `lessons/18-ss-netstat-firewall/lesson.md` (or the PDF).
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

# Exercise: 49. Packet Filtering Mental Model (nftables)

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- Explain chains/tables conceptually
- Prefer high-level tools when enough (ufw/firewalld)
- Log drops thoughtfully
- Test rules remotely with care

## Task

Open `exercise.sh` and implement `firewall_default_inbound`. It prints the
single lowercase word naming the default inbound policy the lesson recommends
for a server firewall. Nothing else is printed and nothing on the system is
touched; the test is a recall check, not a rule load. After it passes, work
the mini-lab only inside a VM snapshot with console access. Record the output
of `nft list ruleset` before and after your change in your notes, and write the
exact three rules that must appear above any `drop` so you do not lose SSH or
break replies. Never test an unfamiliar ruleset on a remote-only machine.

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/49-networking-nft/` | Reference only **after** a real attempt |

## Examples / expected behavior

Run from the exercise folder:

    source ./exercise.sh
    firewall_default_inbound

Expected single line of output:

    deny

Related lab checks (not graded):

    sudo nft list chain inet filter input | head -3
    type filter hook input priority filter; policy drop;

    sudo ufw status verbose | grep Default
    Default: deny (incoming), allow (outgoing), disabled (routed)

In nftables the word is spelled `drop`; the concept is default deny.

## How to work

1. Skim this README, then re-open `lessons/49-networking-nft/lesson.md` (or the PDF).
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

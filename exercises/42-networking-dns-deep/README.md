# Exercise: 42. DNS Debugging and /etc/resolv.conf

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- Read resolv.conf and systemd-resolved
- Debug NXDOMAIN vs timeout
- Understand search domains
- Cache flush awareness

## Task

Open `exercise.sh` and implement the `nxdomain_means` function so it prints
one short token describing what an NXDOMAIN response tells you about the
queried name. Use the vocabulary from the lesson: the token is lowercase,
words joined with hyphens, no spaces, no trailing text. The function must not
call the network; it is a recall check of the response-code table. After the
test passes, run `dig` against a name you invent in your lab and read the
`status:` field to confirm in practice. Then write one sentence in your notes
that contrasts NXDOMAIN with a timeout, and say which one points at the
network path rather than the zone data.

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/42-networking-dns-deep/` | Reference only **after** a real attempt |

## Examples / expected behavior

Run from the exercise folder:

    source ./exercise.sh
    nxdomain_means

Expected single line of output:

    name-not-exist

Related lab check (not graded):

    dig nosuchhost.example.com | grep status
    ;; ->>HEADER<<- opcode: QUERY, status: NXDOMAIN

A timeout prints no status line at all; dig reports that no servers could be
reached. Keep these two outcomes distinct in your notes.

## How to work

1. Skim this README, then re-open `lessons/42-networking-dns-deep/lesson.md` (or the PDF).
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

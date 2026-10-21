# Exercise: 17. Networking Basics: IP, DNS, Ports

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- Explain IP, CIDR, ports at a practical level
- Query DNS with dig/nslookup/getent
- Inspect addresses with ip
- Test connectivity with ping/curl

## Task

Implement default_https_port in exercise.sh so it prints the standard TCP port used by HTTPS, with nothing else on the line. It takes no arguments. Use echo and a plain number; the test compares the output exactly, so avoid extra spaces or text such as "port". When done, confirm the value against the system database with getent services https and read how the port number, protocol and service name relate. Optionally, write a second helper of your own for http (80) and ssh (22) to practice the table from the lesson.

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/17-networking-basics/` | Reference only **after** a real attempt |

## Examples / expected behavior

default_https_port    -> 443

The output is exactly the three characters 443 followed by a newline. Cross-check:
getent services https     -> https    443/tcp
For comparison, http is 80 and ssh is 22.

Related lookups: getent services ssh -> ssh 22/tcp; getent services domain -> domain 53/tcp. Typical URL form: https://host/ implies port 443; http://host/ implies port 80; an explicit https://host:8443/ overrides the default. Print only digits, no label.

## How to work

1. Skim this README, then re-open `lessons/17-networking-basics/lesson.md` (or the PDF).
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

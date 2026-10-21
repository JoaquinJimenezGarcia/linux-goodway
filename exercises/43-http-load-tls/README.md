# Exercise: 43. Load Balancing and Reverse Proxy (Linux view)

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- Explain reverse proxy role
- Read nginx/Caddy basics at config level
- Terminate TLS at proxy
- Health checks and upstreams

## Task

Open `exercise.sh` and implement `tls_termination_means` so it prints one
hyphenated token that states what the proxy does to the client TLS session
when it terminates TLS. Use the vocabulary from the Core concepts table: all
lowercase, words joined by hyphens, no extra output. No network access is
needed. After it passes, build the mini-lab proxy and confirm with
`curl -vk` which hop is encrypted. In your notes, also write which of 502,
503, and 504 you would expect when the backend is stopped, and which log file
proves it. That short note is part of the exercise even though the test does
not check it.

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/43-http-load-tls/` | Reference only **after** a real attempt |

## Examples / expected behavior

Run from the exercise folder:

    source ./exercise.sh
    tls_termination_means

Expected single line of output:

    decrypt-at-proxy

Related lab checks (not graded):

    sudo nginx -t
    nginx: configuration file /etc/nginx/nginx.conf test is successful

    curl -sk -o /dev/null -w "%{http_code}\n" https://127.0.0.1/
    502        # when the backend on 8080 is stopped

Passthrough would instead leave the proxy unable to read the HTTP headers.

## How to work

1. Skim this README, then re-open `lessons/43-http-load-tls/lesson.md` (or the PDF).
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

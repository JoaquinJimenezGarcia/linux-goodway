# Exercise: 19. HTTP from the CLI: curl and friends

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- Fetch URLs with curl
- Inspect headers and status codes
- POST JSON for APIs
- Follow redirects consciously

## Task

Implement http_ok in exercise.sh. It receives an HTTP status code as its first argument. When the code is exactly 200 it must print yes, and for anything else (404, 500, 301, an empty string, or no argument) it must print no. Compare it as a string with quotes around the variable so an empty argument does not cause a syntax error. The function does not need to run curl; the test supplies the codes. After ./test.sh passes, combine it by hand with curl -s -o /dev/null -w '%{http_code}' against a real URL.

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/19-curl-http/` | Reference only **after** a real attempt |

## Examples / expected behavior

http_ok 200    -> yes
http_ok 404    -> no
http_ok 500    -> no
http_ok 301    -> no
http_ok ""     -> no
http_ok        -> no

One word per call followed by a newline, and nothing else on stdout.

Combined use:
code=$(curl -s -o /dev/null -w '%{http_code}' https://example.com)
http_ok "$code" -> yes
Only the exact string 200 counts: 201, 204 and 301 are not accepted by this helper, and curl exit status 0 does not mean HTTP success.

## How to work

1. Skim this README, then re-open `lessons/19-curl-http/lesson.md` (or the PDF).
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

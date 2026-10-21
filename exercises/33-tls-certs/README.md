# Exercise: 33. TLS Certificates and Trust Stores (ops view)

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- Explain cert, key, chain, CA
- Inspect certs with openssl
- Know where system trust stores live
- Plan renewals before expiry

## Task

Implement `openssl_show_dates_flag` in `exercise.sh` so it prints the
option for `openssl x509` that outputs the `notBefore` and `notAfter`
validity dates of a certificate. Print only the option with its leading dash.
After the test passes, generate a short-lived self-signed certificate as
shown in the lesson, run the option against it, and note both dates plus
how many days remain until `notAfter`. Keep the function body to one line; the goal is recall of the lesson vocabulary, not cleverness. Finish by re-reading the Decision guide table and noting one failure mode you could have caused yourself.

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/33-tls-certs/` | Reference only **after** a real attempt |

## Examples / expected behavior

Expected behavior:

```
$ openssl_show_dates_flag
-dates
```

How the option is used in practice:

```
$ openssl x509 -in lab.crt -noout -dates
notBefore=Oct 21 08:00:00 2026 GMT
notAfter=Nov 20 08:00:00 2026 GMT
```

Do not print `-enddate` or `--dates`; the test wants exactly `-dates`.

Self-check: run `bash -c 'source exercise.sh; openssl_show_dates_flag'` from the exercise directory (replace openssl_show_dates_flag with your function name) and compare by eye, then run `./test.sh`. Also confirm there is no trailing whitespace in the output.

## How to work

1. Skim this README, then re-open `lessons/33-tls-certs/lesson.md` (or the PDF).
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

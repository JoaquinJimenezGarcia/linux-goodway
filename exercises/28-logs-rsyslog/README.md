# Exercise: 28. Logging: journald, syslog, and log files

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- Find logs under /var/log
- Use journalctl effectively
- Rotate logs conceptually
- Correlate time across hosts

## Task

Open `exercise.sh` and implement `journal_unit_flag` so it prints the
single `journalctl` option that restricts output to one systemd unit.
This is a vocabulary drill: the function must print just the flag, with no
extra text and no trailing spaces. Then run `./test.sh` until it is green.
After that, run the real command on a Linux host against a unit you know
(for example ssh or cron) and paste three output lines into your notes.

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/28-logs-rsyslog/` | Reference only **after** a real attempt |

## Examples / expected behavior

Expected behavior:

```
$ source exercise.sh
$ journal_unit_flag
-u
```

Real-world use of the same flag:

```
$ journalctl -u ssh -n 3 --no-pager
```

Common mistake: printing `--unit` or `-u nginx`. The test wants only the short
flag `-u`.

Self-check: run `bash -c 'source exercise.sh; journal_unit_flag'` from the exercise directory (replace journal_unit_flag with your function name) and compare by eye, then run `./test.sh`. Also confirm there is no trailing whitespace in the output.

## How to work

1. Skim this README, then re-open `lessons/28-logs-rsyslog/lesson.md` (or the PDF).
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

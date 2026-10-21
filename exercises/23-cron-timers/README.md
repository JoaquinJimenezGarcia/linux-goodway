# Exercise: 23. Scheduling: cron and systemd timers

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- Write crontab entries
- Prefer systemd timers for modern systems
- Handle environment differences in scheduled jobs
- Log scheduled task output

## Task

Implement cron_daily_3am in exercise.sh. It prints the five-field crontab schedule expression for running a job once every day at 03:00 in the morning, and nothing else. The five fields are minute, hour, day of month, month and day of week. Because the value contains asterisks, quote the string so the shell does not expand them into filenames. After the test passes, check your answer with systemd-analyze calendar using the equivalent OnCalendar form, and write the expression for 02:30 every Monday as a second drill.

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/23-cron-timers/` | Reference only **after** a real attempt |

## Examples / expected behavior

cron_daily_3am    -> 0 3 * * *

Field by field: minute 0, hour 3, any day of month, any month, any weekday.
Related: 30 2 * * 1 = Mondays 02:30; */15 * * * * = every 15 minutes.
Without quotes, echo 0 3 * * * would expand the stars to file names.

Test with the helper: [ "$(cron_daily_3am)" = '0 3 * * *' ] && echo pass. A full crontab line adds the command: 0 3 * * * /usr/local/bin/backup.sh. The systemd equivalent is OnCalendar=*-*-* 03:00:00. Print only the five fields separated by single spaces.

## How to work

1. Skim this README, then re-open `lessons/23-cron-timers/lesson.md` (or the PDF).
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

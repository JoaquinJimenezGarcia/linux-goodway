# Exercise: 44. Backups, Snapshots, and Restore Drills

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- Define RPO/RTO simply
- Prefer tested restores
- Know snapshot vs backup
- Encrypt backups and manage keys

## Task

Open `exercise.sh` and implement `rpo_means`. It must print one lowercase
token, with words joined by hyphens, that defines what RPO measures in the
lesson's own words. No file access and no tools are required. After the test
turns green, do the mini-lab restore drill and record two numbers in your
notes: your measured restore time (RTO) and the gap between backup runs
(your effective RPO). Finally explain in one sentence why a snapshot on the
same disk array does not satisfy a 3-2-1 plan. These notes are not graded but
are the point of the module.

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/44-storage-backup/` | Reference only **after** a real attempt |

## Examples / expected behavior

Run from the exercise folder:

    source ./exercise.sh
    rpo_means

Expected single line of output:

    max-data-loss-window

Example reasoning (not graded):

    nightly backup at 02:00, failure at 17:00  -> up to 15h of data lost
    configured RPO is therefore 24h worst case

    restore of 10 files took 2s in the lab     -> measured RTO is 2s
    restore of 500 GB will not scale linearly; measure at realistic size

## How to work

1. Skim this README, then re-open `lessons/44-storage-backup/lesson.md` (or the PDF).
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

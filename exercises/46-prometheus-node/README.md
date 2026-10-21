# Exercise: 46. Node Metrics and Exporters (ops intro)

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- Expose node metrics conceptually
- Know RED/USE for hosts
- Alert on disk/inode/memory
- Avoid high-cardinality labels

## Task

Open `exercise.sh` and implement `alert_on_disk_pct`. It prints the numeric
percent-used threshold that the lesson uses as the example disk alert, as a
bare integer with no percent sign and no text. No metrics stack is required for
the test. After it passes, install node_exporter in a lab VM, compute the
percent used on `/` from the raw `node_filesystem_*` metrics, and compare it
with `df`. Write the alert expression from the lesson in your own words, and
note why `for: 10m` and a tmpfs exclusion are part of a good rule. Also note
one warning-level threshold that should fire earlier and go to a ticket.

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/46-prometheus-node/` | Reference only **after** a real attempt |

## Examples / expected behavior

Run from the exercise folder:

    source ./exercise.sh
    alert_on_disk_pct

Expected single line of output:

    90

Related lab check (not graded):

    df -P / | awk 'NR==2 {print $5}'
    42%

    curl -s localhost:9100/metrics | grep 'node_filesystem_avail_bytes{.*mountpoint="/"'
    node_filesystem_avail_bytes{device="/dev/sda1",fstype="ext4",mountpoint="/"} 3.1e+10

percent used = (1 - avail/size) * 100 should match df within a point or two.

## How to work

1. Skim this README, then re-open `lessons/46-prometheus-node/lesson.md` (or the PDF).
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

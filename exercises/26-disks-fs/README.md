# Exercise: 26. Disks, Partitions, Filesystems, mount

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- List block devices
- Understand partitions vs filesystems
- Mount/umount carefully
- Check free space and inodes

## Task

Implement inode_check_flag in exercise.sh. It takes no arguments and prints the option you pass to df to report inode usage instead of block usage. Print only the flag, including its leading dash. Be careful when testing by hand: echo with a leading dash can be read as an option by some shells, so confirm that your function prints the text exactly (printf '%s\n' is a safe choice). Afterwards run df -i / and df -h / on a real host and explain in one sentence why the two can disagree.

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/26-disks-fs/` | Reference only **after** a real attempt |

## Examples / expected behavior

inode_check_flag    -> -i

Usage: df $(inode_check_flag) /
df -h /   shows bytes used     (blocks)
df -i /   shows inodes used    (number of files)
Both limits matter; either one can cause "No space left on device".

Example sequence on a real host: df -h / shows Use% 39%, df -i / shows IUse% 16%. When IUse% reaches 100% you get No space left on device even though df -h shows plenty free. The function prints just the two characters dash and i.

## How to work

1. Skim this README, then re-open `lessons/26-disks-fs/lesson.md` (or the PDF).
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

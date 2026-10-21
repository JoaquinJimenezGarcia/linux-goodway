# Exercise: 03. Files, Links, and Metadata

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- Inspect files with file, stat, du, df
- Distinguish hard links vs symbolic links
- Understand inodes at a practical level
- Use touch, install, and install-like patterns

## Task

Implement link_kind(ls_first_char_or_name). The input is a string describing how a link was made: either the word "soft" or "hard" (case-insensitive, surrounding whitespace ignored), or the command used: "ln -s" means soft and plain "ln" means hard. Return the lowercase string "soft" for symbolic links and "hard" for hard links. For any unrecognized input return "unknown". The point is to connect the commands to the concepts: ln -s creates a symbolic (soft) link with its own inode, plain ln creates another name for the same inode.

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/03-files-meta/` | Reference only **after** a real attempt |

## Examples / expected behavior

link_kind("soft") -> "soft"
link_kind("HARD") -> "hard"
link_kind("ln -s") -> "soft"
link_kind("ln") -> "hard"
link_kind("  Soft ") -> "soft"
link_kind("copy") -> "unknown"

Shell view:
ln -s a b   -> soft (ls -l shows 'l' and b -> a)
ln a b      -> hard (same inode, link count 2)
link_kind("ln -s a b") may also be treated as soft.
A dangling soft link still reports "soft"; the kind is about creation.

## How to work

1. Skim this README, then re-open `lessons/03-files-meta/lesson.md` (or the PDF).
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

# Exercise: 10. Less, editors, and reading large output

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- Page output with less/more
- Edit files in nano or vim at a basic level
- Search inside less
- Avoid opening multi-GB logs in a GUI editor

## Task

Implement vim_quit_nosave(). It takes no arguments and returns the exact string typed in vim's command-line mode to quit without saving changes, which is ":q!" (colon, letter q, exclamation mark). Return it as a plain string with no newline, no spaces, and no Esc character. The exercise is a memory anchor: when you are stuck in vim after accidental edits, press Esc, then type this and press Enter. Remember that ":wq" saves and quits, ":q" refuses with unsaved changes, and the "!" forces the quit.

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/10-editors-paging/` | Reference only **after** a real attempt |

## Examples / expected behavior

vim_quit_nosave() -> ":q!"

Related commands (for comparison, not returned):
:wq   save and quit
:q    quit (fails with unsaved changes)
:q!   quit and discard changes
ZZ    save and quit in normal mode

The result length is 3 characters and starts with a colon.
The comparison is exact: vim_quit_nosave() == ":q!" is True, while
vim_quit_nosave() == ":wq" is False. No trailing newline is included.

## How to work

1. Skim this README, then re-open `lessons/10-editors-paging/lesson.md` (or the PDF).
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

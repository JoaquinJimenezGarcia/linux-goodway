# Exercise: 24. Packages: apt/dpkg (Debian/Ubuntu)

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- Update and install with apt
- Query packages with dpkg/apt
- Clean caches thoughtfully
- Pin/version awareness

## Task

Implement apt_update_does in exercise.sh. It takes no arguments and prints one hyphenated token describing what apt update does: it refreshes the package indexes (the list of available packages and versions) but installs nothing. The test compares the output exactly, so print only that token in lowercase. As a follow-up on a Debian or Ubuntu system, run sudo apt update and then apt list --upgradable to confirm that no package changed until you run apt upgrade.

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/24-packages-apt/` | Reference only **after** a real attempt |

## Examples / expected behavior

apt_update_does    -> refresh-indexes

On a real system:
sudo apt update      -> downloads indexes, installs nothing
apt list --upgradable -> shows what could be upgraded
sudo apt upgrade     -> actually installs newer versions

Contrast with other verbs: apt install pkg fetches and installs one package, apt upgrade installs newer versions, apt remove deletes software. The helper prints one hyphenated word pair with no spaces: refresh then indexes, joined by a dash.

## How to work

1. Skim this README, then re-open `lessons/24-packages-apt/lesson.md` (or the PDF).
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

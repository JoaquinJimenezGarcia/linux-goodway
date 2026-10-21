# Exercise: 47. Git on the Server and Hooks (ops angle)

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- Use git safely on servers
- Understand deploy keys
- Avoid editing prod checkouts casually
- Know hook basics

## Task

Open `exercise.sh` and implement `prefer_deploy_artifact`. It prints a short
hyphenated token that names the kind of deployable unit the lesson recommends
over pulling a mutable branch on a server. Lowercase, one line, nothing else.
After it passes, do the mini-lab and capture the output of `ls -l
/tmp/lab/app/releases` and the `sha256sum` line. In notes, write the rollback
steps as exactly two commands, and explain why a dirty `git status --short` on
a production host is an incident finding, not a normal state.

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/47-git-on-linux/` | Reference only **after** a real attempt |

## Examples / expected behavior

Run from the exercise folder:

    source ./exercise.sh
    prefer_deploy_artifact

Expected single line of output:

    immutable-artifact

Related lab check (not graded):

    git archive --format=tar.gz -o app-v1.tgz v1
    sha256sum app-v1.tgz
    9f2c...  app-v1.tgz
    ls -l /opt/app
    current -> /opt/app/releases/1.4.2

Rollback shape: ln -sfn /opt/app/releases/1.4.1 /opt/app/current, then
systemctl restart app.service.

## How to work

1. Skim this README, then re-open `lessons/47-git-on-linux/lesson.md` (or the PDF).
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

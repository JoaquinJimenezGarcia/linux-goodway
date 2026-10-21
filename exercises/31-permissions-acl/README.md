# Exercise: 31. ACLs and umask

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- Explain umask defaults
- Read basic ACLs with getfacl
- Decide when ACLs are warranted
- Avoid ACL sprawl

## Task

Implement `file_mode_after_umask022` in `exercise.sh` so it prints the
octal permission of a newly created regular file under umask 022. Derive it
from the rule in the lesson (666 with the umask bits removed), then confirm
by running `umask 022; touch t; stat -c %a t` in a scratch directory. Print
only the three digits. Keep the function body to one line; the goal is recall of the lesson vocabulary, not cleverness. Finish by re-reading the Decision guide table and noting one failure mode you could have caused yourself.

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/31-permissions-acl/` | Reference only **after** a real attempt |

## Examples / expected behavior

Expected behavior:

```
$ file_mode_after_umask022
644
```

Related checks you can do by hand:

```
umask 077  -> new file 600
umask 002  -> new file 664
umask 022  -> new directory 755
```

The test expects exactly `644`, not `0644` and not `rw-r--r--`.

Self-check: run `bash -c 'source exercise.sh; file_mode_after_umask022'` from the exercise directory (replace file_mode_after_umask022 with your function name) and compare by eye, then run `./test.sh`. Also confirm there is no trailing whitespace in the output.

## How to work

1. Skim this README, then re-open `lessons/31-permissions-acl/lesson.md` (or the PDF).
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

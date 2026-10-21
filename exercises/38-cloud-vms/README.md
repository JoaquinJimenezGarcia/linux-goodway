# Exercise: 38. Linux on Cloud VMs: metadata, identity, disks

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- Use instance metadata thoughtfully
- Attach/mount data disks
- Prefer IAM roles over long-lived keys
- Automate with cloud-init basics

## Task

Implement `cloud_init_purpose` in `exercise.sh` so it prints a short
hyphenated phrase that states what cloud-init is for: configuring a generic
cloud image the first time an instance boots. Use the lowercase hyphenated
form from the lesson. Afterwards, write a small cloud-config on paper or in
a file that creates one user and installs one package, and explain which
boot stage runs each part. Keep the function body to one line; the goal is recall of the lesson vocabulary, not cleverness. Finish by re-reading the Decision guide table and noting one failure mode you could have caused yourself.

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/38-cloud-vms/` | Reference only **after** a real attempt |

## Examples / expected behavior

Expected behavior:

```
$ cloud_init_purpose
first-boot-config
```

Where you see it in practice:

```
$ cloud-init status
status: done
```

The test expects exactly `first-boot-config`. Phrases such as `provisioning`,
`First Boot Config`, or `first boot configuration` will fail the comparison.

Self-check: run `bash -c 'source exercise.sh; cloud_init_purpose'` from the exercise directory (replace cloud_init_purpose with your function name) and compare by eye, then run `./test.sh`. Also confirm there is no trailing whitespace in the output.

## How to work

1. Skim this README, then re-open `lessons/38-cloud-vms/lesson.md` (or the PDF).
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

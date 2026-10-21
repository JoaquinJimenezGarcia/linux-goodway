# Exercise: 37. Compose and Kubernetes Concepts for Operators

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- Read a docker-compose file
- Map pods/services/deployments mentally
- Kubectl get/describe/logs basics
- Know what Linux skills transfer to k8s nodes

## Task

Implement `kubectl_logs_cmd` in `exercise.sh` so it prints the two-word
command prefix you use to read the standard output of a container in a
pod. Print exactly `kubectl` followed by one space and the subcommand, with
no pod name and no flags. When the test passes, practise on a local kind or
minikube cluster: start a pod, read its logs, and also try the option that
shows the logs of a previous crashed container. Keep the function body to one line; the goal is recall of the lesson vocabulary, not cleverness. Finish by re-reading the Decision guide table and noting one failure mode you could have caused yourself.

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/37-compose-k8s-lite/` | Reference only **after** a real attempt |

## Examples / expected behavior

Expected behavior:

```
$ kubectl_logs_cmd
kubectl logs
```

Typical real usage built on that prefix:

```
kubectl logs mypod
kubectl logs deploy/hello --tail=20
kubectl logs mypod --previous
```

The test checks the exact two-word string. `kubectl get logs` and
`kubectl log` are not valid answers.

Self-check: run `bash -c 'source exercise.sh; kubectl_logs_cmd'` from the exercise directory (replace kubectl_logs_cmd with your function name) and compare by eye, then run `./test.sh`. Also confirm there is no trailing whitespace in the output.

## How to work

1. Skim this README, then re-open `lessons/37-compose-k8s-lite/lesson.md` (or the PDF).
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

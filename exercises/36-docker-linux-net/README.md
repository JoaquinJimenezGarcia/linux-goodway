# Exercise: 36. Containers, Namespaces, and Networking

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- Name major namespaces (pid, net, mnt, user)
- Explain bridge networking basics
- Debug DNS inside containers
- Use host networking knowingly

## Task

Implement `default_docker_network` in `exercise.sh` so it prints the
name of the network driver and network that new containers join when you
do not pass `--network`. Use the lowercase one-word name shown by
`docker network ls`. If Docker is available, confirm with `docker network
ls` and `docker inspect` on a throwaway container, and record the subnet of
that network in your notes. Keep the function body to one line; the goal is recall of the lesson vocabulary, not cleverness. Finish by re-reading the Decision guide table and noting one failure mode you could have caused yourself.

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/36-docker-linux-net/` | Reference only **after** a real attempt |

## Examples / expected behavior

Expected behavior:

```
$ default_docker_network
bridge
```

Cross-check on a Docker host:

```
$ docker network ls
NETWORK ID   NAME     DRIVER   SCOPE
a1b2c3d4e5f6 bridge   bridge   local
...
```

The test wants exactly `bridge`. Other valid networks such as `host` and
`none` exist, but they are not the default for new containers.

## How to work

1. Skim this README, then re-open `lessons/36-docker-linux-net/lesson.md` (or the PDF).
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

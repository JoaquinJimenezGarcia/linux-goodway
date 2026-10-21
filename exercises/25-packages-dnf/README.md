# Exercise: 25. Packages: dnf/rpm (RHEL/Fedora) and Alpine apk

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- Map apt concepts to dnf and apk
- Install/query/remove packages
- Know when distroless/minimal images help
- Read release notes before major upgrades

## Task

Implement map_install_cmd in exercise.sh. It takes one argument naming a distribution family and prints the name of the native package manager command: debian maps to apt, rhel maps to dnf, and alpine maps to apk. Use a case statement and quote the argument. For an unknown family, print nothing and return 1. Output only the command name, with no other text. Run ./test.sh, then validate the table on real systems or containers by running the actual install command in each family.

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/25-packages-dnf/` | Reference only **after** a real attempt |

## Examples / expected behavior

map_install_cmd debian    -> apt
map_install_cmd rhel      -> dnf
map_install_cmd alpine    -> apk
map_install_cmd arch      -> prints nothing, status 1

Only the command word is printed, followed by a newline.

Supporting facts: apt belongs to Debian and Ubuntu, dnf to Red Hat, Fedora, Rocky and Alma, apk to Alpine. Unknown input such as arch or empty must give status 1 and no output. Check with: map_install_cmd arch; echo "rc=$?" -> rc=1.

## How to work

1. Skim this README, then re-open `lessons/25-packages-dnf/lesson.md` (or the PDF).
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

# Exercise: 20. SSH Basics: Keys, Config, Jump Hosts

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- Generate and use SSH keys
- Write ~/.ssh/config Host entries
- Disable password auth conceptually
- Use jump hosts / ProxyJump

## Task

Implement ssh_key_perms in exercise.sh. It takes no arguments and must print the octal permission mode that OpenSSH expects for a private key file, with nothing else on the line. The test checks the exact string. Afterwards, create a throwaway key with ssh-keygen, confirm its mode with stat -c '%a %n', deliberately loosen it with chmod 644, and read the warning ssh prints. Restore the correct mode and note why a group-readable private key is a security problem.

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/20-ssh-basics/` | Reference only **after** a real attempt |

## Examples / expected behavior

ssh_key_perms    -> 600

Check on a real key:
stat -c '%a %n' ~/.ssh/id_ed25519    -> 600 /home/you/.ssh/id_ed25519
600 = owner read+write, no access for group or others.
The public key (.pub) is usually 644, and the ~/.ssh directory is 700.

Broken example: chmod 644 ~/.ssh/id_ed25519 makes ssh print 'UNPROTECTED PRIVATE KEY FILE' and ignore the key. Repair with chmod 600 ~/.ssh/id_ed25519. Directory ~/.ssh should be 700. Print the digits only, never the word chmod.

## How to work

1. Skim this README, then re-open `lessons/20-ssh-basics/lesson.md` (or the PDF).
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

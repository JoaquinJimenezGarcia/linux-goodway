# Exercise: 21. systemd: Units, Services, Journals

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- Manage services with systemctl
- Read logs with journalctl
- Write a simple unit file
- Enable services on boot

## Task

Implement enable_now_meaning in exercise.sh. It takes no arguments and prints a short token that states what systemctl enable --now does. The token is two ideas joined with hyphens: it starts the service immediately and it also configures it to start at boot. The test compares the output exactly, so print only that token in lowercase. Test your understanding on a VM with a harmless unit by checking systemctl is-active and systemctl is-enabled before and after.

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/21-systemd-units/` | Reference only **after** a real attempt |

## Examples / expected behavior

enable_now_meaning    -> start-and-boot

Meaning on a real host:
systemctl enable --now hello  -> is-active: active, is-enabled: enabled
systemctl start hello         -> is-active: active, is-enabled: disabled (not at boot)
systemctl enable hello        -> is-active: inactive, is-enabled: enabled

Timeline view: before enable --now, systemctl is-enabled prints disabled and is-active prints inactive. After it, both are positive, and the service also survives reboot. Print the token in lowercase with hyphens and no spaces.

## How to work

1. Skim this README, then re-open `lessons/21-systemd-units/lesson.md` (or the PDF).
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

# Exercise: 27. LVM Intro and /etc/fstab

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

- Explain PV/VG/LV mentally
- Read fstab entries
- Add mounts safely with backups
- Use UUIDs over volatile device names

## Task

Implement fstab_field_uuid in exercise.sh. It receives one complete fstab line as a single quoted argument and must print its first whitespace-separated field, which is the device specification such as UUID=1234-abcd. Fields are separated by spaces or tabs, so awk '{print $1}' or read -r both work. Quote $1 when you use it. Do not print the other fields. Afterwards, run it against real lines from /etc/fstab (skipping comments) and name each of the six fields in your notes.

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/27-lvm-fstab/` | Reference only **after** a real attempt |

## Examples / expected behavior

fstab_field_uuid 'UUID=9f8e-11 /srv/app ext4 defaults 0 2'  -> UUID=9f8e-11
fstab_field_uuid '/dev/vda1 / ext4 defaults 0 1'            -> /dev/vda1
fstab_field_uuid 'LABEL=data /data xfs nofail 0 2'          -> LABEL=data

Only field 1 is printed, followed by a newline.

Tab separated lines also work with awk. Skip comment lines when scanning a real file: grep -v '^#' /etc/fstab | while read -r line; do fstab_field_uuid "$line"; done. Blank lines should be ignored by the caller, not by this helper.

## How to work

1. Skim this README, then re-open `lessons/27-lvm-fstab/lesson.md` (or the PDF).
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

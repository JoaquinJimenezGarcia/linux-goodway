---
title: "05. Users, Groups, sudo, and /etc/passwd"
---

# 05. Users, Groups, sudo, and /etc/passwd

**Phase:** Phase 2 — Permissions and identity  
**Estimated time:** 1–2 days  
**Slug:** `05-users-groups`

## Learning objectives

- Explain passwd/shadow/group files at a high level
- Use id, whoami, groups
- Apply least-privilege with sudo
- Create users/groups on a lab system (carefully)

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

## Identity commands

```bash
whoami
id
groups
```

## Key files

- `/etc/passwd` — username, uid, gid, home, shell (public map)
- `/etc/shadow` — password hashes (root-only)
- `/etc/group` — group memberships

## sudo

```bash
sudo -l                 # what can I run?
sudo apt update         # elevates one command
sudo -i                 # root shell (use sparingly)
```

Prefer narrowly scoped sudoers rules in production — not NOPASSWD:ALL for humans.

## Common mistakes

- Editing passwd by hand when `useradd` exists
- Sharing root password instead of sudo
- Leaving passwordless sudo on internet-facing boxes

## Exercises

Work in `exercises/05-users-groups/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/05-users-groups/` until you have an honest failing attempt.**

## Self-check

1. What is in `/etc/shadow` vs `/etc/passwd`?
2. What does `id` show?
3. Why prefer sudo over shared root?

## Further reading

- https://man7.org/linux/man-pages/man5/passwd.5.html

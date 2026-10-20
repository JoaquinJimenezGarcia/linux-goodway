---
title: "20. SSH Basics: Keys, Config, Jump Hosts"
---

# 20. SSH Basics: Keys, Config, Jump Hosts

**Phase:** Phase 9 — Security and SSH  
**Estimated time:** 1–2 days  
**Slug:** `20-ssh-basics`

## Learning objectives

- Generate and use SSH keys
- Write ~/.ssh/config Host entries
- Disable password auth conceptually
- Use jump hosts / ProxyJump

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

```bash
ssh-keygen -t ed25519 -C "you@example"
ssh-copy-id user@server
ssh user@server
```

## Config

```sshconfig
Host lab
  HostName 203.0.113.10
  User ada
  IdentityFile ~/.ssh/id_ed25519
  ProxyJump bastion
```

Prefer keys over passwords. Protect private keys (permissions 600). Never commit them.

## Common mistakes

- Sharing private keys
- chmod 777 on .ssh
- Password auth on internet-facing SSH

## Exercises

Work in `exercises/20-ssh-basics/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/20-ssh-basics/` until you have an honest failing attempt.**

## Self-check

1. ed25519 purpose?
2. What is ProxyJump?
3. Recommended .ssh private key perms?

## Further reading

- https://www.openssh.com/manual.html

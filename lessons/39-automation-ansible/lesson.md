---
title: "39. Config Automation Mindset (Ansible-oriented)"
---

# 39. Config Automation Mindset (Ansible-oriented)

**Phase:** Phase 11 — Containers and cloud Linux  
**Estimated time:** 1–2 days  
**Slug:** `39-automation-ansible`

## Learning objectives

- Prefer idempotent config management
- Separate inventory from playbooks conceptually
- Avoid snowflake servers
- Combine with immutable images when appropriate

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

Ansible (and friends) apply desired state over SSH.

Principles beat tool trivia:

- Idempotent tasks
- Versioned config
- Small blast radius
- Golden images + automation hybrid

Snowflake servers that nobody can recreate are career-limiting in infra.

## Common mistakes

- Manual SSH drift with no record
- One mega playbook without checks
- Automating before understanding

## Exercises

Work in `exercises/39-automation-ansible/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/39-automation-ansible/` until you have an honest failing attempt.**

## Self-check

1. What is idempotency?
2. Why avoid snowflakes?
3. SSH role in Ansible?

## Further reading

- https://docs.ansible.com/

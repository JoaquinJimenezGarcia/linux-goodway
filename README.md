# Linux Goodway: Fundamentals to Proficiency (Infra + AI hosts)

A complete, ordered path from absolute Linux fundamentals to strong systems
engineering — the twin of [golang-goodway](../golang-goodway), with emphasis on
**infrastructure**, operations, and **AI host** skills.

## Study method (non-negotiable)

1. Read the lesson PDF (or Markdown).
2. Type commands yourself — do not blindly copy-paste.
3. Complete `exercises/NN-slug/` until `./test.sh` passes — **no solutions first**.
4. Only then compare with `solutions/NN-slug/`.
5. Next day: rewrite from memory.

Track checkboxes in [`curriculum/PROGRESS.md`](curriculum/PROGRESS.md).

## Practice environment

Use a real Linux system for best results:

- Ubuntu LTS VM (UTM/VirtualBox/cloud), or
- `docker run --rm -it ubuntu:24.04 bash` for many CLI drills

macOS is fine for early shell lessons; systemd/apt/SELinux topics need Linux.

## Repo layout

```
lessons/NN-slug/lesson.md
pdfs/NN-slug.pdf
exercises/NN-slug/     # exercise.sh + test.sh
solutions/NN-slug/
scripts/build-pdfs.sh
```

## Building PDFs

```bash
brew install pandoc typst
./scripts/build-pdfs.sh
```

## Daily workflow

1. Next unchecked item in `curriculum/PROGRESS.md`
2. Read `pdfs/NN-….pdf`
3. `cd exercises/NN-… && ./test.sh` until green
4. Compare solutions later; rewrite next day

Verify all reference solutions:

```bash
./scripts/smoke_test.sh
```

## Curriculum map

| # | Title | Phase | Time | PDF |
|---|-------|-------|------|-----|
| 00 | Orientation: What Linux Is and How to Practice | Phase 0 — Orientation | 1 day | `pdfs/00-orientation.pdf` |
| 01 | The Shell: Prompts, Commands, Arguments, Exit Codes | Phase 1 — Shell and filesystem | 1 day | `pdfs/01-shell-basics.pdf` |
| 02 | The Filesystem Tree: /, /etc, /var, /home, /proc | Phase 1 — Shell and filesystem | 1–2 days | `pdfs/02-filesystem-tree.pdf` |
| 03 | Files, Links, and Metadata | Phase 1 — Shell and filesystem | 1–2 days | `pdfs/03-files-meta.pdf` |
| 04 | Permissions Basics: rwx, chmod, chown | Phase 2 — Permissions and identity | 1–2 days | `pdfs/04-permissions-basics.pdf` |
| 05 | Users, Groups, sudo, and /etc/passwd | Phase 2 — Permissions and identity | 1–2 days | `pdfs/05-users-groups.pdf` |
| 06 | Special Bits: setuid, setgid, sticky | Phase 2 — Permissions and identity | 1 day | `pdfs/06-special-perms.pdf` |
| 07 | Pipes, Redirection, and Exit Status in Pipelines | Phase 3 — Text, pipes, and discovery | 1–2 days | `pdfs/07-pipes-redirects.pdf` |
| 08 | grep, ripgrep mindset, and find | Phase 3 — Text, pipes, and discovery | 1–2 days | `pdfs/08-grep-find.pdf` |
| 09 | sed and awk for Text Engineering | Phase 3 — Text, pipes, and discovery | 2 days | `pdfs/09-sed-awk.pdf` |
| 10 | Less, editors, and reading large output | Phase 3 — Text, pipes, and discovery | 1 day | `pdfs/10-editors-paging.pdf` |
| 11 | Processes: ps, top, /proc, signals | Phase 4 — Processes and jobs | 1–2 days | `pdfs/11-processes.pdf` |
| 12 | Jobs, Background, nohup, screen/tmux intro | Phase 4 — Processes and jobs | 1 day | `pdfs/12-jobs-background.pdf` |
| 13 | Priority, nice, and resource limits (ulimit) | Phase 4 — Processes and jobs | 1 day | `pdfs/13-nice-priority.pdf` |
| 14 | Bash Scripting Fundamentals | Phase 5 — Shell scripting | 2 days | `pdfs/14-bash-scripting-intro.pdf` |
| 15 | Functions, Arguments, and Exit Codes in Scripts | Phase 5 — Shell scripting | 1–2 days | `pdfs/15-bash-functions-args.pdf` |
| 16 | Testing Shell Scripts and Safe Automation | Phase 5 — Shell scripting | 1–2 days | `pdfs/16-bash-testing.pdf` |
| 17 | Networking Basics: IP, DNS, Ports | Phase 6 — Networking | 1–2 days | `pdfs/17-networking-basics.pdf` |
| 18 | Listening Sockets, ss, and Firewalls Intro | Phase 6 — Networking | 1–2 days | `pdfs/18-ss-netstat-firewall.pdf` |
| 19 | HTTP from the CLI: curl and friends | Phase 6 — Networking | 1 day | `pdfs/19-curl-http.pdf` |
| 20 | SSH Basics: Keys, Config, Jump Hosts | Phase 9 — Security and SSH | 1–2 days | `pdfs/20-ssh-basics.pdf` |
| 21 | systemd: Units, Services, Journals | Phase 7 — Services and boot | 2 days | `pdfs/21-systemd-units.pdf` |
| 22 | Boot Process, Targets, and Rescue Ideas | Phase 7 — Services and boot | 1–2 days | `pdfs/22-boot-targets.pdf` |
| 23 | Scheduling: cron and systemd timers | Phase 7 — Services and boot | 1–2 days | `pdfs/23-cron-timers.pdf` |
| 24 | Packages: apt/dpkg (Debian/Ubuntu) | Phase 8 — Packages, disks, storage | 1–2 days | `pdfs/24-packages-apt.pdf` |
| 25 | Packages: dnf/rpm (RHEL/Fedora) and Alpine apk | Phase 8 — Packages, disks, storage | 1 day | `pdfs/25-packages-dnf.pdf` |
| 26 | Disks, Partitions, Filesystems, mount | Phase 8 — Packages, disks, storage | 2 days | `pdfs/26-disks-fs.pdf` |
| 27 | LVM Intro and /etc/fstab | Phase 8 — Packages, disks, storage | 1–2 days | `pdfs/27-lvm-fstab.pdf` |
| 28 | Logging: journald, syslog, and log files | Phase 10 — Observability and troubleshooting | 1–2 days | `pdfs/28-logs-rsyslog.pdf` |
| 29 | Performance Basics: CPU, memory, iowait, OOM | Phase 10 — Observability and troubleshooting | 2 days | `pdfs/29-perf-basics.pdf` |
| 30 | Troubleshooting Method: REDUCE and Bisect | Phase 10 — Observability and troubleshooting | 1–2 days | `pdfs/30-troubleshooting.pdf` |
| 31 | ACLs and umask | Phase 2 — Permissions and identity | 1 day | `pdfs/31-permissions-acl.pdf` |
| 32 | Capabilities, seccomp, and least privilege (intro) | Phase 9 — Security and SSH | 1–2 days | `pdfs/32-capabilities-seccomp.pdf` |
| 33 | TLS Certificates and Trust Stores (ops view) | Phase 9 — Security and SSH | 1–2 days | `pdfs/33-tls-certs.pdf` |
| 34 | Host Hardening Checklist | Phase 9 — Security and SSH | 1–2 days | `pdfs/34-hardening-basics.pdf` |
| 35 | Docker Basics on Linux | Phase 11 — Containers and cloud Linux | 2 days | `pdfs/35-docker-basics.pdf` |
| 36 | Containers, Namespaces, and Networking | Phase 11 — Containers and cloud Linux | 2 days | `pdfs/36-docker-linux-net.pdf` |
| 37 | Compose and Kubernetes Concepts for Operators | Phase 11 — Containers and cloud Linux | 2 days | `pdfs/37-compose-k8s-lite.pdf` |
| 38 | Linux on Cloud VMs: metadata, identity, disks | Phase 11 — Containers and cloud Linux | 1–2 days | `pdfs/38-cloud-vms.pdf` |
| 39 | Config Automation Mindset (Ansible-oriented) | Phase 11 — Containers and cloud Linux | 1–2 days | `pdfs/39-automation-ansible.pdf` |
| 40 | Shell Text Mastery Drill Week | Phase 3 — Text, pipes, and discovery | 2–3 days | `pdfs/40-shell-text-mastery.pdf` |
| 41 | Robust Bash: errexit, nounset, traps | Phase 5 — Shell scripting | 1–2 days | `pdfs/41-bash-robust.pdf` |
| 42 | DNS Debugging and /etc/resolv.conf | Phase 6 — Networking | 1 day | `pdfs/42-networking-dns-deep.pdf` |
| 43 | Load Balancing and Reverse Proxy (Linux view) | Phase 6 — Networking | 1–2 days | `pdfs/43-http-load-tls.pdf` |
| 44 | Backups, Snapshots, and Restore Drills | Phase 8 — Packages, disks, storage | 1–2 days | `pdfs/44-storage-backup.pdf` |
| 45 | Linux for AI Infrastructure | Phase 11 — Containers and cloud Linux | 2 days | `pdfs/45-ai-infra-linux.pdf` |
| 46 | Node Metrics and Exporters (ops intro) | Phase 10 — Observability and troubleshooting | 1–2 days | `pdfs/46-prometheus-node.pdf` |
| 47 | Git on the Server and Hooks (ops angle) | Phase 5 — Shell scripting | 1 day | `pdfs/47-git-on-linux.pdf` |
| 48 | SELinux/AppArmor Awareness | Phase 9 — Security and SSH | 1–2 days | `pdfs/48-selinux-apparmor.pdf` |
| 49 | Packet Filtering Mental Model (nftables) | Phase 6 — Networking | 1–2 days | `pdfs/49-networking-nft.pdf` |
| 50 | systemd Service Hardening Directives | Phase 7 — Services and boot | 1–2 days | `pdfs/50-systemd-hardening.pdf` |
| 51 | Building Your Persistent Linux Lab | Phase 0 — Orientation | 1–2 days | `pdfs/51-lab-vm-practice.pdf` |
| 52 | Linux Interview and Oncall Drills | Phase 10 — Observability and troubleshooting | 2 days | `pdfs/52-interview-drills.pdf` |
| 53 | Capstone: Harden and Operate a Linux Web Server | Phase 12 — Capstones | 3–5 days | `pdfs/53-capstone-server.pdf` |
| 54 | Capstone: Broken Box Challenge | Phase 12 — Capstones | 2–4 days | `pdfs/54-capstone-troubleshoot.pdf` |
| 55 | Capstone: AI Inference Host on Linux | Phase 12 — Capstones | 4–6 days | `pdfs/55-capstone-ai-host.pdf` |

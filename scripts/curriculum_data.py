#!/usr/bin/env python3
"""Linux Goodway curriculum: modules 00–55."""

from __future__ import annotations

MODULES: list[dict] = []


def add(
    n,
    slug,
    title,
    phase,
    days,
    objectives,
    body,
    pitfalls,
    checks,
    reading,
    ex_kind,
    exercise_guide="",
    exercise_examples="",
):
    MODULES.append(
        {
            "n": n,
            "slug": f"{n:02d}-{slug}",
            "title": title,
            "phase": phase,
            "days": days,
            "objectives": objectives,
            "body": body,
            "pitfalls": pitfalls,
            "checks": checks,
            "reading": reading,
            "ex_kind": ex_kind,
            "exercise_guide": exercise_guide,
            "exercise_examples": exercise_examples,
        }
    )


P0 = "Phase 0 — Orientation"
P1 = "Phase 1 — Shell and filesystem"
P2 = "Phase 2 — Permissions and identity"
P3 = "Phase 3 — Text, pipes, and discovery"
P4 = "Phase 4 — Processes and jobs"
P5 = "Phase 5 — Shell scripting"
P6 = "Phase 6 — Networking"
P7 = "Phase 7 — Services and boot"
P8 = "Phase 8 — Packages, disks, storage"
P9 = "Phase 9 — Security and SSH"
P10 = "Phase 10 — Observability and troubleshooting"
P11 = "Phase 11 — Containers and cloud Linux"
P12 = "Phase 12 — Capstones"

# --- Phase 0 ---
add(
    0,
    "orientation",
    "Orientation: What Linux Is and How to Practice",
    P0,
    "1 day",
    [
        "Explain Linux vs Unix vs GNU userland at a beginner level",
        "Choose a practice environment (VM, cloud, WSL, or container)",
        "Open a shell and run your first commands safely",
        "Adopt the study method: attempt → struggle → solution → rewrite",
    ],
    """
## What is Linux?

**Linux** usually means the **kernel** (talks to hardware) plus a **userland**
(shells, coreutils, systemd, package manager) that makes a usable OS.

People say “Linux” for whole distributions: Ubuntu, Debian, Fedora, RHEL, Alpine.

| Layer | Role |
|-------|------|
| Hardware | CPU, disk, NIC |
| Kernel | processes, memory, drivers, networking stack |
| Userland | bash, ls, apt/dnf, sshd, your apps |

## Why learn Linux deeply?

Infrastructure, AI serving, containers, and cloud VMs almost all run Linux.
Copy-pasting Stack Overflow commands without understanding them causes outages.

## Practice environments

Pick one and stick with it for early lessons:

1. **Local VM** (UTM/VirtualBox) with Ubuntu Server
2. **Cloud VM** (small free-tier Linux instance)
3. **WSL2** on Windows
4. **Docker** (`docker run -it --rm ubuntu:24.04 bash`) for many CLI drills

macOS is Unix-like and fine for shell basics, but later lessons need real Linux
(systemd, apt/dnf, `/proc`). Prefer a Linux VM or container for those.

## Study method

1. Read the lesson PDF; type commands yourself.
2. Do exercises in `exercises/NN-slug/` — **no solutions first**.
3. Compare with `solutions/` only after an honest attempt.
4. Next day: rewrite scripts/commands from memory.

Track progress in `curriculum/PROGRESS.md`.
""",
    [
        "Practicing only on macOS and skipping Linux-specific topics forever",
        "Running destructive commands as root without understanding them",
        "Skipping the rewrite-from-memory step",
    ],
    [
        "What is the kernel vs userland?",
        "Name two practice environments suitable for this course",
        "Why avoid looking at solutions first?",
    ],
    ["https://www.kernel.org/", "https://ubuntu.com/tutorials/command-line-for-beginners"],
    "orient_hello",
)

add(
    1,
    "shell-basics",
    "The Shell: Prompts, Commands, Arguments, Exit Codes",
    P1,
    "1 day",
    [
        "Run commands with arguments and flags",
        "Read exit codes (`$?`) and why they matter",
        "Use `--help` / man pages productively",
        "Distinguish absolute vs relative paths",
    ],
    """
## Anatomy of a command

```bash
ls -la /tmp
# ^   ^  ^
# |   |  argument (path)
# |   options/flags
# program name
```

## Exit codes

Every process returns an integer exit status:

```bash
true; echo $?    # 0 = success
false; echo $?   # non-zero = failure
```

Scripts and CI systems rely on this. **0 means success** by convention.

## Getting help

```bash
man ls
ls --help
whatis grep
```

Skim SYNOPSIS first, then EXAMPLES if present.

## Paths

- Absolute: `/home/ada/file` (starts at `/`)
- Relative: `./file`, `../sibling`, `docs/readme`

`.` is current directory; `..` is parent.
""",
    [
        "Ignoring exit codes and assuming success",
        "Confusing flags that need spaces vs combined short flags",
        "Not reading man page SYNOPSIS",
    ],
    [
        "What does exit code 0 mean?",
        "Absolute vs relative path?",
        "How do you open the manual for `cp`?",
    ],
    ["https://man7.org/linux/man-pages/man1/bash.1.html"],
    "shell_exit",
)

add(
    2,
    "filesystem-tree",
    "The Filesystem Tree: /, /etc, /var, /home, /proc",
    P1,
    "1–2 days",
    [
        "Navigate with cd, pwd, ls",
        "Explain key FHS directories",
        "Create, move, copy, remove files carefully",
        "Use tab completion and wildcards",
    ],
    """
## Filesystem Hierarchy (FHS) highlights

| Path | Purpose |
|------|---------|
| `/` | root of the tree |
| `/bin`, `/usr/bin` | user commands |
| `/etc` | configuration |
| `/home` | user home directories |
| `/var` | logs, caches, variable data |
| `/tmp` | temporary (often cleared) |
| `/proc`, `/sys` | kernel/process info (virtual) |
| `/dev` | device nodes |

## Navigation and file ops

```bash
pwd
cd /etc
ls -la
mkdir -p ~/lab/linux-goodway
cp file.txt file.bak
mv oldname newname
rm file.txt          # careful
rm -r dirname        # careful; prefer trash tools when learning
```

## Wildcards

`*` any string, `?` one char, `[abc]` character class.

```bash
ls *.log
```
""",
    [
        "Running `rm -rf /` or similar disasters",
        "Treating `/proc` files like normal disk files to edit casually",
        "Filling `/` by writing huge files to `/tmp` unchecked",
    ],
    [
        "What lives in `/etc`?",
        "What is special about `/proc`?",
        "What does `mkdir -p` do?",
    ],
    ["https://refspecs.linuxfoundation.org/FHS_3.0/fhs/index.html"],
    "fs_nav",
)

add(
    3,
    "files-meta",
    "Files, Links, and Metadata",
    P1,
    "1–2 days",
    [
        "Inspect files with file, stat, du, df",
        "Distinguish hard links vs symbolic links",
        "Understand inodes at a practical level",
        "Use touch, install, and install-like patterns",
    ],
    """
## Inspecting

```bash
file /bin/ls
stat myfile
du -sh *
df -h
```

## Inodes and links

A file name is a directory entry pointing to an **inode** (metadata + data blocks).

- **Hard link**: another name for the same inode (same filesystem only)
- **Symbolic link**: a pointer path (can dangle)

```bash
ln a.txt hard-a
ln -s a.txt soft-a
```

Deleting one hard link name does not remove data until the last link is gone.
""",
    [
        "Assuming `rm` of a symlink deletes the target (it removes the link)",
        "Hard-linking directories (usually forbidden)",
        "Ignoring disk full (`df`) when services fail mysteriously",
    ],
    [
        "Hard link vs symlink?",
        "What does `stat` show that `ls -l` might not?",
        "What does `df -h` report?",
    ],
    ["https://man7.org/linux/man-pages/man1/ln.1.html"],
    "fs_links",
)

add(
    4,
    "permissions-basics",
    "Permissions Basics: rwx, chmod, chown",
    P2,
    "1–2 days",
    [
        "Read `ls -l` permission bits",
        "Change mode with chmod (symbolic and octal)",
        "Change owner/group with chown/chgrp",
        "Predict access for user/group/other",
    ],
    """
## Reading `ls -l`

```text
-rwxr-xr-- 1 ada dev 120 Mar 1 file.sh
│└─┬─┘└─┬─┘└─┬─┘
│  u    g    o
│ user group other
type: - file, d dir, l link
```

Bits: `r` read, `w` write, `x` execute (enter for dirs).

## chmod

```bash
chmod u+x script.sh
chmod 755 script.sh   # rwxr-xr-x
chmod 640 secret.txt  # rw-r-----
```

Octal: owner/group/other each as r=4,w=2,x=1 summed.

## Ownership

```bash
sudo chown ada:dev file
```

On shared servers, wrong group permissions are a common security bug.
""",
    [
        "chmod 777 on everything \"to make it work\"",
        "Forgetting directories need `x` to be entered",
        "Running as root to avoid learning permissions",
    ],
    [
        "What does 644 mean?",
        "Why does a directory need execute?",
        "When is 777 inappropriate?",
    ],
    ["https://man7.org/linux/man-pages/man1/chmod.1.html"],
    "perm_chmod",
)

add(
    5,
    "users-groups",
    "Users, Groups, sudo, and /etc/passwd",
    P2,
    "1–2 days",
    [
        "Explain passwd/shadow/group files at a high level",
        "Use id, whoami, groups",
        "Apply least-privilege with sudo",
        "Create users/groups on a lab system (carefully)",
    ],
    """
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
""",
    [
        "Editing passwd by hand when `useradd` exists",
        "Sharing root password instead of sudo",
        "Leaving passwordless sudo on internet-facing boxes",
    ],
    [
        "What is in `/etc/shadow` vs `/etc/passwd`?",
        "What does `id` show?",
        "Why prefer sudo over shared root?",
    ],
    ["https://man7.org/linux/man-pages/man5/passwd.5.html"],
    "users_id",
)

add(
    6,
    "special-perms",
    "Special Bits: setuid, setgid, sticky",
    P2,
    "1 day",
    [
        "Explain setuid/setgid/sticky bit purposes",
        "Recognize them in `ls -l`",
        "Know security risks of setuid binaries",
        "Use sticky on shared directories like /tmp",
    ],
    """
## Sticky bit (directories)

On `/tmp`, sticky (`chmod +t`) means only file owner (and root) can delete their files —
even if others have write on the directory.

## setuid / setgid

- **setuid** on executable: runs as file owner (e.g. `passwd`)
- **setgid** on dir: new files inherit group

```bash
ls -l /usr/bin/passwd   # often looks like -rwsr-xr-x
```

setuid is powerful and dangerous — audit carefully; never ship custom setuid without review.
""",
    [
        "Creating custom setuid root binaries casually",
        "World-writable setuid files (critical vulnerability)",
        "Ignoring sticky bit issues on shared drop folders",
    ],
    [
        "What does sticky do on a directory?",
        "Why does `passwd` use setuid?",
        "Name one risk of setuid",
    ],
    ["https://man7.org/linux/man-pages/man1/chmod.1.html"],
    "perm_sticky",
)

add(
    7,
    "pipes-redirects",
    "Pipes, Redirection, and Exit Status in Pipelines",
    P3,
    "1–2 days",
    [
        "Redirect stdout/stderr to files",
        "Connect commands with pipes",
        "Use tee, here-docs, and process substitution ideas",
        "Understand pipeline exit status (`pipefail`)",
    ],
    """
## Redirection

```bash
cmd > out.txt        # stdout overwrite
cmd >> out.txt       # append
cmd 2> err.txt       # stderr
cmd > out.txt 2>&1   # both to same file
cmd < in.txt         # stdin from file
```

## Pipes

```bash
ps aux | grep nginx | awk '{print $2}'
```

Data flows left → right as streams. Prefer tools that stream over saving giant temps.

## Bash pipefail

By default, pipeline status is the last command. In scripts:

```bash
set -o pipefail
```

so failures in the middle are not hidden.
""",
    [
        "Clobbering important files with `>`",
        "Grepping `ps` for a process and matching the grep itself",
        "Ignoring stderr while debugging",
    ],
    [
        "What does `2>&1` mean?",
        "Why enable `pipefail`?",
        "What does `tee` do?",
    ],
    ["https://www.gnu.org/software/bash/manual/html_node/Redirections.html"],
    "pipe_wc",
)

add(
    8,
    "grep-find",
    "grep, ripgrep mindset, and find",
    P3,
    "1–2 days",
    [
        "Search file contents with grep",
        "Find files by name/type/time with find",
        "Combine find -exec / xargs safely",
        "Avoid unsafe parsing of filenames with spaces",
    ],
    """
## grep

```bash
grep -RIn "TODO" .
grep -E "error|warn" app.log
grep -v "^#" config   # invert
```

## find

```bash
find . -name "*.log" -mtime -1
find /var/log -type f -size +100M
find . -name "*.tmp" -delete   # careful
```

## Safe xargs

```bash
find . -name "*.txt" -print0 | xargs -0 wc -l
```

Null-delimited pipelines survive spaces/newlines in names.
""",
    [
        "Parsing `ls` output in scripts",
        "`find | xargs` without `-print0`/`-0`",
        "Recursive grep on huge binary trees without limits",
    ],
    [
        "Why `-print0`?",
        "Find files modified in last day?",
        "grep flag to show line numbers?",
    ],
    ["https://man7.org/linux/man-pages/man1/find.1.html"],
    "find_grep",
)

add(
    9,
    "sed-awk",
    "sed and awk for Text Engineering",
    P3,
    "2 days",
    [
        "Perform common sed substitutions",
        "Use awk for column processing",
        "Choose the right tool (cut/sort/uniq vs awk)",
        "Write small one-liners you can explain",
    ],
    """
## sed

```bash
sed 's/foo/bar/' file
sed -i 's/foo/bar/g' file   # in-place (GNU); on macOS sed differs
sed -n '1,20p' file
```

## awk

```bash
awk '{print $1, $3}' file
awk -F: '{print $1}' /etc/passwd
awk '$3 > 1000' data
```

awk is a tiny programming language — excellent for logs and reports.

## Classic combo

```bash
cut -d: -f1 /etc/passwd | sort | uniq
```
""",
    [
        "Blind in-place sed without backup",
        "Using awk where `cut` suffices (or vice versa for complex fields)",
        "Assuming GNU sed flags on BSD/macOS",
    ],
    [
        "What does `s/a/b/g` mean?",
        "How set awk field separator to `:`?",
        "When prefer awk over cut?",
    ],
    ["https://www.gnu.org/software/gawk/manual/"],
    "awk_sum",
)

add(
    10,
    "editors-paging",
    "Less, editors, and reading large output",
    P3,
    "1 day",
    [
        "Page output with less/more",
        "Edit files in nano or vim at a basic level",
        "Search inside less",
        "Avoid opening multi-GB logs in a GUI editor",
    ],
    """
## less

```bash
less huge.log
# /pattern  search
# n next, q quit, F follow (like tail -f)
```

## Editors

Learn **enough** vim or stick with nano while learning Linux:

```bash
nano file.txt
vim file.txt   # :wq save+quit, :q! discard
```

For infra work, vim/emacs fluency pays off over years — but do not block learning shell on editor mastery.
""",
    [
        "cat-ing multi-GB files to the terminal",
        "Getting stuck in vim without knowing `:q!`",
        "Editing production configs without backups",
    ],
    [
        "How search in less?",
        "How quit vim without saving?",
        "Why page instead of cat?",
    ],
    ["https://www.vim.org/"],
    "less_quiz",
)

add(11, "processes", "Processes: ps, top, /proc, signals", P4, "1–2 days",
    ["List and interpret processes", "Read process state from /proc", "Send signals with kill", "Understand PID, PPID, zombie/orphan concepts"],
    """
## Viewing processes

```bash
ps aux
ps -ef
top    # or htop if installed
```

Columns to care about: PID, USER, %CPU, %MEM, COMMAND.

## /proc

```bash
ls /proc/self
cat /proc/$$/status | head
```

Each PID has a directory under `/proc` with fds, environ, cmdline (Linux).

## Signals

```bash
kill -TERM <pid>   # polite stop (15)
kill -KILL <pid>   # force (9) — last resort
kill -HUP <pid>    # often reload config
```

Prefer TERM before KILL. Applications should handle SIGTERM for graceful shutdown.
""",
    ["kill -9 as first resort", "Misreading CPU% in top", "Ignoring zombie processes as always urgent (often waitpid missing)"],
    ["TERM vs KILL?", "What is PPID?", "What does /proc contain?"],
    ["https://man7.org/linux/man-pages/man1/ps.1.html"],
    "proc_list")

add(12, "jobs-background", "Jobs, Background, nohup, screen/tmux intro", P4, "1 day",
    ["Run jobs in background", "Use fg/bg/jobs", "Keep sessions with tmux", "Apply nohup carefully"],
    """
## Job control

```bash
longcmd &
jobs
fg %1
Ctrl-Z   # suspend
bg
```

## tmux (learn early)

Remote work without losing sessions:

```bash
tmux new -s lab
# detach: Ctrl-b d
tmux attach -t lab
```

## nohup

```bash
nohup ./worker > worker.out 2>&1 &
```

Still prefer systemd units for real services.
""",
    ["Leaving critical prod tasks only in a laptop terminal", "nohup without log rotation", "Detaching mentally but not from tmux"],
    ["How detach tmux?", "What does & do?", "When use systemd instead of nohup?"],
    ["https://github.com/tmux/tmux/wiki"],
    "jobs_bg")

add(13, "nice-priority", "Priority, nice, and resource limits (ulimit)", P4, "1 day",
    ["Adjust niceness", "Inspect ulimit", "Explain why limits exist", "Connect to cgroups at a high level"],
    """
## nice

```bash
nice -n 10 ./batch.sh
renice 5 -p <pid>
```

Higher nice value → lower priority (be nicer to others).

## ulimit

```bash
ulimit -a
ulimit -n 4096   # open files (session)
```

Production systems set limits via systemd (`LimitNOFILE=`) or `/etc/security/limits.conf`.

## cgroups

Modern Linux isolates CPU/memory via cgroups (containers use this heavily).
""",
    ["Raising nofile without diagnosing fd leaks", "Assuming nice makes a slow disk fast", "Ignoring OOM killer symptoms"],
    ["Does higher nice mean more CPU?", "Why limit open files?", "What tech do containers use for limits?"],
    ["https://man7.org/linux/man-pages/man1/nice.1.html"],
    "ulimit_quiz")

add(14, "bash-scripting-intro", "Bash Scripting Fundamentals", P5, "2 days",
    ["Write scripts with shebang and set -euo pipefail", "Use variables, quotes, and arrays basics", "Write if/for/while", "Make scripts executable and reusable"],
    """
## Script skeleton

```bash
#!/usr/bin/env bash
set -euo pipefail

name="${1:-world}"
echo "Hello, ${name}"
```

## Quoting

- `"$var"` — expand but keep spaces together
- `'$var'` — literal
- Always quote expansions unless you intentionally word-split

## Conditionals and loops

```bash
if [[ -f "$file" ]]; then
  echo "exists"
fi

for f in *.txt; do
  echo "$f"
done
```

Prefer `[[ ]]` over legacy `[ ]` in bash.
""",
    ["Unquoted variables causing word-splitting bugs", "Omitting set -e and missing failures", "Parsing ls in scripts"],
    ["What does set -euo pipefail do?", "Why quote \"$var\"?", "Shebang purpose?"],
    ["https://mywiki.wooledge.org/BashGuide"],
    "bash_hello")

add(15, "bash-functions-args", "Functions, Arguments, and Exit Codes in Scripts", P5, "1–2 days",
    ["Define functions and local variables", "Validate arguments", "Return meaningful exit codes", "Source libraries carefully"],
    """
```bash
usage() {
  echo "Usage: $0 <input>" >&2
  exit 2
}

[[ $# -ge 1 ]] || usage
input=$1

greet() {
  local who=$1
  echo "Hi $who"
}

greet "$input"
```

Exit codes: 0 ok, non-zero failure; 2 often means misuse.

`source ./lib.sh` pulls definitions into current shell — know the blast radius.
""",
    ["Using exit inside sourced files unexpectedly", "Global variables everywhere", "Swallowing errors with `|| true` habitually"],
    ["How require at least one arg?", "local keyword purpose?", "When source vs execute?"],
    ["https://mywiki.wooledge.org/BashFAQ"],
    "bash_args")

add(16, "bash-testing", "Testing Shell Scripts and Safe Automation", P5, "1–2 days",
    ["Structure scripts for testability", "Write simple assert helpers", "Use dry-run flags", "Avoid destructive defaults"],
    """
## Testable design

- Put logic in functions
- Keep side effects at the edges
- Support `--dry-run`

```bash
assert_eq() {
  [[ "$1" == "$2" ]] || { echo "want $2 got $1" >&2; exit 1; }
}
```

This course uses small `test.sh` harnesses — same idea as unit tests.

## Safety

Never make `rm -rf $VAR/` if VAR can be empty. Guard:

```bash
[[ -n "${DIR:-}" ]] || exit 1
```
""",
    ["Empty-variable rm -rf disasters", "Untested sed -i in prod", "Scripts that only work interactively"],
    ["What is a dry-run?", "Why guard empty paths?", "How assert equality in bash?"],
    ["https://www.shellcheck.net/"],
    "bash_assert")

add(17, "networking-basics", "Networking Basics: IP, DNS, Ports", P6, "1–2 days",
    ["Explain IP, CIDR, ports at a practical level", "Query DNS with dig/nslookup/getent", "Inspect addresses with ip", "Test connectivity with ping/curl"],
    """
## Essentials

- **IP address**: host identity on a network
- **Port**: endpoint for a service (22 ssh, 80 http, 443 https)
- **DNS**: names → addresses

```bash
ip addr
ip route
dig example.com +short
getent hosts example.com
ping -c 3 1.1.1.1
curl -I https://example.com
```

On older systems you may see `ifconfig`/`route` — prefer `ip` on modern Linux.
""",
    ["Assuming ping failure means everything is down (ICMP may be blocked)", "Hardcoding IPs without DNS strategy", "Opening all ports \"temporarily\""],
    ["What is a port?", "How resolve DNS from CLI?", "ip addr shows what?"],
    ["https://man7.org/linux/man-pages/man8/ip.8.html"],
    "net_dns")

add(18, "ss-netstat-firewall", "Listening Sockets, ss, and Firewalls Intro", P6, "1–2 days",
    ["List listening ports with ss", "Map ports to processes", "Explain firewall purpose (nftables/ufw)", "Open only needed ports"],
    """
```bash
ss -tulpn
sudo ss -tulpn | grep ':22'
```

## Firewalls

- **ufw** (Ubuntu simple wrapper)
- **firewalld** (RHEL family)
- **nftables/iptables** (underlying)

```bash
sudo ufw status
sudo ufw allow 22/tcp
```

Default deny inbound is a healthy posture for servers.
""",
    ["Disabling firewall instead of opening one port", "Binding services to 0.0.0.0 unintentionally", "Forgetting IPv6 rules"],
    ["ss -tulpn meaning?", "Why default deny?", "How allow SSH on ufw?"],
    ["https://man7.org/linux/man-pages/man8/ss.8.html"],
    "net_ss")

add(19, "curl-http", "HTTP from the CLI: curl and friends", P6, "1 day",
    ["Fetch URLs with curl", "Inspect headers and status codes", "POST JSON for APIs", "Follow redirects consciously"],
    """
```bash
curl -I https://example.com
curl -sS -o body.txt -w "%{http_code}\\n" https://example.com
curl -X POST -H 'Content-Type: application/json' -d '{"a":1}' https://httpbin.org/post
```

`-sS` silent but show errors. Prefer explicit timeouts in scripts:

```bash
curl --connect-timeout 2 --max-time 10 ...
```
""",
    ["curl without timeouts hanging automation", "Leaking tokens in shell history", "Ignoring TLS verification permanently with -k"],
    ["What does -I do?", "Why set max-time?", "How send JSON POST?"],
    ["https://curl.se/docs/manual.html"],
    "curl_status")

add(20, "ssh-basics", "SSH Basics: Keys, Config, Jump Hosts", P9, "1–2 days",
    ["Generate and use SSH keys", "Write ~/.ssh/config Host entries", "Disable password auth conceptually", "Use jump hosts / ProxyJump"],
    """
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
""",
    ["Sharing private keys", "chmod 777 on .ssh", "Password auth on internet-facing SSH"],
    ["ed25519 purpose?", "What is ProxyJump?", "Recommended .ssh private key perms?"],
    ["https://www.openssh.com/manual.html"],
    "ssh_config")

add(21, "systemd-units", "systemd: Units, Services, Journals", P7, "2 days",
    ["Manage services with systemctl", "Read logs with journalctl", "Write a simple unit file", "Enable services on boot"],
    """
```bash
systemctl status ssh
sudo systemctl restart nginx
sudo systemctl enable --now nginx
journalctl -u nginx -n 100 --no-pager
journalctl -S "1 hour ago"
```

## Unit sketch

```ini
[Unit]
Description=My Worker
After=network.target

[Service]
ExecStart=/usr/local/bin/worker
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Linux servers today are systemd-centric — this is mandatory knowledge for infra.
""",
    ["kill -9 instead of systemctl stop", "Ignoring Restart= policy", "Not checking journal after failed start"],
    ["enable vs start?", "How follow service logs?", "WantedBy meaning?"],
    ["https://www.freedesktop.org/software/systemd/man/systemctl.html"],
    "systemd_quiz")

add(22, "boot-targets", "Boot Process, Targets, and Rescue Ideas", P7, "1–2 days",
    ["Describe BIOS/UEFI → bootloader → kernel → systemd", "List targets (multi-user, graphical, rescue)", "Change default target thoughtfully", "Know when to use recovery modes"],
    """
## Simplified boot chain

Firmware → bootloader (GRUB) → kernel+initramfs → systemd (pid 1) → services

```bash
systemctl get-default
systemctl list-units --type=target
```

Rescue/emergency targets help recover broken systems — practice in a VM, not only in theory.
""",
    ["Editing GRUB carelessly on the only laptop", "Setting graphical target on headless servers", "No backup before bootloader experiments"],
    ["What is pid 1?", "multi-user.target meaning?", "Why practice recovery in a VM?"],
    ["https://www.freedesktop.org/software/systemd/man/systemd.target.html"],
    "boot_quiz")

add(23, "cron-timers", "Scheduling: cron and systemd timers", P7, "1–2 days",
    ["Write crontab entries", "Prefer systemd timers for modern systems", "Handle environment differences in scheduled jobs", "Log scheduled task output"],
    """
```bash
crontab -e
# m h dom mon dow command
0 3 * * * /usr/local/bin/backup.sh
```

## systemd timers

More observable than cron on systemd distros — pair `.timer` + `.service`.

Scheduled jobs often miss env vars available interactively — use absolute paths and explicit `Environment=`.
""",
    ["Relative paths in cron", "Emailing root floods from cron noise", "Duplicate cron+timer doing same job"],
    ["Cron five fields meaning?", "Why absolute paths?", "Timer vs cron advantage?"],
    ["https://man7.org/linux/man-pages/man5/crontab.5.html"],
    "cron_parse")

add(24, "packages-apt", "Packages: apt/dpkg (Debian/Ubuntu)", P8, "1–2 days",
    ["Update and install with apt", "Query packages with dpkg/apt", "Clean caches thoughtfully", "Pin/version awareness"],
    """
```bash
sudo apt update
sudo apt install curl
apt show curl
dpkg -L curl | head
apt-cache policy curl
```

Update package indexes before install. Prefer official repos; be careful with random PPAs.

RHEL family uses `dnf`/`rpm` — concepts transfer.
""",
    ["disabling signature checks", "autoremoving blindly on prod", "mixing distro versions"],
    ["apt update vs upgrade?", "How list files owned by a package?", "Why official repos?"],
    ["https://ubuntu.com/server/docs/package-management"],
    "pkg_quiz")

add(25, "packages-dnf", "Packages: dnf/rpm (RHEL/Fedora) and Alpine apk", P8, "1 day",
    ["Map apt concepts to dnf and apk", "Install/query/remove packages", "Know when distroless/minimal images help", "Read release notes before major upgrades"],
    """
```bash
# RHEL/Fedora
sudo dnf install curl
rpm -ql curl | head

# Alpine
sudo apk add curl
```

Minimal images reduce attack surface for containers — but debugging tools may be absent (install temporarily or use sidecar debug patterns).
""",
    ["Running untrusted RPM scripts without review", "Assuming package names identical across distros", "Upgrading major releases without backups"],
    ["dnf equivalent of apt install?", "Why minimal images?", "apk is for which distro?"],
    ["https://dnf.readthedocs.io/"],
    "pkg_map")

add(26, "disks-fs", "Disks, Partitions, Filesystems, mount", P8, "2 days",
    ["List block devices", "Understand partitions vs filesystems", "Mount/umount carefully", "Check free space and inodes"],
    """
```bash
lsblk
sudo fdisk -l
df -h
df -i
sudo mount /dev/sdb1 /mnt/data
sudo umount /mnt/data
```

Know **inode exhaustion** (df -i) — many tiny files can break services while `df -h` still looks fine.

Practice partitioning only on disposable VMs/disks.
""",
    ["mkfs on the wrong disk", "umount busy filesystems without checking", "Ignoring inode usage"],
    ["lsblk shows what?", "Why df -i?", "mount purpose?"],
    ["https://man7.org/linux/man-pages/man8/lsblk.8.html"],
    "disk_df")

add(27, "lvm-fstab", "LVM Intro and /etc/fstab", P8, "1–2 days",
    ["Explain PV/VG/LV mentally", "Read fstab entries", "Add mounts safely with backups", "Use UUIDs over volatile device names"],
    """
## LVM idea

Physical volumes → volume group → logical volumes (flexible resizing).

## fstab

```bash
UUID=...  /data  ext4  defaults  0  2
```

Always backup fstab before edits. Wrong fstab can fail boot — have rescue plan (VM snapshot).
""",
    ["Using /dev/sdX names that reorder on reboot", "Editing fstab without reboot test in VM", "Shrinking filesystems without backups"],
    ["Why UUID in fstab?", "PV vs LV?", "How recover bad fstab?"],
    ["https://man7.org/linux/man-pages/man5/fstab.5.html"],
    "fstab_parse")

add(28, "logs-rsyslog", "Logging: journald, syslog, and log files", P10, "1–2 days",
    ["Find logs under /var/log", "Use journalctl effectively", "Rotate logs conceptually", "Correlate time across hosts"],
    """
```bash
sudo tail -f /var/log/syslog   # Debian-like
sudo journalctl -xe
sudo journalctl -u ssh -S today
```

Log rotation (logrotate) prevents disks filling. Centralize logs in real infra (Loki/ELK) — but master local logs first.

Keep clocks synced (chrony/ntp) or timelines lie.
""",
    ["Deleting active log files to free space the wrong way", "No retention policy", "Ignoring permission on log dirs"],
    ["Where are traditional text logs?", "journalctl -u meaning?", "Why NTP for logs?"],
    ["https://www.freedesktop.org/software/systemd/man/journalctl.html"],
    "log_grep")

add(29, "perf-basics", "Performance Basics: CPU, memory, iowait, OOM", P10, "2 days",
    ["Read load average correctly", "Spot memory pressure and OOM", "Distinguish CPU-bound vs IO-bound", "Use vmstat/iostat at a basic level"],
    """
```bash
uptime
free -h
vmstat 1 5
# iostat if sysstat installed
dmesg | grep -i oom
```

Load average must be compared to CPU count. High iowait → storage/network path, not always \"need more CPU\".

OOM killer murders processes when memory is exhausted — fix leaks/limits, don't only raise RAM forever.
""",
    ["Misreading load average", "Disabling OOM killer", "Optimizing CPU while disk is the bottleneck"],
    ["Load 4 on 2 CPUs means?", "How spot OOM?", "iowait suggests what?"],
    ["https://www.brendangregg.com/linuxperf.html"],
    "perf_load")

add(30, "troubleshooting", "Troubleshooting Method: REDUCE and Bisect", P10, "1–2 days",
    ["Apply a systematic troubleshooting loop", "Capture evidence before rebooting", "Bisect recent changes", "Write short incident notes"],
    """
## Habit loop

1. **Define** what \"broken\" means (symptom, since when, scope)
2. **Reproduce** or observe live
3. **Evidence**: logs, metrics, `ss`, disk, recent deploys
4. **Hypothesize** one change at a time
5. **Fix** + verify
6. **Notes** for future you

Rebooting loses evidence. Snapshot first when possible.

## \"Did anything change?\"

Configs, packages, certs, DNS, disks full, neighbor noisy tenant — change discipline beats heroics.
""",
    ["Changing five things at once", "Reboot as first step always", "No notes after 3am fixes"],
    ["Why capture evidence first?", "What is bisection?", "Name three evidence sources"],
    ["https://sre.google/sre-book/"],
    "trouble_method")

add(31, "permissions-acl", "ACLs and umask", P2, "1 day",
    ["Explain umask defaults", "Read basic ACLs with getfacl", "Decide when ACLs are warranted", "Avoid ACL sprawl"],
    """
```bash
umask -S
umask 022
touch /tmp/t; ls -l /tmp/t
getfacl file   # if ACL tools installed
```

umask subtracts permissions from defaults. ACLs add finer user/group rules beyond owner/group/other — powerful, easy to make unreadable systems. Prefer simple group ownership when enough.
""",
    ["umask 000 creating world-writable files", "ACLs on every directory", "Forgetting defaults on shared project dirs"],
    ["What does umask 022 yield for files?", "When use ACL vs groups?", "getfacl purpose?"],
    ["https://man7.org/linux/man-pages/man1/umask.1p.html"],
    "umask_calc")

add(32, "capabilities-seccomp", "Capabilities, seccomp, and least privilege (intro)", P9, "1–2 days",
    ["Explain Linux capabilities vs all-powerful root", "Know seccomp exists for syscall filtering", "Apply least privilege to services", "Relate to container security defaults"],
    """
Root is a bundle of **capabilities** (CAP_NET_BIND_SERVICE, CAP_SYS_ADMIN, ...).

Modern services drop capabilities; containers often start with reduced sets.
seccomp filters syscalls (Docker default profile).

You do not need to memorize every CAP — learn to ask: \"does this process need full root?\"
""",
    ["Running containers --privileged by default", "Granting CAP_SYS_ADMIN casually", "Ignoring root in containers as \"fine\""],
    ["What is a capability?", "Why avoid --privileged?", "seccomp filters what?"],
    ["https://man7.org/linux/man-pages/man7/capabilities.7.html"],
    "sec_caps")

add(33, "tls-certs", "TLS Certificates and Trust Stores (ops view)", P9, "1–2 days",
    ["Explain cert, key, chain, CA", "Inspect certs with openssl", "Know where system trust stores live", "Plan renewals before expiry"],
    """
```bash
openssl s_client -connect example.com:443 -servername example.com </dev/null 2>/dev/null | openssl x509 -noout -dates -subject
openssl x509 -in cert.pem -text -noout | head
```

Expired certs cause \"random\" production panic. Automate renewal (ACM E/Let's Encrypt) and monitor expiry.
""",
    ["Copying private keys into git", "Disabling TLS verification permanently", "Forgetting intermediate chain"],
    ["What is a CA?", "How inspect expiry?", "Why automate renewal?"],
    ["https://www.openssl.org/docs/"],
    "tls_dates")

add(34, "hardening-basics", "Host Hardening Checklist", P9, "1–2 days",
    ["Apply a practical hardening baseline", "Disable unused services", "Enforce SSH key auth", "Keep patching cadence"],
    """
## Baseline (servers)

- Updates installed regularly
- SSH: key-only, no root login, non-default port optional (not a real secret)
- Firewall default deny
- Only required packages
- Separate admin users + sudo
- Time sync on
- Disk encryption for laptops; careful key mgmt for servers

Hardening is continuous, not a one-time script from the internet blindly applied.
""",
    ["Blindly running anonymous harden scripts", "Locking yourself out of SSH", "Assuming compliance checkbox equals secure"],
    ["Name five baseline items", "Why disable unused services?", "Risk of remote harden scripts?"],
    ["https://www.cisecurity.org/"],
    "harden_list")

add(35, "docker-basics", "Docker Basics on Linux", P11, "2 days",
    ["Run containers interactively", "Understand images vs containers", "Mount volumes and publish ports", "Read container logs"],
    """
```bash
docker run --rm -it ubuntu:24.04 bash
docker run --rm -p 8080:80 nginx
docker ps -a
docker logs <id>
docker build -t myapp .
```

Containers share the host kernel — they are not VMs. Isolation is strong but not magic; harden accordingly.

Practice on Linux. Docker Desktop on Mac is OK for learning commands, but production semantics are Linux.
""",
    ["docker.sock mounted into untrusted containers", "Running as root inside without need", "Storing secrets in images"],
    ["Image vs container?", "What does --rm do?", "Why shared kernel matters?"],
    ["https://docs.docker.com/get-started/"],
    "docker_quiz")

add(36, "docker-linux-net", "Containers, Namespaces, and Networking", P11, "2 days",
    ["Name major namespaces (pid, net, mnt, user)", "Explain bridge networking basics", "Debug DNS inside containers", "Use host networking knowingly"],
    """
Linux containers = namespaces + cgroups + union filesystems.

```bash
docker network ls
docker run --rm busybox nslookup example.com
```

Network modes: bridge (default), host, none, overlay (swarm/k8s).

When networking \"feels broken\", check: DNS, published ports, firewall, and whether you expected localhost on host vs container.
""",
    ["--network host as default habit", "Assuming localhost in container is the host", "Ignoring cgroup memory limits"],
    ["What do namespaces isolate?", "Default docker network mode?", "localhost confusion?"],
    ["https://docs.docker.com/network/"],
    "ns_quiz")

add(37, "compose-k8s-lite", "Compose and Kubernetes Concepts for Operators", P11, "2 days",
    ["Read a docker-compose file", "Map pods/services/deployments mentally", "Kubectl get/describe/logs basics", "Know what Linux skills transfer to k8s nodes"],
    """
Compose: multi-container apps on one host.
Kubernetes: orchestrates containers across nodes — still Linux underneath.

```bash
kubectl get pods -A
kubectl describe pod X
kubectl logs X
kubectl exec -it X -- sh
```

Node issues are Linux issues: disk pressure, OOM, bad NICs, full inodes, clock skew.
""",
    ["Learning only kubectl YAML without Linux debugging", "exec as the only debug tool", "Running privileged pods casually"],
    ["Pod vs container?", "How fetch logs?", "Name a node-level Linux failure"],
    ["https://kubernetes.io/docs/concepts/"],
    "k8s_quiz")

add(38, "cloud-vms", "Linux on Cloud VMs: metadata, identity, disks", P11, "1–2 days",
    ["Use instance metadata thoughtfully", "Attach/mount data disks", "Prefer IAM roles over long-lived keys", "Automate with cloud-init basics"],
    """
Cloud VMs are Linux with extra APIs:

- Metadata service (IMDSv2 on AWS — hop limits matter)
- Identity via instance profiles/roles
- Ephemeral vs persistent disks
- cloud-init for first boot

```bash
# example pattern only — provider specific
curl -s http://169.254.169.254/ # know your cloud's secure usage!
```

Never expose metadata endpoints to containers/user workloads carelessly.
""",
    ["IMDSv1 on exposed hosts", "Secrets baked into AMIs", "Data on ephemeral disks only"],
    ["What is cloud-init?", "Why IAM roles over keys?", "Metadata risk?"],
    ["https://cloudinit.readthedocs.io/"],
    "cloud_meta")

add(39, "automation-ansible", "Config Automation Mindset (Ansible-oriented)", P11, "1–2 days",
    ["Prefer idempotent config management", "Separate inventory from playbooks conceptually", "Avoid snowflake servers", "Combine with immutable images when appropriate"],
    """
Ansible (and friends) apply desired state over SSH.

Principles beat tool trivia:

- Idempotent tasks
- Versioned config
- Small blast radius
- Golden images + automation hybrid

Snowflake servers that nobody can recreate are career-limiting in infra.
""",
    ["Manual SSH drift with no record", "One mega playbook without checks", "Automating before understanding"],
    ["What is idempotency?", "Why avoid snowflakes?", "SSH role in Ansible?"],
    ["https://docs.ansible.com/"],
    "auto_idemp")

add(40, "shell-text-mastery", "Shell Text Mastery Drill Week", P3, "2–3 days",
    ["Combine grep/sed/awk/sort/uniq fluently", "Write one-liners you can explain line-by-line", "Profile slow pipelines", "Prefer clarity over golf"],
    """
Drill pipelines on real logs (sample files in exercises).

Goals:

- Frequency counts
- Top-N talkers
- Field extraction
- Dedup and joins with `sort`/`join`

Clarity > cleverness. If you cannot explain it, do not ship it.
""",
    ["Unreadable golf one-liners in prod", "Loading entire huge files into arrays unnecessarily", "Locale surprises in sort"],
    ["How top-N with sort|uniq -c?", "Why LC_ALL=C sometimes?", "When rewrite as a script?"],
    ["https://www.gnu.org/software/coreutils/manual/"],
    "text_topn")

add(41, "bash-robust", "Robust Bash: errexit, nounset, traps", P5, "1–2 days",
    ["Use traps for cleanup", "Handle signals in scripts", "Create temp dirs safely", "Write scripts that fail loudly"],
    """
```bash
set -euo pipefail
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

work() { ...; }
work
```

traps ensure cleanup on exit/signals. Combined with nounset, many silent bugs become loud.
""",
    ["rm -rf unprotected tmp", "Ignoring ERR traps for critical scripts", "set +e hiding failures permanently"],
    ["What does trap EXIT do?", "mktemp why?", "nounset catches what?"],
    ["https://mywiki.wooledge.org/SignalTrap"],
    "bash_trap")

add(42, "networking-dns-deep", "DNS Debugging and /etc/resolv.conf", P6, "1 day",
    ["Read resolv.conf and systemd-resolved", "Debug NXDOMAIN vs timeout", "Understand search domains", "Cache flush awareness"],
    """
```bash
cat /etc/resolv.conf
resolvectl status   # systemd-resolved systems
dig +trace example.com
getent ahosts example.com
```

Symptoms: app \"cannot connect\" often starts as DNS. Split corporate DNS and split-horizon issues are common in infra.
""",
    ["Hardcoding 8.8.8.8 breaking private zones", "Ignoring search domain effects", "Assuming dig failure equals network down"],
    ["NXDOMAIN meaning?", "search domain effect?", "Why dig +trace?"],
    ["https://man7.org/linux/man-pages/man5/resolv.conf.5.html"],
    "dns_debug")

add(43, "http-load-tls", "Load Balancing and Reverse Proxy (Linux view)", P6, "1–2 days",
    ["Explain reverse proxy role", "Read nginx/Caddy basics at config level", "Terminate TLS at proxy", "Health checks and upstreams"],
    """
Linux hosts often run nginx/HAProxy/Envoy as edge or sidecars.

Concepts:

- Upstream pool
- Health checks
- TLS termination vs passthrough
- Access/error logs

You will configure these repeatedly in AI/gateway and microservice designs.
""",
    ["Single upstream without health checks", "Weak TLS configs", "Logging secrets at info level"],
    ["What is TLS termination?", "Why health checks?", "Where find nginx error log?"],
    ["https://nginx.org/en/docs/"],
    "proxy_quiz")

add(44, "storage-backup", "Backups, Snapshots, and Restore Drills", P8, "1–2 days",
    ["Define RPO/RTO simply", "Prefer tested restores", "Know snapshot vs backup", "Encrypt backups and manage keys"],
    """
Untested backups are fiction.

Practice:

1. Take backup
2. Restore to a clean VM
3. Measure time and document gaps

Snapshots are not offsite backups. 3-2-1 rule still applies.
""",
    ["Only on-disk snapshots in same AZ", "No restore rehearsal", "Unencrypted sensitive backups"],
    ["RPO vs RTO?", "Why restore drills?", "3-2-1 idea?"],
    ["https://www.veeam.com/blog/321-backup-rule.html"],
    "backup_quiz")

add(45, "ai-infra-linux", "Linux for AI Infrastructure", P11, "2 days",
    ["Prepare GPU hosts at OS level (drivers/toolkit conceptually)", "Tune file limits and disk for datasets", "Isolate model servers with systemd/cgroups", "Observe GPU and host metrics"],
    """
AI infra is still Linux ops:

- Drivers/toolkits (NVIDIA) + container runtimes
- Fast disks for datasets/checkpoints
- High nofile and process limits for many connections
- systemd units for inference servers
- Separating training noisy neighbors from latency-critical serving

Go/Python services you write eventually run here — OS skill multiplies app skill.
""",
    ["Sharing one GPU host with zero isolation", "Datasets on tiny root disks", "No monitoring of GPU temp/utilization"],
    ["Why nofile for inference servers?", "Where put large datasets?", "Why cgroups/systemd isolation?"],
    ["https://docs.nvidia.com/datacenter/cloud-native/"],
    "ai_linux")

add(46, "prometheus-node", "Node Metrics and Exporters (ops intro)", P10, "1–2 days",
    ["Expose node metrics conceptually", "Know RED/USE for hosts", "Alert on disk/inode/memory", "Avoid high-cardinality labels"],
    """
node_exporter + Prometheus/Grafana is a common Linux host monitoring stack.

Alert on:

- Disk >80–90%
- Inodes
- OOM events
- Systemd failed units
- Certificate expiry

Metrics without actionable alerts are wallpaper.
""",
    ["Paging on noisy low-value alerts", "No runbooks", "Cardinality explosions"],
    ["Name three host alerts", "USE method?", "Why inode alerts?"],
    ["https://prometheus.io/docs/guides/node-exporter/"],
    "metrics_quiz")

add(47, "git-on-linux", "Git on the Server and Hooks (ops angle)", P5, "1 day",
    ["Use git safely on servers", "Understand deploy keys", "Avoid editing prod checkouts casually", "Know hook basics"],
    """
Servers may pull release tags via CI, not humans SSH-editing `/opt/app`.

If git is used on hosts:

- Deploy keys read-only when possible
- Clean working trees
- Tagged releases

Prefer artifact images over \"git pull on prod\".
""",
    ["git pull as root on live main", "Write-capable deploy keys broadly", "Uncommitted hotfixes on servers"],
    ["Why immutable artifacts?", "Deploy key purpose?", "Risk of prod git pull?"],
    ["https://git-scm.com/book/en/v2"],
    "git_ops")

add(48, "selinux-apparmor", "SELinux/AppArmor Awareness", P9, "1–2 days",
    ["Know which MAC system your distro uses", "Read basic denials from logs", "Avoid setenforce 0 as permanent fix", "Apply targeted policy changes properly"],
    """
Mandatory Access Control (MAC) confines processes beyond chmod.

- RHEL family: SELinux
- Ubuntu: AppArmor

```bash
getenforce            # SELinux
sudo aa-status        # AppArmor
```

If a service fails only when confined, fix the policy — do not permanently disable MAC on prod.
""",
    ["setenforce 0 forever", "Disabling AppArmor globally", "Ignoring AVC denial logs"],
    ["SELinux vs AppArmor typical distros?", "Why not disable MAC?", "Where see denials?"],
    ["https://www.selinuxproject.org/page/Main_Page"],
    "mac_quiz")

add(49, "networking-nft", "Packet Filtering Mental Model (nftables)", P6, "1–2 days",
    ["Explain chains/tables conceptually", "Prefer high-level tools when enough (ufw/firewalld)", "Log drops thoughtfully", "Test rules remotely with care"],
    """
nftables is the modern Linux packet filter framework.

For many servers, ufw/firewalld is enough. When you need custom:

- Default drop inbound
- Allow established/related
- Explicit allow SSH before enabling drop policies
- Keep a console/VMC session when testing remotely
""",
    ["Locking yourself out mid-SSH", "Logging every accepted packet", "Contradictory overlapping rules"],
    ["Why allow established?", "How avoid lockout?", "ufw vs raw nftables?"],
    ["https://wiki.nftables.org/"],
    "nft_quiz")

add(50, "systemd-hardening", "systemd Service Hardening Directives", P7, "1–2 days",
    ["Apply ProtectSystem/NoNewPrivileges ideas", "Constrain WritablePaths", "Run as dedicated DynamicUser/User", "Read systemd-analyze security"],
    """
```ini
[Service]
User=myapp
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
```

```bash
systemd-analyze security myapp.service
```

Hardened units reduce blast radius when the app is compromised.
""",
    ["Running network services as root without need", "ProtectSystem without testing paths", "Ignoring analyze security suggestions forever"],
    ["NoNewPrivileges meaning?", "PrivateTmp purpose?", "Why dedicated User?"],
    ["https://www.freedesktop.org/software/systemd/man/systemd.exec.html"],
    "systemd_hard")

add(51, "lab-vm-practice", "Building Your Persistent Linux Lab", P0, "1–2 days",
    ["Create a disposable VM snapshot workflow", "Document lab IP/users", "Separate 'break glass' practice VMs", "Automate lab provisioning lightly"],
    """
Your lab should let you:

- Snapshot before dangerous lessons (disks, boot, firewall)
- Reset quickly
- Take notes of what broke

Suggested: Ubuntu LTS VM + second Alpine container host for contrast.
""",
    ["Practicing firewall on the only machine you own without console", "No snapshots", "Mixing prod credentials into lab"],
    ["Why snapshots?", "What two distros to compare?", "Prod creds in lab risk?"],
    ["https://ubuntu.com/download/server"],
    "lab_plan")

add(52, "interview-drills", "Linux Interview and Oncall Drills", P10, "2 days",
    ["Explain debugging aloud with structure", "Solve timed scenarios", "Write clear handoff notes", "Prioritize user impact"],
    """
Practice prompts:

- \"Site is slow\" — what do you check first 10 minutes?
- Disk full at 2am
- TLS expired
- One node NotReady in k8s
- SSH refused suddenly

Score yourself on: structure, evidence, communication, fix verification.
""",
    ["Jumping to exotic theories first", "No communication during incident", "Fixing without verifying"],
    ["First 3 checks for 'slow'?", "Why verify after fix?", "Handoff note contents?"],
    ["https://sre.google/sre-book/managing-incidents/"],
    "oncall_drill")

add(53, "capstone-server", "Capstone: Harden and Operate a Linux Web Server", P12, "3–5 days",
    ["Provision a Linux VM", "Serve a simple site behind a reverse proxy", "Add firewall, SSH hardening, systemd unit", "Document runbook + restore notes"],
    """
## Mission

Build a small but real server:

- Nginx (or Caddy) serving a static site or reverse-proxying an app
- systemd unit for the app
- ufw/firewalld with minimal ports
- SSH key-only
- journald/log rotation awareness
- Backup + restore drill of site content
- Short runbook (start/stop/debug)

## Rubric (excellent)

- Reproducible setup notes
- No password SSH
- Fails closed firewall
- Evidence of restore test
- Clean boot after reboot
""",
    ["ClickOps without notes", "Ports 0.0.0.0 wide open", "No reboot test"],
    ["What ports are open and why?", "How prove restore?", "What happens after reboot?"],
    ["https://ubuntu.com/server/docs"],
    "cap_server")

add(54, "capstone-troubleshoot", "Capstone: Broken Box Challenge", P12, "2–4 days",
    ["Debug a deliberately broken VM", "Capture timeline and root cause", "Fix with minimal change", "Write postmortem"],
    """
## Mission

Someone (you, earlier) breaks a snapshot on purpose: full disk, bad fstab, broken DNS, failed unit, wrong permissions, expired cert — pick 3+.

Restore service with a written postmortem:

- Impact
- Timeline
- Root cause
- Fix
- Prevention

## Rubric

- Structured troubleshooting
- Evidence preserved
- Minimal blast radius
- Clear prevention items
""",
    ["Recreating VM instead of debugging", "Changing everything at once", "No postmortem"],
    ["What was root cause?", "What evidence?", "What prevention?"],
    ["https://sre.google/sre-book/postmortem-culture/"],
    "cap_break")

add(55, "capstone-ai-host", "Capstone: AI Inference Host on Linux", P12, "4–6 days",
    ["Run an inference-friendly Linux host layout", "systemd + reverse proxy + TLS", "Resource limits and logs", "Load test and observe"],
    """
## Mission

Prepare a Linux host (VM is fine without real GPU) as if serving a model API:

- App under systemd (can be a mock HTTP server)
- Reverse proxy with TLS (self-signed OK in lab)
- Limits: MemoryMax / CPUQuota in unit
- Logs + simple metrics endpoint or node exporter
- Firewall only 22/443
- Runbook for deploy/rollback
- Optional: containerized mock model with compose

## Rubric

- Least privilege unit
- Documented capacity limits
- Observability hooks
- Clean failure behavior under kill -TERM
""",
    ["Privileged containers", "No memory limits", "No graceful shutdown testing"],
    ["How bound resources?", "What happens on SIGTERM?", "Which ports exposed?"],
    ["https://www.freedesktop.org/software/systemd/man/systemd.resource-control.html"],
    "cap_ai")


def _apply_expanded_bodies() -> None:
    """Overlay full lesson bodies and exercise guides from scripts/batches/."""
    from batches.batch_00_13 import EXTRA as e0
    from batches.batch_14_27 import EXTRA as e1
    from batches.batch_28_41 import EXTRA as e2
    from batches.batch_42_55 import EXTRA as e3

    extra = {**e0, **e1, **e2, **e3}
    missing = [m["n"] for m in MODULES if m["n"] not in extra]
    if missing:
        raise RuntimeError(f"expanded bodies missing for modules: {missing}")
    for m in MODULES:
        e = extra[m["n"]]
        m["body"] = e["body"]
        m["exercise_guide"] = e["exercise_guide"]
        m["exercise_examples"] = e["exercise_examples"]


_apply_expanded_bodies()

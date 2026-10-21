#!/usr/bin/env python3
"""Extra lesson content for modules 28..41 (batch 28_41).

EXTRA maps module number -> dict(body, exercise_guide, exercise_examples).
ASCII only.
"""

from __future__ import annotations

EXTRA: dict[int, dict[str, str]] = {
    28: {
        "body": r"""
## Why this matters

When something breaks at 03:00, the first question is "what did the system say
just before it broke?" Logs are the system's own answer. On a modern Linux host
two worlds overlap: **systemd-journald** (binary journal, queried with
`journalctl`) and **syslog** (plain text files such as `/var/log/syslog` or
`/var/log/messages`, written by rsyslog). You must be able to read both, filter
fast, and know when logs are being lost or have filled the disk.

Skill goal: go from "the service is down" to the exact error line in under two
minutes, without scrolling through a million lines.

## Core concepts

| Term | Meaning |
|------|---------|
| journald | Service that collects stdout/stderr of units, kernel messages, and syslog() calls into a structured journal |
| journalctl | Query tool for the journal (filter by unit, time, priority, boot) |
| rsyslog | Classic syslog daemon; writes text files and can forward over the network |
| facility | Source category: kern, auth, daemon, user, local0-local7 |
| priority | Severity 0-7: emerg, alert, crit, err, warning, notice, info, debug |
| persistent journal | Journal kept in `/var/log/journal` and surviving reboot |
| volatile journal | Journal kept in `/run/log/journal`, lost on reboot |
| logrotate | Periodic rename/compress/delete of text logs so they do not fill disk |

```
 app stdout/stderr --+
 syslog() call ------+--> journald --+--> /var/log/journal (persistent)
 kernel (dmesg) -----+               |--> /run/log/journal (volatile)
                                     +--> rsyslog --> /var/log/syslog, auth.log
                                                  \--> remote log server
```

The most important flag to memorize is `-u UNIT`: show only messages from one
systemd unit. `journalctl -u nginx` beats `grep nginx` over everything.

## Worked examples

Show the last 50 lines of one service, then follow live:

```bash
journalctl -u ssh -n 50 --no-pager
journalctl -u ssh -f
```

Only errors and worse since this boot:

```bash
journalctl -b -p err
```

Time window (absolute or relative):

```bash
journalctl --since "2026-10-21 09:00" --until "2026-10-21 09:30"
journalctl --since "-15 min" -u nginx
```

Previous boot (needs a persistent journal), useful after a crash or reboot:

```bash
journalctl --list-boots
journalctl -b -1 -p warning
```

Kernel messages only (like dmesg, but with timestamps and boot selection):

```bash
journalctl -k
dmesg --ctime | tail
```

Machine-readable output for scripts:

```bash
journalctl -u myapp -o json --no-pager | head -n 1
journalctl -u myapp -o cat       # message text only
```

Write a log line yourself and find it again:

```bash
logger -t labtest -p user.notice "hello from the lab"
journalctl -t labtest -n 3 --no-pager
grep labtest /var/log/syslog 2>/dev/null | tail -n 3
```

Check disk usage of the journal and trim it:

```bash
journalctl --disk-usage
sudo journalctl --vacuum-size=200M
sudo journalctl --vacuum-time=14d
```

Make the journal persistent if the directory is missing:

```bash
sudo mkdir -p /var/log/journal
sudo systemctl restart systemd-journald
```

## Mini-lab

1. Run `journalctl -u ssh -n 20 --no-pager` (use `sshd` on RHEL-like hosts).
   Which fields appear on each line? Identify host, unit tag, and PID.
2. Run `logger -t lab28 "marker one"`; find it with `journalctl -t lab28`.
3. Run `journalctl -p err -b --no-pager | wc -l`. How many errors this boot?
4. Run `journalctl --disk-usage`. Is the journal persistent? Check with
   `ls /var/log/journal`.
5. Look at `/etc/logrotate.d/` and open one file. Identify rotate count,
   frequency, and the compress setting.
6. In a script, write a function that prints the flag you use to restrict
   `journalctl` to one unit. That is the exercise for this module.

Expected-style output of step 2:

```
Oct 21 10:02:11 host lab28[2314]: marker one
```

## Decision guide / failure modes

| Symptom | First move |
|---------|-----------|
| One service misbehaves | `journalctl -u UNIT -n 100` |
| Host rebooted unexpectedly | `journalctl --list-boots`, then `-b -1 -p err` |
| No logs from before reboot | Journal is volatile; create `/var/log/journal` |
| Disk full under `/var/log` | `du -xh /var/log \| sort -h \| tail`, vacuum journal, fix rotation |
| Need logs from many hosts | Forward with rsyslog or a shipping agent |
| Auth problems | `journalctl -t sshd` or `/var/log/auth.log` |

Failure modes to watch for:

- **Silent app**: app logs to a file you forgot about; systemd captures only
  stdout/stderr. Run it with `systemctl cat UNIT` and check `ExecStart`.
- **Rate limiting**: journald drops bursts ("Suppressed N messages"). A noisy
  loop can hide the real error.
- **Clock jumps**: wrong time makes `--since` windows miss events. Check
  `timedatectl`.
- **Permissions**: non-root users see only their own logs unless they are in
  the `systemd-journal` or `adm` group.
- **Unbounded logs**: a debug-level app fills the disk; set `SystemMaxUse=` in
  `/etc/systemd/journald.conf` and enable logrotate for text files.
- **Grep-only habit**: grepping text logs misses journal-only entries. Prefer
  `journalctl` filters first, grep second.
""",
        "exercise_guide": r"""Open `exercise.sh` and implement `journal_unit_flag` so it prints the
single `journalctl` option that restricts output to one systemd unit.
This is a vocabulary drill: the function must print just the flag, with no
extra text and no trailing spaces. Then run `./test.sh` until it is green.
After that, run the real command on a Linux host against a unit you know
(for example ssh or cron) and paste three output lines into your notes.""",
        "exercise_examples": r"""Expected behavior:

```
$ source exercise.sh
$ journal_unit_flag
-u
```

Real-world use of the same flag:

```
$ journalctl -u ssh -n 3 --no-pager
```

Common mistake: printing `--unit` or `-u nginx`. The test wants only the short
flag `-u`.

Self-check: run `bash -c 'source exercise.sh; journal_unit_flag'` from the exercise directory (replace journal_unit_flag with your function name) and compare by eye, then run `./test.sh`. Also confirm there is no trailing whitespace in the output.""",
    },
    29: {
        "body": r"""
## Why this matters

"The server is slow" is not a diagnosis. Performance work on Linux means
finding which of four resources is saturated: **CPU**, **memory**, **disk I/O**,
or **network**. Each one has a different signature and a different fix. Guessing
wastes hours; a five-minute structured look usually finds the bottleneck. This
module also covers the **OOM killer**, which silently ends processes when
memory runs out and is a frequent cause of "random" service crashes.

## Core concepts

| Resource | Quick tool | Signature of saturation |
|----------|-----------|-------------------------|
| CPU | `uptime`, `top`, `mpstat` | load above core count, high `%us`/`%sy`, run queue long |
| Memory | `free -h`, `vmstat` | low `available`, swap in/out (`si`/`so`), OOM kills |
| Disk I/O | `iostat -x`, `iotop` | high `%util`, high `await`, high `%wa` in top |
| Network | `ss -s`, `sar -n DEV` | drops, retransmits, link at line rate |

Load average (1, 5, 15 minute) counts tasks that are running **or waiting for
CPU or uninterruptible I/O**. Compare it with the number of CPUs:

```
 load < cpus    : headroom
 load ~ cpus    : fully busy, little slack
 load > cpus    : tasks are queueing (CPU or D-state I/O wait)
```

`iowait` (`%wa`) is CPU time spent idle while disk requests are outstanding. A
high value means "waiting on storage", not "CPU is busy".

```
  request --> CPU --> page cache --hit--> done
                         |
                        miss
                         v
                  block layer --> disk --> done   (this wait shows as iowait)
```

Linux uses spare RAM as page cache, so low "free" is normal. Look at
**available** instead.

## Worked examples

CPU count and load, then decide if busy (the exercise logic):

```bash
nproc
uptime
# load_busy CPUS LOAD -> yes if LOAD > CPUS
awk -v c=2 -v l=4 'BEGIN{print (l>c)?"yes":"no"}'
```

Who burns CPU right now:

```bash
top -b -n1 | head -n 15
ps -eo pid,comm,%cpu,%mem --sort=-%cpu | head
```

Memory view:

```bash
free -h
vmstat 1 5
grep -E 'MemAvailable|SwapFree' /proc/meminfo
```

In `vmstat`, watch columns: `r` (runnable), `b` (blocked), `si/so` (swap),
`bi/bo` (blocks in/out), `wa` (iowait).

Disk view:

```bash
iostat -x 1 3
iotop -o        # needs root
```

Find an OOM kill after the fact:

```bash
journalctl -k | grep -i -E 'out of memory|oom'
dmesg -T | grep -i 'killed process'
```

Typical kernel line:

```
Out of memory: Killed process 4121 (java) total-vm:8123456kB, anon-rss:3912000kB
```

Per-process memory and OOM score:

```bash
ps -eo pid,comm,rss --sort=-rss | head
cat /proc/$$/oom_score
```

Create controlled load for practice:

```bash
timeout 10 sh -c 'while :; do :; done' &
uptime
```

## Mini-lab

1. Record `nproc` and `uptime`. Decide: is the load above the CPU count?
2. Start two busy loops as above (one per core is enough to see effect). Watch
   `top` and note %us and load growth over a minute.
3. Run `vmstat 1 5` idle, then during a heavy `dd if=/dev/zero of=/tmp/x
   bs=1M count=500 oflag=dsync`. Compare `bo` and `wa`.
4. Run `free -h`. Explain the difference between `free` and `available`.
5. Search the kernel log for OOM lines. If none, explain what you would look for.
6. Clean up: `kill %1 %2`, `rm -f /tmp/x`.

## Decision guide / failure modes

| Observation | Likely cause | Next step |
|-------------|--------------|-----------|
| load high, `%us` high | CPU-bound process | `top`, profile app, scale out |
| load high, CPU idle, `%wa` high | storage wait | `iostat -x`, check disk, NFS, noisy neighbor |
| `si/so` nonzero constantly | memory pressure, swapping | find big RSS, add RAM or limit |
| process vanished, no app error | OOM kill | check `dmesg`/journal, set limits |
| load high, many `D` state procs | stuck I/O (NFS, dying disk) | `ps -eo stat,comm \| grep '^D'` |
| `%sy` high | syscalls, network, context switching | `strace -c`, `perf top` |

Failure modes to watch for:

- Reading load without knowing the CPU count. Load 4 is fine on 16 cores and a
  disaster on 1.
- Treating `iowait` as CPU use. It is idle time that is blocked on I/O.
- Panicking over low `free` memory when `available` is large.
- Fixing the symptom: raising swap hides a leak. Find the growing RSS.
- Container limits: a cgroup can OOM-kill a process while the host has plenty
  of free RAM. Check `docker inspect` memory limits and `memory.events`.
- One-shot measurements: sample over time (`vmstat 1`, `iostat 1`). A single
  snapshot misses bursts.
""",
        "exercise_guide": r"""Implement `load_busy CPUS LOAD` in `exercise.sh`. It must print `yes`
when the load average is strictly greater than the CPU count and `no`
otherwise (equal means not busy). Load values can be decimals such as 2.5,
so use `awk` rather than shell integer math. Run `./test.sh`, then try your
function with the real values from `nproc` and `uptime` on your machine. Keep the function body to one line; the goal is recall of the lesson vocabulary, not cleverness. Finish by re-reading the Decision guide table and noting one failure mode you could have caused yourself.""",
        "exercise_examples": r"""Expected behavior:

```
$ load_busy 2 4
yes
$ load_busy 4 1
no
$ load_busy 4 4
no
$ load_busy 2 2.5
yes
```

Hint: `awk -v c="$1" -v l="$2" 'BEGIN{print (l>c)?"yes":"no"}'` compares
numbers, not strings, because of the `-v` numeric strings.

Self-check: run `bash -c 'source exercise.sh; load_busy 2 4'` from the exercise directory (replace load_busy 2 4 with your function name) and compare by eye, then run `./test.sh`. Also confirm there is no trailing whitespace in the output.""",
    },
    30: {
        "body": r"""
## Why this matters

Most time lost in operations is not spent fixing; it is spent wandering.
Engineers change random settings, restart services "to see", and destroy the
evidence that would have shown the cause. A repeatable **troubleshooting
method** turns panic into a loop you can run in any incident, on any system,
including ones you have never seen.

## Core concepts

The method in six steps:

| Step | Name | Question answered |
|------|------|-------------------|
| 1 | define-symptom | What exactly is wrong, for whom, since when? |
| 2 | gather | What do logs, metrics, and state say right now? |
| 3 | hypothesize | What are the 2-3 most likely causes? |
| 4 | test | Which cheap, safe test separates the hypotheses? |
| 5 | fix | Apply one change, minimal and reversible |
| 6 | verify and record | Is the symptom gone? What did we learn? |

```
  define-symptom --> gather --> hypothesize --> test --+
        ^                                              |
        |                                       cause found?
        |                                         no /    \ yes
        +--------------- refine ------------------+       fix --> verify --> record
```

The first step is always **define-symptom**. "The website is down" becomes:
"`GET /health` returns 502 from the office network since 09:40; staging is
fine; the last deploy was at 09:35." A precise symptom prunes the search tree.

A second habit is to **work the layers**, bottom to top or top to bottom, never
randomly:

```
 app      : is the process running? errors in its log?
 service  : systemctl status, ports listening (ss -ltnp)
 network  : can I reach the host? DNS? firewall? (ping, curl, dig)
 os       : disk full? memory? load? (df, free, uptime)
 hardware : dmesg errors, SMART, NIC link
```

## Worked examples

Symptom: "the app returns 502."

```bash
# 1 define: who, what, when
curl -sS -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8080/health
# 2 gather
systemctl status myapp --no-pager
journalctl -u myapp -n 50 --no-pager
ss -ltnp | grep 8080
df -h /; free -h
# 3 hypothesize: process dead? port taken? disk full? bad config?
# 4 test cheaply
ss -ltnp | grep -c ':8080'      # 0 means nothing listening
journalctl -u myapp -p err -n 5
# 5 fix one thing
sudo systemctl restart myapp
# 6 verify
curl -sS -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8080/health
```

Symptom: "cannot SSH to the host."

```bash
ping -c2 HOST             # network up?
nc -vz HOST 22            # port reachable?
ssh -v user@HOST          # which stage fails: connect, key, auth?
```

Bisect a change: if the system worked yesterday, ask "what changed?"

```bash
ls -lt /etc | head
journalctl --since yesterday | grep -i -E 'upgrade|install'
last -x | head
```

Compare with a known-good machine:

```bash
diff <(ssh good 'sysctl -a 2>/dev/null' | sort) <(sysctl -a 2>/dev/null | sort)
```

Write notes as you go:

```
10:02 symptom: 502 on /health since 09:40
10:05 gather: myapp inactive (dead), journal: "Permission denied: /var/lib/app"
10:08 hypothesis: dir ownership changed by deploy
10:09 test: ls -ld /var/lib/app -> root:root
10:10 fix: chown app:app /var/lib/app; restart
10:11 verify: 200 OK
```

## Mini-lab

1. Break a service on purpose: create a systemd unit or a script that exits 1,
   or stop `cron` in a throwaway VM.
2. Write the symptom in one sentence before touching anything.
3. List three hypotheses and one test for each. Run the tests in order of
   cheapest first.
4. Apply a single fix, verify, and write a three-line incident note.
5. Repeat with a different fault: fill a small tmpfs (`mount -t tmpfs -o
   size=1m none /mnt/t`) and see how the app fails.

## Decision guide / failure modes

| Situation | Do this |
|-----------|---------|
| Symptom vague | Reproduce it, capture exact error text and time |
| Many possible causes | Test the cheapest or most likely first |
| Problem started after a change | Roll back or diff the change first |
| Cannot reproduce | Add logging or metrics, wait for next occurrence |
| Production at risk | Mitigate first (failover, rollback), diagnose after |
| Stuck for 30 min | Explain the problem aloud to someone; recheck assumptions |

Failure modes:

- **Changing many things at once**: you will not know which one fixed it.
- **Restart first**: a restart clears memory, locks, and logs that held the
  clue. Capture state (`ss`, `ps`, `journalctl`) before restarting.
- **Trusting assumptions**: "DNS is fine" must be tested with `dig`, not
  remembered.
- **Confirmation bias**: look for evidence that would disprove your favorite
  hypothesis.
- **No record**: the same incident returns in a month. Write down cause, fix,
  and detection.
- **Skipping verification**: "should work now" is not a test. Run the original
  failing action again.
""",
        "exercise_guide": r"""Implement `first_troubleshooting_step` in `exercise.sh` so it prints the
name of the very first step in the method from this lesson. Use the
exact hyphenated token from the table (lowercase, with a hyphen, no spaces).
Run `./test.sh` until green. Then write the six steps from memory in your
notes and apply them to one real problem you have had recently. Keep the function body to one line; the goal is recall of the lesson vocabulary, not cleverness. Finish by re-reading the Decision guide table and noting one failure mode you could have caused yourself.""",
        "exercise_examples": r"""Expected behavior:

```
$ first_troubleshooting_step
define-symptom
```

Not accepted: `Define symptom`, `define_symptom`, `gather`, or `restart`.
The test compares the output exactly, so no extra spaces or newline tricks.

Self-check: run `bash -c 'source exercise.sh; first_troubleshooting_step'` from the exercise directory (replace first_troubleshooting_step with your function name) and compare by eye, then run `./test.sh`. Also confirm there is no trailing whitespace in the output.""",
    },
    31: {
        "body": r"""
## Why this matters

Classic Unix permissions (owner, group, other) cannot express "alice may read,
bob may write, everyone else nothing" on one file. **ACLs** (access control
lists) can. And every file your programs create gets its initial permissions
from the **umask**, so a wrong umask silently leaks secrets or breaks shared
directories. This module ties both together so you can predict who can access
what before you test it.

## Core concepts

| Concept | Meaning |
|---------|---------|
| umask | Bits removed from the default creation mode |
| default mode | 666 for files, 777 for directories (before umask) |
| ACL entry | Extra rule such as `user:alice:rw-` or `group:dev:r-x` |
| mask | Upper bound for named users, named groups, and the owning group |
| default ACL | ACL on a directory inherited by new files inside it |
| setfacl/getfacl | Tools to set and show ACLs |

umask arithmetic (subtract the bits, do not subtract the number blindly):

```
 file default   666  = rw- rw- rw-
 umask 022           = --- -w- -w-   (bits to remove)
 result         644  = rw- r-- r--

 dir default    777  = rwx rwx rwx
 umask 022
 result         755  = rwx r-x r-x

 umask 077 -> files 600, dirs 700   (private)
 umask 002 -> files 664, dirs 775   (group collaboration)
```

Files never get the execute bit from creation alone, which is why `touch` with
umask 022 produces 644, not 755.

ACL evaluation order:

```
 1. owner matches        -> owner entry
 2. named user matches   -> user:NAME entry  AND mask
 3. group(s) match       -> owning group or named group entries AND mask
 4. otherwise            -> other entry
```

## Worked examples

Check and change umask in the current shell:

```bash
umask            # prints 0022
umask -S         # u=rwx,g=rx,o=rx
umask 077
touch private.txt && mkdir private.d
ls -ld private.txt private.d
```

Expected:

```
-rw------- 1 you you 0 Oct 21 10:30 private.txt
drwx------ 2 you you 4096 Oct 21 10:30 private.d
```

Return to the usual default and confirm file mode 644:

```bash
umask 022
touch normal.txt
stat -c '%a %n' normal.txt     # 644 normal.txt
```

Grant one extra user access with an ACL:

```bash
sudo apt install acl            # or: sudo dnf install acl
setfacl -m u:bob:rw report.txt
getfacl report.txt
ls -l report.txt                # note the trailing +
```

Sample getfacl output:

```
# file: report.txt
# owner: you
# group: you
user::rw-
user:bob:rw-
group::r--
mask::rw-
other::r--
```

Remove one entry or all entries:

```bash
setfacl -x u:bob report.txt
setfacl -b report.txt
```

Shared project directory with inheritance:

```bash
sudo mkdir /srv/proj
sudo chgrp dev /srv/proj
sudo chmod 2775 /srv/proj                 # setgid keeps group dev
sudo setfacl -d -m g:dev:rwx /srv/proj    # default ACL for new files
sudo setfacl -d -m o::--- /srv/proj       # others get nothing
```

Persist umask for services: set `UMask=0027` in the systemd unit, or edit
`/etc/login.defs` and shell profile for logins.

## Mini-lab

1. Run `umask`. Predict the mode of a new file and a new directory. Create
   both and compare with `stat -c '%a %n'`.
2. Set `umask 027`, create again, predict, verify. Then restore your umask.
3. Create `report.txt`, give a second user (or `nobody` via sudo test) read
   access via `setfacl`. Confirm with `getfacl` and `sudo -u nobody cat`.
4. Lower the mask with `setfacl -m m::r-- report.txt` and observe that the
   named user's effective permission drops (getfacl shows `#effective:`).
5. Create the shared directory with a default ACL and verify a new file
   inside inherits the entries.

## Decision guide / failure modes

| Need | Use |
|------|-----|
| Default privacy for new files | umask 077 or 027 |
| Team shares a directory | group + setgid + umask 002, or default ACL |
| One extra user on one file | `setfacl -m u:NAME:perm` |
| Many users, many rules | groups first; ACLs only where groups do not fit |
| Backup/copy must keep ACLs | `cp -a`, `rsync -A`, `tar --acls` |

Failure modes:

- **Subtracting numbers**: 666 - 022 happens to work, but 666 - 027 style math
  breaks with odd digits. Think in bits.
- **Forgetting the mask**: chmod on a file with ACLs changes the mask and can
  silently cut named-user access.
- **No default ACL on the directory**: new files do not inherit the access
  ACL; only default entries inherit.
- **Filesystem without ACL support**: mount option `acl` missing on some old
  or network filesystems.
- **`ls -l` hides detail**: a trailing `+` is the only hint; always run
  `getfacl` when permissions look odd.
- **Umask in cron/systemd differs** from your login shell, so scripts create
  files with different modes.
""",
        "exercise_guide": r"""Implement `file_mode_after_umask022` in `exercise.sh` so it prints the
octal permission of a newly created regular file under umask 022. Derive it
from the rule in the lesson (666 with the umask bits removed), then confirm
by running `umask 022; touch t; stat -c %a t` in a scratch directory. Print
only the three digits. Keep the function body to one line; the goal is recall of the lesson vocabulary, not cleverness. Finish by re-reading the Decision guide table and noting one failure mode you could have caused yourself.""",
        "exercise_examples": r"""Expected behavior:

```
$ file_mode_after_umask022
644
```

Related checks you can do by hand:

```
umask 077  -> new file 600
umask 002  -> new file 664
umask 022  -> new directory 755
```

The test expects exactly `644`, not `0644` and not `rw-r--r--`.

Self-check: run `bash -c 'source exercise.sh; file_mode_after_umask022'` from the exercise directory (replace file_mode_after_umask022 with your function name) and compare by eye, then run `./test.sh`. Also confirm there is no trailing whitespace in the output.""",
    },
    32: {
        "body": r"""
## Why this matters

Running everything as root is the oldest mistake in Linux. The kernel splits
root's power into about 40 **capabilities** so a process gets only the powers it
needs, and **seccomp** filters which system calls it may make at all. Container
runtimes use both. The single most dangerous container shortcut,
`docker run --privileged`, switches almost all of these protections off. If you
understand capabilities and seccomp you can run services with the least
privilege that still works.

## Core concepts

| Concept | Meaning |
|---------|---------|
| capability | One slice of root power, e.g. `CAP_NET_BIND_SERVICE` |
| permitted/effective set | Capabilities a process may use / is using now |
| bounding set | Upper limit that children can never exceed |
| no_new_privs | Flag preventing gaining privilege through exec (setuid) |
| seccomp | Kernel filter: allow, deny, or kill on specific syscalls |
| seccomp profile | JSON list of allowed syscalls, used by Docker/systemd |
| LSM | AppArmor or SELinux: path/label based mandatory access control |

Common capabilities:

| Capability | Allows |
|------------|--------|
| CAP_NET_BIND_SERVICE | Bind ports below 1024 |
| CAP_NET_ADMIN | Change interfaces, routes, firewall |
| CAP_NET_RAW | Raw sockets (ping, packet capture) |
| CAP_SYS_ADMIN | A huge catch-all (mount, namespaces); avoid |
| CAP_CHOWN | Change file ownership |
| CAP_SYS_PTRACE | Trace other processes |
| CAP_DAC_OVERRIDE | Bypass file permission checks |

```
 process wants to do X
        |
   [seccomp filter]  -- syscall allowed? --no--> EPERM / kill
        |yes
   [capability check] -- has the cap?   --no--> EPERM
        |yes
   [LSM: AppArmor/SELinux] -- policy ok? --no--> denied
        |yes
      done
```

`--privileged` in Docker grants all capabilities, disables the default seccomp
profile, exposes host devices, and relaxes the LSM. Treat it as "root on the
host". The safer pattern is drop everything, add back the one you need.

## Worked examples

See your own shell's capability sets:

```bash
grep Cap /proc/$$/status
capsh --decode=0000000000000000       # decode a hex mask (libcap tools)
getpcaps $$
```

Give a binary just one capability instead of setuid root:

```bash
sudo setcap 'cap_net_bind_service=+ep' ./myserver
getcap ./myserver
./myserver --port 80          # works as a normal user
sudo setcap -r ./myserver     # remove
```

Find risky files with capabilities or setuid bits:

```bash
getcap -r / 2>/dev/null
find / -xdev -perm -4000 -type f 2>/dev/null
```

Docker: least privilege run.

```bash
docker run --rm -it \
  --cap-drop ALL --cap-add NET_BIND_SERVICE \
  --read-only --security-opt no-new-privileges \
  --user 1000:1000 nginx:alpine
```

Compare with the one to avoid:

```bash
docker run --rm -it --privileged ubuntu:24.04 bash   # avoid in production
```

Check that a container is restricted:

```bash
docker run --rm alpine sh -c 'grep Cap /proc/self/status'
docker run --rm --privileged alpine sh -c 'grep CapEff /proc/self/status'
```

The privileged one shows a mask with nearly all bits set.

systemd hardening of a service (no Docker needed):

```ini
[Service]
User=app
NoNewPrivileges=yes
CapabilityBoundingSet=CAP_NET_BIND_SERVICE
AmbientCapabilities=CAP_NET_BIND_SERVICE
SystemCallFilter=@system-service
ProtectSystem=strict
PrivateTmp=yes
```

Audit the result:

```bash
systemd-analyze security myapp.service
```

Seccomp check from inside a container:

```bash
docker run --rm alpine sh -c 'grep Seccomp /proc/self/status'
# Seccomp: 2   (filter mode active)
```

## Mini-lab

1. Print `CapEff` for your shell and for a non-privileged container. Compare.
2. Run a container with `--cap-drop ALL` and try `ping -c1 127.0.0.1`. Observe
   the failure, then add `--cap-add NET_RAW` and retry.
3. Use `setcap` to let a copy of a tiny Python HTTP server bind port 80 as a
   normal user (or explain why a container is simpler).
4. Run `systemd-analyze security` on an existing service and read the top
   three exposure findings.
5. Write down the exact Docker flag you would never put in a production run
   command. That is the exercise.

## Decision guide / failure modes

| Need | Choose |
|------|--------|
| Bind port < 1024 without root | `CAP_NET_BIND_SERVICE` or use a high port + proxy |
| Run a debugger in a container | add `SYS_PTRACE` temporarily, not privileged |
| Network tooling (tcpdump) | `NET_ADMIN`/`NET_RAW` only |
| Need full device access | pass specific `--device`, not `--privileged` |
| Service on the host | systemd sandboxing options |

Failure modes:

- "It works with --privileged" means you have not found the missing capability.
  Use `strace`, `dmesg`, and audit logs to find what was denied.
- Mounting `/var/run/docker.sock` into a container is equal to root on the host.
- Disabling seccomp (`seccomp=unconfined`) to fix one error removes all syscall
  filtering; write a small custom profile instead.
- Capabilities do not replace file permissions, users, or network policy; they
  are one layer.
- Ambient and file capabilities are lost across some exec paths and do not
  work with `no_new_privs` combinations you did not expect. Test the real unit.
""",
        "exercise_guide": r"""Implement `avoid_docker_flag` in `exercise.sh` so it prints the single
Docker run flag that grants a container nearly all host privileges and
disables most sandboxing. Print the long option exactly as typed on the
command line, including both leading dashes. When the test passes, write one
paragraph in your notes explaining what safer pair of flags (drop and add)
you would use instead and why the flag you printed is dangerous.""",
        "exercise_examples": r"""Expected behavior:

```
$ avoid_docker_flag
--privileged
```

Safer pattern to remember (not part of the test):

```
docker run --cap-drop ALL --cap-add NET_BIND_SERVICE \
  --security-opt no-new-privileges IMAGE
```

The test compares the exact string, so do not add quotes, a trailing space,
or the word docker.

Self-check: run `bash -c 'source exercise.sh; avoid_docker_flag'` from the exercise directory (replace avoid_docker_flag with your function name) and compare by eye, then run `./test.sh`. Also confirm there is no trailing whitespace in the output.""",
    },
    33: {
        "body": r"""
## Why this matters

Almost every service you run speaks TLS: HTTPS sites, APIs, databases, mail,
service meshes. The most common TLS outage is boring: **a certificate expired**
and nobody noticed. The second most common is a wrong hostname or a missing
intermediate certificate. With `openssl` you can inspect any certificate or
live server in seconds, and you can create test certificates for labs.

## Core concepts

| Term | Meaning |
|------|---------|
| private key | Secret; never leaves the server; file mode 600 |
| CSR | Certificate signing request: public key plus identity, sent to a CA |
| certificate | Signed statement binding a public key to names (SAN) |
| CA | Certificate authority that signs; clients trust a set of root CAs |
| chain | Leaf cert, intermediate(s), root; server must send leaf + intermediates |
| SAN | Subject Alternative Name list; hostnames the cert is valid for |
| notBefore/notAfter | Validity window; check with `-dates` |
| PEM / DER | Text (base64) vs binary encodings |

```
 client                                   server
   | ---- ClientHello (SNI: example.com) -->|
   | <--- ServerHello + cert chain ---------|
   |  verify: signature chain to trusted root
   |          hostname matches SAN
   |          now between notBefore..notAfter
   | ---- key exchange, encrypted data ---->|
```

The flag you will use daily is `-dates`, which prints `notBefore` and
`notAfter` for a certificate.

## Worked examples

Create a throwaway self-signed certificate for lab use:

```bash
openssl req -x509 -newkey rsa:2048 -nodes -days 30 \
  -keyout lab.key -out lab.crt \
  -subj "/CN=lab.local" -addext "subjectAltName=DNS:lab.local"
chmod 600 lab.key
```

Show validity dates, subject, issuer, and SAN:

```bash
openssl x509 -in lab.crt -noout -dates
openssl x509 -in lab.crt -noout -subject -issuer
openssl x509 -in lab.crt -noout -ext subjectAltName
```

Sample `-dates` output:

```
notBefore=Oct 21 08:00:00 2026 GMT
notAfter=Nov 20 08:00:00 2026 GMT
```

Look at a live server's certificate:

```bash
echo | openssl s_client -connect example.com:443 -servername example.com 2>/dev/null \
  | openssl x509 -noout -dates -issuer -subject
```

See the whole chain and verification result:

```bash
openssl s_client -connect example.com:443 -servername example.com -showcerts </dev/null
# look for: Verify return code: 0 (ok)
```

Will it expire within 14 days? (exit code 0 means still valid after N seconds)

```bash
openssl x509 -in lab.crt -noout -checkend $((14*24*3600)) \
  && echo "ok for 14 days" || echo "expires soon"
```

Check that a key matches a certificate (hashes must be equal):

```bash
openssl x509 -in lab.crt -noout -pubkey | openssl sha256
openssl pkey -in lab.key -pubout | openssl sha256
```

Create a CSR for a real CA:

```bash
openssl req -new -newkey rsa:2048 -nodes -keyout site.key -out site.csr \
  -subj "/CN=www.example.org"
openssl req -in site.csr -noout -text | head -n 20
```

Test with curl, including a custom CA:

```bash
curl -v https://example.com 2>&1 | grep -E 'subject|expire|issuer'
curl --cacert lab.crt --resolve lab.local:8443:127.0.0.1 https://lab.local:8443/
```

Quick local TLS server for tests:

```bash
openssl s_server -accept 8443 -cert lab.crt -key lab.key -www
```

## Mini-lab

1. Generate the lab certificate above with a 2-day lifetime.
2. Print dates with `-dates` and convert `notAfter` to epoch with `date -d`.
3. Run `-checkend 86400` and `-checkend 259200`; explain both exit codes.
4. Start `s_server` and connect with `s_client`. Find `Verify return code`
   and explain why it is not 0 for a self-signed cert.
5. Check the real `notAfter` of two public sites and write a small loop that
   prints `host days_left` for each.

```bash
for h in example.com openai.com; do
  end=$(echo | openssl s_client -connect $h:443 -servername $h 2>/dev/null \
        | openssl x509 -noout -enddate | cut -d= -f2)
  echo "$h $(( ( $(date -d "$end" +%s) - $(date +%s) ) / 86400 ))"
done
```

## Decision guide / failure modes

| Symptom | Likely cause | Check |
|---------|--------------|-------|
| Browser: expired | notAfter passed | `-dates` |
| Hostname mismatch | name not in SAN | `-ext subjectAltName` |
| Works in browser, fails in curl/Java | missing intermediate | `s_client -showcerts` |
| Unknown CA | private CA not trusted | add to trust store or `--cacert` |
| Server will not start | key does not match cert | compare pubkey hashes |
| Random clients fail | wrong clock | `timedatectl`, chrony |

Failure modes:

- Renewing the file but not reloading the service; the old cert stays in memory.
- Putting the private key in git or mode 644.
- Forgetting `-servername`, so a multi-site server returns the default cert.
- Automating issuance (ACME/certbot) without monitoring; always alert at 14
  and 7 days before expiry.
- Using `-k` or `verify=False` "temporarily" and shipping it.
""",
        "exercise_guide": r"""Implement `openssl_show_dates_flag` in `exercise.sh` so it prints the
option for `openssl x509` that outputs the `notBefore` and `notAfter`
validity dates of a certificate. Print only the option with its leading dash.
After the test passes, generate a short-lived self-signed certificate as
shown in the lesson, run the option against it, and note both dates plus
how many days remain until `notAfter`. Keep the function body to one line; the goal is recall of the lesson vocabulary, not cleverness. Finish by re-reading the Decision guide table and noting one failure mode you could have caused yourself.""",
        "exercise_examples": r"""Expected behavior:

```
$ openssl_show_dates_flag
-dates
```

How the option is used in practice:

```
$ openssl x509 -in lab.crt -noout -dates
notBefore=Oct 21 08:00:00 2026 GMT
notAfter=Nov 20 08:00:00 2026 GMT
```

Do not print `-enddate` or `--dates`; the test wants exactly `-dates`.

Self-check: run `bash -c 'source exercise.sh; openssl_show_dates_flag'` from the exercise directory (replace openssl_show_dates_flag with your function name) and compare by eye, then run `./test.sh`. Also confirm there is no trailing whitespace in the output.""",
    },
    34: {
        "body": r"""
## Why this matters

Most compromises of ordinary servers are not clever. Attackers scan the
internet for password SSH, outdated packages, open databases, and forgotten
admin accounts. A small, repeatable **hardening baseline** removes the cheap
attack paths and costs an hour. This module defines a five item baseline you can
apply to any new Linux host, then automate (see the Ansible module).

## Core concepts

The baseline in five items:

| # | Item | Goal |
|---|------|------|
| 1 | ssh-keys | Key-only login, no root login, no passwords |
| 2 | firewall | Default deny inbound, allow only needed ports |
| 3 | updates | Security patches applied automatically or on schedule |
| 4 | sudo | Named admin users, least privilege, no shared root |
| 5 | ntp | Accurate time for logs, TLS, and Kerberos |

```
 internet --> [firewall: allow 22,443 only] --> [sshd: keys only]
                                                     |
                                           [sudo: named admins, logged]
                                                     |
                               [patched packages] + [synced clock + logs]
```

Principles behind the list:

- **Reduce attack surface**: fewer open ports, fewer installed packages, fewer
  running services.
- **Least privilege**: users and services get the minimum rights.
- **Defense in depth**: several independent layers, none assumed perfect.
- **Detect and recover**: logs with correct time, backups, and alerts.

Hardening is not a one-time event; it is a baseline plus periodic checking.

## Worked examples

1. SSH keys only. Edit `/etc/ssh/sshd_config.d/10-hardening.conf`:

```
PasswordAuthentication no
PermitRootLogin no
PubkeyAuthentication yes
MaxAuthTries 3
AllowUsers deploy alice
```

Validate before reloading, and keep a second session open:

```bash
sudo sshd -t && sudo systemctl reload ssh
ssh -o PreferredAuthentications=password -o PubkeyAuthentication=no host   # should fail
```

2. Firewall (Ubuntu with ufw):

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp
sudo ufw allow 443/tcp
sudo ufw enable
sudo ufw status verbose
```

Or with firewalld:

```bash
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

3. Automatic security updates:

```bash
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
systemctl status unattended-upgrades --no-pager
# RHEL family: dnf-automatic
```

4. sudo hygiene:

```bash
sudo visudo -f /etc/sudoers.d/admins     # always visudo, never plain edit
# %admins ALL=(ALL) ALL
getent group sudo
sudo passwd -l root                       # lock root password login
```

5. Time sync:

```bash
timedatectl
systemctl status systemd-timesyncd chrony --no-pager 2>/dev/null
chronyc tracking
```

Audit what is listening and what is installed:

```bash
ss -ltnup
systemctl list-unit-files --state=enabled | head -n 30
dpkg -l | wc -l
```

A tiny checker that counts how many baseline items pass:

```bash
n=0
grep -Rqs '^PasswordAuthentication no' /etc/ssh/sshd_config /etc/ssh/sshd_config.d && n=$((n+1))
ufw status 2>/dev/null | grep -q 'Status: active' && n=$((n+1))
systemctl is-enabled unattended-upgrades >/dev/null 2>&1 && n=$((n+1))
getent group sudo >/dev/null && n=$((n+1))
timedatectl show -p NTPSynchronized --value | grep -q yes && n=$((n+1))
echo "baseline items passing: $n/5"
```

## Mini-lab

1. On a throwaway VM, record `ss -ltnup` before changes.
2. Apply the five items one at a time, testing after each.
3. Confirm password SSH fails, an extra port (for example 8080) is blocked from
   another host, and `timedatectl` shows synchronized.
4. Run `lynis audit system` (if installable) and read the top suggestions.
5. Write the checker above as `baseline.sh` and run it before and after.

## Decision guide / failure modes

| Question | Answer |
|----------|--------|
| Port must be public? | If not, bind to localhost or private network |
| Many admins? | Individual accounts + sudo groups, never shared logins |
| Reboot for kernel patches? | Schedule it; consider live patching where available |
| Cloud host? | Also use provider security groups; defense in depth |
| Brute force noise? | Keys only; fail2ban is optional, not primary |

Failure modes:

- **Locking yourself out**: enabling a firewall or disabling passwords without
  testing a second session. Always test from a new terminal.
- **Firewall allow after enable**: allow SSH before turning it on.
- **Config drift**: manual changes diverge over time; enforce with automation.
- **Updates without restart**: services keep running old libraries; check
  `needrestart` or `checkrestart`.
- **Wrong time**: drifting clocks break TLS and make log correlation useless.
- **Hardening theater**: ticking boxes while leaving a database open on 0.0.0.0.
""",
        "exercise_guide": r"""Implement `count_baseline_items` in `exercise.sh` so it prints the
number of items in the hardening baseline from this lesson: ssh-keys,
firewall, updates, sudo, and ntp. Print just the number, no words. Do the
counting in your head from the table, not from the host. Afterwards, write
a one-line check for each item on your own VM and record which ones fail. Keep the function body to one line; the goal is recall of the lesson vocabulary, not cleverness. Finish by re-reading the Decision guide table and noting one failure mode you could have caused yourself.""",
        "exercise_examples": r"""Expected behavior:

```
$ count_baseline_items
5
```

The five items, in lesson order:

```
1 ssh-keys   2 firewall   3 updates   4 sudo   5 ntp
```

The test expects exactly the digit `5`. Printing `5 items` or `five` fails.
You may optionally verify by counting the words in a list with `wc -w`.

Self-check: run `bash -c 'source exercise.sh; count_baseline_items'` from the exercise directory (replace count_baseline_items with your function name) and compare by eye, then run `./test.sh`. Also confirm there is no trailing whitespace in the output.""",
    },
    35: {
        "body": r"""
## Why this matters

Containers package an application with its userland dependencies so it runs the
same on a laptop, a CI runner, and a server. Docker is the tool most people meet
first. To use it safely you need to separate four ideas: **image**, **container**,
**volume**, and **registry**, and to know the handful of `docker run` flags that
matter, especially `--rm`, which keeps your host free of dead containers.

## Core concepts

| Term | Meaning |
|------|---------|
| image | Read-only layered template (filesystem + metadata) |
| container | A running (or stopped) instance of an image |
| layer | One filesystem diff in an image; cached and shared |
| registry | Image store (Docker Hub, GHCR, private) |
| volume | Docker-managed persistent storage outside the container layer |
| bind mount | Host path mapped into the container |
| Dockerfile | Recipe to build an image |
| tag | Human label such as `nginx:1.27` (`latest` is just a tag) |

```
 Dockerfile --build--> image --run--> container
                         |               |
                      push/pull       writable layer (ephemeral)
                         v               |
                      registry      volume / bind mount (persistent)
```

Key `docker run` flags:

| Flag | Meaning |
|------|---------|
| `-d` | Detached (background) |
| `-it` | Interactive terminal |
| `--rm` | Remove container on exit |
| `-p H:C` | Publish host port H to container port C |
| `-v SRC:DST` | Mount volume or host path |
| `-e K=V` | Environment variable |
| `--name` | Fixed container name |
| `--restart` | Restart policy |

`--rm` means **remove-on-exit**: when the container's main process stops,
Docker deletes the container and its writable layer. Great for throwaway tests;
wrong for something whose logs you need to inspect after a crash.

## Worked examples

First containers:

```bash
docker run --rm hello-world
docker run --rm -it alpine:3.20 sh
docker run --rm ubuntu:24.04 cat /etc/os-release
```

Long-running service with a published port and a named volume:

```bash
docker run -d --name web -p 8080:80 -v webdata:/usr/share/nginx/html nginx:1.27
curl -sI http://127.0.0.1:8080 | head -n 1
docker ps
docker logs -f web
docker exec -it web sh
```

Inspect and clean:

```bash
docker inspect web --format '{{.State.Status}} {{.NetworkSettings.IPAddress}}'
docker stop web && docker rm web
docker images
docker image prune
docker system df
```

Build your own image:

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY app.py .
USER 10001
CMD ["python", "app.py"]
```

```bash
docker build -t myapp:0.1 .
docker run --rm myapp:0.1
```

Show the difference `--rm` makes:

```bash
docker run --name keep alpine true
docker run --rm --name gone alpine true
docker ps -a --filter name=keep --filter name=gone
# keep remains as Exited (0); gone does not exist
docker rm keep
```

Persistence check:

```bash
docker run --rm -v demo:/data alpine sh -c 'echo hi > /data/f'
docker run --rm -v demo:/data alpine cat /data/f      # hi
docker volume rm demo
```

Resource limits:

```bash
docker run --rm --memory 256m --cpus 0.5 alpine sh -c 'echo limited'
docker stats --no-stream
```

## Mini-lab

1. Run `docker run --rm alpine echo hello` and then `docker ps -a`. Is the
   container still listed? Explain via `--rm`.
2. Run nginx on port 8080, curl it, read logs, exec into it, stop and remove.
3. Write a Dockerfile that prints a message. Build, run, and inspect layers
   with `docker history`.
4. Prove a container filesystem is ephemeral: write a file, remove the
   container (no volume), start another, look for the file.
5. Do the same with a named volume and show the data survives.

## Decision guide / failure modes

| Need | Use |
|------|-----|
| One-off command or test | `docker run --rm` |
| Service | `-d --name --restart unless-stopped` + volume |
| Persist data | named volume or bind mount |
| Dev code reload | bind mount of source dir |
| Reproducible deploys | pin tags or digests, not `latest` |

Failure modes:

- **Data loss**: databases in the container layer disappear with `docker rm`.
- **Root in container**: add `USER` in the Dockerfile; avoid `--privileged`.
- **Disk full**: unused images and build cache; `docker system df`, prune.
- **Port clash**: host port already in use; check `ss -ltnp`.
- **`latest` drift**: a rebuild silently changes the base image.
- **Debugging a crash with `--rm`**: the container is gone, so its logs are gone;
  drop `--rm` while investigating.
- **Secrets baked into images**: they stay in layers; pass at runtime.
""",
        "exercise_guide": r"""Implement `docker_rm_flag_meaning` in `exercise.sh` so it prints a short
hyphenated phrase describing what `docker run --rm` does when the
container's main process ends. Use the exact phrase from the lesson, all
lowercase with hyphens. Once the test passes, run the `keep` versus `gone`
experiment from the Worked examples on a machine with Docker and write down
which container remained and why. Keep the function body to one line; the goal is recall of the lesson vocabulary, not cleverness. Finish by re-reading the Decision guide table and noting one failure mode you could have caused yourself.""",
        "exercise_examples": r"""Expected behavior:

```
$ docker_rm_flag_meaning
remove-on-exit
```

What the real flag does:

```
$ docker run --rm alpine echo hi
hi
$ docker ps -a
(no exited alpine container is listed)
```

Do not print `delete`, `remove on exit` with spaces, or the flag itself; the
test compares to `remove-on-exit` exactly.

Self-check: run `bash -c 'source exercise.sh; docker_rm_flag_meaning'` from the exercise directory (replace docker_rm_flag_meaning with your function name) and compare by eye, then run `./test.sh`. Also confirm there is no trailing whitespace in the output.""",
    },
    36: {
        "body": r"""
## Why this matters

A container is not a small VM. It is an ordinary Linux process placed in
**namespaces** (what it can see) and **cgroups** (how much it can use). When a
container cannot reach the internet, or two containers cannot talk, the answer
is almost always in Linux networking you already know: network namespaces,
veth pairs, bridges, iptables/nftables NAT, and routing. Understanding this
turns "Docker networking is magic" into commands you can run.

## Core concepts

| Namespace | Isolates |
|-----------|----------|
| pid | Process IDs (container sees itself as PID 1) |
| net | Interfaces, routes, ports, firewall rules |
| mnt | Mount table / root filesystem |
| uts | Hostname |
| ipc | Shared memory and queues |
| user | UID/GID mapping |
| cgroup | View of cgroup tree |

Docker network drivers:

| Driver | Behavior |
|--------|----------|
| bridge (default) | Containers on a private Linux bridge `docker0`, NAT to the outside |
| host | Shares the host's network namespace; no isolation, no port mapping |
| none | Only loopback |
| user-defined bridge | Like bridge, with DNS names between containers |

The default Docker network is **bridge**.

```
 container A (netns)        container B (netns)
   eth0 172.17.0.2            eth0 172.17.0.3
     |  veth                    |  veth
 ----+--------------------------+----  docker0 bridge 172.17.0.1
                  |
              iptables NAT (MASQUERADE)  <-- outbound
              DNAT host:8080 -> 172.17.0.2:80  <-- published ports
                  |
                host eth0 --> internet
```

Each container's `eth0` is one end of a **veth pair**; the other end is attached
to the bridge on the host. Outbound traffic is masqueraded to the host IP;
inbound published ports use DNAT rules.

## Worked examples

List networks and inspect the default:

```bash
docker network ls
docker network inspect bridge --format '{{range .IPAM.Config}}{{.Subnet}} {{.Gateway}}{{end}}'
ip addr show docker0
bridge link
```

See a container's namespace from the host:

```bash
docker run -d --name n1 alpine sleep 600
pid=$(docker inspect -f '{{.State.Pid}}' n1)
sudo ls -l /proc/$pid/ns
sudo nsenter -t "$pid" -n ip addr
sudo nsenter -t "$pid" -n ip route
```

Create a namespace by hand (no Docker) to see the mechanism:

```bash
sudo ip netns add lab
sudo ip link add veth-h type veth peer name veth-c
sudo ip link set veth-c netns lab
sudo ip addr add 10.99.0.1/24 dev veth-h && sudo ip link set veth-h up
sudo ip -n lab addr add 10.99.0.2/24 dev veth-c
sudo ip -n lab link set veth-c up && sudo ip -n lab link set lo up
ping -c1 10.99.0.2
sudo ip netns exec lab ping -c1 10.99.0.1
```

Cleanup: `sudo ip netns del lab; sudo ip link del veth-h 2>/dev/null`.

User-defined bridge with name resolution:

```bash
docker network create appnet
docker run -d --name db --network appnet redis:7
docker run --rm --network appnet alpine ping -c1 db
```

On the default bridge, names do not resolve; on a user-defined one they do.

Published ports and NAT rules:

```bash
docker run -d --name w -p 8080:80 nginx:alpine
sudo iptables -t nat -L DOCKER -n
curl -sI http://127.0.0.1:8080 | head -n 1
```

Host networking and none:

```bash
docker run --rm --network host alpine ip addr | head
docker run --rm --network none alpine ip addr
```

DNS inside containers:

```bash
docker run --rm alpine cat /etc/resolv.conf
docker run --rm --dns 1.1.1.1 alpine nslookup example.com
```

## Mini-lab

1. Run two alpine containers on the default bridge. Ping by IP, then by name.
   Explain the difference.
2. Create `appnet`, repeat, and observe name resolution works.
3. Use `nsenter` to print the container's routes; identify the gateway as
   `docker0`'s address.
4. Publish a port, then find the DNAT rule in `iptables -t nat -S`.
5. Build the manual veth namespace lab and ping both directions. Clean up.
6. Name the default Docker network, which is the exercise answer.

## Decision guide / failure modes

| Symptom | Check |
|---------|-------|
| Container cannot reach internet | `ip_forward`, MASQUERADE rule, DNS in `resolv.conf` |
| Cannot reach container by name | use a user-defined network |
| Published port unreachable | firewall (ufw/firewalld), `ss -ltnp`, correct `-p` |
| Port conflict | another process owns host port |
| Two stacks clash | overlapping subnets; change `default-address-pools` |

Failure modes:

- `sysctl net.ipv4.ip_forward=0` breaks container egress.
- ufw/firewalld rules vs Docker's own iptables rules: published ports can
  bypass ufw; test from outside.
- `--network host` removes isolation and ignores `-p`.
- Assuming `localhost` inside a container is the host; it is the container.
- Corporate VPN subnets overlapping `172.17.0.0/16` cause strange routing.
""",
        "exercise_guide": r"""Implement `default_docker_network` in `exercise.sh` so it prints the
name of the network driver and network that new containers join when you
do not pass `--network`. Use the lowercase one-word name shown by
`docker network ls`. If Docker is available, confirm with `docker network
ls` and `docker inspect` on a throwaway container, and record the subnet of
that network in your notes. Keep the function body to one line; the goal is recall of the lesson vocabulary, not cleverness. Finish by re-reading the Decision guide table and noting one failure mode you could have caused yourself.""",
        "exercise_examples": r"""Expected behavior:

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
`none` exist, but they are not the default for new containers.""",
    },
    37: {
        "body": r"""
## Why this matters

Once you run more than one container, typing `docker run` by hand stops scaling.
**Docker Compose** describes a multi-container application in one YAML file on
a single host. **Kubernetes** (k8s) goes further: it schedules containers
("pods") across many machines and keeps them running. You do not need to be a
cluster administrator to benefit; you do need the basic vocabulary and the
handful of `kubectl` commands that answer "what is running and why is it
broken?" The most used of these is `kubectl logs`.

## Core concepts

| Compose term | Meaning |
|--------------|---------|
| service | One container definition (image, ports, env) |
| network | Private network where services find each other by name |
| volume | Persistent data |
| `depends_on` | Start order hint (not readiness) |

| Kubernetes term | Meaning |
|-----------------|---------|
| pod | Smallest unit: one or more containers sharing network and storage |
| deployment | Declares desired replicas of a pod; handles rolling updates |
| service | Stable virtual IP/DNS name in front of pods |
| namespace | Logical partition of cluster resources |
| configmap/secret | Configuration and sensitive data injected into pods |
| node | A machine that runs pods |
| ingress | HTTP routing into the cluster |

```
 Compose (one host)                Kubernetes (many nodes)
 +---------------------+           +--------------------------------+
 | web --> api --> db  |           | Deployment(replicas=3)         |
 +---------------------+           |   pod  pod  pod  --scheduled-> nodes
                                   | Service (stable name) <-- clients
                                   +--------------------------------+
```

Kubernetes is **declarative**: you apply desired state and controllers keep
reconciling reality toward it. If a pod dies, the deployment creates another.

## Worked examples

A Compose file, `compose.yaml`:

```yaml
services:
  web:
    image: nginx:1.27
    ports: ["8080:80"]
    depends_on: [api]
  api:
    image: myapp:0.1
    environment:
      DB_HOST: db
    depends_on: [db]
  db:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: example
    volumes: ["pgdata:/var/lib/postgresql/data"]
volumes:
  pgdata:
```

```bash
docker compose up -d
docker compose ps
docker compose logs -f api
docker compose exec db psql -U postgres -c 'select 1'
docker compose down            # keep volumes
docker compose down -v         # also delete volumes
```

Kubernetes manifest, `app.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata: {name: hello}
spec:
  replicas: 2
  selector: {matchLabels: {app: hello}}
  template:
    metadata: {labels: {app: hello}}
    spec:
      containers:
        - name: hello
          image: nginx:1.27
          ports: [{containerPort: 80}]
---
apiVersion: v1
kind: Service
metadata: {name: hello}
spec:
  selector: {app: hello}
  ports: [{port: 80, targetPort: 80}]
```

Daily kubectl loop (try with kind or minikube):

```bash
kubectl apply -f app.yaml
kubectl get pods -o wide
kubectl describe pod POD
kubectl logs POD
kubectl logs deploy/hello --tail=50 -f
kubectl logs POD -c CONTAINER --previous
kubectl exec -it POD -- sh
kubectl get events --sort-by=.lastTimestamp
kubectl rollout status deploy/hello
kubectl scale deploy/hello --replicas=4
kubectl delete -f app.yaml
```

Reading pod status:

| Status | Usual meaning | First command |
|--------|---------------|---------------|
| Pending | cannot be scheduled / image pulling | `describe pod` |
| ImagePullBackOff | wrong image name or no credentials | `describe pod` |
| CrashLoopBackOff | process exits repeatedly | `logs --previous` |
| Running but not Ready | readiness probe failing | `describe`, `logs` |
| OOMKilled | memory limit exceeded | `describe` (Last State) |

Local clusters:

```bash
kind create cluster
kubectl cluster-info
kubectl config get-contexts
kubectl config set-context --current --namespace=dev
```

## Mini-lab

1. Write the Compose file above (use `nginx` and `redis` if you lack images)
   and bring it up. Read logs of one service, then bring it down.
2. Create a local cluster with kind or minikube.
3. Apply the Deployment, scale to 3, delete one pod, and watch it return with
   `kubectl get pods -w`.
4. Break it with an image tag that does not exist. Diagnose via
   `kubectl describe pod` events.
5. Fix it, check `kubectl logs`, and port-forward:
   `kubectl port-forward svc/hello 8080:80`.

## Decision guide / failure modes

| Need | Choose |
|------|--------|
| Local dev, one machine | Compose |
| Single small server, simple stack | Compose or systemd + containers |
| Many nodes, self-healing, rolling updates | Kubernetes |
| Just logs from a pod | `kubectl logs` |
| Why is it not starting | `kubectl describe`, then events |

Failure modes:

- `depends_on` does not wait for the database to be ready; add healthchecks or
  retry logic.
- Wrong kube context: you "delete" in production. Check
  `kubectl config current-context` first.
- Logs for a crashed container need `--previous`.
- Latest tags and no resource limits make clusters unpredictable.
- Secrets in plain YAML in git. Use a secret manager or sealed secrets.
- Treating pods as pets: they are replaceable; store state in volumes or
  external services.
""",
        "exercise_guide": r"""Implement `kubectl_logs_cmd` in `exercise.sh` so it prints the two-word
command prefix you use to read the standard output of a container in a
pod. Print exactly `kubectl` followed by one space and the subcommand, with
no pod name and no flags. When the test passes, practise on a local kind or
minikube cluster: start a pod, read its logs, and also try the option that
shows the logs of a previous crashed container. Keep the function body to one line; the goal is recall of the lesson vocabulary, not cleverness. Finish by re-reading the Decision guide table and noting one failure mode you could have caused yourself.""",
        "exercise_examples": r"""Expected behavior:

```
$ kubectl_logs_cmd
kubectl logs
```

Typical real usage built on that prefix:

```
kubectl logs mypod
kubectl logs deploy/hello --tail=20
kubectl logs mypod --previous
```

The test checks the exact two-word string. `kubectl get logs` and
`kubectl log` are not valid answers.

Self-check: run `bash -c 'source exercise.sh; kubectl_logs_cmd'` from the exercise directory (replace kubectl_logs_cmd with your function name) and compare by eye, then run `./test.sh`. Also confirm there is no trailing whitespace in the output.""",
    },
    38: {
        "body": r"""
## Why this matters

On a cloud provider you do not install an operating system from an ISO. You
launch a **VM from an image**, and it must configure itself on first boot: set
the hostname, create your user, install your SSH key, install packages, and run
your setup commands. The standard tool for that on Linux is **cloud-init**.
Understanding it lets you create repeatable servers, debug "my key was not
installed", and avoid hand-configured snowflakes.

## Core concepts

| Term | Meaning |
|------|---------|
| image (AMI, qcow2, ...) | Disk template the VM boots from |
| instance type | CPU/RAM size of the VM |
| metadata service | Link-local HTTP endpoint at `169.254.169.254` giving instance info |
| user-data | Your script or cloud-config passed at launch |
| cloud-init | Boot-time agent that reads metadata and user-data and configures the VM |
| security group | Cloud firewall around the instance |
| key pair | SSH public key injected at first boot |
| ephemeral disk | Local storage lost when the instance stops/terminates |

The purpose of cloud-init: **first-boot configuration** of a generic image from
metadata and user-data.

```
 launch request (image, type, key, user-data)
        |
        v
   hypervisor boots VM --> kernel --> systemd --> cloud-init stages:
        init-local -> init (network, metadata) -> config -> final (runcmd)
                                       |
                    reads http://169.254.169.254/ (metadata + user-data)
        |
        v
  hostname set, users + keys created, packages installed, scripts run
```

Stages: `cloud-init-local`, `cloud-init`, `cloud-config`, and `cloud-final`.
Most modules run once per instance, some every boot.

## Worked examples

A cloud-config user-data file (must start with `#cloud-config`):

```yaml
#cloud-config
hostname: web-01
users:
  - name: deploy
    groups: [sudo]
    shell: /bin/bash
    sudo: "ALL=(ALL) NOPASSWD:ALL"
    ssh_authorized_keys:
      - ssh-ed25519 AAAA... you@laptop
package_update: true
packages: [nginx, fail2ban]
write_files:
  - path: /etc/motd
    content: |
      managed by cloud-init
runcmd:
  - systemctl enable --now nginx
  - [sh, -c, "echo ready > /var/tmp/ready"]
```

Validate before launch:

```bash
cloud-init schema --config-file user-data.yaml
```

Launch examples (provider CLIs differ; shown for shape only):

```bash
aws ec2 run-instances --image-id AMI --instance-type t3.micro \
  --key-name mykey --user-data file://user-data.yaml
```

Check what happened on the VM:

```bash
cloud-init status --long
sudo cat /var/log/cloud-init-output.log | tail -n 30
sudo less /var/log/cloud-init.log
sudo cloud-init analyze show
```

Read instance metadata (do this from inside the VM):

```bash
curl -s http://169.254.169.254/latest/meta-data/instance-id    # AWS IMDSv1 style
TOKEN=$(curl -sX PUT http://169.254.169.254/latest/api/token \
  -H 'X-aws-ec2-metadata-token-ttl-seconds: 60')
curl -s -H "X-aws-ec2-metadata-token: $TOKEN" \
  http://169.254.169.254/latest/meta-data/local-ipv4
cloud-init query ds.meta_data
```

Test locally without a cloud, using a container or multipass:

```bash
multipass launch 24.04 --name ci-test --cloud-init user-data.yaml
multipass exec ci-test -- cloud-init status --wait
```

Re-run on a lab VM (never on production):

```bash
sudo cloud-init clean --logs
sudo reboot
```

Basic cloud hygiene:

```bash
lsblk
df -h
ip -br addr
sudo journalctl -b -u cloud-init -u cloud-final --no-pager | tail
```

## Mini-lab

1. Write a cloud-config that creates a user, installs one package, and writes a
   file with `write_files`.
2. Launch a VM (free tier, multipass, or a local libvirt image) with it.
3. SSH in and run `cloud-init status --long`. Verify the file and package.
4. Introduce a YAML typo, relaunch, and find the error in
   `/var/log/cloud-init.log`.
5. From the VM, query metadata for the instance id and private IP.
6. Terminate the VM and write down what was lost (ephemeral disk) and what you
   can recreate from the user-data alone.

## Decision guide / failure modes

| Need | Choose |
|------|--------|
| Per-instance first-boot setup | cloud-init user-data |
| Ongoing configuration changes | Ansible or similar, not re-running cloud-init |
| Same server many times | custom image (Packer) + small user-data |
| Secrets | secret manager / instance role, not user-data |
| Debug boot | `cloud-init status`, console log, serial console |

Failure modes:

- First line must be `#cloud-config` or `#!/bin/bash`; otherwise it is ignored.
- User-data is visible to anyone who can read metadata. No secrets there.
- Scripts that need network but run too early; use `runcmd` (final stage).
- Instance with no ingress rule in the security group looks "broken" but is
  just firewalled.
- Wrong login user: images use `ubuntu`, `ec2-user`, `admin`, or `debian`.
- Treating VMs as pets. Anything done by hand disappears when you rebuild.
""",
        "exercise_guide": r"""Implement `cloud_init_purpose` in `exercise.sh` so it prints a short
hyphenated phrase that states what cloud-init is for: configuring a generic
cloud image the first time an instance boots. Use the lowercase hyphenated
form from the lesson. Afterwards, write a small cloud-config on paper or in
a file that creates one user and installs one package, and explain which
boot stage runs each part. Keep the function body to one line; the goal is recall of the lesson vocabulary, not cleverness. Finish by re-reading the Decision guide table and noting one failure mode you could have caused yourself.""",
        "exercise_examples": r"""Expected behavior:

```
$ cloud_init_purpose
first-boot-config
```

Where you see it in practice:

```
$ cloud-init status
status: done
```

The test expects exactly `first-boot-config`. Phrases such as `provisioning`,
`First Boot Config`, or `first boot configuration` will fail the comparison.

Self-check: run `bash -c 'source exercise.sh; cloud_init_purpose'` from the exercise directory (replace cloud_init_purpose with your function name) and compare by eye, then run `./test.sh`. Also confirm there is no trailing whitespace in the output.""",
    },
    39: {
        "body": r"""
## Why this matters

A server configured by hand cannot be recreated reliably. Two engineers run
slightly different commands, and a month later nobody remembers what differs
between staging and production. **Configuration management** writes the desired
state down as code, applies it to many hosts, and can be run again and again.
Ansible is popular because it needs only SSH and Python on the target (agentless)
and uses readable YAML. The key concept is **idempotency**.

## Core concepts

| Term | Meaning |
|------|---------|
| inventory | List of hosts and groups to manage |
| module | A unit of work (`apt`, `copy`, `service`, `user`) |
| task | One module call with arguments |
| play | Tasks applied to a group of hosts |
| playbook | YAML file with one or more plays |
| role | Reusable bundle of tasks, templates, defaults |
| handler | Task that runs only when notified by a change (restart on config change) |
| fact | Collected host information (`ansible_os_family`) |
| check mode | Dry run with `--check`, optionally `--diff` |

**Idempotent** means **same result if repeated**: running the playbook once or
ten times leaves the host in the same state, and later runs report "ok" rather
than "changed".

```
 playbook run 1:  [changed] [changed] [changed]   (system converges)
 playbook run 2:  [ok]      [ok]      [ok]        (nothing to do)
 someone edits server by hand
 playbook run 3:  [ok]      [changed] [ok]        (drift corrected)
```

Compare commands:

```
 non-idempotent:  echo "line" >> /etc/app.conf      (adds a line each time)
 idempotent:      lineinfile / template modules      (ensures the line exists once)
 non-idempotent:  useradd bob                       (fails the second time)
 idempotent:      user: name=bob state=present
```

## Worked examples

Inventory, `inventory.ini`:

```
[web]
web1 ansible_host=203.0.113.10 ansible_user=deploy
web2 ansible_host=203.0.113.11 ansible_user=deploy

[db]
db1 ansible_host=203.0.113.20 ansible_user=deploy
```

Ad hoc checks:

```bash
ansible all -i inventory.ini -m ping
ansible web -i inventory.ini -m command -a 'uptime'
ansible web -i inventory.ini -b -m apt -a 'name=nginx state=present update_cache=yes'
```

A playbook, `site.yml`:

```yaml
- hosts: web
  become: true
  vars:
    app_port: 8080
  tasks:
    - name: Install nginx
      ansible.builtin.apt:
        name: nginx
        state: present
        update_cache: true
    - name: Render site config
      ansible.builtin.template:
        src: site.conf.j2
        dest: /etc/nginx/conf.d/site.conf
        mode: "0644"
      notify: Reload nginx
    - name: Ensure nginx running and enabled
      ansible.builtin.service:
        name: nginx
        state: started
        enabled: true
  handlers:
    - name: Reload nginx
      ansible.builtin.service:
        name: nginx
        state: reloaded
```

Template, `site.conf.j2`:

```
server { listen {{ app_port }}; location / { return 200 "ok from {{ inventory_hostname }}\n"; } }
```

Run, preview, and prove idempotency:

```bash
ansible-playbook -i inventory.ini site.yml --check --diff
ansible-playbook -i inventory.ini site.yml
ansible-playbook -i inventory.ini site.yml     # second run: changed=0
```

Expected recap on the second run:

```
web1 : ok=4 changed=0 unreachable=0 failed=0
```

Limit and debug:

```bash
ansible-playbook site.yml -l web1 -v
ansible-playbook site.yml --tags config --start-at-task "Render site config"
ansible-lint site.yml
```

Avoid shell where a module exists; if you must use `command`, add a guard:

```yaml
- name: Initialize database once
  ansible.builtin.command: /opt/app/init-db.sh
  args:
    creates: /var/lib/app/.initialized
```

## Mini-lab

1. Use a local VM or container as the target with SSH and Python.
2. Write the inventory and run the `ping` module.
3. Create a playbook that installs a package, writes a file via `template`,
   and enables a service.
4. Run twice. Confirm the second run shows `changed=0`.
5. Manually edit the managed file on the target. Run again and observe the drift
   fix.
6. Replace one task with `shell: echo x >> file`. Run twice and see why it is
   not idempotent. Fix with `lineinfile`.

## Decision guide / failure modes

| Need | Choose |
|------|--------|
| Bootstrap new VM | cloud-init first, Ansible afterwards |
| Config for many hosts | Ansible playbooks/roles in git |
| Immutable deploys | build images; use Ansible to build them |
| One-off fix across fleet | ad hoc command, then codify it |
| Secrets | Ansible Vault or external secret store |

Failure modes:

- `shell` and `command` always report changed unless guarded with `creates`,
  `removes`, or `changed_when`.
- Editing hosts by hand makes drift; the next run may undo your hotfix.
- Forgetting `become: true` for root-only tasks.
- Typos in YAML indentation; run `ansible-playbook --syntax-check`.
- Unpinned package versions make "same playbook, different result".
- Running against production without `--check` and `-l` limits first.
""",
        "exercise_guide": r"""Implement `idempotent_means` in `exercise.sh` so it prints the hyphenated
definition used in this lesson for an idempotent operation. Use all
lowercase letters with hyphens between words and no spaces. Afterwards,
list two shell commands from your own history that are not idempotent and
write the module or guard you would use to make each of them safe to repeat. Keep the function body to one line; the goal is recall of the lesson vocabulary, not cleverness. Finish by re-reading the Decision guide table and noting one failure mode you could have caused yourself.""",
        "exercise_examples": r"""Expected behavior:

```
$ idempotent_means
same-result-if-repeated
```

Illustration of the idea:

```
$ ansible-playbook site.yml    # first run:  changed=3
$ ansible-playbook site.yml    # second run: changed=0
```

The test compares the exact string; do not add a period or capital letters.

Self-check: run `bash -c 'source exercise.sh; idempotent_means'` from the exercise directory (replace idempotent_means with your function name) and compare by eye, then run `./test.sh`. Also confirm there is no trailing whitespace in the output.""",
    },
    40: {
        "body": r"""
## Why this matters

Linux administrators spend a surprising share of their time turning text into
answers: which IP hits us most, how many 5xx errors in the last hour, which
users have no shell, which configuration value differs between servers.
Mastery of a small toolbox (`grep`, `cut`, `sort`, `uniq`, `awk`, `sed`, `xargs`,
`tr`) lets you answer such questions in one line, without writing a program. This
module consolidates earlier text lessons into reusable **recipes**, including
the "top N" pattern that powers the exercise.

## Core concepts

| Tool | Best at |
|------|---------|
| `grep` | Select lines by pattern |
| `cut` | Take fixed delimiter fields or char ranges |
| `awk` | Fields, arithmetic, conditions, simple reports |
| `sed` | Stream edits: substitute, delete, print ranges |
| `sort` | Order lines (`-n` numeric, `-r` reverse, `-k` key, `-u` unique) |
| `uniq` | Collapse **adjacent** duplicates; `-c` counts |
| `tr` | Translate or delete characters |
| `xargs` | Turn lines into command arguments |
| `paste`/`join` | Combine files side by side or by key |

The universal pipeline pattern:

```
 source --> select --> extract --> normalize --> count/aggregate --> rank
 (cat)     (grep)     (awk/cut)   (tr/sed)      (sort | uniq -c)    (sort -nr | head)
```

The frequency recipe, used in countless incidents:

```
 sort | uniq -c | sort -nr | head
```

`uniq` only merges adjacent lines, so you must `sort` before `uniq -c`.
Then sort numerically descending to rank.

## Worked examples

Sample data, `access.log`:

```
10.0.0.5 GET /index 200
10.0.0.7 GET /login 500
10.0.0.5 POST /login 200
10.0.0.5 GET /index 200
10.0.0.9 GET /admin 403
```

Top clients:

```bash
awk '{print $1}' access.log | sort | uniq -c | sort -nr | head -n 3
```

```
      3 10.0.0.5
      1 10.0.0.9
      1 10.0.0.7
```

Most frequent token (the exercise function):

```bash
top_token() {
  sort | uniq -c | sort -nr | awk 'NR==1{print $2}'
}
printf 'a\nb\na\n' | top_token      # a
```

Count status codes and find errors:

```bash
awk '{c[$4]++} END{for(k in c) print k, c[k]}' access.log | sort
awk '$4>=500' access.log
grep -c ' 200$' access.log
```

Words from a text file, case-insensitive:

```bash
tr -cs 'A-Za-z' '\n' < README.md | tr 'A-Z' 'a-z' | sort | uniq -c | sort -nr | head
```

System account recipes:

```bash
cut -d: -f1,7 /etc/passwd | grep -v 'nologin\|false'
awk -F: '$3>=1000 && $3<65000 {print $1}' /etc/passwd
```

Edit text safely:

```bash
sed -n '2,4p' access.log
sed 's/10\.0\.0\./net-A./' access.log | head -n 2
sed -i.bak 's/^PermitRootLogin yes/PermitRootLogin no/' sshd_config
```

Safe file handling with `xargs`:

```bash
find . -name '*.log' -print0 | xargs -0 grep -l ERROR
find . -name '*.tmp' -print0 | xargs -0 -r rm -v
```

Join two lists on a key:

```bash
sort -k1,1 users.txt > u.sorted; sort -k1,1 groups.txt > g.sorted
join u.sorted g.sorted
```

Diff and compare:

```bash
diff <(sort a.txt) <(sort b.txt)
comm -12 <(sort a.txt) <(sort b.txt)    # lines in both
```

## Mini-lab

1. Create the sample log and reproduce the top-clients output.
2. Remove the first `sort` from the pipeline and observe wrong counts.
3. Write `top_token` and test with tied input like `a b b a`. Note which wins
   and why (the sort order decides ties).
4. From `/etc/passwd`, list users with login shells sorted by UID.
5. Extract all IPv4-like strings from a log with
   `grep -oE '[0-9]+(\.[0-9]+){3}'` and rank them.
6. Rewrite one of your pipelines as a function in a script with a usage line.

## Decision guide / failure modes

| Task | Use |
|------|-----|
| Filter lines | `grep` |
| Split by delimiter, simple | `cut` |
| Conditions, sums, per-field logic | `awk` |
| Replace text | `sed` |
| Count distinct values | `sort | uniq -c` |
| Filenames with spaces | `-print0 | xargs -0` |

Failure modes:

- `uniq` without `sort` gives misleading counts.
- Locale changes sort order; set `LC_ALL=C` for stable results in scripts.
- `cut` fails on variable-width whitespace; use `awk` instead.
- `sed -i` without a backup suffix destroys originals on a bad regex.
- `cat file | grep` is fine for exploration but needless in scripts.
- Parsing `ls` output; use globs or `find`.
- Whole-pipeline exit status is the last command's unless `pipefail` is set.
""",
        "exercise_guide": r"""Implement `top_token` in `exercise.sh`. It reads tokens from standard input,
one per line, and prints only the most frequent token. Use the recipe from
the lesson: sort, count with `uniq -c`, sort by count descending, then
print the token column. Do not print the count. For ties, whichever token
comes first after the numeric sort is acceptable. Test with piped input using
`printf`, as `test.sh` does. Keep the function body to one line; the goal is recall of the lesson vocabulary, not cleverness. Finish by re-reading the Decision guide table and noting one failure mode you could have caused yourself.""",
        "exercise_examples": r"""Expected behavior:

```
$ printf 'a\nb\na\n' | top_token
a
$ printf 'x\nx\ny\nz\nz\nz\n' | top_token
z
```

Intermediate stage, to help you debug:

```
$ printf 'a\nb\na\n' | sort | uniq -c | sort -nr
      2 a
      1 b
```

Hint: `awk 'NR==1{print $2}'` extracts the second column from the first line.

Self-check: run `bash -c 'source exercise.sh; top_token'` from the exercise directory (replace top_token with your function name) and compare by eye, then run `./test.sh`. Also confirm there is no trailing whitespace in the output.""",
    },
    41: {
        "body": r"""
## Why this matters

A script that works on your laptop when everything goes right is a demo. A
production script must also behave when a command fails, the user presses
Ctrl-C, the disk fills, or the same job starts twice. Robust Bash means
failing loudly, cleaning up after itself, and never leaving half-written
files or stale lock files. The most important tool for cleanup is
`trap ... EXIT`, which runs a handler whenever the script ends, however it ends.

## Core concepts

| Feature | Purpose |
|---------|---------|
| `set -e` | Exit when a command fails (with caveats) |
| `set -u` | Error on unset variables |
| `set -o pipefail` | Pipeline fails if any stage fails |
| `trap CMD EXIT` | Run `CMD` when the shell exits (success, error, or exit call) |
| `trap CMD INT TERM` | Run on Ctrl-C or kill |
| `mktemp` | Create unique temp file/dir safely |
| `flock` | Exclusive lock so only one instance runs |
| `local` | Function-scoped variable |
| quoting | `"$var"` prevents word splitting and globbing |

The cleanup phrase to remember: **trap EXIT**.

```
 start --> setup (mktemp, lock) --> work --> end
                 |                    |       |
                 +---- any exit path -+-------+--> trap handler runs: rm temp, release lock
                       (error, exit, Ctrl-C, normal)
```

The strict-mode header most scripts should start with:

```bash
#!/usr/bin/env bash
set -Eeuo pipefail
IFS=$'\n\t'
```

## Worked examples

Temp file with guaranteed cleanup:

```bash
#!/usr/bin/env bash
set -Eeuo pipefail

tmp=$(mktemp)
cleanup() { rm -f "$tmp"; }
trap cleanup EXIT

curl -fsS https://example.com > "$tmp"
wc -c < "$tmp"
```

Even if `curl` fails and the script aborts, `cleanup` runs and the file is gone.

Handle signals explicitly and keep the exit code:

```bash
cleanup() { rc=$?; rm -rf "$workdir"; exit "$rc"; }
workdir=$(mktemp -d)
trap cleanup EXIT
trap 'echo "interrupted" >&2; exit 130' INT TERM
```

Print line number and command on error:

```bash
trap 'echo "error at line $LINENO: $BASH_COMMAND" >&2' ERR
```

Single instance with `flock`:

```bash
exec 9>/var/lock/myjob.lock
flock -n 9 || { echo "already running" >&2; exit 1; }
```

Argument validation and usage:

```bash
usage() { echo "usage: $0 SRC DST" >&2; exit 2; }
[[ $# -eq 2 ]] || usage
src=$1 dst=$2
[[ -r $src ]] || { echo "cannot read: $src" >&2; exit 1; }
```

Atomic file replace (readers never see half a file):

```bash
tmp=$(mktemp "$dst.XXXXXX")
trap 'rm -f "$tmp"' EXIT
generate_report > "$tmp"
mv -f "$tmp" "$dst"
```

Retry with backoff:

```bash
retry() {
  local n=0 max=5 delay=1
  until "$@"; do
    n=$((n+1)); [[ $n -ge $max ]] && return 1
    sleep "$delay"; delay=$((delay*2))
  done
}
retry curl -fsS https://example.com/health
```

Careful with `set -e`:

```bash
set -e
grep -q foo file || true        # allow "not found"
if ! cmd; then echo "failed"; fi
# `set -e` is ignored inside if/while conditions and left side of && and ||
```

Lint and debug:

```bash
shellcheck script.sh
bash -n script.sh        # syntax check
bash -x script.sh        # trace
PS4='+ ${BASH_SOURCE}:${LINENO}: ' bash -x script.sh
```

## Mini-lab

1. Write a script that creates a temp directory, writes files in it, and then
   calls `false`. With and without `trap ... EXIT`, check if the directory
   remains in `/tmp`.
2. Add `INT` handling and press Ctrl-C during a `sleep 30`; confirm cleanup.
3. Use `flock` and launch the script twice in two terminals.
4. Run `shellcheck` on an old script of yours and fix three warnings.
5. Turn on `pipefail` and test: `false | true; echo $?` with and without it.
6. Write the phrase for this module's exercise: trap EXIT.

## Decision guide / failure modes

| Situation | Use |
|-----------|-----|
| Temp files | `mktemp` + `trap ... EXIT` |
| Cron job overlapping itself | `flock -n` |
| Unsafe user input in paths | quote and validate; use `--` before args |
| Needs structured data or complex logic | switch to Python/Go |
| Long script | functions, `main "$@"`, shellcheck in CI |

Failure modes:

- A later `trap` replaces an earlier one for the same signal; compose them in one
  function.
- `set -e` surprises: it does not trigger inside conditions or in commands
  before `||`. Explicit checks beat magic.
- Unquoted variables with spaces turn `rm -rf $dir/*` into disaster; always
  quote and use `${var:?}` to refuse empty values.
- `kill -9` bypasses traps; SIGKILL cannot be caught. Design stale-lock recovery.
- Cleanup that itself fails; keep handlers tiny and use `|| true`.
- Relying on `cd` succeeding: use `cd "$dir" || exit 1`.
""",
        "exercise_guide": r"""Implement `cleanup_phrase` in `exercise.sh` so it prints the two-word
Bash idiom that guarantees a cleanup handler runs when a script ends by any
route. Print the exact phrase with a single space, no punctuation, and the
signal name in capital letters. Then write a short script that creates a
temp file, fails with `false`, and use `trap` so the temp file is removed;
verify it is gone afterwards. Keep the function body to one line; the goal is recall of the lesson vocabulary, not cleverness. Finish by re-reading the Decision guide table and noting one failure mode you could have caused yourself.""",
        "exercise_examples": r"""Expected behavior:

```
$ cleanup_phrase
trap EXIT
```

Idiom in context:

```
tmp=$(mktemp)
trap 'rm -f "$tmp"' EXIT
```

The test compares the exact string `trap EXIT`. Writing `trap exit`, `EXIT trap`,
or including a command after it will fail.

Self-check: run `bash -c 'source exercise.sh; cleanup_phrase'` from the exercise directory (replace cleanup_phrase with your function name) and compare by eye, then run `./test.sh`. Also confirm there is no trailing whitespace in the output.""",
    },
}

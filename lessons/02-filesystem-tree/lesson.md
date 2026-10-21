---
title: "02. The Filesystem Tree: /, /etc, /var, /home, /proc"
---

# 02. The Filesystem Tree: /, /etc, /var, /home, /proc

**Phase:** Phase 1 — Shell and filesystem  
**Estimated time:** 1–2 days  
**Slug:** `02-filesystem-tree`

## Learning objectives

- Navigate with cd, pwd, ls
- Explain key FHS directories
- Create, move, copy, remove files carefully
- Use tab completion and wildcards

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.
Type every command yourself — muscle memory beats skimming.

## Why this matters

Linux has one single directory tree starting at `/`. Knowing what lives where tells you where to find logs, configuration, binaries and user data, where it is safe to write, and what to back up. The layout follows the Filesystem Hierarchy Standard (FHS), which most distributions follow closely, so skills transfer from Ubuntu to Fedora to Alpine.

## Core concepts

There are no drive letters. Extra disks are *mounted* onto directories in the tree. A path starting with `/` is *absolute*; any other path is *relative* to the current working directory. `.` is the current directory, `..` its parent, and `~` expands to your home.

```
/
+-- bin -> usr/bin     (symlink on merged-usr systems)
+-- boot               kernel, bootloader files
+-- dev                device files (null, sda, tty)
+-- etc                system-wide configuration
+-- home
|    +-- student       your files
+-- proc               virtual: processes and kernel info
+-- root               home of the root user
+-- tmp                temporary files, cleared often
+-- usr
|    +-- bin, lib, share, local
+-- var
     +-- log, cache, lib, spool
```

| Directory | Purpose |
|-----------|---------|
| `/etc` | Host configuration, text files |
| `/home` | Regular users' data |
| `/usr` | Installed programs and libraries (mostly read-only) |
| `/usr/local` | Software you installed by hand |
| `/var` | Variable data: logs, caches, databases |
| `/tmp` | Scratch space, world-writable with sticky bit |
| `/proc`, `/sys` | Kernel-provided virtual views |
| `/dev` | Device nodes such as `/dev/null` |
| `/opt` | Self-contained third-party packages |
| `/run` | Runtime data since boot (pid files, sockets) |

Path normalization matters when joining: joining `/var/` and `log` should give `/var/log`, not `/var//log`. If the second part is itself absolute, it replaces the first (this is how `os.path.join` behaves in Python as well).

## Worked examples

Look at the tree:

```bash
ls /
# sample output: bin  boot  dev  etc  home  lib  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
ls -ld /bin
# sample output: lrwxrwxrwx 1 root root 7 Apr 22  2024 /bin -> usr/bin
```

On a merged-usr system `/bin` is a symlink to `/usr/bin`.

Absolute versus relative:

```bash
cd /var/log
pwd
# sample output: /var/log
cd ../lib
pwd
# sample output: /var/lib
cd
pwd
# sample output: /home/student
```

`cd` with no argument jumps home; `cd -` returns to the previous directory.

Find where a program lives and what mounts exist:

```bash
command -v ls
# sample output: /usr/bin/ls
df -h / /tmp
# sample output: Filesystem      Size  Used Avail Use% Mounted on
# sample output: /dev/sda1         40G   12G   26G  32% /
# sample output: tmpfs            2.0G     0  2.0G   0% /tmp
```

Path tools:

```bash
realpath ../etc/./hostname
# sample output: /etc/hostname
dirname /var/log/syslog; basename /var/log/syslog
# sample output: /var/log
# sample output: syslog
```

## Mini-lab

1. Run `ls /` and `ls /usr` and match each directory to the table above.
2. Run `cat /etc/hostname` and `ls /etc | head`.
3. Run `ls /var/log` and note which files you can read (some need root).
4. Run `echo $PATH | tr ':' '\n'` and check that `/usr/bin` is listed.
5. Run `cd /tmp; mkdir -p lab/a/b; cd lab/a/b; pwd; cd ../..; pwd`.
6. Compare `ls /proc/self` with `cat /proc/self/cmdline | tr '\0' ' '`.
7. Run `findmnt /` (or `mount | head`) to see what is mounted at the root.
8. Write the absolute path of a file from three different starting directories using `realpath`.

## Decision guide / failure modes

Put local configuration in `/etc`, your own data in `$HOME`, hand-installed software in `/usr/local` or `/opt`, logs and databases under `/var`, and throwaway files in `/tmp` (use `mktemp`). Do not hand-edit files under `/usr` that a package manager owns; changes get overwritten on upgrade.

Common failures:

- Running a relative path script from the wrong directory; prefer absolute paths in cron jobs and units.
- Filling `/var` or `/` with logs; check `df -h` and `du -sh /var/*`.
- Assuming `/tmp` survives reboot; many systems mount it as tmpfs.
- Writing `rm -rf /$DIR` with an empty variable, which becomes `rm -rf /`. Quote and check variables.
- Joining paths by string concatenation and producing `//` or losing a separator.

## Common mistakes

- Running `rm -rf /` or similar disasters
- Treating `/proc` files like normal disk files to edit casually
- Filling `/` by writing huge files to `/tmp` unchecked

## Exercises

Work in `exercises/02-filesystem-tree/`. Read that folder's `README.md` fully before coding.

```bash
cd exercises/02-filesystem-tree
chmod +x test.sh exercise.sh
./test.sh
```

### What you will build

Implement abs_join(base, rel). Both arguments are strings. base is an absolute POSIX path such as "/var/log". Return a single absolute path made of base and rel joined by exactly one slash, with no duplicate slashes. If rel itself starts with "/", return rel unchanged because an absolute path overrides the base. Treat "/" as base correctly: abs_join("/", "etc") is "/etc". Do not touch the real filesystem and do not resolve "." or ".." segments; just join cleanly. Trailing slashes on base must not produce "//".

### Study loop

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** run 2–3 lab commands from this lesson on a real Linux host; paste notable output into your notes
- **C (Challenge):** rewrite the exercise from memory the next day

**Do not open `solutions/02-filesystem-tree/` until you have an honest failing attempt.**

## Self-check

Try to answer without scrolling up:

1. What lives in `/etc`?
2. What is special about `/proc`?
3. What does `mkdir -p` do?

## Further reading

- https://refspecs.linuxfoundation.org/FHS_3.0/fhs/index.html

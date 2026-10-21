# batch 0-13
EXTRA = {
  0: {
    "body": r"""## Why this matters

Linux runs most of the servers, containers, cloud instances, routers and Android phones in the world. If you work in backend, DevOps, security or data engineering, you will meet a Linux shell sooner or later, often on a machine that has no graphical desktop at all. Learning it once pays off on every distribution you touch.

This course is practical. You will type commands, break things in a safe sandbox, and read error messages until they stop being scary. Reading output carefully is the real skill; memorizing flags is secondary because `man` and `--help` are always available.

## Core concepts

"Linux" strictly means the kernel: the program that manages CPU, memory, devices and processes. A *distribution* (Ubuntu, Debian, Fedora, Alpine, Arch) bundles the kernel with a C library, an init system, package manager and userland tools (mostly from the GNU project, which is why you also hear "GNU/Linux").

| Term | Meaning | Example |
|------|---------|---------|
| Kernel | Core that talks to hardware | `uname -r` shows its version |
| Distribution | Kernel + packages + defaults | Ubuntu 24.04 |
| Shell | Program that reads your commands | `bash`, `zsh`, `sh` |
| Terminal | Window that displays a text session | GNOME Terminal, tmux pane |
| Package manager | Installs software | `apt`, `dnf`, `apk` |

Terminal and shell are different things: the terminal draws text and sends keystrokes, the shell interprets them and starts programs.

```
 you --keys--> [ terminal ] --> [ shell: bash ] --fork/exec--> [ program ]
                                      |                            |
                                      |                     system calls
                                      v                            v
                                 [ libc ]  ------------------>  [ kernel ] --> hardware
```

Everything you run ends up as system calls into the kernel. A useful motto: in Unix, most things are files or processes.

Safe places to practice: a virtual machine, a Docker container, WSL2 on Windows, or a cloud VM you can delete. Avoid experimenting on a machine holding data you care about.

## Worked examples

Find out where you are and what you are running:

```bash
uname -sr
# sample output: Linux 6.8.0-45-generic
cat /etc/os-release | head -n 2
# sample output: PRETTY_NAME="Ubuntu 24.04.1 LTS"
# sample output: NAME="Ubuntu"
```

`uname -sr` prints kernel name and release; `/etc/os-release` describes the distribution on nearly every modern system.

Who and where:

```bash
whoami
# sample output: student
pwd
# sample output: /home/student
echo "$SHELL"
# sample output: /bin/bash
```

`whoami` prints your username, `pwd` prints the current directory, and `$SHELL` holds your login shell (it may differ from the shell currently running).

Getting help offline:

```bash
man ls | head -n 3
# sample output: LS(1)                 User Commands                LS(1)
ls --help | head -n 1
# sample output: Usage: ls [OPTION]... [FILE]...
```

`man` opens the manual page; press `q` to leave. `--help` gives a shorter summary for most GNU tools. Builtins such as `cd` are documented with `help cd`.

A tiny greeting, the shape of the exercise:

```bash
name="Ada"
echo "Hello, $name!"
# sample output: Hello, Ada!
```

## Mini-lab

1. Start a throwaway environment: `docker run --rm -it ubuntu:24.04 bash` (or open any Ubuntu VM or WSL shell).
2. Run `uname -a` and `cat /etc/os-release`; write down kernel and distribution.
3. Run `whoami`, `pwd`, `hostname`. In a container you are usually `root`.
4. Run `echo $0` to see which shell you are in.
5. Run `man man` and read the first screen, then press `q`.
6. Create a file: `echo "hello linux" > ~/hello.txt` then `cat ~/hello.txt`.
7. Run `ls -l ~/hello.txt` and identify the size and owner.
8. Exit with `exit` (or Ctrl-D). The container disappears because of `--rm`.

## Decision guide / failure modes

Use a VM when you need a full OS with its own kernel and services; use a container for fast, disposable userland (it shares the host kernel); use WSL2 for daily work on Windows; use a real install only when you need hardware access or want to commit.

Common failures:

- `command not found`: typo, tool not installed, or not in `$PATH`. Check with `type NAME` and install via the package manager.
- `Permission denied`: you lack rights on that file. Do not reflexively add `sudo`; read the error first.
- Copy-pasting commands with `rm -rf` or `curl | sh` from the web without reading them. Read first, then run.
- Confusing case: Linux file names are case-sensitive, so `Notes.txt` and `notes.txt` are different.
- Practicing as root in a container, then being surprised on a real system where you are not root.
""",
    "exercise_guide": r"""Implement greet(name). It takes a single string NAME and returns the greeting text "Hello, NAME!" exactly, with a comma, one space and an exclamation mark at the end. Do not print extra whitespace or a trailing newline inside the returned value. If NAME is an empty string, return "Hello, world!" instead. Keep the function pure: no input from the keyboard, no file access. This mirrors what a shell function would do with echo "Hello, $1!" and warms you up for editing and running scripts.""",
    "exercise_examples": r"""greet("Ada") -> "Hello, Ada!"
greet("Linus") -> "Hello, Linus!"
greet("world") -> "Hello, world!"
greet("") -> "Hello, world!"
greet("Mary Ann") -> "Hello, Mary Ann!"

The returned text has no leading or trailing spaces and no newline character.
Typical use: greet("Ada") is printed by the caller, which adds its own newline.
The name is inserted as given; do not change its letter case.""",
  },
  1: {
    "body": r"""## Why this matters

Every task on a Linux server starts at a prompt. Understanding how the shell splits a line into a command and its arguments, and how a program reports success or failure through an exit code, is the foundation for all scripting, CI pipelines and debugging. A misunderstood quote or ignored exit status is behind many production incidents.

## Core concepts

The prompt, for example `student@box:~/work$`, shows user, host, current directory (`~` means home) and a final character: `$` for a normal user, `#` for root. The shell reads a line, splits it into *words* on unquoted whitespace, expands things like `$HOME`, `*.txt` and `$(date)`, then runs the first word as the command and the others as arguments.

```
 ls  -l  "my file.txt"  /tmp
 |   |        |           |
 |   |        |           +-- argument 3
 |   |        +-- argument 2 (quotes keep the space)
 |   +-- option (argument 1 by convention)
 +-- command (argv[0])
```

Commands come in kinds: builtins (`cd`, `echo`), external programs (`/usr/bin/ls`), aliases and functions. `type NAME` tells you which.

When a command ends it returns an *exit code* from 0 to 255. By convention 0 means success and anything else means failure. The code of the last command is in `$?`.

| Code | Usual meaning |
|------|---------------|
| 0 | Success |
| 1 | General error |
| 2 | Misuse of the command (bad option) |
| 126 | Found but not executable |
| 127 | Command not found |
| 128+N | Killed by signal N (130 = Ctrl-C, 137 = KILL) |

Quoting rules: single quotes keep text literal; double quotes allow `$VAR` and `$(cmd)` expansion but prevent word splitting; a backslash escapes one character.

Chaining: `a && b` runs b only if a succeeded; `a || b` runs b only if a failed; `a ; b` runs both regardless.

## Worked examples

Exit codes in action:

```bash
true; echo $?
# sample output: 0
false; echo $?
# sample output: 1
ls /nonexistent; echo $?
# sample output: ls: cannot access '/nonexistent': No such file or directory
# sample output: 2
nosuchcmd; echo $?
# sample output: bash: nosuchcmd: command not found
# sample output: 127
```

`true` and `false` are tiny programs that only return 0 and 1. GNU `ls` returns 2 for a serious trouble such as a missing argument path.

Arguments and quoting:

```bash
printf '[%s]\n' my file.txt
# sample output: [my]
# sample output: [file.txt]
printf '[%s]\n' "my file.txt"
# sample output: [my file.txt]
```

Without quotes the shell hands two arguments to printf; with quotes, one.

Conditional chaining:

```bash
mkdir demo && cd demo && echo "inside $(pwd)"
# sample output: inside /home/student/demo
grep -q root /etc/passwd && echo found || echo missing
# sample output: found
```

Identify a command:

```bash
type cd ls
# sample output: cd is a shell builtin
# sample output: ls is /usr/bin/ls
```

## Mini-lab

1. Run `echo $?` right after opening a shell; note it is 0.
2. Run `false`, then `echo $?`. Then run `echo $?` again and explain why it is now 0 (the previous command was echo).
3. Run `ls /does/not/exist; echo "code=$?"`.
4. Run `foo; echo "code=$?"` and confirm 127.
5. Create a script: `printf '#!/bin/bash\nexit 3\n' > t.sh`, run `./t.sh` (fails with 126 because it is not executable), then `chmod +x t.sh; ./t.sh; echo $?` prints 3.
6. Test quoting: `touch "a b.txt"; ls a b.txt` fails, `ls "a b.txt"` works.
7. Try `cd /tmp && pwd`, then `cd /nope && pwd` and observe that pwd does not run.
8. Use `type -a echo` to see both builtin and external versions.

## Decision guide / failure modes

Use `&&` when the second step depends on the first, `||` for fallbacks, and `;` only when steps are independent. Use single quotes for literal text (regexes, awk programs) and double quotes when you need variables. Use `$?` immediately; any other command overwrites it, so save it with `rc=$?` if needed later.

Common failures:

- Forgetting quotes around variables: `rm $file` with spaces or globs misbehaves; write `rm -- "$file"`.
- Assuming non-zero means a bug. `grep` returns 1 for "no match", which is not an error.
- Pipelines hide failures: the status of `a | b` is b's unless `pipefail` is set (module 7).
- Reading exit codes above 125 as normal; 127 and 126 are shell-level problems, 128+N means a signal.
- Using `;` where `&&` was meant, so a failed `cd` is followed by a destructive command in the wrong directory.
""",
    "exercise_guide": r"""Implement two small functions. success_code() returns the exit code that conventionally means a command succeeded. failure_code() returns a typical generic failure exit code. Both return integers, not strings. success_code must be 0. failure_code must be a non-zero integer in the range 1..255; use 1, the general error code used by shell builtins and most tools. No arguments and no side effects are needed. The exercise checks that you know the convention behind "0 is success, non-zero is failure" that the shell relies on for && and ||.""",
    "exercise_examples": r"""success_code() -> 0
failure_code() -> 1

Shell equivalents:
true; echo $?     prints 0
false; echo $?    prints 1

A test may check: success_code() == 0 and 1 <= failure_code() <= 255.
Both values are ints, so success_code() == "0" would be False.
Rule used by the shell: "cmd1 && cmd2" runs cmd2 only when cmd1 returned 0;
"cmd1 || cmd2" runs cmd2 only when cmd1 returned non-zero.""",
  },
  2: {
    "body": r"""## Why this matters

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
""",
    "exercise_guide": r"""Implement abs_join(base, rel). Both arguments are strings. base is an absolute POSIX path such as "/var/log". Return a single absolute path made of base and rel joined by exactly one slash, with no duplicate slashes. If rel itself starts with "/", return rel unchanged because an absolute path overrides the base. Treat "/" as base correctly: abs_join("/", "etc") is "/etc". Do not touch the real filesystem and do not resolve "." or ".." segments; just join cleanly. Trailing slashes on base must not produce "//".""",
    "exercise_examples": r"""abs_join("/var", "log") -> "/var/log"
abs_join("/var/", "log") -> "/var/log"
abs_join("/", "etc") -> "/etc"
abs_join("/home/student", "docs/a.txt") -> "/home/student/docs/a.txt"
abs_join("/var/log", "/etc/hosts") -> "/etc/hosts"

Edge: abs_join("/usr//", "bin") -> "/usr/bin"  (extra trailing slashes removed).""",
  },
  3: {
    "body": r"""## Why this matters

Everyday work is creating, copying, moving and linking files. Underneath, Linux files are identified by inodes, and names are only entries in directories pointing to them. Understanding this explains why a hard link survives deleting the original, why a symlink can dangle, and why `mv` within one filesystem is instant while across filesystems it copies.

## Core concepts

An *inode* stores metadata (type, owner, permissions, size, timestamps, link count, data location) but not the file name. A directory is a table of name-to-inode entries. A *hard link* is another name for the same inode; the data is removed only when the link count reaches 0 and no process holds it open. A *symbolic (soft) link* is a small separate file containing a path; it can point to a directory, across filesystems, or to something that no longer exists.

```
 hard links                         symbolic link
 a.txt --\                          link.txt --> inode 77 (type l)
          +--> inode 42 --> data              data: "a.txt"  (a path string)
 b.txt --/    (link count 2)                       |
                                                    +--> looks up a.txt by name
```

| Property | Hard link | Symbolic link |
|----------|-----------|---------------|
| Own inode | No, shares target's | Yes |
| Cross filesystem | No | Yes |
| Link to directory | No (normally) | Yes |
| Survives target deletion | Yes, data stays | No, becomes dangling |
| `ls -l` first char | `-` | `l` |
| Create | `ln a b` | `ln -s a b` |

Metadata commands: `ls -l` (type, perms, links, owner, size, mtime), `stat` (all fields including inode), `file` (guess content type). File types by the first character of `ls -l`: `-` regular, `d` directory, `l` symlink, `c`/`b` devices, `s` socket, `p` pipe.

Timestamps: mtime (content changed), ctime (inode metadata changed), atime (read). `touch` updates them or creates an empty file.

## Worked examples

Hard versus soft:

```bash
cd /tmp && echo hi > a.txt
ln a.txt hard.txt
ln -s a.txt soft.txt
ls -li a.txt hard.txt soft.txt
# sample output: 131090 -rw-r--r-- 2 student student 3 Oct 21 10:00 a.txt
# sample output: 131090 -rw-r--r-- 2 student student 3 Oct 21 10:00 hard.txt
# sample output: 131091 lrwxrwxrwx 1 student student 5 Oct 21 10:00 soft.txt -> a.txt
```

Same inode and link count 2 for the hard pair; the symlink has its own inode and shows its target.

Delete the original:

```bash
rm a.txt
cat hard.txt
# sample output: hi
cat soft.txt
# sample output: cat: soft.txt: No such file or directory
```

The hard link still holds the data; the soft link dangles.

Inspect metadata:

```bash
stat -c '%n %i %h %F' hard.txt soft.txt
# sample output: hard.txt 131090 1 regular file
# sample output: soft.txt 131091 1 symbolic link
file soft.txt
# sample output: soft.txt: broken symbolic link to a.txt
```

Test the type in a script:

```bash
[ -L soft.txt ] && echo symlink
# sample output: symlink
readlink soft.txt
# sample output: a.txt
```

## Mini-lab

1. `mkdir -p /tmp/lab3 && cd /tmp/lab3 && echo data > one`.
2. `ln one two` and `ln -s one three`.
3. Run `ls -li` and confirm `one` and `two` share an inode number.
4. Append with `echo more >> two` and `cat one`; both names show the same content.
5. Run `stat one` and read Links, Inode, Modify and Change times.
6. `rm one`, then `cat two` (works) and `cat three` (fails).
7. Recreate `one` with `echo new > one` and `cat three`; the symlink now works again because it resolves by name.
8. Try `ln /etc/hostname hostlink` on a different filesystem (for example from /tmp tmpfs) and read the error "Invalid cross-device link".

## Decision guide / failure modes

Use a symlink for shortcuts, version switches (`current -> release-42`), links across filesystems, and links to directories. Use a hard link for extra names of the same file on one filesystem, as backup tools do to save space. When unsure, choose a symlink; it is visible and easy to inspect.

Common failures:

- Dangling symlinks after moving the target; relative link targets are resolved from the link's directory, not from your current directory.
- Expecting a hard link to follow an editor that replaces the file (many editors write a new file, which breaks the shared inode).
- `ln -s target link` argument order confusion: target first, link name second.
- `rm link/` with a trailing slash on a symlink to a directory may act on the target contents.
- `cp` follows or copies links differently depending on options; use `cp -a` to preserve links and metadata.
""",
    "exercise_guide": r"""Implement link_kind(ls_first_char_or_name). The input is a string describing how a link was made: either the word "soft" or "hard" (case-insensitive, surrounding whitespace ignored), or the command used: "ln -s" means soft and plain "ln" means hard. Return the lowercase string "soft" for symbolic links and "hard" for hard links. For any unrecognized input return "unknown". The point is to connect the commands to the concepts: ln -s creates a symbolic (soft) link with its own inode, plain ln creates another name for the same inode.""",
    "exercise_examples": r"""link_kind("soft") -> "soft"
link_kind("HARD") -> "hard"
link_kind("ln -s") -> "soft"
link_kind("ln") -> "hard"
link_kind("  Soft ") -> "soft"
link_kind("copy") -> "unknown"

Shell view:
ln -s a b   -> soft (ls -l shows 'l' and b -> a)
ln a b      -> hard (same inode, link count 2)
link_kind("ln -s a b") may also be treated as soft.
A dangling soft link still reports "soft"; the kind is about creation.""",
  },
  4: {
    "body": r"""## Why this matters

Permissions are the main safety net on a multi-user system. They decide who can read your SSH keys, who can run a script and who can change a config file. Reading `-rwxr-x---` fluently and choosing correct modes with `chmod` and `chown` prevents both "Permission denied" headaches and dangerous world-writable files.

## Core concepts

Every file has an owner (user), a group and three permission sets: user (u), group (g) and others (o). Each set has read (r), write (w) and execute (x). For directories, r means list names, w means create/delete/rename entries, x means enter and access entries (traverse).

```
 -  rwx  r-x  r--   alice  devs  report.sh
 |   |    |    |
 |   |    |    +-- others: read only       (4)
 |   |    +------- group:  read + execute  (5 = 4+1)
 |   +------------ user:   read/write/exec (7 = 4+2+1)
 +---------------- type: - file, d directory, l link
 mode octal: 754
```

| Octal | Symbolic | Meaning |
|-------|----------|---------|
| 7 | rwx | all |
| 6 | rw- | read, write |
| 5 | r-x | read, execute |
| 4 | r-- | read only |
| 0 | --- | none |

Each digit is the sum r=4, w=2, x=1. Common modes: `644` (`rw-r--r--`) for ordinary files, `755` (`rwxr-xr-x`) for programs and directories, `600` (`rw-------`) for private keys, `700` for private directories.

`chmod` accepts octal (`chmod 640 f`) or symbolic (`chmod u+x f`, `chmod go-w f`, `chmod a=r f`). `chown user:group file` changes ownership (root only for changing the owner); `chgrp` changes only the group; `-R` recurses. New files get mode `0666 & ~umask` (files) or `0777 & ~umask` (directories); with umask `022` that is 644 and 755.

## Worked examples

Read a listing:

```bash
ls -l deploy.sh
# sample output: -rwxr-x--- 1 alice devs 214 Oct 21 10:00 deploy.sh
```

Alice can do everything, group `devs` can read and run, others get nothing.

Change modes:

```bash
chmod 640 deploy.sh
ls -l deploy.sh
# sample output: -rw-r----- 1 alice devs 214 Oct 21 10:00 deploy.sh
chmod u+x,g-r deploy.sh
ls -l deploy.sh
# sample output: -rwx------ 1 alice devs 214 Oct 21 10:00 deploy.sh
stat -c '%a %A %U:%G' deploy.sh
# sample output: 700 -rwx------ alice:devs
```

Change ownership (requires root):

```bash
sudo chown bob:devs deploy.sh
ls -l deploy.sh
# sample output: -rwx------ 1 bob devs 214 Oct 21 10:00 deploy.sh
```

Directory execute bit:

```bash
mkdir d && touch d/f && chmod 644 d
ls d
# sample output: f
cat d/f
# sample output: cat: d/f: Permission denied
```

Listing names needs r, but reaching `d/f` needs x on `d`.

Umask:

```bash
umask
# sample output: 0022
touch n && mkdir m && stat -c '%a %n' n m
# sample output: 644 n
# sample output: 755 m
```

## Mini-lab

1. `cd /tmp && mkdir perm && cd perm && touch f && ls -l f`.
2. Convert the mode you see to octal by hand, then confirm with `stat -c %a f`.
3. `chmod 000 f; cat f` fails (as root it may not; use a normal user or `su`).
4. `chmod u+r f; cat f` works; `chmod 755 f; ls -l f`.
5. Create `s.sh` containing `echo ok`; run `./s.sh` (denied), `chmod +x s.sh`, run again.
6. Set `umask 077`, create a file and a directory, check their modes, then `umask 022`.
7. `mkdir secret && chmod 700 secret`; test access as another user with `sudo -u nobody ls secret`.
8. Convert 640, 755, 600 and 711 to symbolic form on paper, then verify using `chmod` and `ls -l`.

## Decision guide / failure modes

Use octal when you know the full target mode; use symbolic (`u+x`) to change one bit without touching others. Give files 644, scripts 755, private keys 600, shared project directories 770 or 2770 with a group (module 6). Never use 777 as a fix.

Common failures:

- `chmod -R 755 .` makes every data file executable; use `find -type d` and `find -type f` separately.
- SSH refuses a key with "UNPROTECTED PRIVATE KEY FILE": set `chmod 600 ~/.ssh/id_*` and `700 ~/.ssh`.
- Script gives "Permission denied" because it lacks `x` or sits on a `noexec` mount.
- Forgetting directory `x`, so files inside can be listed but not opened.
- `chown -R` with a wrong path or a trailing `/..`; double-check before running as root.
""",
    "exercise_guide": r"""Implement octal_to_human(mode). The input is a three-digit octal permission string such as "755" or "640" (digits 0-7). Return the nine-character symbolic form without the file-type character, like "rwxr-xr-x". Each digit expands to three characters: 4 gives r, 2 gives w, 1 gives x, and missing bits are "-". Digits are in order user, group, others. Do not use the filesystem. You may assume the input is valid three digits; for anything else return an empty string. This is the same mapping chmod and ls -l use.""",
    "exercise_examples": r"""octal_to_human("755") -> "rwxr-xr-x"
octal_to_human("644") -> "rw-r--r--"
octal_to_human("600") -> "rw-------"
octal_to_human("777") -> "rwxrwxrwx"
octal_to_human("000") -> "---------"
octal_to_human("640") -> "rw-r-----"
octal_to_human("12") -> ""   (not three digits)
octal_to_human("789") -> ""   (8 and 9 are not octal digits)
Check: chmod 750 f then ls -l f shows -rwxr-x---, i.e. "rwxr-x---".""",
  },
  5: {
    "body": r"""## Why this matters

Linux is a multi-user system. Each process runs as some user, and that identity decides which files it can touch and which operations it may perform. Knowing how users, groups and `sudo` work lets you give people just enough access, and avoid logging in as root for routine work, which is one of the biggest safety habits in administration.

## Core concepts

A user has a numeric *UID*; the name is only a label. UID 0 is root, with nearly unlimited power. System accounts (daemons such as `www-data`) typically have low UIDs; on many distributions regular users start at 1000. Each user has a primary *GID* plus optional supplementary groups. Account data lives in text files.

```
 /etc/passwd   name:x:UID:GID:comment:home:shell
 /etc/group    group:x:GID:member1,member2
 /etc/shadow   name:password-hash:...      (root only)
 /etc/sudoers  who  where=(as whom)  commands
```

| Command | Purpose |
|---------|---------|
| `id` | Show UID, GID and groups of current user |
| `whoami` | Print effective username |
| `groups` | List group names |
| `useradd` / `adduser` | Create a user (adduser is the friendlier Debian wrapper) |
| `usermod -aG GROUP USER` | Append user to a supplementary group |
| `passwd` | Change password |
| `su - USER` | Start a login shell as another user |
| `sudo CMD` | Run one command as root (or `-u USER`) |
| `visudo` | Safely edit sudoers |

`sudo` asks for *your* password (not root's), checks the rules in `/etc/sudoers` and `/etc/sudoers.d/`, runs the command with elevated privileges and logs the event (often in `/var/log/auth.log` or the journal). On Ubuntu, members of the `sudo` group may run anything; on RHEL-like systems it is the `wheel` group.

Group membership changes take effect on *new* login sessions; run `newgrp` or log in again to see them.

## Worked examples

Who am I:

```bash
id
# sample output: uid=1000(student) gid=1000(student) groups=1000(student),27(sudo),100(users)
id -u
# sample output: 1000
id -un; id -gn
# sample output: student
# sample output: student
```

Look up accounts:

```bash
getent passwd student
# sample output: student:x:1000:1000:Student,,,:/home/student:/bin/bash
grep '^root:' /etc/passwd | cut -d: -f1,3,6,7
# sample output: root:0:/root:/bin/bash
```

Fields are separated by colons: field 3 is the UID.

Use sudo:

```bash
sudo whoami
# sample output: root
sudo -l | head -n 3
# sample output: Matching Defaults entries for student on box:
# sample output:     env_reset, mail_badpass, secure_path=...
```

Create a user and a group, add membership:

```bash
sudo groupadd project
sudo useradd -m -s /bin/bash -G project dana
sudo usermod -aG project student
getent group project
# sample output: project:x:1002:dana,student
```

Without `-a`, `usermod -G` would replace all supplementary groups.

## Mini-lab

1. Run `id` and identify your UID, GID and groups.
2. Run `getent passwd $(id -un)` and name each of the seven fields.
3. Run `sudo -v` to validate sudo works (in a Docker container install it with `apt update && apt install -y sudo`).
4. Create a user: `sudo useradd -m -s /bin/bash lab5`; set a password with `sudo passwd lab5`.
5. Create a group: `sudo groupadd team5` and `sudo usermod -aG team5 lab5`; verify with `id lab5`.
6. Run `sudo -u lab5 id` and compare with your own `id`.
7. As lab5, run `touch /etc/x` and read the error; then `sudo touch /etc/x` as an allowed user and delete it.
8. Clean up: `sudo userdel -r lab5; sudo groupdel team5`.

## Decision guide / failure modes

Use `sudo CMD` for single privileged actions with an audit trail; use `su -` or `sudo -i` only when you truly need a long root session; use dedicated service accounts (no login shell, `nologin`) for daemons. Grant groups rather than individual permissions, and prefer narrow sudo rules over `ALL`.

Common failures:

- `usermod -G` without `-a` silently removes other groups.
- Editing `/etc/sudoers` directly with a typo locks out sudo; always use `visudo`.
- Using `sudo` with redirection: `sudo echo x > /etc/f` fails because the redirection runs in your shell; use `echo x | sudo tee /etc/f`.
- Expecting new group rights without re-login.
- Running everything as root, so one typo or compromised script owns the machine.
""",
    "exercise_guide": r"""Implement parse_uid(id_output). The input is a single line produced by the id command, for example "uid=1000(student) gid=1000(student) groups=1000(student),27(sudo)". Return the numeric user id as an int, taken from the "uid=" field (the digits right after "uid=", before the parenthesis or space). Ignore gid and groups. If there is no uid= field, return -1. The input may have leading or trailing whitespace. This is the same extraction you would do with grep -o or cut in a script.""",
    "exercise_examples": r"""parse_uid("uid=1000(student) gid=1000(student) groups=1000(student),27(sudo)") -> 1000
parse_uid("uid=0(root) gid=0(root) groups=0(root)") -> 0
parse_uid("  uid=33(www-data) gid=33(www-data) groups=33(www-data)  ") -> 33
parse_uid("gid=1000(student)") -> -1
parse_uid("") -> -1

Note: the result is an int, not a string.""",
  },
  6: {
    "body": r"""## Why this matters

Plain read/write/execute bits are not enough for shared systems. Passwords must be changed by ordinary users even though `/etc/shadow` is root-only; `/tmp` must be writable by everyone without letting users delete each other's files; project directories should keep one group for all new files. Special bits solve these problems, and misusing them is also a classic privilege-escalation path.

## Core concepts

There are three extra bits, shown as a fourth leading octal digit (`4755`, `2775`, `1777`).

| Bit | Octal | On a file | On a directory | Shown as |
|-----|-------|-----------|----------------|----------|
| setuid | 4000 | Runs with the file owner's UID | Ignored on Linux | `s` in user x slot |
| setgid | 2000 | Runs with the file's group | New entries inherit the directory's group | `s` in group x slot |
| sticky | 1000 | Ignored on modern Linux | Only owner of an entry (or dir owner or root) may delete or rename it | `t` in others x slot |

A capital `S` or `T` means the special bit is set but the underlying execute bit is not.

```
  /tmp   drwxrwxrwt  root root
              ^^^^^^^^^
        anyone may create files;
        sticky 't': only the file's owner
        (or root / dir owner) may remove them

  /usr/bin/passwd  -rwsr-xr-x root root
                      ^
        runs as root even when alice starts it,
        so it can update /etc/shadow
```

With setuid, the process has an *effective* UID of the file owner while the real UID remains the caller. The kernel ignores setuid on interpreted scripts (`#!` files) for safety, so it only works on compiled binaries.

Because setuid-root programs are high-value targets, keep their number small and audit them with `find`.

## Worked examples

Spot the bits:

```bash
ls -ld /tmp
# sample output: drwxrwxrwt 14 root root 4096 Oct 21 10:00 /tmp
ls -l /usr/bin/passwd
# sample output: -rwsr-xr-x 1 root root 59976 Feb  6  2024 /usr/bin/passwd
stat -c '%a %n' /tmp /usr/bin/passwd
# sample output: 1777 /tmp
# sample output: 4755 /usr/bin/passwd
```

Sticky directory behavior:

```bash
mkdir /tmp/shared && chmod 1777 /tmp/shared
touch /tmp/shared/mine
sudo -u nobody rm /tmp/shared/mine
# sample output: rm: cannot remove '/tmp/shared/mine': Operation not permitted
```

Even though the directory is world-writable, `nobody` is not the owner, so deletion is refused.

Setgid directory for a team:

```bash
sudo mkdir /srv/team && sudo chgrp devs /srv/team
sudo chmod 2775 /srv/team
touch /srv/team/doc && ls -l /srv/team/doc
# sample output: -rw-r--r-- 1 student devs 0 Oct 21 10:05 /srv/team/doc
```

The new file got group `devs`, not the creator's primary group.

Audit setuid files:

```bash
find /usr/bin -perm -4000 -type f 2>/dev/null
# sample output: /usr/bin/passwd
# sample output: /usr/bin/sudo
# sample output: /usr/bin/su
```

## Mini-lab

1. Run `ls -ld /tmp /usr/bin/passwd /usr/bin/sudo` and identify the `t` and `s` letters.
2. As root create `mkdir /tmp/lab6 && chmod 1777 /tmp/lab6`.
3. Create a file as your user, then try deleting it as another user: `sudo -u nobody rm /tmp/lab6/f`.
4. Remove the sticky bit with `chmod -t /tmp/lab6` and repeat; now deletion succeeds if the directory is writable.
5. Create `mkdir /tmp/g6 && chgrp users /tmp/g6 && chmod 2775 /tmp/g6`; add a file and check the group.
6. Set `chmod u+s somefile` on a harmless copy of `/bin/true` and view `ls -l`; notice the `s`. Then `chmod u-s` it.
7. Find setgid files: `find /usr -perm -2000 -type f 2>/dev/null | head`.
8. Convert `4755`, `2770`, `1777` to symbolic form by hand.

## Decision guide / failure modes

Use sticky on shared writable directories (`/tmp`, upload spools); use setgid on directories for team collaboration; use setuid only for small audited binaries that truly need privilege, and prefer `sudo` or capabilities (`setcap`) for new designs.

Common failures:

- Seeing `S` or `T` and assuming it is fine: execute is missing, so the bit's effect may be broken.
- Setting setuid on a shell script and expecting it to work; Linux ignores it.
- Leaving a world-writable directory without sticky bit, so users delete each other's files.
- `chmod -R 2775` also setting setgid on files; apply to directories only.
- Backups or copies that drop special bits; check with `stat` after restoring.
""",
    "exercise_guide": r"""Implement describe_sticky(mode). The input is a string, either an octal mode with four digits like "1777" or a symbolic string like "drwxrwxrwt". Decide whether the sticky bit is set. If it is set, return the string "owner-delete-only", describing its effect on a directory: only the owner of an entry (or the directory owner or root) may delete or rename it. If the sticky bit is not set, return "normal". In octal the sticky bit is the 1 in the leading digit of four digits; in symbolic form it is a "t" or "T" as the last character of the mode.""",
    "exercise_examples": r"""describe_sticky("1777") -> "owner-delete-only"
describe_sticky("0755") -> "normal"
describe_sticky("drwxrwxrwt") -> "owner-delete-only"
describe_sticky("drwxrwxrwx") -> "normal"
describe_sticky("drwxr-xr-T") -> "owner-delete-only"
describe_sticky("2775") -> "normal"   (setgid only, no sticky)
describe_sticky("3775") -> "owner-delete-only"  (setgid + sticky)""",
  },
  7: {
    "body": r"""## Why this matters

The Unix philosophy is small tools that do one thing, combined with pipes. Redirection and pipelines let you filter logs, count records, save results and chain programs without writing a single line of a real program. They are also where silent failures hide: a pipeline can "succeed" even when its first stage crashed.

## Core concepts

Every process starts with three standard streams, referred to by file descriptor numbers: 0 = stdin (input), 1 = stdout (output), 2 = stderr (errors and diagnostics). Redirection connects them to files; a pipe connects one process's stdout to the next process's stdin.

```
 cmd1 --stdout(1)--> | pipe | --stdin(0)--> cmd2 --stdout(1)--> terminal
   \
    +--stderr(2)------------------------------------------> terminal

 cmd > out.txt 2> err.txt     (separate files)
 cmd > all.txt 2>&1           (stderr follows stdout)
```

| Syntax | Effect |
|--------|--------|
| `cmd > f` | Write stdout to f, truncating it |
| `cmd >> f` | Append stdout to f |
| `cmd < f` | Read stdin from f |
| `cmd 2> f` | Send stderr to f |
| `cmd > f 2>&1` | stdout and stderr to f (order matters) |
| `cmd &> f` | Bash shorthand for the line above |
| `a \| b` | Pipe a's stdout into b |
| `cmd <<< "text"` | Here-string as stdin |
| `tee f` | Copy stdin to f and to stdout |
| `/dev/null` | Discard everything written |

Every stage of a pipeline runs at once, as separate processes. By default the exit status of the pipeline is that of the *last* command only. With `set -o pipefail` the status becomes the last non-zero status of any stage, and `${PIPESTATUS[@]}` in bash lists all of them. Scripts commonly start with `set -euo pipefail`.

Tools that work as filters read stdin when given no file: `wc -l`, `sort`, `uniq`, `head`, `tail`, `cut`, `tr`, `grep`.

## Worked examples

Redirect and append:

```bash
echo one > list.txt
echo two >> list.txt
cat list.txt
# sample output: one
# sample output: two
```

Split streams:

```bash
ls /etc/hostname /nope > out.txt 2> err.txt
cat out.txt
# sample output: /etc/hostname
cat err.txt
# sample output: ls: cannot access '/nope': No such file or directory
```

Classic pipeline, top repeated lines:

```bash
printf 'b\na\nb\nc\nb\na\n' | sort | uniq -c | sort -rn | head -n 2
# sample output:       3 b
# sample output:       2 a
```

`uniq` only collapses adjacent duplicates, so sort first.

Counting lines from stdin:

```bash
printf 'x\ny\nz\n' | wc -l
# sample output: 3
wc -l < list.txt
# sample output: 2
```

Using `< file` avoids the file name that `wc -l list.txt` prints.

The pipefail trap:

```bash
false | cat; echo "status=$?"
# sample output: status=0
set -o pipefail
false | cat; echo "status=$?"
# sample output: status=1
```

Redirect order:

```bash
ls /nope 2>&1 > /dev/null | wc -l
# sample output: 1
```

Here stderr goes to the pipe (the old stdout) before stdout is sent to /dev/null.

## Mini-lab

1. `cd /tmp && mkdir lab7 && cd lab7`.
2. `seq 1 10 > nums.txt` and `wc -l < nums.txt` (prints 10).
3. `grep 5 nums.txt | wc -l` and explain why it prints 1.
4. `ls /etc /nope > o.txt 2> e.txt` and inspect both files.
5. `ls /etc /nope > both.txt 2>&1` then `wc -l both.txt`.
6. `cat nums.txt | tee copy.txt | tail -n 2` to see tee in action.
7. Run `false | true; echo $?` with and without `set -o pipefail`; also print `${PIPESTATUS[@]}`.
8. Write a one-liner that counts unique shells in `/etc/passwd`: `cut -d: -f7 /etc/passwd | sort -u | wc -l`.

## Decision guide / failure modes

Use a pipe when the next tool should process data as it streams; use a file redirect when you need to keep the result; use `tee` for both. Use `>>` for logs; use `>` only when overwriting is intended. Use `2>/dev/null` sparingly, since it hides the very errors you need.

Common failures:

- `cmd > f` on a file you also read, e.g. `sort f > f`, empties the file before sort reads it. Use a temp file or `sort -o f f`.
- `cmd 2>&1 > f` instead of `cmd > f 2>&1`: the order is wrong and stderr still hits the terminal.
- Pipeline success hiding failures; use `set -o pipefail`.
- `sudo cmd > /root/file` redirect runs as you; use `| sudo tee`.
- `cat file | grep` is harmless but wasteful; `grep pat file` is simpler.
- `uniq` without `sort` giving wrong counts.
""",
    "exercise_guide": r"""Implement count_lines(text). It receives the full stdin content as one string and returns the number of lines as an int, behaving like wc -l applied to a stream. A line is counted for each newline-terminated line; but if the text is non-empty and does not end with a newline, the last partial line should still be counted (a friendlier variant than wc, which counts only newline characters). An empty string has 0 lines. A string that is only "\n" has 1 line. Do not read files or the real stdin; only use the argument. Blank lines count as lines.""",
    "exercise_examples": r"""count_lines("") -> 0
count_lines("a\n") -> 1
count_lines("a\nb\nc\n") -> 3
count_lines("a\nb") -> 2      (last line has no newline)
count_lines("\n\n") -> 2      (two blank lines)
count_lines("one line only") -> 1

Shell equivalent: printf 'a\nb\nc\n' | wc -l prints 3.
Blank lines count: count_lines("a\n\nb\n") -> 3.
Windows line endings are not special; only the newline character splits.""",
  },
  8: {
    "body": r"""## Why this matters

Almost every troubleshooting session boils down to two questions: "which lines contain this?" and "which files match that?". `grep` searches inside content, `find` searches the tree by name, type, size, time and permissions. Together they let you find an error in gigabytes of logs or a stray file on a full disk in seconds.

## Core concepts

`grep PATTERN [FILE...]` prints matching lines. The pattern is a *basic regular expression* by default; `-E` enables extended regex (`+`, `?`, `|`, `()`), `-F` treats it as a fixed string, and `-P` (GNU) enables Perl-style regex.

| grep option | Meaning |
|-------------|---------|
| `-i` | Ignore case |
| `-n` | Show line numbers |
| `-v` | Invert: lines that do not match |
| `-r` / `-R` | Recurse into directories |
| `-l` | Only list file names with a match |
| `-c` | Count matching lines |
| `-w` | Match whole words |
| `-o` | Print only the matched part |
| `-q` | Quiet, exit status only |
| `-A/-B/-C N` | Show N lines after/before/around |

grep exit codes: 0 match found, 1 no match, 2 error.

`find PATH TESTS ACTION` walks a tree evaluating tests left to right.

```
 find /var/log -type f -name "*.log" -mtime -1 -size +1M -print
        |         |          |             |        |       |
      start    regular     name glob   modified   bigger   action
      point     files                  < 1 day    than 1MB (default)

 find ... -exec cmd {} \;     run cmd once per file
 find ... -exec cmd {} +      batch many files per cmd
 find ... -print0 | xargs -0  safe with spaces in names
```

Useful tests: `-type f|d|l`, `-name` (case-sensitive glob; quote it), `-iname`, `-mtime N`, `-mmin N`, `-size +10M`, `-user`, `-perm`, `-maxdepth N`, `-empty`. Combine with `-a`, `-o`, `!` and parentheses (escaped).

A common pattern is matching TODO markers in source: lines containing the word `TODO` (often with a colon), typically `grep -rn "TODO" src/`.

## Worked examples

Search text:

```bash
printf 'alpha\nTODO: fix\nbeta\ntodo later\n' > notes.txt
grep -n TODO notes.txt
# sample output: 2:TODO: fix
grep -in todo notes.txt
# sample output: 2:TODO: fix
# sample output: 4:todo later
grep -vc TODO notes.txt
# sample output: 3
```

Recursive search over a project:

```bash
grep -rn --include='*.py' 'TODO' .
# sample output: ./app/main.py:12:    # TODO: handle errors
grep -rl 'TODO' . | wc -l
# sample output: 4
```

Use grep in a condition:

```bash
if grep -q '^root:' /etc/passwd; then echo has-root; fi
# sample output: has-root
```

Find files:

```bash
find /var/log -maxdepth 1 -type f -name '*.log' -size +100k
# sample output: /var/log/dpkg.log
find . -type f -mtime -1 -name '*.txt'
# sample output: ./notes.txt
find . -type f -empty -delete
```

Run commands on results safely:

```bash
find . -name '*.tmp' -print0 | xargs -0 rm -f
find . -type f -name '*.sh' -exec chmod +x {} +
```

Extended regex:

```bash
grep -E '^(ERROR|WARN)\b' app.log | head
# sample output: ERROR disk full
# sample output: WARN retry 3
```

## Mini-lab

1. `mkdir -p /tmp/lab8/src && cd /tmp/lab8`.
2. Create sample files: `printf 'x\n# TODO: a\n' > src/a.py; printf 'y\n' > src/b.py; printf 'TODO fix\n' > src/c.txt`.
3. `grep -rn TODO src` and read the file:line:text format.
4. `grep -rl TODO src` and `grep -rL TODO src` to list matching and non-matching files.
5. `grep -rn --include='*.py' TODO src` to limit by extension.
6. `find src -type f -name '*.py'` then `find src -type f -newer src/a.py`.
7. `find /etc -maxdepth 1 -name 'host*' 2>/dev/null`.
8. `find src -type f -exec grep -H TODO {} +` and compare with step 3.

## Decision guide / failure modes

Use `grep` when you know the content; use `find` when you know metadata (name, age, size, owner). Use `grep -r` for quick searches, `find ... -exec grep` or `xargs` when you need fine control over which files. For large code bases `rg` (ripgrep) is faster, but `grep` exists everywhere.

Common failures:

- Unquoted globs: `find . -name *.txt` is expanded by the shell if matching files exist in the current directory; write `'*.txt'`.
- Forgetting `-type f` and getting directories too.
- `xargs` without `-0` breaking on names with spaces.
- Treating grep's exit status 1 as an error in `set -e` scripts; use `|| true` when "no match" is acceptable.
- Regex confusion: in basic grep `+` and `|` are literal unless escaped; use `-E`.
- `grep -r pattern` in a directory with huge binary or generated files; use `--exclude-dir`.
""",
    "exercise_guide": r"""Implement match_todo(line). It takes one line of text and returns True if the line contains the marker TODO as a whole word, uppercase exactly, and False otherwise. "TODO: fix" and "# TODO fix this" match; "todo" in lower case does not, and neither do words that merely contain the letters such as "TODOS" or "AUTODOC". Word boundaries mean the characters on each side of TODO are not letters, digits or underscores (start/end of line counts as a boundary). This mimics grep -w TODO and is a good use of a small regular expression.""",
    "exercise_examples": r"""match_todo("TODO: fix") -> True
match_todo("# TODO fix this") -> True
match_todo("x = 1  // TODO") -> True
match_todo("todo later") -> False
match_todo("TODOS list") -> False
match_todo("AUTODOC") -> False
match_todo("") -> False
match_todo("(TODO)") -> True

Shell equivalent: grep -w TODO file
match_todo("TODO") -> True    (whole line is the marker)
match_todo("TODO_ITEM") -> False   (underscore is a word character)""",
  },
  9: {
    "body": r"""## Why this matters

When data is a stream of text lines such as logs, CSV-like exports or config files, `sed` and `awk` transform it without opening an editor. `sed` edits streams (substitute, delete, print lines); `awk` treats each line as fields and can compute sums, averages and reports. They appear constantly in CI scripts and incident work.

## Core concepts

`sed` reads input line by line into a *pattern space*, applies commands, and prints the result. Its workhorse is substitution: `s/REGEX/REPLACEMENT/FLAGS`. Flags: `g` all occurrences on a line, `i` ignore case, a number replaces only that occurrence. `-n` suppresses automatic printing, `p` prints; `-i` edits files in place (use `-i.bak` to keep a backup).

`awk` runs `pattern { action }` rules per line. Fields are `$1`, `$2`, ... split on whitespace by default (`-F,` sets another separator); `$0` is the whole line; `NF` is the number of fields, `NR` the line number. `BEGIN` runs before input, `END` after.

```
  input line:   alice  42  admin
                 $1    $2   $3      NF=3  NR=1
  awk -F: '$3 >= 1000 { print $1 }' /etc/passwd
        |        |            |
   separator  pattern (cond)  action

  sed 's/old/new/g'  <  in.txt  >  out.txt
        stream editor: line -> [ pattern space ] -> output
```

| Task | sed | awk |
|------|-----|-----|
| Replace text | `sed 's/a/b/g'` | `gsub(/a/,"b")` |
| Print line 3 | `sed -n '3p'` | `NR==3` |
| Delete blanks | `sed '/^$/d'` | `NF` |
| Print column 2 | awkward | `{print $2}` |
| Sum a column | not suited | `{s+=$2} END{print s}` |

Pick sed for text rewriting and line selection, awk for column logic and arithmetic.

## Worked examples

Substitute:

```bash
echo "foo bar foo" | sed 's/foo/X/'
# sample output: X bar foo
echo "foo bar foo" | sed 's/foo/X/g'
# sample output: X bar X
```

Delete and select lines:

```bash
seq 1 5 | sed -n '2,4p'
# sample output: 2
# sample output: 3
# sample output: 4
printf 'a\n\nb\n' | sed '/^$/d'
# sample output: a
# sample output: b
```

In-place edit with backup:

```bash
echo "port=80" > app.conf
sed -i.bak 's/^port=.*/port=8080/' app.conf
cat app.conf app.conf.bak
# sample output: port=8080
# sample output: port=80
```

Columns with awk:

```bash
printf 'a 10\nb 20\nc 5\n' > data.txt
awk '{print $1}' data.txt
# sample output: a
# sample output: b
# sample output: c
awk '{s += $2} END {print s}' data.txt
# sample output: 35
```

Filter by condition and format:

```bash
awk '$2 > 8 {printf "%s is big (%d)\n", $1, $2}' data.txt
# sample output: a is big (10)
# sample output: b is big (20)
awk -F: '$3 == 0 {print $1}' /etc/passwd
# sample output: root
```

Average using NR:

```bash
awk '{s += $2} END {print s / NR}' data.txt
# sample output: 11.6667
```

## Mini-lab

1. `cd /tmp && printf 'apple 3\npear 5\nfig 2\n' > fruit.txt`.
2. Run `awk '{print $2}' fruit.txt` and `awk '{s+=$2} END{print s}' fruit.txt` (prints 10).
3. Run `sed 's/ /,/' fruit.txt` and compare with `sed 's/a/A/g'`.
4. Run `sed -n '/pear/p' fruit.txt` and `sed '/fig/d' fruit.txt`.
5. Run `awk 'NR==2 {print $1}' fruit.txt`.
6. Create `cp fruit.txt f2.txt && sed -i.bak 's/pear/plum/' f2.txt` and `diff f2.txt f2.txt.bak`.
7. Use `ps aux | awk '{print $1}' | sort | uniq -c` to count processes per user.
8. Use `awk -F: '{print $1 ":" $7}' /etc/passwd | head -n 3`.

## Decision guide / failure modes

Use `sed` for find-and-replace and line ranges; use `awk` when you need columns, conditions, sums or formatted output; use `cut` for simple fixed-column extraction. For structured formats (JSON, real CSV with quotes) use `jq` or a CSV tool instead; awk and sed will break on embedded separators.

Common failures:

- `sed -i` on macOS needs `-i ''`; GNU and BSD differ. Test on your target system.
- Using `/` in a pattern that contains paths; choose another delimiter: `s|/usr/local|/opt|`.
- Shell quoting: use single quotes so `$1` reaches awk instead of the shell.
- Non-numeric fields (a header row) counted as 0 in sums; skip with `NR>1`.
- Greedy `.*` matching more than expected.
- Editing files in place with no backup; try without `-i` first.
""",
    "exercise_guide": r"""Implement sum_field2(text). The input is multi-line text where each line has whitespace-separated fields. Return the sum of the second field ($2 in awk) across all lines, as a number (int when all values are integers is fine, or float). Lines with fewer than two fields are skipped, as are lines whose second field is not a number (like a header). Blank lines are skipped. An empty input gives 0. This is the Python equivalent of awk '{s += $2} END {print s}' with a little extra safety for headers and short lines.""",
    "exercise_examples": r"""sum_field2("a 10\nb 20\nc 5\n") -> 35
sum_field2("x 1.5\ny 2.5\n") -> 4.0
sum_field2("name qty\napple 3\npear 5\n") -> 8   (header skipped)
sum_field2("onlyone\nb 7\n") -> 7
sum_field2("") -> 0
sum_field2("a    4\n\nb\t6\n") -> 10   (extra spaces and tabs ok)

Shell: awk '{s+=$2} END{print s}' file
sum_field2("a 1\nb notnum\nc 2\n") -> 3   (non-numeric field is skipped)
sum_field2("a -4\nb 10\n") -> 6   (negative numbers are allowed)""",
  },
  10: {
    "body": r"""## Why this matters

On a remote server you often have no graphical editor. You must read long logs, tweak a config and save it using only a terminal. Knowing how to page through output with `less` and how to survive in `vim` (including how to quit without saving) is a basic survival skill; most people first meet vim by accident and get stuck.

## Core concepts

`less` is a pager: it shows a file one screen at a time, does not load everything into memory, and lets you search backwards and forwards. It is the default pager for `man` and `git log`.

| less key | Action |
|----------|--------|
| Space / `f` | Next page |
| `b` | Previous page |
| `g` / `G` | Top / bottom |
| `/text` then `n` / `N` | Search forward, next / previous match |
| `?text` | Search backward |
| `F` | Follow like `tail -f` (Ctrl-C to stop) |
| `-N` | Toggle line numbers |
| `q` | Quit |

Editors: `nano` is simple (commands shown at the bottom, `^O` write, `^X` exit). `vi`/`vim` is on nearly every system and is *modal*.

```
              i, a, o                    :  (colon)
   NORMAL  ------------>  INSERT      NORMAL ------> COMMAND-LINE
   (move, delete,   <----  (type text)              (:w  :q  :wq  :q!)
    copy, paste)    Esc
```

Normal mode is the default; keys are commands (`dd` delete line, `yy` copy line, `p` paste, `u` undo, `x` delete char, `/word` search). `i` enters insert mode; `Esc` returns to normal mode.

| Command-line | Meaning |
|--------------|---------|
| `:w` | Write (save) |
| `:q` | Quit (refuses if unsaved changes) |
| `:wq` or `ZZ` | Save and quit |
| `:q!` | Quit and discard changes |
| `:w !sudo tee %` | Save a root-owned file you opened without sudo |
| `:set number` | Show line numbers |

The escape route when stuck: press `Esc` a couple of times, then type `:q!` and Enter to leave without saving.

## Worked examples

Page through a big file:

```bash
less /var/log/syslog
# sample output: Oct 21 10:00:01 box CRON[1234]: (root) CMD (...)
# sample output: (END)
```

Inside less, type `/error` Enter to search and `n` for the next hit, `q` to exit.

Pipe into the pager:

```bash
dmesg | less -S
ls -l /usr/bin | less
```

`-S` chops long lines instead of wrapping them.

Editing with vim, a typical sequence:

```bash
vim notes.txt
# sample output: (vim opens; press i, type "hello", press Esc)
# sample output: :wq   (then Enter) saves and exits
```

Quit without saving:

```bash
vim notes.txt
# sample output: (you changed text by mistake)
# sample output: Esc, then :q!  and Enter  -> discards changes
```

Choosing your default editor and pager:

```bash
export EDITOR=nano
export PAGER=less
echo "$EDITOR"
# sample output: nano
```

Programs such as `git commit` and `crontab -e` honor `$EDITOR` (or `$VISUAL`).

Nano quick use:

```bash
nano notes.txt
# sample output: (type text, then Ctrl-O Enter to save, Ctrl-X to exit)
```

## Mini-lab

1. `cd /tmp && seq 1 500 > big.txt && less big.txt`; press `G`, `g`, then `/250` Enter, then `q`.
2. Run `less +F /var/log/dpkg.log` (or any log), see it follow, press Ctrl-C then `q`.
3. Run `vim hello.txt`, press `i`, type two lines, press `Esc`, type `:wq` Enter.
4. `cat hello.txt` to verify the content.
5. Reopen with `vim hello.txt`, press `dd` to delete a line, then `:q` (it refuses) and `:q!` to discard.
6. Reopen, press `yy` then `p` to duplicate a line, `u` to undo, `:x` to save and exit.
7. In vim run `:set number`, search with `/two`, go to line 1 with `gg`.
8. Set `export EDITOR=nano` and run `crontab -e` or `visudo` mentally noting which editor opens; quit without changes.

## Decision guide / failure modes

Use `less` for reading, `nano` when you need a quick edit and want on-screen hints, `vim` when it is the only editor available or you want speed with practice. Use `sed -i` for scripted edits rather than opening an editor.

Common failures:

- Stuck in vim: you are in insert mode or the command line; press `Esc` and use `:q!` to quit without saving or `:wq` to save.
- Typing text in normal mode and triggering random commands; check for `-- INSERT --` at the bottom.
- "E37: No write since last change" means use `:q!` or save first.
- Editing a root-owned file without sudo: you get "E45: readonly"; use `sudoedit` or `:w !sudo tee %`.
- Swap file warnings after a crash: another session may still have the file open; check before deleting `.swp`.
- Using `cat` on huge files and flooding the terminal; use `less` or `head`.
""",
    "exercise_guide": r"""Implement vim_quit_nosave(). It takes no arguments and returns the exact string typed in vim's command-line mode to quit without saving changes, which is ":q!" (colon, letter q, exclamation mark). Return it as a plain string with no newline, no spaces, and no Esc character. The exercise is a memory anchor: when you are stuck in vim after accidental edits, press Esc, then type this and press Enter. Remember that ":wq" saves and quits, ":q" refuses with unsaved changes, and the "!" forces the quit.""",
    "exercise_examples": r"""vim_quit_nosave() -> ":q!"

Related commands (for comparison, not returned):
:wq   save and quit
:q    quit (fails with unsaved changes)
:q!   quit and discard changes
ZZ    save and quit in normal mode

The result length is 3 characters and starts with a colon.
The comparison is exact: vim_quit_nosave() == ":q!" is True, while
vim_quit_nosave() == ":wq" is False. No trailing newline is included.""",
  },
  11: {
    "body": r"""## Why this matters

Every running program is a *process*. When a service hangs, a script eats the CPU or a disk fills up, you need to list processes, understand their state, and stop them correctly. Choosing the right signal decides whether a program shuts down cleanly or loses data.

## Core concepts

A process has a PID, a parent PID (PPID), an owner, a state, and resource usage. New processes are made by `fork` and then `exec` a program; PID 1 (`init`/`systemd`) is the ancestor of all others. When a parent dies, children get re-parented to PID 1.

| State | Letter in `ps` | Meaning |
|-------|----------------|---------|
| Running / runnable | `R` | On CPU or in run queue |
| Sleeping (interruptible) | `S` | Waiting for an event |
| Uninterruptible sleep | `D` | Waiting on I/O, cannot be killed |
| Stopped | `T` | Paused by SIGSTOP/Ctrl-Z |
| Zombie | `Z` | Finished, parent has not collected exit status |

Signals are small messages sent to processes. Some can be caught or ignored, but SIGKILL and SIGSTOP cannot.

| Signal | Number | Default / use |
|--------|--------|---------------|
| SIGHUP | 1 | Terminal closed; often "reload config" |
| SIGINT | 2 | Ctrl-C interrupt |
| SIGQUIT | 3 | Ctrl-\ quit with core dump |
| SIGKILL | 9 | Immediate kill, cannot be caught |
| SIGTERM | 15 | Polite "please terminate" (default of `kill`) |
| SIGSTOP | 19 (x86) | Pause, cannot be caught |
| SIGCONT | 18 (x86) | Resume |

```
   kill PID            kill -9 PID
      |                    |
   SIGTERM(15)         SIGKILL(9)
      |                    |
  process handler:     kernel removes process
  flush, cleanup,      immediately; no cleanup,
  exit(0)              temp files and locks remain
```

Always try TERM first, wait a moment, then KILL as last resort. Tools: `ps` (snapshot), `top`/`htop` (live), `pgrep`/`pkill` (by name), `kill`, `killall`, and `/proc/PID/` for details.

## Worked examples

Snapshots:

```bash
ps aux | head -n 3
# sample output: USER  PID %CPU %MEM    VSZ   RSS TTY  STAT START TIME COMMAND
# sample output: root    1  0.0  0.1 168000 11000 ?    Ss   09:00 0:02 /sbin/init
ps -eo pid,ppid,stat,cmd --sort=-%cpu | head -n 3
# sample output:   PID  PPID STAT CMD
```

Find and signal a process:

```bash
sleep 300 &
# sample output: [1] 4321
pgrep -a sleep
# sample output: 4321 sleep 300
kill 4321
# sample output: [1]+  Terminated   sleep 300
```

Signal list and numbers:

```bash
kill -l | head -n 3
# sample output:  1) SIGHUP   2) SIGINT   3) SIGQUIT   4) SIGILL   5) SIGTRAP
kill -l TERM
# sample output: 15
kill -l KILL
# sample output: 9
```

Exit codes after signals:

```bash
sleep 100 & pid=$!; kill -9 $pid; wait $pid; echo $?
# sample output: 137
```

137 is 128 + 9.

Handling a signal in a script:

```bash
trap 'echo cleaning up; exit 0' TERM
# sample output: (script prints "cleaning up" when it receives SIGTERM)
```

Inspect details:

```bash
cat /proc/$$/status | head -n 3
# sample output: Name:	bash
# sample output: Umask:	0022
# sample output: State:	S (sleeping)
```

## Mini-lab

1. Start `sleep 600 &` and note the PID; run `ps -o pid,ppid,stat,cmd -p PID`.
2. Run `pgrep -a sleep` and `pkill sleep`; confirm with `pgrep sleep` (no output, exit status 1).
3. Start `sleep 600 &` again; send `kill -STOP PID`, check `STAT` shows `T`, then `kill -CONT PID`.
4. Send `kill -TERM PID`; then start another and use `kill -9 PID`; compare `echo $?` after `wait`.
5. Run `ps -eo pid,ppid,cmd --forest | head -n 20` to see the tree.
6. Write a script with `trap 'echo got TERM; exit' TERM; while :; do sleep 1; done`; run in background and `kill` it.
7. Try `trap '' KILL` and note that KILL cannot be trapped.
8. Open `top`, press `P` to sort by CPU, `M` for memory, `q` to quit.

## Decision guide / failure modes

Use `kill PID` (TERM) first so programs can clean up; use HUP to reload daemons that support it; use `kill -9` only for hung processes after TERM fails. Prefer `pkill -f` carefully, with `pgrep -af` to preview matches. Use `systemctl stop` for services rather than killing them by hand.

Common failures:

- `kill -9` leaves lock files, temp data and child processes.
- `pkill python` killing unrelated processes; preview with `pgrep -a`.
- Processes in `D` state ignore every signal, even KILL; the fix is the I/O cause.
- Zombies cannot be killed; fix or restart the parent.
- Confusing PID with job number (`%1`); `kill %1` targets a job, `kill 1` targets init.
- Operation not permitted: you do not own the process; use `sudo` carefully.
""",
    "exercise_guide": r"""Implement signal_num(name). The input is a signal name as a string, with or without the "SIG" prefix and in any letter case, for example "TERM", "SIGKILL" or "int". Return the standard Linux signal number as an int: HUP=1, INT=2, QUIT=3, KILL=9, TERM=15. Specifically TERM must return 15 and KILL must return 9. For any other name return -1. Strip surrounding whitespace first. These numbers are the same ones printed by kill -l NAME, and they help you read exit statuses such as 137 (128 + 9) and 143 (128 + 15).""",
    "exercise_examples": r"""signal_num("TERM") -> 15
signal_num("SIGTERM") -> 15
signal_num("KILL") -> 9
signal_num("sigkill") -> 9
signal_num("INT") -> 2
signal_num("HUP") -> 1
signal_num("FOO") -> -1

Shell: kill -l TERM prints 15, kill -l KILL prints 9.
Exit status 143 means the process ended by SIGTERM (128+15).
signal_num("  term ") -> 15   (whitespace and case are ignored)
signal_num("") -> -1""",
  },
  12: {
    "body": r"""## Why this matters

A command that takes minutes should not freeze your terminal, and a long job over SSH should not die when the connection drops. Shell job control lets you run work in the background and bring it back; `tmux` goes further by keeping whole terminal sessions alive on the server so you can detach and reattach later from anywhere.

## Core concepts

The shell tracks *jobs*: pipelines started from this shell, each with a job number (`%1`). A job runs in the *foreground* (owns the terminal) or *background*. Add `&` to start in the background; press Ctrl-Z to suspend the foreground job (SIGTSTP), then `bg` resumes it in the background or `fg` brings it forward.

| Command | Effect |
|---------|--------|
| `cmd &` | Start in background |
| `jobs` | List this shell's jobs |
| `fg %N` | Bring job N to foreground |
| `bg %N` | Continue stopped job in background |
| Ctrl-Z | Suspend foreground job |
| Ctrl-C | Interrupt foreground job (SIGINT) |
| `wait` | Block until background jobs finish |
| `nohup cmd &` | Ignore SIGHUP, output goes to `nohup.out` |
| `disown %N` | Remove job from shell's table so HUP is not sent |

When a terminal closes, the shell sends SIGHUP to its jobs and they usually die. `nohup` and `disown` mitigate that, but `tmux` (or `screen`) is more robust: the session lives in a server process independent of your terminal.

```
  your terminal  <--- attach / detach --->  [ tmux server ]
                                             |-- session "work"
                                             |     |-- window 0: shell, vim
                                             |     +-- window 1: logs (pane split)
                                             +-- session "build"
   SSH drops -> tmux server and programs keep running
```

tmux commands begin with the prefix, Ctrl-b by default, followed by a key.

| Keys / command | Action |
|----------------|--------|
| `tmux new -s NAME` | New named session |
| Ctrl-b d | Detach from session |
| `tmux ls` | List sessions |
| `tmux attach -t NAME` | Reattach |
| Ctrl-b c | New window |
| Ctrl-b n / p | Next / previous window |
| Ctrl-b % | Split into left/right panes |
| Ctrl-b " | Split into top/bottom panes |
| Ctrl-b [ | Scroll/copy mode (q to exit) |
| `tmux kill-session -t NAME` | Remove session |

## Worked examples

Background and job control:

```bash
sleep 120 &
# sample output: [1] 5012
jobs
# sample output: [1]+  Running                 sleep 120 &
fg %1
# sample output: sleep 120
# (press Ctrl-Z)
# sample output: [1]+  Stopped                 sleep 120
bg %1
# sample output: [1]+ sleep 120 &
```

Wait for background work:

```bash
(sleep 2; echo A) & (sleep 1; echo B) & wait
# sample output: B
# sample output: A
```

Survive logout:

```bash
nohup ./long_task.sh > task.log 2>&1 &
# sample output: [1] 5120
disown -h %1
```

tmux workflow:

```bash
tmux new -s build
# sample output: (new green status bar at the bottom)
# run: make -j4   then press Ctrl-b d
# sample output: [detached (from session build)]
tmux ls
# sample output: build: 1 windows (created Wed Oct 21 10:10:00 2026)
tmux attach -t build
```

Scripted detached session:

```bash
tmux new -d -s logs 'tail -f /var/log/syslog'
tmux send-keys -t logs C-c
tmux kill-session -t logs
```

## Mini-lab

1. Install tmux: `sudo apt update && sudo apt install -y tmux` (or in Docker `apt install -y tmux`).
2. Run `sleep 300 &`, then `jobs`, `fg`, Ctrl-Z, `bg`, and finally `kill %1`.
3. Run `tmux new -s lab12`, then `top` in it.
4. Press Ctrl-b d; confirm your prompt returned; run `tmux ls`.
5. Reattach with `tmux attach -t lab12`; top is still running; quit with `q`.
6. Split the window with Ctrl-b % and run `date` on one side; move panes with Ctrl-b arrow.
7. Create a window with Ctrl-b c and switch with Ctrl-b n and p.
8. Exit all shells (`exit`) or `tmux kill-server` to clean up.

## Decision guide / failure modes

Use `&` and `jobs` for short tasks in one shell; use `nohup` for a single fire-and-forget command; use `tmux` for interactive long-running work, multiple panes or remote sessions; use systemd services or cron for things that must start at boot or run unattended.

Common failures:

- Closing the terminal kills plain background jobs because of SIGHUP.
- Background job still writes to the terminal and interrupts typing; redirect its output.
- Background jobs reading stdin get stopped (SIGTTIN); redirect `< /dev/null`.
- Starting tmux inside tmux creates nesting and confusing prefixes; check `$TMUX`.
- Forgetting the session name, then `tmux ls` to find it; many accidental sessions waste memory.
- Job numbers (`%1`) are per shell and are not PIDs.
""",
    "exercise_guide": r"""Implement tmux_detach_keys(). It takes no arguments and returns the default key sequence used to detach from a tmux session, as the lowercase string "ctrl-b d". That means pressing Ctrl-b (the tmux prefix), releasing it, and then pressing d. The session and everything running in it continue in the background; you can come back later with "tmux attach -t NAME". Return exactly that text: lowercase, a hyphen in ctrl-b, and a single space before d. Do not return the tmux command line (like "tmux detach"), only the keystroke description.""",
    "exercise_examples": r"""tmux_detach_keys() -> "ctrl-b d"

Workflow:
tmux new -s work       start a session
(press ctrl-b d)       detach, programs keep running
tmux ls                work: 1 windows ...
tmux attach -t work    return to the session

The returned value is 8 characters long.
The result is lowercase text, not the tmux command "tmux detach".
Other tmux keys use the same prefix: ctrl-b c makes a new window.""",
  },
  13: {
    "body": r"""## Why this matters

A single heavy job can starve everything else on a machine, and a runaway process can exhaust memory or file descriptors and take a service down. `nice` and `renice` influence how the CPU scheduler shares time, while `ulimit` (resource limits) caps what a process may consume. Together they are basic tools for keeping shared systems predictable.

## Core concepts

*Niceness* is a hint to the scheduler of how "nice" a process is to others. Values range from -20 (highest priority, least nice) to 19 (lowest priority, nicest); the default is 0. A higher niceness number therefore means lower priority: the process gets a smaller share of CPU when there is contention. Ordinary users can only increase niceness of their own processes; only root can lower it (use negative values). Niceness only matters when CPUs are busy; on an idle machine every process runs at full speed.

```
 niceness:  -20 ........ 0 ........ 19
            greedy    default    polite
            high priority        low priority (higher number)

 ps -o pid,ni,pri,cmd    NI = nice value, PRI = kernel priority
 nice -n 10 cmd          start with niceness +10
 renice -n 5 -p PID      change a running process
```

Resource limits (rlimits) are per process and inherited by children. Each has a *soft* limit (enforced) and a *hard* limit (ceiling for the soft one; only root can raise it).

| `ulimit` flag | Resource |
|---------------|----------|
| `-n` | Open file descriptors |
| `-u` | Number of user processes |
| `-v` | Virtual memory (KB) |
| `-s` | Stack size (KB) |
| `-c` | Core file size |
| `-t` | CPU time (seconds) |
| `-f` | Max file size created |
| `-a` | Show all |
| `-S` / `-H` | Select soft / hard limit |

`ulimit` is a shell builtin and affects the current shell and its children. Persistent per-user limits live in `/etc/security/limits.conf` (applied by PAM); for services use `LimitNOFILE=` and friends in a systemd unit. Check a running process with `cat /proc/PID/limits`. For stronger control of CPU and memory in groups of processes, modern systems use cgroups (`systemd-run -p MemoryMax=...`).

## Worked examples

See niceness:

```bash
ps -o pid,ni,cmd -p $$
# sample output:   PID  NI CMD
# sample output:  1201   0 -bash
nice
# sample output: 0
```

Start with lower priority:

```bash
nice -n 10 sh -c 'nice'
# sample output: 10
nice -n 19 gzip -9 bigfile &
```

Change a running process:

```bash
sleep 300 &
# sample output: [1] 6001
renice -n 5 -p 6001
# sample output: 6001 (process ID) old priority 0, new priority 5
ps -o pid,ni,cmd -p 6001
# sample output:   PID  NI CMD
# sample output:  6001   5 sleep 300
renice -n -5 -p 6001
# sample output: renice: failed to set priority for 6001 (process ID): Permission denied
```

Limits:

```bash
ulimit -n
# sample output: 1024
ulimit -Hn
# sample output: 1048576
ulimit -n 256
ulimit -n
# sample output: 256
```

Enforcement with a subshell:

```bash
( ulimit -t 1; while :; do :; done )
# sample output: Killed
```

The loop is stopped after about one second of CPU time (SIGXCPU or SIGKILL depending on soft and hard limits).

Inspect another process:

```bash
grep 'open files' /proc/$$/limits
# sample output: Max open files            1024                 1048576              files
```

## Mini-lab

1. Run `ps -o pid,ni,cmd -p $$` and `nice` to see the default 0.
2. Start `nice -n 15 sleep 200 &` and verify NI=15 with `ps`.
3. Run `renice -n 19 -p PID`; then try to lower it back with `renice -n 0 -p PID` and read the error.
4. As root (or in a container) run `sudo nice -n -5 sleep 100 &` and check NI=-5.
5. Compare CPU shares: run two `nice -n 0 sh -c 'while :; do :; done' &` loops and one with `-n 19` pinned to one CPU (`taskset -c 0`); watch `top`.
6. Run `ulimit -a` and identify open files, processes and stack size.
7. In a subshell run `( ulimit -n 20; ls /proc/self/fd | wc -l )`; then cause "Too many open files" by opening more with a small script.
8. Clean up with `pkill -f 'while :'` and `jobs; kill %1`.

## Decision guide / failure modes

Use `nice` for batch work (backups, compression, builds) that should yield to interactive tasks; use `renice` on something already running; use `ionice` for disk-heavy jobs; use `ulimit` for quick shell-scoped caps and systemd or cgroups for services and containers. Raise `nofile` for servers that open many sockets.

Common failures:

- Believing `nice -n 19` makes a job fast or slow in absolute terms; it matters only under contention.
- Thinking a higher number means higher priority; it is the opposite.
- `Too many open files` in a busy server: soft limit too low (often 1024); raise via limits.conf or `LimitNOFILE`.
- `ulimit` settings vanishing after logout because they were only set in a shell, not persisted.
- Trying to raise a hard limit as a normal user; lowering is allowed, raising is not.
- Confusing `-n` of `nice` (adjustment) with `ulimit -n` (open files).
""",
    "exercise_guide": r"""Implement higher_nice_means(). It takes no arguments and returns the short string "lower-priority", describing what a higher niceness value means for a process: the process is nicer to others, so the scheduler gives it a smaller share of CPU time when there is contention. Return exactly "lower-priority" in lowercase with a hyphen. Niceness ranges from -20 (highest priority) to 19 (lowest priority), the default is 0, and only root may decrease a niceness value. This is the key idea behind nice and renice.""",
    "exercise_examples": r"""higher_nice_means() -> "lower-priority"

Examples in the shell:
nice -n 10 backup.sh      runs with lower priority than default
renice -n 19 -p 4321      make PID 4321 the politest process
nice -n -5 cmd            needs root: higher priority

Niceness 19 -> lowest priority, niceness -20 -> highest priority.""",
  },
}

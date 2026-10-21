"""Extra curriculum content for modules 14-27 (body, exercise guide, examples)."""

from __future__ import annotations

EXTRA: dict[int, dict] = {
  14: {
    "body": r"""
## Why this matters

Every sysadmin task you type twice deserves to become a script. A script is
just a text file of shell commands, but it adds three things the interactive
prompt lacks: repeatability, reviewability, and the ability to run unattended
(cron, systemd, CI). Bash is on nearly every Linux host, so a small bash
script is the cheapest automation you can ship.

The danger is that bash is forgiving in the wrong ways. An unset variable
silently expands to nothing, a failed command does not stop the script, and
an unquoted value splits into several words. This lesson builds the habits
that keep tiny scripts predictable: a shebang, quoting, positional
parameters, and default values such as `${1:-world}`.

## Core concepts

| Concept | Syntax | Meaning |
|---------|--------|---------|
| Shebang | `#!/usr/bin/env bash` | Tells the kernel which interpreter runs the file |
| Executable bit | `chmod +x hello.sh` | Lets you run `./hello.sh` directly |
| Variable | `name=Ada` then `"$name"` | No spaces around `=`; quote on use |
| Positional args | `$1 $2 ... $#` | Arguments passed to the script |
| All args | `"$@"` | Each argument kept as a separate word |
| Default value | `${1:-world}` | Use `$1`, or `world` if unset or empty |
| Command substitution | `$(date +%F)` | Replace with the command output |
| Exit status | `$?` | 0 means success, non-zero means failure |

How a script runs:

```
  you type: ./hello.sh Ada
        |
        v
  kernel reads first line  (#!/usr/bin/env bash)
        |
        v
  bash starts, receives file + args
        |        $0=./hello.sh  $1=Ada  $#=1
        v
  commands run top to bottom
        |
        v
  last command's status becomes the script's exit code
```

Quoting rules in one line: single quotes keep text literal, double quotes
allow `$var` and `$(cmd)` to expand but prevent word splitting, and no quotes
means the shell splits on whitespace and expands globs.

## Worked examples

Create a script that greets a name, defaulting to `world`:

```bash
cat > hello.sh <<'EOF'
#!/usr/bin/env bash
name=${1:-world}
echo "Hello, $name"
EOF
chmod +x hello.sh
./hello.sh
./hello.sh Ada
./hello.sh "Ada Lovelace"
```

Sample output:

```
Hello, world
Hello, Ada
Hello, Ada Lovelace
```

The same idea inside a function, which is what the exercise uses:

```bash
hello() {
  local name=${1:-world}
  echo "Hello, $name"
}
hello
hello Linus
```

Sample output:

```
Hello, world
Hello, Linus
```

Difference between `:-` and `-`:

```bash
unset x; echo "[${x:-fallback}]"
x=""; echo "[${x:-fallback}]"
x=""; echo "[${x-fallback}]"
```

Sample output:

```
[fallback]
[fallback]
[]
```

Checking the exit status and counting arguments:

```bash
./hello.sh a b c; echo "status=$?"
set -- one two three; echo "count=$#"
```

Sample output:

```
Hello, a
status=0
count=3
```

## Mini-lab

1. Create a directory `~/lab14` and `cd` into it.
2. Write `hello.sh` with the shebang, `name=${1:-world}`, and an `echo`.
3. Run it with `bash hello.sh` first, then `chmod +x` and run `./hello.sh`.
4. Run it with no argument, one argument, and a quoted two-word argument.
5. Remove the quotes from `"$name"` in the echo and rerun with
   `"Ada   Lovelace"`; note how the spaces collapse. Restore the quotes.
6. Add `echo "args: $#"` and confirm the count for each run.
7. Run `bash -n hello.sh` (syntax check) and `bash -x ./hello.sh Ada` (trace)
   and read the trace output line by line.
8. Move the greeting into a `hello()` function and call it from the bottom.

## Decision guide / failure modes

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `Permission denied` running `./hello.sh` | No executable bit | `chmod +x hello.sh` |
| `bad interpreter: No such file` | Wrong shebang or CRLF line endings | Fix path; convert with `dos2unix` |
| `name: command not found` | Space around `=` (`name = Ada`) | Write `name=Ada` |
| Output loses spaces | Unquoted variable | Use `"$name"` |
| Greeting is `Hello, ` | Variable empty, no default | Use `${1:-world}` |
| Works in terminal, fails in cron | Different PATH and cwd | Use absolute paths |

When to use bash: glue between commands, file and process orchestration,
small admin tasks. When to switch language: heavy parsing, JSON, data
structures, or anything over a couple of hundred lines; Python or Go will
be safer there.

Rules of thumb: always start with a shebang, quote every expansion, prefer
`${var:-default}` over testing in an `if`, and run `bash -n` and `bash -x`
before trusting a script.
""",
    "exercise_guide": """Open exercise.sh and finish the hello function. It must print exactly "Hello, <name>" on one line, using the first argument as the name. When no argument is given (or it is empty), the name must be "world". Keep the local name variable that is already there and use the ${1:-world} default style from the lesson. Quote the variable when you print it, so a name with spaces such as "Ada Lovelace" is kept intact. Do not print anything else: no extra spaces, no trailing text. Run ./test.sh until every check passes, then run the function by hand with no argument, one argument, and a two-word quoted argument.""",
    "exercise_examples": """hello            -> Hello, world
hello Ada        -> Hello, Ada
hello "Ada L"    -> Hello, Ada L
hello ""         -> Hello, world

Only one line of output per call, ending with a newline. The function returns 0. The text is exactly "Hello, " followed by the name, with a comma and one space.

Try also: ./hello.sh with no file mode set -> use bash hello.sh. Syntax check: bash -n hello.sh prints nothing when fine. Trace: bash -x hello.sh Ada shows + name=Ada then + echo 'Hello, Ada'.""",
  },
  15: {
    "body": r"""
## Why this matters

Once a script grows past ten lines you want named, reusable pieces. Bash
functions give you that, but they behave differently from functions in most
languages: they do not return values, they return an exit status between 0
and 255. Data comes back through stdout (captured with `$(...)`) or through
global variables. Callers decide what to do by checking `$?` or using the
function directly in an `if`.

Exit codes are the shared language of Unix tools. `grep` returns 1 when
nothing matches, `ssh` returns 255 on connection failure, `curl` returns 22
on HTTP errors with `-f`. Your functions should follow the same convention
so that other scripts, cron, and CI can react correctly.

## Core concepts

| Concept | Syntax | Meaning |
|---------|--------|---------|
| Define function | `name() { ...; }` | Body runs in the current shell |
| Arguments | `$1 $2 $#` | Inside a function these are the function's args |
| Return status | `return 2` | Sets `$?` for the caller (0-255) |
| Output value | `echo ok` | Caller captures with `$(fn)` |
| Local variable | `local x=1` | Scope limited to the function |
| Arg count check | `[ "$#" -ge 1 ]` | Test numerically |
| Usage error code | `2` | Convention: misuse of command |
| `exit` vs `return` | `exit 2` | `exit` ends the whole script |

Common exit codes:

| Code | Convention |
|------|-----------|
| 0 | Success |
| 1 | General failure |
| 2 | Misuse, bad arguments |
| 126 | Found but not executable |
| 127 | Command not found |
| 130 | Killed by Ctrl+C |

Data flow of a call:

```
  caller                      function
  ------                      --------
  require_one_arg foo  --->   $1=foo  $#=1
                              [ "$#" -ge 1 ] ?
                                 | yes            | no
                                 v                v
                              echo ok         return 2
                                 |                |
  stdout "ok"   <----------------+                |
  $? = 0                                          |
  $? = 2        <---------------------------------+
```

## Worked examples

A function that checks its arguments:

```bash
require_one_arg() {
  if [ "$#" -ge 1 ]; then
    echo ok
    return 0
  fi
  echo "usage: require_one_arg VALUE" >&2
  return 2
}

require_one_arg hello
echo "status=$?"
require_one_arg
echo "status=$?"
```

Sample output:

```
ok
status=0
usage: require_one_arg VALUE
status=2
```

Using the status in an `if`, and capturing stdout:

```bash
if require_one_arg x >/dev/null; then echo accepted; fi
result=$(require_one_arg x)
echo "captured=$result"
```

Sample output:

```
accepted
captured=ok
```

Local versus global variables:

```bash
counter=1
bump() { local counter=99; counter=$((counter+1)); echo "in: $counter"; }
bump
echo "out: $counter"
```

Sample output:

```
in: 100
out: 1
```

Forwarding all arguments safely:

```bash
wrapper() { printf '[%s]\n' "$@"; }
wrapper "a b" c
```

Sample output:

```
[a b]
[c]
```

## Mini-lab

1. Create `lib.sh` and put `require_one_arg` in it.
2. Source it: `source ./lib.sh`.
3. Call it with zero, one, and three arguments and print `$?` each time.
4. Send the usage message to stderr and prove it with
   `require_one_arg 2>/dev/null` (message disappears) and
   `require_one_arg 2>&1` (message shows).
5. Write `greet_or_fail` that calls `require_one_arg "$1"` and exits the
   script with the same status if it fails.
6. Remove `local` from a variable inside a function and observe the leak
   into the caller.
7. Test with `[ "$#" -ge 1 ]` versus `[ -n "$1" ]` and pass an empty string
   `""` to see the difference.
8. Run `echo $?` twice in a row and explain why the second result is 0.

## Decision guide / failure modes

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `$?` is always 0 | You read it after another command | Capture `rc=$?` immediately |
| Whole script exits on error | Used `exit` in a function | Use `return` in functions |
| Function prints but caller gets nothing | Value was echoed, not captured | `x=$(fn)` |
| Variable changed unexpectedly | Missing `local` | Declare locals |
| `[: too many arguments` | Unquoted `$1` with spaces | Quote: `[ -n "$1" ]` |
| Exit code 256 wraps to 0 | Codes are modulo 256 | Stay within 0-255 |

Return versus echo: use `return` for success or failure, `echo` for data.
Never mix them in a way that makes the output ambiguous; send diagnostics
to stderr with `>&2` so stdout stays clean for capture.

Rule of thumb: validate arguments first, fail fast with code 2, document the
usage line, and keep functions small enough to test on their own.
""",
    "exercise_guide": """Implement require_one_arg in exercise.sh. If the function receives at least one argument it must print the word ok and return 0. If it receives no arguments it must return 2 and should not print ok. You may print a usage message to stderr (use >&2) but nothing on stdout in the failure case. Count arguments with `$#` and compare numerically with `[ "$#" -ge 1 ]`. Use return, not exit, so the sourcing shell is not killed. After ./test.sh passes, call the function by hand and read $? right after each call.""",
    "exercise_examples": """require_one_arg foo        -> prints: ok      status 0
require_one_arg a b c      -> prints: ok      status 0
require_one_arg            -> prints nothing  status 2
require_one_arg ""         -> prints: ok      status 0  (one argument, even if empty)

Check the status immediately: require_one_arg; echo "rc=$?" shows rc=2.

In a script: if require_one_arg "$1" >/dev/null; then echo proceed; else echo usage; fi
Capture: msg=$(require_one_arg x) gives msg=ok. Exit codes: 0 success, 2 means bad usage by convention. Remember return ends the function, exit ends the whole script.""",
  },
  16: {
    "body": r"""
## Why this matters

Automation that runs while you sleep must be careful. A script that does
`rm -rf "$dir"/*` with an empty `$dir` becomes `rm -rf /*`. Real incidents
have happened exactly this way. Safe shell means refusing to continue when
inputs are missing, failing loudly instead of silently, and testing each
condition explicitly.

This lesson covers the test command `[ ]` and `[[ ]]`, strict mode with
`set -euo pipefail`, guard functions that stop a script before it does harm,
and basic ways to test scripts: dry-run flags, `shellcheck`, and tiny
assertion helpers.

## Core concepts

| Concept | Syntax | Meaning |
|---------|--------|---------|
| File test | `[ -d "$d" ]` | True if `$d` is a directory |
| String test | `[ -n "$s" ]` / `[ -z "$s" ]` | Non-empty / empty |
| Numeric test | `[ "$a" -eq 3 ]` | Integer compare |
| Bash test | `[[ $s == abc* ]]` | Pattern match, no word splitting |
| Exit on error | `set -e` | Stop when a command fails |
| Unset is error | `set -u` | Using an undefined variable fails |
| Pipe failures | `set -o pipefail` | Pipeline fails if any stage fails |
| Trap | `trap 'cleanup' EXIT` | Run code on exit |
| Linter | `shellcheck script.sh` | Static analysis of bad patterns |

Layers of defence:

```
  user input / env
        |
        v
  +------------------+   empty? not a dir? -> die (return 1)
  | guard function   |
  +------------------+
        | valid
        v
  +------------------+   set -euo pipefail
  | strict mode      |   stops on first surprise
  +------------------+
        |
        v
  +------------------+   --dry-run prints, does not run
  | dry-run switch   |
  +------------------+
        |
        v
  real action (rm, mv, rsync)
```

## Worked examples

A guard that refuses empty input and echoes the value otherwise:

```bash
safe_dir_or_die() {
  local d=${1:-}
  if [ -z "$d" ]; then
    echo "error: directory required" >&2
    return 1
  fi
  echo "$d"
}

safe_dir_or_die /tmp
echo "status=$?"
safe_dir_or_die
echo "status=$?"
```

Sample output:

```
/tmp
status=0
error: directory required
status=1
```

Using it before a dangerous action:

```bash
target=$(safe_dir_or_die "$1") || exit 1
rm -rf -- "${target:?}"/old-*
```

The `${var:?msg}` form aborts when the variable is unset or empty:

```bash
unset dir
bash -c 'rm -rf "${dir:?dir is empty}"/x'; echo "rc=$?"
```

Sample output:

```
bash: line 1: dir: dir is empty
rc=1
```

Strict mode catching a typo:

```bash
bash -c 'set -u; echo "$undefined_name"'; echo "rc=$?"
```

Sample output:

```
bash: line 1: undefined_name: unbound variable
rc=1
```

Cleanup with trap and a dry-run flag:

```bash
tmp=$(mktemp -d)
trap 'rm -rf -- "$tmp"' EXIT
DRY=${DRY:-0}
run() { if [ "$DRY" = 1 ]; then echo "+ $*"; else "$@"; fi; }
DRY=1 run mv /var/log/app.log /var/log/app.log.1
```

Sample output:

```
+ mv /var/log/app.log /var/log/app.log.1
```

## Mini-lab

1. Write `safe_dir_or_die` and test it with an empty string, no argument,
   and `/tmp`.
2. Add a second check that the path exists with `[ -d "$d" ]`; make it
   return 1 for `/does/not/exist`.
3. Create `cleanup.sh` using `set -euo pipefail` and a `mktemp -d`
   workspace plus `trap ... EXIT`.
4. Add a `DRY` switch so `DRY=1 ./cleanup.sh` only prints actions.
5. Trigger a failure on purpose (`false` mid-script) and watch `set -e` stop
   it; then add `|| true` where failure is acceptable.
6. Run `shellcheck cleanup.sh` if installed (`apt install shellcheck`) and
   fix every warning.
7. Write a tiny `assert_eq` function and use it to test `safe_dir_or_die`.

## Decision guide / failure modes

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Script continues after error | No `set -e` | Add strict mode, or check `$?` |
| `set -e` does not stop in `if` | Commands in conditions are exempt | Test explicitly |
| `grep` kills script with `set -e` | No match returns 1 | `grep ... || true` |
| `[ $x = a ]` breaks on empty | Unquoted variable | `[ "$x" = a ]` |
| Deleted wrong files | Empty variable in path | `${var:?}` and guard functions |
| Temp files left behind | No cleanup on failure | `trap ... EXIT` |

Strict mode is a safety net, not a design. Prefer explicit guards for the
cases you know, keep dry-run available for anything destructive, and always
use `--` before user-supplied paths so a name like `-rf` is not read as an
option.
""",
    "exercise_guide": """Implement safe_dir_or_die in exercise.sh. It takes one argument, the directory name. If the argument is missing or an empty string, the function must return 1 (you may write an error to stderr but print nothing to stdout). Otherwise it must print the argument unchanged on stdout and return 0. Do not check whether the directory exists; this exercise only guards against empty input. Quote the variable everywhere. Run ./test.sh, then try the function in a script that uses set -u to confirm it never touches an unset variable.""",
    "exercise_examples": """safe_dir_or_die /tmp       -> prints: /tmp          status 0
safe_dir_or_die "my dir"   -> prints: my dir        status 0
safe_dir_or_die ""         -> prints nothing        status 1
safe_dir_or_die            -> prints nothing        status 1

Typical use: target=$(safe_dir_or_die "$1") || exit 1

With set -u a plain $1 on an empty call aborts the script, so the ${1:-} default inside the function is what makes the guard safe. A caller can combine it with the strict form: d=$(safe_dir_or_die "$1") || exit 1; rm -rf -- "${d:?}"/old.""",
  },
  17: {
    "body": r"""
## Why this matters

Nearly every outage ticket contains the words "cannot connect". To debug
one you need a mental model of what sits between two machines: an IP
address to find the host, DNS to turn names into addresses, a port to pick
the service, and a route to get packets there. If you can name the layer
that is broken, the fix is usually one command away.

This lesson gives you the minimum vocabulary and the commands to inspect
each layer on a Linux host: `ip`, `resolvectl` or `dig`, `getent`, `ping`,
and the well-known port numbers, such as 443 for HTTPS.

## Core concepts

| Concept | Example | Meaning |
|---------|---------|---------|
| IPv4 address | `192.168.1.20/24` | 32-bit host address plus prefix length |
| IPv6 address | `2001:db8::1` | 128-bit address |
| Gateway | `192.168.1.1` | Next hop for non-local traffic |
| DNS | `example.com -> 93.184.216.34` | Name to address mapping |
| Port | `443` | 16-bit number selecting a service on a host |
| Protocol | TCP / UDP | Reliable stream versus datagrams |
| Socket | `10.0.0.5:443` | IP plus port plus protocol |
| `/etc/resolv.conf` | `nameserver 127.0.0.53` | Where the resolver asks |
| `/etc/hosts` | `127.0.0.1 localhost` | Local static name overrides |

Well-known ports:

| Port | Service |
|------|---------|
| 22 | SSH |
| 53 | DNS |
| 80 | HTTP |
| 443 | HTTPS |
| 25 | SMTP |
| 5432 | PostgreSQL |

What happens when you open https://example.com:

```
  browser/curl
     |  1. name lookup: example.com ?
     v
  resolver --(/etc/hosts, then DNS server)--> 93.184.216.34
     |
     |  2. route lookup: not on my subnet -> send to gateway
     v
  gateway --> internet --> server 93.184.216.34
     |
     |  3. TCP connect to port 443 (default https port)
     v
  TLS handshake, then HTTP request
```

## Worked examples

Show addresses and routes:

```bash
ip -br addr
ip route
```

Sample output:

```
lo        UNKNOWN  127.0.0.1/8 ::1/128
eth0      UP       192.168.1.20/24 fe80::a00:27ff:fe4e:66a1/64
default via 192.168.1.1 dev eth0 proto dhcp metric 100
192.168.1.0/24 dev eth0 proto kernel scope link src 192.168.1.20
```

Resolve a name the way applications do (honours `/etc/hosts` and NSS):

```bash
getent hosts example.com
dig +short example.com
```

Sample output:

```
2606:2800:21f:cb07:6820:80da:af6b:8b2c example.com
93.184.216.34
```

Look up a service port from the system database:

```bash
getent services https
grep -w 443 /etc/services | head -2
```

Sample output:

```
https                 443/tcp
https           443/tcp
https           443/udp         # http protocol over TLS/SSL
```

Reachability and path:

```bash
ping -c 2 192.168.1.1
tracepath -n example.com | head -3
```

Sample output:

```
64 bytes from 192.168.1.1: icmp_seq=1 ttl=64 time=0.612 ms
64 bytes from 192.168.1.1: icmp_seq=2 ttl=64 time=0.540 ms
 1?: [LOCALHOST]                      pmtu 1500
 1:  192.168.1.1                      0.713ms
```

A shell helper for the exercise idea:

```bash
default_https_port() { echo 443; }
default_https_port
```

Sample output:

```
443
```

## Mini-lab

1. Run `ip -br addr` and write down your IPv4 address and prefix length.
2. Run `ip route` and identify the default gateway.
3. Ping the gateway, then ping `1.1.1.1`, then ping `example.com`.
4. Edit nothing, but read `/etc/resolv.conf` and `/etc/hosts`.
5. Compare `getent hosts example.com` with `dig +short example.com`.
6. Add a temporary line to `/etc/hosts` for `lab.test` pointing at
   `127.0.0.1` (needs sudo), run `getent hosts lab.test`, then remove it.
7. Use `getent services ssh http https` and fill a three-row table of
   service and port.
8. Use `tracepath -n example.com` and count the hops.

## Decision guide / failure modes

| Symptom | Layer | Check |
|---------|-------|-------|
| `ping 1.1.1.1` fails | Link / route | `ip addr`, `ip route`, cable or Wi-Fi |
| Ping IP works, name fails | DNS | `resolvectl status`, `dig` |
| Name resolves, connect refused | Service / port | Is the daemon listening? |
| Name resolves, connect times out | Firewall or routing | Security group, `iptables`, route |
| Works by IP, wrong host by name | `/etc/hosts` override | `getent hosts name` |
| Ping blocked but service up | ICMP filtered | Test the real TCP port |

Work bottom-up: address, route, DNS, port, application. Refused means a
host answered and said no; timeout means nothing answered. Remember that
`ping` proves only ICMP; use the real port for the real answer, and that
the default port for https is 443 and for http is 80.
""",
    "exercise_guide": """Implement default_https_port in exercise.sh so it prints the standard TCP port used by HTTPS, with nothing else on the line. It takes no arguments. Use echo and a plain number; the test compares the output exactly, so avoid extra spaces or text such as "port". When done, confirm the value against the system database with getent services https and read how the port number, protocol and service name relate. Optionally, write a second helper of your own for http (80) and ssh (22) to practice the table from the lesson.""",
    "exercise_examples": """default_https_port    -> 443

The output is exactly the three characters 443 followed by a newline. Cross-check:
getent services https     -> https    443/tcp
For comparison, http is 80 and ssh is 22.

Related lookups: getent services ssh -> ssh 22/tcp; getent services domain -> domain 53/tcp. Typical URL form: https://host/ implies port 443; http://host/ implies port 80; an explicit https://host:8443/ overrides the default. Print only digits, no label.""",
  },
  18: {
    "body": r"""
## Why this matters

"Is my service actually listening?" is the first question in network
debugging, and `ss` answers it in one line. The second question is "is
something blocking it?", which brings in firewalls (`ufw`, `firewalld`,
`nftables`, `iptables`). Together they separate a dead daemon from a
blocked port, which saves hours.

`ss` replaced `netstat` on modern systems. It reads kernel socket tables
directly, is faster, and shows more state. The classic flag combination is
`-tulpn`, which you will type thousands of times in your career.

## Core concepts

| Flag | Meaning |
|------|---------|
| `-t` | TCP sockets |
| `-u` | UDP sockets |
| `-l` | Listening sockets only |
| `-p` | Show owning process (needs root for others' processes) |
| `-n` | Numeric ports and addresses, no DNS lookups |
| `-a` | All states, not just listening |
| `-s` | Summary statistics |

So `ss -tulpn` means: TCP and UDP, listening, with process, numeric.

Address columns matter:

| Local address | Reachable from |
|---------------|----------------|
| `127.0.0.1:5432` | Only this machine |
| `0.0.0.0:22` | Any IPv4 interface |
| `[::]:22` | Any IPv6 interface (often IPv4 too) |
| `192.168.1.20:80` | Only that interface address |

Packet path with a host firewall:

```
  client --> NIC --> [ firewall rules ] --> socket (ss shows LISTEN) --> process
                          |
          drop/reject here: ss still shows LISTEN,
          but the client sees timeout (drop) or refused (reject)
```

Firewall front ends:

| Tool | Distro family | Backend |
|------|---------------|---------|
| `ufw` | Ubuntu/Debian | iptables/nftables |
| `firewalld` (`firewall-cmd`) | RHEL/Fedora | nftables |
| `nft` | all modern | kernel netfilter |
| `iptables` | legacy | kernel netfilter |

## Worked examples

List listeners:

```bash
sudo ss -tulpn
```

Sample output:

```
Netid State  Recv-Q Send-Q Local Address:Port Peer Address:Port Process
udp   UNCONN 0      0      127.0.0.53%lo:53   0.0.0.0:*  users:(("systemd-resolve",pid=612,fd=13))
tcp   LISTEN 0      4096   0.0.0.0:22         0.0.0.0:*  users:(("sshd",pid=801,fd=3))
tcp   LISTEN 0      511    127.0.0.1:8080     0.0.0.0:*  users:(("python3",pid=2210,fd=4))
```

Who owns a given port:

```bash
sudo ss -tlpn 'sport = :22'
```

Sample output:

```
State  Recv-Q Send-Q Local Address:Port Peer Address:Port Process
LISTEN 0      4096   0.0.0.0:22         0.0.0.0:*  users:(("sshd",pid=801,fd=3))
```

Established connections and summary:

```bash
ss -tn state established | head -3
ss -s | head -2
```

Sample output:

```
Recv-Q Send-Q Local Address:Port   Peer Address:Port
0      0      192.168.1.20:22      192.168.1.5:50122
Total: 214
```

Firewall inspection and a minimal ufw policy:

```bash
sudo ufw status verbose
sudo ufw allow 22/tcp
sudo ufw allow 443/tcp
sudo ufw enable
sudo nft list ruleset | head -5
```

Sample output:

```
Status: active
Default: deny (incoming), allow (outgoing)
22/tcp                     ALLOW IN    Anywhere
443/tcp                    ALLOW IN    Anywhere
```

The helper from the exercise:

```bash
ss_listening_flags() { echo "-tulpn"; }
sudo ss $(ss_listening_flags)
```

## Mini-lab

1. Run `sudo ss -tulpn` and list every listening port with its process.
2. Start a throwaway listener: `python3 -m http.server 8088 &`.
3. Find it with `ss -tlpn | grep 8088`; note the local address.
4. Restart it bound to localhost only: `--bind 127.0.0.1`; compare columns.
5. Kill it with `kill %1`, confirm it vanished from `ss`.
6. On a VM, check the firewall: `sudo ufw status` or `sudo firewall-cmd
   --list-all`; write down which ports are open.
7. Allow a port, test it from another host with `nc -vz HOST 8088`, then
   remove the rule.
8. Run `ss -s` and compare totals before and after opening a few
   connections.

## Decision guide / failure modes

| Symptom | Meaning | Action |
|---------|---------|--------|
| Port not in `ss -tulpn` | Daemon not running or wrong port | Check service logs |
| Listening on `127.0.0.1` only | Not reachable remotely | Bind `0.0.0.0` or proxy |
| Listening, remote times out | Firewall drops | Open port in firewall/security group |
| Listening, remote refused | Reject rule or wrong IP | Check rules and address |
| Process column empty | Not root | Use `sudo` |
| `Address already in use` | Another process owns port | `ss -tlpn 'sport = :PORT'` |

Order of diagnosis: is it listening (ss), is it bound where expected, does
the firewall allow it, and does the network path (cloud security group)
allow it. Before enabling a firewall over SSH, always allow port 22 first,
or you will lock yourself out.
""",
    "exercise_guide": """Implement ss_listening_flags in exercise.sh. It takes no arguments and must print the exact flag string most admins use to list listening TCP and UDP sockets with owning process and numeric addresses. The test compares the output exactly, so print only the flags with the leading dash and no extra text. Before finishing, run sudo ss with those flags on a real host and write one sentence in your notes for each letter t, u, l, p and n, describing what it adds to the output.""",
    "exercise_examples": """ss_listening_flags    -> -tulpn

Used as: sudo ss $(ss_listening_flags)
The letters mean: t=TCP, u=UDP, l=listening only, p=process, n=numeric.
Do not print ss itself or any explanation, only the flag string.

Example on a host:
sudo ss -tulpn | head -3 shows Netid, State, Local Address:Port and a users:(("sshd",pid=801,fd=3)) column. Without p you lose the process; without n names such as ssh replace 22. Output of the function itself is just the dash and five letters.""",
  },
  19: {
    "body": r"""
## Why this matters

HTTP is the protocol behind web apps, REST APIs, health checks, package
mirrors, and cloud metadata services. A browser hides the details; `curl`
shows them. With `curl` you can see status codes, headers, redirects, TLS
problems, and timing, and you can script health checks that decide whether
a deployment worked.

Knowing the status-code families lets you read an incident at a glance:
2xx worked, 3xx redirected, 4xx the client was wrong, 5xx the server broke.

## Core concepts

| Flag | Meaning |
|------|---------|
| `-s` | Silent: hide progress meter |
| `-S` | Show errors even with `-s` |
| `-I` | HEAD request, headers only |
| `-i` | Include response headers in output |
| `-L` | Follow redirects |
| `-o file` | Write body to file |
| `-w '%{http_code}'` | Print a field after finishing |
| `-f` | Fail (exit 22) on HTTP 4xx/5xx |
| `-X POST -d` | Method and body |
| `-H 'K: V'` | Add header |
| `--max-time 5` | Total timeout in seconds |
| `-k` | Skip TLS verification (avoid in production) |

Status code families:

| Range | Meaning | Examples |
|-------|---------|----------|
| 1xx | Informational | 101 |
| 2xx | Success | 200 OK, 201, 204 |
| 3xx | Redirect | 301, 302, 304 |
| 4xx | Client error | 400, 401, 403, 404, 429 |
| 5xx | Server error | 500, 502, 503, 504 |

One request, step by step:

```
  curl -i https://example.com/
     |
     v   DNS -> TCP connect -> TLS handshake
  GET / HTTP/1.1
  Host: example.com
     |
     v
  HTTP/1.1 200 OK            <-- status line (the code http_ok tests)
  Content-Type: text/html    <-- headers
  <blank line>
  <html>...                  <-- body
```

## Worked examples

Headers only:

```bash
curl -sI https://example.com
```

Sample output:

```
HTTP/2 200
content-type: text/html; charset=UTF-8
cache-control: max-age=604800
```

Extract just the status code, the pattern used in health checks:

```bash
curl -s -o /dev/null -w '%{http_code}\n' https://example.com
curl -s -o /dev/null -w '%{http_code}\n' https://example.com/missing
```

Sample output:

```
200
404
```

Follow a redirect and show the final URL:

```bash
curl -sL -o /dev/null -w '%{http_code} %{url_effective}\n' http://example.com
```

Sample output:

```
200 https://example.com/
```

Send JSON to an API and fail on errors:

```bash
curl -fsS -X POST https://httpbin.org/post \
  -H 'Content-Type: application/json' \
  -d '{"name":"ada"}' | head -4
```

Sample output:

```
{
  "args": {},
  "data": "{\"name\":\"ada\"}",
```

A health-check function in the spirit of the exercise:

```bash
http_ok() { [ "$1" = "200" ] && echo yes || echo no; }
code=$(curl -s -o /dev/null -w '%{http_code}' https://example.com)
http_ok "$code"
```

Sample output:

```
yes
```

Timing breakdown:

```bash
curl -s -o /dev/null -w 'dns=%{time_namelookup} connect=%{time_connect} total=%{time_total}\n' https://example.com
```

Sample output:

```
dns=0.012 connect=0.034 total=0.190
```

## Mini-lab

1. Run `curl -sI https://example.com` and name the status line, a header,
   and the blank line that ends headers.
2. Fetch a 404 with `-w '%{http_code}'` and note the difference from the
   exit status of curl (still 0).
3. Repeat with `-f` and print `$?`; it should be 22.
4. Use `curl -sIL http://github.com` and count the redirect hops.
5. Save a page: `curl -s -o page.html https://example.com` and check
   `wc -c page.html`.
6. POST data to `https://httpbin.org/post` and read the echoed JSON.
7. Add `--max-time 2` against an unroutable address such as `10.255.255.1`
   and observe exit 28 (timeout).
8. Write a loop that checks three URLs and prints the code for each.

## Decision guide / failure modes

| Symptom | Cause | Next step |
|---------|-------|-----------|
| `Could not resolve host` (6) | DNS problem | `dig`, check resolver |
| `Connection refused` (7) | Nothing listening | `ss -tlpn` on server |
| Timeout (28) | Firewall or slow server | `--max-time`, trace path |
| 301/302 with empty body | Redirect not followed | Add `-L` |
| 401/403 | Auth or permission | Check token and headers |
| 502/503/504 | Proxy cannot reach backend | Check upstream service |
| TLS error (60) | Bad or expired certificate | `openssl s_client`, fix cert |

Curl exits 0 for any HTTP response unless you pass `-f`. For automation use
`-fsS` plus `--max-time`, and test `%{http_code}` when you need to
distinguish 200 from other 2xx codes. Never use `-k` as a permanent fix.
""",
    "exercise_guide": """Implement http_ok in exercise.sh. It receives an HTTP status code as its first argument. When the code is exactly 200 it must print yes, and for anything else (404, 500, 301, an empty string, or no argument) it must print no. Compare it as a string with quotes around the variable so an empty argument does not cause a syntax error. The function does not need to run curl; the test supplies the codes. After ./test.sh passes, combine it by hand with curl -s -o /dev/null -w '%{http_code}' against a real URL.""",
    "exercise_examples": """http_ok 200    -> yes
http_ok 404    -> no
http_ok 500    -> no
http_ok 301    -> no
http_ok ""     -> no
http_ok        -> no

One word per call followed by a newline, and nothing else on stdout.

Combined use:
code=$(curl -s -o /dev/null -w '%{http_code}' https://example.com)
http_ok "$code" -> yes
Only the exact string 200 counts: 201, 204 and 301 are not accepted by this helper, and curl exit status 0 does not mean HTTP success.""",
  },
  20: {
    "body": r"""
## Why this matters

SSH is how you reach nearly every Linux server. Passwords work, but keys are
stronger, scriptable, and can be revoked per device. A key pair also makes
Git hosting, deployment tools, and automation possible without typing
secrets. The catch is that OpenSSH is strict about file permissions: if your
private key is readable by others it refuses to use it, with a loud warning.
That is why `ssh_key_perms` returns 600.

This lesson covers generating keys, installing the public key, the client
config file for short host aliases, and the permission rules that cause most
"why does SSH ignore my key" tickets.

## Core concepts

| File | Purpose | Required mode |
|------|---------|---------------|
| `~/.ssh/` | Directory for SSH data | `700` |
| `~/.ssh/id_ed25519` | Private key (keep secret) | `600` |
| `~/.ssh/id_ed25519.pub` | Public key (shareable) | `644` |
| `~/.ssh/authorized_keys` | Public keys allowed to log in | `600` or `644` |
| `~/.ssh/config` | Client aliases and options | `600` |
| `~/.ssh/known_hosts` | Fingerprints of servers you trust | `644` |

Octal modes: 600 means owner read and write, nobody else anything.

Key based login:

```
  client                                  server
  ------                                  ------
  id_ed25519      (private, 600)          ~/.ssh/authorized_keys
  id_ed25519.pub  (public)  --ssh-copy-id--> contains the public key
        |                                        |
        |  1. connect, offer public key          |
        |--------------------------------------->|
        |  2. server sends challenge             |
        |<---------------------------------------|
        |  3. client signs with private key      |
        |--------------------------------------->|
        |  4. server verifies with public key -> login
```

## Worked examples

Generate a modern key pair:

```bash
ssh-keygen -t ed25519 -C "ada@laptop" -f ~/.ssh/id_ed25519
```

Sample output:

```
Generating public/private ed25519 key pair.
Enter passphrase (empty for no passphrase):
Your identification has been saved in /home/ada/.ssh/id_ed25519
Your public key has been saved in /home/ada/.ssh/id_ed25519.pub
SHA256:Hq3...x0 ada@laptop
```

Check and fix permissions:

```bash
ls -l ~/.ssh
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ed25519 ~/.ssh/config
stat -c '%a %n' ~/.ssh/id_ed25519
```

Sample output:

```
-rw------- 1 ada ada 411 Oct 21 10:00 id_ed25519
-rw-r--r-- 1 ada ada  96 Oct 21 10:00 id_ed25519.pub
600 /home/ada/.ssh/id_ed25519
```

Install the public key on a server and log in:

```bash
ssh-copy-id -i ~/.ssh/id_ed25519.pub ada@203.0.113.10
ssh ada@203.0.113.10 'hostname; whoami'
```

Sample output:

```
web01
ada
```

Client config with an alias:

```bash
cat >> ~/.ssh/config <<'EOF'
Host web
  HostName 203.0.113.10
  User ada
  IdentityFile ~/.ssh/id_ed25519
  Port 22
EOF
ssh web hostname
```

Sample output:

```
web01
```

What happens with loose permissions:

```bash
chmod 644 ~/.ssh/id_ed25519
ssh web
```

Sample output:

```
@         WARNING: UNPROTECTED PRIVATE KEY FILE!          @
Permissions 0644 for '/home/ada/.ssh/id_ed25519' are too open.
This private key will be ignored.
```

Helper from the exercise: `ssh_key_perms() { echo 600; }`

## Mini-lab

1. Create a lab key: `ssh-keygen -t ed25519 -f ~/.ssh/lab_key -N ""`.
2. Run `stat -c '%a %n' ~/.ssh/lab_key*` and confirm 600 and 644.
3. Break it with `chmod 644 ~/.ssh/lab_key`, then try
   `ssh -i ~/.ssh/lab_key localhost` and read the warning. Fix it.
4. Add a `Host lab` block to `~/.ssh/config` for localhost or a VM.
5. Run `ssh -v lab` and find the line where your key is offered.
6. Use `ssh-add -l` to see if an agent holds keys; add one with `ssh-add`.
7. View a server fingerprint with `ssh-keyscan localhost` and compare to
   `~/.ssh/known_hosts` entries.
8. Add a passphrase to a key with `ssh-keygen -p -f ~/.ssh/lab_key`.

## Decision guide / failure modes

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `Permission denied (publickey)` | Key not in `authorized_keys` | `ssh-copy-id`, check `-v` output |
| `UNPROTECTED PRIVATE KEY FILE` | Mode wider than 600 | `chmod 600 key` |
| Server still asks password | Home or `.ssh` mode too open on server | `chmod 700 ~/.ssh`, home not group-writable |
| `REMOTE HOST IDENTIFICATION HAS CHANGED` | Rebuilt server or MITM | Verify, then `ssh-keygen -R host` |
| Wrong key used | Many keys offered | `IdentitiesOnly yes` in config |
| Connection timeout | Firewall or wrong port | `nc -vz host 22` |

Use ed25519 unless a legacy system needs RSA 4096. Protect private keys with
a passphrase and an agent, never copy them between machines casually, and
never share anything except the `.pub` file.
""",
    "exercise_guide": """Implement ssh_key_perms in exercise.sh. It takes no arguments and must print the octal permission mode that OpenSSH expects for a private key file, with nothing else on the line. The test checks the exact string. Afterwards, create a throwaway key with ssh-keygen, confirm its mode with stat -c '%a %n', deliberately loosen it with chmod 644, and read the warning ssh prints. Restore the correct mode and note why a group-readable private key is a security problem.""",
    "exercise_examples": """ssh_key_perms    -> 600

Check on a real key:
stat -c '%a %n' ~/.ssh/id_ed25519    -> 600 /home/you/.ssh/id_ed25519
600 = owner read+write, no access for group or others.
The public key (.pub) is usually 644, and the ~/.ssh directory is 700.

Broken example: chmod 644 ~/.ssh/id_ed25519 makes ssh print 'UNPROTECTED PRIVATE KEY FILE' and ignore the key. Repair with chmod 600 ~/.ssh/id_ed25519. Directory ~/.ssh should be 700. Print the digits only, never the word chmod.""",
  },
  21: {
    "body": r"""
## Why this matters

On most modern distributions, systemd starts and supervises your services.
If you deploy a web app, a database, or an agent, you will write a unit
file, enable it, start it, and read its logs with `journalctl`. The command
`systemctl enable --now` is the everyday shortcut that does two things at
once: it makes the service start at boot and starts it right now. Mixing up
`enable` and `start` is a classic cause of "it worked until the reboot".

## Core concepts

| Command | Effect |
|---------|--------|
| `systemctl start X` | Start now; does not persist across reboot |
| `systemctl stop X` | Stop now |
| `systemctl enable X` | Create boot symlink; does not start now |
| `systemctl enable --now X` | Enable and start: start-and-boot |
| `systemctl disable X` | Remove boot link |
| `systemctl restart X` | Stop then start |
| `systemctl reload X` | Re-read config without full restart |
| `systemctl status X` | State, recent logs, main PID |
| `systemctl daemon-reload` | Re-read unit files after editing |
| `journalctl -u X` | Logs for the unit |

Unit file locations:

| Path | Use |
|------|-----|
| `/usr/lib/systemd/system/` | Packages ship units here |
| `/etc/systemd/system/` | Your units and overrides |
| `/etc/systemd/system/X.service.d/` | Drop-in overrides |

Two independent switches:

```
                 running now?        starts at boot?
                 ------------        ---------------
  start / stop       yes/no              unchanged
  enable / disable   unchanged           yes/no
  enable --now       yes                 yes     (= "start-and-boot")

  unit file --> [Unit] After=, Wants=
            --> [Service] ExecStart=, Restart=, User=
            --> [Install] WantedBy=multi-user.target
                                  ^ enable links the unit into this target
```

## Worked examples

A minimal service unit:

```bash
sudo tee /etc/systemd/system/hello.service >/dev/null <<'EOF'
[Unit]
Description=Hello demo service
After=network.target

[Service]
ExecStart=/usr/bin/python3 -m http.server 8099
Restart=on-failure
User=nobody

[Install]
WantedBy=multi-user.target
EOF
sudo systemctl daemon-reload
```

Enable and start in one step:

```bash
sudo systemctl enable --now hello.service
systemctl is-enabled hello.service
systemctl is-active hello.service
```

Sample output:

```
Created symlink /etc/systemd/system/multi-user.target.wants/hello.service
enabled
active
```

Status view:

```bash
systemctl status hello.service --no-pager
```

Sample output:

```
* hello.service - Hello demo service
     Loaded: loaded (/etc/systemd/system/hello.service; enabled; preset: enabled)
     Active: active (running) since Wed 2026-10-21 10:30:00 UTC; 5s ago
   Main PID: 3120 (python3)
```

Logs:

```bash
journalctl -u hello.service -n 3 --no-pager
journalctl -u hello.service -f
journalctl -b -p err --no-pager | tail -3
journalctl --since "10 min ago" -u hello.service
```

Sample output:

```
Oct 21 10:30:00 web01 systemd[1]: Started hello.service - Hello demo service.
```

Drop-in override and clean-up:

```bash
sudo systemctl edit hello.service
sudo systemctl disable --now hello.service
```

Helper from the exercise: `enable_now_meaning() { echo start-and-boot; }`

## Mini-lab

1. Create `hello.service` as shown and run `daemon-reload`.
2. `systemctl start hello` and `systemctl is-enabled hello` (disabled).
3. Reboot-test thinking: explain why it will not return after reboot.
4. `systemctl enable hello`, then `systemctl is-enabled hello`.
5. Stop it and run `systemctl enable --now hello` to see both effects.
6. Break it: change `ExecStart` to a wrong path, `daemon-reload`, restart,
   then read `systemctl status` and `journalctl -u hello -n 20`.
7. Kill the process with `sudo kill -9 MAINPID` and watch `Restart=` revive it.
8. Remove it with `disable --now`, delete the file, `daemon-reload`.

## Decision guide / failure modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| Service gone after reboot | Started but not enabled | `enable` |
| Edits have no effect | Forgot reload | `systemctl daemon-reload` |
| `status=203/EXEC` | Bad `ExecStart` path or not executable | Fix path, `chmod +x` |
| `status=200/CHDIR` or 217/USER | Missing directory or user | Create it |
| Restart loop | App crashes | `journalctl -u X`, add `RestartSec` |
| Starts too early | Needs network or DB | `After=` and `Wants=` |

Use `restart` for code changes, `reload` only if the app supports it, and
`enable --now` for first installs. Do not edit packaged units in `/usr/lib`;
use `systemctl edit` drop-ins.
""",
    "exercise_guide": """Implement enable_now_meaning in exercise.sh. It takes no arguments and prints a short token that states what systemctl enable --now does. The token is two ideas joined with hyphens: it starts the service immediately and it also configures it to start at boot. The test compares the output exactly, so print only that token in lowercase. Test your understanding on a VM with a harmless unit by checking systemctl is-active and systemctl is-enabled before and after.""",
    "exercise_examples": """enable_now_meaning    -> start-and-boot

Meaning on a real host:
systemctl enable --now hello  -> is-active: active, is-enabled: enabled
systemctl start hello         -> is-active: active, is-enabled: disabled (not at boot)
systemctl enable hello        -> is-active: inactive, is-enabled: enabled

Timeline view: before enable --now, systemctl is-enabled prints disabled and is-active prints inactive. After it, both are positive, and the service also survives reboot. Print the token in lowercase with hyphens and no spaces.""",
  },
  22: {
    "body": r"""
## Why this matters

When a server will not boot, hangs at a prompt, or comes up without
networking, you need to know what happens between power-on and a login
prompt. You also need to know how to reach a rescue shell when things go
wrong. On modern Linux the answer centres on one program: the first
userspace process, PID 1, which is `systemd`. It reads targets, pulls in
units, and brings the machine to a goal state.

Understanding targets lets you boot to a text console, drop to rescue mode
to fix a broken `/etc/fstab`, and diagnose slow starts with
`systemd-analyze`.

## Core concepts

| Stage | Component | Job |
|-------|-----------|-----|
| 1 | Firmware (UEFI/BIOS) | Hardware init, find boot device |
| 2 | Bootloader (GRUB) | Load kernel and initramfs |
| 3 | Kernel | Init hardware, mount temporary root |
| 4 | initramfs | Find and mount the real root filesystem |
| 5 | PID 1 (`systemd`) | Start units toward the default target |
| 6 | Login | getty, sshd, display manager |

Targets (groups of units, a replacement for old runlevels):

| Target | Old runlevel | Meaning |
|--------|--------------|---------|
| `poweroff.target` | 0 | Shut down |
| `rescue.target` | 1 | Single user, base system |
| `multi-user.target` | 3 | Full system, text mode, networking |
| `graphical.target` | 5 | Multi-user plus GUI |
| `reboot.target` | 6 | Reboot |
| `emergency.target` | - | Minimal shell, root read-only |

Boot chain:

```
  power on
     |
  [UEFI firmware] -> [GRUB] -> [kernel + initramfs]
                                      |
                              mounts real root /
                                      |
                              exec /sbin/init  -> PID 1 = systemd
                                      |
                       default.target (graphical or multi-user)
                           |            |             |
                     sysinit.target  network   sshd, cron, app...
                                      |
                                  login prompt
```

## Worked examples

Confirm PID 1:

```bash
ps -p 1 -o pid,comm,args
cat /proc/1/comm
```

Sample output:

```
    PID COMMAND         COMMAND
      1 systemd         /sbin/init splash
systemd
```

Default target and what is running:

```bash
systemctl get-default
systemctl list-units --type=target --no-pager | head -6
```

Sample output:

```
multi-user.target
UNIT                   LOAD   ACTIVE SUB    DESCRIPTION
basic.target           loaded active active Basic System
multi-user.target      loaded active active Multi-User System
network.target         loaded active active Network
```

Change the default target and switch live:

```bash
sudo systemctl set-default multi-user.target
sudo systemctl isolate rescue.target
```

Boot timing:

```bash
systemd-analyze
systemd-analyze blame | head -3
systemd-analyze critical-chain | head -5
```

Sample output:

```
Startup finished in 2.1s (kernel) + 6.4s (userspace) = 8.5s
 3.201s cloud-init.service
 1.044s apt-daily.service
 0.890s networkd-wait-online.service
```

Boot logs:

```bash
journalctl -b --no-pager | head -3
journalctl -b -1 -p err --no-pager | tail -3
dmesg | head -3
cat /proc/cmdline
```

Sample output:

```
BOOT_IMAGE=/vmlinuz-6.8.0 root=UUID=1c2d... ro quiet splash
```

One-time boot into rescue: at GRUB press `e`, append
`systemd.unit=rescue.target` to the `linux` line, then `Ctrl+X`.

Helper from the exercise: `pid1_name() { echo systemd; }`

## Mini-lab

1. Run `ps -p 1 -o comm=` and confirm `systemd`.
2. Show the default target with `systemctl get-default`.
3. List active targets and identify `network.target` and `basic.target`.
4. Run `systemd-analyze` and `systemd-analyze blame`; name the slowest unit.
5. Read `cat /proc/cmdline` and find the `root=` argument.
6. Compare `journalctl -b` with `journalctl -b -1` (previous boot).
7. In a VM only, run `sudo systemctl isolate rescue.target`, then return
   with `sudo systemctl isolate multi-user.target` or reboot.
8. Draw the boot chain from memory and compare with this lesson.

## Decision guide / failure modes

| Symptom | Likely cause | Action |
|---------|--------------|--------|
| Drops to emergency shell | Bad `/etc/fstab` entry or fs error | Fix fstab, `fsck`, reboot |
| Hang "A start job is running" | Waiting for a device or network | `systemd-analyze blame`, use `nofail` |
| Boots to text, want GUI | Default is `multi-user` | `set-default graphical.target` |
| Kernel panic, cannot mount root | Wrong `root=` or missing initramfs | Choose older kernel in GRUB |
| Lost root password | Need rescue | Boot with `rd.break` or rescue target |
| Slow boot | One slow unit | `systemd-analyze blame` |

Reading order for any boot problem: firmware, GRUB menu, kernel messages
(`dmesg`), then `journalctl -b`. Always keep an older working kernel
installed and test a changed fstab with `mount -a` before rebooting.
""",
    "exercise_guide": """Implement pid1_name in exercise.sh so it prints the name of the init system that runs as process ID 1 on a modern mainstream Linux distribution. No arguments, no extra text, lowercase. The test compares the exact output. To make it real, run ps -p 1 -o comm= on a Linux VM or container, and note that in a minimal Docker container PID 1 can be your own command instead; write one sentence on why that differs.""",
    "exercise_examples": """pid1_name    -> systemd

On a real host:
ps -p 1 -o comm=    -> systemd
cat /proc/1/comm    -> systemd
In a plain Docker container PID 1 is whatever the container started (often sh or your app), not systemd.

Check default target: systemctl get-default -> multi-user.target. Check boot time: systemd-analyze -> Startup finished in ... Older init systems were SysV init and Upstart, so the name is not init on current Debian, Ubuntu, Fedora or RHEL. Print lowercase letters only.""",
  },
  23: {
    "body": r"""
## Why this matters

Backups, log rotation, certificate renewal, report generation, and cleanup
jobs all need to run on a schedule. Linux offers two mainstream tools:
classic `cron`, which is simple and everywhere, and `systemd` timers, which
add logging, dependencies, and catch-up after downtime. Many "the job never
ran" incidents come from five small things: cron's minimal environment, the
wrong time zone, a missing newline, a relative path, or output that went
nowhere.

## Core concepts

A crontab line has five time fields then a command:

```
  +---------- minute        (0-59)
  | +-------- hour          (0-23)
  | | +------ day of month  (1-31)
  | | | +---- month         (1-12)
  | | | | +-- day of week   (0-7, 0 and 7 are Sunday)
  | | | | |
  0 3 * * *  /usr/local/bin/backup.sh
```

So `0 3 * * *` means every day at 03:00.

| Expression | Meaning |
|------------|---------|
| `*/5 * * * *` | Every 5 minutes |
| `0 * * * *` | Every hour on the hour |
| `0 3 * * *` | Daily at 03:00 |
| `30 2 * * 1` | Mondays at 02:30 |
| `0 0 1 * *` | First of each month at midnight |
| `@reboot` | Once at boot |
| `0 9-17 * * 1-5` | On the hour, 09-17, Monday to Friday |

Cron versus systemd timers:

| Aspect | cron | systemd timer |
|--------|------|---------------|
| Setup | One line in crontab | Two units: `.service` + `.timer` |
| Logs | Mail or your redirect | `journalctl -u name` |
| Missed runs | Lost | `Persistent=true` catches up |
| Environment | Minimal | Defined by the unit |
| Schedule syntax | Five fields | `OnCalendar=*-*-* 03:00:00` |

Where jobs live:

```
  crontab -e            -> per-user  (/var/spool/cron/...)
  /etc/crontab          -> system, has an extra USER column
  /etc/cron.d/*         -> drop-in system files, USER column
  /etc/cron.daily/ ...  -> scripts run by run-parts
  systemctl list-timers -> systemd timers
```

## Worked examples

Edit and list your crontab:

```bash
crontab -e
crontab -l
```

Sample output:

```
# m h dom mon dow command
0 3 * * * /usr/local/bin/backup.sh >>/var/log/backup.log 2>&1
*/15 * * * * /usr/bin/curl -fsS https://example.com/health >/dev/null
```

Set environment explicitly, since cron's PATH is tiny:

```bash
SHELL=/bin/bash
PATH=/usr/local/bin:/usr/bin:/bin
MAILTO=ops@example.com
0 3 * * * cd /srv/app && ./cleanup.sh
```

Prevent overlapping runs with `flock`:

```bash
*/5 * * * * flock -n /tmp/job.lock /usr/local/bin/job.sh
```

A systemd timer pair:

```bash
sudo tee /etc/systemd/system/backup.service >/dev/null <<'EOF'
[Unit]
Description=Nightly backup
[Service]
Type=oneshot
ExecStart=/usr/local/bin/backup.sh
EOF
sudo tee /etc/systemd/system/backup.timer >/dev/null <<'EOF'
[Unit]
Description=Run backup daily at 03:00
[Timer]
OnCalendar=*-*-* 03:00:00
Persistent=true
[Install]
WantedBy=timers.target
EOF
sudo systemctl daemon-reload
sudo systemctl enable --now backup.timer
systemctl list-timers --no-pager | head -3
```

Sample output:

```
NEXT                        LEFT     LAST PASSED UNIT         ACTIVATES
Thu 2026-10-22 03:00:00 UTC 16h left n/a  n/a    backup.timer backup.service
```

Validate a calendar expression:

```bash
systemd-analyze calendar "*-*-* 03:00:00"
```

Sample output:

```
Normalized form: *-*-* 03:00:00
    Next elapse: Thu 2026-10-22 03:00:00 UTC
```

Helper from the exercise: `cron_daily_3am() { echo "0 3 * * *"; }`

## Mini-lab

1. Run `crontab -l` to see whether you have jobs.
2. Add `* * * * * date >> /tmp/cron-test.log` and wait two minutes.
3. Check `tail /tmp/cron-test.log`, then remove the line.
4. Write the cron expression for 02:30 every Monday and weekdays at 9.
5. Add `PATH=` and `SHELL=` at the top of your crontab and explain why.
6. Create the `backup.service` and `backup.timer` pair; run
   `systemctl start backup.service` manually and read its log with
   `journalctl -u backup.service`.
7. Run `systemd-analyze calendar` with three different expressions.
8. Use `flock -n` to make a job skip when the previous run is still active.

## Decision guide / failure modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| Works by hand, not in cron | Minimal env, relative paths | Absolute paths, set `PATH` |
| Nothing happened, no log | Output discarded | Redirect `>>file 2>&1` |
| Job missing after edit | No trailing newline or syntax error | Use `crontab -e`, check syslog |
| `%` breaks command | `%` means newline in crontab | Escape as `\%` |
| Ran at wrong hour | Time zone or DST | `timedatectl`, use UTC |
| Overlapping runs | Job slower than interval | `flock` |
| Missed while off | cron does not catch up | systemd `Persistent=true` |

Choose cron for simple user-level jobs and quick one-liners; choose timers
for services that need logs, dependencies, and catch-up. Always test the
command as the same user with `env -i` to mimic cron's bare environment.
""",
    "exercise_guide": """Implement cron_daily_3am in exercise.sh. It prints the five-field crontab schedule expression for running a job once every day at 03:00 in the morning, and nothing else. The five fields are minute, hour, day of month, month and day of week. Because the value contains asterisks, quote the string so the shell does not expand them into filenames. After the test passes, check your answer with systemd-analyze calendar using the equivalent OnCalendar form, and write the expression for 02:30 every Monday as a second drill.""",
    "exercise_examples": """cron_daily_3am    -> 0 3 * * *

Field by field: minute 0, hour 3, any day of month, any month, any weekday.
Related: 30 2 * * 1 = Mondays 02:30; */15 * * * * = every 15 minutes.
Without quotes, echo 0 3 * * * would expand the stars to file names.

Test with the helper: [ "$(cron_daily_3am)" = '0 3 * * *' ] && echo pass. A full crontab line adds the command: 0 3 * * * /usr/local/bin/backup.sh. The systemd equivalent is OnCalendar=*-*-* 03:00:00. Print only the five fields separated by single spaces.""",
  },
  24: {
    "body": r"""
## Why this matters

On Debian and Ubuntu, software arrives as `.deb` packages managed by two
layers: `dpkg`, which installs single files and tracks what is installed,
and `apt`, which fetches from repositories and resolves dependencies.
Servers need reproducible installs, security updates, and the ability to
answer "which package owns this file" and "what did that upgrade change".

A key point that trips beginners: `apt update` does not upgrade anything.
It only refreshes the local package indexes (the list of available
versions). `apt upgrade` is what installs newer versions. That is why the
exercise answer is `refresh-indexes`.

## Core concepts

| Command | Effect |
|---------|--------|
| `apt update` | Refresh package indexes from repositories |
| `apt upgrade` | Install newer versions of installed packages |
| `apt full-upgrade` | Upgrade, allowing removals to resolve deps |
| `apt install pkg` | Install with dependencies |
| `apt remove pkg` | Remove, keep config |
| `apt purge pkg` | Remove including config |
| `apt autoremove` | Remove no-longer-needed dependencies |
| `apt search / show` | Find and describe packages |
| `apt-cache policy pkg` | Installed vs candidate version |
| `dpkg -l` / `dpkg -L pkg` | List packages / files of a package |
| `dpkg -S /path` | Which package owns a file |
| `dpkg -i file.deb` | Install a local file (no dependency fetch) |

Where things live:

| Path | Content |
|------|---------|
| `/etc/apt/sources.list`, `/etc/apt/sources.list.d/` | Repository definitions |
| `/var/lib/apt/lists/` | Downloaded indexes |
| `/var/cache/apt/archives/` | Downloaded `.deb` files |
| `/var/lib/dpkg/status` | Installed package database |

Layers and data flow:

```
  repositories (archive.ubuntu.com, security.ubuntu.com)
        |
        |  apt update      (downloads Packages indexes only)
        v
  /var/lib/apt/lists/      <- local catalog of what exists
        |
        |  apt install / upgrade   (resolve deps, download .deb)
        v
  /var/cache/apt/archives/*.deb
        |
        |  dpkg (unpack, configure)
        v
  /var/lib/dpkg/status  +  files on disk
```

## Worked examples

Refresh and see what could be upgraded:

```bash
sudo apt update
apt list --upgradable 2>/dev/null | head -4
```

Sample output:

```
Hit:1 http://archive.ubuntu.com/ubuntu noble InRelease
Get:2 http://security.ubuntu.com/ubuntu noble-security InRelease [126 kB]
Reading package lists... Done
8 packages can be upgraded. Run 'apt list --upgradable' to see them.
```

Install and inspect a package:

```bash
sudo apt install -y tree
apt-cache policy tree
dpkg -L tree | head -4
dpkg -S "$(command -v tree)"
```

Sample output:

```
tree:
  Installed: 2.1.1-2ubuntu3
  Candidate: 2.1.1-2ubuntu3
/usr/bin/tree
tree: /usr/bin/tree
```

Upgrade, then clean up:

```bash
sudo apt upgrade -y
sudo apt autoremove -y
sudo apt clean
```

Remove versus purge, and hold a version:

```bash
sudo apt remove nginx
sudo apt purge nginx
sudo apt-mark hold linux-image-generic
apt-mark showhold
```

Add a third-party repo carefully (key then source), then verify:

```bash
curl -fsSL https://example.com/key.gpg | sudo gpg --dearmor -o /etc/apt/keyrings/example.gpg
echo "deb [signed-by=/etc/apt/keyrings/example.gpg] https://example.com/apt stable main" | sudo tee /etc/apt/sources.list.d/example.list
sudo apt update
```

Helper from the exercise: `apt_update_does() { echo refresh-indexes; }`

## Mini-lab

1. Run `sudo apt update` and read the Hit, Get, and Ign lines.
2. Run `apt list --upgradable`; note that nothing was installed yet.
3. Install `tree` and `jq`; use `which` and `dpkg -L jq` to see files.
4. Find the owner of `/bin/ls` with `dpkg -S /bin/ls`.
5. Compare `apt-cache policy` for a package before and after an upgrade.
6. Remove `jq` with `remove`, check config remains, then use `purge`.
7. Use `apt show tree` and read the Depends line.
8. Run `apt-mark hold tree`, try an upgrade, then `unhold`.

## Decision guide / failure modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Unable to locate package` | Stale indexes or wrong name | `apt update`, `apt search` |
| `Could not get lock` | Another apt or unattended-upgrades running | Wait; do not delete lock files blindly |
| `Hash Sum mismatch` | Mirror sync or proxy | Retry, `apt clean`, change mirror |
| `NO_PUBKEY` / signature error | Missing repo key | Install the key in `/etc/apt/keyrings` |
| Broken dependencies | Half-installed package | `sudo apt -f install`, `dpkg --configure -a` |
| Wrong version installed | Another repo has higher priority | `apt-cache policy`, pinning |

Habits: run `apt update` before `apt install`, prefer `apt` over raw
`dpkg -i`, keep unattended security updates on, and read the proposed
removals before pressing yes.
""",
    "exercise_guide": """Implement apt_update_does in exercise.sh. It takes no arguments and prints one hyphenated token describing what apt update does: it refreshes the package indexes (the list of available packages and versions) but installs nothing. The test compares the output exactly, so print only that token in lowercase. As a follow-up on a Debian or Ubuntu system, run sudo apt update and then apt list --upgradable to confirm that no package changed until you run apt upgrade.""",
    "exercise_examples": """apt_update_does    -> refresh-indexes

On a real system:
sudo apt update      -> downloads indexes, installs nothing
apt list --upgradable -> shows what could be upgraded
sudo apt upgrade     -> actually installs newer versions

Contrast with other verbs: apt install pkg fetches and installs one package, apt upgrade installs newer versions, apt remove deletes software. The helper prints one hyphenated word pair with no spaces: refresh then indexes, joined by a dash.""",
  },
  25: {
    "body": r"""
## Why this matters

Linux is not one package system. Debian and Ubuntu use `apt`, Red Hat,
Fedora, Rocky, and Alma use `dnf`, and Alpine (the base of many small
containers) uses `apk`. If you move between laptops, cloud images, and
containers, you must translate quickly: "the install command here is X,
the package name there is Y". Tutorials usually show only one family.

This lesson is a translation table plus the extra concepts: repositories,
GPG keys, groups, and which package provides a given file.

## Core concepts

| Task | Debian / Ubuntu | RHEL / Fedora | Alpine |
|------|-----------------|---------------|--------|
| Refresh metadata | `apt update` | `dnf makecache` (auto) | `apk update` |
| Install | `apt install X` | `dnf install X` | `apk add X` |
| Remove | `apt remove X` | `dnf remove X` | `apk del X` |
| Upgrade all | `apt upgrade` | `dnf upgrade` | `apk upgrade` |
| Search | `apt search X` | `dnf search X` | `apk search X` |
| Info | `apt show X` | `dnf info X` | `apk info X` |
| List installed | `dpkg -l` | `rpm -qa` | `apk info` |
| File owner | `dpkg -S /path` | `rpm -qf /path` | `apk info -W /path` |
| Which package has file | `apt-file search` | `dnf provides '*/file'` | `apk info -W` / pkgs site |
| Local package file | `dpkg -i x.deb` | `rpm -i x.rpm` | `apk add ./x.apk` |
| Repo config | `/etc/apt/sources.list.d/` | `/etc/yum.repos.d/` | `/etc/apk/repositories` |
| C library | glibc | glibc | musl |
| Init | systemd | systemd | OpenRC |

Same job, three dialects:

```
  "install curl"
      |
      +-- debian/ubuntu --> apt install curl
      |
      +-- rhel/fedora   --> dnf install curl
      |
      +-- alpine        --> apk add curl

  Under the hood:  apt -> dpkg (.deb)
                   dnf -> rpm  (.rpm)
                   apk -> .apk archives
```

Detect the family from `/etc/os-release`:

| Field | Example |
|-------|---------|
| `ID` | `ubuntu`, `rocky`, `alpine` |
| `ID_LIKE` | `debian`, `rhel fedora` |

## Worked examples

Detect the distribution:

```bash
. /etc/os-release
echo "$ID / ${ID_LIKE:-none}"
```

Sample output:

```
rocky / rhel centos fedora
```

Install and query on Fedora/RHEL:

```bash
sudo dnf install -y tree
dnf info tree | head -4
rpm -qf /usr/bin/tree
dnf provides '*/bin/dig'
```

Sample output:

```
tree-2.1.0-1.el9.x86_64
bind-utils-9.16.23-1.el9.x86_64 : Utilities for querying DNS name servers
```

Install on Alpine, such as in a container:

```bash
docker run --rm -it alpine:3.20 sh -c 'apk update && apk add curl && curl --version | head -1'
```

Sample output:

```
fetch https://dl-cdn.alpinelinux.org/alpine/v3.20/main/x86_64/APKINDEX.tar.gz
(1/9) Installing ca-certificates (20240705-r0)
curl 8.9.1 (x86_64-alpine-linux-musl) libcurl/8.9.1
```

A portable installer function:

```bash
install_pkg() {
  . /etc/os-release
  case "${ID_LIKE:-$ID}" in
    *debian*|ubuntu|debian) sudo apt-get install -y "$@" ;;
    *rhel*|*fedora*)        sudo dnf install -y "$@" ;;
    alpine)                 apk add --no-cache "$@" ;;
    *) echo "unsupported: $ID" >&2; return 1 ;;
  esac
}
```

The mapping from the exercise:

```bash
map_install_cmd() {
  case "$1" in
    debian) echo apt ;;
    rhel)   echo dnf ;;
    alpine) echo apk ;;
    *)      return 1 ;;
  esac
}
map_install_cmd rhel
```

Sample output:

```
dnf
```

## Mini-lab

1. Run `cat /etc/os-release` and note `ID` and `ID_LIKE`.
2. Start containers: `docker run --rm -it ubuntu:24.04 bash`,
   `fedora:40 bash`, and `alpine:3.20 sh`.
3. In each, install `curl` with the native command and record the output.
4. Use the file-owner query for `/bin/sh` in each environment.
5. Search for `htop` in each package manager.
6. Compare package names: `apache2` versus `httpd`, `dnsutils` versus
   `bind-utils`, `build-essential` versus `gcc make`.
7. Write the `map_install_cmd` function and test the three families plus
   an unknown value.
8. In Alpine, note why `bash` is absent by default and `/bin/sh` is busybox.

## Decision guide / failure modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| `apt: command not found` on Fedora | Wrong family | Use `dnf` |
| `dnf: command not found` on older CentOS 7 | Uses `yum` | Use `yum` |
| Package name not found | Names differ per distro | Search or use `provides` |
| `bash: not found` on Alpine | Only `ash` installed | `apk add bash` |
| Binary fails with "not found" on Alpine | glibc binary on musl | Use a native build or Debian image |
| Repository key error | Missing or expired GPG key | Import vendor key |

Think in tasks, not commands: refresh, install, remove, search, file
owner. Keep a cheat sheet like the table above, and in scripts branch on
`/etc/os-release` instead of guessing.
""",
    "exercise_guide": """Implement map_install_cmd in exercise.sh. It takes one argument naming a distribution family and prints the name of the native package manager command: debian maps to apt, rhel maps to dnf, and alpine maps to apk. Use a case statement and quote the argument. For an unknown family, print nothing and return 1. Output only the command name, with no other text. Run ./test.sh, then validate the table on real systems or containers by running the actual install command in each family.""",
    "exercise_examples": """map_install_cmd debian    -> apt
map_install_cmd rhel      -> dnf
map_install_cmd alpine    -> apk
map_install_cmd arch      -> prints nothing, status 1

Only the command word is printed, followed by a newline.

Supporting facts: apt belongs to Debian and Ubuntu, dnf to Red Hat, Fedora, Rocky and Alma, apk to Alpine. Unknown input such as arch or empty must give status 1 and no output. Check with: map_install_cmd arch; echo "rc=$?" -> rc=1.""",
  },
  26: {
    "body": r"""
## Why this matters

"No space left on device" is one of the most common production failures,
and it has a confusing variant: the disk shows free space but you still
cannot create files. That second case means you ran out of inodes, the
metadata slots that each file consumes. To handle storage you need to read
block devices, partitions, filesystems, mount points, and both kinds of
capacity: bytes and inodes.

## Core concepts

| Term | Meaning |
|------|---------|
| Block device | Raw storage: `/dev/sda`, `/dev/nvme0n1`, `/dev/vda` |
| Partition | A slice of a disk: `/dev/sda1` |
| Filesystem | Structure on the partition: ext4, xfs, btrfs |
| Mount point | Directory where a filesystem appears: `/`, `/data` |
| UUID | Stable filesystem identifier |
| Inode | Metadata record for one file or directory |
| Block usage | Bytes used (`df -h`) |
| Inode usage | Files used (`df -i`) |

Tools:

| Command | Shows |
|---------|-------|
| `lsblk -f` | Devices, filesystem types, UUIDs, mounts |
| `df -h` | Space used per mounted filesystem |
| `df -i` | Inodes used per mounted filesystem |
| `du -sh dir` | Space consumed by a directory |
| `findmnt` | Mount tree |
| `blkid` | UUIDs and types |
| `fdisk -l` / `parted` | Partition tables |
| `mkfs.ext4`, `mount`, `umount` | Create, attach, detach |

Layers from disk to path:

```
  physical disk   /dev/vdb
        |
  partition       /dev/vdb1          (fdisk / parted)
        |
  filesystem      ext4, UUID=abcd... (mkfs.ext4)
        |
  mount point     /data              (mount /dev/vdb1 /data)
        |
  files           /data/app/log.txt  (each file = 1 inode + data blocks)

  Full if EITHER bytes run out (df -h) OR inodes run out (df -i)
```

## Worked examples

Overview of devices:

```bash
lsblk -f
```

Sample output:

```
NAME   FSTYPE FSVER LABEL UUID                                 FSAVAIL FSUSE% MOUNTPOINTS
vda
|-vda1 ext4   1.0         1c2d3e4f-0000-4a5b-9c8d-aaaaaaaaaaaa   12.4G    38% /
vdb
`-vdb1 ext4   1.0         9f8e7d6c-1111-4b3a-8d7c-bbbbbbbbbbbb    9.1G     1% /data
```

Space and inodes:

```bash
df -h /
df -i /
```

Sample output:

```
Filesystem      Size  Used Avail Use% Mounted on
/dev/vda1        20G  7.6G   12G  39% /
Filesystem      Inodes  IUsed   IFree IUse% Mounted on
/dev/vda1      1310720 204118 1106602   16% /
```

Find what is using space:

```bash
sudo du -xh / --max-depth=1 2>/dev/null | sort -h | tail -4
sudo find /var -xdev -type f -size +100M -exec ls -lh {} +
```

Sample output:

```
1.2G    /usr
2.4G    /var
7.0G    /
```

Prepare a new disk (destructive, lab VM only):

```bash
sudo parted -s /dev/vdb mklabel gpt mkpart primary ext4 1MiB 100%
sudo mkfs.ext4 /dev/vdb1
sudo mkdir -p /data
sudo mount /dev/vdb1 /data
findmnt /data
```

Sample output:

```
TARGET SOURCE    FSTYPE OPTIONS
/data  /dev/vdb1 ext4   rw,relatime
```

Run out of inodes on purpose in a small loop filesystem:

```bash
truncate -s 20M /tmp/small.img
mkfs.ext4 -N 512 -q /tmp/small.img
sudo mount -o loop /tmp/small.img /mnt
sudo bash -c 'for i in $(seq 1 600); do : > /mnt/f$i || break; done'
df -i /mnt
```

Sample output:

```
touch: cannot touch ... No space left on device
Filesystem     Inodes IUsed IFree IUse% Mounted on
/dev/loop0        512   512     0  100% /mnt
```

Helper from the exercise: `inode_check_flag() { echo "-i"; }` returns the
flag you pass to `df` (bash echo only treats -n, -e, -E as options).

## Mini-lab

1. Run `lsblk -f` and identify the root device and its UUID.
2. Compare `df -h /` and `df -i /`.
3. Use `du -xh /var --max-depth=1 | sort -h` to find the biggest directory.
4. Create a 50M loop image, format it with ext4, and mount it on `/mnt`.
5. Fill it with `fallocate -l 40M /mnt/big`, check `df -h /mnt`.
6. Create many tiny files and watch `df -i /mnt` climb.
7. Unmount with `sudo umount /mnt`; if busy, find the user with
   `lsof +f -- /mnt` or `fuser -vm /mnt`.
8. Delete a large file held open by a process and see that space returns
   only after the process closes it (`lsof +L1`).

## Decision guide / failure modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| `No space left`, `df -h` shows free | Inodes exhausted | `df -i`, delete tiny files, recreate fs with more inodes |
| `df` full but `du` totals smaller | Deleted file still open | `lsof +L1`, restart the process |
| `target is busy` on umount | Process cwd or open file inside | `fuser -vm`, `lsof` |
| Mount disappears after reboot | Not in fstab | Add UUID entry |
| Read-only filesystem | Errors detected | `dmesg`, `fsck` after unmount |
| Wrong disk formatted | Used wrong device name | Always confirm with `lsblk` first |

Before any `mkfs`, `dd`, or `parted`, read `lsblk` twice and confirm the
device by size and UUID. For capacity questions always ask both: bytes
with `df -h`, inodes with `df -i`.
""",
    "exercise_guide": """Implement inode_check_flag in exercise.sh. It takes no arguments and prints the option you pass to df to report inode usage instead of block usage. Print only the flag, including its leading dash. Be careful when testing by hand: echo with a leading dash can be read as an option by some shells, so confirm that your function prints the text exactly (printf '%s\\n' is a safe choice). Afterwards run df -i / and df -h / on a real host and explain in one sentence why the two can disagree.""",
    "exercise_examples": """inode_check_flag    -> -i

Usage: df $(inode_check_flag) /
df -h /   shows bytes used     (blocks)
df -i /   shows inodes used    (number of files)
Both limits matter; either one can cause "No space left on device".

Example sequence on a real host: df -h / shows Use% 39%, df -i / shows IUse% 16%. When IUse% reaches 100% you get No space left on device even though df -h shows plenty free. The function prints just the two characters dash and i.""",
  },
  27: {
    "body": r"""
## Why this matters

Fixed partitions are hard to change: if `/var` fills up, you cannot easily
grow it. LVM (Logical Volume Manager) adds a flexible layer between disks
and filesystems so that you can resize volumes, combine disks, and take
snapshots without downtime. Then `/etc/fstab` makes mounts survive reboot.
A single mistake in fstab can drop the machine into emergency mode, so you
should know every field and why UUIDs are preferred over device names such
as `/dev/sdb1`, which can change from one boot to the next.

## Core concepts

| LVM term | Meaning | Commands |
|----------|---------|----------|
| PV (Physical Volume) | Disk or partition given to LVM | `pvcreate`, `pvs` |
| VG (Volume Group) | Pool made from one or more PVs | `vgcreate`, `vgextend`, `vgs` |
| LV (Logical Volume) | Slice of the pool that holds a filesystem | `lvcreate`, `lvextend`, `lvs` |
| Extent | Allocation unit, usually 4 MiB | - |

The six fields of an fstab line:

| # | Field | Example | Meaning |
|---|-------|---------|---------|
| 1 | Device | `UUID=9f8e7d6c-...` | What to mount (UUID, LABEL, path) |
| 2 | Mount point | `/data` | Where |
| 3 | Type | `ext4` | Filesystem type |
| 4 | Options | `defaults,nofail` | Mount options |
| 5 | Dump | `0` | Legacy backup flag |
| 6 | Pass | `2` | fsck order: 1 root, 2 others, 0 none |

Stack:

```
  /dev/vdb   /dev/vdc          <- raw disks
      |          |
     PV         PV             pvcreate
       \        /
        VG  vg_data            vgcreate (pool)
        /       \
   LV lv_app   LV lv_logs      lvcreate -L 10G
      |            |
    ext4         xfs           mkfs
      |            |
   /srv/app     /var/log/app   mount + fstab line

  fstab line:  UUID=...  /srv/app  ext4  defaults,nofail  0  2
               ^ field 1 = the "uuid" field
```

## Worked examples

Build a logical volume (lab VM, destructive):

```bash
sudo pvcreate /dev/vdb /dev/vdc
sudo vgcreate vg_data /dev/vdb /dev/vdc
sudo lvcreate -n lv_app -L 10G vg_data
sudo mkfs.ext4 /dev/vg_data/lv_app
sudo mkdir -p /srv/app
sudo mount /dev/vg_data/lv_app /srv/app
```

Inspect:

```bash
sudo pvs
sudo vgs
sudo lvs
```

Sample output:

```
PV         VG      Fmt  Attr PSize   PFree
/dev/vdb   vg_data lvm2 a--  <20.00g <10.00g
VG      #PV #LV #SN Attr   VSize  VFree
vg_data   2   1   0 wz--n- 39.99g 29.99g
LV     VG      Attr       LSize
lv_app vg_data -wi-ao---- 10.00g
```

Grow a volume and its filesystem online:

```bash
sudo lvextend -r -L +5G /dev/vg_data/lv_app
df -h /srv/app
```

Sample output:

```
Size of logical volume vg_data/lv_app changed from 10.00 GiB to 15.00 GiB.
Filesystem                  Size  Used Avail Use% Mounted on
/dev/mapper/vg_data-lv_app   15G   24K   14G   1% /srv/app
```

Persist the mount in fstab using the UUID:

```bash
sudo blkid /dev/vg_data/lv_app
echo 'UUID=9f8e7d6c-1111-4b3a-8d7c-bbbbbbbbbbbb /srv/app ext4 defaults,nofail 0 2' | sudo tee -a /etc/fstab
sudo umount /srv/app
sudo mount -a
findmnt --verify
```

Sample output:

```
/dev/mapper/vg_data-lv_app: UUID="9f8e7d6c-1111-4b3a-8d7c-bbbbbbbbbbbb" TYPE="ext4"
Success, no errors or warnings detected
```

Extract field 1 of an fstab line:

```bash
line='UUID=9f8e7d6c-1111-4b3a-8d7c-bbbbbbbbbbbb /srv/app ext4 defaults 0 2'
echo "$line" | awk '{print $1}'
```

Sample output:

```
UUID=9f8e7d6c-1111-4b3a-8d7c-bbbbbbbbbbbb
```

Helper from the exercise: `fstab_field_uuid() { echo "$1" | awk '{print $1}'; }`

## Mini-lab

1. Use two loop files as fake disks: `truncate -s 200M d1.img d2.img`, then
   `sudo losetup -f --show d1.img` and the same for `d2.img`.
2. Create PVs on both loop devices, one VG, and one 100M LV.
3. Format with ext4 and mount it on `/mnt/lvlab`.
4. Run `pvs`, `vgs`, `lvs` and sketch the stack.
5. Extend the LV by 50M with `lvextend -r` and confirm with `df -h`.
6. Read `blkid` output and write an fstab line using the UUID with
   `nofail`.
7. Test with `sudo mount -a` and `findmnt --verify` before any reboot.
8. Clean up: `umount`, `lvremove`, `vgremove`, `pvremove`, `losetup -d`.

## Decision guide / failure modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| Boot drops to emergency mode | Bad fstab entry, missing disk | Add `nofail`, fix, `mount -a` before reboot |
| Device name changed after reboot | `/dev/sdX` is unstable | Use `UUID=` or LV path |
| `lvextend` grew LV but `df` same | Filesystem not resized | `resize2fs` (ext4) or `xfs_growfs` (xfs) or use `-r` |
| VG has no free extents | Pool exhausted | `vgextend` with a new PV |
| Cannot shrink xfs | XFS does not shrink | Back up, recreate smaller |
| Field count wrong, mount fails | Typo in fstab | `findmnt --verify` |

Rules: back up before touching partitions, never reboot after editing fstab
until `mount -a` succeeds, prefer UUIDs, add `nofail` for non-critical data
disks, and remember that growing is easy but shrinking is risky.
""",
    "exercise_guide": """Implement fstab_field_uuid in exercise.sh. It receives one complete fstab line as a single quoted argument and must print its first whitespace-separated field, which is the device specification such as UUID=1234-abcd. Fields are separated by spaces or tabs, so awk '{print $1}' or read -r both work. Quote $1 when you use it. Do not print the other fields. Afterwards, run it against real lines from /etc/fstab (skipping comments) and name each of the six fields in your notes.""",
    "exercise_examples": """fstab_field_uuid 'UUID=9f8e-11 /srv/app ext4 defaults 0 2'  -> UUID=9f8e-11
fstab_field_uuid '/dev/vda1 / ext4 defaults 0 1'            -> /dev/vda1
fstab_field_uuid 'LABEL=data /data xfs nofail 0 2'          -> LABEL=data

Only field 1 is printed, followed by a newline.

Tab separated lines also work with awk. Skip comment lines when scanning a real file: grep -v '^#' /etc/fstab | while read -r line; do fstab_field_uuid "$line"; done. Blank lines should be ignored by the caller, not by this helper.""",
  },
}

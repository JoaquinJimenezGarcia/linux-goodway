#!/usr/bin/env python3
"""Generate Linux Goodway lessons, exercises, solutions, README, PROGRESS."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = Path(__file__).resolve().parent


def load_modules():
    spec = importlib.util.spec_from_file_location("curriculum_data", SCRIPTS / "curriculum_data.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["curriculum_data"] = mod
    spec.loader.exec_module(mod)
    return mod.MODULES


def exercise_readme(m: dict) -> str:
    objs = "\n".join(f"- {o}" for o in m["objectives"])
    guide = (m.get("exercise_guide") or "").strip()
    if not guide:
        guide = (
            f"Open `exercise.sh` and implement every stub so `./test.sh` passes. "
            f"Each function name maps to an idea from **{m['title']}** — re-read that section "
            f"of the lesson if a test fails."
        )
    examples = (m.get("exercise_examples") or "").strip()
    if not examples:
        examples = (
            "Worked examples live in the lesson body (commands with expected-style output). "
            "Mirror that behavior in your functions; do not hard-code unrelated strings."
        )
    return f"""# Exercise: {m['n']:02d}. {m['title']}

## Goal

Turn the lesson into **working skill**. Reading is not enough — you must retrieve and apply the ideas.

## Concepts from the lesson

{objs}

## Task

{guide}

## Files

| File | Role |
|------|------|
| `exercise.sh` | Your implementation (edit this) |
| `test.sh` | Automated checks — run until green |
| `../solutions/{m['slug']}/` | Reference only **after** a real attempt |

## Examples / expected behavior

{examples}

## How to work

1. Skim this README, then re-open `lessons/{m['slug']}/lesson.md` (or the PDF).
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
"""


def lesson_md(m: dict) -> str:
    objs = "\n".join(f"- {o}" for o in m["objectives"])
    pits = "\n".join(f"- {p}" for p in m["pitfalls"])
    checks = "\n".join(f"{i}. {c}" for i, c in enumerate(m["checks"], 1))
    reads = "\n".join(f"- {r}" for r in m["reading"])
    guide = (m.get("exercise_guide") or "").strip()
    if guide:
        ex_section = f"""## Exercises

Work in `exercises/{m['slug']}/`. Read that folder's `README.md` fully before coding.

```bash
cd exercises/{m['slug']}
chmod +x test.sh exercise.sh
./test.sh
```

### What you will build

{guide}

### Study loop

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** run 2–3 lab commands from this lesson on a real Linux host; paste notable output into your notes
- **C (Challenge):** rewrite the exercise from memory the next day

**Do not open `solutions/{m['slug']}/` until you have an honest failing attempt.**
"""
    else:
        ex_section = f"""## Exercises

Work in `exercises/{m['slug']}/`. Read `README.md`, then run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/{m['slug']}/` until you have an honest failing attempt.**
"""
    return f"""---
title: "{m['n']:02d}. {m['title']}"
---

# {m['n']:02d}. {m['title']}

**Phase:** {m['phase']}  
**Estimated time:** {m['days']}  
**Slug:** `{m['slug']}`

## Learning objectives

{objs}

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.
Type every command yourself — muscle memory beats skimming.

{m['body'].strip()}

## Common mistakes

{pits}

{ex_section}
## Self-check

Try to answer without scrolling up:

{checks}

## Further reading

{reads}
"""


HARNESS = r'''#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

pass=0
fail=0
assert_eq() {
  local got=$1 want=$2 msg=${3:-}
  if [[ "$got" == "$want" ]]; then
    pass=$((pass + 1))
  else
    echo "FAIL ${msg}: got='$got' want='$want'" >&2
    fail=$((fail + 1))
  fi
}
assert_contains() {
  local hay=$1 needle=$2 msg=${3:-}
  if [[ "$hay" == *"$needle"* ]]; then
    pass=$((pass + 1))
  else
    echo "FAIL ${msg}: missing '$needle' in '$hay'" >&2
    fail=$((fail + 1))
  fi
}
assert_file() {
  if [[ -f "$1" ]]; then pass=$((pass+1)); else echo "FAIL missing file $1" >&2; fail=$((fail+1)); fi
}

# shellcheck disable=SC1091
source "$ROOT/solution.sh" 2>/dev/null || source "$ROOT/exercise.sh"

run_tests

echo "Passed $pass failed $fail"
[[ "$fail" -eq 0 ]]
'''


# Each kind: (exercise.sh starter, solution.sh, test body defining run_tests)
EX: dict[str, tuple[str, str, str]] = {}


def ex(kind: str, starter: str, solution: str, run_tests: str):
    EX[kind] = (starter.strip() + "\n", solution.strip() + "\n", run_tests.strip() + "\n")


ex(
    "orient_hello",
    '''#!/usr/bin/env bash
# greet NAME -> "Hello, NAME"
greet() {
  # TODO
  echo ""
}
''',
    '''#!/usr/bin/env bash
greet() {
  echo "Hello, $1"
}
''',
    '''run_tests() {
  assert_eq "$(greet Ada)" "Hello, Ada" greet
}''',
)

ex(
    "shell_exit",
    '''#!/usr/bin/env bash
# success_code prints 0; failure_code prints a non-zero number (not empty)
success_code() { # TODO
  echo ""
}
failure_code() { # TODO
  echo ""
}
''',
    '''#!/usr/bin/env bash
success_code() { echo 0; }
failure_code() { echo 1; }
''',
    '''run_tests() {
  assert_eq "$(success_code)" "0" success
  local f; f=$(failure_code)
  [[ "$f" != "0" && -n "$f" ]] && pass=$((pass+1)) || { echo FAIL failure_code; fail=$((fail+1)); }
}''',
)

ex(
    "fs_nav",
    '''#!/usr/bin/env bash
# abs_join ROOT REL -> ROOT/REL without duplicate slashes (simple)
abs_join() {
  # TODO
  echo ""
}
''',
    '''#!/usr/bin/env bash
abs_join() {
  local root=${1%/}
  local rel=${2#/}
  echo "$root/$rel"
}
''',
    '''run_tests() {
  assert_eq "$(abs_join /home/ada docs/a)" "/home/ada/docs/a" join
  assert_eq "$(abs_join /home/ada/ docs/a)" "/home/ada/docs/a" join2
}''',
)

ex(
    "fs_links",
    '''#!/usr/bin/env bash
# link_kind PATHHINT: if argument is "soft" print "symbolic"; if "hard" print "hard"
link_kind() {
  # TODO
  echo ""
}
''',
    '''#!/usr/bin/env bash
link_kind() {
  case "$1" in
    soft) echo symbolic ;;
    hard) echo hard ;;
    *) echo unknown ;;
  esac
}
''',
    '''run_tests() {
  assert_eq "$(link_kind soft)" "symbolic" soft
  assert_eq "$(link_kind hard)" "hard" hard
}''',
)

ex(
    "perm_chmod",
    '''#!/usr/bin/env bash
# octal_to_human 755 -> rwxr-xr-x (no leading type char)
octal_to_human() {
  # TODO
  echo ""
}
''',
    '''#!/usr/bin/env bash
digit() {
  case "$1" in
    7) echo rwx ;; 6) echo rw- ;; 5) echo r-x ;; 4) echo r-- ;;
    3) echo -wx ;; 2) echo -w- ;; 1) echo --x ;; 0) echo --- ;;
  esac
}
octal_to_human() {
  local o=$1
  echo "$(digit ${o:0:1})$(digit ${o:1:1})$(digit ${o:2:1})"
}
''',
    '''run_tests() {
  assert_eq "$(octal_to_human 755)" "rwxr-xr-x" 755
  assert_eq "$(octal_to_human 644)" "rw-r--r--" 644
}''',
)

ex(
    "users_id",
    '''#!/usr/bin/env bash
# parse_uid "uid=1000(ada) gid=1000(ada)" -> 1000
parse_uid() {
  # TODO
  echo ""
}
''',
    '''#!/usr/bin/env bash
parse_uid() {
  [[ "$1" =~ uid=([0-9]+) ]] && echo "${BASH_REMATCH[1]}"
}
''',
    '''run_tests() {
  assert_eq "$(parse_uid 'uid=1000(ada) gid=1000(ada)')" "1000" uid
}''',
)

ex(
    "perm_sticky",
    '''#!/usr/bin/env bash
# describe_sticky: print "owner-delete-only" explaining /tmp sticky behavior briefly (exact string)
describe_sticky() {
  # TODO
  echo ""
}
''',
    '''#!/usr/bin/env bash
describe_sticky() { echo "owner-delete-only"; }
''',
    '''run_tests() { assert_eq "$(describe_sticky)" "owner-delete-only" sticky; }''',
)

ex(
    "pipe_wc",
    '''#!/usr/bin/env bash
# count_lines multiline string on stdin -> number of lines
count_lines() {
  # TODO read stdin
  echo 0
}
''',
    '''#!/usr/bin/env bash
count_lines() {
  wc -l | awk '{print $1}'
}
''',
    '''run_tests() {
  assert_eq "$(printf 'a\nb\nc\n' | count_lines)" "3" lines
}''',
)

ex(
    "find_grep",
    '''#!/usr/bin/env bash
# match_todo LINE -> "yes" if contains TODO else "no"
match_todo() {
  # TODO
  echo ""
}
''',
    '''#!/usr/bin/env bash
match_todo() {
  if [[ "$1" == *TODO* ]]; then echo yes; else echo no; fi
}
''',
    '''run_tests() {
  assert_eq "$(match_todo 'fix TODO')" "yes" y
  assert_eq "$(match_todo 'clean')" "no" n
}''',
)

ex(
    "awk_sum",
    '''#!/usr/bin/env bash
# sum_field2: read stdin lines "name count" and sum counts
sum_field2() {
  # TODO
  echo 0
}
''',
    '''#!/usr/bin/env bash
sum_field2() {
  awk '{s+=$2} END{print s+0}'
}
''',
    '''run_tests() {
  assert_eq "$(printf 'a 2\nb 5\n' | sum_field2)" "7" sum
}''',
)

ex(
    "less_quiz",
    '''#!/usr/bin/env bash
# vim_quit_nosave -> exact key sequence label ":q!"
vim_quit_nosave() { echo ""; }
''',
    '''#!/usr/bin/env bash
vim_quit_nosave() { echo ":q!"; }
''',
    '''run_tests() { assert_eq "$(vim_quit_nosave)" ":q!" vim; }''',
)

ex(
    "proc_list",
    '''#!/usr/bin/env bash
# signal_num TERM|KILL -> 15|9
signal_num() { echo ""; }
''',
    '''#!/usr/bin/env bash
signal_num() {
  case "$1" in TERM) echo 15 ;; KILL) echo 9 ;; *) echo 0 ;; esac
}
''',
    '''run_tests() {
  assert_eq "$(signal_num TERM)" "15" term
  assert_eq "$(signal_num KILL)" "9" kill
}''',
)

ex(
    "jobs_bg",
    '''#!/usr/bin/env bash
tmux_detach_keys() { echo ""; }  # expect Ctrl-b d as "ctrl-b d"
''',
    '''#!/usr/bin/env bash
tmux_detach_keys() { echo "ctrl-b d"; }
''',
    '''run_tests() { assert_eq "$(tmux_detach_keys)" "ctrl-b d" tmux; }''',
)

ex(
    "ulimit_quiz",
    '''#!/usr/bin/env bash
# higher_nice_means: print "lower-priority"
higher_nice_means() { echo ""; }
''',
    '''#!/usr/bin/env bash
higher_nice_means() { echo "lower-priority"; }
''',
    '''run_tests() { assert_eq "$(higher_nice_means)" "lower-priority" nice; }''',
)

ex(
    "bash_hello",
    '''#!/usr/bin/env bash
hello() {
  local name=${1:-world}
  # TODO print Hello, <name>
  echo ""
}
''',
    '''#!/usr/bin/env bash
hello() {
  local name=${1:-world}
  echo "Hello, $name"
}
''',
    '''run_tests() {
  assert_eq "$(hello)" "Hello, world" def
  assert_eq "$(hello Ada)" "Hello, Ada" arg
}''',
)

ex(
    "bash_args",
    '''#!/usr/bin/env bash
require_one_arg() {
  # TODO: echo ok if $#>=1 else return 2
  return 0
}
''',
    '''#!/usr/bin/env bash
require_one_arg() {
  [[ $# -ge 1 ]] || return 2
  echo ok
}
''',
    '''run_tests() {
  assert_eq "$(require_one_arg x)" "ok" ok
  set +e
  require_one_arg
  local rc=$?
  set -e
  assert_eq "$rc" "2" rc
}''',
)

ex(
    "bash_assert",
    '''#!/usr/bin/env bash
safe_dir_or_die() {
  local d=${1:-}
  # TODO: return 1 if empty, else echo "$d"
  echo "$d"
}
''',
    '''#!/usr/bin/env bash
safe_dir_or_die() {
  local d=${1:-}
  [[ -n "$d" ]] || return 1
  echo "$d"
}
''',
    '''run_tests() {
  assert_eq "$(safe_dir_or_die /tmp)" "/tmp" ok
  set +e
  safe_dir_or_die ""
  local rc=$?
  set -e
  assert_eq "$rc" "1" empty
}''',
)

ex(
    "net_dns",
    '''#!/usr/bin/env bash
default_https_port() { echo ""; }
''',
    '''#!/usr/bin/env bash
default_https_port() { echo 443; }
''',
    '''run_tests() { assert_eq "$(default_https_port)" "443" https; }''',
)

ex(
    "net_ss",
    '''#!/usr/bin/env bash
ss_listening_flags() { echo ""; } # expect -tulpn
''',
    '''#!/usr/bin/env bash
ss_listening_flags() { echo "-tulpn"; }
''',
    '''run_tests() { assert_eq "$(ss_listening_flags)" "-tulpn" ss; }''',
)

ex(
    "curl_status",
    '''#!/usr/bin/env bash
# http_ok CODE -> yes if 200
http_ok() { echo ""; }
''',
    '''#!/usr/bin/env bash
http_ok() { [[ "$1" == "200" ]] && echo yes || echo no; }
''',
    '''run_tests() {
  assert_eq "$(http_ok 200)" "yes" y
  assert_eq "$(http_ok 500)" "no" n
}''',
)

ex(
    "ssh_config",
    '''#!/usr/bin/env bash
ssh_key_perms() { echo ""; } # expect 600
''',
    '''#!/usr/bin/env bash
ssh_key_perms() { echo 600; }
''',
    '''run_tests() { assert_eq "$(ssh_key_perms)" "600" perms; }''',
)

ex(
    "systemd_quiz",
    '''#!/usr/bin/env bash
# enable_now_meaning -> "start-and-boot"
enable_now_meaning() { echo ""; }
''',
    '''#!/usr/bin/env bash
enable_now_meaning() { echo "start-and-boot"; }
''',
    '''run_tests() { assert_eq "$(enable_now_meaning)" "start-and-boot" en; }''',
)

ex(
    "boot_quiz",
    '''#!/usr/bin/env bash
pid1_name() { echo ""; } # systemd on modern linux
''',
    '''#!/usr/bin/env bash
pid1_name() { echo systemd; }
''',
    '''run_tests() { assert_eq "$(pid1_name)" "systemd" pid1; }''',
)

ex(
    "cron_parse",
    '''#!/usr/bin/env bash
# cron_daily_3am -> "0 3 * * *"
cron_daily_3am() { echo ""; }
''',
    '''#!/usr/bin/env bash
cron_daily_3am() { echo "0 3 * * *"; }
''',
    '''run_tests() { assert_eq "$(cron_daily_3am)" "0 3 * * *" cron; }''',
)

ex(
    "pkg_quiz",
    '''#!/usr/bin/env bash
apt_update_does() { echo ""; } # refresh-indexes
''',
    '''#!/usr/bin/env bash
apt_update_does() { echo "refresh-indexes"; }
''',
    '''run_tests() { assert_eq "$(apt_update_does)" "refresh-indexes" apt; }''',
)

ex(
    "pkg_map",
    '''#!/usr/bin/env bash
# map_install_cmd debian|rhel|alpine -> apt|dnf|apk
map_install_cmd() { echo ""; }
''',
    '''#!/usr/bin/env bash
map_install_cmd() {
  case "$1" in debian|ubuntu) echo apt ;; rhel|fedora) echo dnf ;; alpine) echo apk ;; *) echo unknown ;; esac
}
''',
    '''run_tests() {
  assert_eq "$(map_install_cmd debian)" "apt" a
  assert_eq "$(map_install_cmd rhel)" "dnf" d
  assert_eq "$(map_install_cmd alpine)" "apk" k
}''',
)

ex(
    "disk_df",
    '''#!/usr/bin/env bash
inode_check_flag() { echo ""; } # -i
''',
    '''#!/usr/bin/env bash
inode_check_flag() { echo "-i"; }
''',
    '''run_tests() { assert_eq "$(inode_check_flag)" "-i" inodes; }''',
)

ex(
    "fstab_parse",
    '''#!/usr/bin/env bash
# fstab_field_uuid LINE -> first field
fstab_field_uuid() { echo ""; }
''',
    '''#!/usr/bin/env bash
fstab_field_uuid() { awk '{print $1}' <<<"$1"; }
''',
    '''run_tests() {
  assert_eq "$(fstab_field_uuid 'UUID=abc /data ext4 defaults 0 2')" "UUID=abc" uuid
}''',
)

ex(
    "log_grep",
    '''#!/usr/bin/env bash
journal_unit_flag() { echo ""; } # -u
''',
    '''#!/usr/bin/env bash
journal_unit_flag() { echo "-u"; }
''',
    '''run_tests() { assert_eq "$(journal_unit_flag)" "-u" j; }''',
)

ex(
    "perf_load",
    '''#!/usr/bin/env bash
# load_busy CPUS LOAD -> yes if LOAD > CPUS
load_busy() { echo ""; }
''',
    '''#!/usr/bin/env bash
load_busy() {
  local cpus=$1 load=$2
  awk -v c="$cpus" -v l="$load" 'BEGIN{print (l>c)?"yes":"no"}'
}
''',
    '''run_tests() {
  assert_eq "$(load_busy 2 4)" "yes" busy
  assert_eq "$(load_busy 4 1)" "no" idle
}''',
)

ex(
    "trouble_method",
    '''#!/usr/bin/env bash
first_troubleshooting_step() { echo ""; } # define-symptom
''',
    '''#!/usr/bin/env bash
first_troubleshooting_step() { echo "define-symptom"; }
''',
    '''run_tests() { assert_eq "$(first_troubleshooting_step)" "define-symptom" step; }''',
)

ex(
    "umask_calc",
    '''#!/usr/bin/env bash
# file_mode_after_umask022 -> 644
file_mode_after_umask022() { echo ""; }
''',
    '''#!/usr/bin/env bash
file_mode_after_umask022() { echo 644; }
''',
    '''run_tests() { assert_eq "$(file_mode_after_umask022)" "644" umask; }''',
)

ex(
    "sec_caps",
    '''#!/usr/bin/env bash
avoid_docker_flag() { echo ""; } # --privileged
''',
    '''#!/usr/bin/env bash
avoid_docker_flag() { echo "--privileged"; }
''',
    '''run_tests() { assert_eq "$(avoid_docker_flag)" "--privileged" priv; }''',
)

ex(
    "tls_dates",
    '''#!/usr/bin/env bash
openssl_show_dates_flag() { echo ""; } # -dates
''',
    '''#!/usr/bin/env bash
openssl_show_dates_flag() { echo "-dates"; }
''',
    '''run_tests() { assert_eq "$(openssl_show_dates_flag)" "-dates" dates; }''',
)

ex(
    "harden_list",
    '''#!/usr/bin/env bash
# count_baseline_items: print 5 (ssh-keys firewall updates sudo ntp) as number
count_baseline_items() { echo ""; }
''',
    '''#!/usr/bin/env bash
count_baseline_items() { echo 5; }
''',
    '''run_tests() { assert_eq "$(count_baseline_items)" "5" n; }''',
)

ex(
    "docker_quiz",
    '''#!/usr/bin/env bash
docker_rm_flag_meaning() { echo ""; } # remove-on-exit
''',
    '''#!/usr/bin/env bash
docker_rm_flag_meaning() { echo "remove-on-exit"; }
''',
    '''run_tests() { assert_eq "$(docker_rm_flag_meaning)" "remove-on-exit" rm; }''',
)

ex(
    "ns_quiz",
    '''#!/usr/bin/env bash
default_docker_network() { echo ""; } # bridge
''',
    '''#!/usr/bin/env bash
default_docker_network() { echo bridge; }
''',
    '''run_tests() { assert_eq "$(default_docker_network)" "bridge" net; }''',
)

ex(
    "k8s_quiz",
    '''#!/usr/bin/env bash
kubectl_logs_cmd() { echo ""; } # kubectl logs
''',
    '''#!/usr/bin/env bash
kubectl_logs_cmd() { echo "kubectl logs"; }
''',
    '''run_tests() { assert_eq "$(kubectl_logs_cmd)" "kubectl logs" logs; }''',
)

ex(
    "cloud_meta",
    '''#!/usr/bin/env bash
cloud_init_purpose() { echo ""; } # first-boot-config
''',
    '''#!/usr/bin/env bash
cloud_init_purpose() { echo "first-boot-config"; }
''',
    '''run_tests() { assert_eq "$(cloud_init_purpose)" "first-boot-config" ci; }''',
)

ex(
    "auto_idemp",
    '''#!/usr/bin/env bash
idempotent_means() { echo ""; } # same-result-if-repeated
''',
    '''#!/usr/bin/env bash
idempotent_means() { echo "same-result-if-repeated"; }
''',
    '''run_tests() { assert_eq "$(idempotent_means)" "same-result-if-repeated" id; }''',
)

ex(
    "text_topn",
    '''#!/usr/bin/env bash
# top_token: stdin tokens one per line -> most frequent token (tie: first in sort)
top_token() {
  # TODO
  echo ""
}
''',
    '''#!/usr/bin/env bash
top_token() {
  sort | uniq -c | sort -nr | awk 'NR==1{print $2}'
}
''',
    '''run_tests() {
  assert_eq "$(printf 'a\nb\na\n' | top_token)" "a" top
}''',
)

ex(
    "bash_trap",
    '''#!/usr/bin/env bash
# cleanup_phrase -> "trap EXIT"
cleanup_phrase() { echo ""; }
''',
    '''#!/usr/bin/env bash
cleanup_phrase() { echo "trap EXIT"; }
''',
    '''run_tests() { assert_eq "$(cleanup_phrase)" "trap EXIT" trap; }''',
)

ex(
    "dns_debug",
    '''#!/usr/bin/env bash
nxdomain_means() { echo ""; } # name-not-exist
''',
    '''#!/usr/bin/env bash
nxdomain_means() { echo "name-not-exist"; }
''',
    '''run_tests() { assert_eq "$(nxdomain_means)" "name-not-exist" nx; }''',
)

ex(
    "proxy_quiz",
    '''#!/usr/bin/env bash
tls_termination_means() { echo ""; } # decrypt-at-proxy
''',
    '''#!/usr/bin/env bash
tls_termination_means() { echo "decrypt-at-proxy"; }
''',
    '''run_tests() { assert_eq "$(tls_termination_means)" "decrypt-at-proxy" tls; }''',
)

ex(
    "backup_quiz",
    '''#!/usr/bin/env bash
# rpo_means -> "max-data-loss-window"
rpo_means() { echo ""; }
''',
    '''#!/usr/bin/env bash
rpo_means() { echo "max-data-loss-window"; }
''',
    '''run_tests() { assert_eq "$(rpo_means)" "max-data-loss-window" rpo; }''',
)

ex(
    "ai_linux",
    '''#!/usr/bin/env bash
inference_limit_knob() { echo ""; } # nofile
''',
    '''#!/usr/bin/env bash
inference_limit_knob() { echo "nofile"; }
''',
    '''run_tests() { assert_eq "$(inference_limit_knob)" "nofile" nofile; }''',
)

ex(
    "metrics_quiz",
    '''#!/usr/bin/env bash
alert_on_disk_pct() { echo ""; } # print 90 as example threshold number
''',
    '''#!/usr/bin/env bash
alert_on_disk_pct() { echo 90; }
''',
    '''run_tests() { assert_eq "$(alert_on_disk_pct)" "90" disk; }''',
)

ex(
    "git_ops",
    '''#!/usr/bin/env bash
prefer_deploy_artifact() { echo ""; } # immutable-artifact
''',
    '''#!/usr/bin/env bash
prefer_deploy_artifact() { echo "immutable-artifact"; }
''',
    '''run_tests() { assert_eq "$(prefer_deploy_artifact)" "immutable-artifact" art; }''',
)

ex(
    "mac_quiz",
    '''#!/usr/bin/env bash
# mac_for_distro rhel|ubuntu -> selinux|apparmor
mac_for_distro() { echo ""; }
''',
    '''#!/usr/bin/env bash
mac_for_distro() {
  case "$1" in rhel|fedora|centos) echo selinux ;; ubuntu) echo apparmor ;; *) echo unknown ;; esac
}
''',
    '''run_tests() {
  assert_eq "$(mac_for_distro rhel)" "selinux" s
  assert_eq "$(mac_for_distro ubuntu)" "apparmor" a
}''',
)

ex(
    "nft_quiz",
    '''#!/usr/bin/env bash
firewall_default_inbound() { echo ""; } # deny
''',
    '''#!/usr/bin/env bash
firewall_default_inbound() { echo deny; }
''',
    '''run_tests() { assert_eq "$(firewall_default_inbound)" "deny" deny; }''',
)

ex(
    "systemd_hard",
    '''#!/usr/bin/env bash
nonewprivileges_directive() { echo ""; } # NoNewPrivileges=true
''',
    '''#!/usr/bin/env bash
nonewprivileges_directive() { echo "NoNewPrivileges=true"; }
''',
    '''run_tests() { assert_eq "$(nonewprivileges_directive)" "NoNewPrivileges=true" nnp; }''',
)

ex(
    "lab_plan",
    '''#!/usr/bin/env bash
lab_safety_tool() { echo ""; } # snapshots
''',
    '''#!/usr/bin/env bash
lab_safety_tool() { echo snapshots; }
''',
    '''run_tests() { assert_eq "$(lab_safety_tool)" "snapshots" snap; }''',
)

ex(
    "oncall_drill",
    '''#!/usr/bin/env bash
incident_first_10m() { echo ""; } # define-scope-gather-evidence
''',
    '''#!/usr/bin/env bash
incident_first_10m() { echo "define-scope-gather-evidence"; }
''',
    '''run_tests() { assert_eq "$(incident_first_10m)" "define-scope-gather-evidence" oncall; }''',
)

ex(
    "cap_server",
    '''#!/usr/bin/env bash
# checklist_min_ports: print "22,80,443" as allowed example set for web+ssh
checklist_min_ports() { echo ""; }
''',
    '''#!/usr/bin/env bash
checklist_min_ports() { echo "22,80,443"; }
''',
    '''run_tests() { assert_eq "$(checklist_min_ports)" "22,80,443" ports; }''',
)

ex(
    "cap_break",
    '''#!/usr/bin/env bash
postmortem_required_section() { echo ""; } # root-cause
''',
    '''#!/usr/bin/env bash
postmortem_required_section() { echo "root-cause"; }
''',
    '''run_tests() { assert_eq "$(postmortem_required_section)" "root-cause" pm; }''',
)

ex(
    "cap_ai",
    '''#!/usr/bin/env bash
graceful_stop_signal() { echo ""; } # TERM
''',
    '''#!/usr/bin/env bash
graceful_stop_signal() { echo TERM; }
''',
    '''run_tests() { assert_eq "$(graceful_stop_signal)" "TERM" term; }''',
)

# Enrich trivial quiz stubs with related helpers + clearer comments.
from exercise_enrichments import apply as _apply_exercise_enrichments  # noqa: E402

_apply_exercise_enrichments(EX, ex)


def write_exercise(m: dict):
    slug = m["slug"]
    kind = m["ex_kind"]
    if kind not in EX:
        raise SystemExit(f"missing exercise kind: {kind}")
    starter, solution, run_tests = EX[kind]
    ex_dir = ROOT / "exercises" / slug
    sol_dir = ROOT / "solutions" / slug
    ex_dir.mkdir(parents=True, exist_ok=True)
    sol_dir.mkdir(parents=True, exist_ok=True)

    (ex_dir / "exercise.sh").write_text(starter, encoding="utf-8")
    # Build exercise test.sh
    ex_test = HARNESS.replace(
        'source "$ROOT/solution.sh" 2>/dev/null || source "$ROOT/exercise.sh"',
        'source "$ROOT/exercise.sh"',
    )
    # Insert run_tests before the call
    ex_test = ex_test.replace("run_tests\n", run_tests + "\nrun_tests\n")
    (ex_dir / "test.sh").write_text(ex_test, encoding="utf-8")
    (ex_dir / "README.md").write_text(exercise_readme(m), encoding="utf-8")

    (sol_dir / "solution.sh").write_text(solution, encoding="utf-8")
    sol_test = HARNESS.replace(
        'source "$ROOT/solution.sh" 2>/dev/null || source "$ROOT/exercise.sh"',
        'source "$ROOT/solution.sh"',
    )
    sol_test = sol_test.replace("run_tests\n", run_tests + "\nrun_tests\n")
    (sol_dir / "test.sh").write_text(sol_test, encoding="utf-8")
    (sol_dir / "README.md").write_text(
        "Reference solution. Study only after attempting the exercise.\n\n"
        "Compare approach and style, then close this file and rewrite from memory tomorrow.\n",
        encoding="utf-8",
    )


def write_readme(modules: list[dict]):
    rows = "\n".join(
        f"| {m['n']:02d} | {m['title']} | {m['phase']} | {m['days']} | `pdfs/{m['slug']}.pdf` |"
        for m in modules
    )
    text = f"""# Linux Goodway: Fundamentals to Proficiency (Infra + AI hosts)

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
{rows}
"""
    (ROOT / "README.md").write_text(text, encoding="utf-8")


def write_progress(modules: list[dict]):
    lines = ["# Progress tracker\n", "Check boxes as you complete each lesson (PDF + exercises + rewrite).\n"]
    phase = None
    for m in modules:
        if m["phase"] != phase:
            phase = m["phase"]
            lines.append(f"\n## {phase}\n")
        lines.append(f"- [ ] `{m['slug']}` — {m['title']} ({m['days']})")
    (ROOT / "curriculum").mkdir(parents=True, exist_ok=True)
    (ROOT / "curriculum" / "PROGRESS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    modules = sorted(load_modules(), key=lambda m: m["n"])
    if len(modules) != 56:
        raise SystemExit(f"expected 56 modules, got {len(modules)}")

    missing = [m["ex_kind"] for m in modules if m["ex_kind"] not in EX]
    if missing:
        raise SystemExit(f"missing exercise kinds: {missing}")

    for m in modules:
        d = ROOT / "lessons" / m["slug"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "lesson.md").write_text(lesson_md(m), encoding="utf-8")
        write_exercise(m)

    write_readme(modules)
    write_progress(modules)
    (ROOT / "pdfs").mkdir(exist_ok=True)
    (ROOT / "pdfs" / ".gitkeep").write_text("", encoding="utf-8")
    print(f"Wrote {len(modules)} lessons + exercises/solutions")


if __name__ == "__main__":
    main()

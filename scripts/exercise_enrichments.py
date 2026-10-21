#!/usr/bin/env python3
"""Override trivial EX quiz stubs with richer helpers + tests (smoke-safe)."""

from __future__ import annotations


def apply(EX: dict, ex_fn) -> None:
    """Call ex_fn(kind, starter, solution, run_tests) for each enriched kind."""

    def e(kind: str, starter: str, solution: str, run_tests: str) -> None:
        ex_fn(kind, starter, solution, run_tests)

    e(
        "orient_hello",
        '''#!/usr/bin/env bash
# Lesson 00: practice writing tiny shell functions.
# greet NAME -> "Hello, NAME"
greet() {
  # TODO: echo Hello, <arg1>
  echo ""
}
# farewell NAME -> "Goodbye, NAME"
farewell() {
  # TODO
  echo ""
}
''',
        '''#!/usr/bin/env bash
greet() { echo "Hello, $1"; }
farewell() { echo "Goodbye, $1"; }
''',
        '''run_tests() {
  assert_eq "$(greet Ada)" "Hello, Ada" greet
  assert_eq "$(farewell Ada)" "Goodbye, Ada" farewell
}''',
    )

    e(
        "shell_exit",
        '''#!/usr/bin/env bash
# Exit codes: 0 success, non-zero failure. Scripts and CI depend on this.
success_code() { # TODO -> 0
  echo ""
}
failure_code() { # TODO -> any non-zero integer
  echo ""
}
# is_success CODE -> yes|no
is_success() {
  # TODO
  echo ""
}
''',
        '''#!/usr/bin/env bash
success_code() { echo 0; }
failure_code() { echo 1; }
is_success() { [[ "$1" == "0" ]] && echo yes || echo no; }
''',
        '''run_tests() {
  assert_eq "$(success_code)" "0" success
  local f; f=$(failure_code)
  [[ "$f" != "0" && -n "$f" ]] && pass=$((pass+1)) || { echo FAIL failure_code; fail=$((fail+1)); }
  assert_eq "$(is_success 0)" "yes" ok
  assert_eq "$(is_success 1)" "no" bad
}''',
    )

    e(
        "fs_nav",
        '''#!/usr/bin/env bash
# abs_join ROOT REL -> ROOT/REL without duplicate slashes
abs_join() {
  # TODO
  echo ""
}
# basename_of PATH -> last path component
basename_of() {
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
basename_of() {
  local p=${1%/}
  echo "${p##*/}"
}
''',
        '''run_tests() {
  assert_eq "$(abs_join /home/ada docs/a)" "/home/ada/docs/a" join
  assert_eq "$(abs_join /home/ada/ docs/a)" "/home/ada/docs/a" join2
  assert_eq "$(basename_of /home/ada/docs)" "docs" base
}''',
    )

    e(
        "fs_links",
        '''#!/usr/bin/env bash
# link_kind soft|hard -> symbolic|hard
link_kind() {
  # TODO
  echo ""
}
# same_inode_possible soft|hard -> no|yes
same_inode_possible() {
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
same_inode_possible() {
  case "$1" in hard) echo yes ;; soft) echo no ;; *) echo unknown ;; esac
}
''',
        '''run_tests() {
  assert_eq "$(link_kind soft)" "symbolic" soft
  assert_eq "$(link_kind hard)" "hard" hard
  assert_eq "$(same_inode_possible hard)" "yes" inode
  assert_eq "$(same_inode_possible soft)" "no" softinode
}''',
    )

    e(
        "perm_chmod",
        '''#!/usr/bin/env bash
# octal_to_human 755 -> rwxr-xr-x
octal_to_human() {
  # TODO
  echo ""
}
# is_world_writable MODE -> yes if other has write
is_world_writable() {
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
is_world_writable() {
  local d=${1: -1}
  case "$d" in 2|3|6|7) echo yes ;; *) echo no ;; esac
}
''',
        '''run_tests() {
  assert_eq "$(octal_to_human 755)" "rwxr-xr-x" 755
  assert_eq "$(octal_to_human 644)" "rw-r--r--" 644
  assert_eq "$(is_world_writable 666)" "yes" ww
  assert_eq "$(is_world_writable 644)" "no" nw
}''',
    )

    e(
        "users_id",
        '''#!/usr/bin/env bash
# parse_uid "uid=1000(ada) gid=..." -> 1000
parse_uid() {
  # TODO
  echo ""
}
# parse_user "uid=1000(ada) ..." -> ada
parse_user() {
  # TODO
  echo ""
}
''',
        '''#!/usr/bin/env bash
parse_uid() {
  [[ "$1" =~ uid=([0-9]+) ]] && echo "${BASH_REMATCH[1]}"
}
parse_user() {
  # Prefer a variable so ) in the class does not confuse [[ =~ ]]
  local re='uid=[0-9]+[(]([^)]+)[)]'
  [[ "$1" =~ $re ]] && echo "${BASH_REMATCH[1]}"
}
''',
        '''run_tests() {
  assert_eq "$(parse_uid 'uid=1000(ada) gid=1000(ada)')" "1000" uid
  assert_eq "$(parse_user 'uid=1000(ada) gid=1000(ada)')" "ada" user
}''',
    )

    e(
        "perm_sticky",
        '''#!/usr/bin/env bash
# Sticky /tmp: only owner (or root) can delete their files.
describe_sticky() {
  # TODO -> owner-delete-only
  echo ""
}
sticky_bit_digit() {
  # TODO -> 1
  echo ""
}
''',
        '''#!/usr/bin/env bash
describe_sticky() { echo "owner-delete-only"; }
sticky_bit_digit() { echo 1; }
''',
        '''run_tests() {
  assert_eq "$(describe_sticky)" "owner-delete-only" sticky
  assert_eq "$(sticky_bit_digit)" "1" bit
}''',
    )

    e(
        "pipe_wc",
        '''#!/usr/bin/env bash
count_lines() {
  # TODO: lines on stdin
  echo 0
}
count_words() {
  # TODO: words on stdin
  echo 0
}
''',
        '''#!/usr/bin/env bash
count_lines() { wc -l | awk '{print $1}'; }
count_words() { wc -w | awk '{print $1}'; }
''',
        '''run_tests() {
  assert_eq "$(printf 'a\\nb\\nc\\n' | count_lines)" "3" lines
  assert_eq "$(printf 'a b c\\n' | count_words)" "3" words
}''',
    )

    e(
        "find_grep",
        '''#!/usr/bin/env bash
match_todo() {
  # TODO: yes if LINE contains TODO
  echo ""
}
match_fixme() {
  # TODO: yes if LINE contains FIXME
  echo ""
}
''',
        '''#!/usr/bin/env bash
match_todo() {
  if [[ "$1" == *TODO* ]]; then echo yes; else echo no; fi
}
match_fixme() {
  if [[ "$1" == *FIXME* ]]; then echo yes; else echo no; fi
}
''',
        '''run_tests() {
  assert_eq "$(match_todo 'fix TODO')" "yes" y
  assert_eq "$(match_todo 'clean')" "no" n
  assert_eq "$(match_fixme 'FIXME later')" "yes" f
  assert_eq "$(match_fixme 'ok')" "no" fn
}''',
    )

    e(
        "awk_sum",
        '''#!/usr/bin/env bash
sum_field2() {
  # TODO: sum second field from stdin
  echo 0
}
max_field2() {
  # TODO: max second field
  echo 0
}
''',
        '''#!/usr/bin/env bash
sum_field2() { awk '{s+=$2} END{print s+0}'; }
max_field2() { awk 'BEGIN{m=0} {if($2>m)m=$2} END{print m+0}'; }
''',
        '''run_tests() {
  assert_eq "$(printf 'a 2\\nb 5\\n' | sum_field2)" "7" sum
  assert_eq "$(printf 'a 2\\nb 5\\n' | max_field2)" "5" max
}''',
    )

    e(
        "less_quiz",
        '''#!/usr/bin/env bash
vim_quit_nosave() { echo ""; }  # :q!
less_quit_key() { echo ""; }    # q
''',
        '''#!/usr/bin/env bash
vim_quit_nosave() { echo ":q!"; }
less_quit_key() { echo "q"; }
''',
        '''run_tests() {
  assert_eq "$(vim_quit_nosave)" ":q!" vim
  assert_eq "$(less_quit_key)" "q" less
}''',
    )

    e(
        "proc_list",
        '''#!/usr/bin/env bash
signal_num() { echo ""; }          # TERM->15 KILL->9
prefer_first_signal() { echo ""; } # TERM before KILL
''',
        '''#!/usr/bin/env bash
signal_num() {
  case "$1" in TERM) echo 15 ;; KILL) echo 9 ;; *) echo 0 ;; esac
}
prefer_first_signal() { echo TERM; }
''',
        '''run_tests() {
  assert_eq "$(signal_num TERM)" "15" term
  assert_eq "$(signal_num KILL)" "9" kill
  assert_eq "$(prefer_first_signal)" "TERM" prefer
}''',
    )

    e(
        "jobs_bg",
        '''#!/usr/bin/env bash
tmux_detach_keys() { echo ""; }    # ctrl-b d
background_operator() { echo ""; } # &
''',
        '''#!/usr/bin/env bash
tmux_detach_keys() { echo "ctrl-b d"; }
background_operator() { echo "&"; }
''',
        '''run_tests() {
  assert_eq "$(tmux_detach_keys)" "ctrl-b d" tmux
  assert_eq "$(background_operator)" "&" bg
}''',
    )

    e(
        "ulimit_quiz",
        '''#!/usr/bin/env bash
higher_nice_means() { echo ""; }  # lower-priority
ulimit_nofile_flag() { echo ""; } # -n  (implement with printf, not echo)
''',
        '''#!/usr/bin/env bash
higher_nice_means() { echo "lower-priority"; }
# Use printf: echo "-n" is treated as echo's -n flag
ulimit_nofile_flag() { printf '%s\n' '-n'; }
''',
        '''run_tests() {
  assert_eq "$(higher_nice_means)" "lower-priority" nice
  assert_eq "$(ulimit_nofile_flag)" "-n" nofile
}''',
    )

    e(
        "bash_hello",
        '''#!/usr/bin/env bash
hello() {
  local name=${1:-world}
  # TODO: Hello, <name>
  echo ""
}
shout() {
  # TODO: HELLO, <name>
  echo ""
}
''',
        '''#!/usr/bin/env bash
hello() {
  local name=${1:-world}
  echo "Hello, $name"
}
shout() { echo "HELLO, $1"; }
''',
        '''run_tests() {
  assert_eq "$(hello)" "Hello, world" def
  assert_eq "$(hello Ada)" "Hello, Ada" arg
  assert_eq "$(shout Ada)" "HELLO, Ada" shout
}''',
    )

    e(
        "bash_args",
        '''#!/usr/bin/env bash
require_one_arg() {
  # TODO: echo ok if $#>=1 else return 2
  return 0
}
arg_count() {
  # TODO: print $#
  echo 0
}
''',
        '''#!/usr/bin/env bash
require_one_arg() {
  [[ $# -ge 1 ]] || return 2
  echo ok
}
arg_count() { echo $#; }
''',
        '''run_tests() {
  assert_eq "$(require_one_arg x)" "ok" ok
  set +e
  require_one_arg
  local rc=$?
  set -e
  assert_eq "$rc" "2" rc
  assert_eq "$(arg_count a b c)" "3" count
}''',
    )

    e(
        "bash_assert",
        '''#!/usr/bin/env bash
safe_dir_or_die() {
  local d=${1:-}
  # TODO: return 1 if empty else echo d
  echo "$d"
}
assert_nonempty() {
  # TODO: return 1 if empty
  return 0
}
''',
        '''#!/usr/bin/env bash
safe_dir_or_die() {
  local d=${1:-}
  [[ -n "$d" ]] || return 1
  echo "$d"
}
assert_nonempty() {
  [[ -n "${1:-}" ]] || return 1
  return 0
}
''',
        '''run_tests() {
  assert_eq "$(safe_dir_or_die /tmp)" "/tmp" ok
  set +e
  safe_dir_or_die ""
  local rc=$?
  set -e
  assert_eq "$rc" "1" empty
  set +e
  assert_nonempty ""
  rc=$?
  set -e
  assert_eq "$rc" "1" nonempty
  assert_nonempty x
  assert_eq "$?" "0" nonempty_ok
}''',
    )

    e(
        "net_dns",
        '''#!/usr/bin/env bash
default_https_port() { echo ""; }  # 443
default_http_port() { echo ""; }   # 80
default_ssh_port() { echo ""; }    # 22
''',
        '''#!/usr/bin/env bash
default_https_port() { echo 443; }
default_http_port() { echo 80; }
default_ssh_port() { echo 22; }
''',
        '''run_tests() {
  assert_eq "$(default_https_port)" "443" https
  assert_eq "$(default_http_port)" "80" http
  assert_eq "$(default_ssh_port)" "22" ssh
}''',
    )

    e(
        "net_ss",
        '''#!/usr/bin/env bash
ss_listening_flags() { echo ""; }  # -tulpn
ss_tcp_flag() { echo ""; }         # -t
''',
        '''#!/usr/bin/env bash
ss_listening_flags() { echo "-tulpn"; }
ss_tcp_flag() { echo "-t"; }
''',
        '''run_tests() {
  assert_eq "$(ss_listening_flags)" "-tulpn" ss
  assert_eq "$(ss_tcp_flag)" "-t" tcp
}''',
    )

    e(
        "curl_status",
        '''#!/usr/bin/env bash
http_ok() { echo ""; }       # yes if 200
http_redirect() { echo ""; } # yes if 301 or 302
''',
        '''#!/usr/bin/env bash
http_ok() { [[ "$1" == "200" ]] && echo yes || echo no; }
http_redirect() { [[ "$1" == "301" || "$1" == "302" ]] && echo yes || echo no; }
''',
        '''run_tests() {
  assert_eq "$(http_ok 200)" "yes" y
  assert_eq "$(http_ok 500)" "no" n
  assert_eq "$(http_redirect 301)" "yes" r
  assert_eq "$(http_redirect 200)" "no" nr
}''',
    )

    e(
        "ssh_config",
        '''#!/usr/bin/env bash
ssh_key_perms() { echo ""; }  # 600
ssh_dir_perms() { echo ""; }  # 700
''',
        '''#!/usr/bin/env bash
ssh_key_perms() { echo 600; }
ssh_dir_perms() { echo 700; }
''',
        '''run_tests() {
  assert_eq "$(ssh_key_perms)" "600" perms
  assert_eq "$(ssh_dir_perms)" "700" dir
}''',
    )

    e(
        "systemd_quiz",
        '''#!/usr/bin/env bash
enable_now_meaning() { echo ""; }  # start-and-boot
journal_follow_flag() { echo ""; } # -f
''',
        '''#!/usr/bin/env bash
enable_now_meaning() { echo "start-and-boot"; }
journal_follow_flag() { echo "-f"; }
''',
        '''run_tests() {
  assert_eq "$(enable_now_meaning)" "start-and-boot" en
  assert_eq "$(journal_follow_flag)" "-f" follow
}''',
    )

    e(
        "boot_quiz",
        '''#!/usr/bin/env bash
pid1_name() { echo ""; }           # systemd
multi_user_target() { echo ""; }   # multi-user.target
''',
        '''#!/usr/bin/env bash
pid1_name() { echo systemd; }
multi_user_target() { echo "multi-user.target"; }
''',
        '''run_tests() {
  assert_eq "$(pid1_name)" "systemd" pid1
  assert_eq "$(multi_user_target)" "multi-user.target" target
}''',
    )

    e(
        "cron_parse",
        '''#!/usr/bin/env bash
cron_daily_3am() { echo ""; }  # 0 3 * * *
cron_hourly() { echo ""; }     # 0 * * * *
''',
        '''#!/usr/bin/env bash
cron_daily_3am() { echo "0 3 * * *"; }
cron_hourly() { echo "0 * * * *"; }
''',
        '''run_tests() {
  assert_eq "$(cron_daily_3am)" "0 3 * * *" cron
  assert_eq "$(cron_hourly)" "0 * * * *" hourly
}''',
    )

    e(
        "pkg_quiz",
        '''#!/usr/bin/env bash
apt_update_does() { echo ""; }   # refresh-indexes
apt_upgrade_does() { echo ""; }  # install-updates
''',
        '''#!/usr/bin/env bash
apt_update_does() { echo "refresh-indexes"; }
apt_upgrade_does() { echo "install-updates"; }
''',
        '''run_tests() {
  assert_eq "$(apt_update_does)" "refresh-indexes" apt
  assert_eq "$(apt_upgrade_does)" "install-updates" up
}''',
    )

    e(
        "pkg_map",
        '''#!/usr/bin/env bash
map_install_cmd() { echo ""; }  # debian->apt rhel->dnf alpine->apk
map_query_cmd() { echo ""; }    # debian->apt rhel->rpm
''',
        '''#!/usr/bin/env bash
map_install_cmd() {
  case "$1" in debian|ubuntu) echo apt ;; rhel|fedora) echo dnf ;; alpine) echo apk ;; *) echo unknown ;; esac
}
map_query_cmd() {
  case "$1" in debian|ubuntu) echo apt ;; rhel|fedora) echo rpm ;; *) echo unknown ;; esac
}
''',
        '''run_tests() {
  assert_eq "$(map_install_cmd debian)" "apt" a
  assert_eq "$(map_install_cmd rhel)" "dnf" d
  assert_eq "$(map_install_cmd alpine)" "apk" k
  assert_eq "$(map_query_cmd debian)" "apt" qa
  assert_eq "$(map_query_cmd rhel)" "rpm" qr
}''',
    )

    e(
        "disk_df",
        '''#!/usr/bin/env bash
inode_check_flag() { echo ""; }  # -i
df_human_flag() { echo ""; }     # -h
''',
        '''#!/usr/bin/env bash
inode_check_flag() { echo "-i"; }
df_human_flag() { echo "-h"; }
''',
        '''run_tests() {
  assert_eq "$(inode_check_flag)" "-i" inodes
  assert_eq "$(df_human_flag)" "-h" human
}''',
    )

    e(
        "fstab_parse",
        '''#!/usr/bin/env bash
fstab_field_uuid() { echo ""; }   # field 1
fstab_mountpoint() { echo ""; }   # field 2
''',
        '''#!/usr/bin/env bash
fstab_field_uuid() { awk '{print $1}' <<<"$1"; }
fstab_mountpoint() { awk '{print $2}' <<<"$1"; }
''',
        '''run_tests() {
  assert_eq "$(fstab_field_uuid 'UUID=abc /data ext4 defaults 0 2')" "UUID=abc" uuid
  assert_eq "$(fstab_mountpoint 'UUID=abc /data ext4 defaults 0 2')" "/data" mnt
}''',
    )

    e(
        "log_grep",
        '''#!/usr/bin/env bash
journal_unit_flag() { echo ""; }   # -u
journal_since_flag() { echo ""; }  # -S
''',
        '''#!/usr/bin/env bash
journal_unit_flag() { echo "-u"; }
journal_since_flag() { echo "-S"; }
''',
        '''run_tests() {
  assert_eq "$(journal_unit_flag)" "-u" j
  assert_eq "$(journal_since_flag)" "-S" since
}''',
    )

    e(
        "perf_load",
        '''#!/usr/bin/env bash
load_busy() { echo ""; }  # yes if LOAD > CPUS
load_idle() { echo ""; }  # yes if LOAD < CPUS
''',
        '''#!/usr/bin/env bash
load_busy() {
  local cpus=$1 load=$2
  awk -v c="$cpus" -v l="$load" 'BEGIN{print (l>c)?"yes":"no"}'
}
load_idle() {
  local cpus=$1 load=$2
  awk -v c="$cpus" -v l="$load" 'BEGIN{print (l<c)?"yes":"no"}'
}
''',
        '''run_tests() {
  assert_eq "$(load_busy 2 4)" "yes" busy
  assert_eq "$(load_busy 4 1)" "no" notbusy
  assert_eq "$(load_idle 4 1)" "yes" idle
}''',
    )

    e(
        "trouble_method",
        '''#!/usr/bin/env bash
first_troubleshooting_step() { echo ""; }   # define-symptom
second_troubleshooting_step() { echo ""; }  # gather-evidence
''',
        '''#!/usr/bin/env bash
first_troubleshooting_step() { echo "define-symptom"; }
second_troubleshooting_step() { echo "gather-evidence"; }
''',
        '''run_tests() {
  assert_eq "$(first_troubleshooting_step)" "define-symptom" step
  assert_eq "$(second_troubleshooting_step)" "gather-evidence" step2
}''',
    )

    e(
        "umask_calc",
        '''#!/usr/bin/env bash
file_mode_after_umask022() { echo ""; }  # 644
dir_mode_after_umask022() { echo ""; }   # 755
''',
        '''#!/usr/bin/env bash
file_mode_after_umask022() { echo 644; }
dir_mode_after_umask022() { echo 755; }
''',
        '''run_tests() {
  assert_eq "$(file_mode_after_umask022)" "644" umask
  assert_eq "$(dir_mode_after_umask022)" "755" dir
}''',
    )

    e(
        "sec_caps",
        '''#!/usr/bin/env bash
avoid_docker_flag() { echo ""; }   # --privileged
prefer_cap_action() { echo ""; }   # drop
''',
        '''#!/usr/bin/env bash
avoid_docker_flag() { echo "--privileged"; }
prefer_cap_action() { echo drop; }
''',
        '''run_tests() {
  assert_eq "$(avoid_docker_flag)" "--privileged" priv
  assert_eq "$(prefer_cap_action)" "drop" drop
}''',
    )

    e(
        "tls_dates",
        '''#!/usr/bin/env bash
openssl_show_dates_flag() { echo ""; }    # -dates
openssl_show_subject_flag() { echo ""; }  # -subject
''',
        '''#!/usr/bin/env bash
openssl_show_dates_flag() { echo "-dates"; }
openssl_show_subject_flag() { echo "-subject"; }
''',
        '''run_tests() {
  assert_eq "$(openssl_show_dates_flag)" "-dates" dates
  assert_eq "$(openssl_show_subject_flag)" "-subject" subj
}''',
    )

    e(
        "harden_list",
        '''#!/usr/bin/env bash
count_baseline_items() { echo ""; }         # 5
password_auth_on_internet() { echo ""; }    # disable
''',
        '''#!/usr/bin/env bash
count_baseline_items() { echo 5; }
password_auth_on_internet() { echo disable; }
''',
        '''run_tests() {
  assert_eq "$(count_baseline_items)" "5" n
  assert_eq "$(password_auth_on_internet)" "disable" pw
}''',
    )

    e(
        "docker_quiz",
        '''#!/usr/bin/env bash
docker_rm_flag_meaning() { echo ""; }   # remove-on-exit
docker_interactive_flags() { echo ""; } # -it
''',
        '''#!/usr/bin/env bash
docker_rm_flag_meaning() { echo "remove-on-exit"; }
docker_interactive_flags() { echo "-it"; }
''',
        '''run_tests() {
  assert_eq "$(docker_rm_flag_meaning)" "remove-on-exit" rm
  assert_eq "$(docker_interactive_flags)" "-it" it
}''',
    )

    e(
        "ns_quiz",
        '''#!/usr/bin/env bash
default_docker_network() { echo ""; }  # bridge
host_docker_network() { echo ""; }     # host
''',
        '''#!/usr/bin/env bash
default_docker_network() { echo bridge; }
host_docker_network() { echo host; }
''',
        '''run_tests() {
  assert_eq "$(default_docker_network)" "bridge" net
  assert_eq "$(host_docker_network)" "host" host
}''',
    )

    e(
        "k8s_quiz",
        '''#!/usr/bin/env bash
kubectl_logs_cmd() { echo ""; }      # kubectl logs
kubectl_get_pods_cmd() { echo ""; }  # kubectl get pods
''',
        '''#!/usr/bin/env bash
kubectl_logs_cmd() { echo "kubectl logs"; }
kubectl_get_pods_cmd() { echo "kubectl get pods"; }
''',
        '''run_tests() {
  assert_eq "$(kubectl_logs_cmd)" "kubectl logs" logs
  assert_eq "$(kubectl_get_pods_cmd)" "kubectl get pods" pods
}''',
    )

    e(
        "cloud_meta",
        '''#!/usr/bin/env bash
cloud_init_purpose() { echo ""; }    # first-boot-config
cloud_metadata_role() { echo ""; }   # instance-identity
''',
        '''#!/usr/bin/env bash
cloud_init_purpose() { echo "first-boot-config"; }
cloud_metadata_role() { echo "instance-identity"; }
''',
        '''run_tests() {
  assert_eq "$(cloud_init_purpose)" "first-boot-config" ci
  assert_eq "$(cloud_metadata_role)" "instance-identity" meta
}''',
    )

    e(
        "auto_idemp",
        '''#!/usr/bin/env bash
idempotent_means() { echo ""; }       # same-result-if-repeated
package_desired_state() { echo ""; }  # present
''',
        '''#!/usr/bin/env bash
idempotent_means() { echo "same-result-if-repeated"; }
package_desired_state() { echo present; }
''',
        '''run_tests() {
  assert_eq "$(idempotent_means)" "same-result-if-repeated" id
  assert_eq "$(package_desired_state)" "present" pkg
}''',
    )

    e(
        "text_topn",
        '''#!/usr/bin/env bash
top_token() {
  # TODO: most frequent token on stdin
  echo ""
}
count_unique() {
  # TODO: distinct token count
  echo 0
}
''',
        '''#!/usr/bin/env bash
top_token() {
  sort | uniq -c | sort -nr | awk 'NR==1{print $2}'
}
count_unique() {
  sort -u | wc -l | awk '{print $1}'
}
''',
        '''run_tests() {
  assert_eq "$(printf 'a\\nb\\na\\n' | top_token)" "a" top
  assert_eq "$(printf 'a\\nb\\na\\n' | count_unique)" "2" uniq
}''',
    )

    e(
        "bash_trap",
        '''#!/usr/bin/env bash
cleanup_phrase() { echo ""; }   # trap EXIT
graceful_signal() { echo ""; }  # TERM
''',
        '''#!/usr/bin/env bash
cleanup_phrase() { echo "trap EXIT"; }
graceful_signal() { echo TERM; }
''',
        '''run_tests() {
  assert_eq "$(cleanup_phrase)" "trap EXIT" trap
  assert_eq "$(graceful_signal)" "TERM" term
}''',
    )

    e(
        "dns_debug",
        '''#!/usr/bin/env bash
nxdomain_means() { echo ""; }  # name-not-exist
servfail_means() { echo ""; }  # resolver-error
''',
        '''#!/usr/bin/env bash
nxdomain_means() { echo "name-not-exist"; }
servfail_means() { echo "resolver-error"; }
''',
        '''run_tests() {
  assert_eq "$(nxdomain_means)" "name-not-exist" nx
  assert_eq "$(servfail_means)" "resolver-error" sf
}''',
    )

    e(
        "proxy_quiz",
        '''#!/usr/bin/env bash
tls_termination_means() { echo ""; }     # decrypt-at-proxy
backend_after_terminate() { echo ""; }   # http
''',
        '''#!/usr/bin/env bash
tls_termination_means() { echo "decrypt-at-proxy"; }
backend_after_terminate() { echo http; }
''',
        '''run_tests() {
  assert_eq "$(tls_termination_means)" "decrypt-at-proxy" tls
  assert_eq "$(backend_after_terminate)" "http" be
}''',
    )

    e(
        "backup_quiz",
        '''#!/usr/bin/env bash
rpo_means() { echo ""; }  # max-data-loss-window
rto_means() { echo ""; }  # max-downtime-window
''',
        '''#!/usr/bin/env bash
rpo_means() { echo "max-data-loss-window"; }
rto_means() { echo "max-downtime-window"; }
''',
        '''run_tests() {
  assert_eq "$(rpo_means)" "max-data-loss-window" rpo
  assert_eq "$(rto_means)" "max-downtime-window" rto
}''',
    )

    e(
        "ai_linux",
        '''#!/usr/bin/env bash
inference_limit_knob() { echo ""; }  # nofile
memory_limit_knob() { echo ""; }     # MemoryMax
''',
        '''#!/usr/bin/env bash
inference_limit_knob() { echo "nofile"; }
memory_limit_knob() { echo "MemoryMax"; }
''',
        '''run_tests() {
  assert_eq "$(inference_limit_knob)" "nofile" nofile
  assert_eq "$(memory_limit_knob)" "MemoryMax" mem
}''',
    )

    e(
        "metrics_quiz",
        '''#!/usr/bin/env bash
alert_on_disk_pct() { echo ""; }  # 90
alert_on_mem_pct() { echo ""; }   # 95
''',
        '''#!/usr/bin/env bash
alert_on_disk_pct() { echo 90; }
alert_on_mem_pct() { echo 95; }
''',
        '''run_tests() {
  assert_eq "$(alert_on_disk_pct)" "90" disk
  assert_eq "$(alert_on_mem_pct)" "95" mem
}''',
    )

    e(
        "git_ops",
        '''#!/usr/bin/env bash
prefer_deploy_artifact() { echo ""; }  # immutable-artifact
avoid_deploy_method() { echo ""; }     # git-pull-on-prod
''',
        '''#!/usr/bin/env bash
prefer_deploy_artifact() { echo "immutable-artifact"; }
avoid_deploy_method() { echo "git-pull-on-prod"; }
''',
        '''run_tests() {
  assert_eq "$(prefer_deploy_artifact)" "immutable-artifact" art
  assert_eq "$(avoid_deploy_method)" "git-pull-on-prod" avoid
}''',
    )

    e(
        "mac_quiz",
        '''#!/usr/bin/env bash
mac_for_distro() { echo ""; }      # rhel->selinux ubuntu->apparmor
mac_enforcing_word() { echo ""; }  # enforcing
''',
        '''#!/usr/bin/env bash
mac_for_distro() {
  case "$1" in rhel|fedora|centos) echo selinux ;; ubuntu) echo apparmor ;; *) echo unknown ;; esac
}
mac_enforcing_word() { echo enforcing; }
''',
        '''run_tests() {
  assert_eq "$(mac_for_distro rhel)" "selinux" s
  assert_eq "$(mac_for_distro ubuntu)" "apparmor" a
  assert_eq "$(mac_enforcing_word)" "enforcing" enf
}''',
    )

    e(
        "nft_quiz",
        '''#!/usr/bin/env bash
firewall_default_inbound() { echo ""; }      # deny
firewall_default_outbound_lab() { echo ""; } # allow
''',
        '''#!/usr/bin/env bash
firewall_default_inbound() { echo deny; }
firewall_default_outbound_lab() { echo allow; }
''',
        '''run_tests() {
  assert_eq "$(firewall_default_inbound)" "deny" deny
  assert_eq "$(firewall_default_outbound_lab)" "allow" allow
}''',
    )

    e(
        "systemd_hard",
        '''#!/usr/bin/env bash
nonewprivileges_directive() { echo ""; }  # NoNewPrivileges=true
protect_system_strict() { echo ""; }      # ProtectSystem=strict
''',
        '''#!/usr/bin/env bash
nonewprivileges_directive() { echo "NoNewPrivileges=true"; }
protect_system_strict() { echo "ProtectSystem=strict"; }
''',
        '''run_tests() {
  assert_eq "$(nonewprivileges_directive)" "NoNewPrivileges=true" nnp
  assert_eq "$(protect_system_strict)" "ProtectSystem=strict" ps
}''',
    )

    e(
        "lab_plan",
        '''#!/usr/bin/env bash
lab_safety_tool() { echo ""; }   # snapshots
lab_first_action() { echo ""; }  # snapshot-or-backup
''',
        '''#!/usr/bin/env bash
lab_safety_tool() { echo snapshots; }
lab_first_action() { echo "snapshot-or-backup"; }
''',
        '''run_tests() {
  assert_eq "$(lab_safety_tool)" "snapshots" snap
  assert_eq "$(lab_first_action)" "snapshot-or-backup" first
}''',
    )

    e(
        "oncall_drill",
        '''#!/usr/bin/env bash
incident_first_10m() { echo ""; }   # define-scope-gather-evidence
incident_avoid_early() { echo ""; } # random-restarts
''',
        '''#!/usr/bin/env bash
incident_first_10m() { echo "define-scope-gather-evidence"; }
incident_avoid_early() { echo "random-restarts"; }
''',
        '''run_tests() {
  assert_eq "$(incident_first_10m)" "define-scope-gather-evidence" oncall
  assert_eq "$(incident_avoid_early)" "random-restarts" avoid
}''',
    )

    e(
        "cap_server",
        '''#!/usr/bin/env bash
checklist_min_ports() { echo ""; }  # 22,80,443
checklist_ssh_only() { echo ""; }   # 22
''',
        '''#!/usr/bin/env bash
checklist_min_ports() { echo "22,80,443"; }
checklist_ssh_only() { echo "22"; }
''',
        '''run_tests() {
  assert_eq "$(checklist_min_ports)" "22,80,443" ports
  assert_eq "$(checklist_ssh_only)" "22" ssh
}''',
    )

    e(
        "cap_break",
        '''#!/usr/bin/env bash
postmortem_required_section() { echo ""; }  # root-cause
postmortem_also_include() { echo ""; }      # timeline
''',
        '''#!/usr/bin/env bash
postmortem_required_section() { echo "root-cause"; }
postmortem_also_include() { echo timeline; }
''',
        '''run_tests() {
  assert_eq "$(postmortem_required_section)" "root-cause" pm
  assert_eq "$(postmortem_also_include)" "timeline" tl
}''',
    )

    e(
        "cap_ai",
        '''#!/usr/bin/env bash
graceful_stop_signal() { echo ""; }  # TERM
force_stop_signal() { echo ""; }     # KILL
''',
        '''#!/usr/bin/env bash
graceful_stop_signal() { echo TERM; }
force_stop_signal() { echo KILL; }
''',
        '''run_tests() {
  assert_eq "$(graceful_stop_signal)" "TERM" term
  assert_eq "$(force_stop_signal)" "KILL" kill
}''',
    )

    _ = EX  # silence unused if caller only uses ex_fn

#!/usr/bin/env python3
"""Expanded lesson content for modules 42..55 (ASCII only).

EXTRA maps module number -> dict with keys:
  body, exercise_guide, exercise_examples
Merge into curriculum modules by n.
"""

from __future__ import annotations

EXTRA: dict[int, dict[str, str]] = {}

# ---------------------------------------------------------------------------
# 42 DNS deep
# ---------------------------------------------------------------------------
EXTRA[42] = {
    "body": r"""
## Why this matters

When an application says "cannot connect", the first broken link is very often
name resolution, not the network. A web service that works by IP but fails by
name, a container that cannot reach a private API, a deploy that "randomly"
hits an old server: all of these are DNS stories. If you can split a failure
into "name did not resolve", "name resolved to the wrong thing", and "resolver
did not answer", you cut the search space by two thirds in under a minute.

Two answers matter most. **NXDOMAIN** means the authoritative side said the
name does not exist (name-not-exist). A **timeout** means nobody answered at
all, which is a path, firewall, or resolver-health problem. Treating them the
same wastes hours.

## Core concepts

| Piece | What it does | Where to look |
|-------|--------------|---------------|
| Stub resolver | libc code inside every program | `getent ahosts NAME` |
| nsswitch | order of sources: files, dns, mdns | `/etc/nsswitch.conf` |
| /etc/hosts | static overrides, checked first | `cat /etc/hosts` |
| resolv.conf | which nameservers and search domains | `/etc/resolv.conf` |
| systemd-resolved | local caching stub at 127.0.0.53 | `resolvectl status` |
| Recursive resolver | does the walk for you, caches | `dig @1.1.1.1 NAME` |
| Authoritative server | owns the zone data | `dig +trace NAME` |

Response codes you must know: NOERROR (ok, maybe empty answer), NXDOMAIN
(name-not-exist), SERVFAIL (resolver or upstream broke), REFUSED (policy).

```
 app --> libc --> nsswitch --> /etc/hosts ?
                      |
                      v
              resolv.conf / resolved (127.0.0.53)
                      |  cache hit? -> answer
                      v
              recursive resolver --> root --> TLD --> authoritative
                      ^                                   |
                      +----------- answer + TTL ----------+
```

Search domains: with `search corp.example` and `ndots:1`, a short name like
`db` is tried as `db.corp.example` first. That is convenient and also the
reason a typo can resolve to something surprising.

## Worked examples

Example 1: compare what the program sees with what DNS says.

```bash
getent ahosts example.com        # what libc (your apps) resolves
dig +short example.com           # what DNS says via resolv.conf
```

If `getent` fails but `dig` works, suspect nsswitch, hosts, or a search
domain, not the DNS server.

Example 2: NXDOMAIN versus timeout.

```bash
dig nosuchhost.example.com | grep status
# ;; ->>HEADER<<- opcode: QUERY, status: NXDOMAIN
dig @10.255.255.1 example.com +time=2 +tries=1
# ;; connection timed out; no servers could be reached
```

NXDOMAIN is a clean "no such name": fix the name or the zone. The timeout
says the server is unreachable: check route, firewall, UDP/TCP 53.

Example 3: who is the resolver?

```bash
resolvectl status | sed -n 1,20p
resolvectl query example.com
cat /etc/resolv.conf             # often only 127.0.0.53
```

Example 4: walk the delegation to find a stale record.

```bash
dig +trace www.example.com | tail -5
dig www.example.com +noall +answer      # note the TTL column
```

If the TTL says 3600, a changed record may stay stale up to an hour in
caches. Lower the TTL before a planned cutover, not after.

Example 5: flush caches only after you have evidence.

```bash
resolvectl flush-caches
resolvectl statistics | grep -i cache
```

## Mini-lab

1. Run `cat /etc/resolv.conf` and `resolvectl status`; write down the active
   nameserver and search domains.
2. Run `dig example.com` and `getent ahosts example.com`; confirm they agree.
3. Add a fake line to `/etc/hosts` in a lab VM: `203.0.113.9 lab.test`. Run
   `getent hosts lab.test` and `dig lab.test`. Explain why they differ.
4. Query a made-up name and record the status field. Say aloud what that
   status means (name-not-exist).
5. Point dig at an unroutable server with a short timeout and compare the
   failure to step 4.
6. Remove your hosts line. Note the TTL of one record and when it would expire.

## Decision guide / failure modes

| Symptom | Likely cause | First check |
|---------|--------------|-------------|
| NXDOMAIN | typo, missing record, wrong search domain | `dig NAME +search` vs FQDN with dot |
| Timeout | resolver unreachable, port 53 blocked | `dig @server NAME +time=2` |
| SERVFAIL | DNSSEC failure, broken upstream | `dig +cd NAME`, try another resolver |
| Works by dig, fails in app | hosts file, nsswitch, container resolver | `getent ahosts NAME` |
| Old IP returned | cache or high TTL | `dig +trace`, `resolvectl flush-caches` |
| Private zone fails | hardcoded public resolver | remove 8.8.8.8 override |

Failure modes to avoid: editing `/etc/resolv.conf` by hand on a host where
systemd-resolved or NetworkManager rewrites it; declaring "network is down"
because one lookup failed; skipping the trailing dot test for search-domain
surprises. Rule of thumb: always ask the stub what the app sees, then ask the
server what it knows, then walk the chain.
""",
    "exercise_guide": r"""Open `exercise.sh` and implement the `nxdomain_means` function so it prints
one short token describing what an NXDOMAIN response tells you about the
queried name. Use the vocabulary from the lesson: the token is lowercase,
words joined with hyphens, no spaces, no trailing text. The function must not
call the network; it is a recall check of the response-code table. After the
test passes, run `dig` against a name you invent in your lab and read the
`status:` field to confirm in practice. Then write one sentence in your notes
that contrasts NXDOMAIN with a timeout, and say which one points at the
network path rather than the zone data.""",
    "exercise_examples": r"""Run from the exercise folder:

    source ./exercise.sh
    nxdomain_means

Expected single line of output:

    name-not-exist

Related lab check (not graded):

    dig nosuchhost.example.com | grep status
    ;; ->>HEADER<<- opcode: QUERY, status: NXDOMAIN

A timeout prints no status line at all; dig reports that no servers could be
reached. Keep these two outcomes distinct in your notes.""",
}

# ---------------------------------------------------------------------------
# 43 HTTP load balancing, TLS, reverse proxy
# ---------------------------------------------------------------------------
EXTRA[43] = {
    "body": r"""
## Why this matters

Almost every production web service sits behind a reverse proxy or load
balancer: nginx, HAProxy, Envoy, Caddy, or a cloud LB. On Linux you are the
person who configures it, reads its logs, and explains why users see a 502.
Understanding where TLS ends, who sees the real client IP, and how health
checks remove broken backends is the difference between a five-minute fix and
a long outage.

TLS termination means the proxy decrypts the client connection (decrypt-at-
proxy). Traffic to the backend may then be plain HTTP on a private network, or
re-encrypted. Knowing which you have decides where certificates live, what a
packet capture shows, and which hop owns the expiry alarm.

## Core concepts

| Term | Meaning |
|------|---------|
| Reverse proxy | accepts client requests, forwards to backends |
| Upstream / backend | the app servers behind the proxy |
| TLS termination | proxy decrypts client TLS (decrypt-at-proxy) |
| TLS passthrough | proxy forwards encrypted bytes, cannot read HTTP |
| Health check | proxy probes backends, removes failing ones |
| Balancing | round robin, least connections, hash |
| X-Forwarded-For | header carrying the original client address |

```
  client --HTTPS--> [ proxy :443 ] --HTTP--> backend A :8080
                     |  cert+key     \--HTTP--> backend B :8080
                     |  decrypts here
                     +-- health check /healthz every 5s
         (TLS ends at the proxy; backend hop is clear unless re-encrypted)
```

502 Bad Gateway: proxy could not get a valid reply from the backend. 504
Gateway Timeout: backend answered too slowly. 503: no healthy backend or
overload. Learn these three by heart.

## Worked examples

Example 1: a minimal nginx reverse proxy with TLS termination.

```nginx
upstream app {
    server 127.0.0.1:8080;
    server 127.0.0.1:8081;
}
server {
    listen 443 ssl;
    server_name app.example.com;
    ssl_certificate     /etc/ssl/app.crt;
    ssl_certificate_key /etc/ssl/app.key;
    location / {
        proxy_pass http://app;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $remote_addr;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Example 2: validate before reload, never reload blind.

```bash
sudo nginx -t
sudo systemctl reload nginx
```

Example 3: inspect what the client really receives.

```bash
curl -vk https://app.example.com/ 2>&1 | sed -n 1,25p
openssl s_client -connect app.example.com:443 -servername app.example.com </dev/null 2>/dev/null | openssl x509 -noout -dates -subject
```

Example 4: tell proxy failure from backend failure.

```bash
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8080/healthz
curl -s -o /dev/null -w "%{http_code}\n" https://app.example.com/
sudo tail -n 20 /var/log/nginx/error.log
```

If the first is 200 and the second is 502, suspect the proxy to backend hop:
wrong port, SELinux blocking the connect, or a firewall rule.

Example 5: check socket ownership.

```bash
sudo ss -tlnp | grep -E ':(80|443|8080)'
```

## Mini-lab

1. In a lab VM install nginx and run a trivial backend:
   `python3 -m http.server 8080 --bind 127.0.0.1`.
2. Create a self-signed cert with `openssl req -x509 -newkey rsa:2048 -nodes
   -keyout app.key -out app.crt -days 7 -subj "/CN=lab.test"`.
3. Write a server block like Example 1 pointing at the backend. Run
   `nginx -t` and reload.
4. Request it with `curl -vk https://127.0.0.1/` and find the certificate
   subject and the HTTP status.
5. Stop the backend. Request again. Record the status code and the error log
   line. Restart the backend.
6. Say in one sentence where TLS ended and what an observer on the loopback
   backend hop could read.

## Decision guide / failure modes

| Symptom | Likely cause | First check |
|---------|--------------|-------------|
| 502 | backend down, wrong port, connect blocked | `ss -tlnp`, error.log |
| 504 | backend slow, timeout too low | upstream latency, `proxy_read_timeout` |
| Cert warning | expired, wrong SAN, missing chain | `openssl s_client`, full chain file |
| Backend sees proxy IP | no forwarded header handling | `X-Forwarded-For` config |
| Redirect loop | backend thinks it is HTTP | pass `X-Forwarded-Proto` |
| One node gets all traffic | sticky hash, failed health check | upstream status, check config |

Choose termination at the proxy when you need routing by path or host,
caching, WAF, or central certificate management. Choose passthrough when end-
to-end encryption is required and the proxy only needs SNI. Failure modes:
forgetting `nginx -t`, private key world-readable, certificate renewed on disk
but proxy never reloaded, and trusting `X-Forwarded-For` from the internet.
""",
    "exercise_guide": r"""Open `exercise.sh` and implement `tls_termination_means` so it prints one
hyphenated token that states what the proxy does to the client TLS session
when it terminates TLS. Use the vocabulary from the Core concepts table: all
lowercase, words joined by hyphens, no extra output. No network access is
needed. After it passes, build the mini-lab proxy and confirm with
`curl -vk` which hop is encrypted. In your notes, also write which of 502,
503, and 504 you would expect when the backend is stopped, and which log file
proves it. That short note is part of the exercise even though the test does
not check it.""",
    "exercise_examples": r"""Run from the exercise folder:

    source ./exercise.sh
    tls_termination_means

Expected single line of output:

    decrypt-at-proxy

Related lab checks (not graded):

    sudo nginx -t
    nginx: configuration file /etc/nginx/nginx.conf test is successful

    curl -sk -o /dev/null -w "%{http_code}\n" https://127.0.0.1/
    502        # when the backend on 8080 is stopped

Passthrough would instead leave the proxy unable to read the HTTP headers.""",
}

# ---------------------------------------------------------------------------
# 44 Backups, snapshots, restore drills
# ---------------------------------------------------------------------------
EXTRA[44] = {
    "body": r"""
## Why this matters

Everyone has backups until the day they need one. Disks fail, people run
`rm -rf` in the wrong directory, ransomware encrypts both the server and the
mounted share, and cloud accounts get deleted. The only question that matters
afterwards is: how much data did we lose, and how long were we down? Those are
your **RPO** and **RTO**, and they must be decided before the incident, tested
in a drill, and written down.

RPO (recovery point objective) is the maximum data-loss window: the longest
span of recent changes you accept losing. If you back up nightly, your RPO is
about 24 hours, whatever the slide deck says. RTO is how long recovery may
take. Untested backups are fiction.

## Core concepts

| Term | Meaning |
|------|---------|
| RPO | max data-loss window, set by backup frequency |
| RTO | max acceptable time to restore service |
| Snapshot | point-in-time copy, usually on the same storage system |
| Backup | independent copy on separate media or location |
| Full / incremental | whole copy vs only changes since last run |
| Retention | how many restore points you keep and for how long |
| 3-2-1 | 3 copies, 2 media types, 1 offsite |

```
  data ---> snapshot (fast, same array)      <- convenience, not safety
    |
    +-----> backup job --> repo on other host --> offsite copy
                 |                                   |
            encrypt + checksum                  immutable / versioned
   timeline:  |---- RPO ----|  last good copy -> failure
                              |------- RTO ------->| service back
```

A snapshot on the same disk array dies with the array. A backup that you
have never restored is a hope, not a control.

## Worked examples

Example 1: a simple file backup with rsync and hard-link snapshots.

```bash
SRC=/srv/app/data
DST=/backup/app
TS=$(date +%Y%m%d-%H%M)
rsync -a --delete --link-dest="$DST/latest" "$SRC/" "$DST/$TS/"
ln -sfn "$DST/$TS" "$DST/latest"
```

Unchanged files are hard links, so each run looks like a full copy but costs
only the changes.

Example 2: a tar archive with a checksum, ready to copy offsite.

```bash
tar -C /srv/app -czf /tmp/app-$(date +%F).tgz data
sha256sum /tmp/app-$(date +%F).tgz | tee /tmp/app-$(date +%F).tgz.sha256
```

Example 3: encrypt before it leaves the host.

```bash
gpg --symmetric --cipher-algo AES256 /tmp/app-2026-10-21.tgz
```

Store the passphrase or key separately from the backup. A backup you cannot
decrypt is no backup.

Example 4: dedup backup with restic (concept-level).

```bash
restic -r /backup/restic init
restic -r /backup/restic backup /srv/app/data
restic -r /backup/restic snapshots
restic -r /backup/restic check
```

Example 5: a restore drill into a scratch directory, then compare.

```bash
mkdir -p /tmp/restore-test
tar -C /tmp/restore-test -xzf /tmp/app-2026-10-21.tgz
diff -r /srv/app/data /tmp/restore-test/data && echo RESTORE_OK
```

## Mini-lab

1. Create `/tmp/lab/data` with ten small files.
2. Run Example 1 twice, modifying one file between runs. Use `ls -li` on a
   file in both snapshots to see shared inodes for unchanged files.
3. Create a tar archive plus a sha256 file. Corrupt a copy with
   `printf x >> copy.tgz` and show that `sha256sum -c` fails.
4. Delete the original data directory and restore from the backup.
5. Time the restore. Write down: this is my measured RTO for this dataset.
6. State your RPO given how often you ran the job. Write both numbers in a
   one-line runbook note.

## Decision guide / failure modes

| Situation | Choice |
|-----------|--------|
| Need to roll back a risky change in minutes | snapshot (then still back up) |
| Protect against disk, host, or site loss | backup to another host plus offsite |
| Database in use | dump or snapshot with consistency, not raw copy of live files |
| Very low RPO | frequent incrementals, WAL archiving, replication (not a backup) |
| Ransomware concern | immutable or write-once copy, separate credentials |

Failure modes: backups stored on the same disk; replication mistaken for
backup (it replicates the deletion too); no checksum or `restic check`; keys
lost; retention so short that corruption discovered on day 10 is already
overwritten; and never timing a restore so RTO is a guess. Schedule a restore
drill at least quarterly and record the result.
""",
    "exercise_guide": r"""Open `exercise.sh` and implement `rpo_means`. It must print one lowercase
token, with words joined by hyphens, that defines what RPO measures in the
lesson's own words. No file access and no tools are required. After the test
turns green, do the mini-lab restore drill and record two numbers in your
notes: your measured restore time (RTO) and the gap between backup runs
(your effective RPO). Finally explain in one sentence why a snapshot on the
same disk array does not satisfy a 3-2-1 plan. These notes are not graded but
are the point of the module.""",
    "exercise_examples": r"""Run from the exercise folder:

    source ./exercise.sh
    rpo_means

Expected single line of output:

    max-data-loss-window

Example reasoning (not graded):

    nightly backup at 02:00, failure at 17:00  -> up to 15h of data lost
    configured RPO is therefore 24h worst case

    restore of 10 files took 2s in the lab     -> measured RTO is 2s
    restore of 500 GB will not scale linearly; measure at realistic size""",
}

# ---------------------------------------------------------------------------
# 45 AI infra on Linux
# ---------------------------------------------------------------------------
EXTRA[45] = {
    "body": r"""
## Why this matters

AI serving looks exotic, but at 3am it is ordinary Linux trouble: a model
server that dies with "Too many open files", a loader that thrashes because
the dataset sits on a slow disk, a GPU process that gets OOM-killed because a
neighbor leaked host memory. The people who keep inference reliable know
limits, cgroups, systemd, and basic observability. GPU drivers and CUDA are
important, but they sit on top of the same kernel features you already study.

One knob bites first and most often: the open-file-descriptor limit,
`nofile`. A busy inference server holds sockets for every client, plus model
shards, tokenizer files, logs, and worker pipes. The default soft limit of
1024 is far too low, so the process fails under load, not at startup.

## Core concepts

| Area | What to know | Where to look |
|------|--------------|---------------|
| File descriptors | per-process cap (nofile) | `ulimit -n`, `LimitNOFILE=` |
| Memory | RAM, page cache, swap, cgroup limit | `free -h`, `MemoryMax=` |
| Disk | dataset and model weights read speed | `iostat -x 1`, `df -h` |
| GPU (host side) | driver, device nodes, utilization | `nvidia-smi`, `/dev/nvidia*` |
| Processes | one model server, N workers | `systemctl status`, `ps` |
| Isolation | cgroups, user, namespaces | `systemd-cgls`, `systemd-run` |

```
  clients --> proxy --> model server (systemd unit)
                          |  LimitNOFILE=65536   MemoryMax=48G
                          |  User=model          TasksMax=...
                          v
          page cache <-- weights/datasets on NVMe
                          |
                      GPU driver --> /dev/nvidia0 (utilization, memory)
   watch: nofile, RSS, page cache, disk wait, GPU mem, 5xx rate
```

## Worked examples

Example 1: see the limits a running server really has.

```bash
pid=$(pgrep -f model-server | head -1)
grep -E 'open files|processes' /proc/$pid/limits
ls /proc/$pid/fd | wc -l
```

Compare the count with the soft limit. If they are close, you are about to
fail.

Example 2: raise the limit for a systemd service, the correct way.

```ini
[Service]
User=model
LimitNOFILE=65536
MemoryMax=48G
TasksMax=4096
ExecStart=/opt/model/bin/server --port 8000
```

```bash
sudo systemctl daemon-reload
sudo systemctl restart model.service
systemctl show model.service -p LimitNOFILE
```

Editing `/etc/security/limits.conf` does not affect systemd services; use the
unit file or a drop-in.

Example 3: confirm dataset disk is not the bottleneck.

```bash
df -h /data
iostat -x 1 3
```

High `%util` with large `await` while the GPU idles means storage is feeding
the model too slowly.

Example 4: host-side GPU sanity.

```bash
nvidia-smi
ls -l /dev/nvidia*
journalctl -k | grep -i -E 'nvrm|xid' | tail
```

An Xid error in the kernel log points at driver or hardware, not your app.

Example 5: was it the OOM killer?

```bash
journalctl -k | grep -i 'out of memory'
systemctl status model.service | head
```

## Mini-lab

1. In a shell run `ulimit -n`, then `ulimit -Hn`. Note the soft and hard
   values.
2. Write a tiny script that opens many files and watch it fail at the soft
   limit: `python3 -c "f=[open('/dev/null') for _ in range(5000)]"`.
3. Run it again after `ulimit -n 10000` in the same shell.
4. Create a unit for a dummy server (`python3 -m http.server 8000`) with
   `LimitNOFILE=4096` and `MemoryMax=200M`. Start it.
5. Read `/proc/PID/limits` for its main process and confirm 4096.
6. Write the three metrics you would alert on for a model host.

## Decision guide / failure modes

| Symptom | Likely cause | First check |
|---------|--------------|-------------|
| "Too many open files" | low nofile | `/proc/PID/limits`, `LimitNOFILE` |
| Killed with no log | cgroup or global OOM | `journalctl -k`, `MemoryMax` |
| Slow start, idle GPU | slow disk or cold cache | `iostat -x`, warm the cache |
| GPU not found | driver mismatch, missing nodes | `nvidia-smi`, `dmesg` |
| Latency spikes | swap, CPU throttle, noisy neighbor | `vmstat 1`, `cpu.stat` |

Failure modes: raising `limits.conf` and expecting systemd to obey; running
the model server as root; unlimited memory so one leak takes down the host;
and no graceful drain, so deploys drop in-flight requests. Always measure the
real limit of the live process, not the one you think you set.
""",
    "exercise_guide": r"""Open `exercise.sh` and implement `inference_limit_knob`. It prints the name
of the one resource-limit knob, written exactly as the lowercase `ulimit`
resource name, that a busy inference server most commonly exhausts first
because it holds many sockets and files. Print only that word. The test does
not touch the system. After it passes, perform mini-lab steps 1 to 5 and keep
the output of `grep 'open files' /proc/PID/limits` in your notes. Then write
the systemd directive that raises the same limit for a service and say why
`limits.conf` alone does not change it for services.""",
    "exercise_examples": r"""Run from the exercise folder:

    source ./exercise.sh
    inference_limit_knob

Expected single line of output:

    nofile

Related lab checks (not graded):

    ulimit -n
    1024
    grep 'open files' /proc/self/limits
    Max open files            1024                 1048576              files

systemd directive for the same knob: LimitNOFILE=65536 inside [Service].""",
}

# ---------------------------------------------------------------------------
# 46 Prometheus node metrics
# ---------------------------------------------------------------------------
EXTRA[46] = {
    "body": r"""
## Why this matters

You cannot operate what you cannot see. Most Linux outages are slow ones:
a disk that fills over three days, memory that creeps, inodes that run out on
a log directory. Humans do not notice these; a metrics stack does. The common
open-source setup is `node_exporter` on each host, Prometheus scraping it,
Grafana drawing graphs, and Alertmanager paging someone. Knowing what to
alert on, and just as important what not to, keeps your pager useful.

A classic first alert is disk usage. A common starting threshold is 90
percent used on a data filesystem, with a lower warning earlier. At 90 you
still have time to act; at 100 databases stop and logs fail.

## Core concepts

| Idea | Meaning |
|------|---------|
| Exporter | process that exposes metrics over HTTP (`:9100/metrics`) |
| Scrape | Prometheus pulls metrics on an interval |
| Counter | only goes up (`node_network_receive_bytes_total`) |
| Gauge | goes up and down (`node_memory_MemAvailable_bytes`) |
| Label | key/value dimension (`mountpoint="/"`) |
| Cardinality | number of unique label combinations; keep it low |
| USE method | Utilization, Saturation, Errors for resources |
| RED method | Rate, Errors, Duration for services |

```
  host: node_exporter :9100 --metrics--+
  host: node_exporter :9100 --metrics--+--> Prometheus (scrape 15s, TSDB)
  host: node_exporter :9100 --metrics--+        |
                                                +--> Alertmanager --> pager
                                                +--> Grafana dashboards
```

Alert on symptoms users feel or resources about to run out, not on every
spike. An alert should be actionable, and have a clear owner.

## Worked examples

Example 1: look at raw exporter output.

```bash
curl -s localhost:9100/metrics | grep -E '^node_filesystem_(avail|size)_bytes' | head
curl -s localhost:9100/metrics | grep node_load1
```

Example 2: a Prometheus scrape config.

```yaml
scrape_configs:
  - job_name: node
    scrape_interval: 15s
    static_configs:
      - targets: ['10.0.0.11:9100', '10.0.0.12:9100']
```

Example 3: disk percent used, and the alert at 90.

```yaml
groups:
- name: host
  rules:
  - alert: DiskAlmostFull
    expr: (1 - node_filesystem_avail_bytes{fstype!~"tmpfs|overlay"} / node_filesystem_size_bytes{fstype!~"tmpfs|overlay"}) * 100 > 90
    for: 10m
    labels: {severity: page}
    annotations:
      summary: "{{ $labels.instance }} {{ $labels.mountpoint }} over 90 percent"
```

The `for: 10m` prevents flapping. Excluding tmpfs and overlay avoids noise.

Example 4: inodes and memory.

```promql
node_filesystem_files_free / node_filesystem_files < 0.10
node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes < 0.10
```

Example 5: predict instead of react.

```promql
predict_linear(node_filesystem_avail_bytes{mountpoint="/"}[6h], 24*3600) < 0
```

This fires when the trend says the disk will be full within a day, giving you
time to fix it during working hours.

## Mini-lab

1. Install `prometheus-node-exporter` (or download node_exporter) in a lab VM
   and start it.
2. Run `curl -s localhost:9100/metrics | wc -l` and find three metrics you
   recognise from `free`, `df`, and `uptime`.
3. Run `df -h /` and compute the percent used by hand from the exporter's
   avail and size values.
4. Fill a scratch loopback filesystem or use `fallocate -l 1G /tmp/big` and
   watch the metric change after the next scrape.
5. Write an alert rule file with the 90 percent rule and validate it:
   `promtool check rules rules.yml`.
6. List one label you must never put on a metric, such as a user id or
   request id, and say why.

## Decision guide / failure modes

| Question | Choice |
|----------|--------|
| Page a human? | only if user impact is happening or imminent |
| Ticket instead? | slow trends, 80 percent disk, cert in 14 days |
| Which method? | USE for hosts and disks, RED for services |
| Threshold or prediction? | prediction for fills, threshold for hard caps |
| New label? | only if cardinality is bounded and small |

Failure modes: alerting on CPU above 80 percent with no context; no `for:`
clause, so every blip pages; high-cardinality labels such as `user_id` that
blow up the TSDB; scraping only the app and forgetting the host; and alerts
without a runbook link. Test alert rules with `promtool` and trigger them once
on purpose so you know the route to the pager works.
""",
    "exercise_guide": r"""Open `exercise.sh` and implement `alert_on_disk_pct`. It prints the numeric
percent-used threshold that the lesson uses as the example disk alert, as a
bare integer with no percent sign and no text. No metrics stack is required for
the test. After it passes, install node_exporter in a lab VM, compute the
percent used on `/` from the raw `node_filesystem_*` metrics, and compare it
with `df`. Write the alert expression from the lesson in your own words, and
note why `for: 10m` and a tmpfs exclusion are part of a good rule. Also note
one warning-level threshold that should fire earlier and go to a ticket.""",
    "exercise_examples": r"""Run from the exercise folder:

    source ./exercise.sh
    alert_on_disk_pct

Expected single line of output:

    90

Related lab check (not graded):

    df -P / | awk 'NR==2 {print $5}'
    42%

    curl -s localhost:9100/metrics | grep 'node_filesystem_avail_bytes{.*mountpoint="/"'
    node_filesystem_avail_bytes{device="/dev/sda1",fstype="ext4",mountpoint="/"} 3.1e+10

percent used = (1 - avail/size) * 100 should match df within a point or two.""",
}

# ---------------------------------------------------------------------------
# 47 Git on Linux servers
# ---------------------------------------------------------------------------
EXTRA[47] = {
    "body": r"""
## Why this matters

Git is how code reaches servers, but "git on the server" can mean wildly
different things. At one extreme, an engineer SSHs into production, runs
`git pull` in `/opt/app`, edits a config file in place, and leaves the
checkout dirty. Six months later nobody knows what is actually running. At the
other extreme, CI builds a versioned artifact once, and servers receive that
exact artifact and nothing else. The second approach makes rollbacks trivial
and incidents explainable.

Prefer an immutable artifact: a tarball, package, or container image built
once from a tag, checksummed, and deployed unchanged. Git remains the source
of truth for code, while the artifact is the unit of deployment.

## Core concepts

| Concept | Meaning |
|---------|---------|
| Deploy key | SSH key with read-only access to one repo |
| Tag | immutable name for a commit, such as `v1.4.2` |
| Artifact | built output, versioned and checksummed |
| Dirty tree | local modifications that differ from the commit |
| Hook | script git runs on events (`pre-commit`, `post-receive`) |
| Bare repo | repo without a working tree, used as a remote |
| Rollback | redeploy previous artifact by version |

```
  dev --> git push --> CI builds --> artifact app-1.4.2.tgz (sha256)
                                      |
                       registry / artifact store
                                      |
         server: fetch version -> verify checksum -> unpack to
         /opt/app/releases/1.4.2 -> symlink current -> restart
         rollback = point `current` at releases/1.4.1
```

## Worked examples

Example 1: check what a server checkout really is.

```bash
cd /opt/app
git status --short
git describe --tags --always
git diff --stat
```

Any output from `git status --short` means the running code differs from any
commit. That is a finding worth recording.

Example 2: read-only deploy key.

```bash
ssh-keygen -t ed25519 -f ~/.ssh/deploy_app -C "deploy-app-ro" -N ""
# add the .pub as a read-only deploy key in the repo settings
GIT_SSH_COMMAND="ssh -i ~/.ssh/deploy_app -o IdentitiesOnly=yes" \
  git ls-remote git@example.com:org/app.git
```

Example 3: release directories with an atomic symlink switch.

```bash
REL=/opt/app/releases/1.4.2
sudo mkdir -p "$REL"
sudo tar -xzf app-1.4.2.tgz -C "$REL"
sudo ln -sfn "$REL" /opt/app/current
sudo systemctl restart app.service
```

Example 4: verify before deploying.

```bash
sha256sum -c app-1.4.2.tgz.sha256
git verify-tag v1.4.2
```

Example 5: a minimal server-side hook in a bare repo, used only to trigger CI
or notify, not to hot-edit production.

```bash
#!/usr/bin/env bash
# hooks/post-receive
while read old new ref; do
  echo "$(date -Is) $ref $new" >> /var/log/git-push.log
done
```

## Mini-lab

1. Create a repo in `/tmp/lab/app`, commit a file, and tag it `v1`.
2. Build an artifact with `git archive --format=tar.gz -o app-v1.tgz v1`.
3. Compute `sha256sum app-v1.tgz` and save it.
4. Unpack into `releases/v1`, link `current`, and list the layout.
5. Make a second tag `v2`, repeat, switch the symlink, then switch it back.
6. In `releases/v2`, notice there is no `.git` directory; explain why that is
   an advantage on a server.

## Decision guide / failure modes

| Situation | Prefer |
|-----------|--------|
| Production deploy | immutable artifact from a tag |
| Server needs source for debugging | read-only clone in a separate path |
| Secrets in the repo | remove, rotate, use a secret store |
| Need to pull from private repo | deploy key, read-only, one per repo |
| Hotfix at 3am | still build an artifact, even if the pipeline is shortened |

Failure modes: using `git pull` on a branch (not a tag) so the version moves
without notice; storing a personal SSH key on a server; write-enabled deploy
keys; editing files in the checkout; deploying `.git` and secrets into a
web-served directory; and not recording the version that is live. Keep a
`VERSION` file or use `git describe` output baked into the artifact so
`curl /version` answers "what is running".
""",
    "exercise_guide": r"""Open `exercise.sh` and implement `prefer_deploy_artifact`. It prints a short
hyphenated token that names the kind of deployable unit the lesson recommends
over pulling a mutable branch on a server. Lowercase, one line, nothing else.
After it passes, do the mini-lab and capture the output of `ls -l
/tmp/lab/app/releases` and the `sha256sum` line. In notes, write the rollback
steps as exactly two commands, and explain why a dirty `git status --short` on
a production host is an incident finding, not a normal state.""",
    "exercise_examples": r"""Run from the exercise folder:

    source ./exercise.sh
    prefer_deploy_artifact

Expected single line of output:

    immutable-artifact

Related lab check (not graded):

    git archive --format=tar.gz -o app-v1.tgz v1
    sha256sum app-v1.tgz
    9f2c...  app-v1.tgz
    ls -l /opt/app
    current -> /opt/app/releases/1.4.2

Rollback shape: ln -sfn /opt/app/releases/1.4.1 /opt/app/current, then
systemctl restart app.service.""",
}

# ---------------------------------------------------------------------------
# 48 SELinux / AppArmor
# ---------------------------------------------------------------------------
EXTRA[48] = {
    "body": r"""
## Why this matters

Classic Unix permissions (user, group, other) answer "who owns this file".
They do not answer "should a web server ever read `/home` or open a shell".
Mandatory Access Control (MAC) adds a second, policy-driven layer that even
root-owned processes cannot bypass. When a web app is compromised, MAC is
often what stops the attacker at one directory instead of the whole host.

It also causes a famous class of mystery failures: permissions look right,
the service is running, yet "Permission denied" appears. If you do not know
MAC exists, you lose hours. If you answer with `setenforce 0` and move on,
you lose the protection.

Which one you meet depends on the distro family: RHEL, Fedora, Rocky, and
Alma use SELinux; Ubuntu, Debian-family, and SUSE use AppArmor (SUSE moved to
SELinux in recent versions, so check).

## Core concepts

| Item | SELinux | AppArmor |
|------|---------|----------|
| Typical distros | RHEL, Fedora, Alma | Ubuntu, Debian |
| Model | labels on files and processes | path-based profiles |
| Status | `getenforce`, `sestatus` | `aa-status` |
| Modes | enforcing, permissive, disabled | enforce, complain |
| Denial log | `ausearch -m AVC`, audit.log | `journalctl`, `dmesg` |
| Fix files | `restorecon`, `semanage fcontext` | edit profile, `aa-logprof` |
| Fix toggles | `setsebool -P` | profile abstractions |

```
  process (label httpd_t) --wants--> file (label user_home_t)
                |                         |
                +----> kernel policy check --> ALLOW / DENY
                          (after normal chmod/chown checks)
  deny -> audit record (AVC) -> you read it, fix label or policy,
          NOT disable the whole system
```

Rule: chmod passes first, then MAC is consulted. Both must allow.

## Worked examples

Example 1: which system is this host using?

```bash
getenforce 2>/dev/null || echo "no selinux"
sudo aa-status 2>/dev/null | head -3 || echo "no apparmor"
cat /etc/os-release | grep -E '^(ID|ID_LIKE)='
```

Example 2: SELinux, web server cannot read content from a custom path.

```bash
ls -Z /srv/site/index.html
# unconfined_u:object_r:var_t:s0   <- wrong type for web content
sudo semanage fcontext -a -t httpd_sys_content_t "/srv/site(/.*)?"
sudo restorecon -Rv /srv/site
```

Example 3: SELinux, read the denial and use a boolean.

```bash
sudo ausearch -m AVC -ts recent | tail -5
sudo setsebool -P httpd_can_network_connect on
```

Example 4: AppArmor, find and loosen one profile temporarily.

```bash
sudo aa-status
sudo journalctl -k | grep -i apparmor | tail
sudo aa-complain /usr/sbin/mysqld
# test, collect denials, update the profile, then:
sudo aa-enforce /usr/sbin/mysqld
```

Example 5: testing with permissive mode, honestly.

```bash
sudo setenforce 0     # temporary, lasts until reboot
# reproduce failure; if it vanishes, it IS a MAC denial
sudo setenforce 1     # put it back immediately
```

This is a diagnostic, not a fix.

## Mini-lab

1. Identify the distro family with `/etc/os-release` and decide which MAC
   system you should expect.
2. Run `getenforce` or `aa-status`. Record the mode.
3. On SELinux hosts: `ls -Z /var/www /etc/passwd` and compare the type
   fields. On AppArmor hosts: list loaded profiles and count enforced ones.
4. Make a file in `/tmp/site` and compare `ls -Z` before and after
   `restorecon` (SELinux) or note its path (AppArmor).
5. Find where denials are logged on your host and trigger one safely, if you
   can, by running a confined binary against an unexpected path.
6. Write the three-line playbook: read denial, find smallest fix, re-test in
   enforcing mode.

## Decision guide / failure modes

| Symptom | Likely cause | Right action |
|---------|--------------|--------------|
| Perms fine, access denied | MAC label or profile | read AVC or audit log |
| Moved web root | wrong file context | `semanage fcontext` + `restorecon` |
| App must connect outbound | SELinux boolean off | `setsebool -P name on` |
| Need new path for daemon | AppArmor profile lacks rule | edit profile, reload |
| "Just disable it" | pressure | use permissive per-domain, fix, re-enable |

Failure modes: `setenforce 0` left in place and `SELINUX=disabled` in config;
files copied with `cp` instead of `cp --preserve=context` or relabeled;
`mv` keeping the old label; giving up on AppArmor and unloading all profiles.
Fix the smallest thing, in enforcing mode.
""",
    "exercise_guide": r"""Open `exercise.sh` and implement `mac_for_distro`. It takes one argument,
a distro family name, and prints the Mandatory Access Control system that
family uses by default. Handle at least `rhel` and `ubuntu`. Output exactly
one lowercase word per call: no spaces, no extra text. Think about the lesson's
distro table and keep the function a simple case statement. After the tests
pass, run the status command appropriate to your lab VM and record the mode in
your notes. Also write one sentence on why `setenforce 0` is a diagnostic
step and not a fix.""",
    "exercise_examples": r"""Run from the exercise folder:

    source ./exercise.sh
    mac_for_distro rhel
    mac_for_distro ubuntu

Expected output, one line each:

    selinux
    apparmor

Related lab checks (not graded):

    getenforce
    Enforcing
    sudo aa-status | head -2
    apparmor module is loaded.

Only one of these two commands is normally meaningful on a given host.""",
}

# ---------------------------------------------------------------------------
# 49 nftables firewall
# ---------------------------------------------------------------------------
EXTRA[49] = {
    "body": r"""
## Why this matters

A firewall decides which packets reach your services. A good one makes a
compromised app far less useful to an attacker; a bad one locks you out of
your own server at the worst moment. nftables is the modern Linux packet
filter in the kernel. Tools like ufw and firewalld are front ends that
generate nftables (or iptables-nft) rules, so the mental model carries over.

The principle that matters most is the default policy for inbound traffic:
**deny**. You list what is allowed (SSH, HTTPS) and everything else is
dropped. The opposite, default allow with a few blocks, fails open: every new
service you start is instantly exposed.

## Core concepts

| Term | Meaning |
|------|---------|
| Table | container for chains, tied to a family (`inet`, `ip`, `ip6`) |
| Chain | ordered list of rules at a hook (`input`, `forward`, `output`) |
| Rule | match plus verdict (`accept`, `drop`, `reject`) |
| Policy | verdict when no rule matches; set to `drop` for input |
| State | `ct state established,related` lets replies back in |
| Set | named collection of addresses or ports |
| Counter / log | observe what a rule matches |

```
  packet in --> [ prerouting ] --> routing decision
                                      |-> local? --> [ input chain ]  --> socket
                                      |             policy drop
                                      |-> other? --> [ forward chain ]
  app out ----> [ output chain ] ---> network
  input order: lo accept -> established accept -> ssh accept -> https accept -> (drop)
```

Rules evaluate top to bottom, first terminal verdict wins. Order matters,
especially "established" and loopback rules at the top.

## Worked examples

Example 1: a minimal default-deny host firewall.

```bash
# /etc/nftables.conf
table inet filter {
  chain input {
    type filter hook input priority 0; policy drop;
    iif lo accept
    ct state established,related accept
    ct state invalid drop
    ip protocol icmp accept
    ip6 nexthdr icmpv6 accept
    tcp dport 22 accept
    tcp dport { 80, 443 } accept
  }
  chain forward { type filter hook forward priority 0; policy drop; }
  chain output  { type filter hook output priority 0; policy accept; }
}
```

Example 2: load safely and inspect.

```bash
sudo nft -c -f /etc/nftables.conf     # syntax check only
sudo nft -f /etc/nftables.conf
sudo nft list ruleset
```

Example 3: the same intent with ufw.

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

Example 4: add a counter and a rate-limited log to see drops.

```bash
sudo nft add rule inet filter input limit rate 5/minute log prefix "nft-drop: " counter drop
journalctl -k | grep nft-drop | tail
```

Example 5: test from outside, not from the box itself.

```bash
nc -vz -w 2 server.example.com 22
nc -vz -w 2 server.example.com 5432
```

Open port 22 should connect; 5432 should time out (dropped) or be refused.

## Mini-lab

1. In a VM with console access, take a snapshot first.
2. Run `sudo nft list ruleset` and save it to a file as a baseline.
3. Install the Example 1 rules, check with `nft -c`, then load.
4. Keep a second SSH session open. Verify you can open a new one.
5. Start `python3 -m http.server 8080` and test from another machine; the
   port should not be reachable because only 22, 80, and 443 are allowed.
6. Add `tcp dport 8080 accept`, test again, and then remove it.
7. Safety net: schedule `sleep 120; sudo nft flush ruleset` in another
   terminal before experimenting remotely, then cancel it when satisfied.

## Decision guide / failure modes

| Situation | Choice |
|-----------|--------|
| Single server, simple needs | ufw or firewalld |
| Complex sets, NAT, custom logic | nftables directly |
| Container host | know that Docker adds its own rules; check `nft list ruleset` |
| Remote change | schedule a revert or use a console |
| Debugging drops | counters and rate-limited log |

Failure modes: policy accept on input; forgetting the established rule so
replies die; no loopback rule so local services break; applying rules over
SSH with no rollback; mixing ufw, firewalld, and raw nft that overwrite each
other; and never persisting rules so a reboot removes them (or loads
permissive defaults). Verify after reboot.
""",
    "exercise_guide": r"""Open `exercise.sh` and implement `firewall_default_inbound`. It prints the
single lowercase word naming the default inbound policy the lesson recommends
for a server firewall. Nothing else is printed and nothing on the system is
touched; the test is a recall check, not a rule load. After it passes, work
the mini-lab only inside a VM snapshot with console access. Record the output
of `nft list ruleset` before and after your change in your notes, and write the
exact three rules that must appear above any `drop` so you do not lose SSH or
break replies. Never test an unfamiliar ruleset on a remote-only machine.""",
    "exercise_examples": r"""Run from the exercise folder:

    source ./exercise.sh
    firewall_default_inbound

Expected single line of output:

    deny

Related lab checks (not graded):

    sudo nft list chain inet filter input | head -3
    type filter hook input priority filter; policy drop;

    sudo ufw status verbose | grep Default
    Default: deny (incoming), allow (outgoing), disabled (routed)

In nftables the word is spelled `drop`; the concept is default deny.""",
}

# ---------------------------------------------------------------------------
# 50 systemd hardening
# ---------------------------------------------------------------------------
EXTRA[50] = {
    "body": r"""
## Why this matters

Every network service is one bug away from being controlled by someone else.
When that happens, the question is how much damage the compromised process can
do. A service running as root with full filesystem access can read your SSH
keys, install a backdoor, and pivot to the next host. The same bug in a
service that is sandboxed by systemd yields a process that can barely touch
anything. Hardening directives cost a few lines in a unit file and give
defence in depth without changing the application.

The single most valuable line to remember is `NoNewPrivileges=true`. It
prevents the service and all its children from gaining more privileges via
setuid binaries, file capabilities, or similar tricks. Even if an attacker runs
`sudo` or a setuid helper, escalation fails.

## Core concepts

| Directive | Effect |
|-----------|--------|
| `User=` / `DynamicUser=yes` | run as unprivileged account, not root |
| `NoNewPrivileges=true` | block privilege gain through exec |
| `PrivateTmp=true` | private `/tmp` and `/var/tmp` for the unit |
| `ProtectSystem=strict` | whole file system read-only except listed paths |
| `ProtectHome=true` | `/home`, `/root` hidden |
| `ReadWritePaths=` | explicit writable exceptions |
| `CapabilityBoundingSet=` | limit Linux capabilities |
| `PrivateDevices=true` | no access to real devices |
| `SystemCallFilter=` | allow list of syscalls |
| `RestrictAddressFamilies=` | limit socket types |

```
   +---------------------- unit sandbox ----------------------+
   | User=app   NoNewPrivileges=true   PrivateTmp=true        |
   |   +------ view of filesystem ------+                     |
   |   | / read-only (ProtectSystem)    |   writable:         |
   |   | /home hidden (ProtectHome)     |   ReadWritePaths=   |
   |   +--------------------------------+   /var/lib/app      |
   | CapabilityBoundingSet= (empty)  SystemCallFilter=@system-service |
   +----------------------------------------------------------+
   systemd-analyze security app.service  -> exposure score
```

## Worked examples

Example 1: a hardened unit for a small web app.

```ini
[Unit]
Description=Example app
After=network.target

[Service]
User=myapp
Group=myapp
ExecStart=/opt/myapp/bin/server --port 8080
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/var/lib/myapp
PrivateDevices=true
ProtectKernelTunables=true
ProtectControlGroups=true
RestrictAddressFamilies=AF_INET AF_INET6 AF_UNIX
CapabilityBoundingSet=
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Example 2: measure exposure and read the report.

```bash
systemd-analyze security myapp.service | head -20
systemd-analyze security myapp.service --no-pager | tail -3
```

Lower exposure is better; treat the score as guidance, not a goal in itself.

Example 3: a drop-in instead of editing the vendor unit.

```bash
sudo systemctl edit nginx.service
# in the editor:
# [Service]
# NoNewPrivileges=true
# ProtectHome=true
sudo systemctl daemon-reload && sudo systemctl restart nginx
```

Example 4: find why a hardened service fails, e.g. it cannot write a file.

```bash
journalctl -u myapp.service -n 30 --no-pager
sudo systemd-run --pty -p ProtectSystem=strict -p ReadWritePaths=/var/lib/myapp bash
```

A "Read-only file system" error means a needed path is missing from
`ReadWritePaths=`.

Example 5: confirm the setting is live.

```bash
systemctl show myapp.service -p NoNewPrivileges -p ProtectSystem -p User
```

## Mini-lab

1. Create a user `myapp` and a unit running `python3 -m http.server 8080`
   from `/srv/site`.
2. Run `systemd-analyze security myapp.service` and note the score.
3. Add `NoNewPrivileges=true`, `PrivateTmp=true`, `ProtectHome=true`.
   Re-run the analysis; compare.
4. Add `ProtectSystem=strict` and see what breaks. Fix it with
   `ReadWritePaths=` only for what the app writes.
5. Run `ls /tmp` from inside the service via a drop-in test command to see
   the private tmp.
6. Record each directive and the specific attack it blunts.

## Decision guide / failure modes

| Need | Directive |
|------|-----------|
| Cannot become root again | `NoNewPrivileges=true` |
| Stop reading user data | `ProtectHome=true` |
| Limit write damage | `ProtectSystem=strict` + `ReadWritePaths=` |
| No raw sockets or exotic nets | `RestrictAddressFamilies=` |
| Bind port below 1024 without root | `AmbientCapabilities=CAP_NET_BIND_SERVICE` |

Failure modes: applying everything at once so nothing works and nobody knows
which line broke it; `ProtectSystem=strict` without testing writable paths;
the app genuinely needing setuid (some mail daemons), in which case record
the exception; relying on the analyze score instead of reading directives;
and skipping a restart test after reboot. Add one directive at a time.
""",
    "exercise_guide": r"""Open `exercise.sh` and implement `nonewprivileges_directive`. It prints the
exact systemd unit-file line, including the directive name, an equals sign, and
the value, that stops a service and its children from gaining privileges
through setuid or capabilities. Case matters because systemd directives are
case sensitive. Print one line, nothing else. After it passes, apply the
directive to a throwaway unit in your lab VM and verify with
`systemctl show UNIT -p NoNewPrivileges`. Record the before and after exposure
from `systemd-analyze security` and list one thing that stopped working when
you added `ProtectSystem=strict`.""",
    "exercise_examples": r"""Run from the exercise folder:

    source ./exercise.sh
    nonewprivileges_directive

Expected single line of output:

    NoNewPrivileges=true

Related lab check (not graded):

    systemctl show myapp.service -p NoNewPrivileges
    NoNewPrivileges=yes

    systemd-analyze security myapp.service | tail -1
    -> Overall exposure level for myapp.service: 6.9 MEDIUM

systemctl show prints yes for the boolean you wrote as true.""",
}

# ---------------------------------------------------------------------------
# 51 Lab VM practice
# ---------------------------------------------------------------------------
EXTRA[51] = {
    "body": r"""
## Why this matters

Linux skill comes from breaking things on purpose and fixing them. But the
exercises that teach the most, such as editing fstab, changing firewall rules,
resizing disks, and breaking SSH, are exactly the ones that can leave a machine
unbootable or unreachable. If you only have one machine, you will avoid those
exercises and plateau. A lab that you can reset in minutes removes the fear and
makes you faster at real incidents.

The safety tool is the **snapshot**. Take one before every risky experiment,
and revert when you finish or fail. Snapshots turn "I broke it" from a
catastrophe into a two-minute reset.

## Core concepts

| Concept | Meaning |
|---------|---------|
| Hypervisor | software that runs VMs (UTM, VirtualBox, KVM, cloud) |
| Snapshot | frozen state of the VM disk (and optionally RAM) |
| Base image | clean installed VM you clone from |
| Host-only / NAT | virtual networks that keep the lab isolated |
| Console | out-of-band access when SSH or networking is broken |
| Break-glass VM | a VM you are explicitly allowed to destroy |
| Lab notes | a log of IPs, users, commands, and failures |

```
  your laptop (host)
   |
   +-- hypervisor
         |-- vm-ubuntu (snapshot: clean, pre-firewall, pre-disk)
         |-- vm-alpine (contrast: musl, apk, OpenRC)
         |-- vm-break  (disposable: broken boot, bad fstab)
   network: NAT for updates + host-only for lab-to-lab traffic
   rule: never put prod credentials or real data in any lab VM
```

## Worked examples

Example 1: a naming and notes convention.

```text
lab-ubuntu   192.168.56.10  user: student   key: ~/.ssh/lab_ed25519
lab-alpine   192.168.56.11  user: student   key: ~/.ssh/lab_ed25519
lab-break    192.168.56.12  user: student   (disposable)
```

Keep this in a text file in your notes repository.

Example 2: snapshot workflow with VirtualBox command line.

```bash
VBoxManage snapshot lab-ubuntu take clean-install --description "fresh"
VBoxManage snapshot lab-ubuntu list
# ...break things...
VBoxManage controlvm lab-ubuntu poweroff
VBoxManage snapshot lab-ubuntu restore clean-install
```

UTM, VMware, Proxmox, and cloud providers have equivalent snapshot features
in their UI or CLI.

Example 3: a separate key just for the lab.

```bash
ssh-keygen -t ed25519 -f ~/.ssh/lab_ed25519 -C "lab-only" -N ""
ssh-copy-id -i ~/.ssh/lab_ed25519.pub student@192.168.56.10
ssh -i ~/.ssh/lab_ed25519 student@192.168.56.10 hostname
```

Example 4: lightly automate setup so a rebuild is cheap.

```bash
#!/usr/bin/env bash
set -euo pipefail
sudo apt-get update
sudo apt-get install -y curl git jq dnsutils tcpdump nginx
sudo useradd -m -s /bin/bash practice || true
echo "lab provisioned $(date -Is)" | sudo tee /etc/motd
```

Example 5: a quick "what did I change" habit.

```bash
history | tail -50 > ~/notes/session-$(date +%F).txt
sudo cp -a /etc /root/etc-backup-$(date +%F)
```

## Mini-lab

1. Create or pick a VM and install Ubuntu Server LTS.
2. Create a snapshot named `clean-install`.
3. Break something: add a bogus line to `/etc/fstab` and reboot, or flush
   firewall rules wrongly. Observe the symptom.
4. Use the hypervisor console, not SSH, to recover or to restore.
5. Restore the snapshot and confirm the problem is gone.
6. Add a second snapshot, `pre-firewall`, before the nftables module.
7. Write your lab inventory (names, IPs, users, snapshots) in a notes file.

## Decision guide / failure modes

| Situation | Choice |
|-----------|--------|
| Risky disk, boot, or firewall exercise | snapshot first |
| Want to compare distro behavior | second VM, different family |
| Need to test destructive scripts | the break-glass VM only |
| Need real services reachable | host-only network plus forwarding |
| Forgot to snapshot | rebuild from base image, then automate |

Failure modes: practicing firewall rules on your only machine without a
console; having no snapshots; snapshots piling up until the disk is full;
copying real production keys, tokens, or data into the lab; keeping a lab VM
exposed to the internet with a weak password; and not writing down what you
learned. Snapshots are not backups of valuable data, they are undo buttons.
""",
    "exercise_guide": r"""Open `exercise.sh` and implement `lab_safety_tool`. It prints the single
lowercase word naming the feature the lesson says to use before every risky
lab experiment so you can return to a known good state quickly. The test is a
recall check and does not touch a hypervisor. After it passes, do the mini-lab
for real: create a VM, take a snapshot, break `/etc/fstab` on purpose, recover
through the console, and restore. Write down the commands or UI steps you used
and the time the reset took. Note one rule you will follow about credentials
in the lab.""",
    "exercise_examples": r"""Run from the exercise folder:

    source ./exercise.sh
    lab_safety_tool

Expected single line of output:

    snapshots

Related lab check (not graded):

    VBoxManage snapshot lab-ubuntu list
    Name: clean-install (UUID: 6c1e...) *
    Name: pre-firewall (UUID: 02ab...)

A good habit is naming each snapshot after the module it protects.""",
}

# ---------------------------------------------------------------------------
# 52 Interview and oncall drills
# ---------------------------------------------------------------------------
EXTRA[52] = {
    "body": r"""
## Why this matters

Interviews and real incidents test the same thing: can you stay structured
when the situation is vague and urgent? Someone says "the site is slow" and
looks at you. Weak responders jump to a favorite theory, change three things,
and cannot say which one mattered. Strong responders spend the first ten
minutes on a repeatable routine: **define the scope, gather evidence**, and
only then pick a hypothesis. The routine is the skill, and you can practice it.

The first ten minutes are: define the problem and its scope, gather evidence,
communicate. One compact way to remember it is define-scope-gather-evidence.
Fixing comes after you know what is broken and for whom.

## Core concepts

| Step | Question | Example |
|------|----------|---------|
| Define | what exactly is failing? what is expected? | "login returns 500 since 14:05" |
| Scope | who and what is affected? | one region, all users, one host |
| Evidence | what do logs, metrics, and state say? | error rate, load, disk, DNS |
| Hypothesize | what single cause fits all evidence? | full disk on db host |
| Change | smallest reversible action | clear logs, restart one unit |
| Verify | did the symptom end, for everyone? | health check, user report |
| Communicate | status, owner, next update time | message every 15 minutes |

```
  alert/report
      |
      v
  DEFINE (symptom, start time, expected)
      |
      v
  SCOPE (who? where? since when? what changed?)
      |
      v
  EVIDENCE (uptime, df, free, ss, journalctl, metrics)
      |
      v
  hypothesis -> smallest fix -> VERIFY -> write down -> prevent
        ^                          |
        +---- not fixed? back to evidence, do not guess
```

## Worked examples

Example 1: "The site is slow." First ten minutes at the shell.

```bash
uptime                      # load vs CPU count
nproc
free -h                     # memory pressure, swap use
df -h; df -i                # space and inodes
vmstat 1 5                  # run queue, swap, io wait
ss -s                       # socket totals
sudo journalctl -p err -n 30 --no-pager
```

Say aloud what each result rules in or out.

Example 2: "Disk full at 2am."

```bash
df -h
sudo du -xh / --max-depth=2 2>/dev/null | sort -h | tail
sudo lsof +L1 | head        # deleted files still held open
```

Deleted-but-open files explain "df says full, du says not".

Example 3: "TLS expired."

```bash
echo | openssl s_client -connect example.com:443 -servername example.com 2>/dev/null | openssl x509 -noout -enddate
```

Example 4: "SSH refused suddenly."

```bash
nc -vz host 22
sudo systemctl status ssh
sudo ss -tlnp | grep :22
sudo nft list ruleset | grep -n 22
```

Example 5: a handoff note template.

```text
Status: mitigated at 02:40, monitoring
Impact: checkout errors, ~12 min, 8 percent of requests
Evidence: db disk 100 percent, error "no space left"
Action: rotated logs, freed 6 GB, restarted writer
Next: root cause for log growth, owner: ana, due Friday
```

## Mini-lab

1. Pick one scenario from the examples. Set a 10-minute timer.
2. Write the problem statement in one sentence before touching a command.
3. List three scope questions you would ask a stakeholder.
4. Run only read-only commands and paste the output into notes.
5. State one hypothesis and the single command that would disprove it.
6. Practice a status update: what we know, what we are doing, next update
   time. Say it out loud in under 30 seconds.
7. Swap with a friend and break each other's lab VM with a hidden fault.

## Decision guide / failure modes

| Situation | Move |
|-----------|------|
| No idea where to start | define scope, run the baseline commands |
| Two plausible causes | pick the check that separates them cheaply |
| Pressure to restart | capture evidence first, then restart |
| Fix applied | verify from the user's point of view |
| Incident over | note timeline, cause, prevention |

Failure modes: exotic theories before disk, DNS, and memory; silence while
working; changing multiple things at once; declaring victory with no
verification; and no notes, so the next shift repeats your work. Score
yourself on structure, evidence, communication, and verification.
""",
    "exercise_guide": r"""Open `exercise.sh` and implement `incident_first_10m`. It prints a single
hyphenated token that summarizes, in three ordered verbs or nouns, what to do
in the first ten minutes of an incident before proposing a fix. Use lowercase
and hyphens only, one line, no spaces. After it passes, run a timed drill from
the lesson: choose a scenario, write the one-sentence problem, list scope
questions, and run only read-only commands. Save the transcript and a
handoff note in the format shown in Example 5. Rate yourself from 1 to 5 on
structure, evidence, communication, and verification.""",
    "exercise_examples": r"""Run from the exercise folder:

    source ./exercise.sh
    incident_first_10m

Expected single line of output:

    define-scope-gather-evidence

Related drill output (not graded), a good first-minute transcript:

    $ uptime
     02:11:05 up 41 days, load average: 9.12, 8.80, 7.40
    $ nproc
    4

Load of 9 on 4 CPUs is saturation evidence; now find what is waiting.""",
}

# ---------------------------------------------------------------------------
# 53 Capstone server
# ---------------------------------------------------------------------------
EXTRA[53] = {
    "body": r"""
## Why this matters

This capstone ties the course together. You will build a small server the way
a careful operator would: it comes up after a reboot, serves traffic, accepts
administration only from you, exposes the minimum surface, and has a runbook
so someone else could take over. Passing means you can show evidence for each
claim, not just say "it works".

The exposed surface is your first proof. A web server with SSH needs exactly
three TCP ports reachable from outside: 22 for SSH, 80 for HTTP (usually only
to redirect), and 443 for HTTPS. Anything more must be justified in writing.

## Core concepts

| Layer | Deliverable | Evidence |
|-------|-------------|----------|
| Access | key-only SSH, no root login | `sshd -T`, failed password test |
| Network | default-deny firewall: 22, 80, 443 | `nft list ruleset`, external scan |
| Service | systemd unit for the app, hardened | `systemd-analyze security` |
| Edge | nginx or Caddy with TLS | `curl -vk`, cert dates |
| Data | backup and restore drill | restore diff output |
| Observability | logs and basic metrics | `journalctl`, node exporter |
| Operations | runbook, reboot test | notes, uptime after reboot |

```
  internet
     |  22 / 80 / 443 only
  [ firewall: policy drop ]
     |
  [ nginx :443 TLS ] --proxy--> [ app :8080 on 127.0.0.1, User=app ]
     |                               |
  /var/log/nginx              journald, /var/lib/app (RW), backups
  admin: ssh key -> sudo -> systemctl, journalctl, runbook.md
```

## Worked examples

Example 1: baseline and plan.

```bash
hostnamectl
ip -br a
sudo ss -tlnp
sudo useradd -m -s /bin/bash deploy
```

Record every listening port before you change anything.

Example 2: SSH hardening, with a second session open.

```bash
sudo tee /etc/ssh/sshd_config.d/10-hardening.conf <<'EOF'
PasswordAuthentication no
PermitRootLogin no
EOF
sudo sshd -t && sudo systemctl reload ssh
sudo sshd -T | grep -E 'passwordauthentication|permitrootlogin'
```

Example 3: firewall allowing only the required set.

```bash
sudo ufw default deny incoming
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
sudo ufw status numbered
```

Example 4: bind the app to loopback and let the proxy front it.

```bash
sudo ss -tlnp | grep 8080     # expect 127.0.0.1:8080, not 0.0.0.0
curl -sI http://127.0.0.1:8080/ | head -1
curl -skI https://localhost/ | head -1
```

Example 5: backup and restore evidence.

```bash
sudo tar -C /var/lib -czf /tmp/app-backup.tgz app
mkdir -p /tmp/restore && tar -C /tmp/restore -xzf /tmp/app-backup.tgz
diff -r /var/lib/app /tmp/restore/app && echo RESTORE_OK
```

## Mini-lab

1. Provision a fresh VM and snapshot it.
2. Write the baseline: listening ports, users, services.
3. Install nginx, deploy a static page or proxy a small app on loopback.
4. Add a TLS certificate (self-signed is fine) and test with `curl -vk`.
5. Harden SSH, then the firewall; verify with an external scan or `nc`.
6. Write the systemd unit with `User=`, `NoNewPrivileges=true`, and
   `ProtectSystem=strict`.
7. Run the backup and restore drill; save the output.
8. Reboot. Verify everything returns without manual steps.
9. Write `runbook.md`: start, stop, logs, restore, rollback.

## Decision guide / failure modes

| Question | Answer |
|----------|--------|
| Which ports remain open? | 22, 80, 443; justify any extra |
| App listens where? | 127.0.0.1 behind the proxy |
| Password SSH? | off; keys only |
| Proof of restore? | recorded diff or checksum result |
| Survives reboot? | unit enabled, firewall persisted |

Failure modes: ClickOps with no notes; ports open to the world because the
app bound to 0.0.0.0; firewall locking you out; certificates that expire
silently; no reboot test; and a runbook written from memory instead of from
the commands you actually ran. Reproducibility is the rubric.
""",
    "exercise_guide": r"""Open `exercise.sh` and implement `checklist_min_ports`. It prints the
comma-separated list of TCP port numbers, in ascending order and without
spaces, that a hardened web server with remote administration should expose
to the internet: one for SSH, one for plain HTTP, and one for HTTPS. One line,
nothing else. After it passes, build the capstone and produce an evidence
folder with the listening ports, firewall status, `sshd -T` excerpt,
certificate dates, restore diff, and post-reboot checks. Any port beyond
these three needs a written reason.""",
    "exercise_examples": r"""Run from the exercise folder:

    source ./exercise.sh
    checklist_min_ports

Expected single line of output:

    22,80,443

Related lab check (not graded):

    sudo ss -tlnp
    LISTEN 0 511 0.0.0.0:80    ... nginx
    LISTEN 0 511 0.0.0.0:443   ... nginx
    LISTEN 0 128 0.0.0.0:22    ... sshd
    LISTEN 0 128 127.0.0.1:8080 ... app

Port 8080 is fine because it is loopback only and not in the firewall allow set.""",
}

# ---------------------------------------------------------------------------
# 54 Capstone troubleshoot
# ---------------------------------------------------------------------------
EXTRA[54] = {
    "body": r"""
## Why this matters

Real systems rarely fail in one clean way. A disk fills, then a service
cannot write, then a health check fails, then someone "fixes" it by changing
permissions and creates a second fault. This capstone gives you a deliberately
broken VM so you can practice the full loop: diagnose, repair with the smallest
change, and write up what happened. The write-up matters as much as the fix;
without it, the same failure comes back.

A postmortem has a small set of required sections: summary and impact,
timeline, **root cause**, resolution, and prevention. If you must be strict
about one, it is the root cause, because without it the document is only a
diary and nothing can improve.

## Core concepts

| Postmortem section | Purpose |
|--------------------|---------|
| Summary and impact | who was affected, how badly, for how long |
| Timeline | timestamped facts: detect, diagnose, mitigate, resolve |
| Root cause | the underlying reason, not the trigger or the symptom |
| Resolution | exactly what restored service |
| Prevention | concrete actions with owners and dates |
| Lessons | what went well, what was lucky |

```
  symptom (what users saw)   "site returns 503"
        |   why?
  proximate cause            "app cannot write its state file"
        |   why?
  deeper cause               "filesystem is 100 percent full"
        |   why?
  ROOT CAUSE                 "log rotation disabled by an edit last week"
        |
  prevention: restore logrotate, alert at 90 percent disk, add test
```

Keep asking "why" until the answer is something you can fix permanently.
A person's mistake is rarely a root cause; the missing guardrail is.

## Worked examples

Example 1: a broken-box checklist, in order.

```bash
systemctl --failed
journalctl -p err -b --no-pager | tail -30
df -h; df -i
ip -br a; ip r
getent hosts example.com
mount | grep -E 'ro,|errors'
```

Example 2: bad fstab entry, system drops to emergency mode.

```bash
journalctl -xb | grep -i fstab
sudo cp /etc/fstab /root/fstab.bad
sudo nano /etc/fstab     # comment out or fix the bad line
sudo mount -a && echo MOUNT_OK
```

Example 3: permissions broken on a service directory.

```bash
sudo journalctl -u app.service -n 20 --no-pager
namei -l /var/lib/app/state.db
sudo chown -R app:app /var/lib/app
sudo chmod 750 /var/lib/app
```

Fix the specific path, not `chmod -R 777 /`.

Example 4: capture evidence before changing things.

```bash
mkdir -p ~/incident-$(date +%F) && cd ~/incident-$(date +%F)
df -h > df.before; ps aux > ps.before; journalctl -b --no-pager > journal.txt
```

Example 5: a postmortem skeleton.

```text
Title: App 503 after disk fill (2026-10-21)
Impact: 38 minutes of errors for all users
Timeline:
  14:02 alert  14:07 df shows 100 percent  14:21 logs freed  14:40 verified
Root cause: logrotate disabled by manual edit; no disk alert existed
Resolution: re-enabled logrotate, freed space, restarted app
Prevention: alert at 90 percent (owner: sam, Fri), config review rule
```

## Mini-lab

1. Snapshot a healthy VM. Have a friend (or you, earlier) inject at least
   three faults: full disk, bad fstab, wrong permissions, broken DNS, failed
   unit, expired cert.
2. Start a timeline file immediately; add timestamps as you go.
3. Run the baseline checks and save outputs before any change.
4. Fix one fault at a time and verify after each.
5. Do not rebuild the VM; debugging is the exercise.
6. Write the postmortem with all five sections and ask "why" at least three
   times to reach the root cause for each fault.
7. List prevention items that are specific, owned, and testable.

## Decision guide / failure modes

| Situation | Move |
|-----------|------|
| Many symptoms | find the earliest in the timeline |
| Tempting big hammer | stop; list the smallest reversible change |
| Fix works, cause unknown | keep investigating; it will recur |
| Blame-heavy write-up | rewrite around missing guardrails |
| Prevention is vague | add owner, date, and a check that proves it |

Failure modes: recreating the VM instead of debugging; changing everything
at once; no evidence preserved; postmortems that stop at the trigger ("someone
ran rm"); and prevention items like "be careful". The rubric is structured
troubleshooting, minimal blast radius, a clear root cause, and testable
prevention.
""",
    "exercise_guide": r"""Open `exercise.sh` and implement `postmortem_required_section`. It prints
the name of the one postmortem section the lesson calls mandatory because it
explains the underlying reason an incident happened, not just the symptom or
trigger. Output is lowercase, hyphenated, one line, no extra text. After it
passes, run the capstone: break three things in a snapshot, fix them one at a
time with evidence, and write the postmortem with all five sections. Use at
least three "why" steps for each fault and list prevention items with an owner
and a date. Keep the timeline file you started at the first minute.""",
    "exercise_examples": r"""Run from the exercise folder:

    source ./exercise.sh
    postmortem_required_section

Expected single line of output:

    root-cause

Example "why" chain (not graded):

    503 errors            <- app cannot write state
    cannot write state    <- disk 100 percent full
    disk full             <- logs not rotated since the config edit
    root cause            -> rotation disabled, and no disk alert existed

A root cause names a missing guardrail you can fix, not a person.""",
}

# ---------------------------------------------------------------------------
# 55 Capstone AI host
# ---------------------------------------------------------------------------
EXTRA[55] = {
    "body": r"""
## Why this matters

A model API is a long-running service with large memory use, slow startup,
and requests that may take seconds. These traits make deployment behavior
critical. If a deploy kills the process abruptly, in-flight requests fail and
clients see errors. If memory is unbounded, one leak kills everything on the
host. If limits and logs are missing, nobody can say why latency spiked. This
capstone builds a mock inference host (a plain HTTP server is fine, no GPU
needed) that demonstrates the full operational pattern.

Shutdown is the part people forget. systemd stops a service by sending
**SIGTERM** (TERM), waiting for `TimeoutStopSec`, and only then sending SIGKILL.
Your app must catch TERM, stop accepting new requests, finish current ones, and
exit cleanly. KILL cannot be caught, so it is the last resort, never the plan.

## Core concepts

| Layer | Setting | Purpose |
|-------|---------|---------|
| Unit | `User=model`, `NoNewPrivileges=true` | least privilege |
| Limits | `MemoryMax=`, `CPUQuota=`, `LimitNOFILE=` | bound the blast radius |
| Stop | `KillSignal=SIGTERM`, `TimeoutStopSec=30` | graceful drain |
| Edge | reverse proxy with TLS on 443 | termination, timeouts |
| Firewall | allow 22 and 443 only | small surface |
| Observability | journald, metrics endpoint, node exporter | capacity facts |
| Operations | runbook for deploy and rollback | repeatable changes |

```
  client --443/TLS--> [nginx proxy] --> [model server 127.0.0.1:8000]
                                          |  systemd unit, cgroup limits
  deploy: systemctl stop  -> SIGTERM -> app drains requests -> exit 0
                                   \--(30s)--> SIGKILL (last resort)
  watch: memory vs MemoryMax, nofile, p95 latency, 5xx, restart count
```

## Worked examples

Example 1: a mock model server that handles TERM.

```python
#!/usr/bin/env python3
import signal, sys, time
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        time.sleep(2)   # pretend inference
        self.send_response(200); self.end_headers(); self.wfile.write(b"ok\n")

srv = ThreadingHTTPServer(("127.0.0.1", 8000), H)
def stop(sig, frm):
    print("TERM received, draining", flush=True)
    import threading; threading.Thread(target=srv.shutdown).start()
signal.signal(signal.SIGTERM, stop)
srv.serve_forever()
srv.server_close()
print("clean exit", flush=True)
```

Example 2: the unit file.

```ini
[Unit]
Description=Mock model API
After=network.target

[Service]
User=model
ExecStart=/opt/model/server.py
Restart=on-failure
KillSignal=SIGTERM
TimeoutStopSec=30
MemoryMax=1G
CPUQuota=200%
LimitNOFILE=65536
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

Example 3: test graceful stop for real.

```bash
sudo systemctl start model
curl -s localhost:8000/ &
sudo systemctl stop model
journalctl -u model -n 5 --no-pager
```

The log should show the TERM message and a clean exit, and the curl should
still complete.

Example 4: confirm limits are live.

```bash
systemctl show model -p MemoryMax -p CPUQuota -p LimitNOFILE
systemd-cgtop -n 1 | head
```

Example 5: lock the surface and check.

```bash
sudo ufw default deny incoming
sudo ufw allow 22/tcp && sudo ufw allow 443/tcp && sudo ufw enable
sudo ss -tlnp | grep -E ':(8000|443)'
```

## Mini-lab

1. Create the `model` user and install the mock server.
2. Write the unit; start it and verify with `curl`.
3. Put nginx with a self-signed cert in front; proxy to 8000.
4. Allow only 22 and 443 in the firewall.
5. Run a load test: `for i in $(seq 50); do curl -sk https://localhost/ & done; wait`.
6. Run `sudo systemctl stop model` during the load; verify requests finish
   and the log shows TERM handling.
7. Send `kill -KILL` to a copy and compare: requests fail, no clean message.
8. Lower `MemoryMax` to 50M and trigger an allocation to watch the OOM
   event in `journalctl`.
9. Write the deploy and rollback runbook.

## Decision guide / failure modes

| Symptom | Likely cause | First check |
|---------|--------------|-------------|
| Errors during deploy | no TERM handler or short timeout | `journalctl -u`, `TimeoutStopSec` |
| Process killed, no trace | cgroup OOM | `journalctl -k`, `MemoryMax` |
| Too many open files | low nofile | `/proc/PID/limits` |
| Slow under load | CPU quota, disk, cold model | `systemd-cgtop`, `iostat` |
| Port exposed | firewall policy accept | `ss -tlnp`, `nft list ruleset` |

Failure modes: privileged containers; no memory limits; never testing
graceful stop; TERM handler that blocks forever; proxy timeout shorter than
inference time; and no restart-count alert. Clean behavior under TERM is a
rubric item, so demonstrate it with logs.
""",
    "exercise_guide": r"""Open `exercise.sh` and implement `graceful_stop_signal`. It prints the name
of the signal, written in uppercase without the `SIG` prefix, that systemd and
`kill` send by default to ask a service to shut down cleanly so it can drain
in-flight work. One line only. After it passes, finish the capstone: build
the mock model server with a handler for that signal, set limits in the unit,
and prove with logs that a stop during load lets requests complete. Compare
with `kill -KILL` and note the difference. Record limits shown by
`systemctl show` and the firewall ports you allow.""",
    "exercise_examples": r"""Run from the exercise folder:

    source ./exercise.sh
    graceful_stop_signal

Expected single line of output:

    TERM

Related lab check (not graded):

    sudo systemctl stop model
    journalctl -u model -n 3 --no-pager
    model[812]: TERM received, draining
    model[812]: clean exit
    systemd[1]: Stopped Mock model API.

KILL cannot be caught; seeing no drain message means the app was killed.""",
}

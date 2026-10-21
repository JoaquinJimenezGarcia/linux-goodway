---
title: "25. Packages: dnf/rpm (RHEL/Fedora) and Alpine apk"
---

# 25. Packages: dnf/rpm (RHEL/Fedora) and Alpine apk

**Phase:** Phase 8 — Packages, disks, storage  
**Estimated time:** 1 day  
**Slug:** `25-packages-dnf`

## Learning objectives

- Map apt concepts to dnf and apk
- Install/query/remove packages
- Know when distroless/minimal images help
- Read release notes before major upgrades

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.
Type every command yourself — muscle memory beats skimming.

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

## Common mistakes

- Running untrusted RPM scripts without review
- Assuming package names identical across distros
- Upgrading major releases without backups

## Exercises

Work in `exercises/25-packages-dnf/`. Read that folder's `README.md` fully before coding.

```bash
cd exercises/25-packages-dnf
chmod +x test.sh exercise.sh
./test.sh
```

### What you will build

Implement map_install_cmd in exercise.sh. It takes one argument naming a distribution family and prints the name of the native package manager command: debian maps to apt, rhel maps to dnf, and alpine maps to apk. Use a case statement and quote the argument. For an unknown family, print nothing and return 1. Output only the command name, with no other text. Run ./test.sh, then validate the table on real systems or containers by running the actual install command in each family.

### Study loop

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** run 2–3 lab commands from this lesson on a real Linux host; paste notable output into your notes
- **C (Challenge):** rewrite the exercise from memory the next day

**Do not open `solutions/25-packages-dnf/` until you have an honest failing attempt.**

## Self-check

Try to answer without scrolling up:

1. dnf equivalent of apt install?
2. Why minimal images?
3. apk is for which distro?

## Further reading

- https://dnf.readthedocs.io/

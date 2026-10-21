---
title: "27. LVM Intro and /etc/fstab"
---

# 27. LVM Intro and /etc/fstab

**Phase:** Phase 8 — Packages, disks, storage  
**Estimated time:** 1–2 days  
**Slug:** `27-lvm-fstab`

## Learning objectives

- Explain PV/VG/LV mentally
- Read fstab entries
- Add mounts safely with backups
- Use UUIDs over volatile device names

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.
Type every command yourself — muscle memory beats skimming.

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

## Common mistakes

- Using /dev/sdX names that reorder on reboot
- Editing fstab without reboot test in VM
- Shrinking filesystems without backups

## Exercises

Work in `exercises/27-lvm-fstab/`. Read that folder's `README.md` fully before coding.

```bash
cd exercises/27-lvm-fstab
chmod +x test.sh exercise.sh
./test.sh
```

### What you will build

Implement fstab_field_uuid in exercise.sh. It receives one complete fstab line as a single quoted argument and must print its first whitespace-separated field, which is the device specification such as UUID=1234-abcd. Fields are separated by spaces or tabs, so awk '{print $1}' or read -r both work. Quote $1 when you use it. Do not print the other fields. Afterwards, run it against real lines from /etc/fstab (skipping comments) and name each of the six fields in your notes.

### Study loop

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** run 2–3 lab commands from this lesson on a real Linux host; paste notable output into your notes
- **C (Challenge):** rewrite the exercise from memory the next day

**Do not open `solutions/27-lvm-fstab/` until you have an honest failing attempt.**

## Self-check

Try to answer without scrolling up:

1. Why UUID in fstab?
2. PV vs LV?
3. How recover bad fstab?

## Further reading

- https://man7.org/linux/man-pages/man5/fstab.5.html

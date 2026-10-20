---
title: "37. Compose and Kubernetes Concepts for Operators"
---

# 37. Compose and Kubernetes Concepts for Operators

**Phase:** Phase 11 — Containers and cloud Linux  
**Estimated time:** 2 days  
**Slug:** `37-compose-k8s-lite`

## Learning objectives

- Read a docker-compose file
- Map pods/services/deployments mentally
- Kubectl get/describe/logs basics
- Know what Linux skills transfer to k8s nodes

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

Compose: multi-container apps on one host.
Kubernetes: orchestrates containers across nodes — still Linux underneath.

```bash
kubectl get pods -A
kubectl describe pod X
kubectl logs X
kubectl exec -it X -- sh
```

Node issues are Linux issues: disk pressure, OOM, bad NICs, full inodes, clock skew.

## Common mistakes

- Learning only kubectl YAML without Linux debugging
- exec as the only debug tool
- Running privileged pods casually

## Exercises

Work in `exercises/37-compose-k8s-lite/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/37-compose-k8s-lite/` until you have an honest failing attempt.**

## Self-check

1. Pod vs container?
2. How fetch logs?
3. Name a node-level Linux failure

## Further reading

- https://kubernetes.io/docs/concepts/

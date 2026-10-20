---
title: "33. TLS Certificates and Trust Stores (ops view)"
---

# 33. TLS Certificates and Trust Stores (ops view)

**Phase:** Phase 9 — Security and SSH  
**Estimated time:** 1–2 days  
**Slug:** `33-tls-certs`

## Learning objectives

- Explain cert, key, chain, CA
- Inspect certs with openssl
- Know where system trust stores live
- Plan renewals before expiry

## Prerequisites

Complete prior numbered lessons. Prefer a real Linux VM/container for Linux-specific topics.

```bash
openssl s_client -connect example.com:443 -servername example.com </dev/null 2>/dev/null | openssl x509 -noout -dates -subject
openssl x509 -in cert.pem -text -noout | head
```

Expired certs cause "random" production panic. Automate renewal (ACM E/Let's Encrypt) and monitor expiry.

## Common mistakes

- Copying private keys into git
- Disabling TLS verification permanently
- Forgetting intermediate chain

## Exercises

Work in `exercises/33-tls-certs/`. Run:

```bash
./test.sh
```

- **A (Drill):** make `./test.sh` pass
- **B (Apply):** note one real command you ran on a Linux host related to this lesson
- **C (Challenge):** rewrite your solution from memory the next day

**Do not open `solutions/33-tls-certs/` until you have an honest failing attempt.**

## Self-check

1. What is a CA?
2. How inspect expiry?
3. Why automate renewal?

## Further reading

- https://www.openssl.org/docs/

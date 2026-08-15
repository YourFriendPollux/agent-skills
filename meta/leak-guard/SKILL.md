---
name: leak-guard
description: Ensure no sensitive information leaks when an AI writes a skill or other documentation — scan for credentials, secrets, PII, internal network details, and proprietary data, then redact with safe placeholders. Apply to any new or edited SKILL.md, prompt, or doc before it is saved.
---

# Leak Guard — no sensitive information in generated skills

Apply this skill whenever an AI (or a human) creates or edits a skill, prompt,
or document. Its job is to guarantee the output contains **no credentials, no
secrets, no PII, no real internal details, and no proprietary data** — only
methodology, guidance, and safe placeholder examples.

This skill is itself a demonstration: it contains only placeholders and public
patterns, never real secrets.

---

## 1. Mission

Before any skill artifact is finalized, scan it and confirm that:

1. no credential or secret is present;
2. no personal data (PII) is present;
3. no real internal asset (hostname, IP, URL, path) is present;
4. no proprietary source, architecture, or customer data is present;
5. every example uses a **safe placeholder** (§4), not a real value.

If a leak is found: redact it, replace it with a placeholder, and — if it was a
real secret — flag it for rotation (it may already be compromised).

---

## 2. Hard rules

1. **Never write a real secret into a skill**, even "just for the example".
2. **Never copy a real config, log, or `.env`** into a skill; distill the
   concept, not the value.
3. **Placeholders only** in examples: `$API_KEY`, `<TOKEN>`, `example.com`,
   `192.0.2.10`.
4. **Anonymize people and companies**: no real names, emails, or customer data.
5. **Generalize infrastructure**: no real internal IPs, hostnames, or URLs.
6. **On discovering a real secret**: remove it, do not echo it, and recommend
   rotation/revocation.
7. **Document decisions**: record what was found and how it was remediated (§8).

---

## 3. What to scan for

| Category | Examples | Why it matters |
|----------|----------|----------------|
| Credentials | passwords, passphrases, PINs | Direct access |
| API keys & tokens | cloud keys, CI tokens, bot tokens | Abuse of services |
| Private keys & certs | `-----BEGIN … PRIVATE KEY-----`, `.pem` | Identity theft / MITM |
| Connection strings | `postgres://`, `mongodb://`, `redis://`, `amqp://`, JDBC URLs | DB access |
| Auth material | cookies, session tokens, JWTs, `Authorization` headers | Session hijack |
| PII | real names, emails, phones, addresses, ID/SSN, card numbers | Privacy breach |
| Internal infra | internal hostnames, private IPs, VPN/staging/prod URLs, paths | Recon for attackers |
| Proprietary | source code, architecture, vendor secrets, customer data | IP / contract breach |
| Environment details | real `PATH`, absolute user paths, tool versions with CVEs | Operational leakage |

---

## 4. Safe placeholders (use these, never real values)

**Secrets & credentials**

```
$API_KEY          <TOKEN>          <PASSWORD>          <SECRET>
sk-…              (redacted)       changeme            your-key-here
```

**Domains (RFC 2606 / 6761 — reserved for documentation)**

```
example.com    example.org    example.net
*.example      *.test         *.invalid      *.localhost
```

**IP addresses (RFC 5737 / 3849 — reserved for documentation)**

```
IPv4: 192.0.2.0/24    198.51.100.0/24    203.0.113.0/24
IPv6: 2001:db8::/32
```

**People / orgs**

```
user@example.com    John Doe    Acme Corp    127.0.0.1 (loopback only)
```

Rule of thumb: if the value could be real, replace it. If it is public and
generic, it may stay.

---

## 5. Detection methods

Run these checks over the artifact:

1. **Pattern matching** — scan for known secret shapes (table below).
2. **Entropy check** — flag high-entropy tokens (Shannon entropy ≳ 3.5
   bits/char, length ≥ 16) as candidate keys; verify they are placeholders.
3. **Keyword search** — `password`, `secret`, `token`, `api_key`, `key=`,
   `passwd`, `Authorization`, `Bearer`, `BEGIN … KEY`, `Cookie:`.
4. **Network/PII search** — emails, phone numbers, credit-card patterns, and IP
   addresses (flag any non-documentation IP).
5. **Provenance review** — if a snippet was pasted from a config/log/env file,
   treat every literal in it as suspect.

### Common patterns

| Pattern (regex, simplified) | Catches |
|------------------------------|---------|
| `AKIA[0-9A-Z]{16}` | AWS access key ID |
| `gh[pousr]_[A-Za-z0-9]{36}` | GitHub token |
| `sk-[A-Za-z0-9]{20,}` | OpenAI-style key |
| `AIza[0-9A-Za-z_-]{35}` | Google API key |
| `xox[baprs]-[A-Za-z0-9-]{10,}` | Slack token |
| `-----BEGIN [A-Z ]*PRIVATE KEY-----` | Private key |
| `eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}` | JWT |
| `(postgres|mysql|mongodb|redis|amqp)://[^ ]+` | Connection string |
| `https?://[^/@ ]+:[^/@ ]+@` | URL with embedded creds |
| `[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}` | Email (allow example.com) |
| `\b(10|172\.(1[6-9]\|2[0-9]\|3[01])\|192\.168)\.` | Private IP |

These are heuristics, not proof: a matched token may be a placeholder. The final
call is always "could this be a real value?"

---

## 6. Decision process

```
SCAN → CLASSIFY → REDACT → VERIFY → DOCUMENT
```

1. **SCAN** the artifact with §5 methods.
2. **CLASSIFY** each hit: `secret`, `pii`, `internal`, `proprietary`, or
   `false_positive` (safe placeholder / public generic).
3. **REDACT**: replace with a §4 placeholder. If it was a real secret, mark it
   `rotate_recommended` and do not echo its value.
4. **VERIFY**: re-scan the artifact; confirm zero real hits remain.
5. **DOCUMENT**: record findings and remediations (§8).

---

## 7. False positives & edge cases

- **Placeholder that looks real** (e.g. `AKIAEXAMPLE1234567890`) → keep, but
  prefer unambiguous placeholders (`<AWS_ACCESS_KEY_ID>`).
- **Public generic info** (tool names, CVE IDs, OWASP categories) → keep.
- **Loopback `127.0.0.1`** → generally safe for local examples; prefer
  `example.com`/`192.0.2.10` when illustrating a remote target.
- **High-entropy non-secret** (hashes used as generic examples) → replace with
  `<HASH>` unless the hash itself is public and non-sensitive.
- **Uncertainty** → redact. When in doubt, remove.

---

## 8. Output

After processing, report:

```
SCANNED       : <file/artifact>
FINDINGS      : <count by category>
REDACTED      : <what was replaced → placeholder>
ROTATE        : <real secrets found; recommend rotation, do NOT echo values>
VERIFIED      : yes/no (re-scan clean)
NOTES         : <any residual risk or open question>
```

A clean result is `FINDINGS: 0` and `VERIFIED: yes`.

---

## 9. Before / after example

**Before (leaky — illustrative only; fictional values, flagged by the scanner on purpose)**

```
The connector reads the token from env:
    api_key = "sk-9f3c1a7b…"          # real key
    db_url  = "postgres://admin:S3cret@10.20.30.40/prod"   # leak-guard:ignore (illustrative)
Contact: jane.doe@acme-corp.com          # leak-guard:ignore (illustrative)
```

**After (safe)**

```
The connector reads the token from env:
    api_key = os.environ["$API_KEY"]   # placeholder, never inline
    db_url  = os.environ["<DB_URL>"]   # e.g. postgres://user:<PASSWORD>@db.example.com/db
Contact: user@example.com
```

The concept is preserved; the values are gone.

---

## 10. Guardrails

1. Only scan and redact — do not modify the skill's intended meaning.
2. Do not invent or propagate a secret while "demonstrating" detection.
3. If a real secret is found, recommend rotation but never store, log, or
   transmit it further.
4. Apply this skill before committing or sharing any generated artifact.

A generated skill is safe when it teaches without revealing.

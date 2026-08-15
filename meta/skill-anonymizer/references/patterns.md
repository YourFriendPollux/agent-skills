# Detection catalog — exhaustive pre-publication scan

Reference for the anonymization layers in `../SKILL.md` §5. Machine-checkable
patterns live in `../scripts/anonymize_scan.py`; this file is the readable
catalog for manual review and extension.

Convention: lines containing `# example`, `illustrative`, `leak-guard:ignore`,
or an HTML comment (`<!-- … -->`, invisible in rendered markdown) are
documentation and are skipped by the scanner. Keep it that way — a
documentation line must never look like a real value.

---

## 1. Secrets & credentials

| Pattern (simplified) | Catches | Notes |
|----------------------|---------|-------|
| `AKIA[0-9A-Z]{16}` | AWS access key ID | Verify with entropy if truncated |
| `gh[pousr]_[A-Za-z0-9]{36}` | GitHub token | Classic / fine-grained |
| `sk-[A-Za-z0-9]{20,}` | OpenAI-style key | Many providers reuse `sk-`; project keys are `sk-proj-…` |
| `xox[baprs]-[A-Za-z0-9-]{10,}` | Slack token | |
| `AIza[0-9A-Za-z_-]{35}` | Google API key | |
| `ya29\.[A-Za-z0-9_-]+` | Google OAuth token | |
| `-----BEGIN [A-Z ]*PRIVATE KEY-----` | Private key block | Also `BEGIN EC/OPENSSH/RSA` |
| `-----BEGIN CERTIFICATE-----` | Cert (may embed identity) | Usually fine, verify <!-- pattern-doc --> |
| `eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}` | JWT | Decode payload, check claims |
| `(postgres|mysql|mongodb|redis|amqp|sftp|https?)://[^ ]*:[^ ]*@` | Connection string with creds | Flag even if host is placeholder; skip `user:<PASSWORD>@` placeholder examples |
| `arn:aws:[a-z0-9-]+:[a-z0-9-]+:[0-9]{12}:` | AWS account ID / ARN | Account ID is an identifier |
| `s3://[a-z0-9.-]+/` | Bucket names | Internal bucket → internal asset |

**Also scan for:** base64 blobs ≥ 40 chars that decode to JSON (often tokens),
`Authorization: Bearer …` headers, `.npmrc`/`.pypirc`/`.netrc` credentials, <!-- pattern-doc -->
SSH key passphrase prompts, `BEGIN OPENSSH PRIVATE KEY`. <!-- pattern-doc -->

## 2. Entropy method

Anything can hide in a novel format; entropy does not care about format.

1. Extract tokens matching `[A-Za-z0-9_\-]{16,}`.
2. Compute Shannon entropy per token:
   `H = -Σ p(c)·log2(p(c))` over character frequencies.
3. Flag tokens with **length ≥ 16, H ≥ 3.5 bits/char, and at least one
   uppercase letter or digit** as candidate secrets. (All-lowercase long
   tokens are almost always identifiers or hyphenated names, not secrets.)

Calibration: digits-only tokens cap at ~3.32 (not flagged — timestamps,
versions); mixed case+digits+symbols readily exceed 3.5. Hashes used as
generic examples should be replaced with `<HASH>`.

## 3. Keywords (high recall, low precision)

| Keyword set | Lines to review |
|-------------|-----------------|
| `password\s*=`, `pwd\s*=`, `secret\s*=`, `client_secret` | Assignment of a real value <!-- pattern-doc --> (`passwd` is excluded: `/etc/passwd` drowns the report) |
| `api[_-]?key`, `access[_-]?key`, `token\s*=`, `private[_-]?key` | Key material <!-- pattern-doc --> |
| `authorization:\s*bearer`, `cookie\s*=`, `session` | Auth material <!-- pattern-doc --> |
| `.env`, `DATABASE_URL`, `REDIS_URL`, `AMQP_URL`, `JDBC:` | Config references <!-- pattern-doc --> |
| `BEGIN (RSA\|OPENSSH\|EC\|DSA) PRIVATE KEY` | Key blocks <!-- pattern-doc --> |
| truncated key prefixes (`AKIA…`, `ghp_…`, `sk-…`) | NOT scanned as bare prefixes — full keys are caught by §1, truncated ones by entropy; bare prefixes appear mostly in docs <!-- pattern-doc --> |

A keyword hit alone is not a finding — review the line and decide (§4.4 of the
skill).

## 4. PII

| Pattern | Catches | Notes |
|---------|---------|-------|
| `[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}` | Email | Whitelist `example.com/org/net`, `*.test`, `*.invalid`, `*.localhost` |
| `\+[1-9][0-9]{7,14}\b` | E.164 phone | |
| `\(?[0-9]{3}\)?[-. ][0-9]{3}[-. ][0-9]{4}` | US-format phone | |
| `[0-9]{4}[- ]?[0-9]{4}[- ]?[0-9]{4}[- ]?[0-9]{4}` | Card numbers | Run Luhn check to confirm |
| `[0-9]{3}-[0-9]{2}-[0-9]{4}` | US SSN | Ambiguous with dates — verify |
| `[A-Z]{2}[0-9]{6,9}` (context) | Passport-like IDs | Only with context keywords |

**Context keywords that upgrade a candidate to a finding:** `ssn`, `passport`,
`driving`, `license`, `card`, `phone`, `mobile`, `birth`, `address`.

## 5. Internal infrastructure

| Pattern | Catches | Notes |
|---------|---------|-------|
| `\b10\.\d{1,3}\.\d{1,3}\.\d{1,3}\b` | RFC1918 10/8 | |
| `\b172\.(1[6-9]\|2[0-9]\|3[01])\.\d{1,3}\.\d{1,3}\b` | RFC1918 172.16/12 | |
| `\b192\.168\.\d{1,3}\.\d{1,3}\b` | RFC1918 192.168/16 | |
| `169\.254\.169\.254` | Cloud metadata endpoint | AWS/GCP/Azure — high value |
| `\b127\.\d{1,3}\.\d{1,3}\.\d{1,3}\b`, `\b::1\b` | Loopback | Safe in local examples; still flag in logs |
| `(fd\|fc)[0-9a-f]{2}:` | ULA IPv6 | |
| `fe80:` | Link-local IPv6 | <!-- pattern-doc --> |
| `\b[a-z0-9-]+\.(internal\|corp\|local\|lan\|home\|office)\b` | Internal hostname suffixes | Case-insensitive; skip when followed by `(` (`Path.home(` is a call, not a host) |
| `\b[a-z0-9-]+\.(vpn\|intranet\|staging\|prod\|dev\|qa\|uat\|jenkins\|grafana\|gitlab\|admin)\.` | Internal service subdomains | Verify each |
| `([a-z0-9-]+\.)+[a-z]{2,}` with a known TLD, not in safe list | Real-looking domains | Client domains, internal dashboards; the TLD set is curated (common gTLDs/ccTLDs, `google`) so code identifiers (`os.path.join`) are excluded <!-- pattern-doc --> |
| `(/home\|/Users)/[A-Za-z0-9_.-]+` | User-home absolute paths | Usernames, machine names; system paths (`/etc`, `/var`, `/opt`) are low-signal and excluded by default |
| `C:\\(Users\|ProgramData\|Windows)` | Windows paths | |

**Safe (documentation) values — never flag:** `192.0.2.0/24`,
`198.51.100.0/24`, `203.0.113.0/24`, `2001:db8::/32`, `example.com/org/net`,
`*.test`, `*.invalid`, `*.localhost`, `127.0.0.1` in clearly-local examples. <!-- pattern-doc -->

## 6. Client & proprietary names

Automated detection is heuristic; the names list (§4.2 of the skill) is the
reliable path. When no list exists:

1. **Domain-derived candidates**: subdomains and email domains that are not
   the org's own — e.g. `jane@<client>.com`, `<client>.vpn.internal`, <!-- example -->
   `git@<client>:repo.git`. <!-- example -->
2. **Capitalized proper nouns** appearing ≥ 3 times in docs, logs, or code
   comments — review each occurrence.
3. **Identifier patterns**: `PROJ-[0-9]+`, `#[A-Z]+-[0-9]+` (ticket refs),
   contract numbers, support IDs.
4. **Product/codename terms** the user can name faster than a scanner can
   guess — always ask.

Anything in this category is classified `client | proprietary` until a human
confirms it is public.

## 7. File-level indicators

| Filename / extension | Why it is a finding |
|----------------------|---------------------|
| `.env`, `.env.*`, `*.env` | Real credentials file |
| `*.pem`, `*.key`, `*.p12`, `*.pfx`, `*.jks`, `*.keystore`, `id_rsa*` | Key material |
| `.npmrc`, `.pypirc`, `.netrc`, `credentials`, `secrets.yml` | Stored credentials |
| `*.bak`, `*.old`, `*.orig`, `*~`, `*.sql`, `*.dump`, `*.tar.gz`, `*.zip` | Backups/archives hide old state |
| `*.png`, `*.jpg`, `*.pdf`, `*.docx` | EXIF, author, GPS, OCR content |
| `*.log` | Runtime data: IPs, emails, users |
| `.git` dir inside scope, `*.patch`, `*.diff` | History or prior state |

Presence is a finding even if the content looks harmless — verify or exclude.

## 8. Obfuscation & tricks that defeat naive scans

- **Base64 / hex** encoding of secrets — decode and re-scan anything that
  decodes to readable text.
- **Unicode homoglyphs** in values or code — normalize before scanning.
- **Line-split secrets** (`sk-` + newline + continuation) — review multi-line
  assignments.
- **Real values with one char changed** — still a leak; replace, don't tweak.
- **Screenshots** of dashboards, terminals, or configs — the highest-risk
  non-text leak; review every image.

## 9. Safe placeholder vocabulary

Reuse leak-guard's placeholders so redacted output stays greppable and
unambiguous:

```
$API_KEY          <TOKEN>          <PASSWORD>          <SECRET>
<CLIENT_NAME>     <USERNAME>       <HOST>              <DB_URL>
user@example.com  example.com      192.0.2.10          <PROJECT_ID>
```

Prefer explicit placeholders (`<AWS_ACCESS_KEY_ID>`) over lookalikes
(`AKIAEXAMPLE…`): a placeholder must never be mistaken for a real value.

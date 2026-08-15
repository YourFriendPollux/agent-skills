---
name: skill-anonymizer
description: "Run an exhaustive pre-publication anonymization scan of a repository or document set — secrets, PII, internal IPs and hostnames, client and customer names, proprietary data — classify findings, redact with placeholders, produce a sign-off report. Use whenever publishing a repo or docs publicly, or before sharing anything that may contain internal or client data. Complements leak-guard."
version: 1.0.0
author: Dandl AI
license: AGPL-3.0
metadata:
  tags: [meta, anonymization, secrets, pii, pre-publication, security]
  related_skills: [leak-guard, skill-authoring]
---

# Repo Anonymizer — exhaustive pre-publication scan

Before anything leaves the org — a public repo, a blog post, a client delivery,
a support ticket — scan it for everything that must not leave: secrets,
credentials, PII, internal IPs and hostnames, client and customer names, and
proprietary data. This skill is the exhaustive pre-publication method: layered
automated scans, human review, classification, redaction, and a sign-off
report.

**Division of labor with [`leak-guard`](../leak-guard/SKILL.md):** leak-guard
enforces hygiene *while authoring* skills and docs (placeholders, no real
values). This skill scans *anything about to be published* — whole repos,
history, configs, logs, images — and drives it to a verified clean state. Apply
both: leak-guard while writing, this skill before shipping.

---

## 1. When to use

- Before publishing a repository, skill, docs, or artifacts publicly (GitHub,
  npm, PyPI, blog, forum).
- Before sharing any material with anyone outside the org: clients,
  contractors, support, partners.
- When a repo or folder has ever contained real configs, logs, client data,
  internal infrastructure, or credentials.
- Whenever a leak would be costly: security, contractual, or reputational.
- The user says "anonymize", "clean before publish", "scan for leaks",
  "pre-publication check".

## 2. Prerequisites

- A defined publication scope: the exact list of files/dirs going out.
- Access to the full history if the repo was ever private — secrets live in
  `git log`, reflogs, stashes, and old tags, not just the working tree.
- The **names list** (§4.2): clients, customers, people, product codenames,
  internal project names. Ask the user for it; if unavailable, run the
  heuristic pass (§4.6) and mark every hit for manual review.
- Permission to redact or exclude files. When in doubt, ask before deleting.

## 3. Golden rules

1. **Scan everything, including history** — not just the current diff.
2. **Never echo a real value.** Mask every finding in reports (§5): show the
   first/last few characters, never the full secret, email, or IP.
3. **When in doubt, redact or exclude.** A missing file is cheaper than a leak.
4. **Real secret found → recommend rotation immediately.** It may already be
   compromised; state this in the report, do not "fix it later".
5. **Anonymization is per-release.** Re-run the full scan before every
   publication, not once per repo.
6. **The report is the deliverable**: findings classified, files touched,
   residual risk, and an explicit sign-off.

## 4. Workflow

### 4.1 Inventory

List everything in the publication scope. Include hidden files, archives,
images, PDFs, `.env*`, `.git` internals, and CI configs. Exclude only what is
explicitly out of scope (build artifacts, `node_modules`, `.git` history if a
fresh history was requested).

### 4.2 Collect the names list

Ask the user for, and write to a file (one per line, `#` comments allowed):

- client and customer names (orgs, brands, product names);
- people's names and personal emails;
- internal project names and codenames;
- internal product/domain names.

This list is the only reliable way to catch client names; automated heuristics
can only suggest candidates (§4.6).

### 4.3 Automated scan

```bash
python3 meta/skill-anonymizer/scripts/anonymize_scan.py --root <scope> \
  --names names.txt --json findings.json
```

Runs all detection layers (§5): secret patterns, entropy, keywords, PII,
internal infra, names list, file-level indicators. Review every finding; the
scanner is high-recall by design.

### 4.4 Classify

For each finding, record: `secret | pii | internal | client | proprietary |
false_positive`. Keep a ledger (file, line, category, decision). A finding is
`false_positive` only when you can prove it is a placeholder, documentation, or
public generic data — not because you "know it's fine".

### 4.5 Redact or exclude

- **Redact** with safe placeholders from leak-guard: `$API_KEY`, `<TOKEN>`,
  `user@example.com`, `192.0.2.10`, `<CLIENT_NAME>`.
- **Exclude** the file entirely when the value is structural (a real log, a
  real config) — replace with a sanitized template (`config.example`).
- Never "obfuscate" by changing one character of a real value; that is still a
  leak and it breaks the config.

### 4.6 Client-name heuristics (when no names list exists)

1. **Domain-derived**: client names appear in emails
   (`jane@<client>.com`), subdomains (`<client>.vpn.internal`), URLs <!-- example -->
   (`<client>-dashboard.example.com`), git remotes (`git@<client>:repo.git`). <!-- example -->
2. **Frequency analysis**: capitalized proper nouns appearing ≥ 3 times in
   docs/logs/code comments — review each.
3. **Fingerprint terms**: product names, codenames, contract/reference IDs
   (`PROJ-####`, `#ENG-####`), support ticket prefixes.
4. Flag all candidates `client | proprietary` and require manual confirmation.

### 4.7 Verify

1. Re-run the automated scan: **zero findings** except documented
   false positives.
2. Grep the scope for every name in the names list (case-insensitive,
   word-boundary).
3. Read the actual diff/changes once, by eye — patterns miss context.
4. If the repo has history: scan `git log -p` output or clone fresh and
   re-scan (§8.5).

### 4.8 Report & sign-off

Produce the report:

```text
SCOPE        : <files/dirs scanned>
FINDINGS     : <count by category: secret / pii / internal / client / proprietary>
REDACTED     : <file → placeholder>
EXCLUDED     : <file → reason>
ROTATE       : <real secrets found — recommend rotation, never echo values>
FALSE POS.   : <count + why>
RESIDUAL RISK: <what could still leak and why it is accepted>
SIGN-OFF     : <who approved, when>
```

A clean result is `FINDINGS: 0` after verification, with residual risk stated
and sign-off recorded. Do not publish until sign-off exists.

## 5. Detection layers

Full catalog with regexes and examples: [`references/patterns.md`](references/patterns.md).
Summary:

| Layer | What it catches | Notes |
|-------|-----------------|-------|
| 1. Secret patterns | API keys, tokens, private keys, connection strings, JWTs | Extends leak-guard's table |
| 2. Entropy | High-entropy tokens (≥ 16 chars, ≥ 3.5 bits/char, mixed-case) | Catches what patterns miss |
| 3. Keywords | `password=`, `Bearer`, `BEGIN … KEY`, `.env`, `client_secret` | High recall, low precision <!-- pattern-doc --> |
| 4. PII | Emails, phones, cards (Luhn), SSNs | Example domains whitelisted |
| 5. Internal infra | RFC1918, cloud-metadata IP, internal hostname suffixes, real domains, absolute paths | Doc IPs whitelisted |
| 6. Names list | Clients, customers, people, codenames | From §4.2; heuristics in §4.6 |
| 7. File-level | `.env*`, `*.pem`, `*.key`, backups, archives, image/PDF metadata | Presence is a finding |
| 8. Human review | Context, obfuscation, Unicode tricks, base64 | Always run, never skippable |

## 6. Per-file-type checklist

| Type | What to check |
|------|---------------|
| Code | Hardcoded secrets, URLs, hostnames, absolute paths in comments/strings |
| Config / `.env` | Keys, connection strings, endpoints, user accounts |
| Logs | IPs, emails, usernames, paths, real timestamps, trace IDs |
| Docs / skills | Pasted configs, screenshots, real examples, client mentions |
| Images / PDFs | EXIF, metadata, OCR'd content, unredacted regions (redaction ≠ black box over text) |
| Archives / backups | Nested files, hidden files, `.git` remnants, old configs |
| CI configs | Tokens in YAML, registry credentials, deploy keys |
| Git history | `git log -p`, reflog, stashes, tags, author emails, commit messages |

## 7. Pitfalls

| Pitfall | Failure | Fix |
|---------|---------|-----|
| Scanning only the working tree | Secrets in history survive | Scan `git log -p` or fresh clone (§8.5) |
| Forgetting `.env*`, logs, metadata | Biggest leak class missed | Use the per-file checklist (§6) |
| Trusting patterns alone | Novel formats slip through | Entropy + keyword layers always on |
| Echoing findings verbatim | Report itself becomes a leak | Mask values (§3.2) |
| Real-looking placeholders (`AKIAEXAMPLE…`) | Reviewer "knows it's fine" | Proven-false-positive only (§4.4) |
| One-char obfuscation of a real value | Still a leak, breaks config | Redact or exclude properly |
| "Just this example" from a real config | Copy-paste of a secret | Treat every pasted snippet as suspect |
| Unicode / base64 / hex hiding | Plain regex misses it | Human review + decode pass |
| Scanning once, publishing often | Later edits leak | Re-run before every release (§3.5) |

## 8. Verification

1. `anonymize_scan.py` reports zero unclassified findings.
2. Grep for every names-list entry: zero hits.
3. Manual diff review completed (by eye, not just tool output).
4. Report produced with §4.8 format; `ROTATE` section present if real secrets
   were found.
5. Fresh-clone test: `git clone` the to-be-published branch into a clean dir,
   run the scan there, expect zero findings — proves history is clean too.
6. Sign-off recorded before publication.

## 9. Out of scope

- Rotating or revoking secrets: recommend it, never do it.
- Legal or contractual advice on what may be published.
- Rewriting code or architecture as part of anonymization.
- Modifying binaries or images in place — flag them for exclusion instead.

## 10. References

- `references/patterns.md` — the full detection catalog: regexes, entropy
  method, keyword lists, per-file-type notes, safe-placeholder vocabulary.
- `scripts/anonymize_scan.py` — deterministic scanner (stdlib only).
  Usage: `python3 scripts/anonymize_scan.py --help`.
- [`leak-guard`](../leak-guard/SKILL.md) — placeholder vocabulary + hygiene
  while authoring.
- [`skill-authoring`](../skill-authoring/SKILL.md) — the method used to build
  this skill.

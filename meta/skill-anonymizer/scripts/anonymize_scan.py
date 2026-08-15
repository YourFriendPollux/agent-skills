#!/usr/bin/env python3
"""anonymize_scan.py — exhaustive pre-publication leak scan (stdlib only).

Usage:
    python3 anonymize_scan.py [--root DIR] [--names FILE] [--ignore GLOB]...
                              [--json FILE] [--quiet]

Detection layers (see ../references/patterns.md):
  secret patterns | entropy | keywords | PII (email/phone/card/SSN) |
  internal infra (RFC1918, cloud-metadata IP, internal hostnames, absolute
  paths) | unrecognized domains | client/proprietary names (--names) |
  file-level indicators (.env, keys, backups, media).

Documentation convention: lines containing 'leak-guard:ignore', '# example',
'illustrative', 'AKIAEXAMPLE', or an HTML comment ('<!-- … -->', which renders
invisibly in markdown) are skipped. Keep the names list OUTSIDE the scanned
root — the scanner flags the list itself if it is scanned.

Exit code: 0 = no findings, 1 = findings to classify, 2 = usage error.
"""

import argparse
import fnmatch
import json
import math
import os
import re
import sys

VERSION = "1.0.0"

# ---------------------------------------------------------------------------
# Layer 1 — secret patterns
# ---------------------------------------------------------------------------
SECRET_PATTERNS = [
    ("aws-access-key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("github-token", re.compile(r"gh[pousr]_[A-Za-z0-9]{36}")),
    ("openai-key", re.compile(r"sk-[A-Za-z0-9]{20,}")),
    ("openai-project-key", re.compile(r"sk-proj-[A-Za-z0-9_-]{20,}")),
    ("slack-token", re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}")),
    ("google-api-key", re.compile(r"AIza[0-9A-Za-z_-]{35}")),
    ("google-oauth-token", re.compile(r"ya29\.[A-Za-z0-9_-]+")),
    ("private-key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("certificate", re.compile(r"-----BEGIN CERTIFICATE-----")),
    ("jwt", re.compile(r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"
                       r"\.[A-Za-z0-9_-]{10,}")),
    ("connection-string", re.compile(r"[a-z]+://[^ \s]*:[^ \s@]*@")),
    ("arn", re.compile(r"arn:aws:[a-z0-9-]+:[a-z0-9-]+:[0-9]{12}:")),
]

# ---------------------------------------------------------------------------
# Layer 3 — keywords (high recall, low precision)
# ---------------------------------------------------------------------------
# Bare key prefixes (AKIA, ghp_, sk-, xox, ya29) are intentionally NOT here:
# full keys are caught by SECRET_PATTERNS, and bare prefixes appear mostly in
# documentation. High-recall keyword hits need a value shape after them.
# Bare key prefixes (AKIA, ghp_, sk-, xox, ya29) are intentionally NOT here:
# full keys are caught by SECRET_PATTERNS, and bare prefixes appear mostly in
# documentation. High-recall keyword hits need a value shape after them.
# "passwd" is excluded too: /etc/passwd and the Unix command drown the report.
KEYWORD_RE = re.compile(
    r"(password\s*=|pwd\s*=|secret\s*=|client_secret"
    r"|api[_-]?key\s*=|access[_-]?key\s*=|token\s*=|private[_-]?key"
    r"|authorization:\s*bearer|BEGIN (RSA|OPENSSH|EC|DSA) PRIVATE KEY"
    r"|DATABASE_URL|REDIS_URL|AMQP_URL|JDBC:)",
    re.IGNORECASE,
)

# ---------------------------------------------------------------------------
# Layer 4 — PII
# ---------------------------------------------------------------------------
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"(\+[1-9][0-9]{7,14}\b|"
                      r"\(?[0-9]{3}\)?[-. ][0-9]{3}[-. ][0-9]{4})")
CARD_RE = re.compile(r"\b[0-9]{4}[- ]?[0-9]{4}[- ]?[0-9]{4}[- ]?[0-9]{4}\b")
SSN_RE = re.compile(r"\b[0-9]{3}-[0-9]{2}-[0-9]{4}\b")

# ---------------------------------------------------------------------------
# Layer 5 — internal infrastructure
# ---------------------------------------------------------------------------
IP_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
RFC1918_RE = re.compile(r"\b(10|127)(\.\d{1,3}){3}\b|"
                        r"\b172\.(1[6-9]|2[0-9]|3[01])(\.\d{1,3}){2}\b|"
                        r"\b192\.168(\.\d{1,3}){2}\b")
METADATA_IP = "169.254.169.254"
ULA_RE = re.compile(r"\b(?:fd|fc)[0-9a-f]{2}:", re.IGNORECASE)
LINKLOCAL_RE = re.compile(r"\bfe80:", re.IGNORECASE)
INTERNAL_HOST_RE = re.compile(
    r"\b[a-z0-9-]+\.(internal|corp|local|lan|home|office)\b", re.IGNORECASE)
INTERNAL_SVC_RE = re.compile(
    r"\b[a-z0-9-]+\.(vpn|intranet|staging|prod|dev|qa|uat|jenkins|grafana|"
    r"gitlab|admin)\.", re.IGNORECASE)
DOMAIN_RE = re.compile(r"([a-z0-9-]+\.)+[a-z]{2,}", re.IGNORECASE)
# Only user-home paths are high-signal: /etc, /var, /opt, /srv are full of
# generic system paths that drown the report (see references/patterns.md).
PATH_RE = re.compile(r"(/home|/Users)/[A-Za-z0-9_.-]+")
WINPATH_RE = re.compile(r"C:\\(Users|ProgramData|Windows)", re.IGNORECASE)

# Documentation IPs (RFC 5737 / 3849) are always safe.
DOC_IP_PREFIXES = ("192.0.2.", "198.51.100.", "203.0.113.", "2001:db8:")

# Well-known public domains — safe by suffix match ("fonts.google.com" ok,
# "evil-google.com" not).
SAFE_DOMAINS = (
    "example.com", "example.org", "example.net", "example.test",
    "example.invalid", "example.localhost", "localhost",
    "github.com", "github.io", "gitlab.com", "bitbucket.org", "npmjs.com",
    "pypi.org", "python.org", "pythonhosted.org", "nodejs.org",
    "google.com", "gmail.com", "youtube.com", "android.com", "googleapis.com",
    "stackoverflow.com", "stackexchange.com", "medium.com", "wikipedia.org",
    "w3.org", "mozilla.org", "apache.org", "gnu.org", "linux.org", "kernel.org",
    "docker.com", "hub.docker.com", "kubernetes.io", "debian.org",
    "ubuntu.com", "redhat.com", "amazon.com", "aws.amazon.com",
    "microsoft.com", "azure.microsoft.com", "cloud.google.com",
    "openssl.org", "curl.se", "react.dev", "nextjs.org",
    "typescriptlang.org", "rust-lang.org", "go.dev", "openai.com",
    "anthropic.com", "cloudflare.com", "vercel.com", "netlify.com",
    "heroku.com", "digitalocean.com", "postgresql.org", "mysql.com",
    "google",  # brand TLD: about.google, blog.google, … are all public
    "mongodb.com", "redis.io", "nginx.org", "sqlite.org", "json.org",
    "yaml.org", "unicode.org", "ietf.org", "rfc-editor.org", "owasp.org",
    "cve.org", "nist.gov", "readthedocs.io", "mdn.dev", "primer.style",
    "material.io", "fonts.google.com", "semver.org", "snyk.io",
)

# TLDs that are really file extensions — never treat as domains.
EXT_TLDS = {
    "md", "markdown", "txt", "py", "js", "jsx", "ts", "tsx", "css", "scss",
    "html", "htm", "xml", "json", "jsonl", "ndjson", "yml", "yaml", "toml",
    "ini", "cfg", "conf", "log", "sh", "bash", "zsh", "csv", "tsv", "sql",
    "db", "env", "example", "gitignore", "gitattributes", "lock", "mod",
    "sum", "go", "rs", "java", "kt", "swift", "c", "h", "cpp", "hpp",
    "rb", "php", "pl", "ps1", "bat", "cmd", "vue", "svelte", "d", "patch",
    "diff", "orig", "bak", "old", "tar", "gz", "zip", "rar", "7z", "png",
    "jpg", "jpeg", "gif", "svg", "pdf", "doc", "docx", "xls", "xlsx",
    "ppt", "pptx", "ico", "woff", "woff2", "ttf", "otf", "eot", "mp4",
    "mp3", "wav", "pyc", "class", "jar",
}

# Real TLDs (gTLDs + common ccTLDs + brand TLDs). The domain layer only fires
# on these, so dotted code identifiers (os.path.join, json.loads, Path.home)
# are not mistaken for domains.
KNOWN_TLDS = {
    "com", "org", "net", "io", "dev", "ai", "app", "co", "info", "biz",
    "xyz", "me", "tv", "cc", "pro", "mobi", "cloud", "tech",
    "site", "online", "store", "shop", "design", "digital", "media",
    "network", "solutions", "systems", "works", "world", "life", "live",
    "today", "news", "blog",    "wiki", "email", "page", "studio", "agency",
    "guru", "team", "company", "center", "care", "chat", "city",
    "club", "consulting", "data", "directory", "download", "education",
    "engineering", "events", "expert", "family", "finance", "financial",
    "fish", "fit", "fitness", "foundation", "fun", "fund", "games",
    "garden", "gift", "global", "golf", "graphics", "green", "guide",
    "health", "healthcare", "help", "host", "hosting", "house", "icu",
    "industries", "ink", "institute", "insure", "international", "kim",
    "kitchen", "land", "law", "lawyer", "lease", "legal", "limited",
    "link", "loan", "loans", "love", "market", "marketing", "mba", "meet",
    "menu", "money", "movie", "museum", "ninja", "observer", "one", "ong",
    "organic", "partners", "parts", "party", "pet", "photo", "photography",
    "photos", "pics", "pictures", "pink", "pizza", "place", "plumbing",
    "plus", "press", "productions", "properties", "pub", "racing", "radio",
    "realestate", "rent", "rentals", "repair", "report", "restaurant",
    "review", "reviews", "rich", "rocks", "run", "sale", "salon",
    "school", "science", "security", "services", "shoes", "show", "singles",
    "ski", "soccer", "social", "software", "solar", "space", "sport",
    "sports", "storage", "stream", "study", "style", "supplies", "supply",
    "support", "surf", "surgery", "tattoo", "tax", "taxi", "team",
    "technology", "tennis", "theater", "tips", "tires",    "tools", "top",
    "tours", "town", "toys", "trade", "training", "travel", "tube",
    # "name" and "group" are real TLDs but are excluded: in code they appear
    # constantly as attributes (os.name, match.group) and drown the report.

    "university", "uno", "vacations", "ventures", "vet", "video", "villas",
    "vip", "vision", "vote", "voting", "voyage", "watch", "webcam",
    "website", "wedding", "win", "wine", "work", "wow", "wtf", "yoga",
    "zone", "google",
    "us", "uk", "de", "fr", "cn", "jp", "ru", "br", "in", "it", "es",
    "nl", "se", "no", "fi", "dk", "pl", "ch", "at", "be", "pt", "gr",
    "ie", "cz", "sk", "hu", "ro", "bg", "hr", "rs", "si", "ua", "tr",
    "il", "sa", "ae", "qa", "eg", "ma", "ng", "ke", "za", "mx", "ar",
    "cl", "pe", "uy", "ec", "ca", "au", "nz", "sg", "my", "id", "th",
    "vn", "ph", "kr", "tw", "hk", "pk", "bd", "lk", "np", "kz", "uz",
    "by", "lt", "lv", "ee", "is", "lu", "mt", "cy", "eu",
}

# ---------------------------------------------------------------------------
# Layer 2 — entropy
# ---------------------------------------------------------------------------
ENTROPY_TOKEN_RE = re.compile(r"[A-Za-z0-9_\-]{16,}")
ENTROPY_MIN_LEN = 16
ENTROPY_MIN_BITS = 3.5


def shannon_entropy(token):
    if not token:
        return 0.0
    freq = {}
    for ch in token:
        freq[ch] = freq.get(ch, 0) + 1
    n = len(token)
    return -sum((c / n) * math.log2(c / n) for c in freq.values())


# ---------------------------------------------------------------------------
# Layer 7 — file-level indicators
# ---------------------------------------------------------------------------
KEY_FILE_EXTS = {".pem", ".key", ".p12", ".pfx", ".jks", ".keystore"}
KEY_FILE_NAMES = {"id_rsa", "id_ed25519", "id_dsa", "credentials",
                  "secrets.yml", "secrets.yaml", ".npmrc", ".pypirc",
                  ".netrc", ".htpasswd"}
DATA_EXTS = {".sql", ".dump", ".bak", ".old", ".orig", ".db", ".sqlite",
             ".sqlite3", ".mdb"}
LOG_EXTS = {".log"}
MEDIA_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".docx", ".doc",
              ".xlsx", ".xls", ".pptx"}
BINARY_EXTS = {".ico", ".woff", ".woff2", ".ttf", ".otf", ".eot", ".mp4",
               ".mov", ".mp3", ".wav", ".exe", ".dll", ".so", ".dylib",
               ".a", ".o", ".pyc", ".class", ".jar", ".war", ".bin", ".dat",
               ".dmp", ".gz", ".tar", ".zip", ".7z", ".rar"}
SKIP_DIRS = {".git", ".svn", ".hg", "__pycache__", ".venv", "venv",
             "node_modules", "dist", "build", "target", ".idea", ".vscode",
             ".next", ".cache", ".tox", ".mypy_cache", ".pytest_cache",
             ".ruff_cache"}
SKIP_FILES = {".DS_Store"}

# Review-level findings: real hits need eyes, but are often false positives.
REVIEW_CATEGORIES = {"entropy", "keyword", "loopback", "public-ip", "domain",
                     "media", "log", "certificate"}


def is_doc_line(line):
    low = line.lower()
    return ("leak-guard:ignore" in low or "# example" in low
            or "illustrative" in low or "akiaexample" in low
            or "<!--" in low)


def mask(value, keep=3):
    v = value.strip()
    if len(v) <= keep * 2 + 2:
        return "<redacted>"
    return v[:keep] + "…" + v[-keep:]


def mask_email(value):
    if "@" in value:
        local, _, domain = value.partition("@")
        return f"{mask(local)}@{domain}"
    return mask(value)


def is_safe_domain(domain):
    d = domain.lower()
    if "example" in d or d in SAFE_DOMAINS:
        return True
    return any(d.endswith("." + s) for s in SAFE_DOMAINS)


def classify_ip(ip):
    if any(ip.startswith(p) for p in DOC_IP_PREFIXES):
        return None
    if ip == METADATA_IP:
        return "metadata-ip"
    if RFC1918_RE.fullmatch(ip):
        return "loopback-ip" if ip.startswith("127.") else "internal-ip"
    return "public-ip"


def luhn_ok(digits):
    total = 0
    for i, ch in enumerate(reversed(digits)):
        d = ord(ch) - 48
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total % 10 == 0


def file_level_findings(name, path):
    """Return (category, detail) findings for the file itself."""
    base = os.path.basename(path).lower()
    stem, ext = os.path.splitext(base)
    if "example" in base or "template" in base:
        return []
    out = []
    if base == ".env" or base.startswith(".env.") or ".env." in base:
        out.append(("file", "credential file (.env) — exclude or replace with a template"))
    if ext in KEY_FILE_EXTS or stem in KEY_FILE_NAMES or base in KEY_FILE_NAMES:
        out.append(("file", f"key/credential file ({ext or base})"))
    if ext in DATA_EXTS:
        out.append(("file", f"data/backup file ({ext}) — may contain old state"))
    if ext in LOG_EXTS:
        out.append(("log", "runtime log — IPs, emails, users, timestamps"))
    if ext in MEDIA_EXTS:
        out.append(("media", f"{ext} — EXIF/OCR/embedded metadata; review content"))
    return out


def is_binary(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in BINARY_EXTS or ext in MEDIA_EXTS:
        return True
    try:
        with open(path, "rb") as fh:
            return b"\x00" in fh.read(8192)
    except OSError:
        return True


def scan_file(path, names_regexes, ignores):
    """Return (file_findings, line_findings)."""
    findings = []

    for cat, detail in file_level_findings(os.path.basename(path), path):
        findings.append({"file": path, "line": 0, "category": cat,
                         "snippet": detail, "pattern": "file-level"})

    if is_binary(path):
        return findings

    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            for lineno, line in enumerate(fh, 1):
                if is_doc_line(line):
                    continue
                for cat, snippet, pattern in scan_line(line, names_regexes):
                    findings.append({"file": path, "line": lineno,
                                     "category": cat, "snippet": snippet,
                                     "pattern": pattern})
    except OSError as exc:
        findings.append({"file": path, "line": 0, "category": "file",
                         "snippet": f"unreadable: {exc}", "pattern": "io"})
    return findings


def scan_line(line, names_regexes):
    out = []

    # Layer 1 — secret patterns
    for label, rx in SECRET_PATTERNS:
        for m in rx.finditer(line):
            if label == "connection-string" and "<" in m.group(0):
                continue  # placeholder example (postgres://user:<PASSWORD>@…)
            cat = "review" if label == "certificate" else "secret"
            out.append((cat, mask(m.group(0)), label))

    # Layer 2 — entropy
    # All-lowercase 16+ char tokens are almost always identifiers or hyphenated
    # names (skill-name, build_injected_context) — require an uppercase letter
    # or digit so the layer targets random-looking material.
    for tok in ENTROPY_TOKEN_RE.findall(line):
        if (len(tok) >= ENTROPY_MIN_LEN
                and re.search(r"[A-Z0-9]", tok)
                and shannon_entropy(tok) >= ENTROPY_MIN_BITS):
            out.append(("entropy", mask(tok), "entropy"))

    # Layer 3 — keywords
    if KEYWORD_RE.search(line):
        out.append(("keyword", mask(KEYWORD_RE.search(line).group(0)),
                    "keyword"))

    # Layer 4 — PII
    for m in EMAIL_RE.finditer(line):
        domain = m.group(0).rsplit("@", 1)[1]
        if not is_safe_domain(domain):
            out.append(("pii", mask_email(m.group(0)), "email"))
    for m in PHONE_RE.finditer(line):
        out.append(("pii", mask(m.group(0)), "phone"))
    for m in CARD_RE.finditer(line):
        digits = re.sub(r"[^0-9]", "", m.group(0))
        if luhn_ok(digits):
            out.append(("pii", mask(m.group(0)), "credit-card"))
    for m in SSN_RE.finditer(line):
        out.append(("pii", mask(m.group(0)), "ssn"))

    # Layer 5 — internal infrastructure
    for m in IP_RE.finditer(line):
        cat = classify_ip(m.group(0))
        if cat:
            out.append((cat, mask(m.group(0)), "ip"))
    for m in ULA_RE.finditer(line):
        out.append(("internal", mask(m.group(0)), "ula-ipv6"))
    for m in LINKLOCAL_RE.finditer(line):
        out.append(("internal", mask(m.group(0)), "link-local-ipv6"))
    for m in INTERNAL_HOST_RE.finditer(line):
        if line[m.end():m.end() + 1] == "(":
            continue  # Path.home( — a function call, not a hostname
        out.append(("internal", mask(m.group(0)), "internal-hostname"))
    for m in INTERNAL_SVC_RE.finditer(line):
        out.append(("internal", mask(m.group(0)), "internal-subdomain"))
    for m in PATH_RE.finditer(line):
        out.append(("internal", mask(m.group(0)), "absolute-path"))
    for m in WINPATH_RE.finditer(line):
        out.append(("internal", mask(m.group(0)), "windows-path"))
    for m in DOMAIN_RE.finditer(line):
        d = m.group(0)
        tld = d.rsplit(".", 1)[1].lower()
        if (tld in EXT_TLDS or tld not in KNOWN_TLDS
                or is_safe_domain(d)):
            continue  # file extension, code identifier, or known public domain
        out.append(("domain", mask(d), "unrecognized-domain"))

    # Layer 6 — client / proprietary names
    for rx in names_regexes:
        for m in rx.finditer(line):
            out.append(("client", mask(m.group(0)), "names-list"))

    return out


def load_names(path):
    rx = []
    if not path:
        return rx
    with open(path, encoding="utf-8", errors="replace") as fh:
        for raw in fh:
            name = raw.strip()
            if not name or name.startswith("#"):
                continue
            rx.append(re.compile(r"\b" + re.escape(name) + r"\b",
                                 re.IGNORECASE))
    return rx


def main(argv):
    ap = argparse.ArgumentParser(
        description="Exhaustive pre-publication leak scan (stdlib only).")
    ap.add_argument("--root", default=".", help="file or directory to scan")
    ap.add_argument("--names", help="file of names to scan for (one per line)")
    ap.add_argument("--ignore", action="append", default=[],
                    help="glob of files/dirs to skip (repeatable)")
    ap.add_argument("--json", help="write findings as JSON to this file")
    ap.add_argument("--quiet", action="store_true", help="summary only")
    ap.add_argument("--version", action="version", version=VERSION)
    args = ap.parse_args(argv)

    names_regexes = load_names(args.names)
    self_path = os.path.abspath(__file__)
    ignores = args.ignore + ["*" + os.sep + d + os.sep + "*" for d in SKIP_DIRS]

    all_findings = []

    def ignored(rel):
        return any(fnmatch.fnmatch(rel, pat) for pat in ignores)

    def walk(path):
        if os.path.isfile(path):
            yield path
            return
        for root, dirs, files in os.walk(path):
            rel = os.path.relpath(root, args.root)
            dirs[:] = [d for d in dirs
                       if d not in SKIP_DIRS
                       and not ignored(os.path.join(rel, d) + os.sep)]
            for name in sorted(files):
                fpath = os.path.join(root, name)
                if name in SKIP_FILES or os.path.abspath(fpath) == self_path:
                    continue
                if ignored(os.path.join(rel, name)):
                    continue
                yield fpath

    for path in walk(args.root):
        all_findings.extend(scan_file(path, names_regexes, ignores))

    if not args.quiet:
        cur = None
        for f in sorted(all_findings, key=lambda x: (x["file"], x["line"])):
            if f["file"] != cur:
                print(f"FILE  {f['file']}")
                cur = f["file"]
            print(f"  L{f['line']:<5} {f['category']:<12} {f['snippet']}"
                  f"  [{f['pattern']}]")

    by_cat = {}
    for f in all_findings:
        by_cat[f["category"]] = by_cat.get(f["category"], 0) + 1
    hard = sum(v for k, v in by_cat.items() if k not in REVIEW_CATEGORIES)
    total = len(all_findings)
    print(f"SUMMARY  {total} findings "
          f"({', '.join(f'{k}={v}' for k, v in sorted(by_cat.items()))}) — "
          f"{hard} hard, {total - hard} review-level")
    if total == 0:
        print("CLEAN  no findings — ready to publish (after manual review)")

    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(all_findings, fh, indent=2)

    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

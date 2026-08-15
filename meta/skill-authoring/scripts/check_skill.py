#!/usr/bin/env python3
"""check_skill.py — validate a skill folder / SKILL.md before shipping.

Usage:
    python3 check_skill.py <path> [<path> ...]
    python3 check_skill.py .              # scan every SKILL.md in the repo

Checks (ERROR unless noted):
    frontmatter : file starts with `---` and closes it
    name        : present, lowercase-hyphen-case, matches the folder name
    description : present, single-line, no markdown (WARN: no trigger phrase)
    structure   : runbook sections present (WARN when missing)
    size        : SKILL.md <= 300 lines (WARN above)
    secrets     : no embedded credentials in examples (WARN when found;
                  regex-documentation lines and `leak-guard:ignore` are skipped)

Exit code 0 = ready to ship, 1 = fix the errors first.
"""

import os
import re
import sys

VERSION = "1.0.0"

OUTCOME_VERBS = {
    "run", "operate", "write", "scan", "review", "create", "edit", "use",
    "apply", "replicate", "perform", "generate", "analyze", "audit", "install",
    "configure", "build", "test", "check", "validate", "ensure", "automate",
    "prepare", "launch", "monitor", "stop", "report", "summarize", "teach",
    "guide", "produce", "deliver", "handle", "manage", "convert", "refactor",
    "fix", "debug", "design", "document", "maintain", "set", "make", "define",
}

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

REQUIRED_SECTIONS = [
    ("when to use", "When to use"),
    ("workflow", "Workflow"),
    ("verification", "Verification"),
    ("out of scope", "Out of scope"),
    ("golden rules|hard rules", "Golden/Hard rules"),
    ("pitfalls", "Pitfalls"),
]

SECRET_PATTERNS = [
    (r"-----BEGIN (RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----", "private key block"),
    (r"AKIA[0-9A-Z]{16}", "AWS access key ID"),
    (r"ghp_[A-Za-z0-9]{36}", "GitHub token"),
    (r"sk-[A-Za-z0-9]{20,}", "OpenAI-style key"),
    (r"xox[baprs]-[A-Za-z0-9-]{10,}", "Slack token"),
    (r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}", "JWT"),
    (r"[a-z]+://[^\s/]+:[^\s@/]+@", "connection string with credentials"),
]

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
SAFE_DOMAINS = ("example.com", "example.org", "example.net", "example.test",
                "example.invalid", "example.localhost")


def find_skill_files(path):
    """Return SKILL.md paths for a file, a skill folder, or a repo root."""
    if os.path.isfile(path):
        return [path] if path.endswith("SKILL.md") else []
    if os.path.isdir(path):
        direct = os.path.join(path, "SKILL.md")
        if os.path.isfile(direct):
            return [direct]
        found = []
        for root, dirs, files in os.walk(path):
            depth = root[len(path):].count(os.sep)
            dirs[:] = [d for d in dirs if not d.startswith((".", "_"))]
            if depth > 2:  # categories/skill/SKILL.md is the deepest layout
                dirs[:] = []
                continue
            if "SKILL.md" in files:
                found.append(os.path.join(root, "SKILL.md"))
        return sorted(found)
    return []


def parse_frontmatter(text):
    """Return (frontmatter_dict, body) or (None, None) on malformed frontmatter."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, None
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return None, None
    fm, body = {}, "\n".join(lines[end + 1:])
    for line in lines[1:end]:
        if ":" in line and not line.startswith((" ", "\t")):
            key, _, value = line.partition(":")
            fm[key.strip()] = value.strip().strip("\"'").strip()
    return fm, body


def check_skill(path):
    errors, warns = [], []

    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    lines = text.splitlines()
    folder = os.path.basename(os.path.dirname(path))

    fm, body = parse_frontmatter(text)
    if fm is None:
        errors.append("frontmatter: missing or malformed (needs a leading and "
                      "trailing `---` line)")
        return errors, warns

    # --- name ---
    name = fm.get("name", "")
    if not name:
        errors.append("frontmatter: `name` is missing")
    elif not NAME_RE.match(name):
        errors.append(f"name: '{name}' is not lowercase-hyphen-case")
    elif name != folder:
        warns.append(f"name: '{name}' does not match the folder name '{folder}'")

    # --- description ---
    desc = fm.get("description", "")
    if not desc:
        errors.append("frontmatter: `description` is missing (it is the trigger)")
    else:
        if "\n" in desc:
            errors.append("description: must be a single line")
        if "\n" not in desc and len(desc) > 400:
            warns.append(f"description: {len(desc)} chars — keep it short so it "
                         "is readable at a glance")
        first = desc.strip().split()[0].lower().rstrip(".")
        if first in {"a", "an", "the"} or first == "skill":
            warns.append(f"description: starts with '{first}' — start with an "
                         "outcome verb instead")
        elif first not in OUTCOME_VERBS:
            warns.append(f"description: starts with '{first}', not an outcome "
                         "verb (Run/Operate/Write/Scan/…)")
        if not re.search(r"\b(whenever|use when|use it when)\b", desc,
                         re.IGNORECASE):
            warns.append("description: no trigger phrase ('Use whenever …') — "
                         "the description is the entire trigger")

    # --- structure ---
    if not re.search(r"^# ", text, re.MULTILINE):
        warns.append("structure: no H1 title (`# Skill Name`)")
    for pattern, label in REQUIRED_SECTIONS:
        if not re.search(rf"^#{{2,3}} .*{pattern}", text, re.IGNORECASE
                         | re.MULTILINE):
            warns.append(f"structure: no '{label}' section")
    if len(lines) > 300:
        warns.append(f"size: {len(lines)} lines — aim for <= 300 so the body "
                     "loads in one pass; move bulk to references/")

    # --- referenced folders exist (body only; ignore frontmatter mentions) ---
    for sub in ("references", "scripts", "assets"):
        if re.search(rf"{sub}/[A-Za-z0-9._-]+", body) and not os.path.isdir(
                os.path.join(os.path.dirname(path), sub)):
            warns.append(f"structure: body mentions '{sub}/…' but the folder "
                         "does not exist")

    # --- secret scan ---
    for lineno, line in enumerate(lines, 1):
        if ("leak-guard:ignore" in line or "illustrative" in line
                or "AKIAEXAMPLE" in line):  # documented placeholder example
            continue
        if "[" in line and "]" in line:   # regex documentation, not a value
            continue
        if "{" in line and "}" in line:   # regex quantifier, not a value
            continue
        for pattern, label in SECRET_PATTERNS:
            if re.search(pattern, line):
                warns.append(f"secrets: line {lineno}: possible {label} — "
                             "replace with a placeholder (see leak-guard)")
                break
        if EMAIL_RE.search(line) and not any(
                d in line.lower() for d in SAFE_DOMAINS):
            warns.append(f"secrets: line {lineno}: possible real email — use "
                         "user@example.com instead")

    return errors, warns


def main(argv):
    if not argv:
        print("usage: check_skill.py <path> [<path> ...]  ('.' scans the repo)")
        return 2
    total_err = total_warn = 0
    for arg in argv:
        files = find_skill_files(arg)
        if not files:
            print(f"  ERROR  {arg}: no SKILL.md found")
            total_err += 1
            continue
        for path in files:
            errors, warns = check_skill(path)
            total_err += len(errors)
            total_warn += len(warns)
            print(f"CHECK  {path}")
            for msg in errors:
                print(f"  ERROR  {msg}")
            for msg in warns:
                print(f"  WARN   {msg}")
            if not errors and not warns:
                print("  OK     frontmatter, naming, structure, hygiene — "
                      "ready to ship")
            print(f"RESULT {path}: {len(errors)} errors, {len(warns)} warnings")
    print(f"\nTOTAL: {total_err} errors, {total_warn} warnings")
    return 1 if total_err else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

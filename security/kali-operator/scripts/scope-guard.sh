#!/usr/bin/env bash
# scope-guard.sh — Check if a target is within the authorized scope before acting.
# Usage: bash scope-guard.sh <target> <scope-file>
# scope-file format: one target per line (IP, CIDR, domain, or hostname)
# Exit codes: 0=in scope, 1=out of scope, 2=error
set -o pipefail

TARGET="${1:?Usage: $0 <target> <scope-file>}"
SCOPE_FILE="${2:?Usage: $0 <target> <scope-file>}"

if [[ ! -f "$SCOPE_FILE" ]]; then
  echo "[!] Scope file not found: $SCOPE_FILE" >&2
  exit 2
fi

# Normalize target: strip protocol, path, port
TARGET_CLEAN=$(echo "$TARGET" | sed 's|^[a-z]*://||' | sed 's|[:/].*$||' | tr '[:upper:]' '[:lower:]')

# Check exact match first
if grep -qx "$TARGET_CLEAN" "$SCOPE_FILE" 2>/dev/null; then
  echo "[+] In scope (exact match): $TARGET_CLEAN"
  exit 0
fi

# Check CIDR match (if target is an IP)
if [[ "$TARGET_CLEAN" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  while IFS= read -r line || [ -n "$line" ]; do
    line=$(echo "$line" | tr '[:upper:]' '[:lower:]' | xargs)
    [ -z "$line" ] && continue
    [ "${line:0:1}" = "#" ] && continue
    if [[ "$line" == */* ]]; then
      python3 -c "
import ipaddress, sys
net = ipaddress.ip_network('$line', strict=False)
addr = ipaddress.ip_address('$TARGET_CLEAN')
sys.exit(0 if addr in net else 1)
" 2>/dev/null
      if [ $? -eq 0 ]; then
        echo "[+] In scope (CIDR match): $TARGET_CLEAN ∈ $line"
        exit 0
      fi
    fi
  done < "$SCOPE_FILE"
fi

# Check domain suffix match (subdomain of a scoped domain)
while IFS= read -r line || [ -n "$line" ]; do
  line=$(echo "$line" | tr '[:upper:]' '[:lower:]' | xargs)
  [ -z "$line" ] && continue
  [ "${line:0:1}" = "#" ] && continue
  if [[ "$TARGET_CLEAN" == *."$line" || "$TARGET_CLEAN" == "$line" ]]; then
    echo "[+] In scope (domain suffix match): $TARGET_CLEAN ∈ $line"
    exit 0
  fi
done < "$SCOPE_FILE"

echo "[-] OUT OF SCOPE: $TARGET_CLEAN" >&2
echo "    Checked against: $SCOPE_FILE" >&2
exit 1

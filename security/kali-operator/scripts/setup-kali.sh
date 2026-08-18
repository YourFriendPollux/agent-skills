#!/usr/bin/env bash
# setup-kali.sh — Install/update common pentest tools on Kali Linux.
# Usage: bash setup-kali.sh [--category <name>] [--check-only]
# Categories: recon, web, network, exploit, post-exploit, crypto, forensic, all
set -euo pipefail

CHECK_ONLY=false
CATEGORY="all"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --check-only) CHECK_ONLY=true; shift ;;
    --category) CATEGORY="$2"; shift 2 ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

if [[ "$CHECK_ONLY" == true ]]; then
  exec bash "$(dirname "$0")/check-tools.sh" --category "$CATEGORY"
fi

echo "[+] Updating apt repositories..."
sudo apt update -qq

echo "[+] Installing apt packages..."
APT_PACKAGES=(
  nmap masscan dnsutils subfinder amass assetfinder
  ffuf feroxbuster gobuster nikto whatweb wpscan sqlmap
  tcpdump tshark smbclient snmp nfs-common responder
  metasploit-framework exploitdb binwalk rlwrap
  hashcat john hydra
  autopsy sleuthkit foremost libimage-exiftool-perl
  ghidra radare2 gdb strace ltrace
  theharvester spiderfoot
  jq proxychains4 tmux
)
sudo apt install -y -qq "${APT_PACKAGES[@]}"

echo "[+] Installing Go tools..."
GO_TOOLS=(
  "github.com/projectdiscovery/httpx/cmd/httpx@latest"
  "github.com/projectdiscovery/dnsx/cmd/dnsx@latest"
  "github.com/projectdiscovery/katana/cmd/katana@latest"
  "github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest"
  "github.com/lc/gau/v2/cmd/gau@latest"
  "github.com/tomnomnom/waybackurls@latest"
  "github.com/d3mondev/puredns/v2@latest"
  "github.com/hahwul/dalfox/v2@latest"
)
for tool in "${GO_TOOLS[@]}"; do
  echo "  Installing: $tool"
  go install -v "$tool" 2>/dev/null || echo "  [!] Failed: $tool"
done

echo "[+] Installing pipx tools..."
PIPX_TOOLS=(
  enum4linux-ng
  dirsearch
  arjun
  jwt_tool
  netexec
  impacket
  bloodhound
  certipy-ad
  volatility3
  sherlock-project
)
for tool in "${PIPX_TOOLS[@]}"; do
  echo "  Installing: $tool"
  pipx install "$tool" 2>/dev/null || echo "  [!] Failed: $tool (may already be installed)"
done

echo "[+] Downloading linpeas..."
mkdir -p ~/Tools
curl -sL https://github.com/peass-ng/PEASS-ng/releases/latest/download/linpeas.sh -o ~/Tools/linpeas.sh
chmod +x ~/Tools/linpeas.sh

echo "[+] Setup complete. Run check-tools.sh to verify."

#!/usr/bin/env bash
# check-tools.sh — Verify which pentest/security tools are installed.
# Usage: bash check-tools.sh [--category <name>]
# Categories: recon, web, network, exploit, post-exploit, crypto, forensic, all
set -euo pipefail

CATEGORY="all"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --category) CATEGORY="$2"; shift 2 ;;
    *) CATEGORY="$1"; shift ;;
  esac
done

# Tool definitions: tool_name|category|install_hint
TOOLS=(
  # Recon
  "nmap|recon|apt install nmap"
  "masscan|recon|apt install masscan"
  "rustscan|recon|cargo install rustscan"
  "dig|recon|apt install dnsutils"
  "subfinder|recon|go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"
  "amass|recon|apt install amass"
  "httpx|recon|go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest"
  "dnsx|recon|go install -v github.com/projectdiscovery/dnsx/cmd/dnsx@latest"
  "assetfinder|recon|apt install assetfinder"
  "gau|recon|go install github.com/lc/gau/v2/cmd/gau@latest"
  "katana|recon|go install -v github.com/projectdiscovery/katana/cmd/katana@latest"
  "waybackurls|recon|go install -v github.com/tomnomnom/waybackurls@latest"
  "puredns|recon|go install github.com/d3mondev/puredns/v2@latest"
  # Web
  "ffuf|web|apt install ffuf"
  "feroxbuster|web|apt install feroxbuster"
  "gobuster|web|apt install gobuster"
  "dirsearch|web|pipx install dirsearch"
  "nikto|web|apt install nikto"
  "whatweb|web|apt install whatweb"
  "wpscan|web|apt install wpscan"
  "arjun|web|pipx install arjun"
  "nuclei|web|go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest"
  "sqlmap|web|apt install sqlmap"
  "jwt_tool|web|pipx install jwt_tool"
  "dalfox|web|go install -v github.com/hahwul/dalfox/v2@latest"
  # Network
  "tcpdump|network|apt install tcpdump"
  "tshark|network|apt install tshark"
  "enum4linux-ng|network|pipx install enum4linux-ng"
  "smbclient|network|apt install smbclient"
  "snmpwalk|network|apt install snmp"
  "showmount|network|apt install nfs-common"
  "netexec|network|pipx install netexec"
  "crackmapexec|network|pipx install crackmapexec"
  "impacket-smbexec|network|pipx install impacket"
  "impacket-psexec|network|pipx install impacket"
  "impacket-secretsdump|network|pipx install impacket"
  "responder|network|apt install responder"
  " Wireshark|network|apt install wireshark"
  # Exploit
  "msfconsole|exploit|apt install metasploit-framework"
  "searchsploit|exploit|apt install exploitdb"
  "binwalk|exploit|apt install binwalk"
  "rlwrap|exploit|apt install rlwrap"
  # Post-exploit
  "linpeas|post-exploit|curl -L https://github.com/peass-ng/PEASS-ng/releases/latest/download/linpeas.sh -o ~/Tools/linpeas.sh"
  "bloodhound-python|post-exploit|pipx install bloodhound"
  "certipy|post-exploit|pipx install certipy-ad"
  "GetUserSPNs|post-exploit|pipx install impacket"
  "GetNPUsers|post-exploit|pipx install impacket"
  # Crypto
  "hashcat|crypto|apt install hashcat"
  "john|crypto|apt install john"
  "hydra|crypto|apt install hydra"
  # Forensic
  "volatility|forensic|pipx install volatility3"
  "autopsy|forensic|apt install autopsy"
  "sleuthkit|forensic|apt install sleuthkit"
  "foremost|forensic|apt install foremost"
  "exiftool|forensic|apt install libimage-exiftool-perl"
  # RE
  "ghidra|re|apt install ghidra"
  "radare2|re|apt install radare2"
  "gdb|re|apt install gdb"
  "strace|re|apt install strace"
  "ltrace|re|apt install ltrace"
  # OSINT
  "theHarvester|osint|apt install theharvester"
  "spiderfoot|osint|apt install spiderfoot"
  "sherlock|osint|pipx install sherlock-project"
  # Misc
  "jq|misc|apt install jq"
  "proxychains|misc|apt install proxychains4"
  "rlwrap|misc|apt install rlwrap"
  "tmux|misc|apt install tmux"
  "gobuster|misc|apt install gobuster"
)

print_header() {
  echo "CATEGORY: $1"
  printf "%-25s %-15s %-15s %s\n" "TOOL" "STATUS" "CATEGORY" "INSTALL"
  printf "%-25s %-15s %-15s %s\n" "-------------------------" "---------------" "---------------" "----------"
}

check_tool() {
  local entry="$1"
  IFS='|' read -r name category install <<< "$entry"
  name=$(echo "$name" | xargs)  # trim whitespace
  if [[ "$CATEGORY" != "all" && "$category" != "$CATEGORY" ]]; then
    return
  fi
  if command -v "$name" &>/dev/null; then
    printf "%-25s %-15s %-15s %s\n" "$name" "OK" "$category" "-"
  else
    printf "%-25s %-15s %-15s %s\n" "$name" "MISSING" "$category" "$install"
  fi
}

print_header "$CATEGORY"
for entry in "${TOOLS[@]}"; do
  check_tool "$entry"
done

echo ""
echo "Summary:"
total=0
found=0
for entry in "${TOOLS[@]}"; do
  IFS='|' read -r name category _ <<< "$entry"
  name=$(echo "$name" | xargs)
  if [[ "$CATEGORY" != "all" && "$category" != "$CATEGORY" ]]; then
    continue
  fi
  total=$((total + 1))
  if command -v "$name" &>/dev/null; then
    found=$((found + 1))
  fi
done
echo "  $found / $total tools installed"

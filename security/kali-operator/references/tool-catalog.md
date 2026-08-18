# Tool Catalog

Reference catalog of security tools by category. A tool's output is an
**observation**, not a conclusion. Distinguish `OBSERVATION / HYPOTHESIS /
CONFIRMATION / UNCERTAINTY`. A version guessed from a banner is not proof of a
CVE.

Use `scripts/check-tools.sh` to verify which tools are installed.
Use `scripts/setup-kali.sh` to install missing tools.

## Recon & Discovery

| Tool | Purpose | Key flags | Alternatives | Limits |
|------|---------|-----------|--------------|--------|
| `nmap` | Port/service/OS discovery | `-sV -sC -p- --min-rate 300` | `masscan`, `rustscan` | Version guesses need CVE validation; rate limits |
| `masscan` | Fast port scan (all ports) | `--rate 1000 -p1-65535` | `nmap`, `rustscan` | No service detection; pair with nmap |
| `rustscan` | Fast port scanner (Rust) | `-a <host> -- -sV -sC` | `nmap` | Wraps nmap for service detection |
| `arp-scan` | Host discovery on LAN | `--localnet` | `fping`, `nmap -sn` | Only finds hosts that answer ARP |
| `httpx` | HTTP probing in bulk | `-l hosts.txt -mc 200,301 -status-code -title -tech-detect` | `httprobe` | Banner-based tech detection can be wrong |
| `dig` | DNS queries | `ANY`, `MX`, `TXT`, `AXFR` | `host`, `nslookup`, `dnsx` | Zone transfer usually refused (not a vuln) |
| `dnsx` | DNS resolution in bulk | `-d domains.txt -a -resp` | `dig`, `fierce` | |
| `subfinder` | Subdomain enumeration (passive) | `-d domain -all -recursive` | `amass`, `assetfinder` | Public data only; noise |
| `amass` | Subdomain + OSINT enum | `enum -passive -d domain` | `subfinder` | Heavy; slow in active mode |
| `puredns` | Subdomain bruteforce + resolving | `bruteforce wordlist domain` | `ffuf` vhost mode | Requires resolvers list |
| `gau` | Fetch URLs from Wayback/Common Crawl | `--threads 10` | `waybackurls` | Historical data; may be stale |
| `katana` | Web crawling | `-u url -mode active -jc -d 3` | `hakrawler` | JS rendering needs headless mode |
| `waybackurls` | Wayback Machine URL fetch | `domain` | `gau` | |
| `crystal` | Tech fingerprint from terminal | | `whatweb`, `wappalyzer` | |

## Web Application Testing

| Tool | Purpose | Key flags | Alternatives | Limits |
|------|---------|-----------|--------------|--------|
| `ffuf` | Directory/vhost/param brute | `-u URL/FUZZ -w wordlist -mc 200,301,403 -recursion` | `feroxbuster`, `gobuster` | Wordlist-dependent; 403/404 noise |
| `feroxbuster` | Recursive content discovery | `-u URL --depth 2` | `ffuf`, `gobuster` | |
| `gobuster` | Directory/vhost brute | `dir -u URL -w wordlist -x php,html,txt` | `ffuf` | Simpler than ffuf but less flexible |
| `dirsearch` | Directory scanner | `-u URL` | `ffuf` | |
| `nikto` | Web vuln scanner | `-h host -p port` | `nuclei` | Many low-value findings; verify manually |
| `nuclei` | Template-based vuln scanner | `-u URL -t cves/ -t technologies/ -severity high,critical` | `nikto` | Template FP rate; confirm each hit |
| `whatweb` | Tech fingerprint | `-a 3 URL` | `httpx -tech-detect` | Banner-based |
| `wpscan` | WordPress scanner | `--url URL --enumerate u,p,t` | | WordPress only; API key for full DB |
| `arjun` | HTTP parameter discovery | `-u URL` | `paramspider` | |
| `sqlmap` | SQLi detection & exploitation | `-u URL --batch --level 3 --risk 2` | manual `curl` | High request count; use carefully |
| `jwt_tool` | JWT analysis & attacks | `-t token -C -d rockyou.txt` | `jwt-cracker` | |
| `dalfox` | XSS scanner | `url URL --blind https://oast.pro` | manual payloads | FP rate; verify |
| `testssl.sh` | TLS/SSL audit | `host:port` | `sslscan`, `sslyze` | Cipher weakness ≠ exploitability |
| `sslscan` | TLS scan | `host` | `testssl.sh` | |
| `curl` | HTTP requests | `-sI`, `-X POST`, `-d`, `-F` | `httpie` | Manual; not a scanner |

## Network Services

| Tool | Purpose | Key flags | Alternatives | Limits |
|------|---------|-----------|--------------|--------|
| `enum4linux-ng` | SMB/NetBIOS enumeration | `-A host` | `smbclient`, `nmap` scripts | |
| `smbclient` | SMB share access | `-L //host -N` | ` CrackMapExec` | Null session may be refused |
| `netexec` | Network exec (CME successor) | `smb host -u user -p pass --shares` | `crackmapexec` | In-scope AD only |
| `crackmapexec` | Network exec (legacy) | `smb host -u user -p pass` | `netexec` | Deprecated; use netexec |
| `ldapsearch` | LDAP queries | `-x -H ldap://host -s base` | `nmap --script ldap-*` | |
| `snmpwalk` | SNMP enumeration | `-v2c -c public host` | `onesixtyone` | Default community only |
| `showmount` | NFS exports | `-e host` | `nmap --script nfs-*` | |
| `tcpdump` | Packet capture | `-i eth0 -w capture.pcap` | `tshark` | Needs capture perms |
| `tshark` | Packet analysis (CLI Wireshark) | `-r capture.pcap -Y "http"` | `wireshark` (GUI) | |
| `responder` | LLMNR/NBT-NS poisoner | `-I eth0 -rdPv` | ` inveigh` | Offensive; authorized scope only |
| `impacket-*` | Windows protocol toolkit | `psexec`, `secretsdump`, `mssqlclient`, `wmiexec` | `netexec` | In-scope only; no persistence |

## Exploitation

| Tool | Purpose | Key flags | Alternatives | Limits |
|------|---------|-----------|--------------|--------|
| `msfconsole` | Exploitation framework | `use exploit/...; set RHOSTS; run` | `searchsploit`, manual PoC | Lab/CTF only; verify payloads |
| `searchsploit` | Exploit-DB search | `search term` | `nvd.nist.gov` | PoC may be unvalidated; test in lab |
| `binwalk` | Firmware/binary analysis | `-e firmware.bin` | `foremost` | |
| `rlwrap` | Reverse shell upgrade | `rlwrap nc -lvnp 4444` | `pwntools` | |

## Post-Exploitation

| Tool | Purpose | Key flags | Alternatives | Limits |
|------|---------|-----------|--------------|--------|
| `linpeas` | Linux privesc enumeration | `./linpeas.sh -a 2` | manual `find`, `sudo -l` | Output is leads, not verdicts |
| `winpeas` | Windows privesc enumeration | `winpeas.exe` | `Seatbelt`, `PowerUp` | Same — leads only |
| `pspy` | Process monitor (no root) | `./pspy64` | | |
| `bloodhound-python` | AD data collector | `-d domain -u user -p pass -ns DC -c All` | `SharpHound` | Requires valid creds; read-only |
| `certipy` | AD CS abuse | `find -u user -p pass -dc-ip DC` | | ESC1-8 misconfigs |
| `GetUserSPNs.py` | Kerberoasting | `-dc-ip DC domain/user:pass -request` | `netexec` | In-scope only |
| `GetNPUsers.py` | AS-REP roasting | `-dc-ip DC -usersfile users.txt domain/` | | |

## Crypto & Passwords

| Tool | Purpose | Key flags | Alternatives | Limits |
|------|---------|-----------|--------------|--------|
| `hashcat` | GPU hash cracking | `-m 13100 hashes.txt wordlist` | `john` | Only authorized/in-scope hashes |
| `john` | CPU hash cracking | `--wordlist=rockyou.txt hashes` | `hashcat` | Slower than hashcat GPU |
| `hydra` | Online brute force | `-L users -P passes ssh://host` | `netexec` | Noisy; respect rate limits |
| `cewl` | Wordlist from website | `--depth 2 -w list.txt URL` | `crunch` | |
| `crunch` | Pattern wordlist gen | `8 8 -t admin@@@` | `cewl` | |

## Forensics

| Tool | Purpose | Key flags | Alternatives | Limits |
|------|---------|-----------|--------------|--------|
| `volatility` | Memory forensics | `-f memory.dmp windows.info` | `rekall` | Needs matching profile/symbols |
| `sleuthkit` | Disk image analysis | `tsk_list`, `fls`, `icat` | `autopsy` (GUI) | Operate on copies, not originals |
| `autopsy` | Forensic GUI (sleuthkit) | | `sleuthkit` CLI | |
| `foremost` | File carving | `-i image -o output/` | `photorec` | |
| `exiftool` | Metadata reader | `file.jpg` | `strings` | Metadata may be innocuous |
| `binwalk` | Firmware extraction | `-e firmware.bin` | | |

## Reverse Engineering

| Tool | Purpose | Key flags | Alternatives | Limits |
|------|---------|-----------|--------------|--------|
| `ghidra` | Disassembler/decompiler (GUI) | | `radare2`, `IDA` | Static analysis; sanitize before running |
| `radare2` | Disassembler (CLI) | `r2 binary`, `aaa`, `pdf` | `ghidra` | |
| `gdb` | Debugger | `gef`/`pwndbg` recommended | `lldb` | |
| `objdump` | Disassembler | `-d binary` | `radare2` | |
| `strace` | Syscall trace | `-p pid` | `ltrace` | |
| `ltrace` | Library call trace | `./binary` | `strace` | |

## OSINT

| Tool | Purpose | Key flags | Alternatives | Limits |
|------|---------|-----------|--------------|--------|
| `theHarvester` | Email/subdomain harvest | `-d domain -b all` | `recon-ng` | Public data only; dedupe |
| `recon-ng` | OSINT framework | | `spiderfoot` | |
| `spiderfoot` | OSINT automation | `-s target -t all` | `theHarvester` | Heavy; many modules need API keys |
| `sherlock` | Username search | `username` | `holehe` | |

## Utility

| Tool | Purpose | Key flags | Alternatives | Limits |
|------|---------|-----------|--------------|--------|
| `jq` | JSON processor | `.field`, `-r` | `python -m json.tool` | |
| `proxychains` | Proxy traffic | `proxychains nmap -sT host` | | TCP only; no UDP/ICMP |
| `tmux` | Terminal multiplexer | `new -s pentest` | `screen` | |
| `rlwrap` | Readline wrapper | `rlwrap nc -lvnp 4444` | | |
| `seclists` | Wordlist collection | `/usr/share/seclists/` | `SecLists` repo | |

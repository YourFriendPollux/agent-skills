# Wordlist Reference

Guide des wordlists disponibles sur Kali (SecLists et autres) avec cas d'usage.

## SecLists — /usr/share/seclists/

Collection principale. Installer : `sudo apt install seclists`

### Directory brute-force

| Wordlist | Taille | Usage |
|----------|--------|-------|
| `Discovery/Web-Content/raft-medium-directories.txt` | ~65K | Scan général — équilibre couverture/vitesse |
| `Discovery/Web-Content/raft-large-directories.txt` | ~350K | Scan exhaustif — lent |
| `Discovery/Web-Content/directory-list-2.3-medium.txt` | ~220K | Alternative classique |
| `Discovery/Web-Content/common.txt` | ~4.6K | Scan rapide — premier passage |
| `Discovery/Web-Content/raft-small-directories.txt` | ~18K | Scan rapide alternatif |

### File brute-force

| Wordlist | Taille | Usage |
|----------|--------|-------|
| `Discovery/Web-Content/raft-medium-files.txt` | ~57K | Fichiers communs |
| `Discovery/Web-Content/raft-large-files.txt` | ~330K | Exhaustif |
| `Discovery/Web-Content/common-files.txt` | ~3.6K | Rapide |

### API endpoints

| Wordlist | Taille | Usage |
|----------|--------|-------|
| `Discovery/Web-Content/api/api-endpoints.txt` | ~20K | API REST endpoints |
| `Discovery/Web-Content/api/api-seen-in-wild.txt` | ~7K | APIs vues dans la nature |
| `Discovery/Web-Content/api/objects.txt` | ~5K | Noms d'objets API |

### Parameters

| Wordlist | Taille | Usage |
|----------|--------|-------|
| `Discovery/Web-Content/burp-parameter-names.txt` | ~6.4K | Noms de paramètres HTTP |
| `Discovery/Web-Content/arjun-lists/` | variables | Listes Arjun (GET/POST/JSON) |

### Subdomains

| Wordlist | Taille | Usage |
|----------|--------|-------|
| `Discovery/DNS/subdomains-top1million-20000.txt` | ~20K | Top 20K subdomains |
| `Discovery/DNS/subdomains-top1million-110000.txt` | ~110K | Top 110K |
| `Discovery/DNS/bitquark-subdomains-top100000.txt` | ~100K | Alternative |

### Usernames

| Wordlist | Taille | Usage |
|----------|--------|-------|
| `Usernames/Names/names.txt` | ~10K | Noms communs |
| `Usernames/Names/malenames-uspa-top1000.txt` | ~1K | Top 1000 noms masculins US |
| `Usernames/xato-net-10-million-usernames.txt` | ~10M | Massif — bruteforce |

### Passwords

| Wordlist | Taille | Usage |
|----------|--------|-------|
| `Passwords/Common-Credentials/10-million-password-list-top-1000.txt` | ~1K | Top 1000 — rapide |
| `Passwords/Common-Credentials/10-million-password-list-top-100000.txt` | ~100K | Top 100K |
| `Passwords/Leaked-Databases/rockyou-75.txt` | ~7.5K | Rockyou top 75K |
| `/usr/share/wordlists/rockyou.txt` | ~14M | Rockyou complet — référence |

### Payloads

| Wordlist | Taille | Usage |
|----------|--------|-------|
| `Fuzzing/SQLi/Generic-SQLi.txt` | ~400 | Payloads SQLi génériques |
| `Fuzzing/XSS/XSS-Bypass.txt` | ~100 | Payloads XSS bypass WAF |
| `Fuzzing/XSS/xml.txt` | ~300 | XSS contextes XML |
| `Fuzzing/Command-Injection/commix.txt` | ~300 | Command injection payloads |
| `Fuzzing/LFI/LFI-Jhaddix.txt` | ~900 | LFI payloads |
| `Fuzzing/Traverse-Directory/cluster.txt` | ~100 | Path traversal |
| `Fuzzing/User-Agents/User-Agents.txt` | ~2K | User agents pour rotation |

## Autres wordlists sur Kali

| Path | Usage |
|------|-------|
| `/usr/share/wordlists/rockyou.txt` | Mot de passe — référence (14M) |
| `/usr/share/wordlists/metasploit/unix_passwords.txt` | Mots de passe Unix |
| `/usr/share/wordlists/metasploit/unix_users.txt` | Usernames Unix |
| `/usr/share/wordlists/wfuzz/others/common_pass.txt` | Mots de passe communs |
| `/usr/share/nmap/nselib/data/passwords.lst` | Nmap passwords |
| `/usr/share/nmap/nselib/data/usernames.lst` | Nmap usernames |

## Sélection par contexte

| Contexte | Wordlist | Rationale |
|----------|----------|-----------|
| Premier passage rapide | `common.txt` | Couvre 90% des dirs communs en secondes |
| Scan complet | `raft-medium-directories.txt` | Meilleur ratio couverture/temps |
| API discovery | `api-endpoints.txt` + `burp-parameter-names.txt` | Spécialisé API |
| Subdomain bruteforce | `subdomains-top1million-20000.txt` | Top 20K suffit la plupart du temps |
| Password spraying | `10-million-top-1000.txt` | Rapide, couvre les plus fréquents |
| Hash cracking offline | `rockyou.txt` | Référence absolue |
| SQLi fuzzing | `Generic-SQLi.txt` | Payloads testés |
| Path traversal | `LFI-Jhaddix.txt` | Liste de référence LFI |

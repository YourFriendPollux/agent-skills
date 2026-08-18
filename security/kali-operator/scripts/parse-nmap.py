#!/usr/bin/env python3
"""parse-nmap.py — Parse nmap grepable output and extract structured data.

Usage:
  nmap -sV -sC -p- --min-rate 300 <host> -oG scan.gnmap
  python3 parse-nmap.py scan.gnmap [--format json|csv|table]

Output formats:
  table  — human-readable table (default)
  json   — structured JSON
  csv    — CSV for import in other tools
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path


def parse_grepable(filepath: Path) -> list[dict]:
    """Parse nmap grepable output (.gnmap) into list of host dicts."""
    hosts = []
    with open(filepath, encoding="utf-8", errors="replace") as f:
        for line in f:
            if not line.startswith("Host:"):
                continue
            host = {"ip": "", "hostname": "", "state": "", "ports": []}
            # Host: 192.0.2.10 (example.com)     Status: Up
            host_match = re.match(r"Host:\s+(\S+)\s+\(([^)]*)\)\s+Status:\s+(\w+)", line)
            if host_match:
                host["ip"] = host_match.group(1)
                host["hostname"] = host_match.group(2)
                host["state"] = host_match.group(3)
                hosts.append(host)
                continue
            # Host: 192.0.2.10 (example.com)     Ports: 22/open/tcp//ssh/OpenSSH 8.9p1...
            ports_match = re.match(
                r"Host:\s+(\S+)\s+\(([^)]*)\)\s+Ports:\s+(.*)", line
            )
            if ports_match:
                host["ip"] = ports_match.group(1)
                host["hostname"] = ports_match.group(2)
                ports_str = ports_match.group(3)
                for port_entry in ports_str.split(","):
                    port_entry = port_entry.strip()
                    if not port_entry:
                        continue
                    # Format: 22/open/tcp//ssh/OpenSSH 8.9p1 Ubuntu 3ubuntu0.1
                    parts = port_entry.split("/")
                    if len(parts) >= 5:
                        host["ports"].append(
                            {
                                "port": parts[0],
                                "state": parts[1],
                                "protocol": parts[2],
                                "owner": parts[3],
                                "service": parts[4],
                                "version": parts[5] if len(parts) > 5 else "",
                            }
                        )
                host["state"] = "Up" if host["ports"] else "Unknown"
                hosts.append(host)
    return hosts


def print_table(hosts: list[dict]):
    """Print human-readable table."""
    for host in hosts:
        print(f"\n{'='*60}")
        print(f"Host: {host['hostname'] or 'N/A'} ({host['ip']})")
        print(f"State: {host['state']}")
        if host["ports"]:
            print(f"{'PORT':<10} {'STATE':<8} {'SERVICE':<15} {'VERSION'}")
            print(f"{'-'*10} {'-'*8} {'-'*15} {'-'*30}")
            for p in host["ports"]:
                version = p["version"][:50] if p["version"] else ""
                print(
                    f"{p['port']+'/'+p['protocol']:<10} {p['state']:<8} {p['service']:<15} {version}"
                )
        else:
            print("  No open ports")


def print_json(hosts: list[dict]):
    print(json.dumps(hosts, indent=2))


def print_csv(hosts: list[dict]):
    writer = csv.writer(sys.stdout)
    writer.writerow(["ip", "hostname", "state", "port", "protocol", "service", "version"])
    for host in hosts:
        if not host["ports"]:
            writer.writerow([host["ip"], host["hostname"], host["state"], "", "", "", ""])
        for p in host["ports"]:
            writer.writerow(
                [
                    host["ip"],
                    host["hostname"],
                    host["state"],
                    p["port"],
                    p["protocol"],
                    p["service"],
                    p["version"],
                ]
            )


def main():
    parser = argparse.ArgumentParser(description="Parse nmap grepable output.")
    parser.add_argument("file", help="Path to .gnmap file")
    parser.add_argument(
        "--format", "-f", choices=["table", "json", "csv"], default="table"
    )
    args = parser.parse_args()

    filepath = Path(args.file)
    if not filepath.exists():
        print(f"[!] File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    hosts = parse_grepable(filepath)
    if not hosts:
        print("[!] No hosts found in file", file=sys.stderr)
        sys.exit(1)

    if args.format == "json":
        print_json(hosts)
    elif args.format == "csv":
        print_csv(hosts)
    else:
        print_table(hosts)


if __name__ == "__main__":
    main()

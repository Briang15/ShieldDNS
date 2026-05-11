import requests
import os
import datetime

SOURCES = {
    "stevenblack": "https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts",
    "adguard_dns": "https://adguardteam.github.io/AdGuardSDNSFilter/Filters/filter.txt",
    "easyprivacy":  "https://easylist.to/easylist/easyprivacy.txt",
}

BLOCKLIST_PATH = os.path.join(os.path.dirname(__file__), "blocklists", "blocked_domains.txt")


def parse_hosts_format(text):
    domains = set()
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) >= 2 and parts[0] in ("0.0.0.0", "127.0.0.1"):
            domain = parts[1].lower()
            if "." in domain and domain not in ("localhost", "0.0.0.0"):
                domains.add(domain)
    return domains


def parse_adblock_format(text):
    domains = set()
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith(("!", "[", "#")):
            continue
        if line.startswith("||") and line.endswith("^"):
            domain = line[2:-1].lower()
            if "." in domain and "/" not in domain and "*" not in domain:
                domains.add(domain)
    return domains


def fetch(name, url):
    print(f"  Fetching {name}...")
    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        print(f"  OK {name} - {len(r.text):,} bytes")
        return r.text
    except Exception as e:
        print(f"  FAILED {name}: {e}")
        return ""


def update():
    print("\n=== ShieldDNS Blocklist Updater ===")
    print(f"Started: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    all_domains = set()

    text = fetch("stevenblack", SOURCES["stevenblack"])
    if text:
        domains = parse_hosts_format(text)
        print(f"  -> {len(domains):,} domains\n")
        all_domains.update(domains)

    text = fetch("adguard_dns", SOURCES["adguard_dns"])
    if text:
        domains = parse_adblock_format(text)
        print(f"  -> {len(domains):,} domains\n")
        all_domains.update(domains)

    text = fetch("easyprivacy", SOURCES["easyprivacy"])
    if text:
        domains = parse_adblock_format(text)
        print(f"  -> {len(domains):,} domains\n")
        all_domains.update(domains)

    os.makedirs(os.path.dirname(BLOCKLIST_PATH), exist_ok=True)
    with open(BLOCKLIST_PATH, "w") as f:
        f.write(f"# ShieldDNS blocklist - updated {datetime.datetime.now().isoformat()}\n")
        f.write(f"# Total domains: {len(all_domains):,}\n\n")
        for domain in sorted(all_domains):
            f.write(domain + "\n")

    print(f"=== Done ===")
    print(f"Total unique domains blocked: {len(all_domains):,}")
    print(f"Saved to: {BLOCKLIST_PATH}\n")
    return len(all_domains)


if __name__ == "__main__":
    update()

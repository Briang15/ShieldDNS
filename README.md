# ShieldDNS

System-wide ad and tracker blocker for Windows and Android.

## How It Works

Every ad makes a DNS request first. ShieldDNS intercepts that and returns nothing. Ad never loads.

- Windows: writes blocked domains to the system hosts file
- Android: local VPN intercepts DNS queries (Phase 3)

## Structure

    shielddns/
    core/
        update_blocklist.py   # Downloads blocklists
        checker.py            # Domain lookup engine
        blocklists/blocked_domains.txt
    windows/
        hosts_manager.py      # Windows hosts file manager
    android/                  # Phase 3

## Quickstart (Windows)

    pip install requests
    python core/update_blocklist.py
    python windows/hosts_manager.py   # Run as Administrator

## Blocklist Sources

- Steven Black hosts list (~100k domains)
- AdGuard DNS Filter (~50k domains)
- EasyPrivacy (~40k domains)

## Roadmap

- [x] Phase 1 - Blocklist engine
- [x] Phase 2A - Windows hosts file manager
- [ ] Phase 2B - Windows local DNS server
- [ ] Phase 3 - Android VPN-based blocker
- [ ] Phase 4 - GUI polish
- [ ] Phase 5 - Whitelist + per-category blocking

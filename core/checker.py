import os

BLOCKLIST_PATH = os.path.join(os.path.dirname(__file__), "blocklists", "blocked_domains.txt")

# Loaded domains stored as a set for O(1) lookups
_blocked = set()
_loaded = False


def load_blocklist():
    global _blocked, _loaded
    if not os.path.exists(BLOCKLIST_PATH):
        print("No blocklist found. Run update_blocklist.py first.")
        return 0

    _blocked = set()
    with open(BLOCKLIST_PATH, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                _blocked.add(line)

    _loaded = True
    print(f"Blocklist loaded: {len(_blocked):,} domains")
    return len(_blocked)


def is_blocked(domain):
    if not _loaded:
        load_blocklist()

    domain = domain.lower().rstrip(".")

    # Direct match
    if domain in _blocked:
        return True

    # Check parent domains — e.g. sub.ads.example.com -> ads.example.com -> example.com
    parts = domain.split(".")
    for i in range(1, len(parts) - 1):
        parent = ".".join(parts[i:])
        if parent in _blocked:
            return True

    return False


def stats():
    if not _loaded:
        load_blocklist()
    return len(_blocked)


# Quick test when run directly
if __name__ == "__main__":
    load_blocklist()
    test_domains = [
        "doubleclick.net",
        "google.com",
        "ads.google.com",
        "facebook.com",
        "pixel.facebook.com",
        "github.com",
        "googletagmanager.com",
        "amazon.com",
        "s.amazon-adsystem.com",
    ]
    print("\n--- Domain Check ---")
    for d in test_domains:
        status = "BLOCKED" if is_blocked(d) else "allowed"
        print(f"  {status:7}  {d}")

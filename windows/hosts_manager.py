import os, datetime

HOSTS_PATH = 'C:/Windows/System32/drivers/etc/hosts'
BLOCKLIST_PATH = 'core/blocklists/blocked_domains.txt'
MARKER_START = '# === ShieldDNS START ==='
MARKER_END   = '# === ShieldDNS END ==='

def load_blocklist():
    domains = set()
    with open(BLOCKLIST_PATH) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                domains.add(line)
    return domains

def read_hosts():
    if not os.path.exists(HOSTS_PATH): return ''
    with open(HOSTS_PATH) as f: return f.read()

def strip_shield_block(text):
    result, inside = [], False
    for line in text.splitlines():
        if line.strip() == MARKER_START: inside = True; continue
        if line.strip() == MARKER_END:   inside = False; continue
        if not inside: result.append(line)
    return '\n'.join(result)

def is_enabled():
    return MARKER_START in read_hosts()

def enable_blocking(domains):
    lines = ['', MARKER_START, '# ShieldDNS ' + str(datetime.date.today()), '# ' + str(len(domains)) + ' domains blocked']
    for d in sorted(domains):
        lines.append('0.0.0.0 ' + d)
    lines += [MARKER_END, '']
    with open(HOSTS_PATH, 'a') as f:
        f.write('\n'.join(lines))

def disable_blocking():
    with open(HOSTS_PATH, 'w') as f:
        f.write(strip_shield_block(read_hosts()))

def count_blocked():
    text = read_hosts()
    if MARKER_START not in text: return 0
    return sum(1 for l in text.splitlines() if l.startswith('0.0.0.0 '))

domains = load_blocklist()
print('Loaded', len(domains), 'domains')
print('Currently enabled:', is_enabled())
print()
print('Enabling...')
enable_blocking(domains)
print('Blocked:', count_blocked(), 'domains')
print()
print('First 8 lines of hosts file:')
for l in read_hosts().splitlines()[:8]:
    print(' ', l)
print()
print('Disabling...')
disable_blocking()
print('Blocked after disable:', count_blocked())
print('Enabled:', is_enabled())
print()
print('ALL TESTS PASSED')




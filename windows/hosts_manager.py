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
    original = strip_shield_block(read_hosts())
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

if __name__ == '__main__':
    print('ShieldDNS')
    print('Status:', 'ENABLED' if is_enabled() else 'DISABLED')
    print()

    if is_enabled():
        print('Blocking is ON. Type "off" to disable, or Enter to exit.')
        choice = input('> ').strip().lower()
        if choice == 'off':
            disable_blocking()
            print('Blocking disabled.')
    else:
        domains = load_blocklist()
        print(str(len(domains)) + ' domains loaded.')
        print('Type "on" to enable blocking, or Enter to exit.')
        choice = input('> ').strip().lower()
        if choice == 'on':
            print('Enabling...')
            enable_blocking(domains)
            print('Done. ' + str(count_blocked()) + ' domains now blocked.')
            print('Restart your browser for changes to take effect.')

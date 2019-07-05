import re
from nstools.cmd import shell_out

def build_netns_map():
    nsmap = {}
    names = []
    out = shell_out('ip netns')
    for line in out.splitlines():
        a = line.split(' ')
        if len(a) > 0:
            names.append(a[0])
        m = re.search(r'([^\s]+)\s.*?([0-9]+)', line)
        if not m or m.lastindex != 2:
            continue
        nsmap[m.group(2)] = m.group(1)
    return nsmap, names

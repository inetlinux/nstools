import re
from nstools.cmd import shell_out

def build_netns_map():
    ret = {}
    out = shell_out('ip netns')
    for line in out.splitlines():
        m = re.search(r'([^\s]+)\s.*?([0-9]+)', line)
        if not m or m.lastindex != 2:
            continue
        ret[m.group(2)] = m.group(1)
    return ret

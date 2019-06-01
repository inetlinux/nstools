import os
import re
from nstools.common import build_netns_map
from nstools.cmd import shell, shell_out

def ovs_add_br(br):
    if shell('ovs-vsctl br-exists {0}'.format(br)) != 0:
        shell('ovs-vsctl add-br {0}'.format(br))

def ovs_add_allports(br):
    nsmap = build_netns_map()

    for i in range(1, 16):
        netns_names = [
            'r{0}'.format(i),
            'c{0}'.format(i),
            's{0}'.format(i),
            'h{0}'.format(i),
        ]
        for ns in netns_names:
            if ns not in nsmap.values():
                continue
            for ifidx in range(0, 10):
                port = 'veth{0}-{1}'.format(ifidx, ns)
                port_exists = os.path.exists('/sys/class/net/{0}'.format(port))
                if port_exists and shell('ovs-vsctl add-port {0} {1} 2>/dev/null'.format(br, port)) == 0:
                    print("Add port {0}".format(port))

def main(args, cfg):
    ovs_add_br(args.name)
    if args.add_all:
        ovs_add_allports(args.name)

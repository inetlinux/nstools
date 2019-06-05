import re
import subprocess
from nstools.cmd import shell, shell_out

def ovs_add_br(br):
    if shell('ovs-vsctl br-exists {0}'.format(br)) != 0:
        shell('ovs-vsctl add-br {0}'.format(br))

def ovs_get_br(port, default_br):
    br = shell_out('ovs-vsctl port-to-br {0}'.format(port))
    if not br:
        br = default_br
        subprocess.check_call('ovs-vsctl add-port {0} {1}'.format(br, port), shell=1)
    return br

def ovs_set_port(args):
    for p in args.port:
        ovs_get_br(p, args.name)
        if args.tags:
            tags = list(args.tags)
            print('Set vlan tag {0} for port {1}'.format(','.join(tags), p))
            if len(args.tags) == 1:
                shell('ovs-vsctl set port {0} tag={1}'.format(p, tags[0]))
            elif len(args.tags) > 1:
                shell('ovs-vsctl set port {0} trunks={1}'.format(p, ','.join(tags)))

def main(args, cfg):
    ovs_add_br(args.name)
    return ovs_set_port(args)

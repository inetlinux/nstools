import os
import re
from nstools.cmd import shell

def main(args, cfg):
    r1 = args.src
    r2 = args.dst
    name = 'br-{0}{1}'.format(r1.router, r2.router)
    p1 = r1.ifname if r1.ifname.endswith(r1.router) else '{0}-{1}'.format(r1.ifname, r1.router)
    p2 = r2.ifname if r2.ifname.endswith(r2.router) else '{0}-{1}'.format(r2.ifname, r2.router)
    shell('ovs-vsctl add-br {0} -- add-port {0} {1} -- add-port {0} {2}'.format(name, p1, p2))

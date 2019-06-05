from nstools.common import build_netns_map
from nstools.cmd import shell, execv

def main(args, cfg):
    if not args.fast:
        nsmap = build_netns_map()
        if nsmap.get(args.name):
            return execv('ip netns exec {0} {1}'.format(nsmap.get(args.name), ' '.join(args.cmdargs)))
    return execv('ip netns exec {0} {1}'.format(args.name, ' '.join(args.cmdargs)))

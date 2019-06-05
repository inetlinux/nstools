from nstools.common import build_netns_map
from nstools.cmd import shell

def if_exists_netns(netns, ifname):
    cmd = 'ip netns exec {} test -e /sys/class/net/{}'.format(netns, ifname)
    ret = shell(cmd)

    return (ret==0)

def main(args, cfg):
    ifname = args.ifname

    ret = 0
    if not if_exists_netns(args.netns, ifname):
        ret = shell('ip netns exec {} ip link add dev {}'.format(args.netns, ifname))
        shell('ip netns exec {} ip link set dev {} up'.format(args.netns, ifname))

    if args.vlan:
        shell('ip netns exec {0} ip link add link {1} name {1}.{2} type vlan id {2}'.format(args.netns, ifname, args.vlan))
        shell('ip netns exec {0} ip link set dev {1}.{2} up'.format(args.netns, ifname, args.vlan))
        shell('ip netns exec {0} ip addr flush dev {1}'.format(args.netns, ifname))
        if isinstance(args.address, str):
            shell('ip netns exec {0} ip addr add dev {1}.{2} {3}'.format(args.netns, ifname, args.vlan, args.address))
    return ret

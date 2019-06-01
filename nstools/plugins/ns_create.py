import re
from nstools.cmd import shell

def main(args, cfg):
    shell('ip netns add {0}'.format(args.name))

    for i in range(0, args.ifcount):
        pair = ['veth{0}-{1}'.format(i, args.name), 'veth{0}'.format(i)]

        shell('ip link add dev {0} type veth peer name {1} netns {2}'.format(pair[0], pair[1], args.name))
        shell('ip link set dev {0} up'.format(pair[0]))
        shell('ip netns exec {0} ip link set dev {1} up'.format(args.name, pair[1]))

        if not args.address:
            continue
        if len(args.address) <= i:
            continue
        cidr = args.address[i]
        if not re.search('/[0-9]+', cidr):
            cidr = '{0}/24'.format(cidr)
        print("Set ip address {0} for {1}".format(cidr, pair[1]))
        shell('ip netns exec {0} ip addr add dev {1} {2}'.format(args.name, pair[1], cidr))
    shell('ip netns exec {0} ip link set dev lo up'.format(args.name))

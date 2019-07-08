#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
from netaddr import IPNetwork
from jinja2 import Environment, FileSystemLoader
from nstools.cmd import shell_out

def get_addresses(ifname, ifindex, ns=None):
    def exclude(a):
        patterns = ['fe80::']
        for pattern in patterns:
            if a == pattern or re.search(pattern, a):
                return True
        return False

    cmd = 'ip addr show dev {0}'.format(ifname)
    cmd = 'ip netns exec {0} {1}'.format(ns, cmd) if ns else cmd
    out = shell_out(cmd)

    result = {'index': ifindex,  'v4': [], 'v4network': [], 'v6': [], 'v6network': []}
    m = re.search('link/ether ((\w{2}:){5}\w{2})', out)
    if not m:
        return None
    result['mac'] = m.group(1)

    for m in re.finditer('inet (([0-9]+.){3}[0-9]+/[0-9]{1,3})', out, re.M):
        addr = m.group(1)
        if exclude(addr): continue
        result['v4'].append(addr)
        nw = IPNetwork(addr)
        result['v4network'].append({'prefix': str(nw.cidr)})

    for m in re.finditer('inet6 (.+)/[0-9]{1,3}', out, re.M):
        addr = m.group(1)
        if exclude(addr): continue
        result['v6'].append(addr)
        nw = IPNetwork(addr)
        result['v6network'].append({'prefix': str(nw.cidr)})

    return result

def get_ifaddr_map(ns = None):
    exclude_interfaces = ['lo', 'ovs-system', 'docker0', 'br.*']
    result = {}

    cmd = 'ip netns exec {0} ip link show'.format(ns) if ns else 'ip link show'
    out = shell_out(cmd)

    for x in re.finditer('(^[0-9]+): ([a-zA-Z0-9-]+)', out, re.M):
        ifname = x.group(2)
        ifindex= int(x.group(1))
        exclude = False
        for pattern in exclude_interfaces:
            if ifname == pattern or re.search(pattern, ifname):
                exclude = True
                break
        if exclude: continue

        address = get_addresses(ifname, ifindex, ns)
        if not address:
            continue
        result[ifname] = address

    return result


"""
def get_connected_networks(ns = None):
    cmd = 'ip ro show'
    cmd = 'ip netns exec {0} {1}'.format(ns, cmd) if ns else cmd
    out = shell_out(cmd)

    route4 = []
    for x in re.finditer('(^.+/[0-9]{1,3}) .*scope link', out, re.M):
        route4.append({'prefix': x.group(1), 'scope': 'link'})

    return route4
"""

class Env():
    def __init__(self):
        packages_dir = os.path.dirname(os.path.dirname(__file__))
        template_dir = os.path.join(packages_dir, 'templates')
        self.env = Environment(loader=FileSystemLoader(template_dir), keep_trailing_newline=True,
                      trim_blocks=True)

    def template(self, src, dest, **kwargs):
        def write_dest(destf, sbuf, mode, check=True):
            with open(destf, 'w') as fp:
                fp.write(sbuf)
                fp.close()
                os.chmod(destf, mode)

            print('Write to {0}'.format(dest))
            return 0

        mode = kwargs.get('mode', 0o644)
        temp = self.env.get_template(src)
        buff = temp.render(**kwargs)
        return write_dest(dest, buff, mode)

def main(args, cfg):
    router = args.router
    router_dstdir = '/srv/{}'.format(router)
    if not os.path.exists(router_dstdir):
        os.mkdir(router_dstdir)

    env = Env()
    cfg = {'router': router}

    #cfg['ospf']['passive_interfaces'] = args.passive_interfaces if args.passive_interfaces else []

    """
    connected_route = get_connected_networks(args.router)
    for r in connected_route:
        r['area'] = args.default_area
        if args.network_areamap and r['prefix'] in args.network_areamap:
            r['area'] = args.default_area
        cfg['route'].append(r)

    """

    cfg['ifmap'] = get_ifaddr_map(args.router)
    for k, v in cfg['ifmap'].items():
        v['attrs'] = {}
        if args.interface_attributes and k in args.interface_attributes:
            attributes = args.interface_attributes.get(k)
            for attr in attributes:
                if attr == 'passive':
                    v['attrs']['passive'] = True
                elif attr == 'point-to-point':
                    v['attrs']['ospf_network'] = 'point-to-point'
        for n in v['v4network']:
            n['area'] = args.default_area
            if args.network_areamap and n['prefix'] in args.network_areamap:
                n['area'] = args.network_areamap.get(n['prefix'])

    for daemon in args.daemon:
        src = '{0}.conf'.format(daemon)
        dst = '{0}/{1}'.format(router_dstdir, src)
        env.template(src, dst, router=router, cfg=cfg)

    shell_out('chown -R quagga.quaggavt {0}'.format(router_dstdir))
    return 0

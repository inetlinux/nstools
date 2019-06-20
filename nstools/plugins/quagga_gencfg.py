#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
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

    result = {'index': ifindex,  'v4': [], 'v6': []}
    m = re.search('link/ether ((\w{2}:){5}\w{2})', out)
    if not m:
        return None
    result['mac'] = m.group(1)

    for m in re.finditer('inet (([0-9]+.){3}[0-9]+)/[0-9]{1,3}', out, re.M):
        addr = m.group(1)
        if exclude(addr): continue
        result['v4'].append(addr)

    for m in re.finditer('inet6 (.+)/[0-9]{1,3}', out, re.M):
        addr = m.group(1)
        if exclude(addr): continue
        result['v6'].append(addr)

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

def get_connected_networks(ns = None):
    cmd = 'ip ro show'
    cmd = 'ip netns exec {0} {1}'.format(ns, cmd) if ns else cmd
    out = shell_out(cmd)

    route4 = []
    for x in re.finditer('(^.+/[0-9]{1,3}) .*scope link', out, re.M):
        route4.append({'prefix': x.group(1), 'scope': 'link'})

    return route4

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

        mode = kwargs.get('mode', 644)
        temp = self.env.get_template(src)
        buff = temp.render(**kwargs)
        return write_dest(dest, buff, mode)

def main(args, cfg):
    router = args.router
    router_dstdir = '/srv/{}'.format(router)
    if not os.path.exists(router_dstdir):
        os.mkdir(router_dstdir)

    env = Env()
    cfg = {'router': router, 'interfaces': [], 'route': []}

    connected_route = get_connected_networks(args.router)
    for r in connected_route:
        r['area'] = '0'
        if args.input_area:
            r['area'] = input('Input area for {}: '.format(r['prefix']))
        cfg['route'].append(r)

    ifmap = get_ifaddr_map(args.router)
    for k,v in ifmap.items():
        v4ent = {'name': k, 'v4': v['v4']}
        cfg['interfaces'].append(v4ent)

    for daemon in args.daemon:
        src = '{0}.conf'.format(daemon)
        dst = '{0}/{1}'.format(router_dstdir, src)
        env.template(src, dst, cfg=cfg)

    return 0

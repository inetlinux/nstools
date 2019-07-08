import os
import subprocess

def main(args, cfg):
    lines = [
        'configure t',
        'router ospf',
        '{0}'.format(' '.join(args.args)),
        'quit',
        'do write',
    ]

    cmd = 'ip netns exec {0} vtysh -E'.format(args.router)
    for line in lines:
        cmd += " -c '{0}'".format(line)

    return subprocess.call(cmd, shell=True)

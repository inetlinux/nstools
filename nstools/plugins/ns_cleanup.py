import os
import time
import signal
import psutil

from nstools.cmd import shell, shell_out

def main(args, cfg):
    processes = ['dnsmasq', 'dhclient', 'zebra', 'vtysh', 'ospfd']

    for p in psutil.process_iter(attrs=['name', 'pid']):
        if p.info['name'] in processes:
            print(p.info);
            try:
                os.kill(p.info['pid'], signal.SIGTERM)
            except Exception as e:
                print(e)
    time.sleep(1)
    for p in psutil.process_iter(attrs=['name', 'pid']):
        if p.info['name'] in processes:
            print(p.info);

    shell('rm -f /tmp/*.leases')
    shell('ip --all netns delete')

    out = shell_out('ovs-vsctl list-br')
    for br in out.splitlines():
        shell('ovs-vsctl del-br {0}'.format(br))

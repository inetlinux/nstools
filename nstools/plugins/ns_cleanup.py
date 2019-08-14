import os
import time
import glob
import signal
import psutil

from nstools.cmd import shell, shell_out

def main(args, cfg):
    # Terminate processes
    processes = ['dnsmasq', 'zebra', 'vtysh', 'ospfd', 'bgpd']
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


    # Terminate dhclient
    for dh in glob.glob('/tmp/dhclient-*'):
        with open(dh, 'r') as fp:
            pid = fp.read()
            fp.close()
            try:
                os.kill(int(pid), signal.SIGTERM)
            except Exception as e:
                print(e)
            os.unlink(dh)

    for pn in glob.glob('/sys/class/net/veth*'):
        if not os.path.exists(pn):
            continue
        bn = os.path.basename(pn)
        shell('ip link del {0}'.format(bn))

    shell('rm -f /tmp/*.leases')
    shell('ip --all netns delete')
    shell('docker rm -vf faucet')

    # Delete all ovs bridge
    out = shell_out('ovs-vsctl list-br')
    for br in out.splitlines():
        shell('ovs-vsctl del-br {0}'.format(br))

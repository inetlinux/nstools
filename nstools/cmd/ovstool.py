import os
import sys
import argparse
import importlib
import nstools

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action='store_true')
    subparsers = parser.add_subparsers(help='sub-command help')
    add_sub_addports(subparsers)
    if len(sys.argv)<=1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    if args.debug:
        print(args)
    return args.func(args, None)

def add_sub_addports(subparsers):
    sub = subparsers.add_parser('addports', help='Add port to ovs bridge')
    sub.add_argument('--name', '-n', type=str, default='br0', help='bridge name')
    sub.add_argument('--add-all', '-a', action='store_true', help='Add all port to one bridge')
    sub.add_argument('--tag', '-t', type=int, help='vlan tag')
    sub.add_argument('--tags', type=int, help='vlan trunk premit tags')
    sub.set_defaults(func=importlib.import_module('nstools.plugins.ovs_addports').main)
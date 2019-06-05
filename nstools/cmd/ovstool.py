# PYTHON_ARGCOMPLETE_OK

import os
import sys
import argparse
import argcomplete
import importlib
import nstools

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action='store_true')
    subparsers = parser.add_subparsers(help='sub-command help')
    add_sub_addports(subparsers)
    add_sub_setport(subparsers)
    if len(sys.argv)<=1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    if args.debug:
        print(args)
    return args.func(args, None)

def add_sub_addports(subparsers):
    sub = subparsers.add_parser('addports', help='Add all available ports to one ovs bridge')
    sub.add_argument('--name', '-n', type=str, default='br0', help='bridge name')
    sub.set_defaults(func=importlib.import_module('nstools.plugins.ovs_addports').main)

def add_sub_setport(subparsers):
    sub = subparsers.add_parser('setport', help='Add/Set ovs port')
    sub.add_argument('port', nargs='+', type=str, help='port name')
    sub.add_argument('--name', '-n', type=str, default='br0', help='bridge name')
    sub.add_argument('--tags', '-t', nargs='+', type=str, help='vlan trunk premit tags')
    sub.set_defaults(func=importlib.import_module('nstools.plugins.ovs_setport').main)

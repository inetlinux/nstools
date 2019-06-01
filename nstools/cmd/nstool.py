import os
import sys
import argparse
import importlib
import nstools

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action='store_true')
    subparsers = parser.add_subparsers(help='sub-command help')
    add_sub_create(subparsers)
    add_sub_exec(subparsers)
    add_sub_cleanup(subparsers)
    add_sub_addif(subparsers)

    if len(sys.argv)<=1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    if sys.argv[1] == 'exec' and len(sys.argv) > 3:
        cmdline = ' '.join(sys.argv[3:])
        sys.argv[3] = cmdline
        sys.argv = sys.argv[:4]
    args = parser.parse_args()
    if args.debug:
        print(args)
    return args.func(args, None)

def add_sub_create(subparsers):
    sub = subparsers.add_parser('create', help='Create netns')
    sub.add_argument('name', type=str)
    sub.add_argument('-n', '--ifcount', type=int, default=1, help='interface count')
    sub.add_argument('-a', '--address', type=str, nargs='+', help='interface address')
    sub.set_defaults(func=importlib.import_module('nstools.plugins.ns_create').main)

def add_sub_exec(subparsers):
    sub = subparsers.add_parser('exec', help='Execute command under netns')
    sub.add_argument('-f', '--fast', action='store_true')
    sub.add_argument('name', type=str)
    sub.add_argument('cmdargs', type=str, nargs='+', help='command and its args')
    sub.set_defaults(func=importlib.import_module('nstools.plugins.ns_exec').main)

def add_sub_cleanup(subparsers):
    sub = subparsers.add_parser('cleanup', help='Cleanup network experiment environments')
    sub.set_defaults(func=importlib.import_module('nstools.plugins.ns_cleanup').main)

def add_sub_addif(subparsers):
    sub = subparsers.add_parser('addif', help='Add interface under netns')
    sub.set_defaults(func=importlib.import_module('nstools.plugins.ns_addif').main)

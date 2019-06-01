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

    args = parser.parse_args()
    if args.debug:
        print(args)
    return args.func(args, gc)

def add_sub_create(subparsers):
    sub = subparsers.add_parser('create', help='Create netns')
    sub.add_argument('name', type=str)
    sub.add_argument('-n', '--ifcount', type=str, help='interface count')
    sub.add_argument('-a', '--address', type=str, nargs='+', help='interface address')
    sub.set_defaults(func=importlib.import_module('nstools.plugins.ns_create').main)

def add_sub_exec(subparsers):
    sub = subparsers.add_parser('exec', help='Execute command under netns')
    sub.add_argument('name', type=str)
    sub.set_defaults(func=importlib.import_module('nstools.plugins.ns_exec').main)

def add_sub_cleanup(subparsers):
    sub = subparsers.add_parser('cleanup', help='Cleanup network experiment environments')
    sub.set_defaults(func=importlib.import_module('nstools.plugins.ns_cleanup').main)

def add_sub_addif(subparsers):
    sub = subparsers.add_parser('addif', help='Add interface under netns')
    sub.set_defaults(func=importlib.import_module('nstools.plugins.ns_addif').main)

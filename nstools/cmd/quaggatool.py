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
    add_sub_gencfg(subparsers)
    if len(sys.argv)<=1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    if args.debug:
        print(args)
    return args.func(args, None)

def add_sub_gencfg(subparsers):
    sub = subparsers.add_parser('gencfg', help='Generate configurations for Quagga router')
    sub.add_argument("--input-area", action='store_true')
    sub.add_argument('router', type=str, help='router name')
    sub.add_argument('daemon', type=str, nargs='+', help='specific daemon name', choices=['vtysh', 'ospfd', 'zebra'])
    sub.set_defaults(func=importlib.import_module('nstools.plugins.quagga_gencfg').main)

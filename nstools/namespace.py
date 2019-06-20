#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import errno
import ctypes
import ctypes.util
from pathlib import Path

NAMESPACE_NAMES = frozenset(['mnt', 'ipc', 'net', 'pid', 'user', 'uts'])

class Namespace(object):
    _libc = ctypes.CDLL(ctypes.util.find_library('c'), use_errno=True)

    def __init__(self, pid, ns_type, proc='/proc'):
        """
        pid: The PID for the owner of the namespace to enter, or an absolute
             path to a file which represents a namespace handle.

        Example:
        with Namespace(14975, 'net'):
            pass
        with Namespace('/var/run/netns/r1', 'net'):
            pass
        """
        self.ns_type = ns_type
        self.pid = pid
        self.proc = proc

        if isinstance(pid, int):
            self.target_fd = self._nsfd(self.pid, ns_type).open()
        else:
            self.target_fd = Path(pid).open()

        self.target_fileno = self.target_fd.fileno()
        self.parent_fd = self._nsfd('self', ns_type).open()
        self.parent_fileno = self.parent_fd.fileno()

    def _nsfd(self, pid, ns_type):
        return Path(self.proc) / str(pid) / 'ns' / ns_type

    def _close_files(self):
        try:
            self.target_fd.close()
        except:
            pass
        if self.parent_fd is not None:
            self.parent_fd.close()

    def __enter__(self):
        if self._libc.setns(self.target_fileno, 0) == -1:
            e = ctypes.get_errno()
            self._close_files()
            raise OSError(e, errno.errorcode[e])

    def __exit__(self, type, value, tb):
        if self._libc.setns(self.parent_fileno, 0) == -1:
            e = ctypes.get_errno()
            self._close_files()
            raise OSError(e, errno.errorcode[e])

        self._close_files()

if __name__ == '__main__':
    import subprocess
    with Namespace('/var/run/netns/r1', 'net'):
        subprocess.call(['ip', 'a'])

#!/usr/bin/env python3.6

import os
import stat
import subprocess
import sys


def get_executables(dir):
    exec_fyles = []
    for fyle in os.listdir(dir):
        path = os.path.join(dir, fyle)
        if os.stat(path)[stat.ST_MODE] & \
                (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH):
            exec_fyles.append(path)
    return exec_fyles

if __name__ == '__main__':
    assert len(sys.argv) >= 2, "Not enough arguments"
    stdin = sys.stdin.read()
    ret = 0
    for exec_fyle in get_executables(sys.argv[1]):
        ret += subprocess.run([exec_fyle] + sys.argv[2:], input=stdin,
                              universal_newlines=True).returncode
    sys.exit(ret)

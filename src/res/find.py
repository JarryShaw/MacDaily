# -*- coding: utf-8 -*-

import functools
import os
import re
import sys


@functools.lru_cache
def find(root):
    for file in os.listdir(root):
        path = os.path.join(root, file)
        if os.path.islink(path):
            continue
        if os.path.isdir(path):
            if re.match('^/Volumes', path) is not None:
                continue
            if os.path.splitext(path)[1] == '.app':
                print(path)
            find(path)


if __name__ == '__main__':
    sys.exit(find(sys.argv[1]))

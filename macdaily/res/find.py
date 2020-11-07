# -*- coding: utf-8 -*-

import contextlib
import functools
import pathlib
import sys


@functools.lru_cache(maxsize=128)
def find(root):
    with contextlib.suppress(PermissionError):
        for path in root.iterdir():
            with contextlib.suppress(OSError):
                if path.is_symlink():
                    continue
                if path.is_dir():
                    if path.parts[:2] == ('/', 'Volumes'):
                        continue
                    if path.suffix == '.app':
                        print(path)
                    find(path)


if __name__ == '__main__':
    sys.tracebacklimit = 0
    sys.exit(find(pathlib.Path(sys.argv[1]).resolve(strict=True)))

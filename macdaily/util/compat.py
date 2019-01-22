# -*- coding: utf-8 -*-

import sys

# pathlib & subprocess
if sys.version_info[:2] <= (3, 4):
    import pathlib2 as pathlib
    import subprocess32 as subprocess
else:
    import pathlib
    import subprocess

# threading
try:
    import threading
except ImportError:
    import dummy_threading as threading

# multiprocessing
try:
    import multiprocessing
except ImportError:
    multiprocessing = threading

    # make alias for multiprocessing.Queue
    import queue
    setattr(threading, 'Queue', queue.Queue)

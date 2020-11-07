# -*- coding: utf-8 -*-

import sys

# pathlib & subprocess
if sys.version_info[:2] <= (3, 4):
    import pathlib2 as pathlib  # pylint: disable=unused-import
    import subprocess32 as subprocess  # pylint: disable=unused-import
else:
    import pathlib  # pylint: disable=unused-import
    import subprocess  # pylint: disable=unused-import

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

    # make alias for multiprocessing.Process
    setattr(multiprocessing, 'Process', threading.Thread)

    # make alias for multiprocessing.Queue
    import queue
    setattr(multiprocessing, 'Queue', queue.Queue)

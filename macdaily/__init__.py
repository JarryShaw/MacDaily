# -*- coding: utf-8 -*-

import platform

from macdaily.util.error import UnsupportedOS

# check platform
if platform.system() != 'Darwin':
    raise UnsupportedOS('macdaily: script runs only on macOS')

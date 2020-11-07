# -*- coding: utf-8 -*-
"""magic strings"""

import functools


@functools.total_ordering
class minstr:

    def __lt__(self, value):
        if isinstance(value, str):
            return True
        return NotImplemented


@functools.total_ordering
class maxstr:

    def __gt__(self, value):
        if isinstance(value, str):
            return True
        return NotImplemented


# string boundaries
MIN = minstr()
MAX = maxstr()

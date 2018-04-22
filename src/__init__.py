# -*- coding: utf-8 -*-


import os

from jsdaily.daily import main as daily


__all__ = ['daily']


# change working directory
os.chdir(os.path.dirname(__file__))

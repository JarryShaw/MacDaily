#!/usr/bin/python3
# -*- coding: utf-8 -*-


import os


from jsdaily.update import main as update
from jsdaily.uninstall import main as uninstall
from jsdaily.reinstall import main as reinstall
from jsdaily.postinstall import main as postinstall
from jsdaily.dependency import main as dependency
from jsdaily.logging import main as logging


__all__ = ['update', 'uninstall', 'reinstall', 'postinstall', 'dependency', 'logging']


# change working directory
os.chdir(os.path.dirname(__file__))

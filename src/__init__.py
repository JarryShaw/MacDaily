#!/usr/bin/python3
# -*- coding: utf-8 -*-


import os


from jsdaily.jsupdate import main as update
from jsdaily.jsuninstall import main as uninstall
from jsdaily.jsreinstall import main as reinstall
from jsdaily.jspostinstall import main as postinstall
from jsdaily.jsdependency import main as dependency
from jsdaily.jslogging import main as logging


__all__ = ['update', 'uninstall', 'reinstall', 'postinstall', 'dependency', 'logging']


# change working directory
os.chdir(os.path.dirname(__file__))

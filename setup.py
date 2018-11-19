# -*- coding: utf-8 -*-

import os
import platform
import re
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# check platform
if platform.system() != 'Darwin':
    class UnsupportedOS(RuntimeError):
        def __init__(self, message, *args, **kwargs):
            sys.tracebacklimit = 0
            super().__init__(message, *args, **kwargs)
    raise UnsupportedOS('macdaily: script runs only on macOS')

# version string
with open(os.path.join(os.path.dirname(__file__), 'macdaily/util/const.py'), 'r') as file:
    for line in file:
        match = re.match(r"__version__ = '(.*)'", line)
        if match is None:
            continue
        __version__ = match.groups()[0]
        break

# README
with open(os.path.join(os.path.dirname(__file__), 'README.rst'), 'r') as file:
    long_desc = file.read()

# set-up script for pip distribution
setup(
    name='macdaily',
    version=__version__,
    author='Jarry Shaw',
    author_email='jarryshaw@icloud.com',
    url='https://github.com/JarryShaw/macdaily#macdaily',
    license='GNU General Public License v3 (GPLv3)',
    keywords='daily utility script',
    description='Package day-care manager on macOS.',
    long_description=long_desc,
    long_description_content_type='text/x-rst; charset=UTF-8',
    python_requires='>=3.4',
    include_package_data=True,
    extras_require={
        'ptyng': ['ptyng'],
        'pipdeptree': ['pipdeptree'],
        ':python_version == "3.4"': ['pathlib2>=2.3.2', 'subprocess32>=3.5.3'],
    },
    entry_points={
        'console_scripts': [
            # 'macdaily = macdaily.__main__:main',
            'md-update = macdaily.api.update:update',
            'md-uninstall = macdaily.api.uninstall:uninstall',
            'md-reinstall = macdaily.api.reinstall:reinstall',
            'md-postinstall = macdaily.api.postinstall:postinstall',
            'md-logging = macdaily.api.logging:logging',
            'md-launch = macdaily.api.launch:launch',
        ]
    },
    packages=[
        'macdaily',
        'macdaily.api',
        'macdaily.cli',
        'macdaily.cls',
        'macdaily.cls.bundle',
        'macdaily.cls.cleanup',
        'macdaily.cls.dependency',
        'macdaily.cls.install',
        'macdaily.cls.logging',
        'macdaily.cls.reinstall',
        'macdaily.cls.uninstall',
        'macdaily.cls.update',
        'macdaily.cmd',
        'macdaily.core',
        'macdaily.util',
    ],
    package_data={
        '': [
            'LICENSE',
            'README.rst',
        ],
        'macdaily.img': ['*.icns'],
        'macdaily.res': ['*.py', '*.applescript'],
    },
    classifiers=[
        # 'Development Status :: 5 - Production/Stable',
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Environment :: MacOS X',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        # 'Programming Language :: Unix Shell',
        'Topic :: Utilities',
    ]
)

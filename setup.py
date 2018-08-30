# -*- coding: utf-8 -*-


import platform
import setuptools
import sys


# error handling class
class UnsupoortedOS(RuntimeError):
    def __init__(self, message, *args, **kwargs):
        sys.tracebacklimit = 0
        super().__init__(message, *args, **kwargs)


# check platform
if platform.system() != 'Darwin':
    raise UnsupoortedOS('macdaily: script runs only on macOS')


# README
with open('./README.md', 'r') as file:
    long_desc = file.read()


# version
__version__ = '2018.08.30a2'


# set-up script for pip distribution
setuptools.setup(
    name = 'macdaily',
    version = __version__,
    author = 'Jarry Shaw',
    author_email = 'jarryshaw@icloud.com',
    url = 'https://github.com/JarryShaw/macdaily#macdaily',
    license = 'GNU General Public License v3 (GPLv3)',
    keywords = 'daily utility script',
    description = 'Package day-care manager on macOS.',
    long_description = long_desc,
    long_description_content_type='text/markdown',
    python_requires = '>=3.6',
    install_requires = ['setuptools'],
    extras_require = {
        'pipdeptree': ['pipdeptree']
    },
    entry_points = {
        'console_scripts': [
            'macdaily = macdaily.__main__:main',
        ]
    },
    packages = [
        'macdaily',
        'macdaily.libbundle',
        'macdaily.libupdate',
        'macdaily.libuninstall',
        'macdaily.libprinstall',
        'macdaily.libdependency',
        'macdaily.liblogging',
    ],
    package_data = {
        '': [
            'LICENSE',
            'README.md',
        ],
        'macdaily': ['*.py', '*.sh'],
        'macdaily.libbundle': ['*.py', '*.sh'],
        'macdaily.libupdate': ['*.py', '*.sh'],
        'macdaily.libuninstall': ['*.py', '*.sh'],
        'macdaily.libprinstall': ['*.py', '*.sh'],
        'macdaily.libdependency': ['*.py', '*.sh'],
        'macdaily.liblogging': ['*.py', '*.sh'],
    },
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: MacOS X',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Unix Shell',
        'Topic :: Utilities',
    ]
)

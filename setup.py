#!/usr/bin/python3
# -*- coding: utf-8 -*-


import setuptools


with open('./README.rst', 'r', encoding='utf-8') as file:
    long_desc = file.read()


# set-up script for pip distribution
setuptools.setup(
    name = 'jsdaily',
    version = '0.1.5',
    author = 'Jarry Shaw',
    author_email = 'jarryshaw@icloud.com',
    url = 'https://github.com/JarryShaw/jsdaily/',
    license = 'GNU General Public License v3 (GPLv3)',
    keywords = 'daily utility script',
    description = 'Some useful daily utility scripts.',
    long_description = long_desc,
    python_requires = '>=3.6',
    py_modules = ['update', 'uninstall', 'reinstall', 'postinstall', 'dependency'],
    entry_points = {
        'console_scripts': [
            'update = update:main',
            'uninstall = uninstall:main',
            'reinstall = reinstall:main',
            'postinstall = postinstall:main',
            'dependency = dependency:main',
        ]
    },
    packages = setuptools.find_packages(exclude=['deprecated']),
    package_data = {
        '': [
            'LICENSE.txt',
            'README.md',
            'README.rst',
        ],
        'libupdate': ['*.py', '*.sh'],
        'libuninstall': ['*.py', '*.sh'],
        'libprinstall': ['*.py', '*.sh'],
        'libdependency': ['*.py', '*.sh'],
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

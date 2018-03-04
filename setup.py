#!/usr/local/opt/python3/bin/python3.6
# -*- coding: utf-8 -*-


import setuptools


with open('./README.rst', 'r') as file:
    long_des = file.read()


# set-up script for pip distribution
setuptools.setup(
    name = 'scripts',
    version = '0.1.0',
    author = 'Jarry Shaw',
    author_email = 'jarryshaw@icloud.com',
    url = 'https://github.com/JarryShaw/jsdaily/',
    license = 'GNU General Public License v3 (GPLv3)',
    description = 'Some useful daily utility scripts.',
    long_description = long_desc,
    python_requires = '>=3.4',
    py_modules=['update', 'uninstall', 'reinstall', 'postinstall', 'dependency'],
    entry_points={
        'console_scripts': [
            'update = update:main',
            'uninstall = uninstall:main',
            'reinstall = reinstall:main',
            'postinstall = postinstall:main',
            'dependency = dependency:main',
        ]
    },
    classifiers=[
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
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
    ]
)

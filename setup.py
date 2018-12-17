# -*- coding: utf-8 -*-

import platform
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
    print('macdaily: error: script runs only on macOS', file=sys.stderr)
    raise UnsupportedOS

# README
with open('./README.rst', encoding='utf-8') as file:
    long_description = file.read()

# version string
__version__ = '2018.12.17'
# context = pkg_resources.resource_string(__name__, 'macdaily/util/const.py')
# for line in context.splitlines():
#     match = re.match(rb"__version__ = '(.*)'", line)
#     if match is None:
#         continue
#     __version__ = match.groups()[0].decode()
#     break

# set-up script for pip distribution
setup(
    name='macdaily',
    version=__version__,
    author='Jarry Shaw',
    author_email='jarryshaw@icloud.com',
    url='https://github.com/JarryShaw/MacDaily#macdaily',
    license='Apple Public Source License',
    keywords='daily utility script',
    description='macOS Automated Package Manager',
    long_description=long_description,
    # long_description=pkg_resources.resource_string(__name__, 'README.rst').decode(),
    long_description_content_type='text/x-rst; charset=UTF-8',
    python_requires='>=3.4',
    # include_package_data=True,
    # zip_safe=True,
    extras_require={
        ':python_version == "3.4"': ['pathlib2>=2.3.2', 'subprocess32>=3.5.3'],
        'all': ['ptyng>=0.2.0.post4', 'dictdumper>=0.6.3', 'configupdater'],
        'ptyng': ['ptyng>=0.2.0.post4'],
        'tree': ['dictdumper>=0.6.3'],
        'config': ['configupdater'],
    },
    entry_points={
        'console_scripts': [
            'macdaily = macdaily.__main__:main',
            'md-archive = macdaily.api.archive:archive',
            # 'md-bundle = macdaily.api.bundle:bundle',
            'md-cleanup = macdaily.api.cleanup:cleanup',
            'md-config = macdaily.api.config:config [config]',
            'md-dependency = macdaily.api.dependency:dependency [tree]',
            'md-help = macdaily.api.help:help_',
            'md-install = macdaily.api.install:install',
            'md-launch = macdaily.api.launch:launch',
            'md-logging = macdaily.api.logging:logging',
            'md-postinstall = macdaily.api.postinstall:postinstall',
            'md-reinstall = macdaily.api.reinstall:reinstall',
            'md-uninstall = macdaily.api.uninstall:uninstall',
            'md-update = macdaily.api.update:update',
        ]
    },
    # packages=setuptools.find_namespace_packages(
    #     include=['macdaily', 'macdaily.*'],
    # ),
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
        'macdaily.man',
        'macdaily.img',
        'macdaily.res',
        'macdaily.util',
    ],
    package_data={
        '': [
            'LICENSE',
            'README.rst',
        ],
        'macdaily.man': ['*.1'],
        'macdaily.img': ['*.icns'],
        'macdaily.res': ['*.py', '*.applescript'],
    },
    classifiers=[
        # 'Development Status :: 7 - Inactive',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 5 - Production/Stable',
        'Development Status :: 4 - Beta',
        # 'Development Status :: 3 - Alpha',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Environment :: MacOS X',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apple Public Source License',
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

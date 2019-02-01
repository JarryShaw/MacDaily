====================
macdaily-install-pip
====================

----------------------------------
Python Package Automated Installer
----------------------------------

:Version: v2019.02.01
:Date: November 24, 2018
:Manual section: 1
:Author:
    Jarry Shaw, a newbie programmer, is the author, owner and maintainer
    of *MacDaily*. Please contact me at *jarryshaw@icloud.com*.
:Copyright:
    *MacDaily* is licensed under the **Apple Open Source License**.

SYNOPSIS
========

macdaily **install** *pip* [*options*] <*packages*> ...

OPTIONS
=======

optional arguments
------------------

-h, --help            show this help message and exit
-V, --version         show program's version number and exit

specification arguments
-----------------------

-u, --user            install to the Python user install directory for your
                      platform
-b, --brew            install packages of Python installed from Homebrew
-c, --cpython         install packages of CPython implementation
-d, --pre             include pre-release and development versions

-e *VER* [*VER* ...], --python *VER* [*VER* ...]
                      install packages by which version of Python

-r, --pypy            install packages of PyPy implementation
-s, --system          install packages of Python provided by macOS system

-p *PKG* [*PKG* ...], --packages *PKG* [*PKG* ...]
                      name of Python packages to install

general arguments
-----------------

-q, --quiet           run in quiet mode, with no output information
-v, --verbose         run in verbose mode, with detailed output information
-y, --yes             yes for all selections
-n, --no-cleanup      do not run cleanup process

miscellaneous arguments
-----------------------

-I *ARG*, --install *ARG*
                      options for ``pip install <package>`` command

SEE ALSO
========

* ``macdaily-install``
* ``macdaily-install-apm``
* ``macdaily-install-brew``
* ``macdaily-install-cask``
* ``macdaily-install-gem``
* ``macdaily-install-mas``
* ``macdaily-install-npm``
* ``macdaily-install-system``

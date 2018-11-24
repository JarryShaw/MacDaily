===================
macdaily-update-pip
===================

-------------------------------
Python Package Update Automator
-------------------------------

:Version: 2018.11.24
:Date: November 24, 2018
:Manual section: 1
:Author:
    Jarry Shaw, a newbie programmer, is the author, owner
    and maintainer of *MacDaily*. Please contact at *jarryshaw@icloud.com*.
:Copyright:
    *MacDaily* is licensed under the **GNU General Public License v3.0**.

SYNOPSIS
========

macdaily **update** *pip* [*options*] <*packages*>

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
-b, --brew            update packages of Python installed from Homebrew
-c, --cpython         update packages of CPython implementation
-d, --pre             include pre-release and development versions

-e *VER* [*VER* ...], --python *VER* [*VER* ...]
                      indicate packages from which version of Python will
                      update

-r, --pypy            update packages of PyPy implementation
-s, --system          update packages of Python provided by macOS system

-p *PKG* [*PKG* ...], --packages *PKG* [*PKG* ...]
                      name of Python packages to update

general arguments
-----------------

-a, --all             update all Python packages installed through Python
                      Package Index
-q, --quiet           run in quiet mode, with no output information
-v, --verbose         run in verbose mode, with detailed output information
-y, --yes             yes for all selections
-n, --no-cleanup      do not run cleanup process

miscellaneous arguments
-----------------------

-L *ARG*, --logging *ARG*
                      options for ``pip list --outdated`` command

-U *ARG*, --update *ARG*
                      options for ``pip install --upgrade <package>`` command

SEE ALSO
========

* ``macdaily-update``
* ``macdaily-update-apm``
* ``macdaily-update-brew``
* ``macdaily-update-cask``
* ``macdaily-update-gem``
* ``macdaily-update-mas``
* ``macdaily-update-npm``
* ``macdaily-update-system``

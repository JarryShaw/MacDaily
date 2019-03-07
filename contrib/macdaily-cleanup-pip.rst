====================
macdaily-cleanup-pip
====================

----------------------------
Python Package Cache Cleanup
----------------------------

:Version: v2019.3.7.post2
:Date: November 23, 2018
:Manual section: 1
:Author:
    Jarry Shaw, a newbie programmer, is the author, owner and maintainer
    of *MacDaily*. Please contact me at *jarryshaw@icloud.com*.
:Copyright:
    *MacDaily* is licensed under the **Apple Open Source License**.

SYNOPSIS
========

macdaily **cleanup** *pip* [*options*] ...

OPTIONS
=======

optional arguments
------------------

-h, --help      show this help message and exit
-V, --version   show program's version number and exit

specification arguments
-----------------------

-b, --brew            cleanup caches of Python installed from Homebrew
-c, --cpython         cleanup caches of CPython implementation

-e *VER* [*VER* ...], --python *VER* [*VER* ...]
                      indicate packages from which version of Python will
                      cleanup

-r, --pypy            cleanup caches of PyPy implementation
-s, --system          cleanup caches of Python provided by macOS system

general arguments
-----------------

-q, --quiet     run in quiet mode, with no output information
-v, --verbose   run in verbose mode, with detailed output information

SEE ALSO
========

* ``macdaily-cleanup``
* ``macdaily-cleanup-brew``
* ``macdaily-cleanup-cask``
* ``macdaily-cleanup-npm``

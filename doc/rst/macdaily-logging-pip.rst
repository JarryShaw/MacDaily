====================
macdaily-logging-pip
====================

--------------------------------
Python Package Logging Automator
--------------------------------

:Version: v2019.8.4
:Date: August 07, 2019
:Manual section: 8
:Author:
    Jarry Shaw, a newbie programmer, is the author, owner and maintainer
    of *MacDaily*. Please contact me at *jarryshaw@icloud.com*.
:Copyright:
    *MacDaily* is licensed under the **Apple Open Source License**.

SYNOPSIS
========

macdaily **logging** *pip* [*options*] ...

aliases: **cpython**, **pypy**, **python**

OPTIONS
=======

optional arguments
------------------

-h, --help        show this help message and exit
-V, --version     show program's version number and exit

specification arguments
-----------------------

-x, --exclude-editable
                      exclude editable package from output

-b, --brew            log packages of Python installed from Homebrew
-c, --cpython         log packages of CPython implementation

-e *VER* [*VER* ...], --python *VER* [*VER* ...]
                      indicate packages from which version of Python will be
                      logged

-r, --pypy            log packages of PyPy implementation
-s, --system          log packages of Python provided by macOS system

general arguments
-----------------

-q, --quiet       run in quiet mode, with no output information
-v, --verbose     run in verbose mode, with detailed output information
-n, --no-cleanup  do not run cleanup process
-l, --show-log    open log in *Console.app* upon completion of command

SEE ALSO
========

* ``macdaily-logging``
* ``macdaily-logging-apm``
* ``macdaily-logging-app``
* ``macdaily-logging-brew``
* ``macdaily-logging-cask``
* ``macdaily-logging-gem``
* ``macdaily-logging-mas``
* ``macdaily-logging-npm``
* ``macdaily-logging-tap``

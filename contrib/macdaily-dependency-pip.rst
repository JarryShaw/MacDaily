=======================
macdaily-dependency-pip
=======================

-------------------------------
Python Package Dependency Query
-------------------------------

:Version: v2018.12.15
:Date: November 24, 2018
:Manual section: 1
:Author:
    Jarry Shaw, a newbie programmer, is the author, owner and maintainer
    of *MacDaily*. Please contact me at *jarryshaw@icloud.com*.
:Copyright:
    *MacDaily* is licensed under the **Apple Open Source License**.

SYNOPSIS
========

macdaily **dependency** *pip* [*options*] <*packages*> ...

OPTIONS
=======

optional arguments
------------------

-h, --help            show this help message and exit
-V, --version         show program's version number and exit

specification arguments
-----------------------

-b, --brew            query packages of Python installed from Homebrew
-c, --cpython         query packages of CPython implementation

-e *VER* [*VER* ...], --python *VER* [*VER* ...]
                      indicate packages from which version of Python will
                      query

-r, --pypy            query packages of PyPy implementation
-s, --system          query packages of Python provided by macOS system

-p *PKG* [*PKG* ...], --packages *PKG* [*PKG* ...]
                      name of Python packages to query

general arguments
-----------------

-a, --all             query all Python packages installed through Python
                      Package Index
-q, --quiet           run in quiet mode, with no output information
-v, --verbose         run in verbose mode, with detailed output information
-n, --no-cleanup      do not run cleanup process
-f, --tree            show dependencies as a tree [requires *DictDumper*]
-g, --topological     show dependencies in topological order

-d *LEVEL*, --depth *LEVEL*
                      max display depth of the dependency tree

SEE ALSO
========

* ``macdaily-dependency``
* ``macdaily-dependency-brew``

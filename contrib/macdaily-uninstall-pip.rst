======================
macdaily-uninstall-pip
======================

------------------------------------
Automated Python Package Uninstaller
------------------------------------

:Version: v2019.3.8.post2
:Date: November 24, 2018
:Manual section: 1
:Author:
    Jarry Shaw, a newbie programmer, is the author, owner and maintainer
    of *MacDaily*. Please contact me at *jarryshaw@icloud.com*.
:Copyright:
    *MacDaily* is licensed under the **Apple Open Source License**.

SYNOPSIS
========

macdaily **uninstall** *pip* [*options*] <*packages*> ...

OPTIONS
=======

optional arguments
------------------

-h, --help            show this help message and exit
-V, --version         show program's version number and exit

specification arguments
-----------------------

-b, --brew            uninstall packages of Python installed from Homebrew
-c, --cpython         uninstall packages of CPython implementation
-d, --pre             include pre-release and development versions

-e *VER* [*VER* ...], --python *VER* [*VER* ...]
                      indicate packages from which version of Python will be
                      uninstalled

-r, --pypy            uninstall packages of PyPy implementation
-s, --system          uninstall packages of Python provided by macOS system

-p *PKG* [*PKG* ...], --packages *PKG* [*PKG* ...]
                      name of Python packages to uninstall

general arguments
-----------------

-a, --all             uninstall all Python packages installed through
                      Homebrew
-k, --dry-run         list all Python packages which would be removed, but
                      will not actually delete any Python packages

-i, --ignore-dependencies
                      run in non-recursive mode, i.e. ignore dependencies
                      packages

-q, --quiet           run in quiet mode, with no output information
-v, --verbose         run in verbose mode, with detailed output information
-y, --yes             yes for all selections
-n, --no-cleanup      do not run cleanup process

miscellaneous arguments
-----------------------

-L *ARG*, --logging *ARG*
                      options for ``pip freeze`` command

-U *ARG*, --uninstall *ARG*
                      options for ``pip uninstall <package>`` command

SEE ALSO
========

* ``macdaily-uninstall``
* ``macdaily-uninstall-brew``
* ``macdaily-uninstall-cask``

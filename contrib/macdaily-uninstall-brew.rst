=======================
macdaily-uninstall-brew
=======================

--------------------------------------
Automated Homebrew Formula Uninstaller
--------------------------------------

:Version: v2019.3.8
:Date: November 24, 2018
:Manual section: 1
:Author:
    Jarry Shaw, a newbie programmer, is the author, owner and maintainer
    of *MacDaily*. Please contact me at *jarryshaw@icloud.com*.
:Copyright:
    *MacDaily* is licensed under the **Apple Open Source License**.

SYNOPSIS
========

macdaily **uninstall** *brew* [*options*] <*formulae*> ...

OPTIONS
=======

optional arguments
------------------

-h, --help            show this help message and exit
-V, --version         show program's version number and exit

specification arguments
-----------------------

-f, --force           delete all installed versions
-b, --include-build   include the *:build* type dependencies

-o, --include-optional
                      include *:optional* dependencies

-t, --include-test    include (non-recursive) *:test* dependencies

-s, --skip-recommended
                      skip *:recommended* type dependencies

-r, --include-requirements
                      include requirements in addition to dependencies

-p *FORM* [*FORM* ...], --packages *FORM* [*FORM* ...]
                      name of Homebrew formulae to uninstall

general arguments
-----------------

-a, --all             uninstall all Homebrew formulae installed through
                      Homebrew
-k, --dry-run         list all Homebrew formulae which would be removed, but
                      will not actually delete any Homebrew formulae

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
                      options for ``brew list`` command

-U *ARG*, --uninstall *ARG*
                      options for ``brew uninstall <formula>`` command

SEE ALSO
========

* ``brew(1)``
* ``macdaily-uninstall``
* ``macdaily-uninstall-cask``
* ``macdaily-uninstall-pip``

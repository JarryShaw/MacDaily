=======================
macdaily-reinstall-brew
=======================

--------------------------------------
Automated Homebrew Formula Reinstaller
--------------------------------------

:Version: v2019.01.30
:Date: November 24, 2018
:Manual section: 1
:Author:
    Jarry Shaw, a newbie programmer, is the author, owner and maintainer
    of *MacDaily*. Please contact me at *jarryshaw@icloud.com*.
:Copyright:
    *MacDaily* is licensed under the **Apple Open Source License**.

SYNOPSIS
========

macdaily **reinstall** *brew* [*options*] <*formulae*> ...

OPTIONS
=======

optional arguments
------------------

-h, --help            show this help message and exit
-V, --version         show program's version number and exit

specification arguments
-----------------------

-s *PREFIX*, --startswith *PREFIX*
                      reinstall procedure starts from such formula, sort in
                      initial alphabets

-e *SUFFIX*, --endswith *SUFFIX*
                      reinstall procedure ends after such formula, sort in
                      initial alphabets

-p *FORM* [*FORM* ...], --packages *FORM* [*FORM* ...]
                      name of Homebrew formulae to reinstall

general arguments
-----------------

-a, --all             reinstall all Homebrew formulae installed through
                      Homebrew
-q, --quiet           run in quiet mode, with no output information
-v, --verbose         run in verbose mode, with detailed output information
-y, --yes             yes for all selections
-n, --no-cleanup      do not run cleanup process

miscellaneous arguments
-----------------------

-L *ARG*, --logging *ARG*
                      options for ``brew list`` command

-R *ARG*, --reinstall *ARG*
                      options for ``brew reinstall <formula>`` command

SEE ALSO
========

* ``brew(1)``
* ``macdaily-reinstall``
* ``macdaily-reinstall-cask``

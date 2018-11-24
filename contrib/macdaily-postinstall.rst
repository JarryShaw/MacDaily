====================
macdaily-postinstall
====================

-----------------------------------
Homebrew Cask Postinstall Automator
-----------------------------------

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

macdaily **postinstall** [*options*] ...

aliases: **post**, **ps**

DESCRIPTION
===========

*MacDaily* provides intelligent solution for package postinstall automation.
*MacDaily* ``postinstall`` command will automatically postinstall all specified
packages installed through Homebrew (``brew(1)``).

OPTIONS
=======

optional arguments
------------------

-h, --help            show this help message and exit
-V, --version         show program's version number and exit

specification arguments
-----------------------

-s *PREFIX*, --startswith *PREFIX*
                      postinstall procedure starts from such formula, sort
                      in initial alphabets

-e *SUFFIX*, --endswith *SUFFIX*
                      postinstall procedure ends after such formula, sort in
                      initial alphabets

-p *FORM* [*FORM* ...], --packages *FORM* [*FORM* ...]
                      name of Homebrew formulae to postinstall

general arguments
-----------------

-a, --all             postinstall all Homebrew formulae installed through
                      Homebrew
-q, --quiet           run in quiet mode, with no output information
-v, --verbose         run in verbose mode, with detailed output information
-l, --show-log        open log in *Console.app* upon completion of command
-y, --yes             yes for all selections
-n, --no-cleanup      do not run cleanup process

miscellaneous arguments
-----------------------

-L *ARG*, --logging *ARG*
                      options for ``brew list`` command

-P *ARG*, --postinstall *ARG*
                      options for ``brew postinstall <formula>``
                      command

SEE ALSO
========

* ``brew(1)``

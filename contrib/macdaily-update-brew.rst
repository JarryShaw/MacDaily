====================
macdaily-update-brew
====================

---------------------------------
Homebrew Formula Update Automator
---------------------------------

:Version: v2019.3.31.post1
:Date: March 31, 2019
:Manual section: 8
:Author:
    Jarry Shaw, a newbie programmer, is the author, owner and maintainer
    of *MacDaily*. Please contact me at *jarryshaw@icloud.com*.
:Copyright:
    *MacDaily* is licensed under the **Apple Open Source License**.

SYNOPSIS
========

macdaily **update** *brew* [*options*] <*formulae*> ...

aliases: **homebrew**

OPTIONS
=======

optional arguments
------------------

-h, --help            show this help message and exit
-V, --version         show program's version number and exit

specification arguments
-----------------------

-f, --force           always do a slower, full update check even if
                      unnecessary
-m, --merge           ``git merge`` is used to include updates (rather
                      than ``git rebase``)

-p *FORM* [*FORM* ...], --packages *FORM* [*FORM* ...]
                      name of Homebrew formulae to update

general arguments
-----------------

-a, --all             update all Homebrew formulae installed through
                      Homebrew
-q, --quiet           run in quiet mode, with no output information
-v, --verbose         run in verbose mode, with detailed output information
-y, --yes             yes for all selections
-n, --no-cleanup      do not run cleanup process

miscellaneous arguments
-----------------------

-L *ARG*, --logging *ARG*
                      options for ``brew outdated`` command

-U *ARG*, --update *ARG*
                      options for ``brew upgrade <formula>`` command

SEE ALSO
========

* ``brew(1)``
* ``macdaily-update``
* ``macdaily-update-apm``
* ``macdaily-update-cask``
* ``macdaily-update-gem``
* ``macdaily-update-mas``
* ``macdaily-update-npm``
* ``macdaily-update-pip``
* ``macdaily-update-system``

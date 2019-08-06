====================
macdaily-update-cask
====================

------------------------------
Homebrew Cask Update Automator
------------------------------

:Version: v2019.8.4
:Date: August 06, 2019
:Manual section: 8
:Author:
    Jarry Shaw, a newbie programmer, is the author, owner and maintainer
    of *MacDaily*. Please contact me at *jarryshaw@icloud.com*.
:Copyright:
    *MacDaily* is licensed under the **Apple Open Source License**.

SYNOPSIS
========

macdaily **update** *cask* [*options*] <*casks*> ...

aliases: **brew-cask**, **caskroom**

OPTIONS
=======

optional arguments
------------------

-h, --help            show this help message and exit
-V, --version         show program's version number and exit

specification arguments
-----------------------

-f, --force           use ``--force`` when running ``brew cask
                      upgrade <cask>`` command
-g, --greedy          use ``--greedy`` when running ``brew cask
                      upgrade <cask>`` command
-m, --merge           ``git merge`` is used to include updates (rather
                      than ``git rebase``)
-x, --exhaust         exhaustively check Caskroom for outdated Homebrew
                      Casks

-p *CASK* [*CASK* ...], --packages *CASK* [*CASK* ...]
                      name of Caskroom binaries to update

general arguments
-----------------

-a, --all             update all Caskroom binaries installed through
                      Homebrew
-q, --quiet           run in quiet mode, with no output information
-v, --verbose         run in verbose mode, with detailed output information
-y, --yes             yes for all selections
-n, --no-cleanup      do not run cleanup process

miscellaneous arguments
-----------------------

-L *ARG*, --logging *ARG*
                      options for ``brew cask outdated`` command

-U *ARG*, --update *ARG*
                      options for ``brew cask upgrade <cask>`` command

SEE ALSO
========

* ``brew-cask(1)``
* ``macdaily-update``
* ``macdaily-update-apm``
* ``macdaily-update-brew``
* ``macdaily-update-gem``
* ``macdaily-update-mas``
* ``macdaily-update-npm``
* ``macdaily-update-pip``
* ``macdaily-update-system``

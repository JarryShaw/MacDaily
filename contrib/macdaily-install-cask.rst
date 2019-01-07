=====================
macdaily-install-cask
=====================

---------------------------------
Homebrew Cask Automated Installer
---------------------------------

:Version: v2019.01.07
:Date: November 24, 2018
:Manual section: 1
:Author:
    Jarry Shaw, a newbie programmer, is the author, owner and maintainer
    of *MacDaily*. Please contact me at *jarryshaw@icloud.com*.
:Copyright:
    *MacDaily* is licensed under the **Apple Open Source License**.

SYNOPSIS
========

macdaily **install** *cask* [*options*] <*casks*> ...

OPTIONS
=======

optional arguments
------------------

-h, --help            show this help message and exit
-V, --version         show program's version number and exit

specification arguments
-----------------------

-p *CASK* [*CASK* ...], --packages *CASK* [*CASK* ...]
                      name of Caskroom binaries to install

general arguments
-----------------

-q, --quiet           run in quiet mode, with no output information
-v, --verbose         run in verbose mode, with detailed output information
-y, --yes             yes for all selections
-n, --no-cleanup      do not run cleanup process

miscellaneous arguments
-----------------------

-I *ARG*, --install *ARG*
                      options for ``brew cask install <cask>`` command

SEE ALSO
========

* ``brew-cask(1)``
* ``macdaily-install``
* ``macdaily-install-apm``
* ``macdaily-install-brew``
* ``macdaily-install-gem``
* ``macdaily-install-mas``
* ``macdaily-install-npm``
* ``macdaily-install-pip``
* ``macdaily-install-system``

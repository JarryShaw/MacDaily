=======================
macdaily-uninstall-cask
=======================

-----------------------------------
Automated Homebrew Cask Uninstaller
-----------------------------------

:Version: v2018.11.25
:Date: November 24, 2018
:Manual section: 1
:Author:
    Jarry Shaw, a newbie programmer, is the author, owner and maintainer
    of *MacDaily*. Please contact me at *jarryshaw@icloud.com*.
:Copyright:
    *MacDaily* is licensed under the **GNU General Public License v3.0**.

SYNOPSIS
========

macdaily **uninstall** *cask* [*options*] <*casks*> ...

OPTIONS
=======

optional arguments
------------------

-h, --help            show this help message and exit
-V, --version         show program's version number and exit

specification arguments
-----------------------

-f, --force           uninstall even if the Cask does not appear to be
                      present

-p *CASK* [*CASK* ...], --packages *CASK* [*CASK* ...]
                      name of Caskroom binaries to uninstall

general arguments
-----------------

-a, --all             uninstall all Caskroom binaries installed through
                      Homebrew
-k, --dry-run         list all Caskroom binaries which would be removed, but
                      will not actually delete any Caskroom binaries
-q, --quiet           run in quiet mode, with no output information
-v, --verbose         run in verbose mode, with detailed output information
-y, --yes             yes for all selections
-n, --no-cleanup      do not run cleanup process

miscellaneous arguments
-----------------------

-L *ARG*, --logging *ARG*
                      options for ``brew cask list`` command

-U *ARG*, --uninstall *ARG*
                      options for ``brew cask uninstall <formula>`` command

SEE ALSO
========

* ``brew-cask(1)``
* ``macdaily-uninstall``
* ``macdaily-uninstall-brew``
* ``macdaily-uninstall-pip``

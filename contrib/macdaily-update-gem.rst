===================
macdaily-update-gem
===================

-------------------------
Ruby Gem Update Automator
-------------------------

:Version: v2019.01.08
:Date: November 24, 2018
:Manual section: 1
:Author:
    Jarry Shaw, a newbie programmer, is the author, owner and maintainer
    of *MacDaily*. Please contact me at *jarryshaw@icloud.com*.
:Copyright:
    *MacDaily* is licensed under the **Apple Open Source License**.

SYNOPSIS
========

macdaily **update** *gem* [*options*] <*gems*> ...

OPTIONS
=======

optional arguments
------------------

-h, --help            show this help message and exit
-V, --version         show program's version number and exit

specification arguments
-----------------------

-b, --brew            update gems of Ruby installed from Homebrew
-s, --system          update gems of Ruby provided by macOS system

-p *GEM* [*GEM* ...], --packages *GEM* [*GEM* ...]
                      name of Ruby gems to update

general arguments
-----------------

-a, --all             update all gems installed through RubyGems
-q, --quiet           run in quiet mode, with no output information
-v, --verbose         run in verbose mode, with detailed output information
-y, --yes             yes for all selections

miscellaneous arguments
-----------------------

-L *ARG*, --logging *ARG*
                      options for ``gem outdated`` command

-U *ARG*, --update *ARG*
                      options for ``gem update <gem>`` command

SEE ALSO
========

* ``gem(1)``
* ``macdaily-update``
* ``macdaily-update-apm``
* ``macdaily-update-brew``
* ``macdaily-update-cask``
* ``macdaily-update-mas``
* ``macdaily-update-npm``
* ``macdaily-update-pip``
* ``macdaily-update-system``

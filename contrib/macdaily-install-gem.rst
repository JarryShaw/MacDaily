====================
macdaily-install-gem
====================

----------------------------
Ruby Gem Automated Installer
----------------------------

:Version: v2019.3.28.post1
:Date: March 28, 2019
:Manual section: 8
:Author:
    Jarry Shaw, a newbie programmer, is the author, owner and maintainer
    of *MacDaily*. Please contact me at *jarryshaw@icloud.com*.
:Copyright:
    *MacDaily* is licensed under the **Apple Open Source License**.

SYNOPSIS
========

macdaily **install** *gem* [*options*] <*gems*> ...

aliases: **ruby**, **rubygems**

OPTIONS
=======

optional arguments
------------------

-h, --help            show this help message and exit
-V, --version         show program's version number and exit

specification arguments
-----------------------

-b, --brew            install gems by Ruby installed from Homebrew
-s, --system          install gems by Ruby provided by macOS system

-p *GEM* [*GEM* ...], --packages *GEM* [*GEM* ...]
                      name of Ruby gems to install

general arguments
-----------------

-q, --quiet           run in quiet mode, with no output information
-v, --verbose         run in verbose mode, with detailed output information
-y, --yes             yes for all selections

miscellaneous arguments
-----------------------

-I *ARG*, --install *ARG*
                      options for ``gem install <gem>`` command

SEE ALSO
========

* ``gem(1)``
* ``macdaily-install``
* ``macdaily-install-apm``
* ``macdaily-install-brew``
* ``macdaily-install-cask``
* ``macdaily-install-mas``
* ``macdaily-install-npm``
* ``macdaily-install-pip``
* ``macdaily-install-system``

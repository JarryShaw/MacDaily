====================
macdaily-install-mas
====================

-------------------------------------
macOS Application Automated Installer
-------------------------------------

:Version: v2019.3.12
:Date: March 12, 2019
:Manual section: 8
:Author:
    Jarry Shaw, a newbie programmer, is the author, owner and maintainer
    of *MacDaily*. Please contact me at *jarryshaw@icloud.com*.
:Copyright:
    *MacDaily* is licensed under the **Apple Open Source License**.

SYNOPSIS
========

macdaily **install** *mas* [*options*] <*applications*> ...

aliases: **app-store**, **appstore**, **mac**, **mac-app-store**

OPTIONS
=======

optional arguments
------------------

-h, --help            show this help message and exit
-V, --version         show program's version number and exit

specification arguments
-----------------------

-f, --force           force reinstall

-p *APP* [*APP* ...], --packages *APP* [*APP* ...]
                      name of macOS applications to install

general arguments
-----------------

-q, --quiet           run in quiet mode, with no output information
-v, --verbose         run in verbose mode, with detailed output information
-y, --yes             yes for all selections

miscellaneous arguments
-----------------------

-I *ARG*, --install *ARG*
                      options for ``mas install|lucky <application>`` command

SEE ALSO
========

* ``macdaily-install``
* ``macdaily-install-apm``
* ``macdaily-install-brew``
* ``macdaily-install-cask``
* ``macdaily-install-gem``
* ``macdaily-install-npm``
* ``macdaily-install-pip``
* ``macdaily-install-system``

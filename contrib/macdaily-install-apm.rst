====================
macdaily-install-apm
====================

--------------------------------
Atom Plug-In Automated Installer
--------------------------------

:Version: v2019.03.03
:Date: November 24, 2018
:Manual section: 1
:Author:
    Jarry Shaw, a newbie programmer, is the author, owner and maintainer
    of *MacDaily*. Please contact me at *jarryshaw@icloud.com*.
:Copyright:
    *MacDaily* is licensed under the **Apple Open Source License**.

SYNOPSIS
========

macdaily **install** *apm* [*options*] <*plug-ins*> ...

OPTIONS
=======

optional arguments
------------------

-h, --help            show this help message and exit
-V, --version         show program's version number and exit

specification arguments
-----------------------

-b, --beta            install Atom Beta plug-ins

-p *PI* [*PI* ...], --packages *PI* [*PI* ...]
                      name of Atom plug-ins to install

general arguments
-----------------

-q, --quiet           run in quiet mode, with no output information
-v, --verbose         run in verbose mode, with detailed output information
-y, --yes             yes for all selections

miscellaneous arguments
-----------------------

-I *ARG*, --install *ARG*
                      options for ``apm install <plug-in>`` command

SEE ALSO
========

* ``macdaily-install``
* ``macdaily-install-brew``
* ``macdaily-install-cask``
* ``macdaily-install-gem``
* ``macdaily-install-mas``
* ``macdaily-install-npm``
* ``macdaily-install-pip``
* ``macdaily-install-system``

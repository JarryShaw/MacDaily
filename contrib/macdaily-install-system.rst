=======================
macdaily-install-system
=======================

-----------------------------------
System Software Automated Installer
-----------------------------------

:Version: v2019.01.23
:Date: November 24, 2018
:Manual section: 1
:Author:
    Jarry Shaw, a newbie programmer, is the author, owner and maintainer
    of *MacDaily*. Please contact me at *jarryshaw@icloud.com*.
:Copyright:
    *MacDaily* is licensed under the **Apple Open Source License**.

SYNOPSIS
========

macdaily **install** *system* [*options*] <*software*> ...

OPTIONS
=======

optional arguments
------------------

-h, --help            show this help message and exit
-V, --version         show program's version number and exit

specification arguments
-----------------------

-R, --restart         automatically restart (or shut down) if required to
                      complete installation

-p *SW* [*SW* ...], --packages *SW* [*SW* ...]
                      name of system software to install

general arguments
-----------------

-q, --quiet           run in quiet mode, with no output information
-v, --verbose         run in verbose mode, with detailed output information
-y, --yes             yes for all selections

miscellaneous arguments
-----------------------

-I *ARG*, --install *ARG*
                      options for ``softwareupdate --install
                      <software>`` command

SEE ALSO
========

* ``softwareupdate(8)``
* ``macdaily-install``
* ``macdaily-install-apm``
* ``macdaily-install-brew``
* ``macdaily-install-gem``
* ``macdaily-install-mas``
* ``macdaily-install-npm``
* ``macdaily-install-pip``
* ``macdaily-install-system``

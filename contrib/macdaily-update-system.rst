======================
macdaily-update-system
======================

--------------------------------
System Software Update Automator
--------------------------------

:Version: v2018.11.28
:Date: November 24, 2018
:Manual section: 1
:Author:
    Jarry Shaw, a newbie programmer, is the author, owner and maintainer
    of *MacDaily*. Please contact me at *jarryshaw@icloud.com*.
:Copyright:
    *MacDaily* is licensed under the **GNU General Public License v3.0**.

SYNOPSIS
========

macdaily **update** *system* [*options*] <*software*> ...

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
-r, --recommended     only update software that is recommended for your
                      system

-p *SW* [*SW* ...], --packages *SW* [*SW* ...]
                      name of system software to update

general arguments
-----------------

-a, --all             update all system software installed through
                      ``softwareupdate(8)``
-q, --quiet           run in quiet mode, with no output information
-v, --verbose         run in verbose mode, with detailed output information
-y, --yes             yes for all selections

miscellaneous arguments
-----------------------

-L *ARG*, --logging *ARG*
                      options for ``softwareupdate --list`` command

-U *ARG*, --update *ARG*
                      options for ``softwareupdate --install
                      <software>`` command

SEE ALSO
========

* ``softwareupdate(8)``
* ``macdaily-update``
* ``macdaily-update-apm``
* ``macdaily-update-brew``
* ``macdaily-update-cask``
* ``macdaily-update-gem``
* ``macdaily-update-mas``
* ``macdaily-update-npm``
* ``macdaily-update-pip``

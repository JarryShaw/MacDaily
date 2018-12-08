====================
macdaily-install-npm
====================

----------------------------------
Node.js Module Automated Installer
----------------------------------

:Version: v2018.12.08.post1
:Date: November 24, 2018
:Manual section: 1
:Author:
    Jarry Shaw, a newbie programmer, is the author, owner and maintainer
    of *MacDaily*. Please contact me at *jarryshaw@icloud.com*.
:Copyright:
    *MacDaily* is licensed under the **GNU General Public License v3.0**.

SYNOPSIS
========

macdaily **install** *npm* [*options*] <*modules*> ...

OPTIONS
=======

optional arguments
------------------

-h, --help            show this help message and exit
-V, --version         show program's version number and exit

specification arguments
-----------------------

-p *MOD* [*MOD* ...], --packages *MOD* [*MOD* ...]
                      name of Node.js modules to install

general arguments
-----------------

-q, --quiet           run in quiet mode, with no output information
-v, --verbose         run in verbose mode, with detailed output information
-y, --yes             yes for all selections
-n, --no-cleanup      do not run cleanup process

miscellaneous arguments
-----------------------

-I *ARG*, --install *ARG*
                      options for ``npm install --global <module>`` command

SEE ALSO
========

* ``npm(1)``
* ``macdaily-install``
* ``macdaily-install-apm``
* ``macdaily-install-brew``
* ``macdaily-install-cask``
* ``macdaily-install-gem``
* ``macdaily-install-mas``
* ``macdaily-install-pip``
* ``macdaily-install-system``

====================
macdaily-install-npm
====================

----------------------------------
Node.js Module Automated Installer
----------------------------------

:Version: v2019.8.4
:Date: August 07, 2019
:Manual section: 8
:Author:
    Jarry Shaw, a newbie programmer, is the author, owner and maintainer
    of *MacDaily*. Please contact me at *jarryshaw@icloud.com*.
:Copyright:
    *MacDaily* is licensed under the **Apple Open Source License**.

SYNOPSIS
========

macdaily **install** *npm* [*options*] <*modules*> ...

aliases: **node**, **node.js**

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

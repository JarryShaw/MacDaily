===================
macdaily-update-npm
===================

-------------------------------
Node.js Module Update Automator
-------------------------------

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

macdaily **update** *npm* [*options*] <*modules*> ...

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
                      name of Node.js modules to update

general arguments
-----------------

-a, --all             update all Node.js modules installed through Node.js
                      Package Manager
-q, --quiet           run in quiet mode, with no output information
-v, --verbose         run in verbose mode, with detailed output information
-y, --yes             yes for all selections
-n, --no-cleanup      do not run cleanup process

miscellaneous arguments
-----------------------

-L *ARG*, --logging *ARG*
                      options for ``npm outdated --global`` command

-U *ARG*, --update *ARG*
                      options for ``npm upgrade --global <module>`` command

SEE ALSO
========

* ``npm(1)``
* ``macdaily-update``
* ``macdaily-update-apm``
* ``macdaily-update-brew``
* ``macdaily-update-cask``
* ``macdaily-update-gem``
* ``macdaily-update-mas``
* ``macdaily-update-pip``
* ``macdaily-update-system``

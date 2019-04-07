===================
macdaily-update-apm
===================

-----------------------------
Atom Plug-In Update Automator
-----------------------------

:Version: v2019.4.7
:Date: April 07, 2019
:Manual section: 8
:Author:
    Jarry Shaw, a newbie programmer, is the author, owner and maintainer
    of *MacDaily*. Please contact me at *jarryshaw@icloud.com*.
:Copyright:
    *MacDaily* is licensed under the **Apple Open Source License**.

SYNOPSIS
========

macdaily **update** *apm* [*options*] <*plug-ins*> ...

aliases: **atom**

OPTIONS
=======

optional arguments
------------------

-h, --help            show this help message and exit
-V, --version         show program's version number and exit

specification arguments
-----------------------

-b, --beta            update Atom Beta plug-ins

-p *PI* [*PI* ...], --packages *PI* [*PI* ...]
                      name of Atom plug-ins to update

general arguments
-----------------

-a, --all             update all plug-ins installed through Atom Package
                      Manager
-q, --quiet           run in quiet mode, with no output information
-v, --verbose         run in verbose mode, with detailed output information
-y, --yes             yes for all selections

miscellaneous arguments
-----------------------

-L *ARG*, --logging *ARG*
                      options for ``apm upgrade --list`` command

-U *ARG*, --update *ARG*
                      options for ``apm upgrade <plug-in>`` command

SEE ALSO
========

* ``macdaily-update``
* ``macdaily-update-brew``
* ``macdaily-update-cask``
* ``macdaily-update-gem``
* ``macdaily-update-mas``
* ``macdaily-update-npm``
* ``macdaily-update-pip``
* ``macdaily-update-system``

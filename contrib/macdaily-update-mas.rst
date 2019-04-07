===================
macdaily-update-mas
===================

----------------------------------
macOS Application Update Automator
----------------------------------

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

macdaily **update** *mas* [*options*] <*applications*> ...

aliases: **app-store**, **appstore**, **mac**, **mac-app-store**

OPTIONS
=======

optional arguments
------------------

-h, --help            show this help message and exit
-V, --version         show program's version number and exit

specification arguments
-----------------------

-p *APP* [*APP* ...], --packages *APP* [*APP* ...]
                      name of macOS applications to update

general arguments
-----------------

-a, --all             update all macOS applications installed through Mac
                      App Store
-q, --quiet           run in quiet mode, with no output information
-v, --verbose         run in verbose mode, with detailed output information
-y, --yes             yes for all selections

miscellaneous arguments
-----------------------

-L *ARG*, --logging *ARG*
                      options for ``mas outdated`` command

-U *ARG*, --update *ARG*
                      options for ``mas upgrade <application>`` command

SEE ALSO
========

* ``macdaily-update``
* ``macdaily-update-apm``
* ``macdaily-update-brew``
* ``macdaily-update-cask``
* ``macdaily-update-gem``
* ``macdaily-update-npm``
* ``macdaily-update-pip``
* ``macdaily-update-system``

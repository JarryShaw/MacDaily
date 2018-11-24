===============
macdaily-config
===============

-------------------------------------
MacDaily Runtime Configuration Helper
-------------------------------------

:Version: 2018.11.24
:Date: November 24, 2018
:Manual section: 1
:Author:
    Jarry Shaw, a newbie programmer, is the author, owner
    and maintainer of *MacDaily*. Please contact at *jarryshaw@icloud.com*.
:Copyright:
    *MacDaily* is licensed under the **GNU General Public License v3.0**.

SYNOPSIS
========

macdaily **config** [*options*] <*key*> <*value*> ...

aliases: **init**

DESCRIPTION
===========

*MacDaily* supports customise runtime configuration through a *~/.dailyrc*
file. *MacDaily* ``config`` command will help initialise and/or modify these
configurations.

And *ConfigUpdater* is required to support modification of configuration file,
which is a third-party library able to keep comments after parsing the file.

OPTIONS
=======

optional arguments
------------------

-h, --help         show this help message and exit
-V, --version      show program's version number and exit

specification arguments
-----------------------

-a, --add          adds a new line to the option without altering any
                   existing values [requires *ConfigUpdater*]
-g, --get          get the value for a given key
-u, --unset        remove the line matching the key from config file
                   [requires *ConfigUpdater*]
-i, --interactive  enter interactive configuration mode
-l, --list         list all variables set in config file, along with their
                   values

general arguments
-----------------

:key:              a given key
:value:            the value for a given key

-q, --quiet        run in quiet mode, with no output information
-v, --verbose      run in verbose mode, with detailed output information

control arguments
-----------------

options used to set true or false

-T, --true         set the value for a given key to ``true``
-F, --false        set the value for a given key to ``false``

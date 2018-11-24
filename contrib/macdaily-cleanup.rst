================
macdaily-cleanup
================

---------------------------
macOS Package Cache Cleanup
---------------------------

:Version: 2018.11.24
:Date: November 23, 2018
:Manual section: 1
:Author:
    Jarry Shaw, a newbie programmer, is the author, owner
    and maintainer of *MacDaily*. Please contact at *jarryshaw@icloud.com*.
:Copyright:
    *MacDaily* is licensed under the **GNU General Public License v3.0**.

SYNOPSIS
========

macdaily **cleanup** [*options*] <*mode-selection*> ...

aliases: **clean**

DESCRIPTION
===========

*MacDaily* provides intelligent solution for automate caches cleanup.
*MacDaily* ``cleanup`` command will automatically cleanup all caches of
through --

- *brew* -- Homebrew
- *cask* -- Homebrew Casks
- *npm* -- Node.js Package Manager
- *pip* -- Pip Installs Packages

OPTIONS
=======

optional arguments
------------------

-h, --help      show this help message and exit
-V, --version   show program's version number and exit

general arguments
-----------------

-a, --all       cleanup caches of all packages installed through Node.js,
                Homebrew, Caskroom and Python
-q, --quiet     run in quiet mode, with no output information
-v, --verbose   run in verbose mode, with detailed output information
-l, --show-log  open log in *Console.app* upon completion of command

control arguments
-----------------

options used to disable update of certain mode

--no-npm        do not update Node.js modules
--no-pip        do not update Python packages
--no-brew       do not update Homebrew formulae
--no-cask       do not update Caskroom binaries

mode selection
--------------

cleanup caches of packages installed through a specified method, e.g.:
*npm*, *pip*, *brew*, *cask*

SEE ALSO
========

* ``macdaily-cleanup-brew``
* ``macdaily-cleanup-cask``
* ``macdaily-cleanup-npm``
* ``macdaily-cleanup-pip``

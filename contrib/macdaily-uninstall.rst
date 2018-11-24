==================
macdaily-uninstall
==================

----------------------------------
Automate macOS Package Uninstaller
----------------------------------

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

macdaily **uninstall** [*options*] <*mode-selection*> ...

aliases: **un**, **unlink**, **remove**, **rm**, **r**

DESCRIPTION
===========

*MacDaily* provides intelligent solution for automate package uninstaller.
*MacDaily* ``uninstall`` command will recursively remove all specified
packages installed through --

- *brew* -- Homebrew
- *cask* -- Homebrew Casks
- *pip* -- Pip Installs Packages

OPTIONS
=======

optional arguments
------------------

-h, --help            show this help message and exit
-V, --version         show program's version number and exit

general arguments
-----------------

-a, --all             uninstall all packages installed through Homebrew,
                      Caskroom, and etc
-k, --dry-run         list all packages which would be removed, but will not
                      actually delete any packages

-i, --ignore-dependencies
                      run in non-recursive mode, i.e. ignore dependencies
                      packages

-q, --quiet           run in quiet mode, with no output information
-v, --verbose         run in verbose mode, with detailed output information
-l, --show-log        open log in *Console.app* upon completion of command
-y, --yes             yes for all selections
-n, --no-cleanup      do not run cleanup process

package arguments
-----------------

options used to specify packages of each mode

--pip *PKG* [*PKG* ...]
                      name of Python packages to uninstall

--brew *FORM* [*FORM* ...]
                      name of Homebrew formulae to uninstall

--cask *CASK* [*CASK* ...]
                      name of Caskroom binaries to uninstall

control arguments
-----------------

options used to disable uninstall of certain mode

--no-pip              do not uninstall Python packages
--no-brew             do not uninstall Homebrew formulae
--no-cask             do not uninstall Caskroom binaries

mode selection
--------------

uninstall existing packages installed through a specified method, e.g.:
*pip*, *brew*, *cask*

SEE ALSO
========

* ``macdaily-uninstall-brew``
* ``macdaily-uninstall-cask``
* ``macdaily-uninstall-pip``

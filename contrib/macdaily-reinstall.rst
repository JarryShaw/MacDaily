==================
macdaily-reinstall
==================

----------------------------------
Automate macOS Package Reinstaller
----------------------------------

:Version: 2018.11.24a3
:Date: November 24, 2018
:Manual section: 1
:Author:
    Jarry Shaw, a newbie programmer, is the author, owner
    and maintainer of *MacDaily*. Please contact at *jarryshaw@icloud.com*.
:Copyright:
    *MacDaily* is licensed under the **GNU General Public License v3.0**.

SYNOPSIS
========

macdaily **reinstall** [*options*] <*mode-selection*> ...

aliases: **re**

DESCRIPTION
===========

*MacDaily* provides intelligent solution for automate package reinstaller.
*MacDaily* ``reinstall`` command will recursively reinstall all specified
packages installed through --

- *brew* -- Homebrew
- *cask* -- Homebrew Casks

OPTIONS
=======

optional arguments
------------------

-h, --help            show this help message and exit
-V, --version         show program's version number and exit

general arguments
-----------------

-a, --all             postinstall all Homebrew formulae installed through
                      Homebrew
-q, --quiet           run in quiet mode, with no output information
-v, --verbose         run in verbose mode, with detailed output information
-l, --show-log        open log in *Console.app* upon completion of command
-y, --yes             yes for all selections
-n, --no-cleanup      do not run cleanup process

package arguments
-----------------

options used to specify packages of each mode

--brew *FORM* [*FORM* ...]
                      name of Homebrew formulae to reinstall

--cask *CASK* [*CASK* ...]
                      name of Caskroom binaries to reinstall

control arguments
-----------------

options used to disable reinstall of certain mode

--no-brew             do not reinstall Homebrew formulae
--no-cask             do not reinstall Caskroom binaries

mode selection
--------------

reinstall existing packages installed through a specified method, e.g.:
*brew*, *cask*

SEE ALSO
========

* ``macdaily-reinstall-brew``
* ``macdaily-reinstall-cask``

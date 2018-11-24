===============
macdaily-update
===============

------------------------------
macOS Package Update Automator
------------------------------

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

macdaily **update** [*options*] <*mode-selection*> ...

aliases: **up**, **upgrade**

DESCRIPTION
===========

*MacDaily* provides intelligent solution for package update automation.
*MacDaily* ``update`` command will automatically update all outdated packages
installed through --

- *apm* -- Atom Package Manager
- *brew* -- Homebrew
- *cask* -- Homebrew Casks
- *gem* -- RubyGems
- *mas* -- Mac App Store CLI
- *npm* -- Node.js Package Manager
- *pip* -- Pip Installs Packages
- *system* -- macOS Software Update (``softwareupdate(8)``)

OPTIONS
=======

optional arguments
------------------

-h, --help            show this help message and exit
-V, --version         show program's version number and exit

general arguments
-----------------

-a, --all             update all packages installed through Atom, RubyGems,
                      Node.js, Homebrew, Caskroom, Mac App Store, and etc
-q, --quiet           run in quiet mode, with no output information
-v, --verbose         run in verbose mode, with detailed output information
-l, --show-log        open log in *Console.app* upon completion of command
-y, --yes             yes for all selections
-n, --no-cleanup      do not run cleanup process

package arguments
-----------------

options used to specify packages of each mode

--apm *PI* [*PI* ...] name of Atom plug-ins to update

--gem *GEM* [*GEM* ...]
                      name of Ruby gems to update

--mas *APP* [*APP* ...]
                      name of macOS applications to update

--npm *MOD* [*MOD* ...]
                      name of Node.js modules to update

--pip *PKG* [*PKG* ...]
                      name of Python packages to update

--brew *FORM* [*FORM* ...]
                      name of Homebrew formulae to update

--cask *CASK* [*CASK* ...]
                      name of Caskroom binaries to update

--system *SW* [*SW* ...]
                      name of system software to update

control arguments
-----------------

options used to disable update of certain mode

--no-apm              do not update Atom plug-ins
--no-gem              do not update Ruby gems
--no-mas              do not update macOS applications
--no-npm              do not update Node.js modules
--no-pip              do not update Python packages
--no-brew             do not update Homebrew formulae
--no-cask             do not update Caskroom binaries
--no-system           do not update system software

mode selection
--------------

update outdated packages installed through a specified method, e.g.: *apm*,
*gem*, *mas*, *npm*, *pip*, *brew*, *cask*, *system*

SEE ALSO
========

* ``macdaily-update-apm``
* ``macdaily-update-brew``
* ``macdaily-update-cask``
* ``macdaily-update-gem``
* ``macdaily-update-mas``
* ``macdaily-update-npm``
* ``macdaily-update-pip``
* ``macdaily-update-system``

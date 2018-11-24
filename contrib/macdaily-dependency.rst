===================
macdaily-dependency
===================

------------------------------
macOS Package Dependency Query
------------------------------

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

macdaily **dependency** [*options*] <*mode-selection*> ...

aliases: **deps**, **dp**

DESCRIPTION
===========

*MacDaily* provides intelligent solution for package dependency query.
*MacDaily* ``dependency`` command will automatically query dependencies
of packages installed through --

- *brew* -- Homebrew
- *pip* -- Pip Installs Packages

And for **tree** format support in this command, you will need to install
*DictDumper*, which was a sub-project from development of *PyPCAPKit*.

This command was originally inspired from and leveraged *pipdeptree*.
However, if you would like to use *pipdeptree* for all installed Python
distributions, it is highly recommended to install *pipdeptree* with each
executable, which can be a bit fussy.

OPTIONS
=======

optional arguments
------------------

-h, --help         show this help message and exit
-V, --version      show program's version number and exit

general arguments
-----------------

-a, --all             query all packages installed through Python and
                      Homebrew
-q, --quiet           run in quiet mode, with no output information
-v, --verbose         run in verbose mode, with detailed output information
-n, --no-cleanup      do not run cleanup process
-l, --show-log        open log in *Console.app* upon completion of command
-f, --tree            show dependencies as a tree [requires *DictDumper*]
-g, --topological     show dependencies in topological order

-d *LEVEL*, --depth *LEVEL*
                      max display depth of the dependency tree

package arguments
-----------------

options used to specify packages of each mode

--pip *PKG* [*PKG* ...]
                      name of Python packages to query

--brew *FORM* [*FORM* ...]
                      name of Homebrew formulae to query

control arguments
-----------------

options used to disable update of certain mode

--no-pip              do not query Python packages
--no-brew             do not query Homebrew formulae

mode selection
--------------

query dependency of packages installed through a specified method, e.g.:
*pip*, *brew*

SEE ALSO
========

* ``macdaily-dependency-brew``
* ``macdaily-dependency-pip``

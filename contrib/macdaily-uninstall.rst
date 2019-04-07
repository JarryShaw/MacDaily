==================
macdaily-uninstall
==================

-----------------------------------
Automated macOS Package Uninstaller
-----------------------------------

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

*MacDaily* ``uninstall`` supports using with multiple commands. Say, you would
like to uninstall Python packages and Homebrew formulae, each with different
flags and options, then simply use the following command.

.. code:: shell

    macdaily uninstall [global-options] pip [pip-options] brew [brew-options]

But please note that, global options ``--yes``, ``--quiet``, ``--verbose``
and ``--ignore-dependencies`` are **mandatory** for all commands once set to
``True``. That is to say, if you set these flags in global options, they will
overwrite corresponding flags in command specific options.

For all options that take package names, a mini-language for condition
specification is provided.

+--------------+-----------------------+
|    Format    |     Specification     |
+==============+=======================+
| ``package``  | uninstall ``package`` |
+--------------+-----------------------+
| ``!package`` | ignore ``package``    |
+--------------+-----------------------+

NB
    Since exclamation mark (``!``) has special meanings in ``bash(1)``
    scripts, it is highly recommended using ``'!package'`` literal to
    specify ignoring packages.

When using such options, if given wrong package name, *MacDaily*
might give a trivial *did-you-mean* correction.

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

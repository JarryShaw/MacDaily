==================
macdaily-reinstall
==================

-----------------------------------
Automated macOS Package Reinstaller
-----------------------------------

:Version: v2018.12.10
:Date: November 24, 2018
:Manual section: 1
:Author:
    Jarry Shaw, a newbie programmer, is the author, owner and maintainer
    of *MacDaily*. Please contact me at *jarryshaw@icloud.com*.
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

*MacDaily* ``reinstall`` supports using with multiple commands. Say, you would
like to reinstall Homebrew formulae and Casks, each with different flags and
options, then simply use the following command.

.. code:: shell

    macdaily reinstall [global-options] brew [brew-options] cask [cask-options]

But please note that, global options ``--yes``, ``--quiet``, ``--verbose``
and ``--no-cleanup`` are **mandatory** for all commands once set to ``True``.
That is to say, if you set these flags in global options, they will overwrite
corresponding flags in command specific options.

For all options that take package names, a mini-language for condition
specification is provided.

+--------------+-----------------------+
|    Format    |     Specification     |
+==============+=======================+
| ``package``  | reinstall ``package`` |
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

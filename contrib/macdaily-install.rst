================
macdaily-install
================

---------------------------------
macOS Package Automated Installer
---------------------------------

:Version: v2018.11.28
:Date: November 24, 2018
:Manual section: 1
:Author:
    Jarry Shaw, a newbie programmer, is the author, owner and maintainer
    of *MacDaily*. Please contact me at *jarryshaw@icloud.com*.
:Copyright:
    *MacDaily* is licensed under the **GNU General Public License v3.0**.

SYNOPSIS
========

macdaily **install** [*options*] ...

aliases: **i**

DESCRIPTION
===========

*MacDaily* provides intelligent solution for package automate installation.
*MacDaily* ``install`` command will automatically install all specified
packages through --

- *apm* -- Atom Package Manager
- *brew* -- Homebrew
- *cask* -- Homebrew Casks
- *gem* -- RubyGems
- *mas* -- Mac App Store CLI
- *npm* -- Node.js Package Manager
- *pip* -- Pip Installs Packages
- *system* -- macOS Software Update ``softwareupdate(8)``

*MacDaily* ``install`` supports using with multiple commands. Say, you would
like to install Python packages and Homebrew formulae, each with different
flags and options, then simply use the following command.

.. code:: shell

    macdaily install [global-options] pip [pip-options] brew [brew-options]

But please note that, global options ``--yes``, ``--quiet``, ``--verbose``
and ``--no-cleanup`` are **mandatory** for all commands once set to ``True``.
That is to say, if you set these flags in global options, they will overwrite
corresponding flags in command specific options.

For all options that take package names, a mini-language for condition
specification is provided.

+--------------+---------------------+
|    Format    |    Specification    |
+==============+=====================+
| ``package``  | install ``package`` |
+--------------+---------------------+
| ``!package`` | ignore ``package``  |
+--------------+---------------------+

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

-h, --help         show this help message and exit
-V, --version      show program's version number and exit

general arguments
-----------------

-q, --quiet           run in quiet mode, with no output information
-v, --verbose         run in verbose mode, with detailed output information
-l, --show-log        open log in *Console.app* upon completion of command
-y, --yes             yes for all selections
-n, --no-cleanup      do not run cleanup process

package arguments
-----------------

options used to specify packages of each mode

--apm *PI* [*PI* ...]
                      name of Atom plug-ins to install

--gem *GEM* [*GEM* ...]
                      name of Ruby gems to install

--mas *APP* [*APP* ...]
                      name of macOS applications to install

--npm *MOD* [*MOD* ...]
                      name of Node.js modules to install

--pip *PKG* [*PKG* ...]
                      name of Python packages to install

--brew *FORM* [*FORM* ...]
                      name of Homebrew formulae to install

--cask *CASK* [*CASK* ...]
                      name of Caskroom binaries to install

--system *SW* [*SW* ...]
                      name of system software to install

mode selection
--------------

install packages through a specified method, e.g.: *apm*, *gem*, *mas*, *npm*,
*pip*, *brew*, *cask*, *system*

SEE ALSO
========

* ``macdaily-install-apm``
* ``macdaily-install-brew``
* ``macdaily-install-cask``
* ``macdaily-install-gem``
* ``macdaily-install-mas``
* ``macdaily-install-npm``
* ``macdaily-install-pip``
* ``macdaily-install-system``

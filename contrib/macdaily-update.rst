===============
macdaily-update
===============

------------------------------
macOS Package Update Automator
------------------------------

:Version: v2019.01.22
:Date: November 24, 2018
:Manual section: 1
:Author:
    Jarry Shaw, a newbie programmer, is the author, owner and maintainer
    of *MacDaily*. Please contact me at *jarryshaw@icloud.com*.
:Copyright:
    *MacDaily* is licensed under the **Apple Open Source License**.

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

*MacDaily* ``update`` supports using with multiple commands. Say, you would
like to update Python packages and Homebrew formulae, each with different flags
and options, then simply use the following command.

.. code:: shell

    macdaily update [global-options] pip [pip-options] brew [brew-options]

But please note that, global options ``--yes``, ``--quiet``, ``--verbose``
and ``--no-cleanup`` are **mandatory** for all commands once set to ``True``.
That is to say, if you set these flags in global options, they will overwrite
corresponding flags in command specific options.

For all options that take package names, a mini-language for condition
specification is provided.

+--------------+---------------------+
|    Format    |    Specification    |
+==============+=====================+
| ``package``  | upgrade ``package`` |
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

===================
macdaily-dependency
===================

------------------------------
macOS Package Dependency Query
------------------------------

:Version: v2018.11.27
:Date: November 24, 2018
:Manual section: 1
:Author:
    Jarry Shaw, a newbie programmer, is the author, owner and maintainer
    of *MacDaily*. Please contact me at *jarryshaw@icloud.com*.
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

*MacDaily* ``dependency`` supports using with multiple commands. Say, you would
like to query Python package dependencies and Homebrew formula dependencies,
each with different flags and options, then simply use the following command.

.. code:: shell

    macdaily dependency [global-options] pip [pip-options] brew [brew-options]

But please note that, global options ``--depth``, ``--quiet``, ``--verbose``
and ``--topological`` are **mandatory** for all commands once set to ``True``
(or legal value for ``depth`` option). That is to say, if you set these flags
in global options, they will overwrite corresponding flags in command specific
options.

For all options that take package names, a mini-language for condition
specification is provided.

+--------------+---------------------+
|    Format    |    Specification    |
+==============+=====================+
| ``package``  | query ``package``   |
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

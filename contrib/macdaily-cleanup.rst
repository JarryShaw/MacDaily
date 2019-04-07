================
macdaily-cleanup
================

---------------------------
macOS Package Cache Cleanup
---------------------------

:Version: v2019.4.7.post1
:Date: April 07, 2019
:Manual section: 8
:Author:
    Jarry Shaw, a newbie programmer, is the author, owner and maintainer
    of *MacDaily*. Please contact me at *jarryshaw@icloud.com*.
:Copyright:
    *MacDaily* is licensed under the **Apple Open Source License**.

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

*MacDaily* ``cleanup`` supports using with multiple commands. Say, you would
like to cleanup Python and Homebrew caches, each with different flags and
options, then simply use the following command.

.. code:: shell

    macdaily cleanup [global-options] pip [pip-options] brew [brew-options]

But please note that, global options ``--quiet`` and ``--verbose`` are
**mandatory** for all commands once set to ``True``. That is to say, if you set
these flags in global options, they will overwrite corresponding flags in
command specific options.

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

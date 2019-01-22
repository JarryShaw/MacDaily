================
macdaily-logging
================

-------------------------------
macOS Package Logging Automator
-------------------------------

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

macdaily **logging** [*options*] <*mode-selection*> ...

aliases: **log**

DESCRIPTION
===========

*MacDaily* provides intelligent solution for package logging automation.
*MacDaily* ``logging`` command will automatically record all existing packages
installed through --

- *apm* -- Atom Package Manager
- *app* -- macOS Applications
- *brew* -- Homebrew
- *cask* -- Homebrew Casks
- *gem* -- RubyGems
- *mas* -- Mac App Store CLI
- *npm* -- Node.js Package Manager
- *pip* -- Pip Installs Packages
- *tap* -- Homebrew Taps

*MacDaily* ``logging`` supports using with multiple commands. Say, you would
like to record Python packages and Homebrew formulae, each with different flags
and options, then simply use the following command.

.. code:: shell

    macdaily logging [global-options] pip [pip-options] brew [brew-options]

But please note that, global options ``--yes``, ``--quiet`` and ``--show-log``
are **mandatory** for all commands once set to ``True``. That is to say, if you
set these flags in global options, they will overwrite corresponding flags in
command specific options.

NB
    *MacDaily* will record installed packages using following package
    manager requirement specification formats.

+----------+----------------------+
| Command  |       Log File       |
+==========+======================+
| ``apm``  | ``packages.txt``     |
+----------+----------------------+
| ``app``  | ``macOS.log``        |
+----------+----------------------+
| ``brew`` | ``Brewfile``         |
+----------+----------------------+
| ``cask`` | ``Brewfile``         |
+----------+----------------------+
| ``gem``  | ``lockdown.rb``      |
+----------+----------------------+
| ``mas``  | ``Brewfile``         |
+----------+----------------------+
| ``npm``  | ``package.json``     |
+----------+----------------------+
| ``pip``  | ``requirements.txt`` |
+----------+----------------------+
| ``tap``  | ``Brewfile``         |
+----------+----------------------+

OPTIONS
=======

optional arguments
------------------

-h, --help         show this help message and exit
-V, --version      show program's version number and exit

general arguments
-----------------

-a, --all         log all packages installed through Atom, RubyGems,
                  Node.js, Homebrew, Caskroom, Mac App Store, and etc
-q, --quiet       run in quiet mode, with no output information
-v, --verbose     run in verbose mode, with detailed output information
-n, --no-cleanup  do not run cleanup process
-l, --show-log    open log in *Console.app* upon completion of command

control arguments
-----------------

options used to disable logging of certain mode

--no-apm          do not log Atom plug-ins
--no-app          do not log system applications
--no-gem          do not log Ruby gems
--no-mas          do not log macOS applications
--no-npm          do not log Node.js modules
--no-pip          do not log Python packages
--no-tap          do not log Homebrew Taps
--no-brew         do not log Homebrew formulae
--no-cask         do not log Homebrew Casks

mode selection
--------------

log existing packages installed through a specified method, e.g.: *apm*,
*app*, *gem*, *mas*, *npm*, *pip*, *tap*, *brew*, *cask*

SEE ALSO
========

* ``macdaily-logging-apm``
* ``macdaily-logging-app``
* ``macdaily-logging-brew``
* ``macdaily-logging-cask``
* ``macdaily-logging-gem``
* ``macdaily-logging-mas``
* ``macdaily-logging-npm``
* ``macdaily-logging-pip``
* ``macdaily-logging-tap``

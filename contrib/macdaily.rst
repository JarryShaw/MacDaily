========
macdaily
========

-------------------------------
macOS Automated Package Manager
-------------------------------

:Version: v2019.3.9
:Date: March 09, 2019
:Manual section: 8
:Author:
    Jarry Shaw, a newbie programmer, is the author, owner and maintainer
    of *MacDaily*. Please contact me at *jarryshaw@icloud.com*.
:Copyright:
    *MacDaily* is licensed under the **Apple Open Source License**.

SYNOPSIS
========

macdaily [*options*] <*command*> ...

DESCRIPTION
===========

**MacDaily** is an all-in-one collection of console utility written in Python
with support of `PTY <https://en.wikipedia.org/wiki/Pseudo_terminal>`__.
Originally works as an automated housekeeper for Mac to update all packages
outdated, **MacDaily** is now fully functioned and end-user oriented.

**MacDaily** can manage packages of various distributions of
`Atom <https://atom.io>`__, `RubyGems <https://rubygems.org>`__,
`Homebrew <https://brew.sh>`__, `Python <https://pypy.org>`__,
`Node.js <https://nodejs.org>`__, and even macOS software updates (c.f.
``softwareupdate(8)``). Without being aware of everything about your Mac, one
can easily work around and manage packages out of no pain using **MacDaily**.

EXAMPLES
========

:NOTE:
    all acronyms and aliases are left out for a quick and
    clear view of **MacDaily**

- How to use **MacDaily**?

.. code:: shell

    # call from PATH
    $ macdaily <command> [option ...]
    # or call as Python module
    $ python -m macdaily <command> [option ...]
    # or call a certain command
    $ md-${command} [option ...]

- How to set up my disks and daemons interactively?

.. code:: shell

    $ macdaily config --interactive

- How to relaunch daemons after I manually modified *~/.dailyrc*?

.. code:: shell

    $ macdaily launch daemons

- How to archive all ancient logs without running any commands?

.. code:: shell

    $ macdaily archive --all

- How to update all outdated packages?

.. code:: shell

   $ macdaily update --all

- How to update a certain package (eg: *hello* from Homebrew)?

.. code:: shell

    $ macdaily update brew --packages=hello

- How to update without a certain package (eg: update all packages
  except Python package *ptyng*)?

.. code:: shell

    $ macdaily update --all --pip='!ptyng'

- How to uninstall a certain package along with its dependencies (eg:
  *pytest* from brewed CPython version 3.6)?

.. code:: shell

    $ macdaily uninstall pip \
          --brew --cpython --python=3.6 --packages=pytest

- How to reinstall all packages but do not cleanup caches?

.. code:: shell

    $ macdaily reinstall --all --no-cleanup

- How to postinstall packages whose name ranges between *start* and
  *stop* alphabetically?

.. code:: shell

    $ macdaily postinstall --all --start=start --end=stop

- How to show dependency of a certain package as a tree (eg: *gnupg*
  from Homebrew) ?

.. code:: shell

   $ macdaily dependency brew  --tree --packages=gnupg

- How to log all applications on my Mac, a.k.a. *\*.app* files?

.. code:: shell

    $ macdaily logging dotapp

- How to dump a *Macfile* to keep track of all packages?

.. code:: shell

   $ macdaily bundle dump

OPTIONS
=======

optional arguments
------------------

-h, --help     show this help message and exit
-V, --version  show program's version number and exit

command selection
-----------------

MacDaily provides a friendly CLI workflow for the administrator of macOS
to manipulate packages, see **macdaily commands** for more information

:archive: archive ancient runtime logs
:bundle: bundler for all packages on your Mac
:cleanup: remove outdated downloads, caches, etc.
:commands: show available commands and corresponding subsidiaries
:config: get and set MacDaily runtime options
:dependency: show dependencies for packages
:help: show man pages for *command*
:install: install packages
:launch: launch daemon services and helper programs
:logging: record packages on your Mac
:postinstall: run the post-install steps for Homebrew *formula*
:reinstall: reinstall existing packages
:uninstall: recursively uninstall packages
:update: update packages

SEE ALSO
========

* MacDaily documentation: *https://github.com/JarryShaw/MacDaily#generals*

* MacDaily Log Archive Utility

  * ``macdaily-archive``

* macOS Package Cache Cleanup

  * ``macdaily-cleanup``
  * ``macdaily-cleanup-brew``
  * ``macdaily-cleanup-cask``
  * ``macdaily-cleanup-npm``
  * ``macdaily-cleanup-pip``

* MacDaily Runtime Configuration Helper

  * ``macdaily-config``

* macOS Package Dependency Query

  * ``macdaily-dependency``
  * ``macdaily-dependency-brew``
  * ``macdaily-dependency-pip``

* MacDaily Usage Information Manual

  * ``macdaily-help``

* macOS Package Automated Installer

  * ``macdaily-install``
  * ``macdaily-install-apm``
  * ``macdaily-install-brew``
  * ``macdaily-install-cask``
  * ``macdaily-install-gem``
  * ``macdaily-install-mas``
  * ``macdaily-install-npm``
  * ``macdaily-install-pip``
  * ``macdaily-install-system``

* MacDaily Dependency Launch Helper

  * ``macdaily-launch``

* macOS Package Logging Automator

  * ``macdaily-logging``
  * ``macdaily-logging-apm``
  * ``macdaily-logging-app``
  * ``macdaily-logging-brew``
  * ``macdaily-logging-cask``
  * ``macdaily-logging-gem``
  * ``macdaily-logging-mas``
  * ``macdaily-logging-npm``
  * ``macdaily-logging-pip``
  * ``macdaily-logging-tap``

* Homebrew Cask Postinstall Automator

  * ``macdaily-postinstall``

* Automated macOS Package Reinstaller

  * ``macdaily-reinstall``
  * ``macdaily-reinstall-brew``
  * ``macdaily-reinstall-cask``

* Automated macOS Package Uninstaller

  * ``macdaily-uninstall``
  * ``macdaily-uninstall-brew``
  * ``macdaily-uninstall-cask``
  * ``macdaily-uninstall-pip``

* macOS Package Update Automator

  * ``macdaily-update``
  * ``macdaily-update-apm``
  * ``macdaily-update-brew``
  * ``macdaily-update-cask``
  * ``macdaily-update-gem``
  * ``macdaily-update-mas``
  * ``macdaily-update-npm``
  * ``macdaily-update-pip``
  * ``macdaily-update-system``

BUGS
====

If any bugs, please file issues on GitHub:

:JarryShaw/MacDaily: https://github.com/JarryShaw/MacDaily/issues

Contribution is welcome.

========
macdaily
========

------------------------------
macOS Automate Package Manager
------------------------------

:Version: 2018.11.24a3
:Date: November 23, 2018
:Manual section: 1
:Author:
    Jarry Shaw, a newbie programmer, is the author, owner
    and maintainer of *MacDaily*. Please contact at *jarryshaw@icloud.com*.
:Copyright:
    *MacDaily* is licensed under the **GNU General Public License v3.0**.

SYNOPSIS
========

macdaily [*options*] <*command*> ...

DESCRIPTION
===========

**MacDaily** is a mediate collection of console scripts written in Python
with support of `PTY <https://en.wikipedia.org/wiki/Pseudo_terminal>`__.
Originally works as an automatic housekeeper for Mac to update all packages
outdated, **MacDaily** is now fully functioned and end-user oriented. Without
being aware of everything about your Mac, one can easily work around and
manage packages out of no pain using **MacDaily**.

EXAMPLES
========

:NOTE:
    all acronyms and aliases are left out for a quick and
    clear view of **MacDaily**

- How to use **MacDaily**?

.. code:: shell

    # call from PATH
    $ macdaily [command ...] [option ...]
    # or call as Python module
    $ python -m macdaily [command ...] [option ...]
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

    $ macdaily update brew --package=hello

- How to update without a certain package (eg: update all packages
  except Python package *ptyng*)?

.. code:: shell

    $ macdaily update --all --pip='!ptyng'

- How to uninstall a certain package along with its dependencies (eg:
  *pytest* from brewed CPython version 3.6)?

.. code:: shell

    $ macdaily uninstall pip \
          --brew --cpython --python=3.6 --package pytest

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

   $ macdaily dependency brew  --tree --package=gnupg

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

Commands
--------

**MacDaily** provides a friendly CLI workflow for the administrator of macOS
to manipulate packages

SEE ALSO
========

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

* macOS Package Automate Installer

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

* Automate macOS Package Reinstaller

  * ``macdaily-reinstall``
  * ``macdaily-reinstall-brew``
  * ``macdaily-reinstall-cask``

* Automate macOS Package Uninstaller

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

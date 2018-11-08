:Platform:
    OS X Yosemite, OS X El Capitan, macOS Sierra
    macOS High Sierra, macOS Mojave
:Language: Python (version ≥ 3.4)
:Environment: Console | Terminal

========
MacDaily
========

|download| |version| |format| |status|

|python| |implementation|

- `About <#about>`__
- `Installation <#installation>`__
- `Configuration <#configuration>`__
- `Usage Manual <#usage-manual>`__

  - `Start-Up <#start-up>`__
  - `Commands <#commands>`__
  - `Generals <#generals>`__

- `Troubleshooting <#troubleshooting>`__
- `TODO <#todo>`__

--------------

About
-----

  Package day-care manager on macOS.

**MacDaily** is a mediate collection of console scripts written in Python
with support of `PTY <https://en.wikipedia.org/wiki/Pseudo_terminal>`__.
Originally works as an automatic housekeeper for Mac to update all packages
outdated, **MacDaily** is now fully functioned and end-user oriented. Without
being aware of everything about your Mac, one can easily work around and
manage packages out of no pain using **MacDaily**.

Installation
------------

NB
    MacDaily runs only with support of Python from version **3.4**
    or higher. And it shall only work ideally on **macOS**.

Just as many Python packages, MacDaily can be installed through
``pip`` using the following command, which will get you the latest
version from `PyPI <https://pypi.org>`__.

.. code:: shell

    $ pip install macdaily

Or if you prefer the real-latest version and fetch from this Git
repository, then the script below should be used.

.. code:: shell

    $ git clone https://github.com/JarryShaw/MacDaily.git
    $ cd MacDaily
    $ pip install -e .
    # and to update at any time
    $ git pull

Also, for best performance of MacDaily, the notable automation tool
|expect|_ is expected to be installed on your Mac. Recommended installation
approach is from `Homebrew <https://brew.sh>`__, as shown below.

.. code:: shell

    $ brew install expect

.. |expect| replace:: ``expect``
.. _expect: https://core.tcl.tk/expect

Or if you prefer not to install ``unbuffer``, MacDaily will use
|UNIX script utility|_ instead. Make sure that ``/usr/bin/script``
exists and ``/usr/bin`` is in your ``PATH`` environment variable.

.. |UNIX script utility| replace:: UNIX ``script`` utility
.. _UNIX script utility: https://en.wikipedia.org/wiki/Script_(Unix)

For the worst case, MacDaily adopts |ptyng|_ as an alternative. It is
a revised version of |Python pty module|_, intended to support
pseudo-terminal (PTY) on macOS with no further issue. To install ``ptyng``,
you may use the script below.

.. |ptyng| replace:: ``ptyng``
.. _ptyng: https://github.com/JarryShaw/ptyng
.. |Python pty module| replace:: Python ``pty`` module
.. _Python pty module: https://docs.python.org/3/library/pty.html

.. code:: shell

    $ pip install macdaily[ptyng]
    # or explicitly...
    $ pip install macdaily ptyng

And for **tree** format support in ``dependency`` command, you may need
|pipdeptree|_, then implicitly you can use the following script to do
so. However, if you would like to use ``pipdeptree`` for all installed
Python distributions, it is highly recommended to install ``pipdeptree``
with each executable.

.. |pipdeptree| replace:: ``pipdeptree``
.. _pipdeptree: https://github.com/naiquevin/pipdeptree

.. code:: shell

    $ pip install macdaily[pipdeptree]
    # or explicitly...
    $ pip install macdaily pipdeptree

Configuration
-------------

    This part might be kind of garrulous, for some may not know what's
    going on here. 😉

Since robust enough, MacDaily now supports configuration upon
user's own wish. One may set up log path, hard disk path, archive path
and many other things, other than the default settings.

NB
    MacDaily now supports configuration commands,
    see manual of |config|_ command for more information.

The configuration file should lie under ``~/.dailyrc``, which is hidden
from Finder by macOS. To review or edit it, you may use text editors
like ``vim`` and/or ``nano``, or other graphic editors, such as Sublime
Text and/or Virtual Studio Code, or whatever you find favourable.

.. code:: ini

    [Path]
    # In this section, paths for log files are specified.
    # Please, under any circumstances, make sure they are valid.
    logdir = ~/Library/Logs/MacDaily                            ; path where logs will be stored
    dskdir = /Volumes/Your Disk                                 ; path where your hard disk lies
    arcdir = ${dskdir}/Developers                               ; path where ancient logs archive

    [Mode]
    # In this section, flags for modes are configured.
    # If you would like to disable the mode, set it to "false".
    apm      = true                                             ; Atom plug-ins
    app      = true                                             ; macOS Applications
    brew     = true                                             ; Homebrew Formulae
    cask     = true                                             ; Homebrew Casks
    cleanup  = true                                             ; cleanup caches
    gem      = true                                             ; Ruby gems
    mas      = true                                             ; Mac App Store applications
    npm      = true                                             ; Node.js modules
    pip      = true                                             ; Python packages
    system   = true                                             ; macOS software

    [Daemon]
    # In this section, scheduled tasks are set up.
    # You may append and/or remove the time intervals.
    archive     = false                                         ; archive logs
    bundle      = false                                         ; bundle packages
    cleanup     = false                                         ; cleanup caches
    config      = false                                         ; config MacDaily
    dependency  = false                                         ; show dependencies
    launch      = false                                         ; launch daemons
    logging     = true                                          ; log installed packages
    postinstall = false                                         ; postinstall packages
    reinstall   = false                                         ; reinstall packages
    uninstall   = false                                         ; uninstall packages
    update      = true                                          ; update packages
    schedule    =                                               ; scheduled timing (in 24 hours)
        8:00                                                    ; update & logging at 8:00
        22:30-update                                            ; update at 22:30
        23:00-logging                                           ; logging at 23:00

    [Command]
    # In this section, command options are picked.
    # Do make sure these options are available for commands.
    update  = --all --yes --pre --quiet --show-log --no-cask
    logging = --all --quiet --show-log

    [Miscellanea]
    # In this section, miscellaneous specifications are assigned.
    # Please, under any circumstances, make sure all fields are valid.
    askpass = /usr/local/bin/macdaily-askpass                   ; SUDO_ASKPASS utility for Homebrew Casks
    confirm = /usr/local/bin/macdaily-confirm                   ; confirm utility for MacDaily
    timeout = 300                                               ; timeout limit for shell commands in seconds

Above is the default content of ``.dailyrc``, following the grammar of
``INI`` files. Lines and words after number sign (``#``) and semicolon
(``;``) are comments, whose main purpose is to help understanding the
contents of this file.

In section ``Path``, there are path names where logs and some other
things to be stored. In section ``Mode``, there are ten different
modes to indicate if they are *enabled* or *disabled*.

You may wish to set the ``dskdir`` -- *path where your hard disk lies*,
which allows MacDaily to archive your ancient logs and caches into
somewhere never bothers.

Please **NOTE** that, under all circumstances, of section ``Path``,
all values would better be a **valid path name without blank
characters** (``' \t\n\r\f\v'``), except your hard disk ``dskdir``.

Besides, in section ``Daemon``, you can decide which command is
scheduled and when to run such command, with the format of
``HH:MM[-CMD]``. The ``CMD`` is optional, which will be ``any`` if
omits. And you may set up which command(s) will be registered as daemons
and run with schedule through booleans above. These boolean values
help MacDaily indicate which is to be launched when commands in
schedule omit. That is to say, when ``CMD`` omits in schedule, MacDaily
will register all commands that set ``true`` in the above boolean values.

Also, in section ``Option``, you may set up optional arguments for
the daemons above. Do please make sure these commands are **valid**. And
if omit, an empty arguments will be given.

Last but no least, in section ``Miscellanea``, you should **NEVER**
modify any contents under this section in order to keep MacDaily
working. However, you may set up this part with |config|_ command.

Usage Manual
------------

Start-Up
~~~~~~~~

Before we dive into the detailed usage of MacDaily, let's firstly
get our hands dirty with some simple commands.

    **NOTE** -- all acronyms and aliases are left out for a quick and
    clear view of MacDaily

1. How to use MacDaily?

.. code:: shell

    # call from PATH
    $ macdaily [command ...] [flag ...]
    # or call as Python module
    $ python -m macdaily [command ...] [flag ...]

2. How to set up my disks and daemons?

.. code:: shell

    $ macdaily config

3.  How to relaunch daemons after I manually modified ``~/.dailyrc``?

.. code:: shell

    $ macdaily launch

4.  How to archive ancient logs without running any commands?

.. code:: shell

    $ macdaily archive

5.  How to update all outdated packages?

.. code:: shell

   $ macdaily update --all

6.  How to update a certain package (eg: ``hello`` from Homebrew)?

.. code:: shell

    $ macdaily update brew --package=hello

7. How to update without a certain package (eg: update all packages
   except Python package ``ptyng``)?

.. code:: shell

    $ macdaily update --all --pip='!ptyng'

8.  How to uninstall a certain package along with its dependencies (eg:
    ``pytest`` from brewed CPython version 3.6)?

.. code:: shell

    $ macdaily uninstall pip --brew --cpython --python=3.6 --package pytest

9.  How to reinstall all packages but do not cleanup caches?

.. code:: shell

    $ macdaily reinstall --all --no-cleanup

10.  How to postinstall packages whose name ranges between "start" and
     "stop" alphabetically?

.. code:: shell

    $ macdaily postinstall --all --start=start --end=stop

11. How to show dependency of a certain package as a tree (eg: ``gnupg``
    from Homebrew) ?

.. code:: shell

   $ macdaily dependency brew  --tree --package=gnupg

12. How to log all applications on my Mac, a.k.a. ``*.app`` files?

.. code:: shell

    $ macdaily logging dotapp

13. How to dump a ``Macfile`` to keep track of all packages?

.. code:: shell

   $ macdaily bundle dump

Commands
~~~~~~~~

MacDaily supports several different commands. Of all commands,
there are corresponding **aliases** for which to be reckoned as
valid.

+----------------+-----------------------------------------------+
|    Command     |                  Aliases                      |
+================+===============================================+
| |archive|_     |                                               |
+----------------+-----------------------------------------------+
| |bundle|_      |                                               |
+----------------+-----------------------------------------------+
| |config|_      | ``cfg``                                       |
+----------------+-----------------------------------------------+
| |launch|_      | ``init``                                      |
+----------------+-----------------------------------------------+
| |update|_      | ``up``, ``upgrade``                           |
+----------------+-----------------------------------------------+
| |uninstall|_   | ``un``, ``unlink``, ``remove``, ``rm``, ``r`` |
+----------------+-----------------------------------------------+
| |reinstall|_   | ``re``                                        |
+----------------+-----------------------------------------------+
| |postinstall|_ | ``post``, ``ps``,                             |
+----------------+-----------------------------------------------+
| |dependency|_  | ``deps``, ``dp``                              |
+----------------+-----------------------------------------------+
| |logging|_     | ``log``                                       |
+----------------+-----------------------------------------------+

Generals
~~~~~~~~

The man page of MacDaily shows as below.

.. code:: man

    $ macdaily --help
    usage: macdaily [-h] command

    Package Day Care Manager

    optional arguments:
      -h, --help     show this help message and exit
      -V, --version  show program's version number and exit

    Commands:
      macdaily provides a friendly CLI workflow for the administrator of macOS to
      manipulate packages

Commands for ``macdaily`` is shown as above and they are mandatory. For
more detailed usage information, please refer to manuals of corresponding
commands. For developers, internal details can be found in |miscellanea|_
manual. And here is a brief catalogue for the manuals.

- `Archive Command <https://github.com/JarryShaw/MacDaily/blob/dev/doc/archive.rst>`__
- `Bundle Command <https://github.com/JarryShaw/MacDaily/blob/dev/doc/bundle.rst>`__

  - `Dump Macfile <https://github.com/JarryShaw/MacDaily/blob/dev/doc/bundle.rst#dump>`__
  - `Load Macfile <https://github.com/JarryShaw/MacDaily/blob/dev/doc/bundle.rst#load>`__

- `Cleanup Command <https://github.com/JarryShaw/MacDaily/blob/dev/doc/cleanup.rst>`__

  - `Homebrew Formulae <https://github.com/JarryShaw/MacDaily/blob/dev/doc/cleanup.rst#brew>`__
  - `Caskroom Binaries <https://github.com/JarryShaw/MacDaily/blob/dev/doc/cleanup.rst#brew>`__
  - `Node.js Modules <https://github.com/JarryShaw/MacDaily/blob/dev/doc/cleanup.rst#npm>`__
  - `Python Packages <https://github.com/JarryShaw/MacDaily/blob/dev/doc/cleanup.rst#pip>`__

- `Config Command <https://github.com/JarryShaw/MacDaily/blob/dev/doc/config.rst>`__
- `Dependency Command <https://github.com/JarryShaw/MacDaily/blob/dev/doc/dependency.rst>`__

  - `Homebrew Formulae <https://github.com/JarryShaw/MacDaily/blob/dev/doc/dependency.rst#brew>`__
  - `Python Packages <https://github.com/JarryShaw/MacDaily/blob/dev/doc/dependency.rst#pip>`__

- `Launch Command <https://github.com/JarryShaw/MacDaily/blob/dev/doc/launch.rst>`__
- `Logging Command <https://github.com/JarryShaw/MacDaily/blob/dev/doc/logging.rst>`__

  - `Atom Plug-Ins <https://github.com/JarryShaw/MacDaily/blob/dev/doc/logging.rst#apm>`__
  - `Mac Applications <https://github.com/JarryShaw/MacDaily/blob/dev/doc/logging.rst#app>`__
  - `Homebrew Formulae <https://github.com/JarryShaw/MacDaily/blob/dev/doc/logging.rst#brew>`__
  - `Caskroom Binaries <https://github.com/JarryShaw/MacDaily/blob/dev/doc/logging.rst#cask>`__
  - `Ruby Gem <https://github.com/JarryShaw/MacDaily/blob/dev/doc/logging.rst#gem>`__
  - `macOS Applications <https://github.com/JarryShaw/MacDaily/blob/dev/doc/logging.rst#mas>`__
  - `Node.js Modules <https://github.com/JarryShaw/MacDaily/blob/dev/doc/logging.rst#npm>`__
  - `Python Packages <https://github.com/JarryShaw/MacDaily/blob/dev/doc/logging.rst#pip>`__

- `Postinstall Command <https://github.com/JarryShaw/MacDaily/blob/dev/doc/postinstall.rst>`__
- `Reinstall Command <https://github.com/JarryShaw/MacDaily/blob/dev/doc/reinstall.rst>`__

  - `Homebrew Formulae <https://github.com/JarryShaw/MacDaily/blob/dev/doc/logging.rst#brew>`__
  - `Caskroom Binaries <https://github.com/JarryShaw/MacDaily/blob/dev/doc/logging.rst#cask>`__

- `Uninstall Command <https://github.com/JarryShaw/MacDaily/blob/dev/doc/uninstall.rst>`__

  - `Homebrew Formulae <https://github.com/JarryShaw/MacDaily/blob/dev/doc/uninstall.rst#brew>`__
  - `Caskroom Binaries <https://github.com/JarryShaw/MacDaily/blob/dev/doc/uninstall.rst#cask>`__
  - `Python Package <https://github.com/JarryShaw/MacDaily/blob/dev/src/uninstall.rst#pip>`__

- `Update Command <https://github.com/JarryShaw/MacDaily/blob/dev/doc/update.rst>`__

  - `Atom Plug-Ins <https://github.com/JarryShaw/MacDaily/blob/dev/doc/update.rst#apm>`__
  - `Homebrew Formulae <https://github.com/JarryShaw/MacDaily/blob/dev/doc/update.rst#brew>`__
  - `Caskroom Binaries <https://github.com/JarryShaw/MacDaily/blob/dev/doc/update.rst#cask>`__
  - `Ruby Gems <https://github.com/JarryShaw/MacDaily/blob/dev/doc/update.rst#gem>`__
  - `macOS Applications <https://github.com/JarryShaw/MacDaily/blob/dev/doc/update.rst#mas>`__
  - `Node.js Modules <https://github.com/JarryShaw/MacDaily/blob/dev/doc/update.rst#npm>`__
  - `Python Package <https://github.com/JarryShaw/MacDaily/blob/dev/src/update.rst#pip>`__
  - `System Software <https://github.com/JarryShaw/MacDaily/blob/dev/src/update.rst#system>`__

- `Developer Manual <https://github.com/JarryShaw/MacDaily/blob/dev/doc/miscellanea.rst>`__

  - `Project Structure <https://github.com/JarryShaw/MacDaily/blob/dev/doc/miscellanea.rst#repo>`__
  - `Command Classes <https://github.com/JarryShaw/MacDaily/blob/dev/doc/miscellanea.rst#cmd>`__
  - `Miscellaneous Utilities <https://github.com/JarryShaw/MacDaily/blob/dev/doc/miscellanea.rst#util>`__

    - `ANSI Sequences <https://github.com/JarryShaw/MacDaily/blob/dev/doc/miscellanea.rst#color>`__
    - `Print Utilities <https://github.com/JarryShaw/MacDaily/blob/dev/doc/miscellanea.rst#print>`__
    - |script|_

.. |script| replace:: UNIX ``script``
.. _script: https://github.com/JarryShaw/MacDaily/blob/dev/doc/miscellanea.rst#script

Troubleshooting
---------------

1. Where can I find the log files?
    It depends. Since the path where logs go can be modified through
    ``~/.dailyrc``, it may vary as your settings. In default, you may
    find them under ``~/Library/Logs/Scripts``. And with every command,
    logs can be found in its corresponding folder. Logs are named after
    its running time, in the fold with corresponding date as its name.

    Note that, normally, you can only find today's logs in the folder,
    since ``macdaily`` automatically archive ancient logs into
    ``${logdir}/archive`` folder. And every week, ``${logdir}/archive``
    folder will be tape-archived into ``${logdir}/tarfile``. Then after a
    month, and your hard disk available, they will be moved into
    ``/Volumes/Your Disk/Developers/archive.zip``.

2. What if my hard disk ain't plugged-in when running the scripts?
    Then the archiving and removing procedure will **NOT** perform. In
    case there might be some useful resources of yours.

3. Which directory should I set in the configuration file?
    First and foremost, I highly recommend you **NOT** to modify the
    paths in ``~/.dailyrc`` manually, **EXCEPT** your disk path
    ``dskdir``.

    But if you insist to do so, then make sure they are **VALID** and
    **available** with permission granted, and most importantly, have
    **NO** blank characters (``' \t\n\r\f\v'``) in the path, except
    ``dskdir``.

TODO
----

- ✔️ support configuration
- ✔️ support command aliases
- ❌ reconstruct archiving procedure
- ❌ support ``gem`` and ``npm`` in all commands
- ❌ considering support more versions of Python
- ✔️ optimise ``KeyboardInterrupt`` handling procedure
- ✔️ review ``pip`` implementation and version indication
- ❌ add ``--user`` for ``pip`` commands

.. |archive| replace:: ``archive``
.. _archive: https://github.com/JarryShaw/MacDaily/blob/dev/doc/archive.rst
.. |bundle| replace:: ``bundle``
.. _bundle: https://github.com/JarryShaw/MacDaily/blob/dev/doc/bundle.rst
.. |cleanup| replace:: ``cleanup``
.. _cleanup: https://github.com/JarryShaw/MacDaily/blob/dev/doc/cleanup.rst
.. |config| replace:: ``config``
.. _config: https://github.com/JarryShaw/MacDaily/blob/dev/doc/config.rst
.. |dependency| replace:: ``dependency``
.. _dependency: https://github.com/JarryShaw/MacDaily/blob/dev/doc/dependency.rst
.. |launch| replace:: ``launch``
.. _launch: https://github.com/JarryShaw/MacDaily/blob/dev/doc/launch.rst
.. |logging| replace:: ``logging``
.. _logging: https://github.com/JarryShaw/MacDaily/blob/dev/doc/logging.rst
.. |miscellanea| replace:: ``miscellanea``
.. _miscellanea: https://github.com/JarryShaw/MacDaily/blob/dev/doc/miscellanea.rst
.. |postinstall| replace:: ``postinstall``
.. _postinstall: https://github.com/JarryShaw/MacDaily/blob/dev/doc/postinstall.rst
.. |reinstall| replace:: ``reinstall``
.. _reinstall: https://github.com/JarryShaw/MacDaily/blob/dev/doc/reinstall.rst
.. |uninstall| replace:: ``uninstall``
.. _uninstall: https://github.com/JarryShaw/MacDaily/blob/dev/doc/uninstall.rst
.. |update| replace:: ``update``
.. _update: https://github.com/JarryShaw/MacDaily/blob/dev/doc/update.rst

.. |download| image:: http://pepy.tech/badge/macdaily
   :target: http://pepy.tech/count/macdaily
.. |version| image:: https://img.shields.io/pypi/v/macdaily.svg
   :target: https://pypi.org/project/macdaily
.. |format| image:: https://img.shields.io/pypi/format/macdaily.svg
   :target: https://pypi.org/project/macdaily
.. |status| image:: https://img.shields.io/pypi/status/macdaily.svg
   :target: https://pypi.org/project/macdaily
.. |python| image:: https://img.shields.io/pypi/pyversions/macdaily.svg
   :target: https://python.org
.. |implementation| image:: https://img.shields.io/pypi/implementation/macdaily.svg
   :target: http://pypy.org

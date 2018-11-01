+---------------------+----------------------+-------------+
|      Platform       |       Language       | Environment |
+=====================+======================+=============+
| | OS X Yosemite     | |                    | |           |
| | OS X El Capitan   | | Python             | | Console   |
| | macOS Sierra      | |                    | |           |
| | macOS High Sierra | | Bourne-Again Shell | | Terminal  |
| | macOS Mojave      |                      |             |
+---------------------+----------------------+-------------+

========
MacDaily
========

|image0| |image1| |image2| |image3|

|image4| |image5| |image6| |image7|

- `About <#about>`__

- `Installation <#installation>`__

- `Configuration <#configuration>`__

- `Usage Manual <#usage-manual>`__

  - `Start-Up <#startup-up>`__

  - `Commands <#commands>`__

  - `Generals <#generals>`__

- `Troubleshooting <#troubleshooting>`__

- `TODO <#todo>`__

--------------

About
-----

Package day-care manager on macOS.

``macdaily`` is a mediate collection of console scripts written in
**Python** and **Bourne-Again Shell**. Originally works as an automatic
housekeeper for Mac to update all packages outdated, ``macdaily`` is now
fully functioned and end-user oriented. Without being aware of
everything about your Mac, one can easily work around and manage
packages out of no pain using ``macdaily``.

Installation
------------

Just as many Python packages, ``macdaily`` can be installed through
``pip`` using the following command, which will get you the latest
version from `PyPI <https://pypi.org>`__.

.. code:: shell

    pip install macdaily

Or if you prefer the real-latest version and fetch from this Git
repository, then the script below should be used.

.. code:: shell

    git clone https://github.com/JarryShaw/macdaily.git
    cd macdaily
    pip install -e .
    # and to update at any time
    git pull

And for tree format support in dependency command, you may need
``pipdeptree``, then implicitly you can use the following script to do
so.

.. code:: shell

    pip install macdaily[pipdeptree]
    # or explicitly...
    pip install macdaily pipdeptree

Do please **NOTE** that, ``macdaily`` runs only with support of Python
from version **3.4** and on. And it shall only work ideally on
**macOS**.

Configuration
-------------

    This part might be kind of garrulous, for some may not know what's
    going on here. 😉

Since robust enough, ``macdaily`` now supports configuration upon
user's own wish. One may set up log path, hard disk path, archive path
and many other things, other than the default settings.

   **NOTA BENE** -- ``macdaily`` now supports configuration commands,
   see `Config
   Procedure <https://github.com/JarryShaw/MacDaily/tree/master/src#config>`__
   section for more information.

The configuration file should lie under ``~/.dailyrc``, which is hidden
from Finder by macOS. To review or edit it, you may use text editors
like ``vim`` and/or ``nano``, or other graphic editors, such as
``Sublime Text`` and/or ``Atom``, or whatever you find favourable.

.. code:: ini

    [Path]
    # In this section, paths for log files are specified.
    # Please, under any circumstances, make sure they are valid.
    logdir = ~/Library/Logs/MacDaily    ; path where logs will be stored
    tmpdir = /tmp/dailylog              ; path where temporary runtime logs go
    dskdir = /Volumes/Your Disk         ; path where your hard disk lies
    arcdir = ${dskdir}/Developers       ; path where ancient logs archive

    [Mode]
    # In this section, flags for modes are configured.
    # If you would like to disable the mode, set it to "false".
    apm      = true     ; Atom packages
    gem      = true     ; Ruby gems
    mas      = true     ; Mac App Store applications
    npm      = true     ; Node.js modules
    pip      = true     ; Python packages
    brew     = true     ; Homebrew Cellars
    cask     = true     ; Caskroom Casks
    dotapp   = true     ; Applications (*.app)
    macapp   = true     ; all applications in /Application folder
    system   = true     ; macOS system packages
    cleanup  = true     ; cleanup caches
    appstore = true     ; Mac App Store applications in /Application folder

    [Daemon]
    # In this section, scheduled tasks are set up.
    # You may append and/or remove the time intervals.
    update      = true      ; run update on schedule
    uninstall   = false     ; don't run uninstall
    reinstall   = false     ; don't run reinstall
    postinstall = false     ; don't run postinstall
    dependency  = false     ; don't run dependency
    logging     = true      ; run logging on schedule
    schedule    =           ; scheduled timing (in 24 hours)
        8:00                ; update & logging at 8:00
        22:30-update        ; update at 22:30
        23:00-logging       ; logging at 23:00

    [Option]
    # In this section, command options are picked.
    # Do make sure these options are available for commands.
    update  = --all --yes --pre --quiet --show-log --no-cask
    logging = --all --quiet --show-log

    [Account]
    # In this section, account information are stored.
    # You must not modify this part under any circumstances.
    username = ...
    password = ********

    [Environment]
    # In this section, environment specifications are set up.
    # Please, under any circumstances, make sure all fields are valid.
    bash-timeout = 1000     ; timeout limit for each shell script in seconds
    sudo-timeout = 5m       ; sudo command timeout as specified in /etc/sudoers

Above is the default content of ``.dailyrc``, following the grammar of
``INI`` files. Lines and words after number sign (``'#'``) and semicolon
(``';'``) are comments, whose main purpose is to help understanding the
contents of this file.

In section ``[Path]``, there are path names where logs and some other
things to be stored. In section ``[Mode]``, there are ten different
modes to indicate if they are *enabled* or *disabled* when calling from
``--all`` option.

You may wish to set the ``dskdir`` -- *path where your hard disk lies*,
which allows ``macdaily`` to archive your ancient logs and caches into
somewhere never bothers.

Please **NOTE** that, under all circumstances, of section ``[Path]``,
all values would better be a **valid path name without blank
characters** (``\t\n\r\f\v``), except your hard disk ``dskdir``.

Besides, in section ``[Daemon]``, you can decide which command is
scheduled and when to run such command, with the format of
``HH:MM[-CMD]``. The ``CMD`` is optional, which will be ``any`` if
omits. And you may setup which command(s) will be registered as daemons
and run with schedule through six booleans above. These boolean values
help ``macdaily`` indicate which is to be launched when commands in
``schedule`` omit. That is to say, when ``command`` omits in
``schedule``, ``macdaily`` will register all commands that set ``true``
in the above boolean values.

Also, in section ``[Option]``, you may set up optional arguments for
the daemons above. Do please make sure these commands are **valid**. And
if omit, an empty arguments will be given.

Last but no least, in section ``[Account]``, you should **NEVER**
modify any contents under this section in order to keep ``macdaily``
working. However, you may setup this part with ``config`` command.

Usage Manual
------------

Start-Up
~~~~~~~~

Before we dive into the detailed usage of ``macdaily``, let's firstly
get our hands dirty with some simple commands.

    **NOTE** -- all acronyms and aliases are left out for a quick and
    clear view of ``macdaily``

1. How to use ``macdaily``?

.. code:: shell

    # call from $PATH
    $ macdaily [command ...] [flag ...]
    # or call from Python module
    $ python -m macdaily [command ...] [flag ...]

2. How to setup my disks and daemons?

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

6.  How to update a certain package (eg: ``hello`` from Homebrew) ?

.. code:: shell

    $ macdaily update brew --package hello

7.  How to uninstall a certain package along with its dependencies (eg:
    ``pytest`` from brewed CPython version 3.6) ?

.. code:: shell

    $ macdaily uninstall pip --brew --cpython --python_version=3 --package pytest

8.  How to reinstall all packages but do not cleanup caches?

.. code:: shell

    $ macdaily reinstall --all --no-cleanup

9.  How to postinstall packages whose name ranges between "start" and
    "stop" alphabetically?

.. code:: shell

    $ macdaily postinstall --all --startwith=start --endwith=stop

10. How to show dependency of a certain package as a tree (eg: ``gnupg``
    from Homebrew) ?

.. code:: shell

   $ macdaily dependency brew --package gnupg --tree

11. How to log all applications on my Mac, a.k.a. ``*.app`` files?

.. code:: shell

    $ macdaily logging dotapp

12. How to run ``macdaily`` in quiet mode, i.e. with no output
    information (eg: ``logging`` in quiet mode) ?

.. code:: shell

    $ macdaily logging --all --quiet

13. How to dump a ``Macfile`` to keep track of all packages?

.. code:: shell

   $ macdaily bundle dump

Commands
~~~~~~~~

``macdaily`` supports several different commands, from ``archive``,
``bundle``, ``config``, ``launch``, ``update``, ``uninstall``,
``reinstall`` and ``postinstall`` to ``dependency`` and ``logging``. Of
all commands, there are corresponding **aliases** for which to be
reckoned as valid.

+-----------------+-------------------------------------------+
|     Command     |                  Aliases                  |
+=================+===========================================+
| ``archive``     |                                           |
+-----------------+-------------------------------------------+
| ``bundle``      |                                           |
+-----------------+-------------------------------------------+
| ``config``      | ``cfg``                                   |
+-----------------+-------------------------------------------+
| ``launch``      | ``init``                                  |
+-----------------+-------------------------------------------+
| ``update``      | ``up``, ``upgrade``                       |
+-----------------+-------------------------------------------+
| ``uninstall``   | ``un``, ``remove``, ``rm``, ``r``, ``un`` |
+-----------------+-------------------------------------------+
| ``reinstall``   | ``re``                                    |
+-----------------+-------------------------------------------+
| ``postinstall`` | ``post``, ``ps``,                         |
+-----------------+-------------------------------------------+
| ``dependency``  | ``deps``, ``dp``                          |
+-----------------+-------------------------------------------+
| ``logging``     | ``log``                                   |
+-----------------+-------------------------------------------+

Generals
~~~~~~~~

The man page of ``macdaily`` shows as below.

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
more detailed usage information, please refer to the `MacDaily General
Manual <https://github.com/JarryShaw/MacDaily/tree/master/src#macdaily-general-manual>`__.
And here is a brief catalogue for the manual.

- `Archive
  Procedure <https://github.com/JarryShaw/MacDaily/tree/master/src#archive>`__

- `Config
  Procedure <https://github.com/JarryShaw/MacDaily/tree/master/src#config>`__

- `Launch
  Procedure <https://github.com/JarryShaw/MacDaily/tree/master/src#launch>`__

- `Update
  Procedure <https://github.com/JarryShaw/MacDaily/tree/master/src#update>`__

  - `Atom
    Plug-In <https://github.com/JarryShaw/MacDaily/tree/master/src/libupdate#update_apm>`__

  - `Ruby
    Gem <https://github.com/JarryShaw/MacDaily/tree/master/src/libupdate#update_gem>`__

  - `Mac App
    Store <https://github.com/JarryShaw/MacDaily/tree/master/src/libupdate#update_mas>`__

  - `Node.js
    Module <https://github.com/JarryShaw/MacDaily/tree/master/src/libupdate#update_npm>`__

  - `Python
    Package <https://github.com/JarryShaw/MacDaily/tree/master/src/libupdate#update_pip>`__

  - `Homebrew
    Formula <https://github.com/JarryShaw/MacDaily/tree/master/src/libupdate#update_brew>`__

  - `Caskroom
    Binary <https://github.com/JarryShaw/MacDaily/tree/master/src/libupdate#update_cask>`__

  - `System
    Software <https://github.com/JarryShaw/MacDaily/tree/master/src/libupdate#update_system>`__

  - `Cleanup
    Procedure <https://github.com/JarryShaw/MacDaily/tree/master/src/libupdate#update_cleanup>`__

- `Uninstall
  Procedure <https://github.com/JarryShaw/MacDaily/tree/master/src#uninstall>`__

  - `Python
    Package <https://github.com/JarryShaw/MacDaily/tree/master/src/libuninstall#uninstall_pip>`__

  - `Homebrew
    Formula <https://github.com/JarryShaw/MacDaily/tree/master/src/libuninstall#uninstall_brew>`__

  - `Caskroom
    Binary <https://github.com/JarryShaw/MacDaily/tree/master/src/libuninstall#uninstall_cask>`__

- `Reinstall
  Procedure <https://github.com/JarryShaw/MacDaily/tree/master/src#reinstall>`__

  - `Homebrew
    Formula <https://github.com/JarryShaw/MacDaily/tree/master/src/libprinstall#reinstall_brew>`__

  - `Caskroom
    Binary <https://github.com/JarryShaw/MacDaily/tree/master/src/libprinstall#reinstall_cask>`__

  - `Cleanup
    Procedure <https://github.com/JarryShaw/MacDaily/tree/master/src/libprinstall#reinstall_cleanup>`__

- `Postinstall
  Procedure <https://github.com/JarryShaw/MacDaily/tree/master/src#postinstall>`__

  - `Homebrew
    Formula <https://github.com/JarryShaw/MacDaily/tree/master/src/libprinstall#postinstall_brew>`__

  - `Cleanup
    Procedure <https://github.com/JarryShaw/MacDaily/tree/master/src/libprinstall#postinstall_cleanup>`__

- `Dependency
  Procedure <https://github.com/JarryShaw/MacDaily/tree/master/src#dependency>`__

  - `Python
    Package <https://github.com/JarryShaw/MacDaily/tree/master/src/libdependency#dependency_pip>`__

  - `Homebrew
    Formula <https://github.com/JarryShaw/MacDaily/tree/master/src/libdependency#dependency_brew>`__

- `Logging
  Procedure <https://github.com/JarryShaw/MacDaily/tree/master/src#logging>`__

  - `Atom
    Plug-In <https://github.com/JarryShaw/MacDaily/tree/master/src/liblogging#logging_apm>`__

  - `Ruby
    Gem <https://github.com/JarryShaw/MacDaily/tree/master/src/liblogging#logging_gem>`__

  - `Node.js
    Module <https://github.com/JarryShaw/MacDaily/tree/master/src/liblogging#logging_npm>`__

  - `Python
    Package <https://github.com/JarryShaw/MacDaily/tree/master/src/liblogging#logging_pip>`__

  - `Homebrew
    Formula <https://github.com/JarryShaw/MacDaily/tree/master/src/liblogging#logging_brew>`__

  - `Caskroom
    Binary <https://github.com/JarryShaw/MacDaily/tree/master/src/liblogging#logging_cask>`__

  - `macOS
    Application <https://github.com/JarryShaw/MacDaily/tree/master/src/liblogging#logging_dotapp>`__

  - `Installed
    Application <https://github.com/JarryShaw/MacDaily/tree/master/src/liblogging#logging_macapp>`__

  - `Mac App
    Store <https://github.com/JarryShaw/MacDaily/tree/master/src/liblogging#logging_appstore>`__

- `Bundle
  Procedure <https://github.com/JarryShaw/MacDaily/tree/master/src#bundle>`__

  - `Dump
    Macfile <https://github.com/JarryShaw/MacDaily/tree/master/src/libbundle#bundle_dump>`__

  - `Load
    Macfile <https://github.com/JarryShaw/MacDaily/tree/master/src/libbundle#bundle_load>`__

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
   **NO** blank characters (``\t\n\r\f\v``) in the path, except
   ``dskdir``.

TODO
----

- support configuration

- support command aliases

- reconstruct archiving procedure

- support ``gem`` and ``npm`` in all commands

- optimise ``KeyboardInterrupt`` handling procedure

- review ``pip`` implementation and version indication

- considering support more versions of Python

.. |image0| image:: http://pepy.tech/badge/macdaily
   :target: http://pepy.tech/count/macdaily
.. |image1| image:: https://img.shields.io/pypi/v/macdaily.svg
   :target: https://pypi.org/project/macdaily
.. |image2| image:: https://img.shields.io/pypi/format/macdaily.svg
   :target: https://pypi.org/project/macdaily
.. |image3| image:: https://img.shields.io/pypi/status/macdaily.svg
   :target: https://pypi.org/project/macdaily
.. |image4| image:: https://img.shields.io/github/languages/top/JarryShaw/macdaily.svg
   :target: https://github.com/JarryShaw/macdaily
.. |image5| image:: https://img.shields.io/badge/Made%20with-Bash-1f425f.svg
   :target: https://www.gnu.org/software/bash
.. |image6| image:: https://img.shields.io/pypi/pyversions/macdaily.svg
   :target: https://python.org
.. |image7| image:: https://img.shields.io/pypi/implementation/macdaily.svg
   :target: http://pypy.org

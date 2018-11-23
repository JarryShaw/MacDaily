:Command Executable:
    ``macdaily archive`` | ``md-archive``
:Supported Commands:
    ``archive``, ``cleanup``, ``dependency``,
    ``logging``, ``postinstall``, ``reinstall``,
    ``uninstall``, ``update``, ``logging/apm``,
    ``logging/app``, ``logging/brew``, ``logging/cask``,
    ``logging/gem``, ``logging/mas``, ``logging/npm``,
    ``logging/pip``, ``logging/tap``

============================
MacDaily Log Archive Utility
============================

- `About <#about>`__
- `Usage <#usage>`__
- `TODO <#todo>`__

--------------

About
-----

MacDaily provides a genuine interface for archiving ancient logs and files.
The ``archive`` command will move all ancient logs to where it belongs
--

1. daily logs from last week (7 days) -- ``${logdir}/arcfile`` with
   corresponding modes named as ``YYMMDD.tar.gz``
2. weekly archives from last month (approximately 4 weeks) --
   ``${logdir}/tarfile`` with corresponding modes named as
   ``YYMMDD-YYMMDD.tar.xz``
3. even older logs -- inside ``${arcdir}/archive.zip`` with
   corresponding modes and named as ``YYMMDD-YYMMDD.tar.bz``

Actual paths of ``${logdir}`` and ``${arcdir}`` are defined in
``~/.dailyrc``, may vary from your own settings.

Usage
-----

.. code:: man

    usage: macdaily archive [options] <path-selection> ...

    MacDaily Log Archive Utility

    optional arguments:
      -h, --help        show this help message and exit
      -V, --version     show program's version number and exit

    specification arguments:
      CMD               archive logs of specified command, e.g. archive, cleanup,
                        dependency, logging, postinstall, reinstall, uninstall,
                        update, logging/apm, logging/app, logging/brew,
                        logging/cask, logging/gem, logging/mas, logging/npm,
                        logging/pip and logging/tap

    general arguments:
      -a, --all         archive all ancient logs
      -n, --no-storage  do not move ancient logs into external hard disk
      -q, --quiet       run in quiet mode, with no output information
      -v, --verbose     run in verbose mode, with detailed output information
      -l, --show-log    open log in Console.app upon completion of command

TODO
----

- ✔️ reconstruct archive CLI
- ❌ implement further spec for archive commands

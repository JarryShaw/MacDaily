:Command Executable:
    ``macdaily config`` | ``md-config``
:Supported Commands:
    ``key-value`` (obsolete)

=====================================
MacDaily Runtime Configuration Helper
=====================================

- `About <#about>`__
- `Usage <#usage>`__
- `TODO <#todo>`__

--------------

About
-----

MacDaily supports customise runtime configuration through a ``.dailyrc`` file.
MacDaily ``config`` command will help initialise and/or modify these
configurations.

And |configupdater| is required to support modification of configuration file,
which is a third-party library able to keep comments after parsing the file.

.. |configupdater| replace:: ``ConfigUpdater``
.. _configupdater: https://configupdater.readthedocs.io

Usage
-----

.. code:: man

    usage: macdaily config [-h] [-V] [options] <key> <value> ...

    MacDaily Runtime Configuration Helper

    optional arguments:
      -h, --help         show this help message and exit
      -V, --version      show program's version number and exit

    specification arguments:
      -a, --add          adds a new line to the option without altering any
                         existing values
      -g, --get          get the value for a given key
      -u, --unset        remove the line matching the key from config file
      -i, --interactive  enter interactive configuration mode
      -l, --list         list all variables set in config file, along with their
                         values

    general arguments:
      key                a given key
      value              the value for a given key
      -q, --quiet        run in quiet mode, with no output information
      -v, --verbose      run in verbose mode, with detailed output information

    control arguments:
      options used to set true or false

      -T, --true         set the value for a given key to 'true'
      -F, --false        set the value for a given key to 'false'

    aliases: init

This command was originally inspired from ``git config`` command. And the usage
of MacDaily ``config`` command is alike. Also, *interactive* mode can be a
great help for you to set up MacDaily on your computer.

TODO
----

- ✔️ reconstruct config CLI
- ❌ implement further configuration settings

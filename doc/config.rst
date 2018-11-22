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

And |configupdater|_ is required to support modification of configuration file,
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
great help for you to set up MacDaily on your computer. The sample procedure
shows as below.

.. code:: shell

    $ macdaily config --interactive --quiet
    Entering interactive command line setup procedure...
    Default settings are shown as in the square brackets.
    Please directly ENTER if you prefer the default settings.

    For logging utilities, we recommend you to set up your hard disk path.
    You may change other path preferences in configuration `~/.dailyrc` later.
    Please note that all paths must be valid under all circumstances.
    Name of your external hard disk []:

    In default, we will run update and logging commands twice a day.
    You may change daily commands preferences in configuration `~/.dailyrc` later.
    Please enter schedule as HH:MM-CMD format, and each separates with comma.
    Time for daily scripts [8:00,22:30-update,23:00-logging]:

    For better stability, MacDaily depends on several helper programs.
    Your password may be necessary during the launch process.
    Enter passphrase for /Users/***/.ssh/id_rsa (will confirm each use):

    Also, MacDaily supports several different environment setups.
    You may set up these variables here, or later manually in configuration `~/.dailyrc`.
    Please enter these specifications as instructed below.
    Timeout limit for shell scripts in seconds [1,000]:

    Configuration for MacDaily finished. Now launching...

TODO
----

- ✔️ reconstruct config CLI
- ❌ implement further configuration settings

:Command Executable:
    ``macdaily postinstall`` | ``md-postinstall``

===================================
Homebrew Cask Postinstall Automator
===================================

- `About <#about>`__
- `Usage <#usage>`__
- `TODO <#todo>`__

--------------

About
-----

MacDaily provides intelligent solution for package postinstall automation.
MacDaily ``postinstall`` command will automatically postinstall all specified
packages installed through |brew|_ (`Homebrew <https://brew.sh>`__).

Usage
-----

.. code:: man

    usage: macdaily postinstall <general-options> <spec-options> <misc-options> ...

    Homebrew Cask Postinstall Automator

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit

    specification arguments:
      -s PREFIX, --startswith PREFIX
                            postinstall procedure starts from such formula, sort
                            in initial alphabets
      -e SUFFIX, --endswith SUFFIX
                            postinstall procedure ends after such formula, sort in
                            initial alphabets
      -p FORM [FORM ...], --packages FORM [FORM ...]
                            name of Homebrew formulae to postinstall

    general arguments:
      -a, --all             postinstall all Homebrew formulae installed through
                            Homebrew
      -q, --quiet           run in quiet mode, with no output information
      -v, --verbose         run in verbose mode, with detailed output information
      -y, --yes             yes for all selections
      -n, --no-cleanup      do not run cleanup process

    miscellaneous arguments:
      -L ARG, --logging ARG
                            options for 'brew list' command
      -U ARG, --postinstall ARG
                            options for 'brew postinstall <formula>'
                            command

    aliases: post, ps

For ``--packages`` option that take package names, a
mini-language for condition specification is provided.

+--------------+---------------------+
|    Format    |    Specification    |
+==============+=====================+
| ``package``  | upgrade ``package`` |
+--------------+---------------------+
| ``!package`` | ignore ``package``  |
+--------------+---------------------+

NB
    Since exclamation mark (``!``) has special meanings in
    `Shell <https://en.wikipedia.org/wiki/Shell_script>`__ scripts,
    it is highly recommended using ``'!package'`` literal to specify
    ignoring packages.

When using ``--package`` option, if given wrong package name, MacDaily
might give a trivial *did-you-mean* correction.

For *miscellaneous arguments*, the runtime commands are as below.

+------------------------+-------------------------------------------------+
|         Option         |                     Command                     |
+========================+=================================================+
| ``--logging=ARG``      | ``brew list ${ARG}``                            |
+------------------------+-------------------------------------------------+
| ``--postinstall=ARG``  | ``brew postinstall [options] ${ARG} <formula>`` |
+------------------------+-------------------------------------------------+

TODO
----

- ✔️ reconstruct update CLI
- ❌ implement further spec for the mini-language

.. |brew| replace:: ``brew``
.. _brew: #brew

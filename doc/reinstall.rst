:Command Executable:
    ``macdaily reinstall`` | ``md-reinstall``
:Supported Commands:
    ``brew``, ``cask``

===================================
Automated macOS Package Reinstaller
===================================

- `About <#about>`__
- `Usage <#usage>`__
- `Commands <#commands>`__

  - `Homebrew Formulae <#brew>`__
  - `Caskroom Binaries <#cask>`__
  - `Python Package <#pip>`__

- `TODO <#todo>`__

--------------

About
-----

MacDaily provides intelligent solution for automate package reinstaller.
MacDaily ``reinstall`` command will recursively reinstall all specified
packages installed through --

- |brew|_ -- `Homebrew <https://brew.sh>`__
- |cask|_ -- `Homebrew Casks <https://caskroom.github.io>`__

Usage
-----

.. code:: man

    usage: macdaily reinstall [options] <mode-selection> ...

    Automated macOS Package Reinstaller

    optional arguments:
    -h, --help            show this help message and exit
    -V, --version         show program's version number and exit

    general arguments:
    -a, --all             reinstall all packages installed through Homebrew,
                          Caskroom, and etc
    -q, --quiet           run in quiet mode, with no output information
    -v, --verbose         run in verbose mode, with detailed output information
    -l, --show-log        open log in Console.app upon completion of command
    -y, --yes             yes for all selections
    -n, --no-cleanup      do not run cleanup process

    package arguments:
    options used to specify packages of each mode

    --brew FORM [FORM ...]
                          name of Homebrew formulae to reinstall
    --cask CASK [CASK ...]
                          name of Caskroom binaries to reinstall

    control arguments:
    options used to disable reinstall of certain mode

    --no-brew             do not reinstall Homebrew formulae
    --no-cask             do not reinstall Caskroom binaries

    mode selection:
    reinstall existing packages installed through a specified method, e.g.:
    brew, cask

    aliases: re

MacDaily ``reinstall`` supports using with multiple commands. Say, you would
like to reinstall Homebrew formulae and Casks, each with different flags and
options, then simply use the following command.

.. code:: shell

    macdaily reinstall [global-options] brew [brew-options] cask [cask-options]

But please note that, global options ``--yes``, ``--quiet``, ``--verbose``
and ``--no-cleanup`` are *mandatory* for all commands once set to ``True``.
That is to say, if you set these flags in global options, they will overwrite
corresponding flags in command specific options.

For all options that take package names, a mini-language for condition
specification is provided.

+--------------+-----------------------+
|    Format    |     Specification     |
+==============+=======================+
| ``package``  | reinstall ``package`` |
+--------------+-----------------------+
| ``!package`` | ignore ``package``    |
+--------------+-----------------------+

NB
    Since exclamation mark (``!``) has special meanings in
    `Shell <https://en.wikipedia.org/wiki/Shell_script>`__ scripts,
    it is highly recommended using ``'!package'`` literal to specify
    ignoring packages.

When using such options, if given wrong package name, *MacDaily*
might give a trivial *did-you-mean* correction.

Commands
--------

.. raw:: html

    <h4>
      <a name="brew">
        Automated Homebrew Formula Reinstaller
      </a>
    </h4>

.. code:: man

    usage: macdaily reinstall brew [options] <formulae> ...

    Automated Homebrew Formula Reinstaller

    optional arguments:
    -h, --help            show this help message and exit
    -V, --version         show program's version number and exit

    specification arguments:
    -s PREFIX, --startswith PREFIX
                          reinstall procedure starts from such formula, sort in
                          initial alphabets
    -e SUFFIX, --endswith SUFFIX
                          reinstall procedure ends after such formula, sort in
                          initial alphabets
    -p FORM [FORM ...], --packages FORM [FORM ...]
                          name of Homebrew formulae to reinstall

    general arguments:
    -a, --all             reinstall all Homebrew formulae installed through
                          Homebrew
    -q, --quiet           run in quiet mode, with no output information
    -v, --verbose         run in verbose mode, with detailed output information
    -y, --yes             yes for all selections
    -n, --no-cleanup      do not run cleanup process

    miscellaneous arguments:
      -L ARG, --logging ARG
                          options for 'brew list' command
      -R ARG, --reinstall ARG
                          options for 'brew reinstall <formula>' command

    aliases: homebrew

When using ``--packages`` option, if given wrong package name, MacDaily
might give a trivial *did-you-mean* correction.

For *miscellaneous arguments*, the runtime commands are as below.

+----------------------+-----------------------------------------------+
|        Option        |                    Command                    |
+======================+===============================================+
| ``--logging=ARG``    | ``brew list ${ARG}``                          |
+----------------------+-----------------------------------------------+
| ``--reinstall=ARG``  | ``brew reinstall [options] ${ARG} <formula>`` |
+----------------------+-----------------------------------------------+

.. raw:: html

    <h4>
      <a name="cask">
        Automated Homebrew Cask Reinstaller
      </a>
    </h4>

.. code:: man

    usage: macdaily reinstall cask [options] <casks> ...

    Automated Homebrew Cask Reinstaller

    optional arguments:
    -h, --help            show this help message and exit
    -V, --version         show program's version number and exit

    specification arguments:
    -s PREFIX, --startswith PREFIX
                          reinstall procedure starts from such binary, sort in
                          initial alphabets
    -e SUFFIX, --endswith SUFFIX
                          reinstall procedure ends after such binary, sort in
                          initial alphabets
    -f, --force           reinstall even if the Cask does not appear to be
                          present
    -t, --no-quarantine   prevent Gatekeeper from enforcing its security
                          restrictions on the Cask
    -p CASK [CASK ...], --packages CASK [CASK ...]
                          name of Caskroom binaries to reinstall

    general arguments:
    -a, --all             reinstall all Caskroom binaries installed through
                          Homebrew
    -q, --quiet           run in quiet mode, with no output information
    -v, --verbose         run in verbose mode, with detailed output information
    -y, --yes             yes for all selections
    -n, --no-cleanup      do not run cleanup process

    miscellaneous arguments:
      -L ARG, --logging ARG
                          options for 'brew cask list' command
      -R ARG, --reinstall ARG
                          options for 'brew cask reinstall <cask>' command

    aliases: brew-cask, caskroom

When using ``--packages`` option, if given wrong package name, MacDaily
might give a trivial *did-you-mean* correction.

For *miscellaneous arguments*, the runtime commands are as below.

+----------------------+-------------------------------------------------+
|        Option        |                     Command                     |
+======================+=================================================+
| ``--logging=ARG``    | ``brew cask list ${ARG}``                       |
+----------------------+-------------------------------------------------+
| ``--reinstall=ARG``  | ``brew cask reinstall [options] ${ARG} <cask>`` |
+----------------------+-------------------------------------------------+

TODO
----

- ✔️ reconstruct reinstall CLI
- ❌ implement further spec for the mini-language

.. |brew| replace:: ``brew``
.. _brew: #brew
.. |cask| replace:: ``cask``
.. _cask: #cask

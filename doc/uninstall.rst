:Command Executable:
    ``macdaily uninstall`` | ``md-uninstall``
:Supported Commands:
    ``brew``, ``cask``, ``pip``

====================================
Automatate macOS Package Uninstaller
====================================

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

MacDaily provides intelligent solution for automate package uninstaller.
MacDaily ``uninstall`` command will recursively remove all specified
packages installed through --

- |brew|_ -- `Homebrew <https://brew.sh>`__
- |cask|_ -- `Homebrew Casks <https://caskroom.github.io>`__
- |pip|_ -- `Pip Installs Packages <https://pypy.org>`__

Usage
-----

.. code:: man

    usage: macdaily uninstall [options] <mode-selection> ...

    Automate macOS Package Uninstaller

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit

    general arguments:
      -a, --all             uninstall all packages installed through Homebrew,
                            Caskroom, and etc
      -k, --dry-run         list all packages which would be removed, but will not
                            actually delete any packages
      -i, --ignore-dependencies
                            run in non-recursive mode, i.e. ignore dependencies
                            packages
      -q, --quiet           run in quiet mode, with no output information
      -v, --verbose         run in verbose mode, with detailed output information
      -l, --show-log        open log in Console.app upon completion of command
      -y, --yes             yes for all selections
      -n, --no-cleanup      do not run cleanup process

    package arguments:
      options used to specify packages of each mode

      --pip PKG [PKG ...]   name of Python packages to uninstall
      --brew FORM [FORM ...]
                            name of Homebrew formulae to uninstall
      --cask CASK [CASK ...]
                            name of Caskroom binaries to uninstall

    control arguments:
      options used to disable uninstall of certain mode

      --no-pip              do not uninstall Python packages
      --no-brew             do not uninstall Homebrew formulae
      --no-cask             do not uninstall Caskroom binaries

    mode selection:
      uninstall existing packages installed through a specified method, e.g.:
      pip, brew, cask

    aliases: un, unlink, remove, rm, r

MacDaily ``uninstall`` supports using with multiple commands. Say, you would
like to uninstall Python packages and Homebrew formulae, each with different
flags and options, then simply use the following command.

.. code:: shell

    macdaily uninstall [global-options] pip [pip-options] brew [brew-options]

But please note that, global options ``--yes``, ``--quiet``, ``--verbose``
and ``--ignore-dependencies`` are *mandatory* for all commands once set to
``True``. That is to say, if you set these flags in global options, they will
overwrite corresponding flags in command specific options.

For all options that take package names, a mini-language for condition
specification is provided.

+--------------+-----------------------+
|    Format    |     Specification     |
+==============+=======================+
| ``package``  | uninstall ``package`` |
+--------------+-----------------------+
| ``!package`` | ignore ``package``    |
+--------------+-----------------------+

NB
    Since exclamation mark (``!``) has special meanings in
    `Shell <https://en.wikipedia.org/wiki/Shell_script>`__ scripts,
    it is highly recommended using ``'!package'`` literal to specify
    ignoring packages.

Commands
--------

.. raw:: html

    <h4>
      <a name="brew">
        Automate Homebrew Formula Uninstaller
      </a>
    </h4>

.. code:: man

    usage: macdaily uninstall brew [options] <formulae>

    Automate Homebrew Formula Uninstaller

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit

    specification arguments:
      -f, --force           delete all installed versions
      -b, --include-build   include the :build type dependencies
      -o, --include-optional
                            include :optional dependencies
      -t, --include-test    include (non-recursive) :test dependencies
      -s, --skip-recommended
                            skip :recommended type dependencies
      -r, --include-requirements
                            include requirements in addition to dependencies
      -p FORM [FORM ...], --packages FORM [FORM ...]
                            name of Homebrew formulae to uninstall

    general arguments:
      -a, --all             uninstall all Homebrew formulae installed through
                            Homebrew
      -k, --dry-run         list all Homebrew formulae which would be removed, but
                            will not actually delete any Homebrew formulae
      -i, --ignore-dependencies
                            run in non-recursive mode, i.e. ignore dependencies
                            packages
      -q, --quiet           run in quiet mode, with no output information
      -v, --verbose         run in verbose mode, with detailed output information
      -y, --yes             yes for all selections
      -n, --no-cleanup      do not run cleanup process

    miscellaneous arguments:
      -L ARG, --logging ARG
                            options for 'brew list' command
      -U ARG, --uninstall ARG
                            options for 'brew uninstall <formula>' command

When using ``--package`` option, if given wrong package name, MacDaily
might give a trivial *did-you-mean* correction.

For *miscellaneous arguments*, the runtime commands are as below.

+----------------------+---------------------------------------------------------------------+
|        Option        |                              Command                                |
+======================+=====================================================================+
| ``--logging=ARG``    | ``brew list ${ARG}``                                                |
+----------------------+---------------------------------------------------------------------+
| ``--uninstall=ARG``  | ``brew uninstall --ignore-dependencies [options] ${ARG} <formula>`` |
+----------------------+---------------------------------------------------------------------+

.. raw:: html

    <h4>
      <a name="cask">
        Automate Homebrew Cask Uninstaller
      </a>
    </h4>

.. code:: man

    usage: macdaily uninstall cask [options] <casks>

    Automate Homebrew Cask Uninstaller

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit

    specification arguments:
      -f, --force           uninstall even if the Cask does not appear to be
                            present
      -p CASK [CASK ...], --packages CASK [CASK ...]
                            name of Caskroom binaries to uninstall

    general arguments:
      -a, --all             uninstall all Caskroom binaries installed through
                            Homebrew
      -k, --dry-run         list all Caskroom binaries which would be removed, but
                            will not actually delete any Caskroom binaries
      -q, --quiet           run in quiet mode, with no output information
      -v, --verbose         run in verbose mode, with detailed output information
      -y, --yes             yes for all selections
      -n, --no-cleanup      do not run cleanup process

    miscellaneous arguments:
      -L ARG, --logging ARG
                            options for 'brew cask list' command
      -U ARG, --uninstall ARG
                            options for 'brew cask uninstall <cask>' command

When using ``--package`` option, if given wrong package name, MacDaily
might give a trivial *did-you-mean* correction.

For *miscellaneous arguments*, the runtime commands are as below.

+----------------------+-------------------------------------------------+
|        Option        |                     Command                     |
+======================+=================================================+
| ``--logging=ARG``    | ``brew cask list ${ARG}``                       |
+----------------------+-------------------------------------------------+
| ``--uninstall=ARG``  | ``brew cask uninstall [options] ${ARG} <cask>`` |
+----------------------+-------------------------------------------------+

.. raw:: html

    <h4>
      <a name="pip">
        Automate Python Package Uninstaller
      </a>
    </h4>

.. code:: man

    usage: macdaily uninstall pip [options] <packages>

    Automate Python Package Uninstaller

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit

    specification arguments:
      -b, --brew            uninstall packages of Python installed from Homebrew
      -c, --cpython         uninstall packages of CPython implementation
      -d, --pre             include pre-release and development versions
      -e VER [VER ...], --python VER [VER ...]
                            indicate packages from which version of Python will be
                            uninstalled
      -r, --pypy            uninstall packages of PyPy implementation
      -s, --system          uninstall packages of Python provided by macOS system
      -p PKG [PKG ...], --packages PKG [PKG ...]
                            name of Python packages to uninstall

    general arguments:
      -a, --all             uninstall all Python packages installed through Python
                            Package Index
      -k, --dry-run         list all Python packages which would be removed, but
                            will not actually delete any Python packages
      -i, --ignore-dependencies
                            run in non-recursive mode, i.e. ignore dependencies
                            packages
      -q, --quiet           run in quiet mode, with no output information
      -v, --verbose         run in verbose mode, with detailed output information
      -y, --yes             yes for all selections
      -n, --no-cleanup      do not run cleanup process

    miscellaneous arguments:
      -L ARG, --logging ARG
                            options for 'pip freeze' command
      -U ARG, --uninstall ARG
                            options for 'pip uninstall <package>' command

When using ``--package`` option, if given wrong package name, MacDaily
might give a trivial *did-you-mean* correction.

NB
    For stability of Python, MacDaily ``uninstall`` command will **NOT**
    remove any of the following packages: ``pip``, ``setuptools``,
    ``wheel`` and distribute.

For *miscellaneous arguments*, the runtime commands are as below.

+-------------------+----------------------------------------------------+
|      Option       |                        Command                     |
+===================+====================================================+
| ``--logging=ARG`` | ``pip freeze --outdated [options] ${ARG}``         |
+-------------------+----------------------------------------------------+
| ``--update=ARG``  | ``pip uninstall --yes [options] ${ARG} <package>`` |
+-------------------+----------------------------------------------------+

Possible Python executables and corresponding flags are listed as below.

.. image:: https://github.com/JarryShaw/MacDaily/blob/dev/doc/img/Python.png

NB
    Python provided by macOS system (normally located at ``/usr/bin/python`` or
    ``/System/Library/Frameworks/Python.framework/Versions/Current/bin/python``)
    does not have ``pip`` installed. And it is
    `not recommended <https://docs.python.org/3/using/mac.html>`__ to do so.

TODO
----

- ✔️ reconstruct uninstall CLI
- ❌ implement further spec for the mini-language

.. |brew| replace:: ``brew``
.. _brew: #brew
.. |cask| replace:: ``cask``
.. _cask: #cask
.. |pip| replace:: ``pip``
.. _pip: #pip

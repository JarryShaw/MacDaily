:Command Executable:
    ``macdaily logging`` | ``md-logging``
:Supported Commands:
    ``apm``, ``app``, ``brew``, ``cask``,
    ``gem``, ``mas``, ``npm``, ``pip``, ``tap``

===============================
macOS Package Logging Automator
===============================

- `About <#about>`__
- `Usage <#usage>`__
- `Commands <#commands>`__

  - `Atom Plug-Ins <#apm>`__
  - `Mac Applications <#app>`__
  - `Homebrew Formulae <#brew>`__
  - `Caskroom Binaries <#cask>`__
  - `Ruby Gems <#gem>`__
  - `macOS Applications <#mas>`__
  - `Node.js Modules <#npm>`__
  - `Python Package <#pip>`__
  - `Third-party Repositories <#tap>`__

- `TODO <#todo>`__

--------------

About
-----

MacDaily provides intelligent solution for package logging automation.
MacDaily ``logging`` command will automatically record all existing packages
installed through --

- |apm|_ -- `Atom Package Manager <https://atom.io/packages>`__
- |app|_ -- macOS Applications
- |brew|_ -- `Homebrew <https://brew.sh>`__
- |cask|_ -- `Homebrew Casks <https://caskroom.github.io>`__
- |gem|_ -- `RubyGems <https://rubygems.org>`__
- |mas|_ -- `Mac App Store CLI <https://github.com/mas-cli/mas#mas-cli>`__
- |npm|_ -- `Node.js Package Manager <https://nodejs.org>`__
- |pip|_ -- `Pip Installs Packages <https://pypy.org>`__
- |tap|_ -- `Homebrew Taps <https://docs.brew.sh/Taps>`__

Usage
-----

.. code:: man

    usage: macdaily logging [options] <mode-selection> ...

    macOS Package Logging Automator

    optional arguments:
      -h, --help        show this help message and exit
      -V, --version     show program's version number and exit

    general arguments:
      -a, --all         log all packages installed through Atom, RubyGems,
                        Node.js, Homebrew, Caskroom, Mac App Store, and etc
      -q, --quiet       run in quiet mode, with no output information
      -v, --verbose     run in verbose mode, with detailed output information
      -n, --no-cleanup  do not run cleanup process
      -l, --show-log    open log in Console.app upon completion of command

    control arguments:
      options used to disable logging of certain mode

      --no-apm          do not log Atom plug-ins
      --no-app          do not log system applications
      --no-gem          do not log Ruby gems
      --no-mas          do not log macOS applications
      --no-npm          do not log Node.js modules
      --no-pip          do not log Python packages
      --no-tap          do not log Homebrew Taps
      --no-brew         do not log Homebrew formulae
      --no-cask         do not log Homebrew Casks

    mode selection:
      log existing packages installed through a specified method, e.g.: apm,
      app, gem, mas, npm, pip, tap, brew, cask

    aliases: log

MacDaily ``logging`` supports using with multiple commands. Say, you would like
to record Python packages and Homebrew formulae, each with different flags and
options, then simply use the following command.

.. code:: shell

    macdaily logging [global-options] pip [pip-options] brew [brew-options]

But please note that, global options ``--yes``, ``--quiet`` and ``--show-log``
are *mandatory* for all commands once set to ``True``. That is to say, if you
set these flags in global options, they will overwrite corresponding flags in
command specific options.

NB
    MacDaily will record installed packages using following package
    manager requirement specification formats.

+----------+----------------------+
| Command  |       Log File       |
+==========+======================+
| ``apm``  | ``packages.txt``     |
+----------+----------------------+
| ``app``  | ``macOS.log``        |
+----------+----------------------+
| ``brew`` | ``Brewfile``         |
+----------+----------------------+
| ``cask`` | ``Brewfile``         |
+----------+----------------------+
| ``gem``  | ``lockdown.rb``      |
+----------+----------------------+
| ``mas``  | ``Brewfile``         |
+----------+----------------------+
| ``npm``  | ``package.json``     |
+----------+----------------------+
| ``pip``  | ``requirements.txt`` |
+----------+----------------------+
| ``tap``  | ``Brewfile``         |
+----------+----------------------+

Commands
--------

.. raw:: html

    <h4>
      <a name="apm">
        Atom Plug-In Logging Automator
      </a>
    </h4>

.. code:: man

    usage: macdaily logging apm [options] ...

    Atom Plug-In Logging Automator

    optional arguments:
      -h, --help        show this help message and exit
      -V, --version     show program's version number and exit

    specification arguments:
      -b, --beta        log Atom Beta plug-ins

    general arguments:
      -q, --quiet       run in quiet mode, with no output information
      -v, --verbose     run in verbose mode, with detailed output information
      -n, --no-cleanup  do not run cleanup process
      -l, --show-log    open log in Console.app upon completion of command

    aliases: atom

MacDaily ``logging-apm`` command uses ``apm list --installed --bare``
to record installed Atom plug-ins. The corresponding log file will be
named as ``packages.txt``.

NB
    Package Manager (``apm``) of `Atom Beta <https://atom.io/beta>`__
    is normally present as ``apm-beta``.

.. raw:: html

    <h4>
      <a name="app">
        Mac Application Logging Automator
      </a>
    </h4>

.. code:: man

    usage: macdaily logging app [options] ...

    Mac Application Logging Automator

    optional arguments:
      -h, --help        show this help message and exit
      -V, --version     show program's version number and exit

    general arguments:
      -q, --quiet       run in quiet mode, with no output information
      -v, --verbose     run in verbose mode, with detailed output information
      -n, --no-cleanup  do not run cleanup process
      -l, --show-log    open log in Console.app upon completion of command

    aliases: application, macos

MacDaily ``logging-app`` command uses ``sudo python macdaily/res/find.py /`` to
record installed Mac applications. The corresponding log file will be named as
``macOS.log``.

.. raw:: html

    <h4>
      <a name="brew">
        Homebrew Formula Logging Automator
      </a>
    </h4>

.. code:: man

    usage: macdaily logging brew [options] ...

    Homebrew Formula Logging Automator

    optional arguments:
      -h, --help        show this help message and exit
      -V, --version     show program's version number and exit

    general arguments:
      -q, --quiet       run in quiet mode, with no output information
      -v, --verbose     run in verbose mode, with detailed output information
      -n, --no-cleanup  do not run cleanup process
      -l, --show-log    open log in Console.app upon completion of command

    aliases: homebrew

MacDaily ``logging-brew`` command uses ``brew bundle dump`` to record
installed Homebrew formulae. The corresponding log file will be named
as ``Brewfile``.

.. raw:: html

    <h4>
      <a name="cask">
        Homebrew Cask Logging Automator
      </a>
    </h4>

.. code:: man

    usage: macdaily logging cask [options] ...

    Homebrew Cask Logging Automator

    optional arguments:
      -h, --help        show this help message and exit
      -V, --version     show program's version number and exit

    general arguments:
      -q, --quiet       run in quiet mode, with no output information
      -v, --verbose     run in verbose mode, with detailed output information
      -n, --no-cleanup  do not run cleanup process
      -l, --show-log    open log in Console.app upon completion of command

    aliases: brew-cask, caskroom

MacDaily ``logging-cask`` command uses ``brew bundle dump`` to record
installed Homebrew Casks. The corresponding log file will be named
as ``Brewfile``.

.. raw:: html

    <h4>
      <a name="gem">
        Ruby Gem Logging Automator
      </a>
    </h4>

.. code:: man

    usage: macdaily logging gem [options] ...

    Ruby Gem Logging Automator

    optional arguments:
      -h, --help        show this help message and exit
      -V, --version     show program's version number and exit

    specification arguments:
      -b, --brew        log gems of Ruby installed from Homebrew
      -s, --system      log gems of Ruby provided by macOS system

    general arguments:
      -q, --quiet       run in quiet mode, with no output information
      -v, --verbose     run in verbose mode, with detailed output information
      -n, --no-cleanup  do not run cleanup process
      -l, --show-log    open log in Console.app upon completion of command

    aliases: ruby, rubygems

MacDaily ``logging-gem`` command uses ``gem lock <gem-version>`` to record
installed Ruby gems. The corresponding log file will be named as ``lockdown.rb``.

.. raw:: html

    <h4>
      <a name="mas">
        macOS Application Logging Automator
      </a>
    </h4>

.. code:: man

    usage: macdaily logging mas [options] ...

    macOS Application Logging Automator

    optional arguments:
      -h, --help        show this help message and exit
      -V, --version     show program's version number and exit

    general arguments:
      -q, --quiet       run in quiet mode, with no output information
      -v, --verbose     run in verbose mode, with detailed output information
      -n, --no-cleanup  do not run cleanup process
      -l, --show-log    open log in Console.app upon completion of command

    aliases: app-store, appstore, mac, mac-app-store

MacDaily ``logging-mas`` command uses ``brew bundle dump`` to record
installed macOS applications. The corresponding log file will be named
as ``Brewfile``.

.. raw:: html

    <h4>
      <a name="npm">
        Node.js Module Logging Automator
      </a>
    </h4>

.. code:: man

    usage: macdaily logging npm [options] ...

    Node.js Module Logging Automator

    optional arguments:
      -h, --help        show this help message and exit
      -V, --version     show program's version number and exit

    specification arguments:
      -i, --long        show extended information

    general arguments:
      -q, --quiet       run in quiet mode, with no output information
      -v, --verbose     run in verbose mode, with detailed output information
      -n, --no-cleanup  do not run cleanup process
      -l, --show-log    open log in Console.app upon completion of command

    aliases: node, node.js

MacDaily ``logging-npm`` command uses ``npm list --json --global`` to
record installed Node.js modules. The corresponding log file will be named
as ``package.json``.

.. raw:: html

    <h4>
      <a name="pip">
        Python Package Logging Automator
      </a>
    </h4>

.. code:: man

    usage: macdaily logging pip [options] ...

    Python Package Logging Automator

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit

    specification arguments:
      -x, --exclude-editable
                            exclude editable package from output
      -b, --brew            log packages of Python installed from Homebrew
      -c, --cpython         log packages of CPython implementation
      -e VER [VER ...], --python VER [VER ...]
                            indicate packages from which version of Python will be
                            logged
      -r, --pypy            log packages of PyPy implementation
      -s, --system          log packages of Python provided by macOS system

    general arguments:
      -q, --quiet           run in quiet mode, with no output information
      -v, --verbose         run in verbose mode, with detailed output information
      -n, --no-cleanup      do not run cleanup process
      -l, --show-log        open log in Console.app upon completion of command

    aliases: cpython, pypy, python

MacDaily ``logging-pip`` command uses ``python -m pip freeze`` to record
installed Python packages. The corresponding log file will be named as
``requirements.txt``.

Possible Python executables and corresponding flags are listed as below.

.. image:: https://github.com/JarryShaw/MacDaily/tree/master/doc/img/Python.png

NB
    Python provided by macOS system (normally located at ``/usr/bin/python`` or
    ``/System/Library/Frameworks/Python.framework/Versions/Current/bin/python``)
    does not have ``pip`` installed. And it is
    `not recommended <https://docs.python.org/3/using/mac.html>`__ to do so.

.. raw:: html

    <h4>
      <a name="tap">
        Homebrew Tap Logging Automator
      </a>
    </h4>

.. code:: man

    usage: macdaily logging tap [options] ...

    Homebrew Tap Logging Automator

    optional arguments:
      -h, --help        show this help message and exit
      -V, --version     show program's version number and exit

    general arguments:
      -q, --quiet       run in quiet mode, with no output information
      -v, --verbose     run in verbose mode, with detailed output information
      -n, --no-cleanup  do not run cleanup process
      -l, --show-log    open log in Console.app upon completion of command

    aliases: brew-tap

MacDaily ``logging-tap`` command uses ``brew bundle dump`` to record
installed Homebrew Taps. The corresponding log file will be named
as ``Brewfile``.

TODO
----

- ✔️ reconstruct logging CLI
- ❌ considering implement support for custom logging options

.. |apm| replace:: ``apm``
.. _apm: #apm
.. |app| replace:: ``app``
.. _app: #app
.. |brew| replace:: ``brew``
.. _brew: #brew
.. |cask| replace:: ``cask``
.. _cask: #cask
.. |gem| replace:: ``gem``
.. _gem: #gem
.. |mas| replace:: ``mas``
.. _mas: #mas
.. |npm| replace:: ``npm``
.. _npm: #npm
.. |pip| replace:: ``pip``
.. _pip: #pip
.. |tap| replace:: ``tap``
.. _tap: #tap

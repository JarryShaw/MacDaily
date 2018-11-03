:Command Exectuable:
    ``macdaily update`` | ``md-update``
:Supported Commands:
    ``apm``, ``brew``, ``cask``, ``gem``,
    ``mas``, ``npm``,``pip``, ``system``

==============================
macOS Package Update Automator
==============================

- `About <#about>`__
- `Usage <#usage>`__
- `Commands <#commands>`__

  - `Atom Plug-Ins <#apm>`__
  - `Homebrew Formulae <#brew>`__
  - `Caskroom Binaries <#cask>`__
  - `Ruby Gems <#gem>`__
  - `macOS Applications <#mas>`__
  - `Node.js Modules <#npm>`__
  - `Python Package <#pip>`__
  - `System Software <#system>`__

- `TODO <#todo>`__

--------------

About
-----

MacDaily provides intelligent sollution for package update automation.
MacDaily ``update`` command will automatically update all outdated packages
installed through --

- |apm|_ -- `Atom Package Manager <https://atom.io/packages>`__
- |brew|_ -- `Homebrew <https://brew.sh>`__
- |cask|_ -- `Homebrew Casks <https://caskroom.github.io>`__
- |gem|_ -- `RubyGems <https://rubygems.org>`__
- |mas|_ -- `Mac App Store CLI <https://github.com/mas-cli/mas#mas-cli>`__
- |npm|_ -- `Node.js Package Manager <https://nodejs.org>`__
- |pip|_ -- `Pip Installs Packages <https://pypy.org>`__
- |system|_ -- macOS Software Update

Usage
-----

.. code:: shell

    usage: macdaily update [options] <mode-selection> ...

    macOS Package Update Automator

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit

    general arguments:
      -a, --all             update all packages installed through Atom, RubyGem,
                            Node.js, Homebrew, Caskroom, Mac App Store, and etc
      -q, --quiet           run in quiet mode, with no output information
      -v, --verbose         run in verbose mode, with detailed output information
      -l, --show-log        open log in Console.app upon completion of command
      -y, --yes             yes for all selections
      -n, --no-cleanup      do not run cleanup process

    package arguments:
      options used to specify packages of each mode

      --apm PI [PI ...]     name of Atom plug-ins to update
      --gem GEM [GEM ...]   name of Ruby gems to update
      --mas APP [APP ...]   name of macOS applications to update
      --npm MOD [MOD ...]   name of Node.js modules to update
      --pip PKG [PKG ...]   name of Python packages to update
      --brew FORM [FORM ...]
                            name of Homebrew formulae to update
      --cask CASK [CASK ...]
                            name of Caskroom binaries to update
      --system SW [SW ...]  name of system software to update

    control arguments:
      options used to disable update of certain mode

      --no-apm              do not update Atom plug-ins
      --no-gem              do not update Ruby gems
      --no-mas              do not update macOS applications
      --no-npm              do not update Node.js modules
      --no-pip              do not update Python packages
      --no-brew             do not update Homebrew formulae
      --no-cask             do not update Caskroom binaries
      --no-system           do not update system software

    mode selection:
      update outdated packages installed through a specified method, e.g.: apm,
      gem, mas, npm, pip, brew, cask, system

    aliases: up, upgrade

MacDaily ``update`` supports using with multiple commands. Say, you would like
to update Python packages and Homebrew formulae, each with different flags and
options, then simply use the following command.

.. code:: shell

    macdaily update [global-options] pip [pip-options] brew [brew-options]

But please note that, global options ``--yes``, ``--quiet``, ``--verbose``
and ``--no-cleanup`` are *mandatory* for all commands once set to ``True``.
That is to say, if you set these flags in global options, they will overwrite
corresponding flags in command specific options.

Commands
--------

|h-apm|
-------

.. |h-apm| raw:: html

    <a name="apm">Atom Plug-Ins</a>

TODO
----

.. |apm| replace:: ``apm``
.. _apm: #apm
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
.. |system| replace:: ``system``
.. _system: #system

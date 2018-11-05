:Command Executable:
    ``macdaily update`` | ``md-update``
:Supported Commands:
    ``apm``, ``brew``, ``cask``, ``gem``,
    ``mas``, ``npm``, ``pip``, ``system``

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

MacDaily provides intelligent solution for package update automation.
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

.. code:: man

    usage: macdaily update [options] <mode-selection> ...

    macOS Package Update Automator

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit

    general arguments:
      -a, --all             update all packages installed through Atom, RubyGems,
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

For all options that take package names, a mini-language for condition
specification is provided.

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

Commands
--------

.. raw:: html

    <h4>
      <a name="apm">
        Atom Plug-In Update Automator
      </a>
    </h4>

.. code:: man

    usage: macdaily update apm [options] <plug-ins>

    Atom Plug-In Update Automator

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit

    specification arguments:
      -b, --beta            update Atom Beta plug-ins
      -p PI [PI ...], --packages PI [PI ...]
                            name of Atom plug-ins to update

    general arguments:
      -a, --all             update all plug-ins installed through Atom Package
                            Manager
      -q, --quiet           run in quiet mode, with no output information
      -v, --verbose         run in verbose mode, with detailed output information
      -y, --yes             yes for all selections

    miscellaneous arguments:
      -L ARG, --logging ARG
                            options for 'apm upgrade --list' command
      -U ARG, --update ARG  options for 'apm upgrade <plug-in>' command

When using ``--package`` option, if given wrong package name, MacDaily
might give a trivial *did-you-mean* correction.

For *miscellaneous arguments*, the runtime commands are as below.

+-------------------+----------------------------------------------------------------+
|      Option       |                            Command                             |
+===================+================================================================+
| ``--logging=ARG`` | ``apm upgrade ${ARG} --no-color --no-json --list``             |
+-------------------+----------------------------------------------------------------+
| ``--update=ARG``  | ``apm upgrade ${ARG} [options] --no-json --no-list <plug-in>`` |
+-------------------+----------------------------------------------------------------+

NB
    Package Manager (``apm``) of `Atom Beta <https://atom.io/beta>`__
    is normally present as ``apm-beta``.

.. raw:: html

    <h4>
      <a name="brew">
        Homebrew Formula Update Automator
      </a>
    </h4>

.. code:: man

    usage: macdaily update brew [options] <formulae>

    Homebrew Formula Update Automator

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit

    specification arguments:
      -f, --force           always do a slower, full update check even if
                            unnecessary
      -m, --merge           'git merge' is used to include updates (rather
                            than 'git rebase')
      -p FORM [FORM ...], --packages FORM [FORM ...]
                            name of Homebrew formulae to update

    general arguments:
      -a, --all             update all Homebrew formulae installed through
                            Homebrew
      -q, --quiet           run in quiet mode, with no output information
      -v, --verbose         run in verbose mode, with detailed output information
      -y, --yes             yes for all selections
      -n, --no-cleanup      do not run cleanup process

    miscellaneous arguments:
      -L ARG, --logging ARG
                            options for 'brew outdated' command
      -U ARG, --update ARG  options for 'brew upgrade <formula>' command

When using ``--package`` option, if given wrong package name, MacDaily
might give a trivial *did-you-mean* correction.

For *miscellaneous arguments*, the runtime commands are as below.

+-------------------+----------------------------------------------+
|      Option       |                   Command                    |
+===================+==============================================+
| ``--logging=ARG`` | ``brew outdated [options] ${ARG}``           |
+-------------------+----------------------------------------------+
| ``--update=ARG``  | ``brew upgrade [options] ${ARG} <formula>``  |
+-------------------+----------------------------------------------+

.. raw:: html

    <h4>
      <a name="cask">
        Homebrew Cask Update Automator
      </a>
    </h4>

.. code:: man

    usage: macdaily update cask [options] <casks>

    Homebrew Cask Update Automator

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit

    specification arguments:
      -f, --force           use '--force' when running 'brew cask
                            upgrade <cask>' command
      -g, --greedy          use '--greedy' when running 'brew cask
                            upgrade <cask>' command
      -m, --merge           'git merge' is used to include updates (rather
                            than 'git rebase')
      -x, --exhaust         exhaustively check Caskroom for outdated Homebrew
                            Casks
      -p CASK [CASK ...], --packages CASK [CASK ...]
                            name of Caskroom binaries to update

    general arguments:
      -a, --all             update all Caskroom binaries installed through
                            Homebrew
      -q, --quiet           run in quiet mode, with no output information
      -v, --verbose         run in verbose mode, with detailed output information
      -y, --yes             yes for all selections
      -n, --no-cleanup      do not run cleanup process

    miscellaneous arguments:
      -L ARG, --logging ARG
                            options for 'brew cask outdated' command
      -U ARG, --update ARG  options for 'brew cask upgrade <cask>' command

When using ``--package`` option, if given wrong package name, MacDaily
might give a trivial *did-you-mean* correction.

For *miscellaneous arguments*, the runtime commands are as below.

+-------------------+------------------------------------------------+
|      Option       |                    Command                     |
+===================+================================================+
| ``--logging=ARG`` | ``brew cask outdated [options] ${ARG}``        |
+-------------------+------------------------------------------------+
| ``--update=ARG``  | ``brew cask upgrade [options] ${ARG} <cask>``  |
+-------------------+------------------------------------------------+

.. raw:: html

    <h4>
      <a name="gem">
        Ruby Gem Update Automator
      </a>
    </h4>

.. code:: man

    usage: macdaily update gem [options] <gems>

    Ruby Gem Update Automator

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit

    specification arguments:
      -b, --brew            update gems of Ruby installed from Homebrew
      -s, --system          update gems of Ruby provided by macOS system
      -p GEM [GEM ...], --packages GEM [GEM ...]
                            name of Ruby gems to update

    general arguments:
      -a, --all             update all gems installed through RubyGems
      -q, --quiet           run in quiet mode, with no output information
      -v, --verbose         run in verbose mode, with detailed output information
      -y, --yes             yes for all selections

    miscellaneous arguments:
      -L ARG, --logging ARG
                            options for 'gem outdated' command
      -U ARG, --update ARG  options for 'gem update <gem>' command

When using ``--package`` option, if given wrong package name, MacDaily
might give a trivial *did-you-mean* correction.

For *miscellaneous arguments*, the runtime commands are as below.

+-------------------+---------------------------------------+
|      Option       |                Command                |
+===================+=======================================+
| ``--logging=ARG`` | ``gem outdated [options] ${ARG}``     |
+-------------------+---------------------------------------+
| ``--update=ARG``  | ``gem update [options] ${ARG} <gem>`` |
+-------------------+---------------------------------------+

NB
    RubyGems provided by macOS system is normally located at ``/usr/bin/gem``
    or ``/System/Library/Frameworks/Ruby.framework/Versions/Current/usr/bin/gem``.

.. raw:: html

    <h4>
      <a name="mas">
        macOS Application Update Automator
      </a>
    </h4>

.. code:: man

    usage: macdaily update mas [options] <applications>

    macOS Application Update Automator

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit

    specification arguments:
      -p APP [APP ...], --packages APP [APP ...]
                            name of macOS applications to update

    general arguments:
      -a, --all             update all macOS applications installed through Mac
                            App Store
      -q, --quiet           run in quiet mode, with no output information
      -v, --verbose         run in verbose mode, with detailed output information
      -y, --yes             yes for all selections

    miscellaneous arguments:
      -L ARG, --logging ARG
                            options for 'mas outdated' command
      -U ARG, --update ARG  options for 'mas upgrade <application>'
                            command

When using ``--package`` option, if given wrong package name, MacDaily
might give a trivial *did-you-mean* correction.

For *miscellaneous arguments*, the runtime commands are as below.

+-------------------+--------------------------------------+
|      Option       |               Command                |
+===================+======================================+
| ``--logging=ARG`` | ``mas outdated ${ARG}``              |
+-------------------+--------------------------------------+
| ``--update=ARG``  | ``mas upgrade ${ARG} <application>`` |
+-------------------+--------------------------------------+

.. raw:: html

    <h4>
      <a name="npm">
        Node.js Module Update Automator
      </a>
    </h4>

.. code:: man

    usage: macdaily update npm [options] <modules>

    Node.js Module Update Automator

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit

    specification arguments:
      -p MOD [MOD ...], --packages MOD [MOD ...]
                            name of Node.js modules to update

    general arguments:
      -a, --all             update all Node.js modules installed through Node.js
                            Package Manager
      -q, --quiet           run in quiet mode, with no output information
      -v, --verbose         run in verbose mode, with detailed output information
      -y, --yes             yes for all selections
      -n, --no-cleanup      do not run cleanup process

    miscellaneous arguments:
      -L ARG, --logging ARG
                            options for 'npm outdated --global' command
      -U ARG, --update ARG  options for 'npm upgrade --global <module>'
                            command

When using ``--package`` option, if given wrong package name, MacDaily
might give a trivial *did-you-mean* correction.

For *miscellaneous arguments*, the runtime commands are as below.

+-------------------+-----------------------------------------------------------+
|      Option       |                           Command                         |
+===================+===========================================================+
| ``--logging=ARG`` | ``npm outdated ${ARG} --no-parseable --no-json --global`` |
+-------------------+-----------------------------------------------------------+
| ``--update=ARG``  | ``npm upgrade [options] ${ARG} --global <module>``        |
+-------------------+-----------------------------------------------------------+

.. raw:: html

    <h4>
      <a name="pip">
        Python Package Update Automator
      </a>
    </h4>

.. code:: man

    usage: macdaily update pip [options] <packages>

    Python Package Update Automator

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit

    specification arguments:
      -b, --brew            update packages of Python installed from Homebrew
      -c, --cpython         update packages of CPython implementation
      -d, --pre             include pre-release and development versions
      -e VER [VER ...], --python VER [VER ...]
                            indicate packages from which version of Python will
                            update
      -r, --pypy            update packages of PyPy implementation
      -s, --system          update packages of Python provided by macOS system
      -p PKG [PKG ...], --packages PKG [PKG ...]
                            name of Python packages to update

    general arguments:
      -a, --all             update all Python packages installed through Python
                            Package Index
      -q, --quiet           run in quiet mode, with no output information
      -v, --verbose         run in verbose mode, with detailed output information
      -y, --yes             yes for all selections
      -n, --no-cleanup      do not run cleanup process

    miscellaneous arguments:
      -L ARG, --logging ARG
                            options for 'pip list --outdated' command
      -U ARG, --update ARG  options for 'pip install --upgrade <package>'
                            command

When using ``--package`` option, if given wrong package name, MacDaily
might give a trivial *did-you-mean* correction.

For *miscellaneous arguments*, the runtime commands are as below.

+-------------------+------------------------------------------------------+
|      Option       |                         Command                      |
+===================+======================================================+
| ``--logging=ARG`` | ``pip list --outdated [options] ${ARG}``             |
+-------------------+------------------------------------------------------+
| ``--update=ARG``  | ``pip install --upgrade [options] ${ARG} <package>`` |
+-------------------+------------------------------------------------------+

Possible Python executables and corresponding flags are listed as below.

.. image:: https://github.com/JarryShaw/MacDaily/blob/dev/res/img/Python.png

NB
    Python provided by macOS system (normally located at ``/usr/bin/python`` or
    ``/System/Library/Frameworks/Python.framework/Versions/Current/bin/python``)
    does not have ``pip`` installed. And it is
    `not recommended <https://docs.python.org/3/using/mac.html>`__ to do so.

.. raw:: html

    <h4>
      <a name="system">
        System Software Update Automator
      </a>
    </h4>

.. code:: man

    usage: macdaily update system [options] <software>

    System Software Update Automator

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit

    specification arguments:
      -R, --restart         automatically restart (or shut down) if required to
                            complete installation
      -r, --recommended     only update software that is recommended for your
                            system
      -p SW [SW ...], --packages SW [SW ...]
                            name of system software to update

    general arguments:
      -a, --all             update all system software installed through
                            'softwareupdate'
      -q, --quiet           run in quiet mode, with no output information
      -v, --verbose         run in verbose mode, with detailed output information
      -y, --yes             yes for all selections

    miscellaneous arguments:
      -L ARG, --logging ARG
                            options for 'softwareupdate --list' command
      -U ARG, --update ARG  options for 'softwareupdate --install
                            <software>' command

When using ``--package`` option, if given wrong package name, MacDaily
might give a trivial *did-you-mean* correction.

For *miscellaneous arguments*, the runtime commands are as below.

+-------------------+--------------------------------------------------------------------+
|      Option       |                              Command                               |
+===================+====================================================================+
| ``--logging=ARG`` | ``softwareupdate --list ${ARG}``                                   |
+-------------------+--------------------------------------------------------------------+
| ``--update=ARG``  | ``softwareupdate --install --no-scan [options] ${ARG} <software>`` |
+-------------------+--------------------------------------------------------------------+

TODO
----

- ✔️ reconstruct update CLI
- ❌ implement further spec for the mini-language

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

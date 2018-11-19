:Command Executable:
    ``macdaily install`` | ``md-install``
:Supported Commands:
    ``apm``, ``brew``, ``cask``, ``gem``,
    ``mas``, ``npm``, ``pip``, ``system``

================================
macOS Package Automate Installer
================================

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

MacDaily provides intelligent solution for package automate installation.
MacDaily ``install`` command will automatically install all specified packages
through --

- |apm|_ -- `Atom Package Manager <https://atom.io/packages>`__
- |brew|_ -- `Homebrew <https://brew.sh>`__
- |cask|_ -- `Homebrew Casks <https://caskroom.github.io>`__
- |gem|_ -- `RubyGems <https://rubygems.org>`__
- |mas|_ -- `Mac App Store CLI <https://github.com/mas-cli/mas#mas-cli>`__
- |npm|_ -- `Node.js Package Manager <https://nodejs.org>`__
- |pip|_ -- `Pip Installs Packages <https://pypy.org>`__
- |system|_ -- macOS Software Update (c.f. ``softwareupdate(8)``)

Usage
-----

.. code:: man

    usage: macdaily install [options] <mode-selection> ...

    macOS Package Automate Installer

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit

    general arguments:
      -q, --quiet           run in quiet mode, with no output information
      -v, --verbose         run in verbose mode, with detailed output information
      -l, --show-log        open log in Console.app upon completion of command
      -y, --yes             yes for all selections
      -n, --no-cleanup      do not run cleanup process

    package arguments:
      options used to specify packages of each mode

      --apm PI [PI ...]     name of Atom plug-ins to install
      --gem GEM [GEM ...]   name of Ruby gems to install
      --mas APP [APP ...]   name of macOS applications to install
      --npm MOD [MOD ...]   name of Node.js modules to install
      --pip PKG [PKG ...]   name of Python packages to install
      --brew FORM [FORM ...]
                            name of Homebrew formulae to install
      --cask CASK [CASK ...]
                            name of Caskroom binaries to install
      --system SW [SW ...]  name of system software to install

    mode selection:
      install packages through a specified method, e.g.: apm, gem, mas, npm,
      pip, brew, cask, system

    aliases: i

MacDaily ``install`` supports using with multiple commands. Say, you would like
to install Python packages and Homebrew formulae, each with different flags and
options, then simply use the following command.

.. code:: shell

    macdaily install [global-options] pip [pip-options] brew [brew-options]

But please note that, global options ``--yes``, ``--quiet``, ``--verbose``
and ``--no-cleanup`` are *mandatory* for all commands once set to ``True``.
That is to say, if you set these flags in global options, they will overwrite
corresponding flags in command specific options.

For all options that take package names, a mini-language for condition
specification is provided.

+--------------+---------------------+
|    Format    |    Specification    |
+==============+=====================+
| ``package``  | install ``package`` |
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
        Atom Plug-In Automate Installer
      </a>
    </h4>

.. code:: man

    usage: macdaily install apm [options] <plug-ins>

    Atom Plug-In Automate Installer

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit

    specification arguments:
      -b, --beta            install Atom Beta plug-ins
      -p PI [PI ...], --packages PI [PI ...]
                            name of Atom plug-ins to install

    general arguments:
      -q, --quiet           run in quiet mode, with no output information
      -v, --verbose         run in verbose mode, with detailed output information
      -y, --yes             yes for all selections

    miscellaneous arguments:
      -I ARG, --install ARG
                            options for 'apm install <plug-in>' command

For *miscellaneous arguments*, the runtime commands are as below.

+-------------------+--------------------------------------------+
|      Option       |                  Command                   |
+===================+============================================+
| ``--install=ARG`` | ``apm install [options] ${ARG} <plug-in>`` |
+-------------------+--------------------------------------------+

NB
    Package Manager (``apm``) of `Atom Beta <https://atom.io/beta>`__
    is normally present as ``apm-beta``.

.. raw:: html

    <h4>
      <a name="brew">
        Homebrew Formula Automate Installer
      </a>
    </h4>

.. code:: man

    usage: macdaily install brew [options] <formulae>

    Homebrew Formula Automate Installer

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit

    specification arguments:
      -p FORM [FORM ...], --packages FORM [FORM ...]
                            name of Homebrew formulae to install

    general arguments:
      -q, --quiet           run in quiet mode, with no output information
      -v, --verbose         run in verbose mode, with detailed output information
      -y, --yes             yes for all selections
      -n, --no-cleanup      do not run cleanup process

    miscellaneous arguments:
      -I ARG, --install ARG
                            options for 'brew install <formula>' command

For *miscellaneous arguments*, the runtime commands are as below.

+-------------------+----------------------------------------------+
|      Option       |                   Command                    |
+===================+==============================================+
| ``--install=ARG`` | ``brew install [options] ${ARG} <formula>``  |
+-------------------+----------------------------------------------+

.. raw:: html

    <h4>
      <a name="cask">
        Homebrew Cask Automate Installer
      </a>
    </h4>

.. code:: man

    usage: macdaily install cask [options] <casks>

    Homebrew Cask Automate Installer

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit

    specification arguments:
      -p CASK [CASK ...], --packages CASK [CASK ...]
                            name of Caskroom binaries to install

    general arguments:
      -q, --quiet           run in quiet mode, with no output information
      -v, --verbose         run in verbose mode, with detailed output information
      -y, --yes             yes for all selections
      -n, --no-cleanup      do not run cleanup process

    miscellaneous arguments:
      -I ARG, --install ARG
                            options for 'brew cask install <cask>' command

For *miscellaneous arguments*, the runtime commands are as below.

+-------------------+------------------------------------------------+
|      Option       |                    Command                     |
+===================+================================================+
| ``--install=ARG`` | ``brew cask install [options] ${ARG} <cask>``  |
+-------------------+------------------------------------------------+

.. raw:: html

    <h4>
      <a name="gem">
        Ruby Gem Automate Installer
      </a>
    </h4>

.. code:: man

    usage: macdaily install gem [options] <gems>

    Ruby Gem Automate Installer

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit

    specification arguments:
      -b, --brew            install gems by Ruby installed from Homebrew
      -s, --system          install gems by Ruby provided by macOS system
      -p GEM [GEM ...], --packages GEM [GEM ...]
                            name of Ruby gems to install

    general arguments:
      -q, --quiet           run in quiet mode, with no output information
      -v, --verbose         run in verbose mode, with detailed output information
      -y, --yes             yes for all selections

    miscellaneous arguments:
      -I ARG, --install ARG
                            options for 'gem install <gem>' command

For *miscellaneous arguments*, the runtime commands are as below.

+-------------------+----------------------------------------+
|      Option       |                 Command                |
+===================+========================================+
| ``--install=ARG`` | ``gem install [options] ${ARG} <gem>`` |
+-------------------+----------------------------------------+

NB
    RubyGems provided by macOS system is normally located at ``/usr/bin/gem`` or
    ``/System/Library/Frameworks/Ruby.framework/Versions/Current/usr/bin/gem``.

.. raw:: html

    <h4>
      <a name="mas">
        macOS Application Automate Installer
      </a>
    </h4>

.. code:: man

    usage: macdaily install mas [options] <applications>

    macOS Application Automate Installer

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit

    specification arguments:
      -f, --force           force reinstall
      -p APP [APP ...], --packages APP [APP ...]
                            name of macOS applications to install

    general arguments:
      -q, --quiet           run in quiet mode, with no output information
      -v, --verbose         run in verbose mode, with detailed output information
      -y, --yes             yes for all selections

    miscellaneous arguments:
      -I ARG, --install ARG
                            options for 'mas install|lucky <application>'
                            command

Since `Mac App Store CLI <https://github.com/mas-cli/mas#mas-cli>`__ (``mas``)
uses *integral IDs* as application token, when packages specified in
``--package`` option are integral, MacDaily uses ``mas install`` command
directly; otherwise, MacDaily calls ``mas lucky`` command instead.

For *miscellaneous arguments*, the runtime commands are as below.

+-------------------+--------------------------------------+
|      Option       |               Command                |
+===================+======================================+
|                   | ``mas install ${ARG} <application>`` |
+ ``--install=ARG`` +--------------------------------------+
|                   | ``mas lucky ${ARG} <application>``   |
+-------------------+--------------------------------------+

.. raw:: html

    <h4>
      <a name="npm">
        Node.js Module Automate Installer
      </a>
    </h4>

.. code:: man

    usage: macdaily install npm [options] <modules>

    Node.js Module Automate Installer

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit

    specification arguments:
      -p MOD [MOD ...], --packages MOD [MOD ...]
                            name of Node.js modules to install

    general arguments:
      -q, --quiet           run in quiet mode, with no output information
      -v, --verbose         run in verbose mode, with detailed output information
      -y, --yes             yes for all selections
      -n, --no-cleanup      do not run cleanup process

    miscellaneous arguments:
      -I ARG, --install ARG
                            options for 'npm install --global <module>'
                            command

For *miscellaneous arguments*, the runtime commands are as below.

+-------------------+----------------------------------------------------+
|      Option       |                       Command                      |
+===================+====================================================+
| ``--install=ARG`` | ``npm install --global [options] ${ARG} <module>`` |
+-------------------+----------------------------------------------------+

.. raw:: html

    <h4>
      <a name="pip">
        Python Package Automate Installer
      </a>
    </h4>

.. code:: man

    usage: macdaily install pip [options] <packages>

    Python Package Automate Installer

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit

    specification arguments:
      -u, --user            install to the Python user install directory for your
                            platform
      -b, --brew            install packages of Python installed from Homebrew
      -c, --cpython         install packages of CPython implementation
      -d, --pre             include pre-release and development versions
      -e VER [VER ...], --python VER [VER ...]
                            install packages by which version of Python
      -r, --pypy            install packages of PyPy implementation
      -s, --system          install packages of Python provided by macOS system
      -p PKG [PKG ...], --packages PKG [PKG ...]
                            name of Python packages to install

    general arguments:
      -q, --quiet           run in quiet mode, with no output information
      -v, --verbose         run in verbose mode, with detailed output information
      -y, --yes             yes for all selections
      -n, --no-cleanup      do not run cleanup process

    miscellaneous arguments:
      -I ARG, --install ARG
                            options for 'pip install <package>' command

For *miscellaneous arguments*, the runtime commands are as below.

+-------------------+--------------------------------------------+
|      Option       |                    Command                 |
+===================+============================================+
| ``--install=ARG`` | ``pip install [options] ${ARG} <package>`` |
+-------------------+--------------------------------------------+

Possible Python executables and corresponding flags are listed as below.

.. image:: https://github.com/JarryShaw/MacDaily/blob/dev/doc/img/Python.png

NB
    Python provided by macOS system (normally located at ``/usr/bin/python`` or
    ``/System/Library/Frameworks/Python.framework/Versions/Current/bin/python``)
    does not have ``pip`` installed. And it is
    `not recommended <https://docs.python.org/3/using/mac.html>`__ to do so.

.. raw:: html

    <h4>
      <a name="system">
        System Software Automate Installer
      </a>
    </h4>

.. code:: man

    usage: macdaily install system [options] <software>

    System Software Automate Installer

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit

    specification arguments:
      -R, --restart         automatically restart (or shut down) if required to
                            complete installation
      -p SW [SW ...], --packages SW [SW ...]
                            name of system software to install

    general arguments:
      -q, --quiet           run in quiet mode, with no output information
      -v, --verbose         run in verbose mode, with detailed output information
      -y, --yes             yes for all selections

    miscellaneous arguments:
      -I ARG, --install ARG
                            options for 'softwareupdate --install
                            <software>' command

For *miscellaneous arguments*, the runtime commands are as below.

+-------------------+----------------------------------------------------------+
|      Option       |                         Command                          |
+===================+==========================================================+
| ``--update=ARG``  | ``softwareupdate --install [options] ${ARG} <software>`` |
+-------------------+----------------------------------------------------------+

TODO
----

- ✔️ reconstruct update CLI
- ❌ implement further spec for the mini-language
- ❌ implement selection utility when string token given to ``mas`` command

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

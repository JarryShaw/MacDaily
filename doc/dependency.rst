:Command Executable:
    ``macdaily dependency`` | ``md-dependency``
:Supported Commands:
    ``brew``, ``pip``

==============================
macOS Package Dependency Query
==============================

- `About <#about>`__
- `Usage <#usage>`__
- `Commands <#commands>`__

  - `Homebrew Formulae <#brew>`__
  - `Python Package <#pip>`__

- `TODO <#todo>`__

--------------

About
-----

MacDaily provides intelligent solution for package dependency query.
MacDaily ``dependency`` command will automatically query dependencies
of packages installed through --

- |brew|_ -- `Homebrew <https://brew.sh>`__
- |pip|_ -- `Pip Installs Packages <https://pypy.org>`__

And for **tree** format support in this command, you will need to install
|dictdumper|_, which was a sub-project from development of |pypcapkit|_.

.. |dictdumper| replace:: ``DictDumper``
.. _dictdumper: https://github.com/JarryShaw/DictDumper
.. |pypcapkit| replace:: ``PyPCAPKit``
.. _pypcapkit: https://github.com/JarryShaw/PyPCAPKit

This command was originally inspired from and leveraged |pipdeptree|_.
However, if you would like to use ``pipdeptree`` for all installed Python
distributions, it is highly recommended to install ``pipdeptree`` with each
executable, which can be a bit fussy.

.. |pipdeptree| replace:: ``pipdeptree``
.. _pipdeptree: https://github.com/naiquevin/pipdeptree

Usage
-----

.. code:: man

    usage: macdaily dependency [options] <mode-selection> ...

    macOS Package Dependency Query

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit

    general arguments:
      -a, --all             query all packages installed through Python and
                            Homebrew
      -q, --quiet           run in quiet mode, with no output information
      -v, --verbose         run in verbose mode, with detailed output information
      -l, --show-log        open log in Console.app upon completion of command
      -f, --tree            show dependencies as a tree [requires DictDumper]
      -n, --topological     show dependencies in topological order
      -d LEVEL, --depth LEVEL
                            max display depth of the dependency tree

    package arguments:
      options used to specify packages of each mode

      --pip PKG [PKG ...]   name of Python packages to query
      --brew FORM [FORM ...]
                            name of Homebrew formulae to query

    control arguments:
      options used to disable update of certain mode

      --no-pip              do not query Python packages
      --no-brew             do not query Homebrew formulae

    mode selection:
      query dependency of packages installed through a specified method, e.g.:
      pip, brew

    aliases: deps, dp

MacDaily ``dependency`` supports using with multiple commands. Say, you would
like to query Python package dependencies and Homebrew formula dependencies,
each with different flags and options, then simply use the following command.

.. code:: shell

    macdaily dependency [global-options] pip [pip-options] brew [brew-options]

But please note that, global options ``--depth``, ``--quiet``, ``--verbose``
and ``--topological`` are *mandatory* for all commands once set to ``True``
(or legal value for ``depth`` option). That is to say, if you set these flags
in global options, they will overwrite corresponding flags in command specific
options.

For all options that take package names, a mini-language for condition
specification is provided.

+--------------+---------------------+
|    Format    |    Specification    |
+==============+=====================+
| ``package``  | query ``package``   |
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
      <a name="brew">
        Homebrew Formula Dependency Query
      </a>
    </h4>

.. code:: man

    usage: macdaily dependency brew [options] <formulae>

    Homebrew Formula Dependency Query

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit

    specification arguments:
      -b, --include-build   include the :build type dependencies
      -o, --include-optional
                            include :optional dependencies
      -t, --include-test    include (non-recursive) :test dependencies
      -s, --skip-recommended
                            skip :recommended type dependencies
      -r, --include-requirements
                            include requirements in addition to dependencies
      -p FORM [FORM ...], --packages FORM [FORM ...]
                            name of Homebrew formulae to query

    general arguments:
      -a, --all             query all Homebrew formulae installed through Homebrew
      -q, --quiet           run in quiet mode, with no output information
      -v, --verbose         run in verbose mode, with detailed output information
      -f, --tree            show dependencies as a tree [requires DictDumper]
      -n, --topological     show dependencies in topological order
      -d LEVEL, --depth LEVEL
                            max display depth of the dependency tree

When using ``--package`` option, if given wrong package name, MacDaily
might give a trivial *did-you-mean* correction.

.. raw:: html

    <h4>
      <a name="pip">
        Python Package Dependency Query
      </a>
    </h4>

.. code:: man

    usage: macdaily dependency pip [options] <packages>

    Python Package Dependency Query

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit

    specification arguments:
      -b, --brew            query packages of Python installed from Homebrew
      -c, --cpython         query packages of CPython implementation
      -e VER [VER ...], --python VER [VER ...]
                            indicate packages from which version of Python will
                            query
      -r, --pypy            query packages of PyPy implementation
      -s, --system          query packages of Python provided by macOS system
      -p PKG [PKG ...], --packages PKG [PKG ...]
                            name of Python packages to query

    general arguments:
      -a, --all             query all Python packages installed through Python
                            Package Index
      -q, --quiet           run in quiet mode, with no output information
      -v, --verbose         run in verbose mode, with detailed output information
      -f, --tree            show dependencies as a tree [requires DictDumper]
      -n, --topological     show dependencies in topological order
      -d LEVEL, --depth LEVEL
                            max display depth of the dependency tree

When using ``--package`` option, if given wrong package name, MacDaily
might give a trivial *did-you-mean* correction.

Possible Python executables and corresponding flags are listed as below.

.. image:: https://github.com/JarryShaw/MacDaily/blob/dev/doc/img/Python.png

NB
    Python provided by macOS system (normally located at ``/usr/bin/python`` or
    ``/System/Library/Frameworks/Python.framework/Versions/Current/bin/python``)
    does not have ``pip`` installed. And it is
    `not recommended <https://docs.python.org/3/using/mac.html>`__ to do so.


TODO
----

- ✔️ reconstruct dependency CLI
- ❌ implement further spec for the mini-language
- ❌ implement support for ``gem`` and ``npm``
- ❌ support custom options

.. |brew| replace:: ``brew``
.. _brew: #brew
.. |pip| replace:: ``pip``
.. _pip: #pip

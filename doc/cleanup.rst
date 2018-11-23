:Command Executable:
    ``macdaily cleanup`` | ``md-cleanup``
:Supported Commands:
    ``brew``, ``cask``, ``pip``, ``npm``

===========================
macOS Package Cache Cleanup
===========================

- `About <#about>`__
- `Usage <#usage>`__
- `Commands <#commands>`__

  - `Homebrew Formulae <#brew>`__
  - `Caskroom Binaries <#cask>`__
  - `Node.js Modules <#npm>`__
  - `Python Package <#pip>`__

- `TODO <#todo>`__

--------------

About
-----

MacDaily provides intelligent solution for automate caches cleanup.
MacDaily ``cleanup`` command will automatically cleanup all caches of
through --

- |brew|_ -- `Homebrew <https://brew.sh>`__
- |cask|_ -- `Homebrew Casks <https://caskroom.github.io>`__
- |npm|_ -- `Node.js Package Manager <https://nodejs.org>`__
- |pip|_ -- `Pip Installs Packages <https://pypy.org>`__

Usage
-----

.. code:: man

    usage: macdaily cleanup [options] <mode-selection> ...

    macOS Package Cache Cleanup

    optional arguments:
      -h, --help      show this help message and exit
      -V, --version   show program's version number and exit

    general arguments:
      -a, --all       cleanup caches of all packages installed through Node.js,
                      Homebrew, Caskroom and Python
      -q, --quiet     run in quiet mode, with no output information
      -v, --verbose   run in verbose mode, with detailed output information
      -l, --show-log  open log in Console.app upon completion of command

    control arguments:
      options used to disable update of certain mode

      --no-npm        do not update Node.js modules
      --no-pip        do not update Python packages
      --no-brew       do not update Homebrew formulae
      --no-cask       do not update Caskroom binaries

    mode selection:
      cleanup caches of packages installed through a specified method, e.g.:
      npm, pip, brew, cask

MacDaily ``cleanup`` supports using with multiple commands. Say, you would like
to cleanup Python and Homebrew caches, each with different flags and options,
then simply use the following command.

.. code:: shell

    macdaily cleanup [global-options] pip [pip-options] brew [brew-options]

But please note that, global options ``--quiet`` and ``--verbose`` are
*mandatory* for all commands once set to ``True``. That is to say, if you set
these flags in global options, they will overwrite corresponding flags in
command specific options.

Commands
--------

.. raw:: html

    <h4>
      <a name="brew">
        Homebrew Formula Cache Cleanup
      </a>
    </h4>

.. code:: man

    usage: macdaily cleanup brew [options] ...

    Homebrew Formula Cache Cleanup

    optional arguments:
      -h, --help     show this help message and exit
      -V, --version  show program's version number and exit

    general arguments:
      -q, --quiet    run in quiet mode, with no output information
      -v, --verbose  run in verbose mode, with detailed output information

MacDaily ``cleanup-brew`` command will remove logs under
``~/Library/Logs/Homebrew``. And if your external hard drive for archives
available at ``diskdir``, then MacDaily will try and archive caches of Homebrew
Formulae, which lies under ``~/Library/Caches/Homebrew``.

.. raw:: html

    <h4>
      <a name="cask">
        Homebrew Cask Cache Cleanup
      </a>
    </h4>

.. code:: man

    usage: macdaily cleanup cask [options] ...

    Homebrew Cask Cache Cleanup

    optional arguments:
      -h, --help     show this help message and exit
      -V, --version  show program's version number and exit

    general arguments:
      -q, --quiet    run in quiet mode, with no output information
      -v, --verbose  run in verbose mode, with detailed output information

If your external hard drive for archives available at ``diskdir``, then
MacDaily ``cleanup-cask`` command will try and archive caches of Homebrew
Formulae, which lies under ``~/Library/Caches/Homebrew/Cask``.

.. raw:: html

    <h4>
      <a name="npm">
        Node.js Module Cache Cleanup
      </a>
    </h4>

.. code:: man

    usage: macdaily cleanup npm [options] ...

    Node.js Module Cache Cleanup

    optional arguments:
      -h, --help     show this help message and exit
      -V, --version  show program's version number and exit

    general arguments:
      -q, --quiet    run in quiet mode, with no output information
      -v, --verbose  run in verbose mode, with detailed output information

MacDaily ``cleanup-npm`` command will directly run ``npm dedupe --global``
and ``npm cache clean --force`` commands.

.. raw:: html

    <h4>
      <a name="pip">
        Python Package Cache Cleanup
      </a>
    </h4>

.. code:: man

    usage: macdaily cleanup pip [options] ...

    Python Package Cache Cleanup

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit

    specification arguments:
      -b, --brew            cleanup caches of Python installed from Homebrew
      -c, --cpython         cleanup caches of CPython implementation
      -e VER [VER ...], --python VER [VER ...]
                            indicate packages from which version of Python will
                            cleanup
      -r, --pypy            cleanup caches of PyPy implementation
      -s, --system          cleanup caches of Python provided by macOS system

    general arguments:
      -q, --quiet           run in quiet mode, with no output information
      -v, --verbose         run in verbose mode, with detailed output information

MacDaily ``cleanup-pip`` command will directly remove all caches and logs under
``/var/root/Library/Caches/pip/http``, ``/var/root/Library/Caches/pip/wheels``,
``~/Library/Caches/pip/http`` and ``~/Library/Caches/pip/wheels``.

Possible Python executables and corresponding flags are listed as below.

.. image:: https://github.com/JarryShaw/MacDaily/tree/master/doc/img/Python.png

NB
    Python provided by macOS system (normally located at ``/usr/bin/python`` or
    ``/System/Library/Frameworks/Python.framework/Versions/Current/bin/python``)
    does not have ``pip`` installed. And it is
    `not recommended <https://docs.python.org/3/using/mac.html>`__ to do so.

TODO
----

- ✔️ reconstruct cleanup CLI
- ❌ implement further spec for cleanup commands

.. |brew| replace:: ``brew``
.. _brew: #brew
.. |cask| replace:: ``cask``
.. _cask: #cask
.. |npm| replace:: ``npm``
.. _npm: #npm
.. |pip| replace:: ``pip``
.. _pip: #pip

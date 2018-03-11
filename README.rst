.. _header-n0:

jsdaily
=======

Some useful daily utility scripts.

-  `Installation <#header-n101>`__

-  `Usage <#header-n110>`__

   -  ```update`` <#update>`__

      -  `Atom <#update_apm>`__

      -  `Python <#update_pip>`__

      -  `Homebrew <#update_brew>`__

      -  `Caskroom <#update_cask>`__

      -  `App Store <#update_apptore>`__

   -  ```uninstall`` <#uninstall>`__

      -  `Python <#uninstall_pip>`__

      -  `Homebrew <#uninstall_brew>`__

      -  `Caskroom <#uninstall_cask>`__

   -  ```reinstall`` <#reinstall>`__

      -  `Homebrew <#reinstall_brew>`__

      -  `Caskroom <#reinstall_cask>`__

   -  ```postinstall`` <#postinstall>`__

      -  `Homebrew <#postinstall_brew>`__

   -  ```dependency`` <#dependency>`__

      -  `Python <#dependency_pip>`__

      -  `Homebrew <#dependency_brew>`__

   -  ```logging`` <#logging>`__

      -  Atom

      -  Python

      -  Homebrew

      -  Caskroom

      -  App Store

      -  Mac Applications

      -  All Applications (``*.app``)

--------------

.. _header-n101:

Installation
------------

    Note that ``jsdaily`` requires Python versions **since 3.6**

.. code::

    pip install jsdaily

.. _header-n110:

Usage
-----

.. _header-n113:

``update``
~~~~~~~~~~

 ``update`` is a package manager written in Python 3.6 and Bash 3.2,
which automatically update all packages installed through --

-  ``apm`` -- Atom packages

-  ``pip`` -- Python packages, in both version of 2.7 and 3.6, running
   under `CPython <https://www.python.org>`__ or
   `PyPy <https://pypy.org>`__ compiler, and installed through ``brew``
   or official disk images

-  ``brew`` -- `Homebrew <https://brew.sh>`__ packages

-  ``cask`` -- `Caskroom <https://caskroom.github.io>`__ applications

-  ``appstore`` -- Mac App Store or ``softwareupdate`` installed
   applications

 You may install ``update`` through ``pip`` of Python (versions 3.\*).
And log files can be found in directory
``/Library/Logs/Scripts/update/``. The global man page for ``update``
shows as below.

.. code::

    $ update --help
    usage: update [-h] [-V] [-a] [-f] [-m] [-g] [-q] [-v] MODE ...

    Automatic Package Update Manager

    optional arguments:
      -h, --help     show this help message and exit
      -V, --version  show program's version number and exit
      -a, --all      Update all packages installed through pip, Homebrew, and App
                     Store.
      -f, --force    Run in force mode, only for Homebrew or Caskroom.
      -m, --merge    Run in merge mode, only for Homebrew.
      -g, --greedy   Run in greedy mode, only for Caskroom.
      -q, --quiet    Run in quiet mode, with no output information.
      -v, --verbose  Run in verbose mode, with more information.

    mode selection:
      MODE           Update outdated packages installed through a specified
                     method, e.g.: apm, pip, brew, cask, or appstore.

 As it shows, there are five modes in total (if these commands exists).
To update all packages, you may use one of commands below.

.. code::

    $ update
    $ update -a
    $ update --all

1. ``apm`` -- Atom packages

 `Atom <https://atom.io>`__ provides a package manager called ``apm``,
i.e. "Atom Package Manager". The man page for ``update apm`` shows as
below.

.. code::

    $ update apm --help
    usage: update apm [-h] [-a] [-p PKG] [-q] [-v]

    Update installed Atom packages.

    optional arguments:
      -h, --help            show this help message and exit
      -a, --all             Update all packages installed through apm.
      -p PKG, --package PKG
                            Name of packages to be updated, default is all.
      -q, --quiet           Run in quiet mode, with no output information.
      -v, --verbose         Run in verbose mode, with more information.

 If arguments omit, ``update apm`` will update all outdated packages of
Atom. And when using ``-p`` or ``--package``, if given wrong package
name, ``update apm`` might give a trivial "did-you-mean" correction.

1. ``pip`` -- Python packages

 As there\'re all kinds and versions of Python complier, along with its
``pip`` package manager. Here, we support update of following --

-  Python 2.7/3.6 installed through Python official disk images

-  Python 2.7/3.6 installed through ``brew install python/python3``

-  PyPy 2.7/3.5 installed through ``brew install pypy/pypy3``

And the man page shows as below.

.. code::

    $ update pip --help
    usage: update pip [-h] [-a] [-V VER] [-s] [-b] [-c] [-y] [-p PKG] [-q] [-v]

    Update installed Python packages.

    optional arguments:
      -h, --help            show this help message and exit
      -a, --all             Update all packages installed through pip.
      -V VER, --version VER
                            Indicate which version of pip will be updated.
      -s, --system          Update pip packages on system level, i.e. python
                            installed through official installer.
      -b, --brew            Update pip packages on Cellar level, i.e. python
                            installed through Homebrew.
      -c, --cpython         Update pip packages on CPython environment.
      -y, --pypy            Update pip packages on Pypy environment.
      -p PKG, --package PKG
                            Name of packages to be updated, default is all.
      -q, --quiet           Run in quiet mode, with no output information.
      -v, --verbose         Run in verbose mode, with more information.

 If arguments omit, ``update pip`` will update all outdated packages in
all copies of Python. And when using ``-p`` or ``--package``, if given
wrong package name, ``update pip`` might give a trivial "did-you-mean"
correction.

1. ``brew`` -- Homebrew packages

 The man page for ``update brew`` shows as below.

.. code::

    $ update brew --help
    usage: update brew [-h] [-a] [-p PKG] [-f] [-m] [-q] [-v]

    Update installed Homebrew packages.

    optional arguments:
      -h, --help            show this help message and exit
      -a, --all             Update all packages installed through Homebrew.
      -p PKG, --package PKG
                            Name of packages to be updated, default is all.
      -f, --force           Use "--force" when running `brew update`.
      -m, --merge           Use "--merge" when running `brew update`.
      -q, --quiet           Run in quiet mode, with no output information.
      -v, --verbose         Run in verbose mode, with more information.

 Note that, arguments ``-f`` and ``--force``, ``-m`` and ``--merge`` are
using only for ``brew update`` command.

 If arguments omit, ``update brew`` will update all outdated packages of
Homebrew. And when using ``-p`` or ``--package``, if given wrong package
name, ``update brew`` might give a trivial "did-you-mean" correction.

1. ``cask`` -- Caskrooom packages

 The man page for ``update cask`` shows as below.

.. code::

    $ update cask  --help
    usage: update cask [-h] [-a] [-p PKG] [-f] [-g] [-q] [-v]

    Update installed Caskroom packages.

    optional arguments:
      -h, --help            show this help message and exit
      -a, --all             Update all packages installed through Caskroom.
      -p PKG, --package PKG
                            Name of packages to be updated, default is all.
      -f, --force           Use "--force" when running `brew cask upgrade`.
      -g, --greedy          Use "--greedy" when running `brew cask outdated`, and
                            directly run `brew cask upgrade --greedy`.
      -q, --quiet           Run in quiet mode, with no output information.
      -v, --verbose         Run in verbose mode, with more information.

 Note that, arguments ``-f`` and ``--force``, ``-g`` and ``--greedy``
are using only for ``brew cask upgrade`` command. And when latter given,
``update`` will directly run ``brew cask upgrade --greedy``.

 If arguments omit, ``update cask`` will update all outdated packages of
Caskroom. And when using ``-p`` or ``--package``, if given wrong package
name, ``update cask`` might give a trivial "did-you-mean" correction.

1. ``appstore`` -- Mac App Store packages

 The man page for ``update appstore`` shows as below.

.. code::

    $ update appstore --help
    usage: update appstore [-h] [-a] [-p PKG] [-q]

    Update installed App Store packages.

    optional arguments:
      -h, --help            show this help message and exit
      -a, --all             Update all packages installed through App Store.
      -p PKG, --package PKG
                            Name of packages to be updated, default is all.
      -q, --quiet           Run in quiet mode, with no output information.

 If arguments omit, ``update appstore`` will update all outdated
packages in Mac App Store or ``softwareupdate``. And when using ``-p``
or ``--package``, if given wrong package name, ``update appstore`` might
give a trivial "did-you-mean" correction.

.. _header-n213:

``uninstall``
~~~~~~~~~~~~~

 ``uninstall`` is a package manager written in Python 3.6 and Bash 3.2,
which recursively and interactively uninstall packages installed through
--

-  ``pip`` -- Python packages, in both version of 2.7 and 3.6, running
   under `CPython <https://www.python.org>`__ or
   `PyPy <https://pypy.org>`__ compiler, and installed through ``brew``
   or official disk images

-  ``brew`` -- `Homebrew <https://brew.sh>`__ packages

-  ``cask`` -- `Caskroom <https://caskroom.github.io>`__ applications

 You may install ``uninstall`` through ``pip`` of Python (versions
3.\*). And log files can be found in directory
``/Library/Logs/Scripts/uninstall/``. The global man page for
``uninstall`` shows as below.

.. code::

    $ uninstall --help
    usage: uninstall [-h] [-V] [-a] [-f] [-i] [-q] [-v] [-Y] MODE ...

    Package Recursive Uninstall Manager

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit
      -a, --all             Uninstall all packages installed through pip,
                            Homebrew, and App Store.
      -f, --force           Run in force mode, only for Homebrew and Caskroom.
      -i, --ignore-dependencies
                            Run in irrecursive mode, only for Python and Homebrew.
      -q, --quiet           Run in quiet mode, with no output information.
      -v, --verbose         Run in verbose mode, with more information.
      -Y, --yes             Yes for all selections.

    mode selection:
      MODE                  Uninstall given packages installed through a specified
                            method, e.g.: pip, brew or cask.

 As it shows, there are three modes in total (if these commands exists).
The default procedure when arguments omit is to stand alone. To
uninstall all packages, you may use one of commands below.

.. code::

    $ uninstall -a
    $ uninstall --all

1. ``pip`` -- Python packages

 As there're several kinds and versions of Python complier, along wiht
its ``pip`` package manager. Here, we support uninstall procedure in
following --

-  Python 2.7/3.6 installed through Python official disk images

-  Python 2.7/3.6 installed through ``brew install python/python3``

-  PyPy 2.7/3.5 installed through ``brew install pypy/pypy3``

 And the man page shows as below.

.. code::

    $ uninstall pip --help
    usage: uninstall pip [-h] [-a] [-V VER] [-s] [-b] [-c] [-y] [-p PKG] [-i] [-q]
                         [-v] [-Y]

    Uninstall pip installed packages.

    optional arguments:
      -h, --help            show this help message and exit
      -a, --all             Uninstall all packages installed through pip.
      -V VER, --version VER
                            Indicate packages in which version of pip will be
                            uninstalled.
      -s, --system          Uninstall pip packages on system level, i.e. python
                            installed through official installer.
      -b, --brew            Uninstall pip packages on Cellar level, i.e. python
                            installed through Homebrew.
      -c, --cpython         Uninstall pip packages on CPython environment.
      -y, --pypy            Uninstall pip packages on Pypy environment.
      -p PKG, --package PKG
                            Name of packages to be uninstalled, default is null.
      -i, --ignore-dependencies
                            Run in irrecursive mode, i.e. ignore dependencies of
                            installing packages.
      -q, --quiet           Run in quiet mode, with no output information.
      -v, --verbose         Run in verbose mode, with more information.
      -Y, --yes             Yes for all selections.

 If arguments omit, ``uninstall pip`` will stand alone, and do nothing.
To uninstall all packages, use ``-a`` or ``--all`` option. And when
using ``-p`` or ``--package``, if given wrong package name,
``uninstall pip`` might give a trivial “did-you-mean” correction.

1. ``brew`` – Homebrew packages

 The man page for ``uninstall brew`` shows as below.

.. code::

    $ uninstall brew --help
    usage: uninstall brew [-h] [-a] [-p PKG] [-f] [-i] [-q] [-v] [-Y]

    Uninstall Homebrew installed packages.

    optional arguments:
      -h, --help            show this help message and exit
      -a, --all             Uninstall all packages installed through Homebrew.
      -p PKG, --package PKG
                            Name of packages to be uninstalled, default is null.
      -f, --force           Use "--force" when running `brew uninstall`.
      -i, --ignore-dependencies
                            Run in irrecursive mode, i.e. ignore dependencies of
                            installing packages.
      -q, --quiet           Run in quiet mode, with no output information.
      -v, --verbose         Run in verbose mode, with more information.
      -Y, --yes             Yes for all selections.

 If arguments omit, ``uninstall brew`` will stand alone, and do nothing.
To uninstall all packages, use ``-a`` or ``--all`` option. And when
using ``-p`` or ``--package``, if given wrong package name,
``uninstall brew`` might give a trivial “did-you-mean” correction.

1. ``cask`` – Caskrooom packages

 The man page for ``uninstall cask`` shows as below.

.. code::

    $ uninstall cask --help
    usage: uninstall cask [-h] [-a] [-p PKG] [-f] [-q] [-v] [-Y]

    Uninstall installed Caskroom packages.

    optional arguments:
      -h, --help            show this help message and exit
      -a, --all             Uninstall all packages installed through Caskroom.
      -p PKG, --package PKG
                            Name of packages to be uninstalled, default is null.
      -f, --force           Use "--force" when running `brew cask uninstall`.
      -q, --quiet           Run in quiet mode, with no output information.
      -v, --verbose         Run in verbose mode, with more information.
      -Y, --yes             Yes for all selections.

 If arguments omit, ``uninstall cask`` will stand alone, and do nothing.
To uninstall all packages, use ``-a`` or ``--all`` option. And when
using ``-p`` or ``--package``, if given wrong package name,
``uninstall cask`` might give a trivial “did-you-mean” correction.

.. _header-n281:

``reinstall``
~~~~~~~~~~~~~

 ``reinstall`` is a package manager written in Python 3.6 and Bash 3.2,
which automatically and interactively reinstall packages installed
through --

-  ``brew`` -- `Homebrew <https://brew.sh>`__ packages

-  ``cask`` -- `Caskroom <https://caskroom.github.io>`__ applications

 You may install ``reinstall`` through ``pip`` of Python (versions
3.\*). And log files can be found in directory
``/Library/Logs/Scripts/reinstall/``. The global man page for
``reinstall`` shows as below.

.. code::

    $ reinstall --help
    usage: reinstall [-h] [-V] [-a] [-s START] [-e START] [-f] [-q] [-v] MODE ...

    Homebrew Package Reinstall Manager

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit
      -a, --all             Reinstall all packages installed through Homebrew and
                            Caskroom.
      -s START, --startwith START
                            Reinstall procedure starts from which package, sort in
                            initial alphabets.
      -e START, --endwith START
                            Reinstall procedure ends until which package, sort in
                            initial alphabets.
      -f, --force           Run in force mode, using for `brew reinstall`.
      -q, --quiet           Run in quiet mode, with no output information.
      -v, --verbose         Run in verbose mode, with detailed output information.

    mode selection:
      MODE                  Reinstall packages installed through a specified
                            method, e.g.: brew or cask.

 As it shows, there are two modes in total (if these commands exists).
The default procedure when arguments omit is to stand alone. To
reinstall all packages, you may use one of commands below.

.. code::

    $ reinstall -a
    $ reinstall --all

1. ``brew`` – Homebrew packages

 The man page for ``reinstall brew`` shows as below.

.. code::

    $ reinstall brew --help
    usage: reinstall brew [-h] [-p PKG] [-s START] [-e START] [-f] [-q] [-v]

    Reinstall Homebrew packages.

    optional arguments:
      -h, --help            show this help message and exit
      -p PKG, --package PKG
                            Name of packages to be reinstalled, default is null.
      -s START, --startwith START
                            Reinstall procedure starts from which package, sort in
                            initial alphabets.
      -e START, --endwith START
                            Reinstall procedure ends until which package, sort in
                            initial alphabets.
      -f, --force           Run in force mode, using for `brew reinstall`.
      -q, --quiet           Run in quiet mode, with no output information.
      -v, --verbose         Run in verbose mode, with detailed output information.

 If arguments omit, ``reinstall brew`` will stand alone, and do nothing.
To reinstall all packages, use ``-a`` or ``--all`` option. And when
using ``-p`` or ``--package``, if given wrong package name,
``reinstall brew`` might give a trivial “did-you-mean” correction.

1. ``cask`` – Caskrooom packages

 The man page for ``reinstall cask`` shows as below.

.. code::

    $ reinstall cask --help
    usage: reinstall cask [-h] [-p PKG] [-s START] [-e START] [-q] [-v]

    Reinstall Caskroom packages.

    optional arguments:
      -h, --help            show this help message and exit
      -p PKG, --package PKG
                            Name of packages to be reinstalled, default is null.
      -s START, --startwith START
                            Reinstall procedure starts from which package, sort in
                            initial alphabets.
      -e START, --endwith START
                            Reinstall procedure ends until which package, sort in
                            initial alphabets.
      -q, --quiet           Run in quiet mode, with no output information.
      -v, --verbose         Run in verbose mode, with detailed output information.

 If arguments omit, ``reinstall cask`` will stand alone, and do nothing.
To reinstall all packages, use ``-a`` or ``--all`` option. And when
using ``-p`` or ``--package``, if given wrong package name,
``reinstall cask`` might give a trivial “did-you-mean” correction.

.. _header-n323:

``postinstall``
~~~~~~~~~~~~~~~

 ``postinstall`` is a package manager written in Python 3.6 and Bash
3.2, which automatically and interactively postinstall packages
installed through --

-  ``brew`` -- `Homebrew <https://brew.sh>`__ packages

 You may install ``postinstall`` through ``pip`` of Python (versions
3.\*). And log files can be found in directory
``/Library/Logs/Scripts/postinstall/``. The global man page for
``postinstall`` shows as below.

.. code::

    $ postinstall --help
    usage: postinstall [-h] [-V] [-a] [-p PKG] [-s START] [-e START] [-q] [-v]

    Homebrew Package Postinstall Manager

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit
      -a, --all             Postinstall all packages installed through Homebrew.
      -p PKG, --package PKG
                            Name of packages to be postinstalled, default is all.
      -s START, --startwith START
                            Postinstall procedure starts from which package, sort
                            in initial alphabets.
      -e START, --endwith START
                            Postinstall procedure ends until which package, sort
                            in initial alphabets.
      -q, --quiet           Run in quiet mode, with no output information.
      -v, --verbose         Run in verbose mode, with detailed output information.

 As it shows, there is only one mode in total (if these commands
exists). To postinstall all packages, you may use one of commands below.

.. code::

    $ postinstall
    $ postinstall -a
    $ postinstall --all

 If arguments omit, ``postinstall`` will postinstall all installed
packages of Homebrew. And when using ``-p`` or ``--package``, if given
wrong package name, ``postinstall`` might give a trivial "did-you-mean"
correction.

.. _header-n342:

``dependency``
~~~~~~~~~~~~~~

 ``dependency`` is a package manager written in Python 3.6 and Bash 3.2,
which automatically and interactively show dependencies of packages
installed through --

-  ``pip`` -- Python packages, in both version of 2.7 and 3.6, running
   under `CPython <https://www.python.org>`__ or
   `PyPy <https://pypy.org>`__ compiler, and installed through ``brew``
   or official disk images

-  ``brew`` -- `Homebrew <https://brew.sh>`__ packages

 You may install ``dependency`` through ``pip`` of Python (versions
3.\*). And log files can be found in directory
``/Library/Logs/Scripts/dependency/``. The global man page for
``dependency`` shows as below.

.. code::

    $ dependency --help
    usage: dependency [-h] [-V] [-a] [-t] MODE ...

    Trivial Package Dependency Manager

    optional arguments:
      -h, --help     show this help message and exit
      -V, --version  show program's version number and exit
      -a, --all      Show dependencies of all packages installed through pip and
                     Homebrew.
      -t, --tree     Show dependencies as a tree. This feature may request
                     `pipdeptree`.

    mode selection:
      MODE           Show dependencies of packages installed through a specified
                     method, e.g.: pip or brew.

 As it shows, there are two mode in total (if these commands exists).
The default procedure when arguments omit is to stand alone. To show
dependency of all packages, you may use one of commands below.

.. code::

    $ dependency -a
    $ dependency --all

1. ``pip`` -- Python packages

 As there\'re all kinds and versions of Python complier, along with its
``pip`` package manager. Here, we support showing dependency of
following --

-  Python 2.7/3.6 installed through Python official disk images

-  Python 2.7/3.6 installed through ``brew install python/python3``

-  PyPy 2.7/3.5 installed through ``brew install pypy/pypy3``

And the man page shows as below.

.. code::

    $ dependency pip --help
    usage: dependency pip [-h] [-a] [-V VER] [-s] [-b] [-c] [-y] [-p PKG] [-t]

    Show dependencies of Python packages.

    optional arguments:
      -h, --help            show this help message and exit
      -a, --all             Show dependencies of all packages installed through
                            pip.
      -V VER, --version VER
                            Indicate which version of pip will be updated.
      -s, --system          Show dependencies of pip packages on system level,
                            i.e. python installed through official installer.
      -b, --brew            Show dependencies of pip packages on Cellar level,
                            i.e. python installed through Homebrew.
      -c, --cpython         Show dependencies of pip packages on CPython
                            environment.
      -y, --pypy            Show dependencies of pip packages on PyPy environment.
      -p PKG, --package PKG
                            Name of packages to be shown, default is all.
      -t, --tree            Show dependencies as a tree. This feature requests
                            `pipdeptree`.

 If arguments omit, ``dependency pip`` will stand alone, and do nothing.
To show dependency of all packages, use ``-a`` or ``--all`` option. And
when using ``-p`` or ``--package``, if given wrong package name,
``dependency pip`` might give a trivial “did-you-mean” correction.

1. ``brew`` – Homebrew packages

 The man page for ``dependency brew`` shows as below.

.. code::

    $ dependency brew --help
    usage: dependency brew [-h] [-a] [-p PKG] [-t]

    Show dependencies of Homebrew packages.

    optional arguments:
      -h, --help            show this help message and exit
      -a, --all             Show dependencies of all packages installed through
                            Homebrew.
      -p PKG, --package PKG
                            Name of packages to be shown, default is all.
      -t, --tree            Show dependencies as a tree.

 If arguments omit, ``dependency brew`` will stand alone, and do
nothing. To show dependency of all packages, use ``-a`` or ``--all``
option. And when using ``-p`` or ``--package``, if given wrong package
name, ``dependency brew`` might give a trivial “did-you-mean”
correction.

.. _header-n396:

``logging``
~~~~~~~~~~~

 ``logging`` is a logging manager written in Python 3.6 and Bash 3.2,
which automatically log all applications and/or packages installed
through --

-  ``apm`` -- Atom packages

-  ``pip`` -- Python packages, in both version of 2.7 and 3.6, running
   under `CPython <https://www.python.org>`__ or
   `PyPy <https://pypy.org>`__ compiler, and installed through ``brew``
   or official disk images

-  ``brew`` -- `Homebrew <https://brew.sh>`__ packages

-  ``cask`` -- `Caskroom <https://caskroom.github.io>`__ applications

-  ``appstore`` -- Mac App Store or ``softwareupdate`` installed
   applications

-  ``macapp`` -- applications in ``/Applications`` folder

-  ``dotapp`` -- all ``*.app`` files on this Mac, a.k.a.
   ``/Volumes/Macintosh HD`` folder

 You may install ``logging`` through ``pip`` of Python (versions 3.\*).
And log files can be found in directory
``/Library/Logs/Scripts/logging/``. The global man page for ``logging``
shows as below.

.. code::

    $ logging --help
    usage: logging [-h] [-V] [-a] [-v VER] [-s] [-b] [-c] [-y] [MODE [MODE ...]]

    Application and Package Logging Manager

    positional arguments:
      MODE                 The name of logging mode, could be any from followings,
                           apm, pip, brew, cask, dotapp, macapp, or appstore.

    optional arguments:
      -h, --help           show this help message and exit
      -V, --version        show program's version number and exit
      -a, --all            Log applications and packages of all entries.
      -v VER, --pyver VER  Indicate which version of pip will be logged.
      -s, --system         Log pip packages on system level, i.e. python installed
                           through official installer.
      -b, --brew           Log pip packages on Cellar level, i.e. python installed
                           through Homebrew.
      -c, --cpython        Log pip packages on CPython environment.
      -y, --pypy           Log pip packages on PyPy environment.
      -q, --quiet          Run in quiet mode, with no output information.

 As it shows, there are seven mode in total (if these commands exists),
and you may call **multiple** modes at one time. The default procedure
when arguments omit is to stand alone. To log all entries, you may use
one of commands below.

.. code::

    $ logging -a
    $ logging --all
    $ logging apm pip brew cask dotapp macapp appstore

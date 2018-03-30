.. _header-n0:

jsdaily
=======

Some useful daily utility scripts.

-  `Installation <#header-n101>`__

-  `Usage <#header-n110>`__

   -  ```jsupdate`` <#update>`__

      -  `Atom <#update_apm>`__

      -  `Python <#update_pip>`__

      -  `Homebrew <#update_brew>`__

      -  `Caskroom <#update_cask>`__

      -  `App Store <#update_apptore>`__

   -  ```jsuninstall`` <#uninstall>`__

      -  `Python <#uninstall_pip>`__

      -  `Homebrew <#uninstall_brew>`__

      -  `Caskroom <#uninstall_cask>`__

   -  ```jsreinstall`` <#reinstall>`__

      -  `Homebrew <#reinstall_brew>`__

      -  `Caskroom <#reinstall_cask>`__

   -  ```jspostinstall`` <#postinstall>`__

      -  `Homebrew <#postinstall_brew>`__

   -  ```jsdeps`` <#dependency>`__

      -  `Python <#dependency_pip>`__

      -  `Homebrew <#dependency_brew>`__

   -  ```jslogging`` <#logging>`__

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

``jsupdate``
~~~~~~~~~~~~

``jsupdate`` is a package manager written in Python 3.6 and Bash 3.2,
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

You may install ``jsupdate`` through ``pip`` of Python (versions 3.\*).
And log files can be found in directory
``/Library/Logs/Scripts/update/``. The global man page for ``jsupdate``
shows as below.

.. code:: 

    $ jsupdate --help
    usage: jsupdate [-hV] [-qv] [-fgm] [-a] [--[no-]MODE] MODE ...

    Automatic Package Update Manager

    optional arguments:
      -h, --help     show this help message and exit
      -V, --version  show program's version number and exit
      -a, --all      update all packages installed through pip, Homebrew, and App
                     Store
      -f, --force    run in force mode, only for Homebrew or Caskroom
      -m, --merge    run in merge mode, only for Homebrew
      -g, --greedy   run in greedy mode, only for Caskroom
      -q, --quiet    run in quiet mode, with no output information
      -v, --verbose  run in verbose mode, with detailed output information

    mode selection:
      MODE           update outdated packages installed through a specified
                     method, e.g.: apm, pip, brew, cask, appstore, or
                     alternatively and simply, cleanup

As it shows, there are five modes in total (if these commands exists).
To update all packages, you may use one of commands below.

.. code:: 

    $ jsupdate -a
    $ jsupdate --all

1. ``apm`` -- Atom packages

`Atom <https://atom.io>`__ provides a package manager called ``apm``,
i.e. "Atom Package Manager". The man page for ``jsupdate apm`` shows as
below.

.. code:: 

    $ jsupdate apm --help
    usage: jsupdate apm [-h] [-qv] [-a] [-p PKG]

    Update Installed Atom Packages

    optional arguments:
      -h, --help            show this help message and exit
      -a, --all             update all packages installed through apm
      -p PKG, --package PKG
                            name of packages to be updated, default is all
      -q, --quiet           run in quiet mode, with no output information
      -v, --verbose         run in verbose mode, with detailed output information

If arguments omit, ``jsupdate apm`` will **NOT** update outdated
packages of Atom. And when using ``-p`` or ``--package``, if given wrong
package name, ``jsupdate apm`` might give a trivial "did-you-mean"
correction.

1. ``pip`` -- Python packages

As there\'re all kinds and versions of Python complier, along with its
``pip`` package manager. Here, we support update of following --

-  Python 2.7/3.6 installed through Python official disk images

-  Python 2.7/3.6 installed through ``brew install python@2/python``

-  PyPy 2.7/3.5 installed through ``brew install pypy/pypy3``

And the man page shows as below.

.. code:: 

    $ jsupdate pip --help
    usage: jsupdate pip [-h] [-qv] [-bcsy] [-V VER] [-a] [-p PKG]

    Update Installed Python Packages

    optional arguments:
      -h, --help            show this help message and exit
      -a, --all             update all packages installed through pip
      -V VER, --python_version VER
                            indicate which version of pip will be updated
      -s, --system          update pip packages on system level, i.e. python
                            installed through official installer
      -b, --brew            update pip packages on Cellar level, i.e. python
                            installed through Homebrew
      -c, --cpython         update pip packages on CPython environment
      -y, --pypy            update pip packages on PyPy environment
      -p PKG, --package PKG
                            name of packages to be updated, default is all
      -q, --quiet           run in quiet mode, with no output information
      -v, --verbose         run in verbose mode, with detailed output information

If arguments omit, ``jsupdate pip`` will **NOT** update outdated
packages in all copies of Python. And when using ``-p`` or
``--package``, if given wrong package name, ``jsupdate pip`` might give
a trivial "did-you-mean" correction.

1. ``brew`` -- Homebrew packages

The man page for ``jsupdate brew`` shows as below.

.. code:: 

    $ jsupdate brew --help
    usage: jsupdate brew [-h] [-qv] [-fm] [-a] [-p PKG] [--no-cleanup]

    Update Installed Homebrew Packages

    optional arguments:
      -h, --help            show this help message and exit
      -a, --all             update all packages installed through Homebrew
      -p PKG, --package PKG
                            name of packages to be updated, default is all
      -f, --force           use "--force" when running `brew update`
      -m, --merge           use "--merge" when running `brew update`
      -q, --quiet           run in quiet mode, with no output information
      -v, --verbose         run in verbose mode, with detailed output information
      --no-cleanup          do not remove caches & downloads

Note that, arguments ``-f`` and ``--force``, ``-m`` and ``--merge`` are
using only for ``brew update`` command.

If arguments omit, ``jsupdate brew`` will **NOT** update outdated
packages of Homebrew. And when using ``-p`` or ``--package``, if given
wrong package name, ``jsupdate brew`` might give a trivial
"did-you-mean" correction.

1. ``cask`` -- Caskrooom packages

The man page for ``jsupdate cask`` shows as below.

.. code:: 

    $ jsupdate cask --help
    usage: jsupdate cask [-h] [-qv] [-fg] [-a] [-p PKG] [--no-cleanup]

    Update Installed Caskroom Packages

    optional arguments:
      -h, --help            show this help message and exit
      -a, --all             update all packages installed through Caskroom
      -p PKG, --package PKG
                            name of packages to be updated, default is all
      -f, --force           use "--force" when running `brew cask upgrade`
      -g, --greedy          use "--greedy" when running `brew cask outdated`, and
                            directly run `brew cask upgrade --greedy`
      -q, --quiet           run in quiet mode, with no output information
      -v, --verbose         run in verbose mode, with detailed output information
      --no-cleanup          do not remove caches & downloads

Note that, arguments ``-f`` and ``--force``, ``-g`` and ``--greedy`` are
using only for ``brew cask upgrade`` command. And when latter given,
``jsupdate`` will directly run ``brew cask upgrade --greedy``.

If arguments omit, ``jsupdate cask`` will **NOT** update outdated
packages of Caskroom. And when using ``-p`` or ``--package``, if given
wrong package name, ``jsupdate cask`` might give a trivial
"did-you-mean" correction.

1. ``appstore`` -- Mac App Store packages

The man page for ``jsupdate appstore`` shows as below.

.. code:: 

    $ jsupdate appstore --help
    usage: jsupdate appstore [-h] [-q] [-a] [-p PKG]

    Update installed App Store packages

    optional arguments:
      -h, --help            show this help message and exit
      -a, --all             update all packages installed through App Store
      -p PKG, --package PKG
                            name of packages to be updated, default is all
      -q, --quiet           run in quiet mode, with no output information

If arguments omit, ``jsupdate appstore`` will **NOT** update outdated
packages in Mac App Store or ``softwareupdate``. And when using ``-p``
or ``--package``, if given wrong package name, ``jsupdate appstore``
might give a trivial "did-you-mean" correction.

.. _header-n213:

``jsuninstall``
~~~~~~~~~~~~~~~

``jsuninstall`` is a package manager written in Python 3.6 and Bash 3.2,
which recursively and interactively uninstall packages installed through
--

-  ``pip`` -- Python packages, in both version of 2.7 and 3.6, running
   under `CPython <https://www.python.org>`__ or
   `PyPy <https://pypy.org>`__ compiler, and installed through ``brew``
   or official disk images

-  ``brew`` -- `Homebrew <https://brew.sh>`__ packages

-  ``cask`` -- `Caskroom <https://caskroom.github.io>`__ applications

You may install ``jsuninstall`` through ``pip`` of Python (versions
3.\*). And log files can be found in directory
``/Library/Logs/Scripts/uninstall/``. The global man page for
``jsuninstall`` shows as below.

.. code:: 

    $ jsuninstall --help
    usage: jsuninstall [-hV] [-qv] [-fiY] [-a] [--[no-]MODE] MODE ...

    Package Recursive Uninstall Manager

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit
      -a, --all             uninstall all packages installed through pip,
                            Homebrew, and App Store
      -f, --force           run in force mode, only for Homebrew and Caskroom
      -i, --ignore-dependencies
                            run in irrecursive mode, only for Python and Homebrew
      -q, --quiet           run in quiet mode, with no output information
      -v, --verbose         run in verbose mode, with more information
      -Y, --yes             yes for all selections

    mode selection:
      MODE                  uninstall given packages installed through a specified
                            method, e.g.: pip, brew or cask

As it shows, there are three modes in total (if these commands exists).
The default procedure when arguments omit is to stand alone. To
uninstall all packages, you may use one of commands below.

.. code:: 

    $ jsuninstall -a
    $ jsuninstall --all

1. ``pip`` -- Python packages

As there're several kinds and versions of Python complier, along wiht
its ``pip`` package manager. Here, we support uninstall procedure in
following --

-  Python 2.7/3.6 installed through Python official disk images

-  Python 2.7/3.6 installed through ``brew install python@2/python``

-  PyPy 2.7/3.5 installed through ``brew install pypy/pypy3``

And the man page shows as below.

.. code:: 

    $ jsuninstall pip --help
    usage: jsuninstall pip [-h] [-qv] [-iY] [-bcsy] [-V VER] [-a] [-p PKG]

    Uninstall Installed Python Packages

    optional arguments:
      -h, --help            show this help message and exit
      -a, --all             uninstall all packages installed through pip
      -V VER, --python_version VER
                            indicate packages in which version of pip will be
                            uninstalled
      -s, --system          uninstall pip packages on system level, i.e. python
                            installed through official installer
      -b, --brew            uninstall pip packages on Cellar level, i.e. python
                            installed through Homebrew
      -c, --cpython         uninstall pip packages on CPython environment
      -y, --pypy            uninstall pip packages on Pypy environment
      -p PKG, --package PKG
                            name of packages to be uninstalled, default is null
      -i, --ignore-dependencies
                            run in irrecursive mode, i.e. ignore dependencies of
                            installing packages
      -q, --quiet           run in quiet mode, with no output information
      -v, --verbose         run in verbose mode, with more information
      -Y, --yes             yes for all selections

If arguments omit, ``jsuninstall pip`` will stand alone, and do nothing.
To uninstall all packages, use ``-a`` or ``--all`` option. And when
using ``-p`` or ``--package``, if given wrong package name,
``jsuninstall pip`` might give a trivial “did-you-mean” correction.

1. ``brew`` – Homebrew packages

The man page for ``jsuninstall brew`` shows as below.

.. code:: 

    $ jsuninstall brew --help
    usage: jsuninstall brew [-h] [-qv] [-iY] [-f] [-a] [-p PKG]

    Uninstall Installed Homebrew Packages

    optional arguments:
      -h, --help            show this help message and exit
      -a, --all             uninstall all packages installed through Homebrew
      -p PKG, --package PKG
                            name of packages to be uninstalled, default is null
      -f, --force           use "--force" when running `brew uninstall`
      -i, --ignore-dependencies
                            run in irrecursive mode, i.e. ignore dependencies of
                            installing packages
      -q, --quiet           run in quiet mode, with no output information
      -v, --verbose         run in verbose mode, with more information
      -Y, --yes             yes for all selections

If arguments omit, ``jsuninstall brew`` will stand alone, and do
nothing. To uninstall all packages, use ``-a`` or ``--all`` option. And
when using ``-p`` or ``--package``, if given wrong package name,
``jsuninstall brew`` might give a trivial “did-you-mean” correction.

1. ``cask`` – Caskrooom packages

The man page for ``jsuninstall cask`` shows as below.

.. code:: 

    $ jsuninstall cask --help
    usage: jsuninstall cask [-h] [-qv] [-Y] [-f] [-a] [-p PKG]

    Uninstall Installed Caskroom Packages

    optional arguments:
      -h, --help            show this help message and exit
      -a, --all             uninstall all packages installed through Caskroom
      -p PKG, --package PKG
                            name of packages to be uninstalled, default is null
      -f, --force           use "--force" when running `brew cask uninstall`
      -q, --quiet           run in quiet mode, with no output information
      -v, --verbose         run in verbose mode, with more information
      -Y, --yes             yes for all selections

If arguments omit, ``jsuninstall cask`` will stand alone, and do
nothing. To uninstall all packages, use ``-a`` or ``--all`` option. And
when using ``-p`` or ``--package``, if given wrong package name,
``jsuninstall cask`` might give a trivial “did-you-mean” correction.

.. _header-n281:

``jsreinstall``
~~~~~~~~~~~~~~~

``jsreinstall`` is a package manager written in Python 3.6 and Bash 3.2,
which automatically and interactively reinstall packages installed
through --

-  ``brew`` -- `Homebrew <https://brew.sh>`__ packages

-  ``cask`` -- `Caskroom <https://caskroom.github.io>`__ applications

You may install ``jsreinstall`` through ``pip`` of Python (versions
3.\*). And log files can be found in directory
``/Library/Logs/Scripts/reinstall/``. The global man page for
``jsreinstall`` shows as below.

.. code:: 

    $ jsreinstall --help
    usage: jsreinstall [-hV] [-qv] [-f] [-es PKG] [-a] [--[no-]MODE] MODE ...

    Homebrew Package Reinstall Manager

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit
      -a, --all             reinstall all packages installed through Homebrew and
                            Caskroom
      -s START, --startwith START
                            reinstall procedure starts from which package, sort in
                            initial alphabets
      -e START, --endwith START
                            reinstall procedure ends until which package, sort in
                            initial alphabets
      -f, --force           run in force mode, using for `brew reinstall`
      -q, --quiet           run in quiet mode, with no output information
      -v, --verbose         run in verbose mode, with detailed output information

    mode selection:
      MODE                  reinstall packages installed through a specified
                            method, e.g.: brew or cask, or alternatively and
                            simply, cleanup

As it shows, there are two modes in total (if these commands exists).
The default procedure when arguments omit is to stand alone. To
reinstall all packages, you may use one of commands below.

.. code:: 

    $ jsreinstall -a
    $ jsreinstall --all

1. ``brew`` – Homebrew packages

The man page for ``jsreinstall brew`` shows as below.

.. code:: 

    $ jsreinstall brew --help
    usage: jsreinstall brew [-hV] [-qv] [-f] [-se PKG] [-a] [--[no-]MODE] MODE ...

    Reinstall Homebrew Packages

    optional arguments:
      -h, --help            show this help message and exit
      -a, --all             reinstall all packages installed through Homebrew
      -p PKG, --package PKG
                            name of packages to be reinstalled, default is null
      -s START, --startwith START
                            reinstall procedure starts from which package, sort in
                            initial alphabets
      -e START, --endwith START
                            reinstall procedure ends until which package, sort in
                            initial alphabets
      -f, --force           run in force mode, using for `brew reinstall`
      -q, --quiet           run in quiet mode, with no output information
      -v, --verbose         run in verbose mode, with detailed output information

If arguments omit, ``jsreinstall brew`` will stand alone, and do
nothing. To reinstall all packages, use ``-a`` or ``--all`` option. And
when using ``-p`` or ``--package``, if given wrong package name,
``jsreinstall brew`` might give a trivial “did-you-mean” correction.

1. ``cask`` – Caskrooom packages

The man page for ``jsreinstall cask`` shows as below.

.. code:: 

    $ jsreinstall cask --help
    usage: jsreinstall cask [-hV] [-qv] [-se PKG] [-a] [--[no-]MODE] MODE ...

    Reinstall Caskroom Packages

    optional arguments:
      -h, --help            show this help message and exit
      -a, --all             reinstall all packages installed through Caskroom
      -p PKG, --package PKG
                            name of packages to be reinstalled, default is null
      -s START, --startwith START
                            reinstall procedure starts from which package, sort in
                            initial alphabets
      -e START, --endwith START
                            reinstall procedure ends until which package, sort in
                            initial alphabets
      -q, --quiet           run in quiet mode, with no output information
      -v, --verbose         run in verbose mode, with detailed output information

If arguments omit, ``jsreinstall cask`` will stand alone, and do
nothing. To reinstall all packages, use ``-a`` or ``--all`` option. And
when using ``-p`` or ``--package``, if given wrong package name,
``jsreinstall cask`` might give a trivial “did-you-mean” correction.

.. _header-n323:

``jspostinstall``
~~~~~~~~~~~~~~~~~

``jspostinstall`` is a package manager written in Python 3.6 and Bash
3.2, which automatically and interactively postinstall packages
installed through --

-  ``brew`` -- `Homebrew <https://brew.sh>`__ packages

You may install ``jspostinstall`` through ``pip`` of Python (versions
3.\*). And log files can be found in directory
``/Library/Logs/Scripts/postinstall/``. The global man page for
``jspostinstall`` shows as below.

.. code:: 

    $ jspostinstall --help
    usage: jspostinstall [-hV] [-qv] [-eps PKG] [-a] [--no-cleanup]

    Homebrew Package Postinstall Manager

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit
      -a, --all             postinstall all packages installed through Homebrew
      -p PKG, --package PKG
                            name of packages to be postinstalled, default is all
      -s START, --startwith START
                            postinstall procedure starts from which package, sort
                            in initial alphabets
      -e START, --endwith START
                            postinstall procedure ends until which package, sort
                            in initial alphabets
      -q, --quiet           run in quiet mode, with no output information
      -v, --verbose         run in verbose mode, with detailed output information
      --no-cleanup          do not remove postinstall caches & downloads

As it shows, there is only one mode in total (if these commands exists).
To postinstall all packages, you may use one of commands below.

.. code:: 

    $ jspostinstall -a
    $ jspostinstall --all

If arguments omit, ``jspostinstall`` will postinstall all installed
packages of Homebrew. And when using ``-p`` or ``--package``, if given
wrong package name, ``jspostinstall`` might give a trivial
"did-you-mean" correction.

.. _header-n342:

``jsdeps``
~~~~~~~~~~

``jsdeps`` is a package manager written in Python 3.6 and Bash 3.2,
which automatically and interactively show dependencies of packages
installed through --

-  ``pip`` -- Python packages, in both version of 2.7 and 3.6, running
   under `CPython <https://www.python.org>`__ or
   `PyPy <https://pypy.org>`__ compiler, and installed through ``brew``
   or official disk images

-  ``brew`` -- `Homebrew <https://brew.sh>`__ packages

You may install ``jsdeps`` through ``pip`` of Python (versions 3.\*).
And log files can be found in directory
``/Library/Logs/Scripts/dependency/``. The global man page for
``jsdeps`` shows as below.

.. code:: 

    $ jsdeps --help
    usage: jsdeps [-hV] [-t] [-a] [--[no-]MODE] MODE ...

    Trivial Package Dependency Manager

    optional arguments:
      -h, --help     show this help message and exit
      -V, --version  show program's version number and exit
      -a, --all      show dependencies of all packages installed through pip and
                     Homebrew
      -t, --tree     show dependencies as a tree. This feature may request
                     `pipdeptree`

    mode selection:
      MODE           show dependencies of packages installed through a specified
                     method, e.g.: pip or brew

As it shows, there are two mode in total (if these commands exists). The
default procedure when arguments omit is to stand alone. To show
dependency of all packages, you may use one of commands below.

.. code:: 

    $ jsdeps -a
    $ jsdeps --all

1. ``pip`` -- Python packages

As there\'re all kinds and versions of Python complier, along with its
``pip`` package manager. Here, we support showing dependency of
following --

-  Python 2.7/3.6 installed through Python official disk images

-  Python 2.7/3.6 installed through ``brew install python@2/python``

-  PyPy 2.7/3.5 installed through ``brew install pypy/pypy3``

And the man page shows as below.

.. code:: 

    $ jsdeps pip --help
    usage: jsdeps pip [-h] [-qv] [-bcsy] [-V VER] [-a] [-p PKG]

    Show Dependencies of Python Packages

    optional arguments:
      -h, --help            show this help message and exit
      -a, --all             show dependencies of all packages installed through
                            pip
      -v VER, --python_version VER
                            indicate which version of pip will be updated
      -s, --system          show dependencies of pip packages on system level,
                            i.e. python installed through official installer
      -b, --brew            show dependencies of pip packages on Cellar level,
                            i.e. python installed through Homebrew
      -c, --cpython         show dependencies of pip packages on CPython
                            environment
      -y, --pypy            show dependencies of pip packages on PyPy environment
      -p PKG, --package PKG
                            name of packages to be shown, default is all
      -t, --tree            show dependencies as a tree. This feature requests
                            `pipdeptree`

If arguments omit, ``jsdeps pip`` will stand alone, and do nothing. To
show dependency of all packages, use ``-a`` or ``--all`` option. And
when using ``-p`` or ``--package``, if given wrong package name,
``jsdeps pip`` might give a trivial “did-you-mean” correction.

1. ``brew`` – Homebrew packages

The man page for ``jsdeps brew`` shows as below.

.. code:: 

    $ jsdeps brew --help
    usage: jsdeps brew [-h] [-t] [-a] [-p PKG]

    Show Dependencies of Homebrew Packages

    optional arguments:
      -h, --help            show this help message and exit
      -a, --all             show dependencies of all packages installed through
                            Homebrew
      -p PKG, --package PKG
                            name of packages to be shown, default is all
      -t, --tree            show dependencies as a tree

If arguments omit, ``jsdeps brew`` will stand alone, and do nothing. To
show dependency of all packages, use ``-a`` or ``--all`` option. And
when using ``-p`` or ``--package``, if given wrong package name,
``jsdeps brew`` might give a trivial “did-you-mean” correction.

.. _header-n396:

``jslogging``
~~~~~~~~~~~~~

``jslogging`` is a logging manager written in Python 3.6 and Bash 3.2,
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

You may install ``jslogging`` through ``pip`` of Python (versions 3.\*).
And log files can be found in directory
``/Library/Logs/Scripts/logging/``. The global man page for
``jslogging`` shows as below.

.. code:: 

    $ jslogging --help
    usage: logging [-h] [-V] [-a] [-v VER] [-s] [-b] [-c] [-y] [-q]
                   [MODE [MODE ...]]

    Application & Package Logging Manager

    positional arguments:
      MODE                  name of logging mode, could be any from followings,
                            apm, pip, brew, cask, dotapp, macapp, or appstore

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit
      -a, --all             log applications and packages of all entries
      -v VER, --python_version VER
                            indicate which version of pip will be logged
      -s, --system          log pip packages on system level, i.e. python
                            installed through official installer
      -b, --brewed          log pip packages on Cellar level, i.e. python
                            installed through Homebrew
      -c, --cpython         log pip packages on CPython environment
      -y, --pypy            log pip packages on PyPy environment
      -q, --quiet           run in quiet mode, with no output information

As it shows, there are seven mode in total (if these commands exists),
and you may call **multiple** modes at one time. The default procedure
when arguments omit is to stand alone. To log all entries, you may use
one of commands below.

.. code:: 

    $ jslogging -a
    $ jslogging --all
    $ jslogging apm pip brew cask dotapp macapp appstore

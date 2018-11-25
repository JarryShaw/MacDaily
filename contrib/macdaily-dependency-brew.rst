========================
macdaily-dependency-brew
========================

---------------------------------
Homebrew Formula Dependency Query
---------------------------------

:Version: v2018.11.25
:Date: November 24, 2018
:Manual section: 1
:Author:
    Jarry Shaw, a newbie programmer, is the author, owner and maintainer
    of *MacDaily*. Please contact me at *jarryshaw@icloud.com*.
:Copyright:
    *MacDaily* is licensed under the **GNU General Public License v3.0**.

SYNOPSIS
========

macdaily **dependency** *brew* [*options*] <*formulae*> ...

OPTIONS
=======

optional arguments
------------------

-h, --help            show this help message and exit
-V, --version         show program's version number and exit

specification arguments
-----------------------

-b, --include-build   include the *:build* type dependencies

-o, --include-optional
                      include *:optional* dependencies

-t, --include-test    include (non-recursive) *:test* dependencies

-s, --skip-recommended
                      skip *:recommended* type dependencies

-r, --include-requirements
                      include requirements in addition to dependencies

-p *FORM* [*FORM* ...], --packages *FORM* [*FORM* ...]
                      name of Homebrew formulae to query

general arguments
-----------------

-a, --all             query all Homebrew formulae installed through Homebrew
-q, --quiet           run in quiet mode, with no output information
-v, --verbose         run in verbose mode, with detailed output information
-n, --no-cleanup      do not run cleanup process
-f, --tree            show dependencies as a tree [requires *DictDumper*]
-g, --topological     show dependencies in topological order

-d *LEVEL*, --depth *LEVEL*
                      max display depth of the dependency tree

SEE ALSO
========

* ``brew(1)``
* ``macdaily-dependency``
* ``macdaily-dependency-pip``

=======================
macdaily-reinstall-cask
=======================

-----------------------------------
Automated Homebrew Cask Reinstaller
-----------------------------------

:Version: v2019.01.24
:Date: November 24, 2018
:Manual section: 1
:Author:
    Jarry Shaw, a newbie programmer, is the author, owner and maintainer
    of *MacDaily*. Please contact me at *jarryshaw@icloud.com*.
:Copyright:
    *MacDaily* is licensed under the **Apple Open Source License**.

SYNOPSIS
========

macdaily **reinstall** *cask* [*options*] <*casks*> ...

OPTIONS
=======

optional arguments
------------------

-h, --help            show this help message and exit
-V, --version         show program's version number and exit

specification arguments
-----------------------

-s *PREFIX*, --startswith *PREFIX*
                      reinstall procedure starts from such binary, sort in
                      initial alphabets

-e *SUFFIX*, --endswith *SUFFIX*
                      reinstall procedure ends after such binary, sort in
                      initial alphabets

-f, --force           reinstall even if the Cask does not appear to be
                      present
-t, --no-quarantine   prevent Gatekeeper from enforcing its security

-p *CASK* [*CASK* ...], --packages *CASK* [*CASK* ...]
                      name of Caskroom binaries to reinstall

general arguments
-----------------

-a, --all             reinstall all Homebrew formulae installed through
                      Homebrew
-q, --quiet           run in quiet mode, with no output information
-v, --verbose         run in verbose mode, with detailed output information
-y, --yes             yes for all selections
-n, --no-cleanup      do not run cleanup process

miscellaneous arguments
-----------------------

-L *ARG*, --logging *ARG*
                      options for ``brew cask list`` command

-R *ARG*, --reinstall *ARG*
                      options for ``brew cask reinstall <cask>`` command

SEE ALSO
========

* ``brew-cask(1)``
* ``macdaily-reinstall``
* ``macdaily-reinstall-brew``

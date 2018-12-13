:Command Executable:
    ``macdaily help`` | ``md-help``
:Supported Commands:
    all MacDaily commands and subsidiaries

=================================
MacDaily Usage Information Manual
=================================

- `About <#about>`__
- `Usage <#usage>`__
- `TODO <#todo>`__

--------------

About
-----

MacDaily provides a collection of revised manuals to help users dig into.
MacDaily ``help`` command will lead you to these
`man pages <https://en.wikipedia.org/wiki/man_page>`__, which are generated
by ``rst2man.py`` from |docutils|_ and displayed with ``man(1)``.

.. |docutils| replace:: ``docutils``
.. _docutils: http://docutils.sourceforge.net

Usage
-----

.. code:: man

    usage: macdaily help [options] <cmd-selection> ...

    MacDaily Usage Information Manual

    optional arguments:
    -h, --help     show this help message and exit
    -V, --version  show program's version number and exit

    specification arguments:
    CMD            display manual information about such command

    aliases: doc, man

TODO
----

- ✔️ reconstruct help CLI
- ❌ implement and revise man pages

:Command Executable:
    ``macdaily launch`` | ``md-launch``
:Supported Commands:
    ``askpass``, ``confirm``

=================================
MacDaily Dependency Launch Helper
=================================

- `About <#about>`__
- `Usage <#usage>`__
- `Programs <#programs>`__

  - `Askpass Helper Program <#askpass>`__
  - `Confirm Helper Program <#confirm>`__

- `TODO <#todo>`__

--------------

About
-----

MacDaily depends on several homemade helper programs, i.e. |askpass|_ and
|confirm|_. MacDaily ``launch`` command will help initialise and launch these
helper programs.

Usage
-----

.. code:: man

    usage: macdaily launch [-h] [-V] [-a] [-q] [-v] [PROG [PROG ...]]

    MacDaily Dependency Launch Helper

    optional arguments:
      -h, --help     show this help message and exit
      -V, --version  show program's version number and exit

    specification arguments:
      PROG           helper program to launch, choose from  'askpass' and
                     'confirm'

    general arguments:
      -a, --all      launch all help programs, i.e.  'askpass' and
                     'confirm'
      -q, --quiet    run in quiet mode, with no output information
      -v, --verbose  run in verbose mode, with detailed output information

    aliases: init

Programs
--------

.. raw:: html

    <h4>
      <a name="askpass">
        Askpass Helper Program
      </a>
    </h4>

.. code:: man

    macdaily-askpass [-h|--help] [prompt]

MacDaily ``askpass`` helper program locates at
``macdaily/res/askpass.applescript`` by default. It is to be set as
``SUDO_ASKPASS`` environment variable and used with ``sudo --askpass`` command
(c.f. ``sudo(8)`` and ``sudo.conf(5)``).

.. image:: https://github.com/JarryShaw/MacDaily/blob/dev/doc/img/askpass.png

.. raw:: html

    <h4>
      <a name="confirm">
        Confirm Helper Program
      </a>
    </h4>

.. code:: man

    macdaily-confirm [-h|--help] [prompt]

MacDaily ``confirm`` helper program locates at
``macdaily/res/confirm.applescript`` by default. It is to help MacDaily ask for
confirmation when ``stdin`` is not available.

.. image:: https://github.com/JarryShaw/MacDaily/blob/dev/doc/img/confirm.png

TODO
----

- ✔️ reconstruct logging CLI
- ❌ considering implement more helper programs

.. |askpass| replace:: ``askpass``
.. _askpass: #askpass
.. |confirm| replace:: ``confirm``
.. _confirm: #confirm

=======
Confirm
=======

The ``confirm`` utility for macOS. Originally inspired from the work of
`@theseal <https://github.com/theseal/ssh-askpass>`__, it is now also an
important component `MacDaily <https://github.com/JarryShaw/MacDaily>`__.

Usage
=====

.. code:: shell

    confirm [-h|--help] [prompt]

.. image:: https://github.com/JarryShaw/Confirm/blob/master/sample/confirm.png

Installation
============

Homebrew
--------

.. code:: shell

    $ brew tap jarryshaw/tap
    $ brew install confirm
    # or simply, a one-liner
    $ brew install jarryshaw/tap/confirm

Manually
--------

.. code:: shell

    $ sudo cp confirm /usr/local/bin/

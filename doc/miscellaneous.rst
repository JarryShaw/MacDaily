================
Developer Manual
================

- `Project Structure <#repo>`__
- `Command Classes <#cmd>`__
- `Miscellaneous Utilities <#util>`__

  - `ANSI Sequences <#color>`__
  - `Print Utilities <#print>`__
  - |script|_

- `TODO <#todo>`__

.. |script| replace:: UNIX ``script``
.. _script: #script

--------------

.. raw:: html

    <h3>
      <a name="repo">
        Project Structure
      </a>
    </h3>

+-----------+-------------------------------------------------------------+
| Submodule |                         Description                         |
+===========+=============================================================+
| ``api``   | core API for each *verbal command*                          |
+-----------+-------------------------------------------------------------+
| ``cli``   | core CLI for each *verbal command*                          |
+-----------+-------------------------------------------------------------+
| ``cls``   | detailed implementation of each **specific verbal command** |
+-----------+-------------------------------------------------------------+
| ``cmd``   | base implementation of each *verbal command*                |
+-----------+-------------------------------------------------------------+
| ``core``  | base implementation of each *specific command*              |
+-----------+-------------------------------------------------------------+
| ``util``  | miscellaneous utilities                                     |
+-----------+-------------------------------------------------------------+

NB
    Commands are considered as *verbal* and *specific*. Say
    ``UpdateCommand`` is a *verbal command*, ``PipCommand``
    is a *specific command*, and ``PipUpdate`` is a
    **specific verbal command** with detailed implementation.

.. raw:: html

    <h3>
      <a name="cmd">
        Command Classes
      </a>
    </h3>

With support of |abc|_, MacDaily implemented an *abstract basic command*,
which indicates default work flow and several reusable functions. Work
flow of MacDaily commands is as below.

.. |abc| replace:: Python ``abc`` module
.. _abc: https://docs.python.org/3/library/abc.html

1. check executable

   1. if none exits, exit
   2. else continue

2. parse options and packages

   1. merge package specification in options
   2. extract command line options
   3. if no package specifications and ``all`` flag **NOT** set, exit
   4. else continue

3. locate executables
4. run command-specified processors

   1. for each executable

      1. command-specified logging process (*optional*)

         1. fetch packages for main process
         2. if found package specifications, provide trivial did-you-mean
            function
         3. else continue

      2. ask for comfirmation on main process

         1. if cancelled, exit
         2. else continue

      3. command-specified main process

         1. run main process for each package
         2. run checkout process (*optional*)

   2. run cleanup process (*optional*)

Also, MacDaily commands have all kinds of properties to help incorporate
detailed implementations. These properties are listed below.

+-----------------------+-----------------------+------------------------------------------------------------------+
|       Property        |         Type          |                           Description                            |
+=======================+=======================+==================================================================+
| ``cmd``               | ``str``               | *verbal* command type                                            |
+-----------------------+-----------------------+------------------------------------------------------------------+
| ``act``               | ``tuple<str>``        | command actions                                                  |
+-----------------------+-----------------------+------------------------------------------------------------------+
| ``act[0]``            | ``str``               | *verb* action                                                    |
+-----------------------+-----------------------+------------------------------------------------------------------+
| ``act[1]``            | ``str``               | *verb* (*past participle*) action                                |
+-----------------------+-----------------------+------------------------------------------------------------------+
| ``act[2]``            | ``str``               | *adjective* action                                               |
+-----------------------+-----------------------+------------------------------------------------------------------+
| ``job``               | ``tuple<str>``        | command jobs                                                     |
+-----------------------+-----------------------+------------------------------------------------------------------+
| ``job[0]``            | ``str``               | *singular* job                                                   |
+-----------------------+-----------------------+------------------------------------------------------------------+
| ``job[1]``            | ``str``               | *plural* job                                                     |
+-----------------------+-----------------------+------------------------------------------------------------------+
| ``name``              | ``str``               | command name (**full name**)                                     |
+-----------------------+-----------------------+------------------------------------------------------------------+
| ``mode``              | ``str``               | command mode (**acronym**)                                       |
+-----------------------+-----------------------+------------------------------------------------------------------+
| ``time``              | ``float`` / ``None``  | `Homebrew <https://brew.sh>`__ renew (``brew update``) timestamp |
+-----------------------+-----------------------+------------------------------------------------------------------+
| ``desc``              | ``tuple<str>``        | command descriptions                                             |
+-----------------------+-----------------------+------------------------------------------------------------------+
| ``desc[0]``           | ``str``               | *singular* description                                           |
+-----------------------+-----------------------+------------------------------------------------------------------+
| ``desc[1]``           | ``str``               | *plural* description                                             |
+-----------------------+-----------------------+------------------------------------------------------------------+
| ``packages``          | ``set<str>``          | process succeeded packages                                       |
+-----------------------+-----------------------+------------------------------------------------------------------+
| ``failed``            | ``set<str>``          | process failed packages                                          |
+-----------------------+-----------------------+------------------------------------------------------------------+
| ``ignored``           | ``set<str>``          | ignored packages (*specified in options*)                        |
+-----------------------+-----------------------+------------------------------------------------------------------+
| ``notfound``          | ``set<str>``          | unknown packages (*not found in registry*)                       |
+-----------------------+-----------------------+------------------------------------------------------------------+

.. raw:: html

    <h3>
      <a name="util">
        Miscellaneous Utilities
      </a>
    </h3>

+--------------------------+------------------------------+
|         Submodule        |          Description         |
+==========================+==============================+
| ``macdaily.util.compat`` | compatibility support        |
+--------------------------+------------------------------+
| ``macdaily.util.const``  | collection of contant macros |
+--------------------------+------------------------------+
| ``macdaily.util.error``  | user refined exceptions      |
+--------------------------+------------------------------+
| ``macdaily.util.tools``  | utility functions            |
+--------------------------+------------------------------+

Version string, terminal commands, environment macros,
`ANSI <https://en.wikipedia.org/wiki/ANSI_escape_code>`__
strings and etc. can be found in ``macdaily.util.const``. Further
information please refer to `ANSI Sequences <#color>`__
section.

+--------------------------------+------------------------------+
|            Submodule           |          Description         |
+================================+==============================+
| ``macdaily.util.const.macro``  | collection of contant macros |
+--------------------------------+------------------------------+
| ``macdaily.util.const.string`` | ``maxstr`` & ``minstr``      |
+--------------------------------+------------------------------+
| ``macdaily.util.const.term``   | terminal display ANSI codes  |
+--------------------------------+------------------------------+

For ``macdaily.util.error``, three user refined exceptions,
``ModeError`` (derived from ``NameError``), ``UnsupportedOS``
(derived from ``RuntimeError``) and ``ConfigNotFoundError``
(derived from ``FileNotFoundError``), are derived from
``Error``, an ``Exception`` class that silence the error
traceback.

And in ``macdaily.util.tools``, various miscellaneous utility
functions are defined. Further information please refer to
`Print Utilities <#print>`__ and |script|_ sections.

+--------------------------------+------------------------------+
|           Submodule            |          Description         |
+================================+==============================+
| ``macdaily.util.tools.deco``   | decorators                   |
+--------------------------------+------------------------------+
| ``macdaily.util.tools.get``    | ``get`` utilities            |
+--------------------------------+------------------------------+
| ``macdaily.util.tools.make``   | ``make`` utilities           |
+--------------------------------+------------------------------+
| ``macdaily.util.tools.misc``   | miscellaneous util functions |
+--------------------------------+------------------------------+
| ``macdaily.util.tools.print``  | ``print`` utilities          |
+--------------------------------+------------------------------+
| ``macdaily.util.tools.script`` | UNIX ``script`` utilities    |
+--------------------------------+------------------------------+

.. raw:: html

    <h4>
      <a name="color">
        ANSI Sequences
      </a>
    </h4>

+-------------------+-----------------+--------------------------+
|        Name       |      Value      |       Description        |
+===================+=================+==========================+
| ``reset``         | ``'\033[0m'``   | reset                    |
+-------------------+-----------------+--------------------------+
| ``bold``          | ``'\033[1m'``   | bold                     |
+-------------------+-----------------+--------------------------+
| ``dim``           | ``'\033[2m'``   | dim                      |
+-------------------+-----------------+--------------------------+
| ``under``         | ``'\033[4m'``   | underline                |
+-------------------+-----------------+--------------------------+
| ``flash``         | ``'\033[5m'``   | flash                    |
+-------------------+-----------------+--------------------------+
| ``red_dim``       | ``'\033[31m'``  | dim red foreground       |
+-------------------+-----------------+--------------------------+
| ``green_dim``     | ``'\033[32m'``  | dim green foreground     |
+-------------------+-----------------+--------------------------+
| ``yellow_dim``    | ``'\033[33m'``  | dim yellow foreground    |
+-------------------+-----------------+--------------------------+
| ``purple_dim``    | ``'\033[34m'``  | dim purple foreground    |
+-------------------+-----------------+--------------------------+
| ``pink_dim``      | ``'\033[35m'``  | dim pink foreground      |
+-------------------+-----------------+--------------------------+
| ``blue_dim``      | ``'\033[36m'``  | dim blue foreground      |
+-------------------+-----------------+--------------------------+
| ``red_bg_dim``    | ``'\033[41m'``  | dim red background       |
+-------------------+-----------------+--------------------------+
| ``green_bg_dim``  | ``'\033[42m'``  | dim green background     |
+-------------------+-----------------+--------------------------+
| ``yellow_bg_dim`` | ``'\033[43m'``  | dim yellow background    |
+-------------------+-----------------+--------------------------+
| ``purple_bg_dim`` | ``'\033[44m'``  | dim purple background    |
+-------------------+-----------------+--------------------------+
| ``pink_bg_dim``   | ``'\033[45m'``  | dim pink background      |
+-------------------+-----------------+--------------------------+
| ``blue_bg_dim``   | ``'\033[46m'``  | dim blue background      |
+-------------------+-----------------+--------------------------+
| ``grey``          | ``'\033[90m'``  | bright grey foreground   |
+-------------------+-----------------+--------------------------+
| ``red``           | ``'\033[91m'``  | bright red foreground    |
+-------------------+-----------------+--------------------------+
| ``green``         | ``'\033[92m'``  | bright green foreground  |
+-------------------+-----------------+--------------------------+
| ``yellow``        | ``'\033[93m'``  | bright yellow foreground |
+-------------------+-----------------+--------------------------+
| ``purple``        | ``'\033[94m'``  | bright purple foreground |
+-------------------+-----------------+--------------------------+
| ``pink``          | ``'\033[95m'``  | bright pink foreground   |
+-------------------+-----------------+--------------------------+
| ``blue``          | ``'\033[96m'``  | bright blue foreground   |
+-------------------+-----------------+--------------------------+
| ``grey_bg``       | ``'\033[100m'`` | bright grey background   |
+-------------------+-----------------+--------------------------+
| ``red_bg``        | ``'\033[101m'`` | bright red background    |
+-------------------+-----------------+--------------------------+
| ``green_bg``      | ``'\033[102m'`` | bright green background  |
+-------------------+-----------------+--------------------------+
| ``yellow_bg``     | ``'\033[103m'`` | bright yellow background |
+-------------------+-----------------+--------------------------+
| ``purple_bg``     | ``'\033[104m'`` | bright purple background |
+-------------------+-----------------+--------------------------+
| ``pink_bg``       | ``'\033[105m'`` | bright pink background   |
+-------------------+-----------------+--------------------------+
| ``blue_bg``       | ``'\033[106m'`` | bright blue background   |
+-------------------+-----------------+--------------------------+

.. raw:: html

    <h4>
      <a name="print">
        Print Utilities
      </a>
    </h4>

MacDaily defines several ``print`` functions to better make prompts
using `emoji <https://en.wikipedia.org/wiki/Emoji>`__ and
`ANSI escape code <https://en.wikipedia.org/wiki/ANSI_escape_code>`__.

.. code:: python

    print_info(text, file, redirect=False)
    print_misc(text, file, redirect=False)
    print_scpt(text, file, redirect=False)
    print_term(text, file, redirect=False)
    print_text(text, file, redirect=False)

- ``text`` -- ``str``, text to print
- ``file`` -- ``str``, log file name
- ``redirect`` -- ``bool``, redirect flag; if ``True``, redirect ``stdout`` to
  ``/dev/null``

.. raw:: html

    <h4>
      <a name="script">
        UNIX <code>script</code>
      </a>
    </h4>

As |UNIX script utility|_ designed, it is to
*make typescript of terminal session*. The MacDaily ``script``
function makes a typescript of everything printed on your terminal.
It is, as suggests in |Python pty module|_, implemented with support
of pseudo-terminal (PTY).

.. |UNIX script utility| replace:: UNIX ``script`` utility
.. _UNIX script utility: https://en.wikipedia.org/wiki/Script_(Unix)
.. |Python pty module| replace:: Python ``pty`` module
.. _Python pty module: https://docs.python.org/3/library/pty.html#example

Since ``pty`` module in Python standard library has minor bugs with process
termination on macOS. Thus, |ptyng|_ is introduced. ``ptyng`` module revised
``pty.spawn`` function, automatically terminate child process once it is
a zombie ('dead' in other words) and return from function call as
normal/trivial scenerios expected.

.. |ptyng| replace:: ``ptyng``
.. _ptyng: https://github.com/JarryShaw/ptyng

Another issue, however, is found when trying to implement a |UNIX yes utility|_
by using a user refined ``stdin_read`` function for ``pty.spawn``. When running
in terminal (TTY), the pseudo-input function is only called until a keyboard
event occurred.

.. |UNIX yes utility| replace:: UNIX ``yes`` utility
.. _UNIX yes utility: https://en.wikipedia.org/wiki/Yes_(Unix)

Considering such issue, the automation tool |expect|_ is then introduced.
Within ``expect``, ``unbuffer``, an alternative of UNIX ``script`` utility, is
provided. With support of ``unbuffer``, the issue above is truly resolved.

And for better readability, MacDaily will strip all
`ANSI escape code <https://en.wikipedia.org/wiki/ANSI_escape_code>`__ and use
``col -b`` to trim backspaces from the output when writing into *typescript*.
Also, to distinguish MacDaily program information and other output, MacDaily
will add ANSI sequence ``'\033[2m'`` (faint, decreased intensity) to the
latter.

.. code:: python

    script(argv=SHELL, file='typescript', *, password=None, yes=None, prefix=None,
           redirect=False, timeout=None, shell=False, executable=SHELL, suffix=None)

.. raw:: html

    <blockquote>
      Utility function works as UNIX <code>script</code> utility.
    </blockquote>

- ``argv`` -- string, or a sequence of program arguments
- ``file`` -- saves all dialogue in file
- ``shell`` -- if ``True``, the command will be executed through the shell
- ``executable`` -- a replacement program to execute
- ``timeout`` -- an integral timeout interval
- ``redirect`` -- if ``True``, the command will redirect ``stdout`` to
  ``/dev/null``
- ``password`` -- string to be consealed in dialogue
- ``yes`` -- string to be used as ``yes expletive`` in UNIX ``yes`` utility
- ``prefix`` -- string as the prefix of program arguments
- ``suffix`` -- string as the suffix of program arguments

NB
    There are three different core functions for the ``script`` function.
    Please always make sure that one of these functions are available for
    MacDaily.

When |expect|_ installed and ``unbuffer`` found in ``PATH``, MacDaily will use
``unbuffer`` as core function. Otherwise if UNIX ``script`` utility found in
``PATH``, it will be used. For the worst case, a ``ptyng`` based function
will be used. Corresponding commands of each core function are listed as below.

+--------------+-----------------------------------------------------------------------------------+
|     Core     |                                      Command                                      |
+==============+===================================================================================+
| ``unbuffer`` | ``[prefix] [yes expletive |] unbuffer -p ${argv} [suffix]``                       |
+--------------+-----------------------------------------------------------------------------------+
|  ``script``  | ``[prefix] script -q /dev/null ${SHELL} -c "[yes expletive |] ${argv} [suffix]"`` |
+--------------+-----------------------------------------------------------------------------------+
|  ``ptyng``   | ``ptyng.spawn(argv, master_read, stdin_read, timeout=timeout)``                   |
+--------------+-----------------------------------------------------------------------------------+

.. code:: python

    run(argv, file, *, redirect=False, password=None, yes=None, shell=False,
        prefix=None, suffix=None, timeout=None, executable=SHELL, verbose=False)

.. raw:: html

    <blockquote>
      Call <code>script</code> function with given arguments.
    </blockquote>

- ``redirect`` -- if ``True``, append ``> /dev/null`` to ``suffix``
- ``verbose`` -- if ``True``, output error traceback (if any) to ``stdout``
- all other arguments are the same as for ``script`` function

.. code:: python

    sudo(argv, file, password, *, askpass=None, sethome=False, yes=None,
         redirect=False, verbose=False, timeout=None, executable=SHELL, suffix=None)

.. raw:: html

    <blockquote>
      Call <code>run</code> function with given arguments.
    </blockquote>

- ``askpass`` -- executable path of askpass helper program (``SUDO_ASKPASS``)
- ``sethome`` -- if ``True``, call ``sudo`` with ``--set-home`` option
- all other arguments are the same as described in ``run`` function

NB
    When using ``sudo`` function, ``shell`` argument will always set to
    ``True``.

If running as ``root`` (System Administrator), ``prefix`` will be unset.
And when using ``unbuffer`` or ``ptyng`` as core function, ``yes`` argument
will be unset. Corrresponding ``prefix`` argument of each core function
are listed as below.

+--------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|     Core     |                                                                                        ``prefix``                                                                                        |
+==============+==========================================================================================================================================================================================+
| ``unbuffer`` | ``[yes expletive |] echo 'password' | sudo --stdin --validate --prompt='Password\n' && [SUDO_ASKPASS='askpass'] sudo [--set-home] [--askpass --prompt='Enter your password for USER.']`` |
+--------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|  ``script``  | ``echo 'password' | sudo --stdin --validate --prompt='Password\n' && [SUDO_ASKPASS='askpass'] sudo [--set-home] [--askpass --prompt='Enter your password for USER.']``                   |
+--------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|  ``ptyng``   | ``echo 'password' | sudo --stdin --validate --prompt='Password\n' && [SUDO_ASKPASS='askpass'] sudo [--set-home] [--askpass --prompt='Enter your password for USER.']``                   |
+--------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

.. |expect| replace:: ``expect``
.. _expect: https://core.tcl.tk/expect

TODO
----

- ✔️ implementation
- ✔️ documentation

# jsdaily

Some useful daily utility scripts.

* [`update`](#update)
    - [Atom](#update_apm)
    - [Python](#update_pip)
    - [Homebrew](#update_brew)
    - [Caskroom](#update_cask)
    - [App Store](#update_apptore)
* [`uninstall`](#uninstall)
    - [Python](#uninstall_pip)
    - [Homebrew](#uninstall_brew)
    - [Caskroom](#uninstall_cask)
* [`reinstall`](#reinstall)
    - [Homebrew](#reinstall_brew)
    - [Caskroom](#reinstall_cask)
* [`postinstall`](#postinstall)
    - [Homebrew](#postinstall_brew)
* [`dependency`](#dependency)
    - [Python](#dependency_pip)
    - [Homebrew](#dependency_brew)

---

&nbsp;

<a name="update"> </a>

##### `update`

&emsp; `update` is a package manager written in Python 3.6 and Bash 3.2, which automatically update all packages installed through ——

  - `apm` -- Atom packages
  - `pip` -- Python packages, in both version of 2.7 and 3.6, running under [CPython](https://www.python.org) or [PyPy](https://pypy.org) compiler, and installed through `brew` or official disk images
  - `brew` -- [Homebrew](https://brew.sh) packages
  - `cask` -- [Caskroom](https://caskroom.github.io) applications
  - `appstore` -- Mac App Store or `softwareupdate` installed applications

&emsp; You may install `update` through `pip` of Python (versions 3.\*). And log files can be found in directory `/Library/Logs/Scripts/update/`. The global man page for `update` shows as below.

```
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
```

&emsp; As it shows, there are five modes in total (if these commands exists). To update all packages, you may use one of commands below.

```
$ update
$ update -a
$ update --all
```

<a name="update_apm"> </a>

1. `apm` -- Atom packages

&emsp; [Atom](https://atom.io) provides a package manager called `apm`, i.e. "Atom Package Manager". The man page for `update apm` shows as below.

```
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
```

&emsp; If arguments omit, `update apm` will update all outdated packages of Atom. And when using `-p` or `--package`, if given wrong package name, `update apm` might give a trivial "did-you-mean" correction.

<a name="update_pip"> </a>

2. `pip` -- Python packages

&emsp; As there\'re all kinds and versions of Python complier, along with its `pip` package manager. Here, we support update of following ——

 - Python 2.7/3.6 installed through Python official disk images
 - Python 2.7/3.6 installed through `brew install python/python3`
 - PyPy 2.7/3.5 installed through `brew install pypy/pypy3`

And the man page shows as below.

```
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
```

&emsp; If arguments omit, `update pip` will update all outdated packages in all copies of Python. And when using `-p` or `--package`, if given wrong package name, `update pip` might give a trivial "did-you-mean" correction.

<a name="update_brew"> </a>

3. `brew` -- Homebrew packages

&emsp; The man page for `update brew` shows as below.

```
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
```

&emsp; Note that, arguments `-f` and `--force`, `-m` and `--merge` are using only for `brew update` command.

&emsp; If arguments omit, `update brew` will update all outdated packages of Homebrew. And when using `-p` or `--package`, if given wrong package name, `update brew` might give a trivial "did-you-mean" correction.

<a name="update_cask"> </a>

4. `cask` -- Caskrooom packages

&emsp; The man page for `update cask` shows as below.

```
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
```

&emsp; Note that, arguments `-f` and `--force`, `-g` and `--greedy` are using only for `brew cask upgrade` command. And when latter given, `update` will directly run `brew cask upgrade --greedy`.

&emsp; If arguments omit, `update cask` will update all outdated packages of Caskroom. And when using `-p` or `--package`, if given wrong package name, `update cask` might give a trivial "did-you-mean" correction.

<a name="update_appstore"> </a>

5. `appstore` -- Mac App Store packages

&emsp; The man page for `update appstore` shows as below.

```
$ update appstore --help
usage: update appstore [-h] [-a] [-p PKG] [-q]

Update installed App Store packages.

optional arguments:
  -h, --help            show this help message and exit
  -a, --all             Update all packages installed through App Store.
  -p PKG, --package PKG
                        Name of packages to be updated, default is all.
  -q, --quiet           Run in quiet mode, with no output information.
```

&emsp; If arguments omit, `update appstore` will update all outdated packages in Mac App Store or `softwareupdate`. And when using `-p` or `--package`, if given wrong package name, `update appstore` might give a trivial "did-you-mean" correction.


&nbsp;

<a name="uninstall"> </a>

##### `uninstall`

&emsp; `uninstall` is a package manager written in Python 3.6 and Bash 3.2, which recursively and interactively uninstall packages installed through ——

  - `pip` -- Python packages, in both version of 2.7 and 3.6, running under [CPython](https://www.python.org) or [PyPy](https://pypy.org) compiler, and installed through `brew` or official disk images
  - `brew` -- [Homebrew](https://brew.sh) packages
  - `cask` -- [Caskroom](https://caskroom.github.io) applications

&emsp; You may install `uninstall` through `pip` of Python (versions 3.\*). And log files can be found in directory `/Library/Logs/Scripts/uninstall/`. The global man page for `uninstall` shows as below.

```
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
```

&emsp; As it shows, there are three modes in total (if these commands exists). The default procedure when arguments omit is to stand alone. To uninstall all packages, you may use one of commands below.

```
$ uninstall -a
$ uninstall --all
```

<a name="uninstall_pip"> </a>

1. `pip` -- Python packages

&emsp; As there're several kinds and versions of Python complier, along wiht its `pip` package manager. Here, we support uninstall procedure in following ——

 * Python 2.7/3.6 installed through Python official disk images
 * Python 2.7/3.6 installed through `brew install python/python3`
 * PyPy 2.7/3.5 installed through `brew install pypy/pypy3`

&emsp; And the man page shows as below.

```
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
```

&emsp; If arguments omit, `uninstall pip` will stand alone, and do nothing. To uninstall all packages, use `-a` or `--all` option. And when using `-p` or `--package`, if given wrong package name, `uninstall pip` might give a trivial “did-you-mean” correction.

<a name="uninstall_brew"> </a>

2. `brew` – Homebrew packages

&emsp; The man page for `uninstall brew` shows as below.

```
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
```

&emsp; If arguments omit, `uninstall brew` will stand alone, and do nothing. To uninstall all packages, use `-a` or `--all` option. And when using `-p` or `--package`, if given wrong package name, `uninstall brew` might give a trivial “did-you-mean” correction.

<a name="uninstall_cask"> </a>

3. `cask` – Caskrooom packages

&emsp; The man page for `uninstall cask` shows as below.

```
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
```

&emsp; If arguments omit, `uninstall cask` will stand alone, and do nothing. To uninstall all packages, use `-a` or `--all` option. And when using `-p` or `--package`, if given wrong package name, `uninstall cask` might give a trivial “did-you-mean” correction.

&nbsp;

<a name="reinstall"> </a>

##### `reinstall`

&emsp; `reinstall` is a package manager written in Python 3.6 and Bash 3.2, which automatically and interactively reinstall packages installed through ——

  - `brew` -- [Homebrew](https://brew.sh) packages
  - `cask` -- [Caskroom](https://caskroom.github.io) applications

&emsp; You may install `reinstall` through `pip` of Python (versions 3.\*). And log files can be found in directory `/Library/Logs/Scripts/reinstall/`. The global man page for `reinstall` shows as below.

```
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
```

&emsp; As it shows, there are two modes in total (if these commands exists). The default procedure when arguments omit is to stand alone. To reinstall all packages, you may use one of commands below.

```
$ reinstall -a
$ reinstall --all
```

<a name="reinstall_brew"> </a>

1. `brew` – Homebrew packages

&emsp; The man page for `reinstall brew` shows as below.

```
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
```

&emsp; If arguments omit, `reinstall brew` will stand alone, and do nothing. To reinstall all packages, use `-a` or `--all` option. And when using `-p` or `--package`, if given wrong package name, `reinstall brew` might give a trivial “did-you-mean” correction.

<a name="reinstall_cask"> </a>

2. `cask` – Caskrooom packages

&emsp; The man page for `reinstall cask` shows as below.

```
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
```

&emsp; If arguments omit, `reinstall cask` will stand alone, and do nothing. To reinstall all packages, use `-a` or `--all` option. And when using `-p` or `--package`, if given wrong package name, `reinstall cask` might give a trivial “did-you-mean” correction.

&nbsp;

<a name="postinstall"> </a>

##### `postinstall`

&nbsp; `postinstall` is a package manager written in Python 3.6 and Bash 3.2, which automatically and interactively reinstall packages installed through ——

  - `brew` -- [Homebrew](https://brew.sh) packages

&emsp; You may install `postinstall` through `pip` of Python (versions 3.\*). And log files can be found in directory `/Library/Logs/Scripts/postinstall/`. The global man page for `postinstall` shows as below.

```
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
```

&emsp; As it shows, there is only one mode in total (if these commands exists). To postinstall all packages, you may use one of commands below.

```
$ postinstall
$ postinstall -a
$ postinstall --all
```

<a name="postinstall_brew"> </a>

&emsp; If arguments omit, `postinstall` will postinstall all installed packages of Homebrew. And when using `-p` or `--package`, if given wrong package name, `postinstall` might give a trivial "did-you-mean" correction.

<a name="dependency"> </a>

##### `dependency`

&nbsp; `dependency` is a package manager written in Python 3.6 and Bash 3.2, which automatically and interactively show dependencies of packages installed through ——

  - `pip` -- Python packages, in both version of 2.7 and 3.6, running under [CPython](https://www.python.org) or [PyPy](https://pypy.org) compiler, and installed through `brew` or official disk images
  - `brew` -- [Homebrew](https://brew.sh) packages

&emsp; You may install `dependency` through `pip` of Python (versions 3.\*). And log files can be found in directory `/Library/Logs/Scripts/dependency/`. The global man page for `dependency` shows as below.

```
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
```

&emsp; As it shows, there are two mode in total (if these commands exists). The default procedure when arguments omit is to stand alone. To show dependency of all packages, you may use one of commands below.

```
$ dependency -a
$ dependency --all
```

<a name="dependency_pip"> </a>

1. `pip` -- Python packages

&emsp; As there\'re all kinds and versions of Python complier, along with its `pip` package manager. Here, we support showing dependency of following ——

 - Python 2.7/3.6 installed through Python official disk images
 - Python 2.7/3.6 installed through `brew install python/python3`
 - PyPy 2.7/3.5 installed through `brew install pypy/pypy3`

And the man page shows as below.

```
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
```

&emsp; If arguments omit, `dependency pip` will stand alone, and do nothing. To show dependency of all packages, use `-a` or `--all` option. And when using `-p` or `--package`, if given wrong package name, `dependency pip` might give a trivial “did-you-mean” correction.

<a name="dependency_brew"> </a>

2. `brew` – Homebrew packages

&emsp; The man page for `dependency brew` shows as below.

```
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
```

&emsp; If arguments omit, `dependency brew` will stand alone, and do nothing. To show dependency of all packages, use `-a` or `--all` option. And when using `-p` or `--package`, if given wrong package name, `dependency brew` might give a trivial “did-you-mean” correction.

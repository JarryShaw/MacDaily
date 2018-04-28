---

Status: Stable

Platform: macOS High Sierra

Language: Python & Bourne-Again Shell

Environment: Console | Terminal

Requirements: Python>=3.6 & Bash>=3.2

Implementation: CPython | PyPy

---

# jsdaily

&nbsp;

 - [About](#about)
 - [Installation](#install)
 - [Configuration](#config)
 - [Usage Manual](#usage)
    * [Start-Up](#startup)
    * [Commands](#command)
    * [Update Procedure](#update)
        - [Atom Plug-In](#update_apm)
        - [Ruby Gem](#update_gem)
        - [Node.js Module](#update_npm)
        - [Python Package](#update_pip)
        - [Homebrew Formula](#update_brew)
        - [Caskroom Binary](#update_cask)
        - [Mac App Store](#update_apptore)
        - [Cleanup Procedure](#update_cleanup)
    * [Uninstall Procedure](#uninstall)
    * [Reinstall Procedure](#reinstall)
    * [Postinstall Procedure](#postinstall)
    * [Dependency Procedure](#dependency)
    * [Logging Procedure](#logging)
 - [Troubleshooting](#issue)

---

&nbsp;

<a name="about"> </a>

## About

 > Just some useful daily utility scripts.

&emsp; `jsdaily` is a mediate collection of console scripts written in __Python__ and __Bourne-Again Shell__. Originally works as an automatic housekeeper for one's Mac, which should update all packages outdated, `jsdaily` is now fully functioned and end-user oriented. Without being aware of everything about your Mac, one can easily work around and manage packages out of no pain using `jsdaily`.

&nbsp;

<a name="install"> </a>

## Installation

&emsp; As of many Python packages, `jsdaily` can install through `pip` with the following command, which will get you the latest version from [PyPI](https://pypi.org).

```
$ pip install jsdaily
```

&emsp; Or if you prefer the real-latest version, fetch from this Git repository, then the script below should be used.

```
$ git clone https://github.com/JarryShaw/jsdaily.git
$ python setup.py install
```

&emsp; Do please __NOTE__ that, `jsdaily` runs only with support of Python from version ***3.6*** and on. And it shall only work ideally on ***macOS***.

&nbsp;

<a name="config"> </a>

## Configuration

 > This part might be kind of garrulous, some users may not know what's going on here. :wink:

&emsp; Since robust enough, `jsdaily` now supports configuration upon user's own wish. One may set up log path, hard disk path, archive path and many other things, other than the default settings.

&emsp; The configuration file should be stored under `~/.dailyrc`, which is hidden from Finder by macOS. To review or edit it, you may use text editors like `vim` and `nano`, or other graphic editors, such as `Sublime Text` and `Atom`, or whatever you find favourable.

```
[Path]
# In this section, paths for log files are specified.
# Please, under any circumstances, make sure they are valid.
logdir = /Library/Logs/Scripts      ; path where logs will be stored
tmpdir = /tmp/log                   ; path where temporary runtime logs go
dskdir = /Volumes/Your Disk         ; path where your hard disk lies
arcdir = ${dskdir}/Developers       ; path where ancient logs archive

[Mode]
# In this section, flags for modes are configured.
# If you would like to disable the mode, set it to "false".
apm      = true     ; Atom packages
gem      = true     ; Ruby gems
npm      = true     ; Node.js modules
pip      = true     ; Python packages
brew     = true     ; Homebrew Cellars
cask     = true     ; Caskroom Casks
dotapp   = true     ; Applications (*.app)
macapp   = true     ; applications in /Application folder
cleanup  = true     ; cleanup caches
appstore = true     ; Mac App Store applications
```

&emsp; Above is the content of `.dailyrc`, following the grammar of `INI` files. Lines and words after number sign (`'#'`) and semicolon (`';'`) are comments, whose main purpose is to help understanding the contents of this file.

&emsp; In section `[Path]`, there are path names where logs and some other things to be stored. In section `[Mode]`, there are ten different modes to indicate if they are *enabled* or *disabled* in default.

&emsp; You may wish to set the `dskdir` -- *path where your hard disk lies*, which allows `jsdaily` to archive your ancient logs and caches into somewhere never bothers.

&emsp; Please __NOTE__ that, under all circumstances, of section `[Path]`, all values would better be a ***valid path name without blank characters*** (`' \t\n\r\f\v'`), except your hard disk `dskdir`.

&nbsp;

<a name="usage"> </a>

## Usage Manual

<a name="startup"> </a>

### Start-Up

&emsp; Before we dive into the usage of `jsdaily`, let's firstly get our hands dirty with some simple commands.

 > __NOTE__ -- all acronyms and aliases are left out for a quick and clear view of `jsdaily`

1. How to update all outdated packages?

    ```
    $ jsdaily update --all
    ```

2. How to update a certain package (eg: `hello` from Homebrew) ?

    ```
    $ jsdaily update brew --package hello
    ```

3. How to uninstall a certain package along with its dependencies (eg: `pytest` from brewed CPython version 3.6) ?

    ```
    $ jsdaily uninstall pip --brew --cpython --python_version 3 --package pytest
    ```

4. How to reinstall all packages but do not cleanup caches?

    ```
    $ jsdaily reinstall --all --no-cleanup
    ```

5. How to postinstall packages whose name ranges between "start" and "stop" alphabetically?

    ```
    $ jsdaily postinstall --all --startwith start --endwith stop
    ```

6. How to show dependency of a certain package as a tree (eg: `gnupg` from Homebrew) ?

    ```
    $ jsdaily dependency brew --package gnupg --tree
    ```

7. How to log all applications on my Mac, a.k.a. `*.app` files?

    ```
    $ jsdaily logging dotapp
    ```

8. How to run `jsdaily` in quiet mode, i.e. with no output information (eg: `logging` in quiet mode) ?

    ```
    $ jsdaily logging --all --quiet
    ```

<a name="command"> </a>

### Commands

&emsp; `jsdaily` supports several different commands, from `update`, `unisntall`, `reinstall` and `postinstall` to `dependency` and `logging`. Of all commands, there are corresponding **aliases** for which to be reckoned as valid.

| Command       | Aliases                         |
| :------------ | :------------------------------ |
| `update`      | `up`, `U`, `upgrade`            |
| `uninstall`   | `un`, `remove`, `rm`, `r`, `un` |
| `reinstall`   | `re`, `R`                       |
| `postinstall` | `post`, `ps`, `p`               |
| `dependency`  | `deps`, `dep`, `dp`, `de`, `d`  |
| `logging`     | `log`, `lg`, `l`                |

&emsp; And the man page of `jsdaily` shows as below.

```
$ jsdaily --help
usage: jsdaily [-h] command

Package Day Care Manager

optional arguments:
  -h, --help     show this help message and exit
  -V, --version  show program's version number and exit

Commands:
  jsdaily provides a friendly CLI workflow for the administrator of macOS to
  manipulate packages
```

<a name="update"> </a>

### Update Procedure

&emsp; The `update` command will automatically update all outdated packages installed through --

 - `apm` -- [Atom](https://atom.io) plug-ins
 - `gem` -- [Ruby](https://www.ruby-lang.org) gems
 - `npm` -- [Node.js](https://nodejs.org) modules
 - `pip` -- Python packages, in both version of 2.\* and 3.\*, running under [CPython](https://www.python.org) or [PyPy](https://pypy.org) compiler, and installed through `brew` or official disk images (`*.dmg`)
 - `brew` -- [Homebrew](https://brew.sh) formulae
 - `cask` -- [Caskroom](https://caskroom.github.io) binaries
 - `appstore` -- Mac App Store or `softwareupdate` installed applications

and an additional `cleanup` procedure, which prunes and deduplicates files, archives and removes caches. The man page of `update` shows as below.

```
$ jsdaily update --help
usage: jsdaily update [-hV] [-qv] [-fgm] [-a] [--[no-]MODE] MODE ...

Automatic Package Update Manager

optional arguments:
  -h, --help     show this help message and exit
  -V, --version  show program's version number and exit
  -a, --all      update all packages installed through Atom, pip, RubyGem,
                 Node.js, Homebrew, Caskroom, App Store, and etc
  -f, --force    run in force mode, only for Homebrew or Caskroom
  -m, --merge    run in merge mode, only for Homebrew
  -g, --greedy   run in greedy mode, only for Caskroom
  -r, --restart  automatically restart if necessary, only for App Store
  -Y, --yes      yes for all selections, only for pip
  -q, --quiet    run in quiet mode, with no output information
  -v, --verbose  run in verbose mode, with detailed output information

mode selection:
  MODE           update outdated packages installed through a specified
                 method, e.g.: apm, gem, npm, pip, brew, cask, appstore, or
                 alternatively and simply, cleanup

aliases: update, up, U, upgrade
```

&emsp; Note that disabled modes in configuration file `.dailyrc` will not update under any circumstances. To update all packages, use one of the commands below.

```
$ jsdaily update -a
$ jsdaily update --all
```

<a name="update_apm"> </a>

1. `apm` -- Atom Plug-In

&emsp; [Atom](https://atom.io) provides a package manager called `apm`, i.e. "Atom Package Manager". The man page for `jsdaily update apm` shows as below.

```
$ jsdaily update apm --help
usage: jsdaily update apm [-h] [-qv] [-a] [-p PKG]

Update Installed Atom Packages

optional arguments:
  -h, --help            show this help message and exit
  -a, --all             update all packages installed through apm
  -p PKG, --package PKG
                        name of packages to be updated, default is all
  -q, --quiet           run in quiet mode, with no output information
  -v, --verbose         run in verbose mode, with detailed output information
```

&emsp; If arguments omit, `jsdaily` will __NOT__ update outdated packages of Atom. And when using `-p` or `--package`, if given wrong package name, `jsdaily` might give a trivial "did-you-mean" correction.

<a name="update_gem"> </a>

2. `gem` -- Ruby Gem

&emsp; [Ruby](https://www.ruby-lang.org) provides a package manager called `gem`, which may refer to

 - `/usr/bin/gem` -- system built-in RubyGem (which is left out for security reasons)
 - `/usr/local/bin/gem` -- brewed or installed through other methods by user

The man page for `jsdaily update gem` shows as below.

```
$ jsdaily update gem --help
usage: jsdaily update gem [-h] [-qv] [-a] [-p PKG]

Update Installed Ruby Packages

optional arguments:
  -h, --help            show this help message and exit
  -a, --all             update all packages installed through gem
  -p PKG, --package PKG
                        name of packages to be updated, default is all
  -q, --quiet           run in quiet mode, with no output information
  -v, --verbose         run in verbose mode, with detailed output information
```

&emsp; If arguments omit, `jsdaily` will __NOT__ update outdated packages of Ruby. And when using `-p` or `--package`, if given wrong package name, `jsdaily` might give a trivial "did-you-mean" correction.

<a name="update_npm"> </a>

3. `npm` -- Node.js Module

&emsp; [Node.js](https://nodejs.org) provides a package manager called `npm`, i.e. "Node.js Package Manger". The man page for `jsdaily update npm` shows as below.

```
$ jsdaily update npm --help
usage: jsdaily update npm [-h] [-qv] [-a] [-p PKG]

Update Installed Node.js Packages

optional arguments:
  -h, --help            show this help message and exit
  -a, --all             update all packages installed through gem
  -p PKG, --package PKG
                        name of packages to be updated, default is all
  -q, --quiet           run in quiet mode, with no output information
  -v, --verbose         run in verbose mode, with detailed output information
```

&emsp; If arguments omit, `jsdaily` will __NOT__ update outdated packages of Ruby. And when using `-p` or `--package`, if given wrong package name, `jsdaily` might give a trivial "did-you-mean" correction.

<a name="update_pip"> </a>

4. `pip` -- Python Package

&emsp; As there\'re all kinds and versions of Python complier, along with its `pip` package manager. Here, we support update of the following --

 - Python 2.\*/3.\* installed through Python official disk images (`*.dmg`)
 - Python 2/3 installed through `brew install python@2/python`
 - PyPy 2/3 installed through `brew install pypy/pypy3`

And the man page for `jsdaily update pip` shows as below.

```
$ jsdaily update pip --help
usage: jsdaily update pip [-h] [-qv] [-bcsy] [-V VER] [-a] [-p PKG]

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
```

&emsp; If arguments omit, `jsdaily` will __NOT__ update outdated packages in all copies of Python. And when using `-p` or `--package`, if given wrong package name, `jsdaily` might give a trivial "did-you-mean" correction.

<a name="update_brew"> </a>

5. `brew` -- Homebrew Formula

&emsp; [Homebrew](https://brew.sh) is the missing package manager for macOS. The man page for `jsdaily update brew` shows as below.

```
$ jsdaily update brew --help
usage: jsdaily update brew [-h] [-qv] [-fm] [-a] [-p PKG] [--no-cleanup]

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
```

 > __NOTE__ -- arguments `-f` and `--force`, `-m` and `--merge` are using only for `brew update` command

&emsp; If arguments omit, `jsdaily` will __NOT__ update outdated packages of Homebrew. And when using `-p` or `--package`, if given wrong package name, `jsdaily` might give a trivial "did-you-mean" correction.

<a name="update_cask"> </a>

6. `cask` -- Caskrooom Binary

&emsp; [Caskroom](https://caskroom.github.io) is a friendly binary installer for macOS. The man page for `jsdaily update cask` shows as below.

```
$ jsdaily update cask --help
usage: jsdaily update cask [-h] [-qv] [-fg] [-a] [-p PKG] [--no-cleanup]

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
```

 > __NOTE__ -- arguments `-f` and `--force`, `-g` and `--greedy` are using only for `brew cask upgrade` command; and when the latter given, `jsdaily` will directly run `brew cask upgrade --greedy`

&emsp; If arguments omit, `jsdaily` will __NOT__ update outdated packages of Caskroom. And when using `-p` or `--package`, if given wrong package name, `jsdaily` might give a trivial "did-you-mean" correction.

<a name="update_appstore"> </a>

7. `appstore` -- Mac App Store

&emsp; `softwareupdate` is the system software update tool. The man page for `jsdaily update appstore` shows as below.

```
$ jsdaily update appstore --help
usage: jsdaily update appstore [-h] [-q] [-a] [-p PKG]

Update installed App Store packages

optional arguments:
  -h, --help            show this help message and exit
  -a, --all             update all packages installed through App Store
  -p PKG, --package PKG
                        name of packages to be updated, default is all
  -q, --quiet           run in quiet mode, with no output information
```

&emsp; If arguments omit, `jsdaily` will __NOT__ update outdated packages in Mac App Store or `softwareupdate`. And when using `-p` or `--package`, if given wrong package name, `jsdaily` might give a trivial "did-you-mean" correction.

<a name="update_cleanup"> </a>

8. `cleanup` -- Cleanup Procedure

&emsp; `cleanup` prunes and deduplicates files, archives and removes caches. The man page for `jsdaily update cleanup` shows as below.

```
$ jsdaily update cleanup --help
usage: jsdaily update cleanup [-h] [-q] [--no-brew] [--no-cask]

Cleanup Caches & Downloads

optional arguments:
  -h, --help   show this help message and exit
  --no-gem     do not remove Ruby caches & downloads
  --no-npm     do not remove Node.js caches & downloads
  --no-pip     do not remove Python caches & downloads
  --no-brew    do not remove Homebrew caches & downloads
  --no-cask    do not remove Caskroom caches & downloads
  -q, --quiet  run in quiet mode, with no output information
```

&emsp; If arguments omit, `jsdaily` will cleanup all caches as its default setup.

<a name="uninstall"> </a>

### Uninstall Procedure

&emsp; The `uninstall` command will recursively uninstall all dependency packages installed through --

 - `pip` -- Python packages, in both version of 2.\* and 3.\*, running under [CPython](https://www.python.org) or [PyPy](https://pypy.org) compiler, and installed through `brew` or official disk images (`*.dmg`)
 - `brew` -- [Homebrew](https://brew.sh) formulae
 - `cask` -- [Caskroom](https://caskroom.github.io) binaries

The man page of `uninstall` shows as below.

```
$ jsdaily uninstall --help
usage: jsdaily uninstall [-hV] [-qv] [-fiY] [-a] [--[no-]MODE] MODE ...

Package Recursive Uninstall Manager

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit
  -a, --all             uninstall all packages installed through pip,
                        Homebrew, and App Store
  -f, --force           run in force mode, only for Homebrew and Caskroom
  -i, --ignore-dependencies
                        run in non-recursive mode, only for Python and Homebrew
  -q, --quiet           run in quiet mode, with no output information
  -v, --verbose         run in verbose mode, with more information
  -Y, --yes             yes for all selections

mode selection:
  MODE                  uninstall given packages installed through a specified
                        method, e.g.: pip, brew or cask

aliases: uninstall, remove, rm, r, un
```

&emsp; Note that disabled modes in configuration file `.dailyrc` will not uninstall under any circumstances. To uninstall all packages, use one of the commands below.

```
$ jsdaily uninstall -a
$ jsdaily uninstall --all
```

<a name="uninstall_pip"> </a>

1. `pip` -- Python Package

&emsp; As there're several kinds and versions of Python complier, along wiht its `pip` package manager. Here, we support uninstall procedure in following --

 - Python 2.\*/3.\* installed through Python official disk images (`*.dmg`)
 - Python 2/3 installed through `brew install python@2/python`
 - PyPy 2/3 installed through `brew install pypy/pypy3`

&emsp; And the man page for `jsdaily uninstall pip` shows as below.

```
$ jsdaily uninstall pip --help
usage: jsdaily uninstall pip [-h] [-qv] [-iY] [-bcsy] [-V VER] [-a] [-p PKG]

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
                        run in non-recursive mode, i.e. ignore dependencies
                        of uninstalling packages
  -q, --quiet           run in quiet mode, with no output information
  -v, --verbose         run in verbose mode, with more information
  -Y, --yes             yes for all selections
```

&emsp; If arguments omit, `jsdaily` will __NOT__ uninstall packages in all copies of Python. And when using `-p` or `--package`, if given wrong package name, `jsdaily` might give a trivial “did-you-mean” correction.

<a name="uninstall_brew"> </a>

2. `brew` – Homebrew Formula

&emsp; [Homebrew](https://brew.sh) is the missing package manager for macOS. The man page for `jsdaily uninstall brew` shows as below.

```
$ jsdaily uninstall brew --help
usage: jsdaily uninstall brew [-h] [-qv] [-iY] [-f] [-a] [-p PKG]

Uninstall Installed Homebrew Packages

optional arguments:
  -h, --help            show this help message and exit
  -a, --all             uninstall all packages installed through Homebrew
  -p PKG, --package PKG
                        name of packages to be uninstalled, default is null
  -f, --force           use "--force" when running `brew uninstall`
  -i, --ignore-dependencies
                        run in non-recursive mode, i.e. ignore dependencies of
                        uninstalling packages
  -q, --quiet           run in quiet mode, with no output information
  -v, --verbose         run in verbose mode, with more information
  -Y, --yes             yes for all selections
```

&emsp; If arguments omit, `jsdaily` will __NOT__ uninstall packages of Homebrew. And when using `-p` or `--package`, if given wrong package name, `jsdaily` might give a trivial “did-you-mean” correction.

<a name="uninstall_cask"> </a>

3. `cask` – Caskrooom Binary

&emsp; [Caskroom](https://caskroom.github.io) is a friendly binary installer for macOS. The man page for `jsdaily uninstall cask` shows as below.

```
$ jsdaily uninstall cask --help
usage: jsdaily uninstall cask [-h] [-qv] [-Y] [-f] [-a] [-p PKG]

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
```

&emsp; If arguments omit, `jsdaily` will __NOT__ uninstall packages of Caskroom. And when using `-p` or `--package`, if given wrong package name, `jsdaily` might give a trivial “did-you-mean” correction.

&nbsp;

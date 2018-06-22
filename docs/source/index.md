---

Platform: macOS High Sierra

Language: Python | Bourne-Again Shell

Environment: Console | Terminal

---

&nbsp;

# jsdaily

[![Downloads](http://pepy.tech/badge/jsdaily)](http://pepy.tech/count/jsdaily)
[![version](https://img.shields.io/pypi/v/jsdaily.svg)](https://pypi.org/project/jsdaily)
[![format](https://img.shields.io/pypi/format/jsdaily.svg)](https://pypi.org/project/jsdaily)
[![status](https://img.shields.io/pypi/status/jsdaily.svg)](https://pypi.org/project/jsdaily)

[![language](https://img.shields.io/github/languages/top/JarryShaw/jsdaily.svg)](https://github.com/JarryShaw/jsdaily)
[![made-with-bash](https://img.shields.io/badge/Made%20with-Bash-1f425f.svg)](https://www.gnu.org/software/bash)
[![python](https://img.shields.io/pypi/pyversions/jsdaily.svg)](https://python.org)
[![implementation](https://img.shields.io/pypi/implementation/jsdaily.svg)](http://pypy.org)

&nbsp;

 - [About](#about)
 - [Installation](#install)
 - [Configuration](#configuration)
 - [Usage Manual](#usage)
    * [Start-Up](#startup)
    * [Commands](#command)
    * [Archive Procedure](#archive)
    * [Config Procedure](#config)
    * [Launch Procedure](#launch)
    * [Update Procedure](#update)
        - [Atom Plug-In](#update_apm)
        - [Ruby Gem](#update_gem)
        - [Node.js Module](#update_npm)
        - [Python Package](#update_pip)
        - [Homebrew Formula](#update_brew)
        - [Caskroom Binary](#update_cask)
        - [Mac App Store](#update_appstore)
        - [Cleanup Procedure](#update_cleanup)
    * [Uninstall Procedure](#uninstall)
        - [Python Package](#uninstall_pip)
        - [Homebrew Formula](#uninstall_brew)
        - [Caskroom Binary](#uninstall_cask)
    * [Reinstall Procedure](#reinstall)
        - [Homebrew Formula](#reinstall_brew)
        - [Caskroom Binary](#reinstall_cask)
        - [Cleanup Procedure](#reinstall_cleanup)
    * [Postinstall Procedure](#postinstall)
        - [Homebrew Formula](#postinstall_brew)
        - [Cleanup Procedure](#postinstall_cleanup)
    * [Dependency Procedure](#dependency)
        - [Python Package](#dependency_pip)
        - [Homebrew Formula](#dependency_brew)
    * [Logging Procedure](#logging)
        - [Atom Plug-In](#logging_apm)
        - [Ruby Gem](#logging_gem)
        - [Node.js Module](#logging_npm)
        - [Python Package](#logging_pip)
        - [Homebrew Formula](#logging_brew)
        - [Caskroom Binary](#logging_cask)
        - [macOS Application](#logging_dotapp)
        - [Installed Application](#logging_macapp)
        - [Mac App Store](#logging_appstore)
 - [Troubleshooting](#issue)
 - [TODO](#todo)

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

<a name="configuration"> </a>

## Configuration

 > This part might be kind of garrulous, some users may not know what's going on here. :wink:

&emsp; Since robust enough, `jsdaily` now supports configuration upon user's own wish. One may set up log path, hard disk path, archive path and many other things, other than the default settings.

 > __NOTA BENE__ -- `jsdaily` now supports configuration commands, see [Config Procedure](#config) section for more information.

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

[Daemon]
# In this section, scheduled tasks are set up.
# You may append and/or remove the time intervals.
update      = true      ; run update on schedule
uninstall   = false     ; don't run uninstall
reinstall   = false     ; don't run reinstall
postinstall = false     ; don't run postinstall
dependency  = false     ; don't run dependency
logging     = true      ; run logging on schedule
schedule    =           ; scheduled timing (in 24 hours)
    8:00                ; any daemon commands at 8:00
    22:30-update        ; update at 22:30
    23:00-logging       ; logging at 23:00

```

&emsp; Above is the content of `.dailyrc`, following the grammar of `INI` files. Lines and words after number sign (`'#'`) and semicolon (`';'`) are comments, whose main purpose is to help understanding the contents of this file.

&emsp; In section `[Path]`, there are path names where logs and some other things to be stored. In section `[Mode]`, there are ten different modes to indicate if they are *enabled* or *disabled* in default.

&emsp; You may wish to set the `dskdir` -- *path where your hard disk lies*, which allows `jsdaily` to archive your ancient logs and caches into somewhere never bothers. 

&emsp; Please __NOTE__ that, under all circumstances, of section `[Path]`, all values would better be a ***valid path name without blank characters*** (`' \t\n\r\f\v'`), except your hard disk `dskdir`.

&emsp; Besides, in section `[Daemon]`, you can decide which command is scheduled and when to run such command, with the format of `HH:MM[-CMD]`. 

&emsp; Please __NOTE__ that, the `CMD` is optional, which will be `any` when omits. And you may setup which command(s) will be registered as daemons and run with schedule through six booleans above. These boolean values help `jsdaily` indicate which is to be launched when commands in `schedule` omit. That is to say, when `command` omits in `schedule`, `jsdaily` will register all commands that set `true` in the above boolean values.

&nbsp;

<a name="usage"> </a>

## Usage Manual

<a name="startup"> </a>

### Start-Up

&emsp; Before we dive into the usage of `jsdaily`, let's firstly get our hands dirty with some simple commands.

 > __NOTE__ -- all acronyms and aliases are left out for a quick and clear view of `jsdaily`

1 . How to use `jsdaily`?

    ```shell
    # call from /usr/local/bin
    jsdaily [command ...] [flag ...]
    # or call from Python module
    python -m jsdaily [command ...] [flag ...]
    ```

2. How to setup my disks and daemons?

    ```
    $ jsdaily config
    ```

3. How to relaunch daemons after I manually modified `~/.jsdaily`?

    ```
    $ jsdaily launch
    ```

4. How to archive ancient logs without running any commands?

    ```
    $ jsdaily archive
    ```

5. How to update all outdated packages?

    ```
    $ jsdaily update --all
    ```

6. How to update a certain package (eg: `hello` from Homebrew) ?

    ```
    $ jsdaily update brew --package hello
    ```

7. How to uninstall a certain package along with its dependencies (eg: `pytest` from brewed CPython version 3.6) ?

    ```
    $ jsdaily uninstall pip --brew --cpython --python_version 3 --package pytest
    ```

8. How to reinstall all packages but do not cleanup caches?

    ```
    $ jsdaily reinstall --all --no-cleanup
    ```

9. How to postinstall packages whose name ranges between "start" and "stop" alphabetically?

    ```
    $ jsdaily postinstall --all --startwith start --endwith stop
    ```

10. How to show dependency of a certain package as a tree (eg: `gnupg` from Homebrew) ?

    ```
    $ jsdaily dependency brew --package gnupg --tree
    ```

11. How to log all applications on my Mac, a.k.a. `*.app` files?

    ```
    $ jsdaily logging dotapp
    ```

12. How to run `jsdaily` in quiet mode, i.e. with no output information (eg: `logging` in quiet mode) ?

    ```
    $ jsdaily logging --all --quiet
    ```

<a name="command"> </a>

### Commands

&emsp; `jsdaily` supports several different commands, from `archive`, `config`, `launch`, `update`, `unisntall`, `reinstall` and `postinstall` to `dependency` and `logging`. Of all commands, there are corresponding **aliases** for which to be reckoned as valid.

| Command                       | Aliases                         |
| :---------------------------- | :------------------------------ |
| [`archive`](#archive)         |                                 |
| [`config`](#config)           | `cfg`                           |
| [`launch`](#launch)           | `init`                          |
| [`update`](#update)           | `up`, `upgrade`                 |
| [`uninstall`](#uninstall)     | `un`, `remove`, `rm`, `r`, `un` |
| [`reinstall`](#reinstall)     | `re`                            |
| [`postinstall`](#postinstall) | `post`, `ps`,                   |
| [`dependency`](#dependency)   | `deps`, `dp`                    |
| [`logging`](#logging)         | `log`                           |

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

<a name="archive"> </a>

### Archive Procedure

```
$ jsdaily archive
```

&emsp; The `archive` command will move all ancient logs to where it belongs --

 - daily logs from last week (7 days) -- `${logdir}/archive` with corresponding modes named as `YYMMDD.tar.gz`
 - weekly archives from last month (approximately 4 weeks) -- `${logdir}/tarfile` with corresponding modes named as `YYMMDD-YYMMDD.tar.bz`
 - even older logs -- inside `${arcdir}/archive.zip` with corresponding modes and named as `YYMMDD-YYMMDD.tar.xz`

Actual paths of `${logdir}` and `${arcdir}` are defined in `~/.dailyrc`, may vary from your own settings.

<a name="config"> </a>

### Config Procedure

```
$ jsdaily config
Entering interactive command line setup procedure...
Default settings are shown as in the square brackets.
Please directly ENTER if you prefer the default settings.

For logging utilities, we recommend you to set up your hard disk path.
You may change other path preferences in configuration `~/.dailyrc` later.
Please note that all paths must be valid under all circumstances.
Name of your hard disk []:

In default, we will run update and logging commands twice a day.
You may change daily commands preferences in configuration `~/.dailyrc` later.
Please enter schedule as HH:MM-CMD format, and each separates with comma.
Time for daily scripts [8:00,22:30-update,23:00-logging]:
```

&emsp; As shown above, the `config` command will help modify `~/.dailyrc`. For more information on `~/.dailyrc`, please refer to the [Configuration](#configuration) section.

### Launch Procedure

```
$ jsdaily launch
```

&emsp; The `launch` command will reload `~/.dailyrc` and register daemons to `Launch Agents` on macOS. Please __NOTE__ that, launched daemons will set `RunAtLoad` to `<true/>`, which means after `launch` commands, they will be directly called by the `Launch Agents`.

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

2. `brew` -- Homebrew Formula

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

3. `cask` -- Caskrooom Binary

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

<a name="reinstall"> </a>

### Reinstall Procedure

&emsp; The `reinstall` command will automatically reinstall all given packages installed through --

 - `brew` -- [Homebrew](https://brew.sh) formulae
 - `cask` -- [Caskroom](https://caskroom.github.io) binaries

and an additional `cleanup` procedure, which prunes and deduplicates files, archives and removes caches. The man page of `reinstall` shows as below.

```
$ jsdaily reinstall --help
usage: jsdaily reinstall [-hV] [-qv] [-f] [-es PKG] [-a] [--[no-]MODE] MODE ...

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

aliases: reinstall, re, R
```

&emsp; Note that disabled modes in configuration file `.dailyrc` will not reinstall under any circumstances. To reinstall all packages, use one of the commands below.

```
$ jsdaily reinstall -a
$ jsdaily reinstall --all
```

<a name="reinstall_brew"> </a>

1. `brew` -- Homebrew Formula

&emsp; [Homebrew](https://brew.sh) is the missing package manager for macOS. The man page for `jsdaily reinstall brew` shows as below.

```
$ jsdaily reinstall brew --help
usage: jsdaily reinstall brew [-hV] [-qv] [-f] [-se PKG] [-a] [--[no-]MODE] MODE ...

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
```

&emsp; If arguments omit, `jsdaily` will __NOT__ reinstall packages of Homebrew. And when using `-p` or `--package`, if given wrong package name, `jsdaily` might give a trivial “did-you-mean” correction.

<a name="reinstall_cask"> </a>

2. `cask` -- Caskrooom Binary

&emsp; [Caskroom](https://caskroom.github.io) is a friendly binary installer for macOS. The man page for `jsdaily reinstall cask` shows as below.

```
$ jsdaily reinstall cask --help
usage: jsdaily reinstall cask [-hV] [-qv] [-se PKG] [-a] [--[no-]MODE] MODE ...

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
```

&emsp; If arguments omit, `jsdaily` will __NOT__ reinstall packages of Caskroom. And when using `-p` or `--package`, if given wrong package name, `jsdaily` might give a trivial “did-you-mean” correction.

<a name="reinstall_cleanup"> </a>

3. `cleanup` -- Cleanup Procedure

&emsp; `cleanup` prunes and deduplicates files, archives and removes caches. The man page for `jsdaily reinstall cleanup` shows as below.

```
$ jsdaily update reinstall --help
usage: jsdaily reinstall cleanup [-h] [-q] [--no-brew] [--no-cask]

Cleanup Caches & Downloads

optional arguments:
  -h, --help   show this help message and exit
  --no-brew    do not remove Homebrew caches & downloads
  --no-cask    do not remove Caskroom caches & downloads
  -q, --quiet  run in quiet mode, with no output information
```

&emsp; If arguments omit, `jsdaily` will cleanup all caches as its default setup.

<a name="postinstall"> </a>

### Postinstall Procedure

&emsp; The `postinstall` command will automatically postinstall all given packages installed through --

 - `brew` -- [Homebrew](https://brew.sh) formulae

and an additional `cleanup` procedure, which prunes and deduplicates files, archives and removes caches. The man page of `postinstall` shows as below.

```
$ jsdaily postinstall --help
usage: jsdaily postinstall [-hV] [-qv] [-eps PKG] [-a] [--no-cleanup]

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

aliases: postinstall, post, ps, p
```

&emsp; Note that disabled modes in configuration file `.dailyrc` will not postinstall under any circumstances. To postinstall all packages, use one of the commands below.

```
$ jsdaily postinstall -a
$ jsdaily postinstall --all
```

<a name="postinstall_brew"> </a>

1. `brew` -- Homebrew Formula

&emsp; [Homebrew](https://brew.sh) is the missing package manager for macOS. If arguments omit, `jsdaily` will __NOT__ postinstall packages of Homebrew. And when using `-p` or `--package`, if given wrong package name, `jsdaily` might give a trivial “did-you-mean” correction.

<a name="postinstall_cleanup"> </a>

2. `cleanup` -- Cleanup Procedure

&emsp; `cleanup` prunes and deduplicates files, archives and removes caches. If `--no-cleanup` option not set, `jsdaily` will cleanup all caches as its default setup.

<a name="dependency"> </a>

### Dependency Procedure

&emsp; The `dependency` command will automatically show dependencies of all packages installed through --

 - `pip` -- Python packages, in both version of 2.\* and 3.\*, running under [CPython](https://www.python.org) or [PyPy](https://pypy.org) compiler, and installed through `brew` or official disk images (`*.dmg`)
 - `brew` -- [Homebrew](https://brew.sh) formulae

The man page of `dependency` shows as below.

```
$ jsdaily dependency --help
usage: jsdaily dependency [-hV] [-t] [-a] [--[no-]MODE] MODE ...

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

aliases: dependency, deps, dep, dp, de, d
```

&emsp; Note that disabled modes in configuration file `.dailyrc` will not show dependencies under any circumstances. To show dependencies of all packages, use one of the commands below.

```
$ jsdaily dependency -a
$ jsdaily dependency --all
```

<a name="dependency_pip"> </a>

1. `pip` -- Python Package

&emsp; As there're several kinds and versions of Python complier, along with its `pip` package manager. Here, we support dependency procedure in following --

 - Python 2.\*/3.\* installed through Python official disk images (`*.dmg`)
 - Python 2/3 installed through `brew install python@2/python`
 - PyPy 2/3 installed through `brew install pypy/pypy3`

&emsp; And the man page for `jsdaily dependency pip` shows as below.

```
$ jsdaily dependency pip --help
usage: jsdaily dependency pip [-h] [-qv] [-bcsy] [-V VER] [-a] [-p PKG]

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
```

&emsp; If arguments omit, `jsdaily` will __NOT__ show package dependencies in all copies of Python. And when using `-p` or `--package`, if given wrong package name, `jsdaily` might give a trivial “did-you-mean” correction.

<a name="dependency_brew"> </a>

2. `brew` -- Homebrew Formula

&emsp; [Homebrew](https://brew.sh) is the missing package manager for macOS. The man page for `jsdaily dependency brew` shows as below.

```
$ jsdaily dependency brew --help
usage: jsdaily dependency brew [-h] [-t] [-a] [-p PKG]

Show Dependencies of Homebrew Packages

optional arguments:
  -h, --help            show this help message and exit
  -a, --all             show dependencies of all packages installed through
                        Homebrew
  -p PKG, --package PKG
                        name of packages to be shown, default is all
  -t, --tree            show dependencies as a tree
```

&emsp; If arguments omit, `jsdaily` will __NOT__ show package dependencies of Homebrew. And when using `-p` or `--package`, if given wrong package name, `jsdaily` might give a trivial “did-you-mean” correction.

<a name="logging"> </a>

### Logging Procedure

&emsp; The `logging` command will automatically log all applications and/or packages installed through --

 - `apm` -- [Atom](https://atom.io) plug-ins
 - `gem` -- [Ruby](https://www.ruby-lang.org) gems
 - `npm` -- [Node.js](https://nodejs.org) modules
 - `pip` -- Python packages, in both version of 2.\* and 3.\*, running under [CPython](https://www.python.org) or [PyPy](https://pypy.org) compiler, and installed through `brew` or official disk images (`*.dmg`)
 - `brew` -- [Homebrew](https://brew.sh) formulae
 - `cask` -- [Caskroom](https://caskroom.github.io) binaries
 - `dotapp` -- all `*.app` files on this Mac, a.k.a. `/` root directory
 - `macapp` -- applications in `/Application` folder
 - `appstore` -- Mac App Store applications

The man page of `logging` shows as below.

```
$ jsdaily logging --help
usage: jsdaily logging [-h] [-V] [-a] [-v VER] [-s] [-b] [-c] [-y] [-q]
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

aliases: logging, log, lg, l
```

&emsp; Note that disabled modes in configuration file `.dailyrc` will not be logged under any circumstances. To log all packages, use one of the commands below.

```
$ jsdaily logging -a
$ jsdaily logging --all
$ jsdaily logging apm gem npm pip brew cask dotapp macapp appstore
```

<a name="logging_apm"> </a>

1. `apm` -- Atom Plug-In

&emsp; [Atom](https://atom.io) provides a package manager called `apm`, i.e. "Atom Package Manager".

<a name="logging_gem"> </a>

2. `gem` -- Ruby Gem

&emsp; [Ruby](https://www.ruby-lang.org) provides a package manager called `gem`, which may refer to

 - `/usr/bin/gem` -- system built-in RubyGem (which is left out for security reasons)
 - `/usr/local/bin/gem` -- brewed or installed through other methods by user

<a name="logging_npm"> </a>

3. `npm` -- Node.js Module

&emsp; [Node.js](https://nodejs.org) provides a package manager called `npm`, i.e. "Node.js Package Manger".

<a name="logging_pip"> </a>

4. `pip` -- Python Package

&emsp; As there\'re all kinds and versions of Python complier, along with its `pip` package manager. Here, we support update of the following --

 - Python 2.\*/3.\* installed through Python official disk images (`*.dmg`)
 - Python 2/3 installed through `brew install python@2/python`
 - PyPy 2/3 installed through `brew install pypy/pypy3`

<a name="logging_brew"> </a>

5. `brew` -- Homebrew Formula

&emsp; [Homebrew](https://brew.sh) is the missing package manager for macOS.

<a name="logging_cask"> </a>

6. `cask` -- Caskrooom Binary

&emsp; [Caskroom](https://caskroom.github.io) is a friendly binary installer for macOS.

<a name="logging_dotapp"> </a>

7. `dotapp` -- macOS Application (`*.app`)

 > __NOTE__ -- symbolic links and files or folders under `/Volumes` are ignored

&emsp; On macOS, applications are folders named as `*.app` files. The `logging dotapp` command will walk through all directories from `/` root directory and seek `*.app` files.

<a name="logging_macapp"> </a>

8. `macapp` -- Installed Application

&emsp; On macOS, system-wide applications are placed in `/Application` folder.

<a name="logging_appstore"> </a>

9. `appstore` -- Mac App Store

&emsp; On macOS, applications may be installed through Mac App Store, whose `*.app` folder will contain some identical information.

&nbsp;

<a name="issue"> </a>

## Troubleshooting

1. Where can I find the log files?

    &emsp; It depends. Since the path where logs go can be modified through `~/.dailyrc`, it may vary as your settings. In default, you may find them under `/Library/Logs/Scripts`. And with every command, logs can be found in its corresponding folder. Logs are named after its running time, in the fold with corresponding date as its name.

    &emsp; Note that, normally, you can only find today's logs in the folder, since `jsdaily` automatically archive ancient logs into `./archive` folder. And every week, `./archive` folder will be tape-archived into `./tarfile`. Then after a month, and your hard disk available, they will be moved into `/Volumes/Your Diks/Developers/archive.zip`.

2. What if my hard disk ain't plugged-in when running the scripts?

    &emsp; Then the archiving and removing procedure will __NOT__ perform. In case, there might be some useful resources of you.

3. Which directory should I set in the configuration file?

    &emsp; First and foremost, I highly recommend you __NOT__ to modify the paths in `~/.dailyrc`, __EXCEPT__ your disk path `dskdir`.

    &emsp; But if you insist to do so, then make sure they are __VALID__ and ***available*** with permission granted, and most importantly, have __NO__ blank characters (`' \t\n\r\f\v'`) in the path, except `dskdir`.

&nbsp;

<a name="todo"> </a>

## TODO

 - [x] support configuration
 - [x] support command aliases
 - [x] reconstruct archiving procedure
 - [ ] support `gem` and `npm` in all commands
 - [x] optimise `KeyboardInterrupt` handling procedure
 - [ ] review `pip` implementation and version indication

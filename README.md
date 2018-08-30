---
Platform: OS X Yosemite ~ macOS Mojave

Language: Python | Bourne-Again Shell

Environment: Console | Terminal
---

&nbsp;

# MacDaily

[![Downloads](http://pepy.tech/badge/macdaily)](http://pepy.tech/count/macdaily)
[![version](https://img.shields.io/pypi/v/macdaily.svg)](https://pypi.org/project/macdaily)
[![format](https://img.shields.io/pypi/format/macdaily.svg)](https://pypi.org/project/macdaily)
[![status](https://img.shields.io/pypi/status/macdaily.svg)](https://pypi.org/project/macdaily)

[![language](https://img.shields.io/github/languages/top/JarryShaw/macdaily.svg)](https://github.com/JarryShaw/macdaily)
[![made-with-bash](https://img.shields.io/badge/Made%20with-Bash-1f425f.svg)](https://www.gnu.org/software/bash)
[![python](https://img.shields.io/pypi/pyversions/macdaily.svg)](https://python.org)
[![implementation](https://img.shields.io/pypi/implementation/macdaily.svg)](http://pypy.org)

&nbsp;

 - [About](#about)
 - [Installation](#install)
 - [Configuration](#configuration)
 - [Usage Manual](#usage)
    * [Start-Up](#startup)
    * [Commands](#command)
    * [Generals](#general)
 - [Troubleshooting](#issue)
 - [TODO](#todo)

---

&nbsp;

<a name="about"> </a>

## About

 > Package day-care manager on macOS.

&emsp; `macdaily` is a mediate collection of console scripts written in __Python__ and __Bourne-Again Shell__. Originally works as an automatic housekeeper for Mac to update all packages outdated, `macdaily` is now fully functioned and end-user oriented. Without being aware of everything about your Mac, one can easily work around and manage packages out of no pain using `macdaily`.

&nbsp;

<a name="install"> </a>

## Installation

&emsp; Just as many Python packages, `macdaily` can be installed through `pip` using the following command, which will get you the latest version from [PyPI](https://pypi.org).

```sh
pip install macdaily
```

&emsp; Or if you prefer the real-latest version and fetch from this Git repository, then the script below should be used.

```sh
git clone https://github.com/JarryShaw/macdaily.git
cd macdaily
pip install -e .
# and to update at any time
git pull
```

&emsp; And for tree format support in dependency command, you may need `pipdeptree`, then implicily you can use the following script to do so.

```sh
pip install macdaily[pipdeptree]
# or explicitly...
pip install macdaily pipdeptree
```

&emsp; Do please __NOTE__ that, `macdaily` runs only with support of Python from version ***3.6*** and on. And it shall only work ideally on ***macOS***.

&nbsp;

<a name="configuration"> </a>

## Configuration

 > This part might be kind of garrulous, for some may not know what's going on here. :wink:

&emsp; Since robust enough, `macdaily` now supports configuration upon user's own wish. One may set up log path, hard disk path, archive path and many other things, other than the default settings.

 > __NOTA BENE__ -- `macdaily` now supports configuration commands, see [Config Procedure](https://github.com/JarryShaw/MacDaily/tree/master/src#config) section for more information.

&emsp; The configuration file should lie under `~/.dailyrc`, which is hidden from Finder by macOS. To review or edit it, you may use text editors like `vim` and/or `nano`, or other graphic editors, such as `Sublime Text` and/or `Atom`, or whatever you find favourable.

```
[Path]
# In this section, paths for log files are specified.
# Please, under any circumstances, make sure they are valid.
logdir = ~/Library/Logs/MacDaily    ; path where logs will be stored
tmpdir = /tmp/dailylog              ; path where temporary runtime logs go
dskdir = /Volumes/Your Disk         ; path where your hard disk lies
arcdir = ${dskdir}/Developers       ; path where ancient logs archive

[Mode]
# In this section, flags for modes are configured.
# If you would like to disable the mode, set it to "false".
apm      = true     ; Atom packages
gem      = true     ; Ruby gems
mas      = true     ; Mac App Store applications
npm      = true     ; Node.js modules
pip      = true     ; Python packages
brew     = true     ; Homebrew Cellars
cask     = true     ; Caskroom Casks
dotapp   = true     ; Applications (*.app)
macapp   = true     ; all applications in /Application folder
system   = true     ; macOS system packages
cleanup  = true     ; cleanup caches
appstore = true     ; Mac App Store applications in /Application folder

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
    8:00                ; update & logging at 8:00
    22:30-update        ; update at 22:30
    23:00-logging       ; logging at 23:00

[Option]
# In this section, command options are picked.
# Do make sure these options are available for commands.
update  = --all --yes --pre --quiet --restart --show-log --no-cask
logging = --all --quiet --show-log

[Account]
# In this section, account information are stored.
# You must not modify this part under any circumstances.
username = ...
password = ********
```

&emsp; Above is the default content of `.dailyrc`, following the grammar of `INI` files. Lines and words after number sign (`'#'`) and semicolon (`';'`) are comments, whose main purpose is to help understanding the contents of this file.

&emsp; In section `[Path]`, there are path names where logs and some other things to be stored. In section `[Mode]`, there are ten different modes to indicate if they are *enabled* or *disabled* when calling from `--all` option.

&emsp; You may wish to set the `dskdir` -- *path where your hard disk lies*, which allows `macdaily` to archive your ancient logs and caches into somewhere never bothers.

&emsp; Please __NOTE__ that, under all circumstances, of section `[Path]`, all values would better be a ***valid path name without blank characters*** (` \t\n\r\f\v`), except your hard disk `dskdir`.

&emsp; Besides, in section `[Daemon]`, you can decide which command is scheduled and when to run such command, with the format of `HH:MM[-CMD]`. The `CMD` is optional, which will be `any` if omits. And you may setup which command(s) will be registered as daemons and run with schedule through six booleans above. These boolean values help `macdaily` indicate which is to be launched when commands in `schedule` omit. That is to say, when `command` omits in `schedule`, `macdaily` will register all commands that set `true` in the above boolean values.

&emsp; Also, in section `[Option]`, you may set up optional arguments for the daemons above. Do please make sure these commands are **valid**. And if omit, an empty arguments will be given.

&emsp; Last but no least, in section `[Account]`, you should **NEVER** modify any contents under this section in order to keep `macdaily` working. However, you may setup this part with [`config`](https://github.com/JarryShaw/MacDaily/tree/master/src#config) command.

&nbsp;

<a name="usage"> </a>

## Usage Manual

<a name="startup"> </a>

### Start-Up

&emsp; Before we dive into the detailed usage of `macdaily`, let's firstly get our hands dirty with some simple commands.

 > __NOTE__ -- all acronyms and aliases are left out for a quick and clear view of `macdaily`

1. How to use `macdaily`?

    ```shell
    # call from $PATH
    $ macdaily [command ...] [flag ...]
    # or call from Python module
    $ python -m macdaily [command ...] [flag ...]
    ```

2. How to setup my disks and daemons?

    ```
    $ macdaily config
    ```

3. How to relaunch daemons after I manually modified `~/.dailyrc`?

    ```
    $ macdaily launch
    ```

4. How to archive ancient logs without running any commands?

    ```
    $ macdaily archive
    ```

5. How to update all outdated packages?

    ```
    $ macdaily update --all
    ```

6. How to update a certain package (eg: `hello` from Homebrew) ?

    ```
    $ macdaily update brew --package hello
    ```

7. How to uninstall a certain package along with its dependencies (eg: `pytest` from brewed CPython version 3.6) ?

    ```
    $ macdaily uninstall pip --brew --cpython --python_version=3 --package pytest
    ```

8. How to reinstall all packages but do not cleanup caches?

    ```
    $ macdaily reinstall --all --no-cleanup
    ```

9. How to postinstall packages whose name ranges between "start" and "stop" alphabetically?

    ```
    $ macdaily postinstall --all --startwith=start --endwith=stop
    ```

10. How to show dependency of a certain package as a tree (eg: `gnupg` from Homebrew) ?

    ```
    $ macdaily dependency brew --package gnupg --tree
    ```

11. How to log all applications on my Mac, a.k.a. `*.app` files?

    ```
    $ macdaily logging dotapp
    ```

12. How to run `macdaily` in quiet mode, i.e. with no output information (eg: `logging` in quiet mode) ?

    ```
    $ macdaily logging --all --quiet
    ```

13. How to dump a `Macfile` to keep track of all packages?

    ```
    $ macdaily bundle dump
    ```

<a name="command"> </a>

### Commands

&emsp; `macdaily` supports several different commands, from `archive`, `bundle`, `config`, `launch`, `update`, `unisntall`, `reinstall` and `postinstall` to `dependency` and `logging`. Of all commands, there are corresponding **aliases** for which to be reckoned as valid.

| Command                       | Aliases                         |
| :---------------------------- | :------------------------------ |
| [`archive`](#archive)         |                                 |
| [`bundle`](#bundle)           |                                 |
| [`config`](#config)           | `cfg`                           |
| [`launch`](#launch)           | `init`                          |
| [`update`](#update)           | `up`, `upgrade`                 |
| [`uninstall`](#uninstall)     | `un`, `remove`, `rm`, `r`, `un` |
| [`reinstall`](#reinstall)     | `re`                            |
| [`postinstall`](#postinstall) | `post`, `ps`,                   |
| [`dependency`](#dependency)   | `deps`, `dp`                    |
| [`logging`](#logging)         | `log`                           |

<a name="general"> </a>

### Generals

&emsp; The man page of `macdaily` shows as below.

```
$ macdaily --help
usage: macdaily [-h] command

Package Day Care Manager

optional arguments:
  -h, --help     show this help message and exit
  -V, --version  show program's version number and exit

Commands:
  macdaily provides a friendly CLI workflow for the administrator of macOS to
  manipulate packages
```

&emsp; Commands for `macdaily` is shown as above and they are mandatory. For more detailed usage information, please refer to the [MacDaily General Manual](https://github.com/JarryShaw/MacDaily/tree/master/src#macdaily-general-manual). And here is a brief catalogue for the manual.

 * [Archive Procedure](https://github.com/JarryShaw/MacDaily/tree/master/src#archive)
 * [Config Procedure](https://github.com/JarryShaw/MacDaily/tree/master/src#config)
 * [Launch Procedure](https://github.com/JarryShaw/MacDaily/tree/master/src#launch)
 * [Update Procedure](https://github.com/JarryShaw/MacDaily/tree/master/src#update)
     - [Atom Plug-In](https://github.com/JarryShaw/MacDaily/tree/master/src/libupdate#update_apm)
     - [Ruby Gem](https://github.com/JarryShaw/MacDaily/tree/master/src/libupdate#update_gem)
     - [Mac App Store](https://github.com/JarryShaw/MacDaily/tree/master/src/libupdate#update_mas)
     - [Node.js Module](https://github.com/JarryShaw/MacDaily/tree/master/src/libupdate#update_npm)
     - [Python Package](https://github.com/JarryShaw/MacDaily/tree/master/src/libupdate#update_pip)
     - [Homebrew Formula](https://github.com/JarryShaw/MacDaily/tree/master/src/libupdate#update_brew)
     - [Caskroom Binary](https://github.com/JarryShaw/MacDaily/tree/master/src/libupdate#update_cask)
     - [System Software](https://github.com/JarryShaw/MacDaily/tree/master/src/libupdate#update_system)
     - [Cleanup Procedure](https://github.com/JarryShaw/MacDaily/tree/master/src/libupdate#update_cleanup)
 * [Uninstall Procedure](https://github.com/JarryShaw/MacDaily/tree/master/src#uninstall)
     - [Python Package](https://github.com/JarryShaw/MacDaily/tree/master/src/libuninstall#uninstall_pip)
     - [Homebrew Formula](https://github.com/JarryShaw/MacDaily/tree/master/src/libuninstall#uninstall_brew)
     - [Caskroom Binary](https://github.com/JarryShaw/MacDaily/tree/master/src/libuninstall#uninstall_cask)
 * [Reinstall Procedure](https://github.com/JarryShaw/MacDaily/tree/master/src#reinstall)
     - [Homebrew Formula](https://github.com/JarryShaw/MacDaily/tree/master/src/libprinstall#reinstall_brew)
     - [Caskroom Binary](https://github.com/JarryShaw/MacDaily/tree/master/src/libprinstall#reinstall_cask)
     - [Cleanup Procedure](https://github.com/JarryShaw/MacDaily/tree/master/src/libprinstall#reinstall_cleanup)
 * [Postinstall Procedure](https://github.com/JarryShaw/MacDaily/tree/master/src#postinstall)
     - [Homebrew Formula](https://github.com/JarryShaw/MacDaily/tree/master/src/libprinstall#postinstall_brew)
     - [Cleanup Procedure](https://github.com/JarryShaw/MacDaily/tree/master/src/libprinstall#postinstall_cleanup)
 * [Dependency Procedure](https://github.com/JarryShaw/MacDaily/tree/master/src#dependency)
     - [Python Package](https://github.com/JarryShaw/MacDaily/tree/master/src/libdependency#dependency_pip)
     - [Homebrew Formula](https://github.com/JarryShaw/MacDaily/tree/master/src/libdependency#dependency_brew)
 * [Logging Procedure](https://github.com/JarryShaw/MacDaily/tree/master/src#logging)
     - [Atom Plug-In](https://github.com/JarryShaw/MacDaily/tree/master/src/liblogging#logging_apm)
     - [Ruby Gem](https://github.com/JarryShaw/MacDaily/tree/master/src/liblogging#logging_gem)
     - [Node.js Module](https://github.com/JarryShaw/MacDaily/tree/master/src/liblogging#logging_npm)
     - [Python Package](https://github.com/JarryShaw/MacDaily/tree/master/src/liblogging#logging_pip)
     - [Homebrew Formula](https://github.com/JarryShaw/MacDaily/tree/master/src/liblogging#logging_brew)
     - [Caskroom Binary](https://github.com/JarryShaw/MacDaily/tree/master/src/liblogging#logging_cask)
     - [macOS Application](https://github.com/JarryShaw/MacDaily/tree/master/src/liblogging#logging_dotapp)
     - [Installed Application](https://github.com/JarryShaw/MacDaily/tree/master/src/liblogging#logging_macapp)
     - [Mac App Store](https://github.com/JarryShaw/MacDaily/tree/master/src/liblogging#logging_appstore)
 * [Bundle Procedure](https://github.com/JarryShaw/MacDaily/tree/master/src#bundle)
     - [Dump Macfile](https://github.com/JarryShaw/MacDaily/tree/master/src/libbundle#bundle_dump)
     - [Load Macfile](https://github.com/JarryShaw/MacDaily/tree/master/src/libbundle#bundle_load)

&nbsp;

<a name="issue"> </a>

## Troubleshooting

1. Where can I find the log files?

    &emsp; It depends. Since the path where logs go can be modified through `~/.dailyrc`, it may vary as your settings. In default, you may find them under `~/Library/Logs/Scripts`. And with every command, logs can be found in its corresponding folder. Logs are named after its running time, in the fold with corresponding date as its name.

    &emsp; Note that, normally, you can only find today's logs in the folder, since `macdaily` automatically archive ancient logs into `${logdir}/archive` folder. And every week, `${logdir}/archive` folder will be tape-archived into `${logdir}/tarfile`. Then after a month, and your hard disk available, they will be moved into `/Volumes/Your Diks/Developers/archive.zip`.

2. What if my hard disk ain't plugged-in when running the scripts?

    &emsp; Then the archiving and removing procedure will __NOT__ perform. In case there might be some useful resources of yours.

3. Which directory should I set in the configuration file?

    &emsp; First and foremost, I highly recommend you __NOT__ to modify the paths in `~/.dailyrc` manually, __EXCEPT__ your disk path `dskdir`.

    &emsp; But if you insist to do so, then make sure they are __VALID__ and ***available*** with permission granted, and most importantly, have __NO__ blank characters (` \t\n\r\f\v`) in the path, except `dskdir`.

&nbsp;

<a name="todo"> </a>

## TODO

 - [x] support configuration
 - [x] support command aliases
 - [x] reconstruct archiving procedure
 - [ ] support `gem` and `npm` in all commands
 - [x] optimise `KeyboardInterrupt` handling procedure
 - [ ] review `pip` implementation and version indication
 - [x] considering support more versions of Python

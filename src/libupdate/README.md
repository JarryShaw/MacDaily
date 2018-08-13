# MacDaily Update Manual

 - [Atom Plug-In](#update_apm)
 - [Ruby Gem](#update_gem)
 - [Mac App Store](#update_mas)
 - [Node.js Module](#update_npm)
 - [Python Package](#update_pip)
 - [Homebrew Formula](#update_brew)
 - [Caskroom Binary](#update_cask)
 - [System Software](#update_system)
 - [Cleanup Procedure](#update_cleanup)

---

<a name="update_apm"> </a>

1. `apm` -- Atom Plug-In

&emsp; [Atom](https://atom.io) provides a package manager called `apm`, i.e. "Atom Package Manager". The man page for `macdaily update apm` shows as below.

```
$ macdaily update apm --help
usage: macdaily update apm [-h] [-qv] [-a] [-p PKG]

Update Installed Atom Packages

optional arguments:
  -h, --help            show this help message and exit
  -a, --all             update all packages installed through apm
  -p PKG, --package PKG
                        name of packages to be updated, default is all
  -q, --quiet           run in quiet mode, with no output information
  -v, --verbose         run in verbose mode, with detailed output information
  --show-log            open log in Console upon completion of command
```

&emsp; If arguments omit, `macdaily` will __NOT__ update outdated packages of Atom. And when using `-p` or `--package`, if given wrong package name, `macdaily` might give a trivial "did-you-mean" correction.

<a name="update_gem"> </a>

2. `gem` -- Ruby Gem

&emsp; [Ruby](https://www.ruby-lang.org) provides a package manager called `gem`, which may refer to

 - `/usr/bin/gem` -- system built-in RubyGem (which is left out for security reasons)
 - `/usr/local/bin/gem` -- brewed or installed through other methods by user

The man page for `macdaily update gem` shows as below.

```
$ macdaily update gem --help
usage: macdaily update gem [-h] [-qv] [-a] [-p PKG]

Update Installed Ruby Packages

optional arguments:
  -h, --help            show this help message and exit
  -a, --all             update all packages installed through gem
  -p PKG, --package PKG
                        name of packages to be updated, default is all
  -q, --quiet           run in quiet mode, with no output information
  -v, --verbose         run in verbose mode, with detailed output information
  --show-log            open log in Console upon completion of command
```

&emsp; If arguments omit, `macdaily` will __NOT__ update outdated packages of Ruby. And when using `-p` or `--package`, if given wrong package name, `macdaily` might give a trivial "did-you-mean" correction.

<a name="update_mas"> </a>

3. `mas` -- Mac App Store Application

&emsp; [MAS](https://github.com/mas-cli/mas#mas-cli) is a simple command line interface for the Mac App Store. The man page for [`macdaily update mas`] shows as below.

```
$ macdaily update mas --help
usage: macdaily update mas [-h] [-qv] [-a] [-p PKG]

Update Installed Mac App Store Packagess

optional arguments:
  -h, --help            show this help message and exit
  -a, --all             update all packages installed through Mac App Store
  -p PKG, --package PKG
                        name of packages to be updated, default is all
  -q, --quiet           run in quiet mode, with no output information
  -v, --verbose         run in verbose mode, with detailed output information
  --show-log            open log in Console upon completion of command
```

&emsp; If arguments omit, `macdaily` will __NOT__ update outdated packages of Ruby. And when using `-p` or `--package`, if given wrong package name, `macdaily` might give a trivial "did-you-mean" correction.

<a name="update_npm"> </a>

4. `npm` -- Node.js Module

&emsp; [Node.js](https://nodejs.org) provides a package manager called `npm`, i.e. "Node.js Package Manger". The man page for `macdaily update npm` shows as below.

```
$ macdaily update npm --help
usage: macdaily update npm [-h] [-qv] [-a] [-p PKG]

Update Installed Node.js Packages

optional arguments:
  -h, --help            show this help message and exit
  -a, --all             update all packages installed through gem
  -p PKG, --package PKG
                        name of packages to be updated, default is all
  -q, --quiet           run in quiet mode, with no output information
  -v, --verbose         run in verbose mode, with detailed output information
  --show-log            open log in Console upon completion of command
```

&emsp; If arguments omit, `macdaily` will __NOT__ update outdated packages of Ruby. And when using `-p` or `--package`, if given wrong package name, `macdaily` might give a trivial "did-you-mean" correction.

<a name="update_pip"> </a>

5. `pip` -- Python Package

&emsp; As there\'re all kinds and versions of Python complier, along with its `pip` package manager. Here, we support update of the following --

 - Python 2.\*/3.\* installed through Python official disk images (`*.dmg`)
 - Python 2/3 installed through `brew install python@2/python`
 - PyPy 2/3 installed through `brew install pypy/pypy3`

And the man page for `macdaily update pip` shows as below.

```
$ macdaily update pip --help
usage: macdaily update pip [-h] [-qv] [-bcsy] [-V VER] [-a] [-p PKG]

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
  --show-log            open log in Console upon completion of command
```

&emsp; If arguments omit, `macdaily` will __NOT__ update outdated packages in all copies of Python. And when using `-p` or `--package`, if given wrong package name, `macdaily` might give a trivial "did-you-mean" correction.

<a name="update_brew"> </a>

6. `brew` -- Homebrew Formula

&emsp; [Homebrew](https://brew.sh) is the missing package manager for macOS. The man page for `macdaily update brew` shows as below.

```
$ macdaily update brew --help
usage: macdaily update brew [-h] [-qv] [-fm] [-a] [-p PKG] [--no-cleanup]

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
  --show-log            open log in Console upon completion of command
```

 > __NOTE__ -- arguments `-f` and `--force`, `-m` and `--merge` are using only for `brew update` command

&emsp; If arguments omit, `macdaily` will __NOT__ update outdated packages of Homebrew. And when using `-p` or `--package`, if given wrong package name, `macdaily` might give a trivial "did-you-mean" correction.

<a name="update_cask"> </a>

7. `cask` -- Caskrooom Binary

&emsp; [Caskroom](https://caskroom.github.io) is a friendly binary installer for macOS. The man page for `macdaily update cask` shows as below.

```
$ macdaily update cask --help
usage: macdaily update cask [-h] [-qv] [-fg] [-a] [-p PKG] [--no-cleanup]

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
  --show-log            open log in Console upon completion of command
```

 > __NOTE__ -- arguments `-f` and `--force`, `-g` and `--greedy` are using only for `brew cask upgrade` command; and when the latter given, `macdaily` will directly run `brew cask upgrade --greedy`

&emsp; If arguments omit, `macdaily` will __NOT__ update outdated packages of Caskroom. And when using `-p` or `--package`, if given wrong package name, `macdaily` might give a trivial "did-you-mean" correction.

<a name="update_appstore"> </a>

8. `system` -- Mac App Store

&emsp; `softwareupdate` is the system software update tool. The man page for `macdaily update system` shows as below.

```
$ macdaily update system --help
usage: macdaily update system [-h] [-q] [-a] [-p PKG]

Update installed App Store packages

optional arguments:
  -h, --help            show this help message and exit
  -a, --all             update all packages installed through App Store
  -p PKG, --package PKG
                        name of packages to be updated, default is all
  -q, --quiet           run in quiet mode, with no output information
  --show-log            open log in Console upon completion of command
```

&emsp; If arguments omit, `macdaily` will __NOT__ update outdated packages in Mac App Store or `softwareupdate`. And when using `-p` or `--package`, if given wrong package name, `macdaily` might give a trivial "did-you-mean" correction.

<a name="update_cleanup"> </a>

9. `cleanup` -- Cleanup Procedure

&emsp; `cleanup` prunes and deduplicates files, archives and removes caches. The man page for `macdaily update cleanup` shows as below.

```
$ macdaily update cleanup --help
usage: macdaily update cleanup [-h] [-q] [--no-brew] [--no-cask]

Cleanup Caches & Downloads

optional arguments:
  -h, --help   show this help message and exit
  --no-gem     do not remove Ruby caches & downloads
  --no-npm     do not remove Node.js caches & downloads
  --no-pip     do not remove Python caches & downloads
  --no-brew    do not remove Homebrew caches & downloads
  --no-cask    do not remove Caskroom caches & downloads
  -q, --quiet  run in quiet mode, with no output information
  --show-log   open log in Console upon completion of command
```

&emsp; If arguments omit, `macdaily` will cleanup all caches as its default setup.

# MacDaily Uninstall Manual

 - [Python Package](#uninstall_pip)
 - [Homebrew Formula](#uninstall_brew)
 - [Caskroom Binary](#uninstall_cask)

---

<a name="uninstall_pip"> </a>

1. `pip` -- Python Package

&emsp; As there're several kinds and versions of Python complier, along with its `pip` package manager. Here, we support uninstall procedure in following --

 - Python 2.\*/3.\* installed through Python official disk images (`*.dmg`)
 - Python 2/3 installed through `brew install python@2/python`
 - PyPy 2/3 installed through `brew install pypy/pypy3`

&emsp; And the man page for `macdaily uninstall pip` shows as below.

```
$ macdaily uninstall pip --help
usage: macdaily uninstall pip [-h] [-qv] [-iY] [-bcsy] [-V VER] [-a] [-p PKG]

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
  --show-log            open log in Console upon completion of command
```

&emsp; If arguments omit, `macdaily` will __NOT__ uninstall packages in all copies of Python. And when using `-p` or `--package`, if given wrong package name, `macdaily` might give a trivial “did-you-mean” correction.

<a name="uninstall_brew"> </a>

2. `brew` -- Homebrew Formula

&emsp; [Homebrew](https://brew.sh) is the missing package manager for macOS. The man page for `macdaily uninstall brew` shows as below.

```
$ macdaily uninstall brew --help
usage: macdaily uninstall brew [-h] [-qv] [-iY] [-f] [-a] [-p PKG]

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
  --show-log            open log in Console upon completion of command
```

&emsp; If arguments omit, `macdaily` will __NOT__ uninstall packages of Homebrew. And when using `-p` or `--package`, if given wrong package name, `macdaily` might give a trivial “did-you-mean” correction.

<a name="uninstall_cask"> </a>

3. `cask` -- Caskrooom Binary

&emsp; [Caskroom](https://caskroom.github.io) is a friendly binary installer for macOS. The man page for `macdaily uninstall cask` shows as below.

```
$ macdaily uninstall cask --help
usage: macdaily uninstall cask [-h] [-qv] [-Y] [-f] [-a] [-p PKG]

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
  --show-log            open log in Console upon completion of command
```

&emsp; If arguments omit, `macdaily` will __NOT__ uninstall packages of Caskroom. And when using `-p` or `--package`, if given wrong package name, `macdaily` might give a trivial “did-you-mean” correction.

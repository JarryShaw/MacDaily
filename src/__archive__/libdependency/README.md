# MacDaily Dependency Manual

 - [Python Package](#dependency_pip)
 - [Homebrew Formula](#dependency_brew)

---

<a name="dependency_pip"> </a>

1. `pip` -- Python Package

&emsp; As there're several kinds and versions of Python complier, along with its `pip` package manager. Here, we support dependency procedure in following --

 - Python 2.\*/3.\* installed through Python official disk images (`*.dmg`)
 - Python 2/3 installed through `brew install python@2/python`
 - PyPy 2/3 installed through `brew install pypy/pypy3`

&emsp; And the man page for `macdaily dependency pip` shows as below.

```
$ macdaily dependency pip --help
usage: macdaily dependency pip [-h] [-qv] [-bcsy] [-V VER] [-a] [-p PKG]

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

&emsp; If arguments omit, `macdaily` will __NOT__ show package dependencies in all copies of Python. And when using `-p` or `--package`, if given wrong package name, `macdaily` might give a trivial “did-you-mean” correction.

<a name="dependency_brew"> </a>

2. `brew` -- Homebrew Formula

&emsp; [Homebrew](https://brew.sh) is the missing package manager for macOS. The man page for `macdaily dependency brew` shows as below.

```
$ macdaily dependency brew --help
usage: macdaily dependency brew [-h] [-t] [-a] [-p PKG]

Show Dependencies of Homebrew Packages

optional arguments:
  -h, --help            show this help message and exit
  -a, --all             show dependencies of all packages installed through
                        Homebrew
  -p PKG, --package PKG
                        name of packages to be shown, default is all
  -t, --tree            show dependencies as a tree
```

&emsp; If arguments omit, `macdaily` will __NOT__ show package dependencies of Homebrew. And when using `-p` or `--package`, if given wrong package name, `macdaily` might give a trivial “did-you-mean” correction.

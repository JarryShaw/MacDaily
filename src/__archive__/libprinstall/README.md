# MacDaily Reinstall & Postinstall Manual

 * [Reinstall Procedure](#reinstall)
    - [Homebrew Formula](#reinstall_brew)
    - [Caskroom Binary](#reinstall_cask)
    - [Cleanup Procedure](#reinstall_cleanup)
 * [Postinstall Procedure](#postinstall)
    - [Homebrew Formula](#postinstall_brew)
    - [Cleanup Procedure](#postinstall_cleanup)

---

<a name="reinstall"> </a>

## Reinstall Procedure

<a name="reinstall_brew"> </a>

1. `brew` -- Homebrew Formula

&emsp; [Homebrew](https://brew.sh) is the missing package manager for macOS. The man page for `macdaily reinstall brew` shows as below.

```
$ macdaily reinstall brew --help
usage: macdaily reinstall brew [-hV] [-qv] [-f] [-se PKG] [-a] [--[no-]MODE] MODE ...

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
  --show-log            open log in Console upon completion of command
```

&emsp; If arguments omit, `macdaily` will __NOT__ reinstall packages of Homebrew. And when using `-p` or `--package`, if given wrong package name, `macdaily` might give a trivial “did-you-mean” correction.

<a name="reinstall_cask"> </a>

2. `cask` -- Caskrooom Binary

&emsp; [Caskroom](https://caskroom.github.io) is a friendly binary installer for macOS. The man page for `macdaily reinstall cask` shows as below.

```
$ macdaily reinstall cask --help
usage: macdaily reinstall cask [-hV] [-qv] [-se PKG] [-a] [--[no-]MODE] MODE ...

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
  --show-log            open log in Console upon completion of command
```

&emsp; If arguments omit, `macdaily` will __NOT__ reinstall packages of Caskroom. And when using `-p` or `--package`, if given wrong package name, `macdaily` might give a trivial “did-you-mean” correction.

<a name="reinstall_cleanup"> </a>

3. `cleanup` -- Cleanup Procedure

&emsp; `cleanup` prunes and deduplicates files, archives and removes caches. The man page for `macdaily reinstall cleanup` shows as below.

```
$ macdaily update reinstall --help
usage: macdaily reinstall cleanup [-h] [-q] [--no-brew] [--no-cask]

Cleanup Caches & Downloads

optional arguments:
  -h, --help   show this help message and exit
  --no-brew    do not remove Homebrew caches & downloads
  --no-cask    do not remove Caskroom caches & downloads
  -q, --quiet  run in quiet mode, with no output information
  --show-log   open log in Console upon completion of command
```

&emsp; If arguments omit, `macdaily` will cleanup all caches as its default setup.

&nbsp;

<a name="postinstall"> </a>

## Postinstall Procedure

<a name="postinstall_brew"> </a>

1. `brew` -- Homebrew Formula

&emsp; [Homebrew](https://brew.sh) is the missing package manager for macOS. If arguments omit, `macdaily` will __NOT__ postinstall packages of Homebrew. And when using `-p` or `--package`, if given wrong package name, `macdaily` might give a trivial “did-you-mean” correction.

<a name="postinstall_cleanup"> </a>

2. `cleanup` -- Cleanup Procedure

&emsp; `cleanup` prunes and deduplicates files, archives and removes caches. If `--no-cleanup` option not set, `macdaily` will cleanup all caches as its default setup.

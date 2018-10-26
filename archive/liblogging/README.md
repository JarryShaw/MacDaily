# MacDaily Logging Manual

 - [Atom Plug-In](#logging_apm)
 - [Ruby Gem](#logging_gem)
 - [Node.js Module](#logging_npm)
 - [Python Package](#logging_pip)
 - [Homebrew Formula](#logging_brew)
 - [Caskroom Binary](#logging_cask)
 - [macOS Application](#logging_dotapp)
 - [Installed Application](#logging_macapp)
 - [Mac App Store](#logging_appstore)

---

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

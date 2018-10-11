# MacDaily Bundle Manual

 - [What is a `Macfile`?](#macfile)
 - [Dump Macfile](#bundle_dump)
 - [Load Macfile](#bundle_load)

---

<a name="macfile"> </a>

### What is a `Macfile`?

&emsp; Alike [`Brewfile`](https://github.com/Homebrew/homebrew-bundle#homebrew-bundle), a `Macfile` is a text file designed to keep track of all packages installed on your Mac. By now, a `Macfile` may contain packages installed through --

 - `apm` -- [Atom](https://atom.io) plug-ins
 - `gem` -- [Ruby](https://www.ruby-lang.org) gems
 - `mas` -- [Mac App Store](https://github.com/mas-cli/mas#mas-cli) applications
 - `npm` -- [Node.js](https://nodejs.org) modules
 - `pip` -- Python packages, in both version of 2.\* and 3.\*, running under [CPython](https://www.python.org) or [PyPy](https://pypy.org) compiler, and installed through `brew` or official disk images (`*.dmg`)
 - `tap` -- [Taps](https://docs.brew.sh/Taps), third-party repositories for [Homebrew](https://brew.sh) formulae
 - `brew` -- [Homebrew](https://brew.sh) formulae
 - `cask` -- [Caskroom](https://caskroom.github.io) binaries

&nbsp;

<a name="bundle_dump"> </a>

&emsp; Simply dump a `Macfile` into `~/.Macfile`. More options are coming...

### Dump Macfile

&nbsp;

<a name="bundle_load"> </a>

### Load Macfile

&emsp; Load `~/.Macfile` and reinstall all packages described in the file. More options are coming...

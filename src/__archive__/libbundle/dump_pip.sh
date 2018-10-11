#!/bin/bash


# parameter assignment
verbose=$1


# dump procedure
#   dump_pip executable pprint
function dump_pip() {
    local executable=$1
    local pprint=$2

    if [ -e $executable ] ; then
        if ( $verbose ) ; then
            list=`$executable -m pip freeze 2> /dev/null | sed "s/\(.*\)*==.*/\1/" | sort | uniq | xargs`
            for name in $list ; do
                $executable -m pip show $name 2> /dev/null | grep "Summary: " | cut -c 10- | sed "s/^/# /"
                version=`$executable -m pip show $name 2> /dev/null | grep "Version: " | cut -c 10-`
                echo -e $pprint \"$name\", version: $version
            done
        else
            $executable -m pip freeze 2> /dev/null | sed "s/\(.*\)*==\(.*\)*/$pprint \"\1\", version: \2/" | sort | uniq >> ~/.Macfile
        fi
    fi
}


# CPython 2.* installed from installer
dump_pip "/Library/Frameworks/Python.framework/Versions/2.0/bin/python2.0" "pip2.0"
dump_pip "/Library/Frameworks/Python.framework/Versions/2.1/bin/python2.1" "pip2.1"
dump_pip "/Library/Frameworks/Python.framework/Versions/2.2/bin/python2.2" "pip2.2"
dump_pip "/Library/Frameworks/Python.framework/Versions/2.3/bin/python2.3" "pip2.3"
dump_pip "/Library/Frameworks/Python.framework/Versions/2.4/bin/python2.4" "pip2.4"
dump_pip "/Library/Frameworks/Python.framework/Versions/2.5/bin/python2.5" "pip2.5"
dump_pip "/Library/Frameworks/Python.framework/Versions/2.6/bin/python2.6" "pip2.6"
dump_pip "/Library/Frameworks/Python.framework/Versions/2.7/bin/python2.7" "pip2.7"

# CPython 3.* installed from installer
dump_pip "/Library/Frameworks/Python.framework/Versions/3.0/bin/python3.0" "pip3.0"
dump_pip "/Library/Frameworks/Python.framework/Versions/3.1/bin/python3.1" "pip3.1"
dump_pip "/Library/Frameworks/Python.framework/Versions/3.2/bin/python3.2" "pip3.2"
dump_pip "/Library/Frameworks/Python.framework/Versions/3.3/bin/python3.3" "pip3.3"
dump_pip "/Library/Frameworks/Python.framework/Versions/3.4/bin/python3.4" "pip3.4"
dump_pip "/Library/Frameworks/Python.framework/Versions/3.5/bin/python3.5" "pip3.5"
dump_pip "/Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6" "pip3.6"
dump_pip "/Library/Frameworks/Python.framework/Versions/3.7/bin/python3.7" "pip3.7"

# CPython 2.* installed from Homebrew
brew link python@2 --force > /dev/null 2>&1
dump_pip "/usr/local/opt/python@2/bin/python2" "pip2"

# CPython 3.* installed from Homebrew
brew link python > /dev/null 2>&1
dump_pip "/usr/local/opt/python@3/bin/python3" "pip3"

# PyPy 2.* installed from Homebrew
brew link pypy > /dev/null 2>&1
dump_pip "/usr/local/opt/pypy/bin/pypy" "pip_pypy"

# PyPy 3.* installed from Homebrew
brew link pypy3 > /dev/null 2>&1
dump_pip "/usr/local/opt/pypy3/bin/pypy3" "pip_pypy3"

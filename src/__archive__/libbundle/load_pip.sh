#!/bin/bash


# terminal display
reset="\033[0m"         # reset
under="\033[4m"         # underline
flash="\033[5m"         # flash
red="\033[91m"          # bright red foreground
blush="\033[101m"       # bright red background
purple="\033[104m"      # bright purple background


# parameter assignment
line=$1


# check Python version & implementation
pip=`sed "s/\(pip[_a-z0-9.]*\) .*/\1/" <<< $line`


# fetch corresponding binary path
case $pip in
	"pip2.0" )
        prefix="/Library/Frameworks/Python.framework/Versions/2.0/bin"
        suffix="python2.0"
        pprint="2.0" ;;
    "pip2.1" )
        prefix="/Library/Frameworks/Python.framework/Versions/2.1/bin"
        suffix="python2.1"
        pprint="2.1" ;;
    "pip2.2" )
        prefix="/Library/Frameworks/Python.framework/Versions/2.2/bin"
        suffix="python2.2"
        pprint="2.2" ;;
    "pip2.3" )
        prefix="/Library/Frameworks/Python.framework/Versions/2.3/bin"
        suffix="python2.3"
        pprint="2.3" ;;
    "pip2.4" )
        prefix="/Library/Frameworks/Python.framework/Versions/2.4/bin"
        suffix="python2.4"
        pprint="2.4" ;;
    "pip2.5" )
        prefix="/Library/Frameworks/Python.framework/Versions/2.5/bin"
        suffix="python2.5"
        pprint="2.5" ;;
    "pip2.6" )
        prefix="/Library/Frameworks/Python.framework/Versions/2.6/bin"
        suffix="python2.6"
        pprint="2.6" ;;
    "pip2.7" )
        prefix="/Library/Frameworks/Python.framework/Versions/2.7/bin"
        suffix="python2.7"
        pprint="2.7" ;;
    "pip3.0" )
        prefix="/Library/Frameworks/Python.framework/Versions/3.0/bin"
        suffix="python3.0"
        pprint="3.0" ;;
    "pip3.1" )
        prefix="/Library/Frameworks/Python.framework/Versions/3.1/bin"
        suffix="python3.1"
        pprint="3.1" ;;
    "pip3.2" )
        prefix="/Library/Frameworks/Python.framework/Versions/3.2/bin"
        suffix="python3.2"
        pprint="3.2" ;;
    "pip3.3" )
        prefix="/Library/Frameworks/Python.framework/Versions/3.3/bin"
        suffix="python3.3"
        pprint="3.3" ;;
    "pip3.4" )
        prefix="/Library/Frameworks/Python.framework/Versions/3.4/bin"
        suffix="python3.4"
        pprint="3.4" ;;
    "pip3.5" )
        prefix="/Library/Frameworks/Python.framework/Versions/3.5/bin"
        suffix="python3.5"
        pprint="3.5" ;;
    "pip3.6" )
        prefix="/Library/Frameworks/Python.framework/Versions/3.6/bin"
        suffix="python3.6"
        pprint="3.6" ;;
    "pip3.7" )
        prefix="/Library/Frameworks/Python.framework/Versions/3.7/bin"
        suffix="python3.7"
        pprint="3.7" ;;
    "pip2" )
        prefix="/usr/local/opt/python@2/bin"
        suffix="python2"
        pprint="2"
        # link brewed python@2
        brew link python@2 --force > /dev/null 2>&1 ;;
    "pip3" )
        prefix="/usr/local/opt/python@3/bin"
        suffix="python3"
        pprint="3"
        # link brewed python
        brew link python > /dev/null 2>&1 ;;
    "pip_pypy" )
        prefix="/usr/local/opt/pypy/bin"
        suffix="pypy"
        pprint="_pypy"
        # link brewed pypy
        brew link pypy > /dev/null 2>&1 ;;
    "pip_pypy3" )
        prefix="/usr/local/opt/pypy3/bin"
        suffix="pypy3"
        pprint="_pypy3"
        # link brewed pypy3
        brew link pypy3 > /dev/null 2>&1 ;;
    * )
        exit 1 ;;
esac


# make package name
package=`
python << EOF
# split line
line = '$line'
prefix, suffix = line.split(', ', 1)

# fetch name & version
name = prefix.split(' ', 1)[1][1:-1]
version = suffix.split(': ', 1)[1]

# print package name
print('%s==%s' % (name, version))
EOF
`


# reinstall package
echo "+ pip$pprint install $package"
sudo -H $prefix/$suffix -m pip install $package
echo

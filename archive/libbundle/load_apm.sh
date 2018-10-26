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


# check apm installed
which apm > /dev/null 2>&1
if [ $? -ne 0 ] ; then
    echo -e "bundle: ${blush}${flash}apm${reset}: command not found"
    echo -e "bundle: ${red}apm${reset}: you may download Atom from ${purple}${under}https://atom.io${reset}"
    exit 1
fi


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
print('%s@%s' % (name, version))
EOF
`

# reinstall package
echo "+ apm install $package"
apm install $package
echo

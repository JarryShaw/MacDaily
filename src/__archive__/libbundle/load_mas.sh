#!/bin/bash


# terminal display
reset="\033[0m"         # reset
flash="\033[5m"         # flash
red="\033[91m"          # bright red foreground
blush="\033[101m"       # bright red background


# parameter assignment
line=$1


# check mas installed
which mas > /dev/null 2>&1
if [ $? -ne 0 ] ; then
    echo -e "bundle: ${blush}${flash}mas${reset}: command not found"
    echo -e "bundle: ${red}mas${reset}: you may download MAS through following command --\`${bold}brew install mas${reset}\`"
    exit 1
fi


# make package name
package=`
python << EOF
# split line
line = '$line'
prefix, suffix = line.split(', ', 1)

# fetch name & version
# name = prefix.split(' ', 1)[1][1:-1]
version = suffix.split(': ', 1)[1]

# print package name
print(version)
EOF
`

# reinstall package
echo "+ mas install $package"
mas install $package
echo

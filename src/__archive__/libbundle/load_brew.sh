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


# check brew installed
which brew > /dev/null 2>&1
if [ $? -ne 0 ] ; then
    echo -e "bundle: ${blush}${flash}tap${reset}: command not found"
    echo -e -n "bundle: ${red}tap${reset}: you may find Homebrew on ${purple}${under}https://brew.sh${reset}, "
    echo -e -n "or install Homebrew through following command -- "
    echo -e "\`{bold}/usr/bin/ruby -e \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)${reset}\"\`"
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
# version = suffix.split(': ', 1)[1]

# print package name
print(name)
EOF
`

# reinstall package
echo "+ brew install $package"
brew install $package
echo

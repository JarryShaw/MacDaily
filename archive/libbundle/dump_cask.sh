#!/bin/bash


# parameter assignment
verbose=$1


# check cask installed
brew cask > /dev/null 2>&1
if [ $? -ne 0 ] ; then
    exit 1
fi


# dump procedure
if ( $verbose ) ; then
    # fetch description for verbose output
    list=`brew cask list 2> /dev/null | sort | uniq | xargs`
    for name in $list ; do
        brew cask info $name 2> /dev/null | awk "NR==6" | sed "s/^/# /" >> ~/.Macfile
        version=`brew cask list $name --versions 2> /dev/null | sed "s/.* \(.*\)*/\1/"`
        echo -e cask \"$name\", version: $version >> ~/.Macfile
    done
else
    brew cask list --versions 2> /dev/null | sed "s/\(.*\)* \(.*\)*/cask \"\1\", version: \2/" | sort | uniq >> ~/.Macfile
fi

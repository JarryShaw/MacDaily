#!/bin/bash


# parameter assignment
verbose=$1


# check brew installed
which brew > /dev/null 2>&1
if [ $? -ne 0 ] ; then
    exit 1
fi


# dump procedure
if ( $verbose ) ; then
    # fetch description for verbose output
    list=`brew list 2> /dev/null | sort | uniq | xargs`
    for name in $list ; do
        brew info $name 2> /dev/null | awk "NR==2" | sed "s/^/# /" >> ~/.Macfile
        version=`brew list $name --versions 2> /dev/null | sed "s/.* \(.*\)*/\1/"`
        echo -e brew \"$name\", version: $version >> ~/.Macfile
    done
else
    brew list --versions 2> /dev/null | sed "s/\(.*\)* \(.*\)*/brew \"\1\", version: \2/" | sort | uniq >> ~/.Macfile
fi

#!/bin/bash


# parameter assignment
verbose=$1


# check npm installed
which npm > /dev/null 2>&1
if [ $? -ne 0 ] ; then
    exit 1
fi


# dump procedure
if ( $verbose ) ; then
    # fetch description for verbose output
    list=`npm list --global --parseable 2> /dev/null | sed "s/.*\/\([[:print:]]*\)*/\1/" | sort | uniq | xargs`
    for name in $list ; do
        npm view $name description 2> /dev/null | sed "s/^/# /" >> ~/.Macfile
        version=`npm view $name version 2> /dev/null`
        echo -e npm \"$name\", version: $version >> ~/.Macfile
    done
else
    npm list --global 2> /dev/null | grep '@' | sed "s/.* \(.*\)@\([0-9.]*\).*/npm \"\1\", version: \2/" | sort | uniq >> ~/.Macfile
fi

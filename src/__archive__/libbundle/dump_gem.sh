#!/bin/bash


# parameter assignment
verbose=$1


# check gem installed
which gem > /dev/null 2>&1
if [ $? -ne 0 ] ; then
    exit 1
fi


# dump procedure
if ( $verbose ) ; then
    # fetch description for verbose output
    list=`gem list 2> /dev/null | sed "s/\(.*\)* (.*)/\1/" | sort | uniq | xargs`
    for name in $list ; do
        gem list $name --detail 2> /dev/null | tail -1 | sed "s/    /# /" >> ~/.Macfile
        version=`gem list 2> /dev/null | grep $name | sed "s/\(.*\)* (\(default: \)*\([0-9.]*\)*.*)/\3/"`
        echo -e gem \"$name\", version: $version >> ~/.Macfile
    done
else
    gem list 2> /dev/null | sed "s/\(.*\)* (\(default: \)*\([0-9.]*\)*.*)/gem \"\1\", version: \3/" | sort | uniq >> ~/.Macfile
fi

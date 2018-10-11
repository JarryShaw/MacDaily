#!/bin/bash


# parameter assignment
verbose=$1


# check mas installed
which mas > /dev/null 2>&1
if [ $? -ne 0 ] ; then
    exit 1
fi


# dump procedure
if ( $verbose ) ; then
    # fetch description for verbose output
    list=`mas list 2> /dev/null | sed "s/\([0-9]*\)* .*/\1/" | sort | uniq | xargs`
    for temp in $list ; do
        mas info $temp 2> /dev/null | head -1 | sed "s/^/# /" >> ~/.Macfile
        name=`mas list 2> /dev/null | grep $temp | sed "s/[0-9]* \(.*\)* ([0-9.]*)/\1/"`
        echo -e mas \"$name\", id: $temp >> ~/.Macfile
    done
else
    mas list 2> /dev/null | sed "s/\([0-9]*\)* \([[:print:]]*\)* ([0-9.]*)/mas \"\2\", id: \1/" | sort | uniq >> ~/.Macfile
fi

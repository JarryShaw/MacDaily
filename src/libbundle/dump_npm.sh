# #!/bin/bash


# parameter assignment
arg_v=$1


# dump procedure
if ( $arg_v ) ; then
    # fetch description for verbose output
    list=`npm list --global --parseable 2> /dev/null | sed "s/.*\/\([[:print:]]*\)*/\1/" | sort | uniq | xargs`
    for name in $list ; do
        npm view $name description | sed "s/^/# /" >> ~/.Macfile
        echo npm "$name" >> ~/.Macfile
    done
else
    npm list --global --parseable 2> /dev/null | sed "s/.*\/\([[:print:]]*\)*/npm \"\1\"/" | sort | uniq >> ~/.Macfile
fi

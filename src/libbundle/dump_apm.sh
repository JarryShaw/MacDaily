# #!/bin/bash


# parameter assignment
arg_v=$1


# dump procedure
if ( $arg_v ) ; then
    # fetch description for verbose output
    list=`apm list --bare 2> /dev/null | sed "s/\(.*\)*@.*/\1/" | sort | uniq | xargs`
    for name in $list ; do
        apm show $name | awk "NR==4" | sed "s/├── /# /" >> ~/.Macfile
        echo apm "$name" >> ~/.Macfile
    done
else
    apm list --bare 2> /dev/null | grep '@' | sed "s/\(.*\)*@.*/apm: \"\1\"/" | sort | uniq >> ~/.Macfile
fi

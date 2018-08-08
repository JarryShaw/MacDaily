# #!/bin/bash


# parameter assignment
arg_v=$1


# dump procedure
if ( $arg_v ) ; then
	# fetch description for verbose output
	list=`gem list 2>/dev/null | sed "s/\(.*\)* (.*)/\1/" | sort | uniq | xargs`
	for name in $list ; do
		gem list $name --detail | tail -1 | sed "s/    /# /" >> ~/.Macfile
		echo gem "$name" >> ~/.Macfile
	done
else
	gem list 2>/dev/null | sed "s/\(.*\)* (.*)/gem \"\1\"/" | sort | uniq >> ~/.Macfile
fi

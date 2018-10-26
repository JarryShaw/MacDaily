#!/bin/bash


# parameter assignment
verbose=$1


# cleanup Macfile
> ~/.Macfile


# start dump procedure
for mode in apm brew cask gem mas npm pip tap ; do
    path=`python -c "import os; print(os.path.join(os.path.dirname(os.path.abspath('$0')), 'dump_${mode}.sh'))"`
    bash $path $verbose
done

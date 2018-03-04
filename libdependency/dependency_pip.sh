#!/bin/bash


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1


# preset terminal output colours
blush="tput setaf 1"    # blush / red
green="tput setaf 2"    # green
reset="tput sgr0"       # reset


################################################################################
# Show Python site packages dependencies.
#
# Parameter list:
#   1. Log Date
#   2. System Flag
#   3. Cellar Flag
#   4. CPython Flag
#   5. PyPy Flag
#   6. Version
#       |-> 1 : Both
#       |-> 2 : Python 2.*
#       |-> 3 : Python 3.*
#   7. Tree Flag
#   8. Package
#       ............
################################################################################


# parameter assignment
logdate=$1
arg_s=$2
arg_b=$3
arg_c=$4
arg_y=$5
arg_V=$6
arg_t=$7
arg_pkg=${*:8}


# log file prepare
logfile="/Library/Logs/Scripts/dependency/$logdate.log"
tmpfile="/tmp/log/dependency.log"


# remove /tmp/log/dependency.log
rm -f $tmpfile


# create /tmp/log/dependency.log & /Library/Logs/Scripts/dependency/logdate.log
touch $logfile
touch $tmpfile


# log current status
echo "- /bin/bash $0 $@" >> $tmpfile


# log commands
# usage: $logprefix [command] | logcattee | logsuffix
logprefix="script -q /dev/null"
logcattee="tee -a $tmpfile"
logsuffix="grep ^.*$"


# pip dependency function usage:
#   pipdependency package python pip-suffix pip-suffix pip-pprint
function pipdependency {
    # parameter assignment
    local arg_pkg=$1
    local python=$2
    local prefix=$3
    local suffix=$4
    local pprint=$5

    # log function call
    echo "+ pipdependency $@" >> $tmpfile

    # if tree flag set
    if ( $arg_t ) ; then
        # check if `pipdeptree` installed
        if $python -m pipdeptree > /dev/null 2>&1 ; then
            case $arg_pkg in
                all)
                    $logprefix echo "++ pipdeptree$pprint" | $logcattee | $logsuffix
                    $logprefix pipdeptree$pprint | $logcattee | $logsuffix
                    $logprefix echo | $logcattee | $logsuffix ;;
                *)
                    $logprefix echo "++ pipdeptree$pprint -p $arg_pkg" | $logcattee | $logsuffix
                    $logprefix pipdeptree$pprint -p $arg_pkg | $logcattee | $logsuffix
                    $logprefix echo | $logcattee | $logsuffix ;;
            esac
        else
            $blush
            $logprefix echo "Error: Package pipdeptree not installed on pip$pprint." | $logcattee | $logsuffix
            $reset
            $logprefix echo | $logcattee | $logsuffix
        fi
    else
        $logprefix echo "++ pip$pprint show $arg_pkg | grep \"Requires: \" | sed \"s/Requires: //\" | sed \"s/,//g\" | tr \" \" \"\n\"" | $logcattee | $logsuffix
        $logprefix $prefix/pip$suffix show $arg_pkg | grep "Requires: " | sed "s/Requires: //" | sed "s/,//g" | tr " " "\n" | $logcattee | $logsuffix
        $logprefix echo | $logcattee | $logsuffix
    fi
}


# pip logging function usage:
#   piplogging mode
function piplogging {
    # parameter assignment
    mode=$1

    # log function call
    echo "+ piplogging $@" >> $tmpfile

    # make prefix & suffix of pip
    case $mode in
        1)  # pip_sys
            python="/Library/Frameworks/Python.framework/Versions/2.7/bin/python2.7"
            prefix="/Library/Frameworks/Python.framework/Versions/2.7/bin"
            suffix=""
            pprint="_sys" ;;
        2)  # pip_sys3
            python="/Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6"
            prefix="/Library/Frameworks/Python.framework/Versions/3.6/bin"
            suffix="3"
            pprint="_sys3" ;;
        3)  # pip
            python="/usr/local/opt/python2/bin/python2"
            prefix="/usr/local/opt/python2/bin"
            suffix=""
            pprint="" ;;
        4)  # pip3
            python="/usr/local/opt/python3/bin/python3"
            prefix="/usr/local/opt/python3/bin"
            suffix="3"
            pprint="3" ;;
        5)  # pip_pypy
            python="/usr/local/opt/pypy2/bin/pypy"
            prefix="/usr/local/opt/pypy2/bin"
            suffix="_pypy"
            pprint="_pypy" ;;
        6)  # pip_pypy3
            python="/usr/local/opt/pypy3/bin/pypy3"
            prefix="/usr/local/opt/pypy3/bin"
            suffix="_pypy3"
            pprint="_pypy3" ;;
    esac

    # if tree flag set
    if ( $arg_t ) ; then
        # check if executive of pipdeptree exists
        pipdeptree="/usr/local/bin/pipdeptree$pprint"
        if [ ! -e $pipdeptree ] ; then
            touch $pipdeptree
            echo "#!$python" >> $pipdeptree
            cat libdependency/pipdeptree.py >> $pipdeptree
        fi
    fi

    # if executive exits
    if [ -e $prefix/pip$suffix ] ; then
        for name in $arg_pkg ; do
            # All or Specified Packages
            case $name in
                all)
                    # if tree flag set
                    if ( $arg_t ) ; then
                        list="all"
                    else
                        # list=`pipdeptree$pprint | grep -e "==" | grep -v "required"`
                        list=`$prefix/pip$suffix list --format legacy | sed "s/\(.*\)* (.*).*/\1/"`
                    fi

                    for pkg in $list ; do
                        pipdependency $pkg $python $prefix $suffix $pprint
                    done ;;
                *)
                    flag=`$prefix/pip$suffix list --format legacy | sed "s/\(.*\)* (.*).*/\1/" | awk "/^$name$/"`
                    if [[ -nz $flag ]]; then
                        pipdependency $name $python $prefix $suffix $pprint
                    else
                        $blush
                        $logprefix echo "Error: No pip$pprint package names $name installed." | $logcattee | $logsuffix
                        $reset

                        # did you mean
                        dym=`$prefix/pip$suffix list --format legacy | sed "s/\(.*\)* (.*).*/\1/" | grep $name | xargs | sed "s/ /, /g"`
                        if [[ -nz $dym ]] ; then
                            $logprefix echo "Did you mean any of the following packages: $dym?" | $logcattee | $logsuffix
                        fi
                        $logprefix echo | $logcattee | $logsuffix
                    fi ;;
            esac
        done
    else
        echo -e "pip$pprint: Not installed.\n" >> $tmpfile
    fi
}


# preset all mode bools
mode_pip_sys=false      # 2.* / system / cpython
mode_pip_sys3=false     # 3.* / system / cpython
mode_pip=false          # 2.* / cellar / cpython
mode_pip3=false         # 3.* / cellar / cpython
mode_pip_pypy=false     # 2.* / cellar / pypy
mode_pip_pypy3=false    # 3.* / cellar / pypy


# if system flag set
if ( $arg_s ) ; then
    case $arg_V in
        1)  mode_pip_sys=true
            mode_pip_sys3=true ;;
        2)  mode_pip_sys=true ;;
        3)  mode_pip_sys3=true ;;
    esac
fi


# if cellar flag set
if ( $arg_b ) ; then
    case $arg_V in
        1)  mode_pip=true
            mode_pip3=true
            mode_pip_pypy=true
            mode_pip_pypy3=true ;;
        2)  mode_pip=true
            mode_pip_pypy=true ;;
        3)  mode_pip3=true
            mode_pip_pypy3=true ;;
    esac
fi


# if cpython flag set
if ( $arg_c ) ; then
    case $arg_V in
        1)  mode_pip_sys=true
            mode_pip_sys3=true
            mode_pip=true
            mode_pip3=true ;;
        2)  mode_pip_sys=true
            mode_pip=true ;;
        3)  mode_pip_sys3=true
            mode_pip3=true ;;
    esac
fi


# if pypy flag set
if ( $arg_y ) ; then
    case $arg_V in
        1)  mode_pip_pypy=true
            mode_pip_pypy3=true ;;
        2)  mode_pip_pypy=true ;;
        3)  mode_pip_pypy3=true ;;
    esac
fi


# call piplogging function according to modes
list=( [1]=$mode_pip_sys $mode_pip_sys3 $mode_pip $mode_pip3 $mode_pip_pypy $mode_pip_pypy3 )
for index in ${!list[*]} ; do
    if ( ${list[$index]} ) ; then
        piplogging $index
    fi
done


# read /tmp/log/dependency.log line by line then migrate to log file
while read -r line ; do
    # plus `+` proceeds in line
    if [[ $line =~ ^(\+\+*\ )(.*)$ ]] ; then
        # add "+" in the beginning, then write to /Library/Logs/Scripts/dependency/logdate.log
        echo "+$line" >> $logfile
    # minus `-` proceeds in line
    elif [[ $line =~ ^(-\ )(.*)$ ]] ; then
        # replace "-" with "+", then write to /Library/Logs/Scripts/dependency/logdate.log
        echo "$line" | sed "y/-/+/" >> $logfile
    # colon `:` in line
    elif [[ $line =~ ^([[:alnum:]][[:alnum:]]*)(:)(.*)$ ]] ; then
        # if this is a warning
        if [[ $( tr "[:upper:]" "[:lower:]" <<< $line ) =~ ^([[:alnum:]][[:alnum:]]*:\ )(.*)(warning:\ )(.*) ]] ; then
            # log tag
            prefix="WAR"
            # log content
            suffix=`echo $line | sed "s/\[[0-9][0-9]*m//g" | sed "s/warning: //"`
        # if this is an error
        elif [[ $( tr "[:upper:]" "[:lower:]" <<< $line ) =~ ^([[:alnum:]][[:alnum:]]*:\ )(.*)(error:\ )(.*)$ ]] ; then
            # log tag
            prefix="ERR"
            # log content
            suffix=`echo $line | sed "s/\[[0-9][0-9]*m//g" | sed "s/error: //"`
        # if this is asking for password
        elif [[ $line =~ ^(Password:)(.*) ]] ; then
            # log tag
            prefix="PWD"
            # log content
            suffix="content hidden due to security reasons"
        # otherwise, extract its own tag
        else
            # log tag
            prefix=`echo $line | sed "s/\[[0-9][0-9]*m//g" | sed "s/\(.*\)*:\ .*/\1/" | cut -c 1-3 | tr "[:lower:]" "[:upper:]"`
            # log content
            suffix=`echo $line | sed "s/\[[0-9][0-9]*m//g" | sed "s/.*:\ \(.*\)*.*/\1/"`
        fi
        # write to /Library/Logs/Scripts/dependency/logdate.log
        echo "$prefix: $suffix" >> $logfile
    # colourised `[??m` line
    elif [[ $line =~ ^(.*)(\[[0-9][0-9]*m)(.*)$ ]] ; then
        # error (red/[31m) line
        if [[ $line =~ ^(.*)(\[31m)(.*)$ ]] ; then
            # add `ERR` tag and remove special characters then write to /Library/Logs/Scripts/dependency/logdate.log
            echo "ERR: $line" | sed "s/\[[0-9][0-9]*m//g" >> $logfile
        # warning (yellow/[33m)
        elif [[ $line =~ ^(.*)(\[33m)(.*)$ ]] ; then
            # add `WAR` tag and remove special characters then write to /Library/Logs/Scripts/dependency/logdate.log
            echo "WAR: $line" | sed "s/\[[0-9][0-9]*m//g" >> $logfile
        # other colourised line
        else
            # add `INF` tag and remove special characters then write to /Library/Logs/Scripts/dependency/logdate.log
            echo "INF: $line" | sed "s/\[[0-9][0-9]*m//g" >> $logfile
        fi
    # empty / blank line
    elif [[ $line =~ ^([[:space:]]*)$ ]] ; then
        # directlywrite to /Library/Logs/Scripts/dependency/logdate.log
        echo $line >> $logfile
    # non-empty line
    else
        # add `OUT` tag, remove special characters and discard flushed lines then write to /Library/Logs/Scripts/dependency/logdate.log
        echo "OUT: $line" | sed "s/\[\?[0-9][0-9]*[a-zA-Z]//g" | sed "/\[[A-Z]/d" | sed "/##*\ \ *.*%/d" >> $logfile
    fi
done < $tmpfile


# remove /tmp/log/dependency.log
rm -f $tmpfile


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1

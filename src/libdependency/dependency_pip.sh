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
#       |-> 1  : All
#       |-> 2  : Python 2.*
#       |-> 20 : Python 2.0.*
#       |-> 21 : Python 2.1.*
#       |-> 22 : Python 2.2.*
#       |-> 23 : Python 2.3.*
#       |-> 24 : Python 2.4.*
#       |-> 25 : Python 2.5.*
#       |-> 26 : Python 2.6.*
#       |-> 27 : Python 2.7.*
#       |-> 3  : Python 3.*
#       |-> 31 : Python 3.1.*
#       |-> 32 : Python 3.2.*
#       |-> 33 : Python 3.3.*
#       |-> 34 : Python 3.4.*
#       |-> 35 : Python 3.5.*
#       |-> 36 : Python 3.6.*
#       |-> 37 : Python 3.7.*
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
        1)  # pip2.0
            python="/Library/Frameworks/Python.framework/Versions/2.0/bin/python2.0"
            prefix="/Library/Frameworks/Python.framework/Versions/2.0/bin"
            suffix="2.0"
            pprint="2.0" ;;
            2)  # pip2.1
            python="/Library/Frameworks/Python.framework/Versions/2.1/bin/python2.1"
            prefix="/Library/Frameworks/Python.framework/Versions/2.1/bin"
            suffix="2.1"
            pprint="2.1" ;;
        3)  # pip2.2
            python="/Library/Frameworks/Python.framework/Versions/2.2/bin/python2.2"
            prefix="/Library/Frameworks/Python.framework/Versions/2.2/bin"
            suffix="2.2"
            pprint="2.2" ;;
        4)  # pip2.3
            python="/Library/Frameworks/Python.framework/Versions/2.3/bin/python2.3"
            prefix="/Library/Frameworks/Python.framework/Versions/2.3/bin"
            suffix="2.3"
            pprint="2.3" ;;
        5)  # pip2.4
            python="/Library/Frameworks/Python.framework/Versions/2.4/bin/python2.4"
            prefix="/Library/Frameworks/Python.framework/Versions/2.4/bin"
            suffix="2.4"
            pprint="2.4" ;;
        6)  # pip2.5
            python="/Library/Frameworks/Python.framework/Versions/2.5/bin/python2.5"
            prefix="/Library/Frameworks/Python.framework/Versions/2.5/bin"
            suffix="2.5"
            pprint="2.5" ;;
        7)  # pip2.6
            python="/Library/Frameworks/Python.framework/Versions/2.6/bin/python2.6"
            prefix="/Library/Frameworks/Python.framework/Versions/2.6/bin"
            suffix="2.6"
            pprint="2.6" ;;
        8)  # pip2.7
            python="/Library/Frameworks/Python.framework/Versions/2.7/bin/python2.7"
            prefix="/Library/Frameworks/Python.framework/Versions/2.7/bin"
            suffix="2.7"
            pprint="2.7" ;;
        9)  # pip3.0
            python="/Library/Frameworks/Python.framework/Versions/3.0/bin/python3.0"
            prefix="/Library/Frameworks/Python.framework/Versions/3.0/bin"
            suffix="3.0"
            pprint="3.0" ;;
        10)  # pip3.1
            python="/Library/Frameworks/Python.framework/Versions/3.1/bin/python3.1"
            prefix="/Library/Frameworks/Python.framework/Versions/3.1/bin"
            suffix="3.1"
            pprint="3.1" ;;
        11)  # pip3.2
            python="/Library/Frameworks/Python.framework/Versions/3.2/bin/python3.2"
            prefix="/Library/Frameworks/Python.framework/Versions/3.2/bin"
            suffix="3.2"
            pprint="3.2" ;;
        12)  # pip3.3
            python="/Library/Frameworks/Python.framework/Versions/3.3/bin/python3.3"
            prefix="/Library/Frameworks/Python.framework/Versions/3.3/bin"
            suffix="3.3"
            pprint="3.3" ;;
        13)  # pip3.4
            python="/Library/Frameworks/Python.framework/Versions/3.4/bin/python3.4"
            prefix="/Library/Frameworks/Python.framework/Versions/3.4/bin"
            suffix="3.4"
            pprint="3.4" ;;
        14)  # pip3.5
            python="/Library/Frameworks/Python.framework/Versions/3.5/bin/python3.5"
            prefix="/Library/Frameworks/Python.framework/Versions/3.5/bin"
            suffix="3.5"
            pprint="3.5" ;;
        15)  # pip3.6
            python="/Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6"
            prefix="/Library/Frameworks/Python.framework/Versions/3.6/bin"
            suffix="3.6"
            pprint="3.6" ;;
        16)  # pip3.7
            python="/Library/Frameworks/Python.framework/Versions/3.7/bin/python3.7"
            prefix="/Library/Frameworks/Python.framework/Versions/3.7/bin"
            suffix="3.7"
            pprint="3.7" ;;
        17)  # pip2
            python="/usr/local/opt/python@2/bin/python2"
            prefix="/usr/local/opt/python@2/bin"
            suffix="2"
            pprint="2" ;;
        18)  # pip3
            python="/usr/local/opt/python@3/bin/python3"
            prefix="/usr/local/opt/python@3/bin"
            suffix="3"
            pprint="3" ;;
        19)  # pip_pypy
            python="/usr/local/opt/pypy/bin/pypy"
            prefix="/usr/local/opt/pypy/bin"
            suffix="_pypy"
            pprint="_pypy" ;;
        20)  # pip_pypy3
            python="/usr/local/opt/pypy3/bin/pyp3"
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
            chmod 777 $pipdeptree
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
mode_pip_sys20=false    # 2.0.* / system / cpython
mode_pip_sys21=false    # 2.1.* / system / cpython
mode_pip_sys22=false    # 2.2.* / system / cpython
mode_pip_sys23=false    # 2.3.* / system / cpython
mode_pip_sys24=false    # 2.4.* / system / cpython
mode_pip_sys25=false    # 2.5.* / system / cpython
mode_pip_sys26=false    # 2.6.* / system / cpython
mode_pip_sys27=false    # 2.7.* / system / cpython
mode_pip_sys30=false    # 3.0.* / system / cpython
mode_pip_sys31=false    # 3.1.* / system / cpython
mode_pip_sys32=false    # 3.2.* / system / cpython
mode_pip_sys33=false    # 3.3.* / system / cpython
mode_pip_sys34=false    # 3.4.* / system / cpython
mode_pip_sys35=false    # 3.5.* / system / cpython
mode_pip_sys36=false    # 3.6.* / system / cpython
mode_pip_sys37=false    # 3.7.* / system / cpython
mode_pip_brew2=false    # 2.* / cellar / cpython
mode_pip_brew3=false    # 3.* / cellar / cpython
mode_pip_pypy2=false    # 2.* / cellar / pypy
mode_pip_pypy3=false    # 3.* / cellar / pypy


# if system flag set
if ( $arg_s ) ; then
    case $arg_V in
        1)  mode_pip_sys20=true
            mode_pip_sys21=true
            mode_pip_sys22=true
            mode_pip_sys23=true
            mode_pip_sys24=true
            mode_pip_sys25=true
            mode_pip_sys26=true
            mode_pip_sys27=true
            mode_pip_sys30=true
            mode_pip_sys31=true
            mode_pip_sys32=true
            mode_pip_sys33=true
            mode_pip_sys34=true
            mode_pip_sys35=true
            mode_pip_sys36=true
            mode_pip_sys37=true ;;
        2)  mode_pip_sys20=true
            mode_pip_sys21=true
            mode_pip_sys22=true
            mode_pip_sys23=true
            mode_pip_sys24=true
            mode_pip_sys25=true
            mode_pip_sys26=true
            mode_pip_sys27=true ;;
        20) mode_pip_sys20=true ;;
        21) mode_pip_sys21=true ;;
        22) mode_pip_sys22=true ;;
        23) mode_pip_sys23=true ;;
        24) mode_pip_sys24=true ;;
        25) mode_pip_sys25=true ;;
        26) mode_pip_sys26=true ;;
        27) mode_pip_sys27=true ;;
        3)  mode_pip_sys30=true
            mode_pip_sys31=true
            mode_pip_sys32=true
            mode_pip_sys33=true
            mode_pip_sys34=true
            mode_pip_sys35=true
            mode_pip_sys36=true
            mode_pip_sys37=true ;;
        30) mode_pip_sys30=true ;;
        31) mode_pip_sys31=true ;;
        32) mode_pip_sys32=true ;;
        33) mode_pip_sys33=true ;;
        34) mode_pip_sys34=true ;;
        35) mode_pip_sys35=true ;;
        36) mode_pip_sys36=true ;;
        37) mode_pip_sys37=true ;;
    esac
fi


# if cellar flag set
if ( $arg_b ) ; then
    case $arg_V in
        1)  mode_pip_brew2=true
            mode_pip_brew3=true
            mode_pip_pypy2=true
            mode_pip_pypy3=true ;;
        2)  mode_pip_brew2=true
            mode_pip_pypy2=true ;;
        3)  mode_pip_brew3=true
            mode_pip_pypy3=true ;;
    esac
fi


# if cpython flag set
if ( $arg_c ) ; then
    case $arg_V in
        1)  mode_pip_sys20=true
            mode_pip_sys21=true
            mode_pip_sys22=true
            mode_pip_sys23=true
            mode_pip_sys24=true
            mode_pip_sys25=true
            mode_pip_sys26=true
            mode_pip_sys27=true
            mode_pip_sys30=true
            mode_pip_sys31=true
            mode_pip_sys32=true
            mode_pip_sys33=true
            mode_pip_sys34=true
            mode_pip_sys35=true
            mode_pip_sys36=true
            mode_pip_sys37=true
            mode_pip_brew2=true
            mode_pip_brew3=true ;;
        2)  mode_pip_sys20=true
            mode_pip_sys21=true
            mode_pip_sys22=true
            mode_pip_sys23=true
            mode_pip_sys24=true
            mode_pip_sys25=true
            mode_pip_sys26=true
            mode_pip_sys27=true
            mode_pip_brew2=true ;;
        3)  mode_pip_sys30=true
            mode_pip_sys31=true
            mode_pip_sys32=true
            mode_pip_sys33=true
            mode_pip_sys34=true
            mode_pip_sys35=true
            mode_pip_sys36=true
            mode_pip_sys37=true
            mode_pip_brew3=true ;;
    esac
fi


# if pypy flag set
if ( $arg_y ) ; then
    case $arg_V in
        1)  mode_pip_pypy2=true
            mode_pip_pypy3=true ;;
        2)  mode_pip_pypy2=true ;;
        3)  mode_pip_pypy3=true ;;
    esac
fi


# call piplogging function according to modes
list=( \
    [1]=$mode_pip_sys20 $mode_pip_sys21 $mode_pip_sys22 $mode_pip_sys23 $mode_pip_sys24 $mode_pip_sys25 $mode_pip_sys26 $mode_pip_sys27 \
        $mode_pip_sys30 $mode_pip_sys31 $mode_pip_sys32 $mode_pip_sys33 $mode_pip_sys34 $mode_pip_sys35 $mode_pip_sys36 $mode_pip_sys37 \
        $mode_pip_brew2 $mode_pip_brew3 $mode_pip_pypy2 $mode_pip_pypy3 \
)
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

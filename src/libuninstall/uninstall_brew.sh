#!/bin/bash


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1


# terminal display
reset="\033[0m"         # reset
bold="\033[1m"          # bold
red="\033[91m"          # bright red foreground
green="\033[92m"        # bright green foreground
yellow="\033[93m"       # bright yellow foreground


################################################################################
# Uninstall Homebrew packages.
#
# Parameter list:
#   1. Encrypted Password
#   2. Log File
#   3. Temp File
#   4. Force Flag
#   5. Quiet Flag
#   6. Verbose Flag
#   7. Ignore-Dependencies Flag
#   8. Yes Flag
#   9. Package
#       ............
################################################################################


# parameter assignment
password=`python -c "print(__import__('base64').b64decode(__import__('sys').stdin.readline().strip()).decode())" <<< $1`
# echo $1 | cut -c2- | rev | cut -c2- | rev
logfile=`python -c "print(__import__('sys').stdin.readline().strip().strip('\''))" <<< $2`
tmpfile=`python -c "print(__import__('sys').stdin.readline().strip().strip('\''))" <<< $3`
arg_f=$4
arg_q=$5
arg_v=$6
arg_i=$7
arg_Y=$8
arg_pkg=${*:9}


# remove /tmp/log/uninstall.log
rm -f "$tmpfile"


# create /tmp/log/uninstall.log & /Library/Logs/Scripts/uninstall/logdate.log
touch "$logfile"
touch "$tmpfile"


# log current status
echo "- /bin/bash $0 $@" >> "$tmpfile"


# log commands
logprefix="script -aq "$tmpfile""
if ( $arg_q ) ; then
    logsuffix="grep ^$"
else
    logsuffix="grep ^.*$"
fi


# brew fix missing function usage
#   brew_fixmissing packages
function brew_fixmissing {
    # parameter assignment
    local arg_pkg=${*:1}

    # reinstall missing packages
    for $name in $arg_pkg ; do
        # ask for password up-front
        sudo --reset-timestamp
        sudo --stdin --validate <<< $password ; echo

        $logprefix printf "+ ${bold}brew reinstall $name $force $verbose $quiet${reset}\n" | $logsuffix
        if ( $arg_q ) ; then
            $logprefix brew reinstall $name $force $verbose $quiet > /dev/null 2>&1
        else
            $logprefix brew reinstall $name $force $verbose $quiet
        fi
        $logprefix echo | $logsuffix
    done

    # inform if missing packages fixed
    $logprefix printf "uninstall: ${green}brew${reset}: all missing packages reinstalled\n" | $logsuffix
}


# if quiet flag set
if ( $arg_q ) ; then
    quiet="--quiet"
else
    quiet=""
fi


# if verbose flag set
if ( $arg_v ) ; then
    verbose="--verbose"
else
    verbose=""
fi


# if force flag set
if ( $arg_f ) ; then
    force="--force"
else
    force=""
fi


# uninstall procedure
for name in $arg_pkg ; do
    case $name in
        all)
            list=`brew list -1`
            for pkg in $list; do
                # ask for password up-front
                sudo --reset-timestamp
                sudo --stdin --validate <<< $password ; echo

                $logprefix printf "+ ${bold}brew uninstall $pkg --ignore-dependencies $force $verbose $quiet${reset}\n" | $logsuffix
                if ( $arg_q ) ; then
                    $logprefix brew uninstall $pkg --ignore-dependencies $force $verbose $quiet > /dev/null 2>&1
                else
                    $logprefix brew uninstall $pkg --ignore-dependencies $force $verbose $quiet
                fi
                $logprefix echo | $logsuffix
            done ;;
        *)
            # check if package installed
            flag=`brew list -1 | awk "/^$name$/"`
            if [[ ! -z $flag ]] ; then
                # ask for password up-front
                sudo --reset-timestamp
                sudo --stdin --validate <<< $password ; echo

                $logprefix printf "+ ${bold}brew uninstall $name --ignore-dependencies $force $verbose $quiet${reset}\n" | $logsuffix
                if ( $arg_q ) ; then
                    $logprefix brew uninstall $name --ignore-dependencies $force $verbose $quiet > /dev/null 2>&1
                else
                    $logprefix brew uninstall $name --ignore-dependencies $force $verbose $quiet
                fi
                $logprefix echo | $logsuffix

                # if ignore-dependencies flag not set
                if ( ! $arg_i ) ; then
                    list=`brew deps $name --installed`
                    for pkg in $list; do
                        # check if package installed
                        if brew list --versions $pkg > /dev/null ; then
                            # ask for password up-front
                            sudo --reset-timestamp
                            sudo --stdin --validate <<< $password ; echo

                            $logprefix printf "+ ${bold}brew uninstall $pkg --ignore-dependencies $force $verbose $quiet${reset}\n" | $logsuffix
                            if ( $arg_q ) ; then
                                $logprefix brew uninstall $pkg --ignore-dependencies $force $verbose $quiet > /dev/null 2>&1
                            else
                                $logprefix brew uninstall $pkg --ignore-dependencies $force $verbose $quiet
                            fi
                            $logprefix echo | $logsuffix
                        fi
                    done
                fi
            else
                $logprefix printf "uninstall: ${yellow}brew${reset}: no formula names ${red}$name${reset} installed\n" | $logsuffix

                # did you mean
                tmp=`brew list -1 | grep $name | xargs`
                if [[ ! -z $tmp ]] ; then
                    dym=`python -c "print('${red}' + '${reset}, ${red}'.join(__import__('sys').stdin.read().strip().split()) + '${reset}')" <<< $tmp`
                    $logprefix printf "uninstall: ${yellow}brew${reset}: did you mean any of the following formulae: $dym?\n" | $logsuffix
                fi
                $logprefix echo | $logsuffix
            fi ;;
    esac
done


# fix missing brew dependencies
tmparg=`brew missing 2>/dev/null | sed "s/.*: \(.*\)*/\1/" | sort -u | xargs`
if [[ ! -z $tmparg ]] ; then
    missing==`python -c "print('${red}' + '${reset}, ${red}'.join([ item.split('==')[0] for item in __import__('sys').stdin.read().strip().split() ]) + '${reset}')" <<< $tmparg`
    $logprefix printf "uninstall: ${red}brew${reset}: dependency ${bold}formulae${reset} found missing: $missing\n" | $logsuffix
    if ( $arg_Y || $arg_q ) ; then
        $logprefix echo | $logsuffix
        brew_fixmissing $tmparg
    else
        while true ; do
            read -p "Would you like to reinstall? (y/N)" yn
            case $yn in
                [Yy]* )
                    $logprefix echo | $logsuffix
                    brew_fixmissing $tmparg
                    break ;;
                [Nn]* )
                    $logprefix printf "uninstall: ${red}brew${reset}: missing formulae remain\n" | $logsuffix
                    $reset
                    break ;;
                * )
                    printf "uninstall: ${red}brew${reset}: invalid choice\n" ;;
            esac
        done
    fi
fi


# aftermath works
bash ./libuninstall/aftermath.sh "$logfile" "$tmpfile"


# remove /tmp/log/uninstall.log
rm -f "$tmpfile"


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1

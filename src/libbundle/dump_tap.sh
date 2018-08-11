#!/bin/bash


# parameter assignment
verbose=$1


# check brew installed
which brew > /dev/null 2>&1
if [ $? -ne 0 ] ; then
    exit 1
fi


# fetch tap description
#   desc_tap tap
function desc_tap () {
    local tap=$1
    python << EOF
import datetime
import json
import random
import sys
import time

# check for 2/3 capability
if sys.version_info.major == 3:
    from urllib.request import urlopen
    from urllib.error import HTTPError
    from json.decoder import JSONDecodeError
elif sys.version_info.major == 2:
    from urllib2 import urlopen
    from urllib2 import HTTPError
    JSONDecodeError = ValueError
else:
    print('NIL')
    sys.exit(1)

# fetch repo and user
user, repo = '$tap'.split('/')

# wait some time for API rate limit
time.sleep(random.randint(0, datetime.datetime.now().second // 6))

# request GitHub API
try:
    response = urlopen('https://api.github.com/search/repositories?q=%s+user:%s' % (repo, user))
    html = response.read()
    data = json.loads(html)
    response.close()
except HTTPError as error:
    desc = 'NIL (%s)' % error
except JSONDecodeError as error:
    desc = 'NIL (%s)' % error
except Exception as error:
    desc = 'NIL (%s)' % error
else:
    desc = data.get('items', [dict()])[0].get('description', 'NIL')
finally:
    print(desc)
EOF
}


# dump procedure
if ( $verbose ) ; then
    # fetch description for verbose output
    list=`brew tap 2> /dev/null | grep "^[a-zA-Z0-9\-]*/[a-zA-Z0-9\-]*$" | sort | uniq | xargs`
    for name in $list ; do
        desc=`desc_tap $name 2> /dev/null`
        echo $name
        desc_tap $name
        echo "# $desc" >> ~/.Macfile
        echo -e tap \"$name\" >> ~/.Macfile
    done
else
    brew tap 2> /dev/null | grep "^[a-zA-Z0-9\-]*/[a-zA-Z0-9\-]*$" | sed "s/\(.*\)*/tap \"\1\"/" | sort | uniq >> ~/.Macfile
fi

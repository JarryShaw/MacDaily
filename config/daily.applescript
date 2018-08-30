#!/usr/bin/osascript

-- show notification
display notification "Daily scheduled script `{mode}` running..." with title "MacDaily"

-- run script
do shell script "{sys.executable} -m macdaily {mode} {argv}"

#!/usr/bin/osascript

-- show notification
display notification "Daily scheduled script `logging` running..." with title "macdaily"

-- run script
do shell script "{sys.executable} -m macdaily {mode} {argv}"

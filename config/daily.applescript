#!/usr/bin/osascript

display notification "Scheduled script `{mode}` running..." with title "MacDaily"
tell application "Terminal"
    activate
    do script "macdaily {mode} --all"
end tell

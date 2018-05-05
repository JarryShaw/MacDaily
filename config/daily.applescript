#!/usr/bin/osascript

display notification "Daily scheduled script `{mode}` running..." with title "jsdaily"
tell application "Terminal"
    activate
    do script "jsdaily {mode} --all"
end tell

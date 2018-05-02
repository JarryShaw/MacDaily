tell application "Terminal"
	if not (exists window 1) then reopen
	activate
	display notification "Scripts running..." with title "jsdaily"
	do script "jsdaily update --all" in window 1
	do script "jsdaily logging --all" in window 1
	display notification "Script done..." with title "jsdaily"
end tell

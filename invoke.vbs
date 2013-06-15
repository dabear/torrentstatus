Dim cmd
For Each arg In WScript.Arguments
	cmd = cmd & " """ & arg & """"
Next 
cmd = Trim(cmd)

Set WshShell = WScript.CreateObject("WScript.Shell")
WshShell.Run cmd, 0

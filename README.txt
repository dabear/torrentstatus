
Assuming this structure:
C:\scripts\torrentstatus
C:\scripts\torrentstatus\README.txt
C:\scripts\torrentstatus\runit.bat
C:\scripts\torrentstatus\torrentstatus\
C:\scripts\torrentstatus\torrentstatus\handle_status_change.py
(etc..)

If you want to call this script manually, make sure that the folder "C:\scripts\torrentstatus\" is in python's searchpath.
You can do that by setting the environment variable PYTHONPATH, either permanently through your system properties, or temporarily by doing

set PYTHONPATH=%PYTHONPATH%;C:\scripts\torrentstatus\

You can then test the module by executing:
c:\python27\python.exe -m torrentstatus.handle_status_change --help

Add the following to utorrent's settings "advanced"->"execute program":
C:\scripts\torrentstatus\invoke.vbs C:\scripts\torrentstatus\runit.bat --torrentname "%N" --torrentstatus %S  --laststatus %P --downloadpath "%D" 

You can test the script functionality from command line by doing something like:
	C:\scripts\torrentstatus\runit.bat --torrentname "The.Foo-nb" --torrentstatus 5  --laststatus 6 --downloadpath "H:\Other\The.foo-nb" 


# Torrentstatus, what is it?
Currently in pre-alpha mode, this set of python scripts makes up a package that can be called manually or automatically by utorrent when a torrent download starts or completes.
Actions implemented are as follows:
  -on start of download:
    -Send email
    -(todo:) Change label of torrent based on a list of regexp matched against tracker url
  -on completion of download:
    -Send email
    -Alert through pynma (notify my android)
    -Download subtitles (depends on filebot being installed)

    
# Dependencies
  -utorrent
  -python 2.7 or later python version in the 2.x-series
  -filebot executable installed and available from your path. Can be downloaded from http://www.filebot.net/#download
  -(todo:) utorrent webui


# First time setup, setting up config file
Open command line and navigate to the location of settings.py
Run the python interpreter against settings.py
c:\python27\python settings.py
A new config.ini file will be created at ~/.config/Torrentstatus/
Edit this file, add your settings for sending email and your nma api key ( https://www.notifymyandroid.com/account.jsp)

# Calling script manually without installing to system(hacking PYTHONPATH)

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
C:\scripts\torrentstatus\invoke.vbs  C:\scripts\torrentstatus\runit.bat --torrentname "%N" --torrentstatus %S  --laststatus %P --downloadpath "%D"  --torrenttype "%K" --filename "%F" --hash "%I"

invoke.vbs is needed when calling a bat file silently. Only applicable if you did not install the package 
You can test the script functionality from command line by doing something like:
C:\scripts\torrentstatus\runit.bat --torrentname "Under.the.Dome.S01E01.720p.HDTV.X264-DIMENSION.mkv" --torrentstatus 5  --laststatus 6 --downloadpath "h:\Other"  --torrenttype "single" --filename "Under.the.Dome.S01E01.720p.HDTV.X264-DIMENSION.mkv" --hash "6E5385285A6BC9D91A42F1B096156407DFBD4C4B"



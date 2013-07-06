# Torrentstatus

Currently in pre-alpha mode, this set of python scripts makes up a package that can be used for automating certain torrent related activities

## Actions implemented are as follows:
### on start of download:
- Send email
- (todo:) Change label of torrent based on a list of regexp matched against tracker url
###  On completion of download:
- Send email
- Alert through pynma (notify my android)
- Download subtitles (depends on filebot being installed)

    
## Requirements
- uTorrent for windows
- Python 2.7 or later python version in the 2.x-series
- Filebot executable installed and available from your path.  Can be downloaded from http://www.filebot.net/#download
- (todo:) utorrent webui


## First time setup, setting up config file
Open command line and navigate to the location of settings.py
Run the python interpreter against settings.py
c:\python27\python settings.py .

A new config.ini file will be created at ~/.config/Torrentstatus/

Edit this file, add your settings for sending email and your nma api key ( https://www.notifymyandroid.com/account.jsp)


## Usage
Add this to uTorrents "run program when torrent changes status" config:
  ```sh
C:\scripts\torrentstatus\invoke.vbs  C:\scripts\torrentstatus\runit.bat --torrentname "%N" --torrentstatus %S  --laststatus %P --downloadpath "%D"  --torrenttype "%K" --filename "%F" --hash "%I"
  ```

Note invoke.vbs is just a wrapper to avoid a flashing console window. This wrapper will be removed soon.


## Debugging

Assuming this structure:
- C:\scripts\torrentstatus
- C:\scripts\torrentstatus\README.txt
- C:\scripts\torrentstatus\runit.bat
- C:\scripts\torrentstatus\torrentstatus\
- C:\scripts\torrentstatus\torrentstatus\handle_status_change.py
(etc..) a

If you want to call this script manually, make sure that the folder "C:\scripts\torrentstatus\" is in python's searchpath.
You can do that by setting the environment variable PYTHONPATH, either permanently through your system properties, or temporarily by doing
  ```sh
set PYTHONPATH=%PYTHONPATH%;C:\scripts\torrentstatus\
  ```

You can then test the module by executing:
  ```sh
c:\python27\python.exe -m torrentstatus.handle_status_change --help
  ```


### Invoking onfinish handler manually
  ```sh

Note the torrent doesn't actually have to exist to test this functionality;

C:\scripts\torrentstatus\runit.bat --torrentname "Kodemysteriene - VG+" --torrentstatus 5  --laststatus 6 --downloadpath "h:\Other\Kodemysteriene - VG+"  --torrenttype "multi" --filename "Kodemysteriene - VG+.pdf" --hash "D700D1F9BC72DCAE1FB2B1E54F39BA3D27C4440B"
  ```



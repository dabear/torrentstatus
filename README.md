# Torrentstatus

Currently in pre-alpha mode, this set of python scripts makes up a package that can be used for automating certain torrent related activities

## Actions implemented are as follows:
### on start of download:
- Send email
- (todo:) Change label of torrent based on a list of regexp matched against tracker url

### On completion of download:
- Send email
- Alert through pynma (notify my android)
- Download subtitles (depends on filebot being installed)

    
## Requirements
- uTorrent for windows
- Python 3.3 or later 
- Filebot executable installed and available from your path.  Can be downloaded from http://www.filebot.net/#download
- (todo:) utorrent webui

## Installation

Download and install setuptools for python from here:
https://bitbucket.org/pypa/setuptools/raw/0.8/ez_setup.py
Example:
  ```bat
c:\Python33\python.exe ez_setup.py
  ```

Download the source ( [ZIP][] here) and run setup.py
  ```bat
cd pathToFolder
c:\python33\python setup.py install
  ```



## First time setup, setting up config file
Open command line and run the python interpreter against 

  ```bat

c:\python33\python -m torrentsettings.setup
  ```

A new config.ini file will be created at ~/.config/Torrentstatus/

Edit this file, add your settings for sending email and your nma api key ( https://www.notifymyandroid.com/account.jsp)


## Usage
- Add this to uTorrents "run program when torrent changes status" config:
  ```bat
c:\python33\pythonw.exe -m torrentstatus.handle_status_change --torrentname "%N" --torrentstatus %S  --laststatus %P --downloadpath "%D"  --torrenttype "%K" --filename "%F" --hash "%I"
  ```
- Create a windows scheduled task to run c:\python27\pythonw.exe -m torrentstatus.download on a regular basis. This downloads subtitles for finished torrents with media files available.



## Debugging


Use python.exe, *not* pythonw.exe for debugging purposes
Install package in develop mode
  ```bat
cd pathToFolder
c:\python33\python setup.py develop
  ```

  ```bat
c:\python33\python.exe -m torrentstatus.handle_status_change --help
  ```


### Invoking onfinish handler manually
  

Note the torrent doesn't actually have to exist to test this functionality;

```bat
c:\python33\python.exe -m torrentstatus.handle_status_change --torrentname "Kodemysteriene - VG+" --torrentstatus 5  --laststatus 6 --downloadpath "h:\Other\Kodemysteriene - VG+"  --torrenttype "multi" --filename "Kodemysteriene - VG+.pdf" --hash "D700D1F9BC72DCAE1FB2B1E54F39BA3D27C4440B"
  ```



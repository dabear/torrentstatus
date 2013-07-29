# Torrentstatus

Currently in alpha mode, this set of python scripts makes up a package that can be used for automating certain torrent related activities

## Actions implemented are as follows:
### on start of download:
- Send email
- Change label of torrent based on a ruleset defined in a config file ("auto label" feature). Uses [Bearlang][] for user defined label rules, after the first run, %HOMEPATH%\.config\Torrentstatus\torrentlabels.ini will be created, see the torrentlabels example below

### On completion of download:
- Send email
- Alert through pynma (notify my android)
- Registers completed download in a locally stored sqlite database. Facilitates subtitle downloading.
- Download subtitles. Depends on filebot being installed. This feature is currently fully coded but not called on complete.

    
## Dependencies
- uTorrent for windows
- Python 3.3 or later 
- Filebot executable installed and available from your path.  Can be downloaded from http://www.filebot.net/#download
- utorrent webui setup and configured

## Installation

Download the source ( [ZIP][] here) and run setup.py
  ```bat
cd pathToFolder
c:\python33\python setup.py install
  ```



## First time setup, setting up config file
Open command line and run the python interpreter against 

  ```bat

c:\python33\python -m torrentstatus.settings
  ```

A new config.ini file will be created at ~/.config/Torrentstatus/

Edit this file, add your settings for sending email and your nma api key ( https://www.notifymyandroid.com/account.jsp)


## Usage
- Add this to uTorrents "run program when torrent changes status" config:
  ```bat
  
c:\python33\pythonw.exe -m torrentstatus.handle_status_change --torrentname "%N" --torrentstatus %S  --laststatus %P --downloadpath "%D"  --torrenttype "%K" --filename "%F" --hash "%I" --tracker "%T"
  ```
- Create a windows scheduled task to run c:\python33\pythonw.exe -m torrentstatus.download on a regular basis. This downloads subtitles for finished torrents with media files available.
 


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
  

Note the torrent or its path doesn't actually have to exist to test this functionality. Remember to add the debug switch:

  ```bat
c:\python33\python.exe -m torrentstatus.handle_status_change --torrentname "Kodemysteriene - VG+" --torrentstatus 5  --laststatus 6 --downloadpath "h:\Other\Kodemysteriene - VG+"  --torrenttype "multi" --filename "Kodemysteriene - VG+.pdf" --hash "D700D1F9BC72DCAE1FB2B1E54F39BA3D27C4440B" --tracker "foo.bar.com/announce" --debug
  ```


## Torrentlabel rules

Rules can be defined in torrentlabels.ini, located in the users config dir for torrentstatus. The full config path is %HOMEPATH%\.config\Torrentstatus\torrentlabels.ini

Please note that a label can have many rules, but only one keyword and one rule per line.
 You have to repeat keywords if you want multiple rules for a label.
 Variables here are the same as provided to sys.args when calling torrentstatus.handle_status_change .
 Please note that all rules must be defined in the same section "Torrentlabels". Torrentlabels.ini will be created on the first run
 Here are some examples:


  ```sh
[Torrentlabels]
Series season packs = contains(tracker, 'mytvsite.com') && equals(torrenttype, 'multi')
Series = contains(tracker, 'mytvsite.com') && equals(torrenttype, 'single')
Movies = contains(tracker, 'mymoviesite')
Movies = contains(tracker, 'myothermoviesite')
  ```


[ZIP]: https://github.com/dabear/torrentstatus/archive/master.zip
[BearLang]: https://github.com/dabear/BearLang
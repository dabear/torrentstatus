# Torrentstatus

Currently in beta, this set of python scripts makes up a package that can be used for automating certain torrent related activities

## Actions implemented are as follows:
### on start of download:
- Send email
- Change label of torrent based on a ruleset defined in a config file ("auto label" feature). Uses [Bearlang][] for user defined label rules. After the first run, torrentlabels.ini will be created; please see the torrentlabels example below.

### On completion of download:
- Send email
- Alert through pynma (notify my android)
- Registers completed download in a locally stored sqlite database. Facilitates subtitle downloading.
- Download subtitles. Depends on filebot being installed. This feature is currently fully coded but not called on complete.

    
## Dependencies
- uTorrent for windows
- Python 3.3 or later 
- utorrent webui setup and configured

## Installation

Download the torrentstatus source ( [ZIP][] here) and run setup.py
  ```bat
cd pathToFolder
c:\python33\python setup.py install
  ```



## First time setup, setting up config file
Open command line and run the python interpreter against 

  ```bat

c:\python33\python -m torrentstatus.settings
  ```

A new config.ini and torrentlabels.ini file will be created, and the config path will be displayed on the console.

Edit config.ini to enable sending emails when a torrent starts or completes.
Edit torrentlabels.ini to set labels on new torrents based on criterias defined in that file.

## Usage
- Add this to uTorrents "run program when torrent changes status" config:

  ```bat
c:\python33\pythonw.exe -m torrentstatus.handle_status_change --torrentname "%N" --torrentstatus %S  --laststatus %P --downloadpath "%D"  --torrenttype "%K" --filename "%F" --hash "%I" --tracker "%T"
  ```

 


## Debugging


Use python.exe, *not* pythonw.exe for debugging purposes.
Install the package in development mode:
  ```bat
cd pathToFolder
c:\python33\python setup.py develop
  ```

  ```bat
  
c:\python33\python.exe -m torrentstatus.handle_status_change --help
  ```


### Testing plugins directly
  

Note the torrent or its path doesn't actually have to exist to test this functionality. Remember to add the debug switch:


  ```bat
c:\python33\python.exe -m torrentstatus.handle_status_change --torrentname "Kodemysteriene - VG+" --torrentstatus 5  --laststatus 6 --downloadpath "h:\Other\Kodemysteriene - VG+"  --torrenttype "multi" --filename "Kodemysteriene - VG+.pdf" --hash "D700D1F9BC72DCAE1FB2B1E54F39BA3D27C4440B" --tracker "foo.bar.com/announce" --debug
  ```


## torrentlabels.ini rules

Rules can be defined in torrentlabels.ini, located in the users config dir for torrentstatus. The full config path is displayed on screen if you run "python -m torrentstatus.settings"

Please note that a rule definition can be repeated on consecutive lines in the ini file.
 You have to repeat keywords if you want multiple rules for a label.
 Variables here are the same as provided to sys.args when calling torrentstatus.handle_status_change .
 Please note that all rules must be defined in the same section "Torrentlabels". Torrentlabels.ini will be created the first time you run "python -m torrentstatus.settings".

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
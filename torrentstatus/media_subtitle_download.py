#!/usr/bin/python
# -*- coding: utf-8 -*-
__version__ = '0.1'
__all__ = [
    'SubtitleDownloader'
]
"""This module provides a single class SubtitleDownloader,
a proxy class that initiates a Periscope instance and downloads subtitles.

You can set which directory to search for media files,
and which media files to lookup a matching subtitle for.
Periscope will decide what online sources to use for subtitle matching
"""

#c:\python27\python.exe c:\python27\scripts\periscope "%1" -l en
#C:\Python27\Lib\site-packages\periscope.egg\..
#http://code.google.com/p/periscope/wiki/PythonModuleUsage
import os, sys
import logging
import periscope
import argparse
import os.path
import subprocess
log_file = "c:\\windows\\temp\\media_subtitle_download.log"

periscope_temp = "C:\\windows\\temp\\periscope"


def setup_logging():

    logger = logging.getLogger(os.path.splitext(__file__)[0] )
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s %(message)s")
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger





def log(s):
    
    if hasattr(log, "no_logging") and log.no_logging:
        return
    if not hasattr(log, "logger"):
        log.logger = setup_logging()
          
    print s
    
    log.logger.info(s)

class SubtitleDownloader():
    #parser.add_argument("--extensions", help="Pipe separated list over file extensions that are valid media files")
    #parser.add_argument("--languages", help="Specifies which languages should be attempted when downloading subs. Separated with a pipe char. Example: no|en")
    #parser.add_argument("--write-retry-file", action="store_true")
    #parser.add_argument("--no-logging", action="store_true", help="if specified, indicates that logs should not be written")
    #parser.add_argument("--filedir", help = "Specifies directory which should be searched for media files. Defaults to current directory")
    #parser.add_argument("--exclude-existing", action="store_true", help="Don't try downloading subfiles if they already exist")
    #parser.add_argument("--wait-confirm", action="store_true", help="User must press Enter to confirm window close")
    def __init__(self, extensions=".mkv|.avi|.mp4|.mpeg", languages="no|en", write_retry_file=True, no_logging=False, filedir=".", exclude_existing=True):
        self.downloader = periscope.Periscope(periscope_temp)
        self.allowed_extensions = tuple(extensions.split("|"))
        self.allowed_languages = languages.split("|")
        self.filedir = os.path.abspath(filedir) #important
        self.files = self.get_media_files()
        
        # Exclude files with matching .srt files
        if exclude_existing:
            self.files = [ x for x in self.files if not os.path.exists(x.rsplit(".", 1)[0]+".srt") ]
        if write_retry_file:
            self.write_retry_file()
            
    def write_retry_file(self, filedir=None):
        """"Writes an executable pyc file to the filedir( or self.filedir if filedir is None) that calls this subtitle downloader script
        
        Usefull if you wan
        """
        if filedir is None:
            filedir = self.filedir
            
        filename = os.path.join(filedir, "0-retry-download-subtitles-for-media-in-dir.bat")
        log("Writing " + filename)
        ex = sys.executable.replace("pythonw", "python")
        #os.lchmod(path, mode)
        # windows only
        if os.name is "nt":
            #in my config I do not have .py files accociated with python on windows
            with open( filename, "w") as f:
                f.write( '"%s" "%s" --wait-confirm'  % (ex, os.path.abspath( __file__ ) ))
        else:
            with open(filename[:-3]+"srt", "w") as f:
                f.write("""#!/usr/bin/env python
        import subprocess
        subprocess.call([{0}, {1}, '--wait-confirm'])
                        """.format(ex, os.path.abspath( __file__ ))  )
                
    
    def get_media_files(self, filedir=None, allowed_extensions=None):
        if filedir is None:
            filedir = self.filedir
        if allowed_extensions is None:
            allowed_extensions = self.allowed_extensions
            
        #list of all media files in filedir(=current directory by default)
        return  [os.path.join(filedir, x) for x in os.listdir(filedir) if x.endswith( allowed_extensions) ]

    def download_subtitles(self, for_files=None):
        """Downloads subtitle files for files specified in for_files or self.files if for_files is None
        
        Files are downloaded to the same directory where the media files are located
        """
        if for_files is None:
            for_files = self.files
        downloaded = []
        for file in for_files:
            log( "Trying to download sub for file:" + file)
            try:
                subtitle = self.downloader.downloadSubtitle(file, self.allowed_languages)
            except:
                log("Error: Did not find a sub for the file: " + file + ": unexpected exception..")
            if subtitle:
                downloaded.append(subtitle)
                log( "Found a sub from {0} in language {1}, downloaded to {2}".format( subtitle['plugin'], subtitle['lang'], subtitle['subtitlepath']))
            else:
                log("Error: Did not find a sub for the file: " + file)
        if not for_files: 
            log("Did not find any media files({0}) that does not already have matching .srt-files, so nothing to do!".format(self.allowed_extensions))
            
        return downloaded, for_files


    
if __name__ == '__main__':


    downloader =SubtitleDownloader(filedir=".")
    downloader.download_subtitles()
    raw_input("press ok")
    


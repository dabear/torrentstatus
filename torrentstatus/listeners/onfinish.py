#!/usr/bin/env python
# -*- coding: utf-8 -*-

from torrentstatus.notifications.email import send_email
from torrentstatus.notifications.nma  import send_push_notification


import torrentstatus.utils

import os.path
import sqlite3

# C:\scripts\torrentstatus\runit.bat --torrentname "Under.the.Dome.S01E01.720p.HDTV.X264-DIMENSION.mkv" --torrentstatus 5  --laststatus 6 --downloadpath "h:\Other"  --torrenttype "single" --filename "Under.the.Dome.S01E01.720p.HDTV.X264-DIMENSION.mkv" --hash "6E5385285A6BC9D91A42F1B096156407DFBD4C4B"
# C:\scripts\torrentstatus\runit.bat --torrentname "Kodemysteriene - VG+" --torrentstatus 5  --laststatus 6 --downloadpath "h:\Other\Kodemysteriene - VG+"  --torrenttype "multi" --filename "Kodemysteriene - VG+.pdf" --hash "D700D1F9BC72DCAE1FB2B1E54F39BA3D27C4440B"
#
# C:\Dropbox\Dropbox\scripts\torrentstatus>c:\python27\python.exe -m torrentstatus.handle_status_change --torrentname "Kodemysteriene - VG+" --torrentstatus 5  --laststatus 6 --downloadpath "h:\Other\Kodemysteriene - VG+"  --torrenttype "multi" --filename "Kodemysteriene - VG+.pdf" --hash "D700D1F9BC72DCAE1FB2B1E54F39BA3D27C4440B"
#


#
#  Write new file path to database
#  create table Mediafiles( id INTEGER PRIMARY KEY ASC, path TEXT, added_date DATE, is_processed BOOLEAN, processed_date DATE, srt_file TEXT)
#   Mediafiles
#  -id  (pk)
#  -path
#  -added_date
#  -is_processed
#  -processed_date
#  -srt_file


#
#
def listener(args):                
    send_push_notification("Torrent downloaded", args.torrentname)
    send_email("Torrent-download complete",
                  "download of torrent {0} complete".format(args.torrentname))
    
  
    cursor, conn =  torrentstatus.utils.connect_db()
    
    if cursor:
        
       
        #
        # Get all media files in download dir
        # Add them into database for later processing. Sometimes subtitles become available some
        # time after files are downloaded, therefore subtitle downloading should be handled by
        # download.py
        #       
        if args.torrenttype == "multi":
            mediafiles = []
            for path in torrentstatus.utils.get_media_files(args.downloadpath):
                if not torrentstatus.utils.get_subtitle_info(path)[0]:
                    mediafiles.append( (None, path, False, None, "") )
            if mediafiles:
                print("multi torrent, got paths: {0}".format( ','.join(str(v) for v in mediafiles) ))
                cursor.executemany("INSERT INTO  Mediafiles( id,path, added_date, is_processed, processed_date, srt_file) VALUES(?, ?, strftime('%s','now'), ?, ?, ?)", mediafiles)
            
        elif args.torrenttype == "single":
            #check if args.downloadpath + args.filename exists, check if it is is a media file, add it
            path = os.path.join(args.downloadpath, args.filename)
            print("single torrent, got path:{0}".format(path))
            print("has subtitlefile? {0}".format(torrentstatus.utils.get_subtitle_info(path) ))
            if os.path.exists(path) and os.path.isfile(path) and torrentstatus.utils.is_media_file(path) and not torrentstatus.utils.get_subtitle_info(path)[0]:
                print("executing single media insert")
                cursor.execute("INSERT INTO Mediafiles( id,path, added_date, is_processed, processed_date, srt_file) VALUES(?, ?, strftime('%s','now'), ?, ?, ?)",  (None, path, False, None, "") )
        conn.commit()
        conn.close()
        
        
    print("finished processing\r\n")
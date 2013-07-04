#!/usr/bin/python
# -*- coding: utf-8 -*-

#from torrentstatus.media_subtitle_download  import SubtitleDownloader
from torrentstatus.notifications.email import send_email
from torrentstatus.notifications.nma  import send_push_notification
from torrentstatus.Settings import Settings

import torrentstatus.utils

import os.path
import sqlite3


# C:\scripts\torrentstatus\runit.bat --torrentname "Under.the.Dome.S01E01.720p.HDTV.X264-DIMENSION.mkv" --torrentstatus 5  --laststatus 6 --downloadpath "h:\Other"  --torrenttype "single" --filename "Under.the.Dome.S01E01.720p.HDTV.X264-DIMENSION.mkv" --hash "6E5385285A6BC9D91A42F1B096156407DFBD4C4B"


#c:\Python27\python handle_status_change.py --torrentname "Dexter.S07E10.720p.HDTV.x264-IMMERSE.mkv" --torrentstatus 5  --laststatus 6 --downloadpath "H:\Other"


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
#C:\scripts\torrentstatus\invoke.vbs  C:\scripts\torrentstatus\runit.bat --torrentname "Brickleberry.S01E10.NORSUB.PDTV.x264-LEVERPOSTEi.mp4" --torrentstatus 12  --laststatus 13 --downloadpath "H:\incomplete"  --torrenttype "single" --filename "Brickleberry.S01E10.NORSUB.PDTV.x264-LEVERPOSTEi.mp4"
#C:\scripts\torrentstatus\invoke.vbs  C:\scripts\torrentstatus\runit.bat --torrentname "Brickleberry.S01E10.NORSUB.PDTV.x264-LEVERPOSTEi.mp4" --torrentstatus 6  --laststatus 12 --downloadpath "H:\incomplete"  --torrenttype "single" --filename "Brickleberry.S01E10.NORSUB.PDTV.x264-LEVERPOSTEi.mp4"
# C:\scripts\torrentstatus\runit.bat --torrentname "Brickleberry.S01E10.NORSUB.PDTV.x264-LEVERPOSTEi.mp4" --torrentstatus 5  --laststatus 6 --downloadpath "h:\Other"  --torrenttype "single" --filename "Brickleberry.S01E10.NORSUB.PDTV.x264-LEVERPOSTEi.mp4"

#
#
def listener(args):                
    send_push_notification("Torrent nedlasta", "%s" % args.torrentname  )
    send_email("Torrent-nedlasting ferdig",
                   "Nedlasting av torrent {0} ferdig".format(args.torrentname))
    
  
    cursor, conn =  torrentstatus.utils.connect_db()
    
    if cursor:
        
        print("got cursor")
        #
        # Get all media files in download dir
        # Add them into database for later processing. Sometimes subtitles become available some
        # time after files are downloaded
        #

        
        #todo filter out those files with .srt already available
        if args.torrenttype == "multi":
            #iterate over args.downloadpath, find media files, filter away those files that don't exist,
            #check if it is is a media file, add it
            path = args.downloadpath
            mediafiles = []
            for f in torrentstatus.utils.get_media_files(path):
                if not torrentstatus.utils.has_subtitle_file(f):
                    mediafiles.append( (None, f, False, None, "") )
            if mediafiles:
                cursor.executemany("INSERT INTO  Mediafiles( id,path, added_date, is_processed, processed_date, srt_file) VALUES(?, ?, strftime('%s','now'), ?, ?, ?)", mediafiles)
            
        elif args.torrenttype == "single":
            #check if args.downloadpath + args.filename exists, check if it is is a media file, add it
            path = os.path.join(args.downloadpath, args.filename)
            print("single torrent, got path:{0}".format(path))
            if os.path.exists(path) and os.path.isfile(path) and torrentstatus.utils.is_media_file(path) and not torrentstatus.utils.has_subtitle_file(path):
                print("executing single media insert")
                cursor.execute("INSERT INTO Mediafiles( id,path, added_date, is_processed, processed_date, srt_file) VALUES(?, ?, strftime('%s','now'), ?, ?, ?)",  (None, path, False, None, "") )
        conn.commit()
        conn.close()
        
        
    print("finished processing\r\n")
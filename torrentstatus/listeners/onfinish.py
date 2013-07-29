#!/usr/bin/env python
# -*- coding: utf-8 -*-

from torrentstatus.notifications.email import send_email
from torrentstatus.notifications.nma import send_push_notification


import torrentstatus.utils

import os.path

#
#  Write new file path to database
#   Mediafiles
#  -id  (pk) (INTEGER)
#  -path (TEXT)
#  -added_date (DATE)
#  -is_processed (Date)
#  -processed_date (Date)
#  -srt_file (Text)


def listener(args):

    send_push_notification("Torrent downloaded", args.torrentname, debug=args.debug)
    send_email("Torrent-download complete",
               "download of torrent {0} complete".format(args.torrentname), debug=args.debug)

    cursor, conn = torrentstatus.utils.connect_db()

    if cursor:
        #
        # Get all media files in download dir
        # Add them into database for later processing. Sometimes subtitles become available some
        # time after files are downloaded, so subtitle downloading should be handled by
        # download.py on a schedule
        #
        if args.torrenttype == "multi":
            mediafiles = []
            for path in torrentstatus.utils.get_media_files(args.downloadpath):
                if not torrentstatus.utils.get_subtitle_info(path)[0]:
                    mediafiles.append((None, path, False, None, ""))
            if mediafiles:
                print("multi torrent, inserting into db: {0}".format(','.join(str(v) for v in mediafiles)))
                if not args.debug:
                    cursor.executemany("INSERT INTO Mediafiles(id, path, added_date,"
                                       " is_processed, processed_date, srt_file)" +
                                       "VALUES(?, ?, strftime('%s','now'), ?, ?, ?)", mediafiles)

        elif args.torrenttype == "single":
            #check if args.downloadpath + args.filename exists, check if it is is a media file, add it
            path = os.path.join(args.downloadpath, args.filename)
            print("single torrent, got path:{0}".format(path))
            print("has subtitlefile? {0}".format(torrentstatus.utils.get_subtitle_info(path)))
            if os.path.exists(path) and os.path.isfile(path) and torrentstatus.utils.is_media_file(path) and not \
               torrentstatus.utils.get_subtitle_info(path)[0]:
                print("executing single media insert", path)
                if not args.debug:
                    cursor.execute("INSERT INTO Mediafiles(id,path, added_date,"
                                   " is_processed, processed_date, srt_file)" +
                                   "VALUES(?, ?, strftime('%s','now'), ?, ?, ?)",  (None, path, False, None, ""))
        conn.commit()
        conn.close()

    print("finished processing\r\n")


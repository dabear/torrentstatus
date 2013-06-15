#!/usr/bin/python
# -*- coding: utf-8 -*-

#from torrentstatus.media_subtitle_download  import SubtitleDownloader
from torrentstatus.notifications.email import send_email
from torrentstatus.notifications.nma  import send_push_notification

def listener(args):         
 #   try:
 #       downloader = SubtitleDownloader(filedir=args.downloadpath)
 #       downloaded, needed = downloader.download_subtitles()
 #       downloaded = "{0} media files needed subtitles, {1} subtitles downloaded ".format(len(downloaded), len(needed))
 #   except Exception as e:
 #       downloaded = "failed: {0}".format(e) 
  
        
    send_push_notification("Torrent nedlasta", "%s" % args.torrentname  )
    send_email("Torrent-nedlasting ferdig",
                    ("Nedlasting av torrent {0} ferdig, subtitlestatus:  {1}".format(args.torrentname, downloaded))  )
    print "ferdig"
#!/usr/bin/python
# -*- coding: utf-8 -*-

#from torrentstatus.media_subtitle_download  import SubtitleDownloader
from torrentstatus.notifications.email import send_email
from torrentstatus.notifications.nma  import send_push_notification

def listener(args):                
    send_push_notification("Torrent nedlasta", "%s" % args.torrentname  )
    send_email("Torrent-nedlasting ferdig",
                    "Nedlasting av torrent {0} ferdig".format(args.torrentname))  
    print "ferdig"
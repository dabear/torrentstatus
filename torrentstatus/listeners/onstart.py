#!/usr/bin/python
# -*- coding: utf-8 -*-
from torrentstatus.notifications.email import send_email

def listener(args):
    send_email( "Torrent download started",
               "Download of torrent {0} started".format(args.torrentname))  
    print("Started processing file")
    #python3 utorrentctl.py --set-props AC90C1B8E2748FA00DA922650B19B8FFCED60B2F.label="bar"
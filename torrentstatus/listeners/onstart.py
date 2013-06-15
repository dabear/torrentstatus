#!/usr/bin/python
# -*- coding: utf-8 -*-
from torrentstatus.notifications.email import send_email

#todo: move out contents of handle_status_change to here
def listener(args):
    send_email( "Torrent-nedlasting starta",
               ("Nedlasting av torrent %s starta" % args.torrentname)  )
    print "starta"
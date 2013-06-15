#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import os, sys


from listeners import onfinish, onstart

# To make this code in email.py work:
#   from ..Settings import Settings
# handle_status_change must be invoked as a module, with the following code:
#   c:\python27\python -m torrentstatus.handle_status_change --help
#



parser = argparse.ArgumentParser(description='Behandler torrent-status, sender notifications per mail og til telefoner')
parser.add_argument("--torrentname", help="Ex.: Dexter.S07E10.720p.HDTV.x264-IMMERSE.mkv", required=True)
parser.add_argument("--torrentstatus", type=int, help="Current torrent status. Ex.: 5 (any value 0-12)", required=True)
parser.add_argument("--laststatus", type=int, help="Previous torrent status. Ex.: 6 (any value 0-12)", required=True)
parser.add_argument("--downloadpath", help="File path where media from torrent is downloaded to. This is used"
                                           " for downloading subtitles Ex.: H:\Other", required=True)
args = parser.parse_args()

#print args

#

statuses = ("no information","error", "checked", "paused", "super seeding",
            "seeding", "downloading", "super seeding forced", "seeding forced",
            "downloading forced", "seeding queued", "finished", "queued",
            "stopped")
#
# C:\scripts\torrentstatus>c:\Python27\python handle_status_change.py --torrentname "Dexter.S07E10.720p.HDTV.x264-IMMERSE.mkv" --torrentstatus 5  --laststatus 6 --downloadpath "H:\Other"
#

# Typically, a torrent will begin with these statuses:
# from stopped (--torrentstatus 12) to queued (--torrentstatus 13):
#     --torrentname "Dexter.S07E10.720p.HDTV.x264-IMMERSE.mkv" --torrentstatus 12  --laststatus 13 --downloadpath "H:\Other"
# and then from queued (--laststatus 12) to downloading ( --torrentstatus 6 ):
#     --torrentname "Dexter.S07E10.720p.HDTV.x264-IMMERSE.mkv" --torrentstatus 6  --laststatus 12 --downloadpath "H:\Other" 
# and then from downloading (--laststatus 6) to seeding ( --torrentstatus 5 ) or finished ( --torrentstatus 5 ):
#     --torrentname "Dexter.S07E10.720p.HDTV.x264-IMMERSE.mkv" --torrentstatus 5  --laststatus 6 --downloadpath "H:\Other" 
if args.torrentname and args.torrentstatus and args.laststatus:
    torrentstatus = statuses[args.torrentstatus]
    laststatus = statuses[args.laststatus]
    
    if torrentstatus == "downloading" or torrentstatus == "downloading forced":
        onstart.listener(args)
    #
    # torrentstatus = "finished" might happen when download is complete OR
    # when seeding is complete. So check that utorrent last downloaded something
    if (torrentstatus == "finished" or torrentstatus == "seeding") \
        and (laststatus == "downloading" or laststatus == "downloading forced"):
        onfinish.listener(args)   

#end



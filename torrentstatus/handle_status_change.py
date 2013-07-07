#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import os, sys


from torrentstatus.listeners import onfinish, onstart

parser = argparse.ArgumentParser(description="""Process torrent status changes.
                                 Example: c:\python27\pythonw.exe -m torrentstatus.handle_status_change --torrentname "%N" --torrentstatus %S  --laststatus %P --downloadpath "%D"  --torrenttype "%K" --filename "%F" --hash "%I"
                                 """)
parser.add_argument("--torrentname", help="Ex.: Dexter.S07E10.720p.HDTV.x264-IMMERSE.mkv", required=True)
parser.add_argument("--torrentstatus", type=int, help="Current torrent status. Ex.: 5 (any value 0-12)", required=True)
parser.add_argument("--laststatus", type=int, help="Previous torrent status. Ex.: 6 (any value 0-12)", required=True)
parser.add_argument("--downloadpath", help="File path where media from torrent is downloaded to. This is used"
                                           " for downloading subtitles Ex.: H:\Other", required=True)
parser.add_argument("--filename", help="File name used when"
                                           " downloading subtitles Ex.: foo.bar.s01e01.xvid.avi", required=True)
parser.add_argument("--torrenttype", help="single|multi"
                                           " .Indicates if torrent contains a single file or multiple files", required=True)
parser.add_argument("--hash", help="Torrenthash for given torrent"
                                           " ", required=True)
args = parser.parse_args()


statuses = ("no information","error", "checked", "paused", "super seeding",
            "seeding", "downloading", "super seeding forced", "seeding forced",
            "downloading forced", "seeding queued", "finished", "queued",
            "stopped")


# Typically, a torrent will begin with these statuses:
# from stopped (--torrentstatus 12) to queued (--torrentstatus 13):
#     --torrentname "Dexter.S07E10.720p.HDTV.x264-IMMERSE.mkv" --torrentstatus 12  --laststatus 13 --downloadpath "H:\Other"
# and then from queued (--laststatus 12) to downloading ( --torrentstatus 6 ):
#     --torrentname "Dexter.S07E10.720p.HDTV.x264-IMMERSE.mkv" --torrentstatus 6  --laststatus 12 --downloadpath "H:\Other" 
# and then from downloading (--laststatus 6) to seeding ( --torrentstatus 5 ) or finished ( --torrentstatus 11 ):
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



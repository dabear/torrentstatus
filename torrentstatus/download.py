#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime

from torrentstatus.Settings import Settings
import torrentstatus.utils

import os
import subprocess

#
# This script is supposed to be run on a schedule
# Loop through all records in database, fetch subtitle where missing, update database
#

def fetch_subtitle(filename):
    base = os.path.basename(filename)
    result = subprocess.call(["filebot", "-get-subtitles", filename, "--q", base, "--lang", "en", "--output", "srt", "--encoding", "utf8", "-non-strict"])
    pass
    return False

if __name__ == '__main__':
    conn, cur = torrentstatus.utils.connect_db()
    if conn:
        today = datetime.datetime.today()
        delta = datetime.timedelta(days=30)
        media = get_media(conn, cur)
        for row in media:
            try:
                processed = datetime.fromtimestamp(row["processed_date"])
            except:
                processed = False
                
            #delte old records
            if (row["srt_file"] or row["is_processed"] == 1 and processed and processed < (today-delta)) or \
                not os.path.exists(row["path"]):
                cur.execute("DELETE FROM Mediafiles WHERE id=?",(row["id"]))
            #download new
            elif not row["srt_file"] and not row["is_processed"]:
                ok = fetch_subtitle(row["path"])
                if ok:
                    cur.execute("UPDATE Mediafiles SET is_processed=1,processed_date=strftime('%s','now') WHERE id=?", row["id"])
    
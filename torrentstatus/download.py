#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import torrentstatus.utils

import os
import subprocess


# This script is supposed to be run on a schedule
# Loop through all records in database, fetch subtitle where missing, update database
#


def fetch_subtitle(filename):
    print("\n\n\nfetching subtitle for {0}".format(filename))
    base = os.path.basename(filename)
    noext = base.rsplit(".", 1)[0]
    print("\nAlso searching by name;{0}".format(noext))
    result = subprocess.call(["filebot", "-non-strict", "-get-subtitles", filename, "--q", noext,
                              "--lang", "en", "--output", "srt", "--encoding",
                              "utf8"])

    print("got result from filebot:{0}".format(result))
    return torrentstatus.utils.get_subtitle_info(filename, langcode="eng")

if __name__ == '__main__':
    cur, conn = torrentstatus.utils.connect_db()
    update_sql = ("UPDATE Mediafiles SET is_processed=1,processed_date" +
                  "=strftime('%s','now'),srt_file=? WHERE id=?")
    if conn:
        today = datetime.datetime.today()
        delta = datetime.timedelta(days=30)
        media = torrentstatus.utils.get_media_list(conn, cur)
        for row in media:
            print("got media {0}".format(row["path"]))
            try:
                processed = datetime.fromtimestamp(row["processed_date"])
            except:
                processed = False

            #delte old records
            if (processed and processed < (today-delta)) or \
               not os.path.exists(row["path"]):
                print("id {0} is now either outdated or file does no longer exist"
                      "? {1}. Deleting from DB".format(row["id"], row["path"]))
                cur.execute("DELETE FROM Mediafiles WHERE id=?", (row["id"],))
            #download new
            elif not row["srt_file"] and not row["is_processed"]:
                ok, srtfile = fetch_subtitle(row["path"])
                if ok:
                    print("running:", update_sql)
                    print("updating id {0}, it is now processed".format(row["id"]))
                    cur.execute(update_sql, (srtfile, row["id"]))
        conn.commit()
        conn.close()

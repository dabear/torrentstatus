#!/usr/bin/python
# -*- coding: utf-8 -*-
from pynma import PyNMA
from torrentstatus import Settings

settings = Settings.Settings.nma
if settings and settings.has_key("key"):
    def send_push_notification(event="torrent completed", desc=u"Torrent er ferdig nedlasta", url="http://example.com"):
        key = settings["key"]
        p = PyNMA(key)
        try:
            res = res = p.push("Utorrent Notifier", event,
                               desc,
                               url, batch_mode=False, html=True)
        except:
            pass
        if __name__ == "__main__":
            print(res)

else:
    def send_push_notification(*args):
        print "Not sending notification, check that key is defined for nma in Settings.py"
#!/usr/bin/python
# -*- coding: utf-8 -*-
from torrentstatus.notifications.pynma import PyNMA
from torrentstatus.settings import settings


if settings and "nma_key" in settings and settings["nma_key"]:
    def send_push_notification(event="torrent completed", desc="Torrent is downloaded",
                               url="http://example.com", debug=False):
        key = settings["nma_key"]
        p = PyNMA(key)

        if debug:
            print("send_push_notification using key {}".format(key))
            return

        try:
            p.push("Utorrent Notifier", event,
                   desc, url,
                   batch_mode=False,
                   html=True)
        except Exception as e:
            raise e

else:
    def send_push_notification(*args):
        print("Not sending notification, check if nma_key is defined in config file")




#!/usr/bin/python
# -*- coding: utf-8 -*-

# To disable notifications, set its value to False
#class Settings(object):
#    email = False
#    nma = False

class Settings(object):
    email = {"send_from": "",
             "send_to": "",
             "smtp": "smtp.altibox.no"}
    nma = {"key": ""}
    log_file = "c:\\windows\\temp\\utorrent-notifier.log"

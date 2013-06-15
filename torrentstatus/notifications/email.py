#!/usr/bin/python
# -*- coding: utf-8 -*-
import smtplib

from torrentstatus import Settings
settings = Settings.Settings.email

if not settings:
    def send_email(*args):
        print "not sending email, no settings defined in Settings.py"
else:
    def send_email(subject, body, sender=settings["send_from"], receiver=settings["send_to"], smtp=settings["smtp"]):
        #print sender
        msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n%s"
               %(sender, receiver, subject, body))
        s = smtplib.SMTP(smtp)
        s.sendmail(sender, [receiver], msg)
        s.quit()

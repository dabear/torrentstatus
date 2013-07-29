#!/usr/bin/python
# -*- coding: utf-8 -*-
import smtplib

from torrentstatus.settings import settings


if not settings:
    def send_email(*args):
        print("not sending email, no settings defined in configuration file")
else:
    def send_email(subject, body, sender=settings["email_send_from"],
                   receiver=settings["email_send_to"], smtp=settings["email_smtp"], debug=False):
        msg = ("From: {0}\r\nTo: {1}\r\nSubject: {2}\r\n\r\n{3}".format(sender, receiver, subject, body))
        print("sending mail:{0}".format(msg))
        if debug:
            print("debug mode on, not sending above mail")
            return
        s = smtplib.SMTP(smtp)
        s.sendmail(sender, [receiver], msg)
        s.quit()

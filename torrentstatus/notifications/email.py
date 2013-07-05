#!/usr/bin/python
# -*- coding: utf-8 -*-
import smtplib

from torrentstatus.settings import settings


if not settings:
    def send_email(*args):
        print("not sending email, no settings defined in configuration file")
else:
    def send_email(subject, body, sender=settings["email_send_from"], receiver=settings["email_send_to"], smtp=settings["email_smtp"]):
        #print sender
        msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n%s"
               %(sender, receiver, subject, body))
        s = smtplib.SMTP(smtp)
        s.sendmail(sender, [receiver], msg)
        s.quit()

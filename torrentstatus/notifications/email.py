#!/usr/bin/python
# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

from torrentstatus.settings import config

settings = config.getSettingsAsDict()

if not settings:
    def send_email(*args):
        print("not sending email, no settings defined in configuration file")
        return False
else:
    def send_email(subject, body, sender=settings["email_send_from"],
                   receiver=settings["email_send_to"], smtp=settings["email_smtp"], debug=False):
        #msg = ("From: {0}\r\nTo: {1}\r\nSubject: {2}\r\n\r\n{3}".format(sender, receiver, subject, body))
        msg = MIMEMultipart('alternative')
        msg.set_charset('utf8')
        msg['FROM'] = sender
        msg['Subject'] = Header(subject.encode('utf-8'), 'UTF-8').encode()
        msg['To'] = receiver
        _attach = MIMEText(body.encode('utf-8'), 'html', 'UTF-8')
        msg.attach(_attach)
        print("sending mail:{0}".format(msg))
        if debug:
            print("debug mode on, not sending above mail")
            return
        s = smtplib.SMTP(smtp)
        try:
            s.sendmail(sender, [receiver], msg.as_string())
        except smtplib.SMTPException as err:
            print("Could not send email:", str(err))
            return False
        s.quit()
        return True

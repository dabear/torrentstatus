#!/usr/bin/python
# -*- coding: utf-8 -*-
__all__ = ["config", "labels_config"]

import os
import collections
from pprint import pprint
from appdirs import AppDirs

try:
    import ConfigParser
except:
    import configparser as ConfigParser


#default settings
DEFAULTS_CONFIG = {
    'email_send_from': ("bjorn@example.com",),
    'email_send_to': ("bjorn@example.com",),
    'email_smtp': ("smtp.altibox.no",),
    'nma_key': ("0zmfq03bug1aghi1vtqy1bhfb7hfb8lq267maw2p3hebgh60",),
    'webui_enable': ("0",),
    'webui_username': ("bjorninge",),
    "webui_password": ("password",),
    "webui_host": ("192.168.10.102:9050",),
    "plugin_setlabel_enable": ("1",),
    "plugin_sendmail_enable": ("1",),
    "plugin_copydata_enable": ("0",),
    "plugin_copydata_todir": ("H:/tobesynced",),
    "extra_plugins_dir": ("plugins",)
}

DEFAULTS_SETLABEL = {
    'adefaultlabel': ("startswith(tracker, 'http://tracker.undefined.net')",),
}
COMMENTS_SETLABEL = """;
; This is a comment. Here are some examples that can be used to specify utorrent labels.
; Please note that a label can have many rules, but only one keyword and one rule per line.
; You have to repeat keywords if you want multiple rules for a label.
; Variables here are the same as provided to sys.args when calling torrentstatus.handle_status_change .
; Also, The default label "adefaultlabel" can be changed, but not removed
; Here are some examples:
;
; Series season packs = contains(tracker, 'mytvsite.com') && equals(torrenttype, 'multi')
; Series = contains(tracker, 'mytvsite.com') && equals(torrenttype, 'single')
; Movies = contains(tracker, 'mymoviesite')
; Movies = contains(tracker, 'myothermoviesite')
"""

def get_config_dir():
    dirs = AppDirs("Torrentstatus", "dabear")
    return dirs.user_data_dir


# Subclassing OrderedDict is not possible anymore.
# This is a workaround
# it allows configparser to support multiple keywords with the same name
# example:
# hey=baar
# spam=baz
# hey=eggs
#
# result:
# {'hey': 'baar\neggs', 'spam': 'baz'}
#
class MultiOrderedDict(collections.MutableMapping):
    def __init__(self, *args, **kwargs):
        self.store = collections.OrderedDict({})
        self.update(dict(*args, **kwargs))  # Use the free update to set keys

    #def __getattr__(self, name):
    #    self.store.__getattr__(name)

    def __getitem__(self, key):
        #print ("__getitem__ called with key: ", key)
        #print ("self.store is: ")
        #pprint(self.store)
        val = self.store[self.__keytransform__(key)]
        return val

    def __setitem__(self, key, value):
        #print("setting mdict key:", key)
        #print("setting mdict val:",  value)
        if isinstance(value, list) and key in self.store:
            self.store[self.__keytransform__(key)].extend(value)
        else:
            self.store[self.__keytransform__(key)] = value

    def __delitem__(self, key):
        del self.store[self.__keytransform__(key)]

    def __missing__(self, key):
        return self.store.__missing__(key)

    def __iter__(self):
        return self.store.__iter__()

    def __keytransform__(self, key):
        return key

    def items(self, *args, **kwargs):
        return self.store.items(*args, **kwargs)

    def copy(self, *args, **kwargs):
        return self.store.copy(*args, **kwargs)

    def update(self, *args, **kwargs):
        return self.store.update(*args, **kwargs)

    def __str__(self):
        return self.store.__str__()

    def __repr__(self):
        return self.store.__repr__()

    def __contains__(self, item):
        return self.store.__contains__(item)

    def __len__(self):
        return self.store.__len__()


class CSettings():
    def __init__(self, defaults, section,
                 configfilebasename, initopcomments):
        self.cfg = None
        self.section = section
        self.defaults = defaults
        self.configfile = get_config_dir() + os.path.sep + configfilebasename
        self.comments = initopcomments
        self.loadSettings()
        self.checkSection()

    # load/save config
    def loadSettings(self):
        # load settings
        #self.cfg = ConfigParser.SafeConfigParser(strict=False) #,dict_type=MultiOrderedDict)
        self.cfg = ConfigParser.SafeConfigParser(strict=False, dict_type=MultiOrderedDict)

        self.cfg.read(self.getSettingsFile())

    def saveSettings(self):
        filename = self.getSettingsFile()
        with open(filename, 'wt', encoding='utf8') as openf:
            if os.path.getsize(filename) == 0:
                openf.write(self.comments)
            self.cfg.write(openf)

    def getSettingsFile(self):
        path = self.configfile
        dirname = os.path.dirname(path)
        if not os.path.exists(dirname):
            print("Setting up config file dir")
            os.makedirs(dirname)

        return path

    def checkSection(self):
        modify = False
        # check for existing section
        if not self.cfg.has_section(self.section):
            print("section is not found, writing new section:", self.section)
            modify = True
            self.cfg.add_section(self.section)

        for opt in self.defaults:
            if not self.cfg.has_option(self.section, opt):
                print("option not found, writing new option:", opt, self.defaults[opt][0])
                modify = True
                self.cfg.set(self.section, opt, self.defaults[opt][0])

        # save if changed
        if modify:
            self.saveSettings()

    def getSetting(self, option):
        return self.cfg.get(self.section, option)

    def getAllSettings(self):
        return self.cfg.items(self.section)

    def test(self):
        return self.cfg.get(self.section, "test")

    def getSettingsAsDict(self):
        d = {}
        for t in self.getAllSettings():
            d[t[0]] = t[1]
        return d

config = CSettings(DEFAULTS_CONFIG, section="Torrentstatus",
                   configfilebasename="config.ini", initopcomments="")
config.checkSection()

labels_config = CSettings(DEFAULTS_SETLABEL, section="Torrentlabels",
                          configfilebasename="torrentlabels.ini", initopcomments=COMMENTS_SETLABEL)
labels_config.checkSection()


if __name__ == '__main__':
    print("\nGeneral config file is located in {0}, please "
          "modify to enable all functionality. "
          "Below is a list over parsed options from "
          "the configuration file:\n".format(config.getSettingsFile()))
    pprint(config.getSettingsAsDict())

    print("\nLabels config file is located in {0}, please "
          "change this file to match your needs. "
          "Showing default labels below:".format(labels_config.getSettingsFile()))
    pprint(labels_config.getSettingsAsDict())

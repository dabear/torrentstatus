#!/usr/bin/python
# -*- coding: utf-8 -*-
__all__ = [ "settings", "CSettings" ]

import os
import collections
from pprint import pprint

try:
    import ConfigParser
except:
    import configparser as ConfigParser

def get_config_dir():
    config_home = os.getenv( "XDG_CONFIG_HOME" )
    if config_home is None:
        config_home = os.path.expanduser( "~" ) + os.path.sep + ".config"
    return config_home + os.path.sep + "Torrentstatus" + os.path.sep

#default settings
DEFAULTS = { 
    'email_send_from'  :("bjorn@example.com",),
    'email_send_to'    :("bjorn@example.com",), 
    'email_smtp'       :("smtp.altibox.no",), 
    'nma_key'          :("0zmfq03bug1aghi1vtqy1bhfb7hfb8lq267maw2p3hebgh60",),
    'media_db'     :("~/.config/Torrentstatus/mediafiles.db",), 
    'sub_lang'  :("eng",),
    'webui_enable': ("0",),
    'webui_username': ("bjorninge",),
    "webui_password": ("password",),
    "webui_host": ("192.168.10.102:9050",),
        
}




# Subclassing OrderedDict is not possible anymore.
# This is a workaround
# it allows configparser to support multiple keywords with the same name
# example:
# hey=baar
# spam=baz
# hey=eggs
#
# result:
# {'hey': 'bar\nbar2', 'spam': 'baz'}
#

class MultiOrderedDict(collections.MutableMapping ):
    def __init__(self, *args, **kwargs):
        self.store = collections.OrderedDict({})
        self.update(dict(*args, **kwargs)) # use the free update to set keys
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
            self.store[self.__keytransform__(key)].extend( value)
        else:  
            self.store[self.__keytransform__(key)] = value

    def __delitem__(self, key):
        del self.store[self.__keytransform__(key)]
    def __missing__(self, key):
        return self.store.__missing__(key)
    def __len__(self):
        return len(self.store)
    def __iter__(self):
        return self.store.__iter__()
    def __keytransform__(self, key):
        return key
    def items(self, *args,**kwargs):
        return self.store.items(*args,**kwargs)
    def copy(self, *args,**kwargs):
        return self.store.copy(*args,**kwargs)
    def update(self, *args,**kwargs):
        return self.store.update(*args,**kwargs)
    def __str__(self):
        return self.store.__str__()
    def __repr__(self):
        return self.store.__repr__()
    def __contains__(self, item):
        return self.store.__contains__(item)
    
    def __len__(self):
        return self.store.__len__()
    

class CSettings():  
    def __init__(self, defaults, section="Torrentstatus",
                 configfilebasename="config.ini", initopcomments=""):
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
        self.cfg = ConfigParser.SafeConfigParser(strict=False,dict_type=MultiOrderedDict)
        
        
        
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

conf = CSettings(DEFAULTS)
conf.checkSection()
settings = conf.getSettingsAsDict()


if __name__ == '__main__':
    print("\nconfiguration file is located in {0}, please "
            "modify to enable all functionality. "
            "Below is a list over parsed options from "
            "the configuration file:\n".format(conf.getSettingsFile()) )
    pprint(settings)
    
    
    

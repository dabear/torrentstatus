#!/usr/bin/python
# -*- coding: utf-8 -*-
__all__ = [ "settings" ]

import os
from pprint import pprint

try:
    import ConfigParser
except:
    import configparser as ConfigParser

#default location
config_location = "~/.config/Torrentstatus/config.ini"
#default settings
g_settings = { 
    'email_send_from'  :("bjorn@example.com",),
    'email_send_to'    :("bjorn@example.com",), 
    'email_smtp'       :("smtp.altibox.no",), 
    'nma_key'          :("0zmfq03bug1aghi1vtqy1bhfb7hfb8lq267maw2p3hebgh60",), #this key is fake..
    'media_db'     :("~/.config/Torrentstatus/mediafiles.db",), 
    'sub_lang'  :("eng",),
    "test": ("bar",)
}


    
    
class CSettings():
    loaded_settings = False
    
    def __init__(self):
        self.cfg = None
        self.section = 'Torrentstatus'
        self.loadSettings()
        self.checkSection()
    
    
    
    # load/save config
    def loadSettings(self):
   
        # options -> default
        dflt = {}
        for opt in g_settings:
            dflt[opt] = g_settings[opt][0]
        
        # load settings
        self.cfg = ConfigParser.SafeConfigParser()
        self.cfg.read(self.getSettingsFile())
    
    def saveSettings(self):
      
        f = open(self.getSettingsFile(), 'wb')
        self.cfg.write(f)
        f.close()
    
    def getSettingsFile(self):
        path = os.path.normpath(os.path.expanduser(config_location))
        dirname = os.path.dirname(path)
        if not os.path.exists(dirname):
            print("Setting up config file dir")
            os.makedirs(dirname)
            
        return path
    
    def checkSection(self):
        modify = False
        # check for existing section
        if not self.cfg.has_section(self.section):
            modify = True
            self.cfg.add_section(self.section)
            
        
        for opt in g_settings:
            if not self.cfg.has_option(self.section, opt):
                modify = True
                self.cfg.set(self.section, opt, g_settings[opt][0])
               
                
        # save if changed
        if modify:
            self.saveSettings()
    
    
    
    # access/modify PlexConnect settings
    def getSetting(self, option):

        return self.cfg.get(self.section, option)

    def getAllSettings(self):
        return self.cfg.items(self.section)



conf = CSettings()
conf.checkSection()
settings = {}



for t in conf.getAllSettings():
    settings[t[0]] = t[1]

if __name__ == '__main__':
   print("\nconfiguration file is located in {0}, please modify to enable all functionality. "
         "Below is a list over parsed options from the configuration file:\n".format(conf.getSettingsFile()) )
   pprint(settings)

#!/usr/bin/python
# -*- coding: utf-8 -*-
__all__ = [ "settings" ]

import os
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

#default location
config_dir = "~/.config/Torrentstatus/config.ini"
#default settings
defaults = { 
    'email_send_from'  :("bjorn@example.com",),
    'email_send_to'    :("bjorn@example.com",), 
    'email_smtp'       :("smtp.altibox.no",), 
    'nma_key'          :("0zmfq03bug1aghi1vtqy1bhfb7hfb8lq267maw2p3hebgh60",), #this key is fake..
    'media_db'     :("~/.config/Torrentstatus/mediafiles.db",), 
    'sub_lang'  :("eng",),
    'webui_enable': ("0",),
    'webui_username': ("bjorninge",),
    "webui_password": ("password",),
    "webui_host": ("192.168.10.102:9050",),
        
}


    
    
class CSettings():  
    def __init__(self, defaults, section="Torrentstatus", configfilebasename="config.ini"):
        self.cfg = None
        self.section = section
        self.defaults = defaults
        self.configfile = get_config_dir() + os.path.sep + configfilebasename
        
        self.loadSettings()
        self.checkSection()
        
        
    
    
    
    # load/save config
    def loadSettings(self):
   
        # options -> default
        dflt = {}
        for opt in self.defaults:
            dflt[opt] = self.defaults[opt][0]
        
        # load settings
        self.cfg = ConfigParser.SafeConfigParser()
        self.cfg.read(self.getSettingsFile())
    
    def saveSettings(self):
      
        #f = open(self.getSettingsFile(), 'wb')
        with open(self.getSettingsFile(), 'at', encoding='utf8') as f:
            self.cfg.write(f)
       
    
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
            modify = True
            self.cfg.add_section(self.section)
            
        
        for opt in self.defaults:
            if not self.cfg.has_option(self.section, opt):
                modify = True
                self.cfg.set(self.section, opt, self.defaults[opt][0])
               
                
        # save if changed
        if modify:
            self.saveSettings()
    
    
    
    # access/modify PlexConnect settings
    def getSetting(self, option):

        return self.cfg.get(self.section, option)

    def getAllSettings(self):
        return self.cfg.items(self.section)



conf = CSettings(defaults)
conf.checkSection()
settings = {}



for t in conf.getAllSettings():
    settings[t[0]] = t[1]

if __name__ == '__main__':
   print("\nconfiguration file is located in {0}, please modify to enable all functionality. "
         "Below is a list over parsed options from the configuration file:\n".format(conf.getSettingsFile()) )
   pprint(settings)

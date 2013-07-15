#!/usr/bin/python
# -*- coding: utf-8 -*-

from torrentstatus.notifications.email import send_email
from torrentstatus.utorrent import uTorrent as utorrent
from torrentstatus.utorrent.connection import Connection
from torrentstatus.bearlang import BearLang

from torrentstatus.settings import CSettings
from torrentstatus.settings import settings

from pprint import pprint

#
#c:\python33\python.exe -m torrentstatus.handle_status_change --torrentname "G.I.Joe.Retaliation.2013.Extended.Action.Cut.720p.BluRay.x264-VeDeTT" --torrentstatus 6  --laststatus 12 --downloadpath "H:\incomplete\G.I.Joe.Retaliation.2013.Extended.Action.Cut.720p.BluRay.x264-VeDeTT"  --torrenttype "multi" --filename "Proof\vedett-gijoe.720p-proof.jpg" --hash "5A4A07F55AF06508BD193E74EB5A5A403210ED43" --tracker "http://tracker.norbits.net/announce.php?passkey=1ed77a3b064c5c91c49d5d1b3dc4fa56"
#



def intTryParse(value):
    try:
        val = int(value)
        return val
    except ValueError:
        return False
    
defaults = { 
    'spamlol1' :("startswith(tracker, 'http://tracker.undefined.net')",),
    
        
}



conf = CSettings(defaults, section="Torrentlabels", configfilebasename="torrentlabels.ini")
conf.checkSection()
labels = {}



for t in conf.getAllSettings():
    labels[t[0]] = t[1]


#print("\nconfiguration file is located in {0}, please modify to enable all functionality. "
#      "Below is a list over parsed options from the configuration file:\n".format(conf.getSettingsFile()) )
#pprint(labels)
   
def get_new_torrent_labels(args):

    global labels
    
    new_labels = []
    
    for label, rule in labels.items():
        #print("\n\ngot rule({0}) and args:{1}".format(rule, tempargs))
        print("\n\nrule:{0}\nlabel:{1}\n".format(rule, label) )
        parser = BearLang(rule, args)
        parser.parse()
        is_match = parser.execute()
        
        print("ismatch:{0}\n".format(is_match))
        if is_match:    
            new_labels.append(label)
    return new_labels

__conn = False

def listener(args):
    send_email( "Torrent download started",
                "Download of torrent {0} started".format(args.torrentname))  
    print("Started processing file")
    
    global __conn
    
    tempargs = vars(args)

    #print ("got torrent '{0}' with hash {1} and tracker{2} ".format(args.torrentname, args.hash, args.tracker) )
    new_labels = get_new_torrent_labels(tempargs)
    
  
            
 
    
    #only connect to utorrent if we need to do a label change
    if new_labels and settings["webui_enable"] and intTryParse(settings["webui_enable"]) == 1:
        if not __conn:
            try:
                __conn = Connection( settings["webui_host"], settings["webui_username"],  settings["webui_password"] ).utorrent( None)
            except Exception as e:
                print("Could not connect to webui, make sure webui_host, "
                      "webui_username and webui_password is correctly defined in configuration file. Error:{0}".format(e))
        if __conn:
            #remove first label
            #set new label
            print ("got torrent '{0}' with hash {1} and tracker{2}, new_labels:{3}".format(args.torrentname, args.hash, args.tracker, new_labels) )
            
            #remove existing label
            __conn.torrent_set_props( [{args.hash: {'label': ''}}])
            for new_label in new_labels:
                #time.sleep(5)
                __conn.torrent_set_props( [{args.hash: {'label': new_label}}])
                
            #
            #utorrent.torrent_set_props( [{'AC90C1B8E2748FA00DA922650B19B8FFCED60B2F': {'label': 'hei'}}])
            #
        
        
        
    else:
        print("Not trying to connect to webui")

    
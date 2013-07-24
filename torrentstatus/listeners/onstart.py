#!/usr/bin/python
# -*- coding: utf-8 -*-

from contextlib import contextmanager

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
    
DEFAULTS = { 
    'spamlol1' :("startswith(tracker, 'http://tracker.undefined.net')",),
    
        
}
COMMENTS = """;
; This is a comment. Here are some examples that can be used to specify utorrent labels.
; Please note that a label can have many rules, but only one keyword and one rule per line.
; You have to repeat keywords if you want multiple rules for a label.
; Variables here are the same as provided to sys.args when calling torrentstatus.handle_status_change .
; Also, The default label "spamlol" can be changed, but not removed
; Here are some examples:
;
; Series season packs = contains(tracker, 'mytvsite.com') && equals(torrenttype, 'multi')
; Series = contains(tracker, 'mytvsite.com') && equals(torrenttype, 'single')
; Movies = contains(tracker, 'mymoviesite')
; Movies = contains(tracker, 'myothermoviesite')
"""


def get_new_torrent_labels(labels, args):
    """Transforms torrent labels and args passing them into a BearLang Instance
    
    Parameters:
        labels (Dict) A dict of label and rules for that label
        args (Dict) A dict of arguments, will be passed to Bearlang
    
    Returns:
        a list of labels that match the rules defined.
    """
    new_labels = []
    
    for label, ruleset in labels.items():
        # multiple rules accepted when configparser uses MultiOrderedDict
        rules = ruleset.split("\n")
        
        for rule in rules:
            rule = rule.strip()
            print("\n\nrule:{0}\nlabel:{1}".format(rule, label) )
            parser = BearLang(rule, args)
            is_match = parser.execute()
            
            print("ismatch:{0}\n".format(is_match))
            if is_match:    
                new_labels.append(label)
    return new_labels




@contextmanager
def utorrent_connection(host, username, password):
    try:
        conn = Connection(host,username,password ).utorrent( None)
    except Exception as err:
        yield None, err
    else:
        try:
            yield conn, None
        finally:
            pass




def listener(args):
    send_email( "Torrent download started",
                "Download of torrent {0} started".format(args.torrentname))  
    print("Started processing file")
    
    tempargs = vars(args)
    
    conf = CSettings(DEFAULTS, section="Torrentlabels", configfilebasename="torrentlabels.ini",initopcomments=COMMENTS)
    conf.checkSection()
    labels = conf.getSettingsAsDict()

    debug = True
    if __name__ == '__main__' or debug:
        print("\nconfiguration file is located in {0}, please modify to enable all functionality. "
          "Below is a list over parsed options from the configuration file:\n".format(conf.getSettingsFile()) )
        pprint(labels)
   
    
    new_labels = get_new_torrent_labels(labels, tempargs)
    
    #only connect to utorrent if we need to do a label change
    if new_labels and settings["webui_enable"] and intTryParse(settings["webui_enable"]) == 1:
        
        with utorrent_connection(settings["webui_host"], settings["webui_username"],  settings["webui_password"] ) as (conn, err):
            if err:
                print("Could not connect to webui, make sure webui_host, "
                      "webui_username and webui_password is correctly defined in configuration file. Error:{0}".format(err))
            else:
                print("connection to utorrent web ui ok")
                print ("got torrent '{0}' with hash {1} and tracker {2}, new_labels: {3}".format(args.torrentname, args.hash, args.tracker, new_labels) )
                
                #remove existing label
                conn.torrent_set_props( [{args.hash: {'label': ''}}])
                #set new labels
                for new_label in new_labels:    
                    conn.torrent_set_props( [{args.hash: {'label': new_label}}])    
    else:
        print("Not trying to connect to webui")


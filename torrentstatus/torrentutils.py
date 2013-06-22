#!/usr/bin/python
# -*- coding: utf-8 -*-
__version__ = '0.1'
__all__ = [
    'TorrentUtils'
]
"""This module provides utility functions for finding media files in specific directories
"""

import os, sys
import logging
import os.path
log_file = "c:\\windows\\temp\\media_finder.log"


def setup_logging():

    logger = logging.getLogger(os.path.splitext(__file__)[0] )
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s %(message)s")
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger





def log(s):
    
    if hasattr(log, "no_logging") and log.no_logging:
        return
    if not hasattr(log, "logger"):
        log.logger = setup_logging()
          
    print s
    
    log.logger.info(s)


         

def get_media_files( filedir=None, extensions=".mkv|.avi|.mp4|.mpeg"):
    if filedir is None:
        raise ValueError("filedir parameter must be set")  
    allowed_extensions = tuple(extensions.split("|"))
    #self.files = [ x for x in self.files if not os.path.exists(x.rsplit(".", 1)[0]+".srt") ]  
    #list of all media files in filedir
    return  [os.path.join(filedir, x) for x in os.listdir(filedir) if x.endswith( allowed_extensions) ]

    

    



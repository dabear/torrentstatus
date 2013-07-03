#!/usr/bin/python
# -*- coding: utf-8 -*-
__version__ = '0.1'
__all__ = [
    'utils'
]
"""This module provides utility functions for finding and manipulating media files and related metadata
"""

import os, sys
import sqlite3

from Settings import Settings

def connect_db():
    
    path = os.path.expanduser(Settings.media_db)
    dirname = os.path.dirname(path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
        
    try:
        sqlite3.enable_callback_tracebacks(True)
        conn = sqlite3.connect(path, detect_types = sqlite3.PARSE_COLNAMES) 
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Mediafiles( id INTEGER PRIMARY KEY ASC, path TEXT, added_date DATE, is_processed BOOLEAN, processed_date DATE, srt_file TEXT);
        """ )
        
        return (cursor, conn)
    except Exception as e:
        print "could not access database: {0}. Error: {1}".format(path, e)
        return (False, False)

def get_media(conn,cur):
    "returns media from database"
    cur.execute("SELECT id, path, added_date, is_processed, processed_date, srt_file FROM Mediafiles")
    for row in torrentstatus.utils.IterRows(cur):
        yield row

def IterRows(cursor, arraysize=1000):
    'An iterator that uses fetchmany to keep memory usage down'
    while True:
        results = cursor.fetchmany(arraysize)
        if not results:
            break
        for result in results:
            yield result

def has_subtitle_file(filename):
    assert os.path.exists(filename)
    base = filename.rsplit(".", 1) # spam-eggs.sausage.avi ->spam-eggs.sausage
    return os.path.exists(base + ".srt") #->spam-eggs.sausage.srt

def is_media_file(filename, extensions=".mkv|.avi|.mp4|.mpeg"):
    allowed_extensions = tuple(extensions.split("|"))
    return filename.lower().endswith( allowed_extensions)
         

def get_media_files( filedir=None):
    if filedir is None:
        raise ValueError("filedir parameter must be set")  
    #list of all media files in filedir
    return  [os.path.join(filedir, x) for x in os.listdir(filedir) if is_media_file(filename) ]

    

    



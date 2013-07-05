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

from torrentstatus.settings import settings

def connect_db():
    
    path = os.path.expanduser(settings["media_db"])
    dirname = os.path.dirname(path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
        
    try:
        sqlite3.enable_callback_tracebacks(True)
        conn = sqlite3.connect(path, detect_types=sqlite3.PARSE_COLNAMES)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Mediafiles( id INTEGER PRIMARY KEY ASC, path TEXT, added_date DATE, is_processed BOOLEAN, processed_date DATE, srt_file TEXT);
        """ )
        
        return (cursor, conn)
    except Exception as e:
        print ("could not access database: {0}. Error: {1}".format(path, e))
        return (False, False)

def get_media_list(conn,cur):
    "returns media from database"
    cur.execute("SELECT id, path, added_date, is_processed, processed_date, srt_file FROM Mediafiles")
    for row in IterRows(cur):
        yield row

def IterRows(cursor, arraysize=1000):
    'An iterator that uses fetchmany to keep memory usage down'
    while True:
        results = cursor.fetchmany(arraysize)
        if not results:
            break
        for result in results:
            yield result

def get_subtitle_info(filename, langcode=settings["sub_lang"]):
    assert os.path.exists(filename)
    if langcode:
        langcode = "." + langcode
    base = filename.rsplit(".", 1)[0] # spam-eggs.sausage.avi ->spam-eggs.sausage
    checkfile = ''.join((base, langcode, ".srt"))
    checkfile2 = ''.join((base, ".srt"))
    return (os.path.exists(checkfile) or os.path.exists(checkfil2)) , checkfile #->spam-eggs.sausage.srt

def is_media_file(filename, extensions=".mkv|.avi|.mp4|.mpeg"):
    allowed_extensions = tuple(extensions.split("|"))
    return filename.lower().endswith( allowed_extensions)
         

def get_media_files( filedir=None):
    if filedir is None:
        raise ValueError("filedir parameter must be set")  
    #list of all media files in filedir
    files = []
    for x in os.listdir(filedir):
        filename = os.path.join(filedir, x)
        if is_media_file(filename):
            files.append(filename)
    return files
    

    



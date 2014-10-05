#!/usr/bin/env python
# -*- coding: utf-8 -*-
__version__ = '0.1'
"""This module provides utility functions for finding and manipulating media files and related metadata
"""

import os
import errno
from appdirs import AppDirs
import shutil


def get_config_dir():
    dirs = AppDirs("Torrentstatus", "dabear")
    return dirs.user_data_dir


def IterRows(cursor, arraysize=1000):
    'An iterator that uses fetchmany to keep memory usage down'
    while True:
        results = cursor.fetchmany(arraysize)
        if not results:
            break
        for result in results:
            yield result


def is_media_file(filename, extensions=".mkv|.avi|.mp4|.mpeg"):
    allowed_extensions = tuple(extensions.split("|"))
    return filename.lower().endswith(allowed_extensions)


def copy(src, dest):
    print("copying {0} to {1}".format(src, dest))
    try:
        shutil.copytree(src, dest)
    except OSError as err:
        # If the error was caused because the source wasn't a directory
        if err.errno == errno.ENOTDIR:
            try:
                shutil.copy(src, dest)
            except IOError as err2:
                print('File not copied. Error: {0}'.format(str(err2) ))
                return False
        else:
            print('Directory/File not copied. Error: {0}'.format(str(err) ))
            return False
    return True


def get_media_files(filedir=None):
    if filedir is None:
        raise ValueError("filedir parameter must be set")
    #list of all media files in filedir
    files = []
    try:
        for x in os.listdir(filedir):
            filename = os.path.join(filedir, x)
            if is_media_file(filename):
                files.append(filename)
    except (OSError, IOError):
        pass

    return files

def intTryParse(value):
    try:
        val = int(value)
        return val
    except ValueError:
        return False





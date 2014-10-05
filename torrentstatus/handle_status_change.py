#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import os
import sys


from torrentstatus import utils
from torrentstatus.settings import config, get_config_dir

from yapsy.PluginManager import PluginManager
from yapsy.PluginFileLocator import PluginFileAnalyzerWithInfoFile, PluginFileLocator

##
# When running in windowed mode, stdin is fixed size.
# This redirects stdin&stderr to file, to avoid that restriction.
##
if "pythonw" in sys.executable or sys.stdin is None or sys.stderr is None:

    debugfile = utils.get_config_dir() + os.path.sep + "torrentstatus_stdout.log"
    sys.stdout = sys.stderr = open(debugfile, 'w')


##
#
# example plugin loading:
# https://github.com/headmyshoulder/stuff/blob/master/code_template/code_template.py
##
def get_plugins():
 
    plugin_analyzer = PluginFileAnalyzerWithInfoFile(name="torrentstausanalyzer", extensions="plugin-manifest")
    plugin_locator = PluginFileLocator(analyzers=[plugin_analyzer])

    extra_plugins_dir = config.getSettingsAsDict()["extra_plugins_dir"]
    plugin_extras = os.path.join(get_config_dir(), extra_plugins_dir)

    directories = [os.path.join(os.path.dirname(os.path.realpath(__file__)), "plugins")]

    ##
    ## Allow user defined plugins
    ## These plugins should be named as
    ## name.function.{py, plugin-manifest}
    ## Example:
    ## MyPlugin.onstart.py
    ## MyPlguin.onstart.plugin-manifest
    ##
    if os.path.exists(plugin_extras):
        directories.append(plugin_extras)

    manager = PluginManager(directories_list=directories, plugin_locator=plugin_locator)
    manager.collectPlugins()
    plugins = manager.getAllPlugins()

    # Activate all loaded plugins
    for pluginInfo in plugins:
        manager.activatePluginByName(pluginInfo.name)
    return plugins


def call_plugin(plugin, methodname, *args):
    try:
        #print("Calling plugin {0}'s method {1} with args {2} - {3}".format(plugin.name, methodname, plugin.details, *args))
        plugin_result = getattr(plugin.plugin_object, methodname)(plugin.details, *args)
        if plugin_result is not None:
            status = "success" if plugin_result else "error"
            print("Called plugin {0}'s method '{1}' with {2}".format(plugin.name, methodname, status) )
    except AttributeError:
        print("Call failed")
        return False
    return True


parser = argparse.ArgumentParser(description="""Process torrent status changes.
Example:
c:\python33\pythonw.exe -m torrentstatus.handle_status_change --torrentname "%N" --torrentstatus %S ^
--laststatus %P --downloadpath "%D"  --torrenttype "%K" --filename "%F" --hash "%I" --tracker "%T"
                                 """)
parser.add_argument("--torrentname", help="Ex.: Dexter.S07E10.720p.HDTV.x264-IMMERSE.mkv", required=True)
parser.add_argument("--torrentstatus", type=int, help="Current torrent status. Ex.: 5 (any value 0-12)", required=True)
parser.add_argument("--laststatus", type=int, help="Previous torrent status. Ex.: 6 (any value 0-12)", required=True)
parser.add_argument("--downloadpath", help="File path where media from torrent is downloaded to. This is used"
                                           " for downloading subtitles Ex.: H:\Other", required=True)
parser.add_argument("--filename", help="File name used when"
                                       " downloading subtitles Ex.: foo.bar.s01e01.xvid.avi", required=True)
parser.add_argument("--torrenttype", help="single|multi"
                                          " .Indicates if torrent contains a single file or multiple files",
                                          required=True)
parser.add_argument("--hash", help="Torrenthash for given torrent",
                    required=True)
parser.add_argument("--tracker", help="Tracker url for given torrent. Used to set label.",
                    required=True)
parser.add_argument('--debug', dest='debug', action='store_true')
parser.set_defaults(debug=False)
args = parser.parse_args()

statuses = ("no information", "error", "checked", "paused", "super seeding",
            "seeding", "downloading", "super seeding forced", "seeding forced",
            "downloading forced", "seeding queued", "finished", "queued",
            "stopped")


plugins = get_plugins()


# Typically, a torrent will begin with these statuses:
# from stopped (--torrentstatus 12) to queued (--torrentstatus 13):
#     --torrentname "Dexter.S07E10.720p.HDTV.x264-IMMERSE.mkv" --torrentstatus 12  --laststatus 13 --downloadpath "H:\Other"
# and then from queued (--laststatus 12) to downloading ( --torrentstatus 6 ):
#     --torrentname "Dexter.S07E10.720p.HDTV.x264-IMMERSE.mkv" --torrentstatus 6  --laststatus 12 --downloadpath "H:\Other" 
# and then from downloading (--laststatus 6) to seeding ( --torrentstatus 5 ) or finished ( --torrentstatus 11 ):
#     --torrentname "Dexter.S07E10.720p.HDTV.x264-IMMERSE.mkv" --torrentstatus 5  --laststatus 6 --downloadpath "H:\Other" 
if args.torrentname and args.torrentstatus and args.laststatus:
    currentstatus = statuses[args.torrentstatus]
    laststatus = statuses[args.laststatus]

    #
    # Onstart and Onfinish are implemented atop of the statuses provided by utorrent
    # Plugins should normally only react to these two events
    #
    if currentstatus == "downloading" or currentstatus == "downloading forced":
        #onstart.listener(args)
        #don't expand args, plugin should receive this as one parameter
        pluginmethod = "start"
    #
    # torrentstatus = "finished" might happen when download is complete OR
    # when seeding is complete. So check that utorrent last downloaded something
    elif (currentstatus == "finished" or currentstatus == "seeding") \
            and (laststatus == "downloading" or laststatus == "downloading forced"):
        pluginmethod = "finish"
    else:
        pluginmethod = currentstatus.replace(" ", "")

    #don't expand args, plugin should receive this as one parameter
    results = [call_plugin(plugin, "on" + pluginmethod, args) for plugin in plugins]

#end



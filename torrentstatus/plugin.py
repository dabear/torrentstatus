from yapsy.IPlugin import IPlugin


class iTorrentAction(IPlugin):
    def onstart(self, pluginconfig, utorrentargs):
        pass
        #print("Plugin did not implement onstart")

    def onfinish(self, pluginconfig, utorrentargs):
        pass
        #print("Plugin did not implement onfinish")
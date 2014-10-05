from torrentstatus.plugin import iTorrentAction
from torrentstatus.settings import config
import torrentstatus.utils
import os.path
from torrentstatus.utils import intTryParse

settings = config.getSettingsAsDict()


class CopyDataOnFinish(iTorrentAction):
    def onfinish(self, pluginconfig, utorrentargs):
        """Plugin to copy torrent data when a torrent has been finished

        Hardcoded at the moment, this plugin will copy multi file torrents to a subfolder,
        while single file torrents are copied to the root
        """
        if intTryParse(settings["plugin_copydata_enable"]) != 1:
            return False

        abasedir = os.path.basename(utorrentargs.downloadpath)

        if utorrentargs.torrenttype == "multi":
            path = utorrentargs.downloadpath
            path2 = os.path.join(settings["plugin_copydata_todir"], abasedir)
            return torrentstatus.utils.copy(path, path2)

        elif utorrentargs.torrenttype == "single":
        ##    #check if args.downloadpath + args.filename exists, check if it is is a media file, add it
            path = os.path.join(utorrentargs.downloadpath, utorrentargs.filename)
            path2 = os.path.join(settings["plugin_copydata_todir"], utorrentargs.filename)

            return torrentstatus.utils.copy(path, path2)
        return False

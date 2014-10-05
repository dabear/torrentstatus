from torrentstatus.plugin import iTorrentAction
from torrentstatus.notifications.email import send_email


class SendMailOnFinish(iTorrentAction):
    def onfinish(self, config, utorrentargs):
        #print("plugin SendMailOnFinish called!")
        #print("config: {0}\n args: {1}\n".format(config, utorrentargs))
        send_email("Torrent-download complete",
                   "download of torrent {0} complete".format(utorrentargs.torrentname))
        return True

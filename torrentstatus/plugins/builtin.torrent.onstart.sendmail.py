from torrentstatus.plugin import iTorrentAction
from torrentstatus.notifications.email import send_email


class SendMailOnStart(iTorrentAction):
    def onstart(self, config, utorrentargs):
        return send_email("Torrent download started",
               "Download of torrent {0} started".format(utorrentargs.torrentname))
    
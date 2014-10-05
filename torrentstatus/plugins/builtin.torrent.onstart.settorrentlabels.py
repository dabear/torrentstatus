from torrentstatus.plugin import iTorrentAction
from torrentstatus.utorrent.connection import Connection
from contextlib import contextmanager

from torrentstatus.bearlang import BearLang
from torrentstatus.settings import config, labels_config

from torrentstatus.utils import intTryParse


@contextmanager
def utorrent_connection(host, username, password):
    try:
        conn = Connection(host, username, password).utorrent(None)
    except Exception as err:
        yield None, err
    else:
        try:
            yield conn, None
        finally:
            pass


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
            parser = BearLang(rule, args)
            is_match = parser.execute()

            print("\nrule:{0}, label:{1}, ismatch: {2}\n".format(rule, label, is_match))

            if is_match:
                new_labels.append(label)
    return new_labels


settings = config.getSettingsAsDict()


class SetLabelsOnStart(iTorrentAction):
    def onstart(self, pluginconfig, utorrentargs):
        tempargs = vars(utorrentargs)

        # Use labels definition from config file and match them up against
        # provided input to the main script
        labels = labels_config.getSettingsAsDict()
        new_labels = get_new_torrent_labels(labels, tempargs)

        #only connect to utorrent if we need to do a label change
        if new_labels and intTryParse(settings["webui_enable"]) == 1:

            with utorrent_connection(settings["webui_host"],
                                     settings["webui_username"],
                                     settings["webui_password"]) as (conn, err):
                if err:
                    print("Could not connect to webui, make sure webui_host, "
                          "webui_username and webui_password is correctly "
                          "defined in configuration file. Error:{0}".format(err))
                else:
                    print("Connection to utorrent web ui ok")
                    print ("Got torrent '{0}' with hash {1} and tracker {2}. \n Setting new_labels: {3}"
                           .format(utorrentargs.torrentname, utorrentargs.hash, utorrentargs.tracker, new_labels))

                    if utorrentargs.debug:
                        print("debug mode on, not doing update")
                        return

                    #remove existing label
                    conn.torrent_set_props([{utorrentargs.hash: {'label': ''}}])
                    #set new labels
                    for new_label in new_labels:
                        conn.torrent_set_props([{utorrentargs.hash: {'label': new_label}}])
                    return True
        else:
            print("Not trying to connect to webui")
            return False

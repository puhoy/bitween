import logging
from threading import Lock
from time import time

from .torrentlist import TorrentList

logger = logging.getLogger(__name__)


class ContactList:
    def __init__(self):
        self.dict = {}
        self.lock = Lock()

    def __iter__(self):
        with self.lock:
            for x, y in self.dict:
                yield x, y.torrents_as_dict

    def get_contact(self, jid):
        if not self.dict.get(jid, False):
            self.dict[jid] = Contact(jid=jid)
        return self.dict[jid]


class Contact:
    def __init__(self, jid='', ip_v4='', ip_v6=''):
        self.jid = jid
        self.ip_v4 = ip_v4
        self.ip_v6 = ip_v6

        self.last_seen = ''

        self.torrents = TorrentList()

        self.lock = Lock()

    def set_torrents(self, torrent_dict_list):
        self.torrents = TorrentList()
        for t in torrent_dict_list:
            self.add_torrent(t['size'], t['hash'], t['name'], files=None)


    def add_torrent(self, size, sha_hash, name='', files=None):
        self.torrents.add(size=size, sha_hash=sha_hash, name=name, files=files)

    @property
    def torrents_as_dict(self):
        return self.torrents.as_dict

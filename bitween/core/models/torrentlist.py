import logging
from threading import Lock
from time import time

logger = logging.getLogger(__name__)


class Torrent:
    def __init__(self, size, sha_hash, name='', files=None):
        """

        :param size:
        :param hash:
        :param name:
        :param files:
        """
        if files is None:
            files = []
        self.hash = sha_hash
        self.name = name

        self.size = size
        self.files = files

        self.jids_lastseen = []
        # {"jid": "", "last_seen": ""}

    @property
    def as_dict(self):
        d = {"hash": self.hash,
             "name": self.name,
             "size": self.size,
             "files": self.files}
        return d


class TorrentList:
    """
    """
    def __init__(self):
        self.list = [] #  todo: this should be a dict
        self.lock = Lock()

    def add(self, size, sha_hash, name='', files=None):
        with self.lock:
            found = False
            for t in self.list:
                if t.hash == sha_hash:
                    # we have this torrent, maybe we can add a filelist or name
                    if name:
                        t.name = name
                    if files:
                        t.files = files
                    # t.jids_lastseen[jid] = time()
                    found = True
                    break

            if not found:
                t = Torrent(size, sha_hash, name=name, files=None)
                self.list.append(t)

    def __iter__(self):
        with self.lock:
            for x in self.list:
                yield x

    @property
    def as_dict(self):
        d = {}
        for t in self.__iter__():
            d[t.hash] = t.as_dict

        return d


def search(term):
    pass
